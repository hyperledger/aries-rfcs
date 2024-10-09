# 0213: Transfer Policy Protocol

- Authors: [Sam Curren](mailto:telegramsam@gmail.com)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2019-09-03
- Status Note: Initial version
- Start Date: 2019-09-03
- Tags: [feature](/tags.md#feature), [protocol](/tags.md#protocol)

## Summary

A protocol to share and request changes to policy that relates to message transfer.

## Motivation

Explicit Policy Enables clear expectations.

## Tutorial

### Roles

**policy_holder** uses the policy to manage messages directed to the _recipient_.
**recipient** the agent the policy relates to.

## Reference

### Policy Publish

Used to share current policy by policy holder.
This can be sent unsolicited or in response to a `policy_share_request`.

```json
{
  "@id": "123456781",
  "@type": "https://didcomm.org/transferpolicy/1.0/policy",
  "queue_max_duration": 86400,
  "message_count_limit": 1000,
  "message_size_limit": 65536,
  "queue_size_limit": 65536000,
  "pickup_allowed": true,
  "delivery_retry_count_limit": 5,
  "delivery_retry_count_seconds": 86400,
  "delivery_retry_backoff": "exponential"
}
```

### Policy Share Request

Used to ask for a `policy` message to be sent.

```json
{
  "@id": "123456781",
  "@type": "https://didcomm.org/transferpolicy/1.0/policy_share_request"
}
```

### Policy Change Request

Sent to request a policy change. The expected response is a `policy` message.

```json
{
  "@id": "123456781",
  "@type": "https://didcomm.org/transferpolicy/1.0/policy_change_request",
  "queue_max_duration": 86400,
  "message_count_limit": 1000,
  "message_size_limit": 65536,
  "queue_size_limit": 65536000,
  "pickup_allowed": true,
  "delivery_retry_count_limit": 5,
  "delivery_retry_count_seconds": 86400,
  "delivery_retry_backoff": "exponential"
}
```

Only attributes that you desire to change need to be included.

## Prior art

Concepts here borrow heavily from a [document](https://hackmd.io/@8VtAqKThQ6mKa9T7JgzIaw/SJw9Ead2N?type=view) written by Andrew Whitehead of BCGov.

## Unresolved questions

- Is the attribute list too extensive for a first pass?
- Which policy attributes should be required? Which optional?

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

| Name / Link | Implementation Notes |
| ----------- | -------------------- |
|             |
