# 0211: Mediator Coordination Protocol
- Authors: [Sam Curren](mailto:telegramsam@gmail.com), [Daniel Bluhm](mailto:daniel@indicio.tech), [Adam Burdett](mailto:burdettadam@gmail.com)
- Status: [ADOPTED](/README.md#adopted)
- Since: 2024-05-01
- Status Note: Discussed and implemented and part of AIP 2.0.
- Start Date: 2019-09-03
- Tags: [feature](/tags.md#feature), [protocol](/tags.md#protocol), [test-anomaly](/tags.md#test-anomaly)

## Summary

A protocol to coordinate mediation configuration between a mediating agent and the recipient.

## Application Scope

This protocol is needed when using an edge agent and a mediator agent from different vendors. Edge agents and mediator agents from the same vendor may use whatever protocol they wish without sacrificing interoperability.

## Motivation

Use of the forward message in the Routing Protocol requires an exchange of information. The Recipient must know which endpoint and routing key(s) to share, and the Mediator needs to know which keys should be routed via this relationship.

## Protocol

**Name**: coordinate-mediation

**Version**: 1.0

**Base URI**: `https://didcomm.org/coordinate-mediation/1.0/`

### Roles

**mediator** - The agent that will be receiving `forward` messages on behalf of the _recipient_.
**recipient** - The agent for whom the `forward` message payload is intended.

### Flow
A recipient may discover an agent capable of routing using the Feature Discovery Protocol. If protocol is supported with the _mediator_ role, a _recipient_ may send a `mediate-request` to initiate a routing relationship.

First, the _recipient_ sends a `mediate-request` message to the _mediator_. If the _mediator_ is willing to route messages, it will respond with a `mediate-grant` message. The _recipient_ will share the routing information in the grant message with other contacts.

When a new key is used by the _recipient_, it must be registered with the _mediator_ to enable route identification. This is done with a `keylist-update` message.

The `keylist-update` and `keylist-query` methods are used over time to identify and remove keys that are no longer in use by the _recipient_.

## Reference

> **Note on terms:** Early versions of this protocol included the concept of
> terms for mediation.  This concept has been removed from this version due to a
> need for further discussion on representing terms in DIDComm in general and
> lack of use of these terms in current implementations.


### Mediation Request
This message serves as a request from the _recipient_ to the _mediator_, asking for the permission (and routing information) to publish the endpoint as a mediator.

```jsonc
{
    "@id": "123456781",
    "@type": "<baseuri>/mediate-request",
}
```

### Mediation Deny

This message serves as notification of the mediator denying the recipient's
request for mediation.

```jsonc
{
    "@id": "123456781",
    "@type": "<baseuri>/mediate-deny",
}
```

### Mediation Grant

A route grant message is a signal from the mediator to the recipient that permission is given to distribute the included information as an inbound route.

```jsonc
{
    "@id": "123456781",
    "@type": "<baseuri>/mediate-grant",
    "endpoint": "http://mediators-r-us.com",
    "routing_keys": ["did:key:z6Mkfriq1MqLBoPWecGoDLjguo1sB9brj6wT3qZ5BxkKpuP6"]
}
```

`endpoint`: The endpoint reported to mediation client connections.

`routing_keys`: List of keys in intended routing order. Key used as recipient of forward messages.


### Keylist Update

Used to notify the _mediator_ of keys in use by the _recipient_.

```jsonc
{
    "@id": "123456781",
    "@type": "<baseuri>/keylist-update",
    "updates":[
        {
            "recipient_key": "did:key:z6MkpTHR8VNsBxYAAWHut2Geadd9jSwuBV8xRoAnwWsdvktH",
            "action": "add"
        }
    ]
}
```

`recipient_key`: Key subject of the update.

`action`: One of `add` or `remove`.

### Keylist Update Response

Confirmation of requested keylist updates.

```jsonc
{
    "@id": "123456781",
    "@type": "<baseuri>/keylist-update-response",
    "updated": [
        {
            "recipient_key": "did:key:z6MkpTHR8VNsBxYAAWHut2Geadd9jSwuBV8xRoAnwWsdvktH",
            "action": "" // "add" or "remove"
            "result": "" // [client_error | server_error | no_change | success]
        }
    ]
}
```

`recipient_key`: Key subject of the update.

`action`: One of `add` or `remove`.

`result`: One of `client_error`, `server_error`, `no_change`, `success`; describes the resulting state of the keylist update.

### Key List Query

Query mediator for a list of keys registered for this connection.

```jsonc
{
    "@id": "123456781",
    "@type": "<baseuri>/keylist-query",
    "paginate": {
        "limit": 30,
        "offset": 0
    }
}
```

`paginate` is optional.

### Key List

Response to key list query, containing retrieved keys.

```jsonc
{
    "@id": "123456781",
    "@type": "<baseuri>/keylist",
    "keys": [
        {
            "recipient_key": "did:key:z6MkpTHR8VNsBxYAAWHut2Geadd9jSwuBV8xRoAnwWsdvktH"
        }
    ],
    "pagination": {
        "count": 30,
        "offset": 30,
        "remaining": 100
    }
}
```

`pagination` is optional.

### Encoding of keys

All keys are encoded using the [`did:key`](https://w3c-ccg.github.io/did-method-key/) method as per
[RFC0360](../0360-use-did-key/README.md).

## Prior art

There was an Indy HIPE that never made it past the PR process that described a similar approach. That HIPE led to a partial implementation of this inside the Aries Cloud Agent Python

## Future Considerations
- Should we allow listing keys by date? You could query keys in use by date?
- We are missing a way to check a single key (or a few keys) without doing a full list.
- Mediation grant supports only one endpoint. What can be done to support multiple endpoint options i.e. http, ws, etc.
- Requiring proof of key ownership (with a signature) would prevent an edge case where a malicious party registers a key for another party at the same mediator, and before the other party.
- How do we express terms and conditions for mediation?

## Unresolved questions

- None

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

Name / Link | Implementation Notes
--- | ---
[Aries Cloud Agent - Python](https://github.com/hyperledger/aries-cloudagent-python/blob/main/Mediation.md) | Added in ACA-Py 0.6.0 [MISSING test results](/tags.md#test-anomaly)****
[DIDComm mediator](https://github.com/Sirius-social/didcomm-mediator) | Open source cloud-based mediator.
