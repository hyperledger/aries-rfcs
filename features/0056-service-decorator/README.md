# 0056: Service Decorator
- Author: Sam Curren <sam@sovrin.org>, Tobias Looker <>
- Start Date: 2019-06-03

## Status
- Status: [PROPOSED](/README.md#rfc-lifecycle)
- Status Date: 2019-06-03
- Status Note: Needs refinement and validation, will be useful in any connectionless communication.

## Summary

The `~service` decorator describes a DID service endpoint inline to a message.

## Motivation

This allows messages to self contain endpoint and routing information normally in a DID Document. This comes in handy when DIDs or DID Documents have not been exchanged.

Examples include the Connect Protocol and Challenge Protocols.

The `~service` decorator on a message contains the service definition that you might expect to find in a DID Document. These values function the same way.

## Tutorial

Usage looks like this, with the contents defined the [Service Endpoint section of the DID Spec](https://w3c-ccg.github.io/did-spec/#service-endpoints):

```json=
{
    "@type": "somemessagetype",
    "~service": {
        "recipientKeys": ["8HH5gYEeNc3z7PYXmd54d4x6qAfCNrqQqEB3nS7Zfu7K"],
        "routingKeys": ["8HH5gYEeNc3z7PYXmd54d4x6qAfCNrqQqEB3nS7Zfu7K"]
        "serviceEndpoint": "https://example.com/endpoint"
    }
}
```



## Reference

The contents of the `~service` decorator are defined by the  [Service Endpoint section of the DID Spec](https://w3c-ccg.github.io/did-spec/#service-endpoints).

The decorator should not be used when the message recipient already has a service endpoint. 

## Drawbacks

The current service block definition is not very compact, and could cause problems when attempting to transfer a message via QR code.

## Rationale and alternatives

- Use of any other format would be yet a new format. Piggybacking upon the DID spec allows common logic to process the data in both places.

## Prior art

The Connect Protocol had previously included this same information as an attribute of the messages themselves. 

## Unresolved questions

- We need a way to specify types and formats for inline keys
- Does allowing multiple service type definitions make sense?
- Should we allow for pointing to a remote service block instead of including it line?
- Should we allow for the decorator to be used within an existing connection? What should the behavior be? What security vulnerabilities does this present?
