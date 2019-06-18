# 0051: Decentralized Key Management

>NOTE: This RFC is somewhat unusual in that it is enormously
complex and detailed. It arose out of years-long efforts by community members
to wrap their brains around how key management should be solved
without a central authority. It represents deep thinking by many
industry experts, including important voices outside the Aries
community. It is published as part of a research
grant from the US Department of Homeland Security.

- Author: Drummond Reed <drummond@connect.me> et al.
- Start Date: 2018-09-01 (approx, backdated)

## Status
- Status: [PROPOSED](/README.md#rfc-lifecycle)
- Status Date: 2019-03-29
- Status Note: Somewhat familiar to many in the community, and
  influential in the designs of other RFCs--but not yet deeply explored
  or socialized.

## Summary

Describes a general approach to key management in a decentralized,
self-sovereign world. We expect Indy to embody the principles
described here, although this doc is likely to color numerous
protocols and ecosystem features, not just to a single narrow
problem.

## Motivation

A decentralized key management system (DKMS) is an approach to cryptographic key
management where there is no central authority. DKMS leverages the security,
immutability, availability, and resiliency properties of distributed ledgers
to provide highly scalable key distribution, verification, and recovery.

Key management is vital to exercising sovereignty in a digital ecosystem,
and decentralization is a vital principle as well. Therefore, we need a
coherent and comprehensive statement of philosophy and architecture on
this vital nexus of topics.

## Tutorial

>The bulk of the content for this RFC is located in the [official architecture
documentation -- dkms-v4.md](dkms-v4.md); readers are encouraged to go there to learn more. Here
we present only the highest-level background context, for those who may but unaware
of some basics. 

#### Background Concepts
##### Key Types
DKMS uses the following key types:
1. **Master keys**: Keys that are not cryptographically protected. They are distributed manually or
initially installed and protected by procedural controls and physical or electronic isolation.
2. **Key encrypting keys**: Symmetric or public keys used for key transport or storage of other keys.
3. **Data keys**: Used to provide cryptographic operations on user data (e.g., encryption, authentication).

The keys at one level are used to protect items at a lower level. Consequently, special measures
are used to protect master keys, including severely limiting access and use, hardware protection,
and providing access to the key only under shared control.

##### Key Loss
Key loss means the owner no longer controls the key and it can assume there is no further risk of compromise. For example devices unable to function due to water, electricity, breaking, fire, hardware failure, acts of God, etc.

##### Compromise
Key compromise means that private keys and/or master keys have become or can become known either passively or actively.

##### Recovery
In decentralized identity management, recovery is important since identity owners have no “higher authority”
to turn to for recovery.
1. Offline recovery uses physical media or removable digital media to store recovery keys.
2. Social recovery employs entities trusted by the identity owner called "trustees" who store recovery data on an identity owners behalf—typically
in the trustees own agent(s).

These methods are not exclusive and should be combined with key rotation and revocation for proper security.

## Reference
1. [Design and architecture](dkms-v4.md)
2. **Public Registry for Agent Authorization Policy**. An identity owner create a policy on the ledger that defines its agents and their authorizations. 
   Agents while acting on the behalf of the identity owner need to prove that they are authorised. [More details](pdf/aap.pdf)
3. [Shamir Secret](shamir_secret.md)
4. [Trustee Protocols](trustee_protocols.md)
     

## Drawbacks, Rationale and alternatives, Prior art, Unresolved Questions

The material that's normally in these sections of a RFC appears in 
the [official architecture documentation -- dkms-v4.md](dkms-v4.md).