# 0212: Pickup Protocol
- Authors: [Sam Curren](telegramsam@gmail.com)
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
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/messagepickup/1.0/status_request"
}
```
### Status
Status details about pending messages
```json=
{
    "@id": "123456781",
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/messagepickup/1.0/status",
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
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/messagepickup/1.0/batch_pickup",
    "batch_size": 10
}
```

### Batch
A message that contains multiple waiting messages.
```json=
{
    "@id": "123456781",
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/messagepickup/1.0/batch",
    "messages": []
}
```
### Noop
Used to receive another message implicitly. This message has no expected behavior when received.
```json=
{
    "@id": "123456781",
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/messagepickup/1.0/noop"
}
```


## Prior art

Concepts here borrow heavily from a [document](https://hackmd.io/@8VtAqKThQ6mKa9T7JgzIaw/SJw9Ead2N?type=view) written by Andrew Whitehead of BCGov.

## Unresolved questions

- We are using multiple roles to indicate which portions of the protocol are supported by each party. This is a new thing we have not done before. Is this ok?
  
## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

Name / Link | Implementation Notes
--- | ---
 |  | 
