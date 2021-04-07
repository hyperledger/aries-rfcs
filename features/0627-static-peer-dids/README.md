# Aries RFC 0627: Static Peer DIDs
- Authors: [Daniel Hardman](daniel.hardman@gmail.com)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2021-04-07
- Status Note: formally freezes a set of features that have been relatively stable for about 18 months
- Start Date: 2021-03-24
- Tags: [feature](/tags.md#feature)

## Summary

Formally documents a very crisp profile of peer DID functionality that can be referenced in [Aries Interop Profiles](../../concepts/0302-aries-interop-profile/README.md).

## Motivation

The [Peer DID Spec](https://identity.foundation/peer-did-method-spec) includes a number of advanced features that are still evolving. However, a subset of its functionality is easy to implement and would be helpful to freeze for the purpose of Aries interop.

## Tutorial

### Spec version

The Peer DID method spec is still undergoing minor evolution. However, it is relatively stable, particularly in the simpler features.

This Aries RFC targets the version of the spec that is dated April 2, 2021 in its [rendered form](https://identity.foundation/peer-did-method-spec), or [github commit 202a913](https://github.com/decentralized-identity/peer-did-method-spec/commit/202a91338f18e28612724b60f3843c6f6b123226) in its source form. Note that the rendered form of the spec may update without warning, so the github commit is the better reference.

### Targeted layers

Support for peer DIDs is imagined to target configurable "layers" of interoperability:

![layers](https://identity.foundation/peer-did-method-spec/impl-layers.png)

For a careful definition of what these layers entail, please see https://identity.foundation/peer-did-method-spec/#layers-of-support.

This Aries RFC targets Layers 1 and 2. That is, code that complies with this RFC would satisfy the required behaviors for Layer 1 and for Layer 2. Note, however, that Layer 2 is broken into _accepting_ and _giving_ static peer DIDs. An RFC-compliant implementation may choose to implement either side, or both.

Support for Layer 3 (dynamic peer DIDs that have updatable state and that synchronize that state using [Sync Connection Protocol as documented in Aries RFC 0030](../0030-sync-connection/README.md)) is NOT required by this RFC. However, if there is an intent to support dynamic updates in the future, use of `numalgo` Method 1 is encouraged, as this allows static peer DIDs to acquire new state when dynamic support is added. (See next section.)

### Targeted Methods (`numalgo`)

Peer DIDs can use several different algorithms to generate the entropy that constitutes their _numeric basis_. See https://identity.foundation/peer-did-method-spec/#generation-method for details.

This RFC targets Method 0 (inception key without doc) and Method 1 (genesis doc). Code that complies with this RFC, and that intends to accept static DIDs at Layer 2a, MUST accept peer DIDs that use either method. Code that intends to give peer DIDs (Layer 2b) MUST give peer DIDs that use at least one of these two methods.

Method 2 is a promising feature of peer DIDs and will likely play a strong role in DIDComm v2, but is not a requirement for compliance with this RFC.

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

*Implementation Notes* [may need to include a link to test results](/README.md#accepted).

Name / Link | Implementation Notes
--- | ---
 | 

