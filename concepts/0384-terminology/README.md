# 0384: Terminology And Its Governance 
- Authors: [Rieks Joosten](RieksJ@github-email) -- email is optional
- Status: [PROPOSED](/README.md#proposed)
- Since: 2020-01-16
- Status Note: experimental
- Supersedes:
- Start Date: 2019-09-06
- Tags: concept

## Summary

This document introduces a way of defining and using terms in Aries RFCs. 

## Motivation

Existing glossaries, e.g. [Sovrin Glossary V2](https://sovrin.org/wp-content/uploads/Sovrin-Glossary-V2.pdf), section 3.1 of a recent [(draft) NIST Cybersecurity White Paper](https://csrc.nist.gov/publications/detail/white-paper/2019/07/09/a-taxonomic-approach-to-understanding-emerging-blockchain-idms/draft), or the much cited [Terminology by Pfitzmann and Hansen](https://dud.inf.tu-dresden.de/literatur/Anon_Terminology_v0.34.pdf), have been quite useful to get a general understanding of SSI and related stuff. However, none of them are sufficiently precise (or comprehensive) for our (technical) purposes.

This has recently been demonstrated e.g. by the W3C thread on Identity Hubs and Agents, where [Daniel Hardman](https://lists.w3.org/Archives/Public/public-credentials/2019Aug/0087.html) proposed to develop an aligned mental model and terminology that will let us begin to tell a coherent and consistent story about hubs and agents. [Here is the proposal](https://lists.w3.org/Archives/Public/public-credentials/2019Aug/att-0087/Terminology_for_Agent_Hub-Related_Identity_Concepts.pdf).

Also, we have witnessed numerous discussions about terminology (e.g. 'Identity' is a well-known one) that were very unproductive and did not resolve any issues. The fact that the definition of various terms keeps popping up as an issue is another indicator that at least for these kinds of terms, we need to get a better grip on their definitions.

We do not intend to set up a terminology big-time. Every term that appears in it must be relevant for the work that is being done within the Aries project, and worth the effort. Terms that do not pose any difficulties need not be defined.

The purpose we aim to achieve is to increasingly improve our own understanding of what it is we are doing (getting better mental models), which would imply that software is expected to have less functional issues, and discussions that are hindered by participants using conflicting or inconsistent terms, are going to be shorter and more efficient. 
As a side-effect, an improvement of the quality of the documentation will also improve the understanding of others, which means that the software may be used wider, and there are less questions that need to be responded to.

The (obvious) downside is that it takes some discipline by those that write and use definitions.

## Tutorial [@dhh1128]

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

## Reference [@dhh1128]

Provide guidance for implementers, procedures to inform testing,
interface definitions, formal function prototypes, error codes,
diagrams, and other technical details that might be looked up.
Strive to guarantee that:

- Interactions with other features are clear.
- Implementation trajectory is well defined.
- Corner cases are dissected by example.

## Drawbacks

The (obvious) downside of doing this is that it takes some discipline by those that write and use definitions. However, when only a few will start doing this, we will be able to see the effects and we are confident that after the initial hurdle of setting things up and getting a first body of terms, the benefits will quite soon outweigh the burden of creating definitions according to this RFC.

Another drawback is that (most) users must change the way they think about terminology: rather than focussing on the specific term and from there think or discuss about what it should mean, they need to train themselves to focus on the meaning that they want to express (the disctinctions they want or need to make), and once they are clear, tag a name to it.

## Rationale and alternatives

The design of the method we propose is the best in the space of possible designs, simply because it is capable of helping solve terminological issues where traditional approaches fail. Such failures are exposed e.g. by

- discussions about terminological issues, at the end of which no, or hardly any progress has been made in resolving such issues.
- terms (such as Identity) that continuously seem to lack a good definition, in spite of having been discussed for decades.
- utterances, such as the [post by Daniel Hardman](https://lists.w3.org/Archives/Public/public-credentials/2019Aug/0087.html) that proposed to develop an aligned mental model and terminology that will let us begin to tell a coherent and consistent story about hubs and agents where at least some of the terminology already seems to exist.

We need a new approach to solve these issues that traditional approaches don't. Not coming up with a new approach simply means that the situation stays as cumbersome as it currently is (which may be acceptable when taken into account where we stand today).

The way we propose to do terminology differs from traditional ways as follows:

1. We assume every terminology to be scoped. This means that a terminology is valid/applicable within that scope, and ideally should not be applied outside that scope so as to prevent (emotional) discussions. There are many reasons for this. First, this is how it works: every person has its own personal terminology which is (only) valid for itself. Secondly, terminology that is agreed upon by multiple persons must always serve some purpose that is shared by everyone; people that do not share that purpose would not make the effort to reach such agreement. So people that are in the scope of a terminology can readily be called **stakeholders (of that terminology)**. An Aries terminology would define the terms that Aries developers (the stakeholders) agree upon and hence can rely upon as they work in pursuit of the goals of the Aries project.
2. We only allow stakeholders of a terminology to propose changes to existing definitions and to introduce new definitions to that terminology. The reason for this is that the definitions must support the goals that all stakeholders share, and while external influences may be very valuable and appreciated, we reserve the right to discard such ideas if they hinder the reaching of the goals.
3. We value the meaning of a term over the term itself. This means that *__we do not discuss whether or not a specific term has 'the correct meaning'__* (there is no such thing). Discussions may be about
    - whether or not the meaning as it is colloquially and/or formally expressed is understood in the same way by all stakeholders. If this is not the case, stakeholders will find out what meaning(s) appear to be in conflict, sort it out and create as many definitions as there are (relevant) meanings.
    - whether or not a meaning is relevant for reaching the shared goals. If it is not, it is not defined in the terminology. If it is, it will be defined.
    - what name or phrase to tack onto a meaning, so that it can then be used to refer to that meaning. We consider the choice of the name to be far less important than the formulation of the meaning we want to agree on. After all, it is the meaning of a term that helps them to understand how to best reach their common goals, not the name.

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

