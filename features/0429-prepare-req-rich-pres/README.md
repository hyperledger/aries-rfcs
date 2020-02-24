# 0429: Prerequisites to Request Rich Presentation
- Authors: [Brent Zundel](<brent.zundel@evernym.com>), [Ken Ebert](<ken@sovrin.org>)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2020-02-21
- Status Note: Part of proposed Rich Schema capabilities for credentials 
- Supersedes: 
- Start Date: 2020-02-19 
- Tags: [feature](/tags.md#feature), [rich-schemas](/tags.md#rich-schemas)

## Summary

Describes the prerequisites a verifier must ensure are in place before requesting
a rich presentation.

## Motivation

To inform verifiers of the steps they should take in order to make sure they
have the necessary rich schema objects in place before they use them to request
proofs.

## Tutorial

### Rich Schema Presentation Definition Workflow 
1. The verifier checks his wallet or the ledger to see if the presentation
definition already exists. (The verifier determines which attribute or
predicates he needs a holder to present to satisfy the verifier's business
rules. Presentation definitions specify desired attributes and predicates).
   1. If not, the verifier creates a new presentation definition and stores the
   presentation definition in his wallet locally and, optionally, anchors it to
   the verifiable data registry. (Anchoring the presentation definition to the
   verifiable data registry allows other verifiers to easily use it.)
1. Using the presentation definition, request a presentation from the holder.
The [Present Proof Protocol 1.0](https://github.com/hyperledger/aries-rfcs/tree/master/features/0037-present-proof)
will be the model for another RFC containing minor modifications for presenting
a proof based on verifiable credentials using the new rich schema objects.

![](rich_presentation_prereqs.png)

## Reference

- [RFC 0250: Rich Schema Objects](https://github.com/hyperledger/aries-rfcs/tree/master/concepts/0250-rich-schemas)
- [RFC 0420: Rich Schema Objects Common](https://github.com/hyperledger/aries-rfcs/tree/master/concepts/0420-rich-schemas-common)
- [RFC XXXX: Aries Rich Schema Presentation Definitions](https://github.com/hyperledger/aries-rfcs/tree/master/features/XXXX-rich-schema-pres-defs)
- [RFC 0037: Present Proof Protocol 1.0](https://github.com/hyperledger/aries-rfcs/tree/master/features/0037-present-proof)



## Unresolved questions

The RFC for Rich Schema Presentation Definitions is incomplete.
   
## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull
request to add your implementation. If the implementation is open source,
include a link to the repo or to the implementation within the repo. Please be
consistent in the "Name" field so that a mechanical processing of the RFCs can
generate a list of all RFCs supported by an Aries implementation.

Name / Link | Implementation Notes
--- | ---
 | 
