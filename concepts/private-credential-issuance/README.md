# 0194: How Private Individuals Can Issue Credentials
- Authors: Daniel Hardman and Lovesh Harchandani
- Status: [PROPOSED](/README.md#proposed)
- Since: 2019-12-26
- Status Note: (explanation of current status)  
- Start Date: 2019-8-26
- Tags: concept, protocol

## Summary

This document describes an approach to let private individuals issue credentials without needing to have a public DID or credential definition on the ledger but more importantly without disclosing their identity to the credential receiver or the verifier. The idea is for the private individual to anchor its identity in a public entity (DID) like an organization. The public entity issues a credential to the private individual which acts as a permission for the private individual to issue credentials on behalf of the public entity. To say it another way, the public entity is delegating the issuance capability to the private individual. The receiver of the delegated credential (from the private individual) does not learn the identity of the private individual but only learn that the public entity has allowed this private individual to issue credentials on its behalf. When such a credential is used for a proof, the verifier's knowledge of the issuer is same as the credential receiver, it only knows identity of the public entity. The contrasts the current anonymous credential scheme used by Aries where the credential receiver and proof verifier know the identity of the credential issuer. Additionally, using the same cryptographic techniques, the private individual can delegate issuance rights further, if allowed by the public entity. 

## Motivation

Letting private individuals issue credentials has 2 problems. First being that in the current anonymous credential scheme, an issuer has to have a public DID, a credential definition and optionally a revocation registry. The issuer incurs a cost (fee) in writing those to the ledger. Though it can be solved by subsidizing the writes (the techniques will vary depending on the ledger), the second problem of protecting the privacy of the issuer demands a different approach which this document specifies. Lets consider a few use cases, the first one of recommendations. When a recommendation is given as a credential and the recommender does not wish to be identified exactly but only wants to reveal that he is authorized to recommend by the platform since he is a known buyer/user of the service or a registered user, the recommender gets a credential from which he can either issue another credential for the recomendee or create a proof and whats learnt is the recommender had a credential from the platform. Another example are testomonies which are essentially attestations where the attester gives a credential specifying the attestation. Another example is of contracts between two organizations where the identities of the members actually involved in signing the contract are not revealed but still both organizations' members are convinced that members on the other side are infact members of the other organization. In general, in a lot of scenarios involving delegated actions require individuals to issue credentials without disclosing the individual's identity.
The next section will refer to these use-cases again to illustrate other details. 

## Tutorial

Since delegatable credentials are the most important primitive for this document, we first describe their 2 variations and their properties. The entity delegating the credential issuance rights and identified to the verifier is generally called the root issuer in the delegated credential literature but since this entity is the one the lets private individuals issue credentials by issuing delegatable credentials, we call it Private Credential Facilitator (PCF). On demand, a PCF is willing to issue a personal trust root (PTR) credential to any individual who requests provided that they satisfy the criterial the PCF specifies. Before moving further, it should be clarified that there are two kinds of delegatable anonymous credentials, the more efficient one which provides no privacy among the issuers but only verifiers so if Acme Corp. is the PCF and Alice requests a delegatable anonymous credential which it further delegates to Bob which further delegates to Carol. Here Carol knows the identity (a public key) of Bob and both Carol and Bob know the identity of Alice but when Carol or Bob uses its credential to create a proof and send it to the verifier, the verifier only learns about the PCF, i.e. Acme Corp. To get privacy between delegators as well, less efficient schemes exist. The choice of the scheme should depend on the situation whether privacy between delegators is required or not. The first reference is a scheme which does not allow for privacy between delegators while the second and third do.  
In the first scheme, each issuer passes on the its received credentials to the issuer it is delegating to. In the above Acme Corp., Alice, Bob and Carol example, if when Alice delegates to Bob, it gives Bob a new credential but also the credential it received from Acme Corp. 


## Reference

1. [Practical UC-Secure Delegatable Credentials with Attributes and Their Application to Blockchain](https://acmccs.github.io/papers/p683-camenischA.pdf).
2. [Delegatable Attribute-based Anonymous Credentials from Dynamically Malleable Signatures](https://eprint.iacr.org/2018/340)
3. [Delegatable Anonymous Credentials from Mercurial Signatures](https://eprint.iacr.org/2018/923)

## Drawbacks

Why should we *not* do this?

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

