# 0441: Prover and Verifier Best Practices for Proof Presentation
- Authors: [Stephen Klump](stephen.klump@becker-carroll.com)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2020-10-31
- Status Note:  See [RFC 0037](../../concepts/0037-present-proof/README.md) for the Present Proof protocol.
- Start Date: 2020-10-31
- Tags: [concept](/tags.md#concept), [credentials](/tags.md#credentials)

## Summary

This work prescribes best practices for provers in credential selection (toward proof presentation), and for verifiers in proof acceptance, in fulfilment of the Present Proof protocol [RFC0037](../../features/0037-present-proof/README.md). Of particular instance is behaviour against presentation requests and presentations in their various non-revocation interval profiles.

## Motivation

Agents should behave consistently in automatically selecting credentials and proving presentations evincing semantic ambiguity.

## Tutorial

The subsections below outline best practices for provers and verifiers.

### Presentation Requests and Non-Revocation Intervals

This section prescribes best practices in formulating and interpreting non-revocation intervals on proof requests.

A non-revocation interval contains `"from"` and `"to"` (integer) EPOCH times. For historical reasons, any timestamp within this interval is technically acceptable in a non-revocation subproof. However, these semantics allow for ambiguity in cases where revocation occurs within the interval, and in cases where the ledger supports reinstatement. These best practices obviate this equivocation, fostering deterministic outcomes.

#### Verifier Non-Revocation Interval Formulation

The verifier MUST specify, as current [INDY-HIPE 11](https://github.com/hyperledger/indy-hipe/blob/master/text/0011-cred-revocation/README.md) notes, the same integer EPOCH time for both ends of the interval. In effect, where the presentation request specifies a non-revocation interval, the verifier MUST request a non-revocation instant.

#### Prover Non-Revocation Interval Processing

In querying the nodes for revocation status, given a revocation interval on a single instant (i.e., on `"from"` and `"to"` the same), the prover MUST query the ledger for all germane revocation updates from registry creation through that instant (i.e., from zero through `"to"` value): if the credential has been revoked prior to the instant, the revocation necessarily will appear in the aggregate delta.

### Provers, Presentation Proposals, and Presentation Requests

In fulfilment of the [RFC0037](../../features/0037-present-proof/README.md) Present Proof protocol, provers may initiate with a presentation proposal or verifiers may initiate with a presentation request. In the former case, the prover has both a presentation proposal and a presentation request; in the latter case, the prover has only a presentation request.

#### With Presentation Proposal

If prover initiated the protocol with a presentation proposal specifying a value (or predicate threshold) for an attribute, and the presentation request does not require a different value for it, then the prover MUST select a credential matching the presentation proposal, in addition to following the best practices below regarding the presentation request.

#### Presentation Request

The following subsections discuss non-revocation interval applicability and prover best practices for credential selection.

##### Non-Revocation Interval Applicability to Requested Items

A non-revocation interval within a presentation request is **specifically applicable**, **generally applicable**, or **inapplicable** to a requested item (attribute or predicate).

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

##### Credential Selection Best Practices

The following subsections outline a prover's best practices in matching a credential to a requested item. Note that where a prover selects a revocable credential for inclusion, the prover MUST create a corresponding sub-proof of non-revocation at a timestamp within the non-revocation interval applicable to the requested item (insofar as possible; see [below](#timestamp-outside-non-revocation-interval)).

> **Question:** Should the prover prefer a credential that is revocable but not revoked if there is a choice between revocable credentials satisfying an applicable non-revocation interval, if the prover has a choice between credentials that are revoked and not?  Is it ever a use case to present a revoked credential to make the proof verify as false?

> **Working Hypothesis:** Provers should always prefer irrevocable credentials to revocable credentials. Presentation of an irrevocable credential constitutes proof of non-revocation.

###### Requested Item Has Specifically Applicable Non-Revocation Interval

Where a presentation request includes a non-revocation interval specifically applicable to a requested item, the prover MUST select an irrevocable credential if one satisfies; otherwise, the prover MUST select an irrevocable credential if one satisfies. If no such credential resides in the wallet, the prover MUST reject the presentation request.

> **Question:** Which is better: revocable (because the presentation request specifically asks regarding the item), or irrevocable (because it can never be revoked and hence is the most direct proof)?

> **Working Hypothesis:** Provers should always prefer irrevocable credentials to revocable credentials. Presentation of an irrevocable credential constitutes proof of non-revocation.

Note that selecting an irrevocable credential for presentation may lead to a superfluous non-revocation interval at the verifier (see [below](#superfluous-non-revocation-interval)).

###### Requested Item Has Generally Applicable Non-Revocation Interval

Where a presentation request includes a non-revocation interval generally applicable to a requested item, the prover MUST select an irrevocable credential if one satisfies; otherwise, the prover MUST select an irrevocable credential if one satisfies. If no such credential resides in the wallet, the prover MUST reject the presentation request.

> **Question:** Which is better: revocable (because the presentation request specifically asks regarding the item), or irrevocable (because it can never be revoked and hence is the most direct proof)?

> **Working Hypothesis:** Provers should always prefer irrevocable credentials to revocable credentials. Presentation of an irrevocable credential constitutes proof of non-revocation.

Note that if the presentation request includes only a generally applicable non-revocation interval but the presentation includes exclusively irrevocable credentials to satisfy all requested items, the presentation requests's non-revocation interval becomes superfluous to the presentation (see [below](#superfluous-non-revocation-interval)).

###### All Non-Revocation Intervals are Inapplicable to Requested Item

Where a presentation request's non-revocation intervals are all inapplicable to a requested item (including the case where the presentation request has no non-revocation intervals at all), the prover MUST select a matching irrevocable credential if possible. If the wallet contains only revocable credentials matching the requested item, the prover MUST reject the presentation request.

For example, consider:

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
}
```

for which the prover must select an irrevocable credential to satisfy requested attribute `"legalName"` and a revocable credential to satisfy requested attribute `"regdate"`.

> **Counterpoint:** Consider a presentation request with one requested item having a specifically applicable non-revocation interval and one with only inapplicable non-revocation intervals. If the prover may choose a revocable credential to satisfy the requested item with no applicable non-revocation interval, the proof will include a non-revocation subproof on that credential. However, if a presentation request has no non-revocation intervals at all, and the prover may select revocable credentials to satisfy its requested items, the presentation will not include a non-revocation subproof and in this way the prover may present a revoked credential to appear as valid as an irrevocable credential in a proof.

> **Question:** Would it be better to choose a default (maximally inclusive, to jibe with any other items having applicable non-revocation intervals that the revocable credential may satisfy) non-revocation interval for items having only revocable credentials but only inapplicable non-revocation intervals in the presentation?

> **Working Hypothesis:** To minimize the available surface for tamperning, provers should never assume default behaviour for non-revocation intervals beyond their `"from"` and `"to"` components (0 and present epoch respectively).

> **Question:** Is it ever appropriate to interpolate a default non-revocation interval, or does the absence of any specifically or generally applicable non-revocation interval signify an explicit expectation of an irrevocable credential? Note that any item may carry restrictions by credential definition for precise formulation.

> **Working Hypothesis:** To minimize the available surface for tamperning, provers should never assume default behaviour for non-revocation intervals as above. Since provers must prefer revocable credentials where they can, the absence of a non-revocation interval on a presentation request signifies a requirement for irrevocable credentials.

### Verifiers and Presentations

This section prescribes verifier best practices concerning a received presentation by its timestamps against the corresponding presentation request's non-revocation intervals.

#### Suspicious Timestamp

Any timestamp in the future evinces tampering: the verifier MUST reject a presentation with a future timestamp. Similarly, any timestamp predating the creation of its corresponding credential's revocation registry on the ledger evinces tampering: the verifier MUST reject a presentation with such a timestamp.

#### Superfluous Timestamp

This section outlines verifier best practices given timestamps superfluous to a presentation.

##### Timestamp for Irrevocable Credential

A presentation's inclusion of a timestamp pertaining to an irrevocable credential evinces tampering: the verifier MUST reject such a presentation.

##### Superfluous Timestamp

A verifier MUST reject a presentation including a timestamp pertaining to a revocable credential to satisfy a requested item with no applicable non-revocation interval. Any such presentation evinces tampering since, as per credential selection best practices [above](#credential-selection-best-practices), the prover MUST choose an irrevocable credential to fulfill a requested item with no applicable non-revocation interval.

For example, consider proof request:

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
                "from": 1600003000,
                "to": 1600003000
            }
        }
    },
    "requested_predicates": {
    },
}
```

against a proof presentation on a single credential

```jsonc
{
    // ...
    "identifiers": [
        {
            "schema_id": "WgWxqztrNooG92RXvxSTWv:2:sri:1.0",
            "cred_def_id": "WgWxqztrNooG92RXvxSTWv:3:CL:20:tag",
            "rev_reg_id": "WgWxqztrNooG92RXvxSTWv:4:WgWxqztrNooG92RXvxSTWv:3:CL:20:tag:CL_ACCUM:0",
            "timestamp": 1600003000
        }
    ]
}
```

is incorrect: no single (revocable) credential can satisfy both `"legalname"` and `"regdate"` requested attributes as the presentation request specifies them.

#### Missing Timestamps

A presentation with no timestamp for a revocable credential purporting to satisfy a requested item in the corresponding presentation request, where the requested item has an applicable non-revocation interval, evinces tampering: the verifier MUST reject such a presentation.

It is licit for a presentation to have no timestamp for an irrevocable credential: the corresponding non-revocation interval is superfluous in the presentation request.

> **Question:** Does the presentation of an irrevocable credential constitute proof of non-revocation over any possible non-revocation interval?

> **Working Hypothesis:** Yes.

#### Timestamp Outside Non-Revocation Interval

A presentation may include a timestamp outside of a the non-revocation interval applicable to the requested item that a presented credential purports to satisfy. If the latest timestamp from the ledger for a presented credential's revocation registry predates the non-revocation interval, but the timestamp is not in the future, the verifier MUST log and continue the proof verification process.

In all other cases where a presented timestamp falls outside the applicable non-revocation interval, the verifier MUST reject the presentation.

> **Question:**  What does logging entail, from a standards point of view?

> **Working Hypothesis:** Leave it underspecified and leave it to the implementation.

## Reference

* [RFC 0037](../../features/0037-present-proof/README.md): Present Proof protocol
* [INDY-HIPE 11](https://github.com/hyperledger/indy-hipe/blob/master/text/0011-cred-revocation/README.md): Indy revocation.
