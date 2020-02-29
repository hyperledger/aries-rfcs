# Aries RFC 0056: Service Decorator

- Authors: [Sam Curren](sam@sovrin.org), Tobias Looker
- Status: [PROPOSED](/README.md#proposed)
- Since: 2019-06-03
- Status Note: Needs refinement and validation, will be useful in any connectionless communication.
- Start Date: 2019-06-03
- Tags: [feature](/tags.md#feature), [decorator](/tags.md#decorator)

## Summary

The `~service` decorator describes a DID service endpoint inline to a message.

## Motivation

This allows messages to self contain endpoint and routing information normally in a DID Document. This comes in handy when DIDs or DID Documents have not been exchanged.

Examples include the Connect Protocol and Challenge Protocols.

The `~service` decorator on a message contains the service definition that you might expect to find in a DID Document. These values function the same way.

The `~service` decorator may also be used for protocols which involve more than a simple request and response.  For example, using the `~service` decorator with the
Present Proof Protocol allows a prover to present a proof to a verifier when the prover and verifier do not have a pre-existing connection or relationship.
In this case, the `~service` decorator must be used on all messages of the Present Proof Protocol.

More generally, when a `~service` decorator is used for any single message of a protocol, the `~service` decorator MUST be present on ALL messages of that protocol.

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

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

Name / Link | Implementation Notes
--- | ---
 |  |
