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

### Provers, Presentation Proposals, and Presentation Requests

In fulfilment of the [RFC0037](../../features/0037-present-proof/README.md) Present Proof protocol, provers may initiate with a presentation proposal or verifiers may initiate with a presentation request. In the former case, the prover has both a presentation proposal and a presentation request; in the latter case, the prover has only a presentation request.

#### With Presentation Proposal

If prover initiated the protocol with a presentation proposal specifying a value (or predicate threshold) for an attribute, the prover MUST select a credential matching the presentation proposal, in addition to following the best practices below regarding the presentation request.

#### Presentation Request

The following subsections discuss non-revocation interval applicability and prover best practices for credential selection.

##### Non-Revocation Interval Applicability to Requested Items

A non-revocation interval within a presentation request is **specifically applicable**, **generally applicable**, or **inapplicable** to a requested item (attribute or predicate).

Within a presentation request, a top-level non-revocation interval is **generally  applicable** to all requested items. A non-revocation interval defined particularly for  a requested item is **specifically applicable** to that requested attribute or predicate but **inapplicable** to all others.

A non-revocation interval specifically applicable to a requested item overrides any generally applicable non-revocation interval: no requested item may have both.

##### Credential Selection Best Practices

The following subsections outline a prover's best practices in matching a credential to a requested item. Note that where a prover selects a revocable credential for inclusion, the prover MUST create a corresponding sub-proof of non-revocation at a timestamp within the non-revocation interval applicable to the requested item (insofar as possible; see [below](#timestamp-outside-non-revocation-interval)).

> **Question:** Should the prover prefer a credential that is revocable but not revoked if there is a choice between revocable credentials satisfying an applicable non-revocation interval, if the prover has a choice between credentials that are revoked and not?  Is it ever a use case to present a revoked credential to make the proof verify as false?

###### Requested Item Has Specifically Applicable Non-Revocation Interval

Where a presentation request includes a non-revocation interval specifically applicable to a requested item, the prover MUST select a revocable credential if possible. If no such revocable credential resides in the wallet, the prover MUST reject the presentation request.

###### Requested Item Has Generally Applicable Non-Revocation Interval

Where a presentation request includes a non-revocation interval generally applicable to a requested item, the prover MUST select a revocable credential if possible. If the wallet holds only irrevocable credentials satisfying the requested item, the prover MUST select an irrevocable credential.

Note that if the presentation request includes only a generally applicable non-revocation interval but the wallet has exclusively irrevocable credentials to satisfy all requested items, the presentation requests's non-revocation interval becomes superfluous to the presentation (see [below](#superfluous-non-revocation-interval)).

###### All Non-Revocation Intervals are Inapplicable to Requested Item

Where a presentation request's non-revocation intervals are all inapplicable to a requested item (including the case where the presentation request has no non-revocation intervals at all), the prover MUST select a matching irrevocable credential if possible. If the wallet contains only revocable credentials matching the requested item, the prover MUST reject the presentation request.

> Counterpoint: Consider a presentation request with one requested item having a specifically applicable non-revocation interval and one with only inapplicable non-revocation intervals. If the prover may choose a revocable credential to satisfy the requested item with no applicable non-revocation interval, the proof will include a non-revocation subproof on that credential. However, if a presentation request has no non-revocation intervals at all, and the prover may select revocable credentials to satisfy its requested items, the presentation will not include a non-revocation subproof and in this way the prover may present a revoked credential to appear as valid as an irrevocable credential in a proof.

> Would it be better to choose a default (maximally inclusive, to jibe with any other items having applicable non-revocation intervals that the revocable credential may satisfy) non-revocation interval for items having only revocable credentials but only inapplicable non-revocation intervals in the presentation?

> **Question:** Is it ever appropriate to interpolate a default non-revocation interval, or does the absence of any specifically or generally applicable non-revocation interval signify an explicit expectation of an irrevocable credential? Note that any item may carry restrictions by credential definition for precise formulation.

### Verifiers and Presentations

This section prescribes verifier best practices concerning a received presentation by its timestamps against the corresponding presentation request's non-revocation intervals.

#### Suspicious Timestamp

Any timestamp in the future evinces tampering: the verifier MUST reject a presentation with a future timestamp. Similarly, any timestamp predating the creation of its corresponding credential's revocation registry on the ledger evinces tampering: the verifier MUST reject a presentation with such a timestamp.

#### Superfluous Timestamp

This section outlines verifier best practices given timestamps superfluous to a presentation.

##### Timestamp for Irrevocable Credential

A presentation's inclusion of a timestamp pertaining to an irrevocable credential evinces tampering: the verifier MUST reject such a presentation.

##### Timestamp for Requested Item with No Applicable Non-Revocation Interval

A presentation may include a timestamp pertaining to a revocable credential to satisfy a requested item with no specifically applicable nor generally applicable non-revocation interval. There are two possibilities:

- if the credential satisfies another requested item in the presentation request with a specifically applicable non-revocation interval, the verifier MUST continue with the proof verification process
- if the credential satisfies no requested item with a specifically applicable non-revocation interval, the timestamp evinces tampering: the verifier MUST reject the presentation.

#### Missing Timestamps

A presentation with no timestamp for a revocable credential purporting to satisfy a requested item in the corresponding proof request, where the requested item has a specifically applicable or generally applicable non-revocation interval, evinces tampering: the verifier MUST reject such a presentation.

It is licit for a presentation to have no timestamp for an irrevocable credential: the corresponding non-revocation interval is superfluous in the presentation request; see [below](#superfluous-non-revocation-interval).

> **Question:** Does the presentation of an irrevocable credential constitute proof of non-revocation over any possible non-revocation interval?

#### Superfluous Non-Revocation Interval

A presentation having no timestamp for a revocable credential purporting to satisfy a requested item in the presentation request, where the requested item has a specifically applicable or generally applicable non-revocation interval, evinces tampering: the verifier MUST reject such a presentation.

However, *ceteris paribus*, if the credential is irrevocable, its presentation constitutes proof of non-revocation over any non-revocation interval: the verifier MUST ignore the non-revocation interval for the requested item.

> **Question, as above:** Does the presentation of an irrevocable credential constitute proof of non-revocation over any possible non-revocation interval?

#### Missing Non-Revocation Interval

A presentation request's requested item having neither specifically nor generally applicable non-revocation interval, where the presentation cites a revocable credential with a timestamp to satisfy, does not necessarily evince tampering:

- if the credential additionally satisfies another requested item with a specifically applicable non-revocation interval, the verifier MUST continue with the proof verification process
- if the credential satisfies no requested item with a specifically applicable non-revocation interval, the missing non-revocation interval evinces tampering: the verifier MUST reject the presentation (see [above](#revocable-credential-for-requested-item)).

#### Timestamp Outside Non-Revocation Interval

A presentation may include a timestamp outside of a the non-revocation interval applicable to the requested item that a presented credential purports to satisfy. There are two cases:

- the ledger may not have an update as recent as the pertinent non-revocation interval, and so a timestamp may predate the non-revocation interval as long as it is not suspicious as [above](#suspicious-timestamp)
- the earliest timestamp from the ledger for a presented credential's revocation registry may postdate the non-revocation interval: in this case, creation of proof is not possible and so its inclusion evinces tampering.

Hence, the verifier MUST log and continue the proof verification process in the case of a (non-suspicious) timestamp predating its non-revocation interval in the presentation request, but MUST reject the presentation on a timestamp postdating the interval.

> **Question:**  What does logging entail, from a standards point of view?

## Reference

See [RFC 0037](../../features/0037-present-proof/README.md) for the Present Proof protocol.
