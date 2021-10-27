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

**Mediator** - The agent that has messages waiting for pickup by the _recipient_.
**Recipient** - The agent who is picking up messages.

### Flow

status can be used to see how many messages are pending. The Recipient sends a StatusRequest message to the Mediator.

Messages are retrieved when the Recipient  sends a `delivery_request` message to the Mediator.

Message delivery is confirmed with a `message_received` acknowledgement, at which point the message can be removed from the mediator's queue.

When live delivery is enabled, messages that arrive when an existing connection exists are delivered over the connection immediately.

## Reference

Each message sent should use the ~transport decorator as follows, which has been adopted from [RFC 0092 transport return route](/features/0092-transport-return-route/README.md) protocol. This has been omitted from the examples for brevity.

```json=
"~transport": {
    "return_route": "all"
}
```


### StatusRequest

Sent by the _recipient_ to the _mediator_ to request a `status` message.

```json=
{
    "@id": "123456781",
    "@type": "https://didcomm.org/messagepickup/2.0/status-request",
    "recipient_key": "<key for messages>"
}
```

- `recipient_key` is optional. When specified only return status related to that recipient key. This allows the _Recipient_ to discover if any messages are in the queue that were sent to a specific key.

### Status

Status details about pending messages

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

`message_count` is the only required attribute. The others may be present if offered by the _message_holder_.

`longest_waited_seconds` is in seconds, and is the longest delay of any message in the queue.

`total_size` is in bytes.

If a `recipient_key` was specified in the status-request message, the matching value MUST be specified in the `recipient_key` attribute of the status message.

`live_delivery` state is also indicated in the status message. 

### Delivery Request

A request from the _Recipient_ to the _Mediator_ to have waiting messages delivered. 
Examples:

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


After receipt of this message, the mediator should deliver up to the limit indicated. 

`recipient_key` is optional. When specified only return messages sent to that recipient key.

If no messages are available to be sent, a status message MUST be sent immediately.

Delivered messages MUST not be deleted until delivery is acknowledged by a `messages-received` message.


### Message Received
After receiving messages, the Recipient sends an ack message like this:
```json=
{
    "@type": "https://didcomm.org/messagepickup/2.0/messages-received",
    "message_tag_list": ["123","456"]
}
```

`message_tag_list` identifiers are tags of each message received. The tag of each message is present in the encrypted form of the message as an artifact of encryption, and is indexed by the mediator. The tag is sufficiently unique within the scope of a recipient to uniquely identify the message.

Upon receipt of this message, the `Mediator` knows that the messages have been received, and can remove them from the collection of queued messages with confidence. The mediator should send an updated `status` message reflecting the changes to the queue.

### Multiple Recipients

If a message arrives at a mediator addressed to multiple recipients, the message should be queued for each recipient independently. If one of the addressed recipients retrieves a message and indicates it has been received, that message must still be held and then removed by the other addressed recipients.

## Live Mode
Live mode is the practice of delivering newly arriving messages directly to a connected _Recipient_. It is disabled by default and only activated by the _Recipient_. Messages that arrive when Live Mode is off MUST be stored in the queue for retrieval as described above. If live mode is active, and the connection is broken, a new inbound connection starts with live mode off.

Live mode must only be enabled when a persistent transport is used, such as websockets.

_Recipients_ have three modes of possible operation for message delivery with various abilities and level of development complexity:

1. Never activate live mode. Poll for new messages with a `status_request` message, and retrieve them when available.
2. Retrieve all messages from queue, and then activate Live Mode. This simplifies message processing logic in the _Recipient_.
3. Activate Live Mode immediately upon connecting to the _Mediator_. Retrieve messages from the queue as possible. When receiving a message delivered live, the Queue may be queried for any pending messages delivered to the same key for processing.

### Live Mode Change
Live Mode is changed with a `live_delivery_change` message as follows:
```json=
{
    "@type": "https://didcomm.org/messagepickup/2.0/live_delivery_change",
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