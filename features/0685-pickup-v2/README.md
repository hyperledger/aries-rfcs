# 0212: Pickup Protocol 2.0

- Authors: [Sam Curren](telegramsam@gmail.com), [James Ebert](james.ebert@indicio.tech)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2019-09-03
- Status Note: Initial version
- Start Date: 2020-12-22
- Tags: [feature](/tags.md#feature), [protocol](/tags.md#protocol)

## Summary

A protocol to facilitate an agent picking up messages held at a mediator.

## Motivation

Messages can be picked up simply by sending a message to the _Mediator_ with a `return_route` decorator specified. This mechanism is implicit, and lacks some desired behavior made possible by more explicit messages.

This protocol is the explicit companion to the implicit method of picking up messages.

## Tutorial

### Roles

**Mediator** - The agent that has messages waiting for pickup by the _Recipient_.

**Recipient** - The agent who is picking up messages.

### Flow

The `status-request` message is sent by the _Recipient_ to the _Mediator_ to query how many messages are pending.

The `status` message is the response to `status-request` to communicate the state of the message queue.

The `delivery-request` message is sent by the _Recipient_ to request delivery of pending messages.

The `message-received` message is sent by the _Recipient_ to confirm receipt of delivered messages, 
prompting the _Mediator_ to clear messages from the queue.

The `live-delivery-change` message is used to set the state of `live_delivery`. 

- When Live Mode is enabled, messages that arrive when an existing connection exists are delivered over the connection immediately, 
rather than being pushed to the queue. See [Live Mode](#live-mode) for more details.

## Reference

Each message sent MUST use the `~transport` decorator as follows, which has been adopted from [RFC 0092 transport return route](/features/0092-transport-return-route/README.md) protocol. This has been omitted from the examples for brevity.

```json=
"~transport": {
    "return_route": "all"
}
```

## Message Types

### Status Request

Sent by the _Recipient_ to the _Mediator_ to request a `status` message.
#### Example:

```json=
{
    "@id": "123456781",
    "@type": "https://didcomm.org/messagepickup/2.0/status-request",
    "recipient_key": "<key for messages>"
}
```

`recipient_key` is optional. When specified, the _Mediator_ MUST only return status related to that recipient key. This allows the _Recipient_ to discover if any messages are in the queue that were sent to a specific key. You can find more details about `recipient_key` and how it's managed in [0211-route-coordination](https://github.com/hyperledger/aries-rfcs/blob/master/features/0211-route-coordination/README.md).

### Status

Status details about waiting messages.

#### Example:

```json=
{
    "@id": "123456781",
    "@type": "https://didcomm.org/messagepickup/2.0/status",
    "recipient_key": "<key for messages>",
    "message_count": 7,
    "longest_waited_seconds": 3600,
    "newest_received_time": "2019-05-01 12:00:00Z",
    "oldest_received_time": "2019-05-01 12:00:01Z",
    "total_bytes": 8096,
    "live_delivery": false
}
```

`message_count` is the only REQUIRED attribute. The others MAY be present if offered by the _Mediator_.

`longest_waited_seconds` is in seconds, and is the longest delay of any message in the queue.

`total_bytes` represents the total size of all messages.

If a `recipient_key` was specified in the `status-request` message, the matching value MUST be specified 
in the `recipient_key` attribute of the status message.

`live_delivery` state is also indicated in the status message. 

> Note: due to the potential for confusing what the actual state of the message queue
> is, a status message MUST NOT be put on the pending message queue and MUST only
> be sent when the _Recipient_ is actively connected (HTTP request awaiting
> response, WebSocket, etc.).

### Delivery Request

A request from the _Recipient_ to the _Mediator_ to have waiting messages delivered. 

#### Examples:

```json=
{
    "@id": "123456781",
    "@type": "https://didcomm.org/messagepickup/2.0/delivery-request",
    "limit": 10,
    "recipient_key": "<key for messages>"
}
```

```json=
{
    "@type": "https://didcomm.org/messagepickup/2.0/delivery-request",
    "limit": 1
}
```


`limit` is a REQUIRED attribute, and after receipt of this message, the _Mediator_ SHOULD deliver up to the `limit` indicated. 

> Note: due to the nature of HTTP, the _Mediator_ is only able to send a single message at a time, if the `delivery-request` is sent over HTTP.
> If the _Recipient_ requests more than one message over HTTP, the _Mediator_ will only be able to send one message in response. 
> This has the potential to result in seemingly unexpected behavior and is something to be aware of.

`recipient_key` is optional. When specified, the _Mediator_ MUST only return messages sent to that recipient key.

If no messages are available to be sent, a `status` message MUST be sent immediately.

Delivered messages MUST NOT be deleted until delivery is acknowledged by a `messages-received` message.

### Messages Received
After receiving messages, the _Recipient_ sends an ack message indiciating 
which messages are safe to clear from the queue.

#### Example:

```json=
{
    "@type": "https://didcomm.org/messagepickup/2.0/messages-received",
    "message_tag_list": ["123","456"]
}
```

`message_tag_list` is a list of tags of each message received. The tag of each message is present in the encrypted form of the message as an artifact of encryption, and is indexed by the mediator. The tag is sufficiently unique within the scope of a recipient to uniquely identify the message.

Upon receipt of this message, the _Mediator_ knows which messages have been received, and can remove them from the collection of queued messages with confidence. The mediator SHOULD send an updated `status` message reflecting the changes to the queue.

### Multiple Recipients

If a message arrives at a _Mediator_ addressed to multiple _Recipients_, the message MUST be queued for each _Recipient_ independently. If one of the addressed _Recipients_ retrieves a message and indicates it has been received, that message MUST still be held and then removed by the other addressed _Recipients_.

## Live Mode
Live mode is the practice of delivering newly arriving messages directly to a connected _Recipient_. It is disabled by default and only activated by the _Recipient_. Messages that arrive when Live Mode is off MUST be stored in the queue for retrieval as described above. If Live Mode is active, and the connection is broken, a new inbound connection starts with Live Mode disabled.

Messages already in the queue are not affected by Live Mode - they must still be requested with `delivery-request` messages.

Live mode MUST only be enabled when a persistent transport is used, such as WebSockets.

_Recipients_ have three modes of possible operation for message delivery with various abilities and level of development complexity:

1. Never activate live mode. Poll for new messages with a `status_request` message, and retrieve them when available.
2. Retrieve all messages from queue, and then activate Live Mode. This simplifies message processing logic in the _Recipient_.
3. Activate Live Mode immediately upon connecting to the _Mediator_. Retrieve messages from the queue as possible. When receiving a message delivered live, the queue may be queried for any waiting messages delivered to the same key for processing.

### Live Mode Change
Live Mode is changed with a `live-delivery-change` message.

#### Example:

```json=
{
    "@type": "https://didcomm.org/messagepickup/2.0/live-delivery-change",
    "live_delivery": true
}
```

Upon receiving the `live_delivery_change` message, the _Mediator_ MUST respond with a `status` message.

If sent with `live_delivery` set to `true` on a connection incapable of live delivery, a `problem_report` SHOULD be sent as follows:

```json=
{
  "@type": "https://didcomm.org/notification/1.0/problem-report",
  "~thread": {
    "pthid": "<message id of offending live_delivery_change>"
  },
  "description": "Connection does not support Live Delivery"
}
```

## Prior art

Version 1.0 of this protocol served as the main inspiration for this version. Version 1.0 suffered from not being very explicit, and an incomplete model of message delivery signaling.

## Alternatives

- An alternative to deriving a message ID is to wrap each message in a delivery wrapper. This would enable the mediator to include a mediator managed id and metadata along with the message itself, but carries the downside of double encrypting messages and extra processing.

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

Name / Link | Implementation Notes
--- | ---
 |  |
