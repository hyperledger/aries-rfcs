# 0441: Prover and Verifier Best Practices for Proof Presentation
- Authors: [Stephen Klump](mailto:stephen.klump@becker-carroll.com)
- Status: [ACCEPTED](/README.md#accepted)
- Since: 2021-04-15
- Status Note: Interoperability guidance when using Indy AnonCreds Present Proof. An element of the Indy AnonCreds subtarget for [AIP v2.0](../../concepts/0302-aries-interop-profile/README.md).
- Start Date: 2020-10-31
- Tags: [concept](/tags.md#concept), [credentials](/tags.md#credentials)

## Summary

This work prescribes best practices for provers in credential selection (toward proof presentation), for verifiers in proof acceptance, and for both regarding non-revocation interval semantics in fulfilment of the Present Proof protocol [RFC0037](../../features/0037-present-proof/README.md). Of particular instance is behaviour against presentation requests and presentations in their various non-revocation interval profiles.

## Motivation

Agents should behave consistently in automatically selecting credentials and proving presentations.

## Tutorial

The subsections below introduce constructs and outline best practices for provers and verifiers.

### Presentation Requests and Non-Revocation Intervals

This section prescribes norms and best practices in formulating and interpreting non-revocation intervals on proof requests.

#### Semantics of Non-Revocation Interval Presence and Absence

The presence of a non-revocation interval applicable to a requested item (see [below](#non-revocation-interval-applicability-to-requested-items)) in a presentation request signifies that the verifier requires proof of non-revocation status of the credential providing that item.

The absence of any non-revocation interval applicable to a requested item signifies that the verifier has no interest in its credential's non-revocation status.

A revocable or non-revocable credential may satisfy a presentation request with or without a non-revocation interval. The presence of a non-revocation interval conveys that if the prover presents a revocable credential, the presentation must include proof of non-revocation. Its presence does not convey any restriction on the revocability of the credential to present: in many cases the verifier cannot know whether a prover's credential is revocable or not.

#### Non-Revocation Interval Applicability to Requested Items

A **requested item** in a presentation request is an attribute or a predicate, proof of which the verifier requests presentation. A non-revocation interval within a presentation request is **specifically applicable**, **generally applicable**, or **inapplicable** to a requested item.

Within a presentation request, a top-level non-revocation interval is **generally  applicable** to all requested items. A non-revocation interval defined particularly for  a requested item is **specifically applicable** to that requested attribute or predicate but **inapplicable** to all others.

A non-revocation interval specifically applicable to a requested item overrides any generally applicable non-revocation interval: no requested item may have both.

For example, in the following (indy) proof request

```json
{
    "name": "proof-request",
    "version": "1.0",
    "nonce": "1234567890",
    "requested_attributes": {
        "legalname": {
            "name": "legalName",
            "restrictions": [
                {
                    "issuer_did": "WgWxqztrNooG92RXvxSTWv"
                }
            ]
        },
        "regdate": {
            "name": "regDate",
            "restrictions": [
                {
                    "issuer_did": "WgWxqztrNooG92RXvxSTWv"
                }
            ],
            "non_revoked": {
                "from": 1600001000,
                "to": 1600001000
            }
        }
    },
    "requested_predicates": {
    },
    "non_revoked": {
        "from": 1600000000,
        "to": 1600000000
    }
}
```

the non-revocation interval on 1600000000 is **generally applicable** to the referent `"legalname"` while the non-revocation interval on 1600001000 **specifically applicable** to referent `"regdate"`.

#### Semantics of Non-Revocation Interval Endpoints

A non-revocation interval contains `"from"` and `"to"` (integer) EPOCH times. For historical reasons, any timestamp within this interval is technically acceptable in a non-revocation subproof. However, these semantics allow for ambiguity in cases where revocation occurs within the interval, and in cases where the ledger supports reinstatement. These best practices require the `"from"` value, should the prover specify it, to equal the `"to"` value: this approach fosters deterministic outcomes.

A missing `"from"` specification defaults to the same value as the interval's `"to"` value. In other words, the non-revocation intervals

```json
{
    "to": 1234567890
}
```

and

```json
{
    "from": 1234567890,
    "to": 1234567890
}
```

are semantically equivalent.

##### Verifier Non-Revocation Interval Formulation

The verifier MUST specify, as current [INDY-HIPE 11](https://github.com/hyperledger/indy-hipe/blob/main/text/0011-cred-revocation/README.md) notes, the same integer EPOCH time for both ends of the interval, or else omit the `"from"` key and value. In effect, where the presentation request specifies a non-revocation interval, the verifier MUST request a non-revocation instant.

##### Prover Non-Revocation Interval Processing

In querying the nodes for revocation status, given a revocation interval on a single instant (i.e., on `"from"` and `"to"` the same, or `"from"` absent), the prover MUST query the ledger for all germane revocation updates from registry creation through that instant (i.e., from zero through `"to"` value): if the credential has been revoked prior to the instant, the revocation necessarily will appear in the aggregate delta.

### Provers, Presentation Proposals, and Presentation Requests

In fulfilment of the [RFC0037](../../features/0037-present-proof/README.md) Present Proof protocol, provers may initiate with a presentation proposal or verifiers may initiate with a presentation request. In the former case, the prover has both a presentation proposal and a presentation request; in the latter case, the prover has only a presentation request.

#### Credential Selection Best Practices

This section specifies a prover's best practices in matching a credential to a requested item. The specification pertains to automated credential selection: obviously, a human user may select any credential in response to a presentation request; it is up to the verifier to verify the resulting presentation as satisfactory or not.

Note that where a prover selects a revocable credential for inclusion in response to a requested item with a non-revocation interval in the presentation request, the prover MUST create a corresponding sub-proof of non-revocation at a timestamp within that non-revocation interval (insofar as possible; see [below](#timestamp-outside-non-revocation-interval)).

##### With Presentation Proposal

If prover initiated the protocol with a presentation proposal specifying a value (or predicate threshold) for an attribute, and the presentation request does not require a different value for it, then the prover MUST select a credential matching the presentation proposal, in addition to following the best practices below regarding the presentation request.

##### Preference for Irrevocable Credentials

In keeping with the specification [above](#semantics-of-non-revocation-interval-presence-and-absence), presentation of an irrevocable credential *ipso facto* constitutes proof of non-revocation. Provers MUST always prefer irrevocable credentials to revocable credentials, when the wallet has both satisfying a requested item, whether the requested item has an applicable non-revocation interval or not. Note that if a non-revocation interval is applicable to a credential's requested item in the presentation request, selecting an irrevocable credential for presentation may lead to a missing timestamp at the verifier (see [below](#missing-timestamp)).

If only revocable credentials are available to satisfy a requested item with no applicable non-revocation interval, the prover MUST present such for proof. As per [above](#semantics-of-non-revocation-interval-presence-and-absence), the absence of a non-revocation interval signifies that the verifier has no interest in its revocation status.

### Verifiers, Presentations, and Timestamps

This section prescribes verifier best practices concerning a received presentation by its timestamps against the corresponding presentation request's non-revocation intervals.

#### Timestamp for Irrevocable Credential

A presentation's inclusion of a timestamp pertaining to an irrevocable credential evinces tampering: the verifier MUST reject such a presentation.

#### Missing Timestamp

A presentation with no timestamp for a revocable credential purporting to satisfy a requested item in the corresponding presentation request, where the requested item has an applicable non-revocation interval, evinces tampering: the verifier MUST reject such a presentation.

It is licit for a presentation to have no timestamp for an irrevocable credential: the applicable non-revocation interval is superfluous in the presentation request.

#### Timestamp Outside Non-Revocation Interval

A presentation may include a timestamp outside of a the non-revocation interval applicable to the requested item that a presented credential purports to satisfy. If the latest timestamp from the ledger for a presented credential's revocation registry predates the non-revocation interval, but the timestamp is not in the future (relative to the instant of presentation proof, with a reasonable allowance for clock skew), the verifier MUST log and continue the proof verification process.

Any timestamp in the future (relative to the instant of presentation proof, with a reasonable allowance for clock skew) evinces tampering: the verifier MUST reject a presentation with a future timestamp. Similarly, any timestamp predating the creation of its corresponding credential's revocation registry on the ledger evinces tampering: the verifier MUST reject a presentation with such a timestamp.

### Dates and Predicates

This section prescribes issuer and verifier best practices concerning representing dates for use in predicate proofs (eg proving Alice is over 21 without revealing her birth date).

#### Dates in Credentials

In order for dates to be used in a predicate proof they MUST be expressed as an Int32. While unix timestamps could work for this, it has several drawbacks including: can't represent dates outside of the years 1901-2038, isn't human readable, and is overly precise in that birth time down to the second is generally not needed for an age check. To address these issues, date attributes SHOULD be represented as integers in the form YYYYMMDD (eg 19991231). This addresses the issues with unix timestamps (or any seconds-since-epoch system) while still allowing date values to be compared with < > operators. Note that this system won't work for any general date math (eg adding or subtracting days), but it will work for predicate proofs which just require comparisons. In order to make it clear that this format is being used, the attribute name SHOULD have the suffix `_dateint`. Since most datetime libraries don't include this format, [here](https://github.com/kiva/protocol-common/blob/main/src/date.conversion.ts) are some examples of helper functions written in typescript.

#### Dates in Presentations

When constructing a proof request, the verifier SHOULD express the minimum/maximum date as an integer in the form YYYYMMDD. For example if today is Jan 1, 2021 then the verifier would request that `bithdate_dateint` is before or equal to Jan 1 2000 so `<= 20000101`. The holder MUST construct a predicate proof with a YYYYMMDD represented birth date less than that value to satisfy the proof request.

## Reference

* [RFC 0037](../../features/0037-present-proof/README.md): Present Proof protocol
* [INDY-HIPE 11](https://github.com/hyperledger/indy-hipe/blob/main/text/0011-cred-revocation/README.md): Indy revocation.

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

*Implementation Notes* [may need to include a link to test results](/README.md#accepted).

Name / Link | Implementation Notes
--- | ---
 | 
