# 0212: Pickup Protocol
- Authors: [Sam Curren](telegramsam@gmail.com), [Pavel Minenkov](minikspb@gmail.com)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2019-09-03
- Status Note: Initial version
- Start Date: 2019-09-03
- Tags: [feature](/tags.md#feature), [protocol](/tags.md#protocol)

## Summary

A protocol to coordinate routing configuration between a routing agent and the recipient.

## Motivation

Messages can be picked up simply by sending a message to the _message holder_ with a `return_route` decorator specified. This mechanism is implicit, and lacks some desired behavior made possible by more explicit messages.
This protocol is the explicit companion to the implicit method of picking up messages.

## Tutorial

### Roles

**message_holder** - The agent that has messages waiting for pickup by the _recipient_.
**recipient** - The agent who is picking up messages.
**batch_sender** - A _message_holder_ that is capable of returning messages in a `batch`.
**batch_recipient** - A _recipient_ that is capable of receiving and processing a `batch` message.

### Flow

status can be used to see how many messages are pending.
batch retrieval can be executed when many messages ...

## Reference

### StatusRequest
Sent by the _recipient_ to the _message_holder_ to request a `status` message.
```json=
{
    "@id": "123456781",
    "@type": "https://didcomm.org/messagepickup/1.0/status-request"
}
```
### Status
Status details about pending messages
```json=
{
    "@id": "123456781",
    "@type": "https://didcomm.org/messagepickup/1.0/status",
    "message_count": 7,
    "duration_waited": 3600,
    "last_added_time": "2019-05-01 12:00:00Z",
    "last_delivered_time": "2019-05-01 12:00:01Z",
    "last_removed_time": "2019-05-01 12:00:01Z",
    "total_size": 8096
}
```
`message_count` is the only required attribute. The others may be present if offered by the _message_holder_.
### Batch Pickup
A request to have multiple waiting messages sent inside a `batch` message.
```json=
{
    "@id": "123456781",
    "@type": "https://didcomm.org/messagepickup/1.0/batch-pickup",
    "batch_size": 10,
    "~timing": {
      "delay_milli": 3000
    }
}
```

`batch_size` is count of messages that **recipient** wants to retrieve

#### message timings 
[feature-0032](https://github.com/Purik/aries-rfcs/tree/0212_pickup/features/0032-message-timing)

`~timings.delay_milli` *(optional)* is timeout in milliseconds _recipient_ is ready to wait. For example, if **recipient** has set
this value to "3000ms" and batch_size has set to `5` then it says: give me all datta immediately if you have `5` messages in queue 
otherwise I'm ready to wait for "3000ms". If _message_holder_ keep in queue `message_count < 5` then it should delay response
to try to fill all requested `batch_size` in requested `~timings.delay_milli` time. 

In other words combination of `batch_size` and `~timings.delay_milli` delegate to _message_holder_ responsibility
to fill all requested `batch_size` for restricted `~timings.delay_milli` time.

Cases:
  - _message_holder_ has `10` messages in the queue. _recipient_ requested batch with `batch_size = 3`. 
    _message_holder_ will return batch with `3` messages and `7` messages continue to keep
  - _message_holder_ has `10` messages in the queue. _recipient_ requested batch with `batch_size = 30`.
    _message_holder_ will return batch with `10` messages and queue will be empty
  - _message_holder_ has `10` messages in the queue. _recipient_ requested batch with `batch_size = 30` and `~timings.delay_milli = 3000 (3000 msec)`
    _message_holder_ delay response cause of it queue has not size corresponded for `30` requesting size, suppose 
    _message_holder_ received `5` messages within `3000 msec`, so it will respond with `10+5=15` messages in response
  - _message_holder_ has `0` messages in the queue. _recipient_ requested batch with `batch_size = 30` and `~timings.delay_milli = 3000 (3000 msec)`
    _message_holder_ did not receive any messages within `3000 msec` so it will return empty messages list. 

### Batch
A message that contains multiple waiting messages.
```json=
{
    "@id": "123456781",
    "@type": "https://didcomm.org/messagepickup/1.0/batch",
    "messages~attach": [
        {
            "@id" : "06ca25f6-d3c5-48ac-8eee-1a9e29120c31",
            "message" : "{
                ...
            }"
        },

        {
            "@id" : "344a51cf-379f-40ab-ab2c-711dab3f53a9a",
            "message" : "{
                ...
            }"
        }
    ]
}
```
### Message Query With Message Id List
A request to read single or multiple messages with a message message id array.
```json=
{
    "@id": "123456781",
    "@type": "https://didcomm.org/messagepickup/1.0/list-pickup",
    "message_ids": [
        "06ca25f6-d3c5-48ac-8eee-1a9e29120c31",
        "344a51cf-379f-40ab-ab2c-711dab3f53a9a"
        ]
}
```
`message_ids` message id array for picking up messages. Any message id in `message_ids` could be delivered via several ways to the recipient (Push notification or with an envoloped message).
### Message List Query Response
A response to query with message id list.
```json=
{
    "@type": "https://didcomm.org/messagepickup/1.0/list-response",
    "messages~attach": [
        {
            "@id" : "06ca25f6-d3c5-48ac-8eee-1a9e29120c31",
            "message" : "{
                ...
            }"
        },
        {
            "@id" : "344a51cf-379f-40ab-ab2c-711dab3f53a9a",
            "message" : "{
                ...
            }"
        }
    ]
}
```
### Noop
Used to receive another message implicitly. This message has no expected behavior when received.
```json=
{
    "@id": "123456781",
    "@type": "https://didcomm.org/messagepickup/1.0/noop",
    "~timing": {
      "delay_milli": 3000
    }
}
```

It is useful to work with [Mediation flow](https://github.com/Sirius-social/didcomm-mediator/blob/main/docs/Mediation.md)
in cases when **recipient** and **batch_recipient** are same entity. **recipient** may declare it with set [`serviceEndpoint`: `didcomm:transport/queue`](https://github.com/decentralized-identity/didcomm-messaging/blob/main/extensions/return_route/main.md#queue-transport)

`~timing.delay_milli` is optional attribute


For mediator case this message is similar to `https://didcomm.org/messagepickup/1.0/batch` with `batch_size=1`
with some exception:
  - If _message_holder_ has empty queue then it will return `problem_report` with `empty_queue` problem code.
    Expected `noop` request make sense for filled queues  
  - If _message_holder_ has empty queue **BUT** _recipient_ has set `~timing.delay_milli` then _message_holder_
    will delay for `~timing.delay_milli` or less to wait incoming message. If message was received within
    specific time period, it will make response immediately else return `problem_report` with `timeout_occurred` problem code.
    In other words `~timings.delay_milli` delegate to _message_holder_ responsibility
    to try to make response within restricted `~timings.delay_milli` time.


Cases:
  - _message_holder_ has `10` messages in the queue. _recipient_. 
    _message_holder_ will make response immediately
  - _message_holder_ has `0` messages in the queue.
    _message_holder_ will return `problem_report` with `empty_queue` problem code.
  - _message_holder_ has `0` messages in the queue and _recipient_ has set `~timings.delay_milli = 3000 (3000 msec)`
    _message_holder_ did not receive any messages within `3000 msec` so it will return `problem_report` with `timeout_occurred` problem code.
  - _message_holder_ has `0` messages in the queue and _recipient_ has set `~timings.delay_milli = 3000 (3000 msec)`
    _message_holder_ received some messages after `1000 msec` so it will return immediately

    
### Problem reports & problem codes
```json=
{
    "@id": "123456781",
    "@type": "https://didcomm.org/messagepickup/1.0/problem_report",
    "problem-code": "timeout_occurred",
    "explain": "Message queue is empty, timeout occurred"
}
```
problem codes:
 - **timeout_occurred**: **message_holder** can't fill response with messages cause of message queue is empty. 
  typically, in scenarios if `~timing.delay_milli` is set
 - **empty_queue**: _message_holder_ can not process request cause of queue is empty
 - **invalid_request**: unexpected request type

## Prior art

Concepts here borrow heavily from a [document](https://hackmd.io/@8VtAqKThQ6mKa9T7JgzIaw/SJw9Ead2N?type=view) written by Andrew Whitehead of BCGov.

## Unresolved questions

- We are using multiple roles to indicate which portions of the protocol are supported by each party. This is a new thing we have not done before. Is this ok?

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

Name / Link | Implementation Notes
--- | ---
 [DIDComm mediator](https://github.com/Sirius-social/didcomm-mediator/blob/main/docs/Mediation.md#using-a-mediator) | Open source cloud-based mediator.
