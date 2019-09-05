# Title (Ex. 0000: RFC Topic)
- Authors: [Rieks Joosten](RieksJ@github-email) -- email is optional
- Status: [PROPOSED](/README.md#proposed)
- Since: 2019-09-06
- Status Note: experimental
- Supersedes:
- Start Date: 2019-09-06
- Tags: concept

## Summary

This document introduces a way of defining and using terms in Aries RFCs. 

## Motivation

Existing glossaries, e.g. [Sovrin Glossary V2](https://sovrin.org/wp-content/uploads/Sovrin-Glossary-V2.pdf), section 3.1 of a recent [(draft) NIST Cybersecurity White Paper](https://csrc.nist.gov/publications/detail/white-paper/2019/07/09/a-taxonomic-approach-to-understanding-emerging-blockchain-idms/draft), or the much cited [Terminology by Pfitzmann and Hansen](https://dud.inf.tu-dresden.de/literatur/Anon_Terminology_v0.34.pdf), have been quite useful to get a general understanding of SSI and related stuff. However, none of them are sufficiently precise (or comprehensive) for our (technical) purposes.

This has recently been demonstrated e.g. by the W3C thread on Identity Hubs and Agents, where [Daniel Hardman](https://lists.w3.org/Archives/Public/public-credentials/2019Aug/0087.html) proposed to develop an aligned mental model and terminology that will let us begin to tell a coherent and consistent story about hubs and agents. [Here is the proposal](https://lists.w3.org/Archives/Public/public-credentials/2019Aug/att-0087/Terminology_for_Agent_Hub-Related_Identity_Concepts.pdf)

The purpose we aim to achieve is to increasingly improve our own understanding of what it is we are doing (getting better mental models), which would imply that software is expected to have less functional issues, and discussions that are hindered by participants using conflicting or inconsistent terms, are going to be shorter and more efficient. 
As a side-effect, an improvement of the quality of the documentation will also improve the understanding of others, which means that the software may be used wider, and there are less questions that need to be responded to.

The (obvious) downside is that it takes some discipline by those that write and use definitions.

## Tutorial

Explain the proposal as if it were already implemented and you
were teaching it to another Aries contributor or Aries consumer. That generally
means:

- Introducing new named concepts.
- Explaining the feature largely in terms of examples.
- Explaining how Aries contributors and/or consumers should *think* about the
feature, and how it should impact the way they use the ecosystem.
- If applicable, provide sample error messages, deprecation warnings, or
migration guidance.

Some enhancement proposals may be more aimed at contributors (e.g. for
consensus internals); others may be more aimed at consumers.

## Reference

Provide guidance for implementers, procedures to inform testing,
interface definitions, formal function prototypes, error codes,
diagrams, and other technical details that might be looked up.
Strive to guarantee that:

- Interactions with other features are clear.
- Implementation trajectory is well defined.
- Corner cases are dissected by example.

## Drawbacks

The (obvious) downside of doing this is that it takes some discipline by those that write and use definitions. However, when only a few will start doing this, we will be able to see the effects and we are confident that after the initial hurdle of setting things up and getting a first body of terms, the benefits will quite soon outweigh the burden of creating definitions according to this RFC.

## Rationale and alternatives

- Why is this design the best in the space of possible designs?
- What other designs have been considered and what is the rationale for not
choosing them?
- What is the impact of not doing this?

## Prior art

Discuss prior art, both the good and the bad, in relation to this proposal.
A few examples of what this can include are:

- Does this feature exist in other SSI ecosystems and what experience have
their community had?
- For other teams: What lessons can we learn from other attempts?
- Papers: Are there any published papers or great posts that discuss this?
If you have some relevant papers to refer to, this can serve as a more detailed
theoretical background.

This section is intended to encourage you as an author to think about the
lessons from other implementers, provide readers of your proposal with a
fuller picture. If there is no prior art, that is fine - your ideas are
interesting to us whether they are brand new or if they are an adaptation
from other communities.

Note that while precedent set by other communities is some motivation, it
does not on its own motivate an enhancement proposal here. Please also take
into consideration that Aries sometimes intentionally diverges from common
identity features.

## Unresolved questions

- What parts of the design do you expect to resolve through the
enhancement proposal process before this gets merged?
- What parts of the design do you expect to resolve through the
implementation of this feature before stabilization?
- What related issues do you consider out of scope for this 
proposal that could be addressed in the future independently of the
solution that comes out of this doc?
   
## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

Name / Link | Implementation Notes
--- | ---
 |  | 

