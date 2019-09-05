# [Term](#_Term): Claim (about an Entity, by a Party)

| | |
| --- | --- |
| [Colloquial Definition](#ColloquialDefinition) |an artefact, that is created by or on behalf of a Party (called the **issuer of the Claim**), representing one or more characteristics and/or statements about a single Entity (called the **Subject of the Claim**). |
| [Formal Definition](#FormalDefinition) | an artefact, that is created by or on behalf of a Party, representing one or more characteristics and/or statements about a single Entity.|
| [Example(s)](#Examples) | |
| [Relevance](#Relevance) | In order for a Party to reason or communicate about (characteristics of) an Entity, it needs a way to represent the relevant information (knowledge). Claims are the basic elements for reasoning or communicating with – very much like sentences (in linguistics), or propositions and predicates (in logic).|
| [Properties](#Properties) | Every Claim either represents a part of the Identity of an Entity within the context of a specific Party, or represents a lie by that Party. |
| [Specializations](#Specializations) |**Digital Claim**: a Claim that has a digital representation, i.e. can be stored and transferred through digital means.<br><br>**Attribute**: a Claim, that implicitly identifies its Subject, and further consists of a key-value pair, where the ‘key’ is an Identifier for the semantics of both the Claim (in the scope of its issuer) and the (optional) value.<br><br>**Verifiable Claim**: a Claim for which a proof is present by which Parties other than the issuer can determine the provenance of the Claim and whether or not the Claim has been modified since the proof was generated. |
| [Pitfalls](#Pitfalls) | A Claim does not imply truth, first because truth is subjective, and a Party that relies on a Claim (being truthful) may have other ideas about truth than the issuer of the Claim, and secondly because parties may lie, i.e. issue claims that do not represent what they themselves consider to be true. This implies that Parties that rely on other Parties to provide verifiable claims that represent (their) truth must do some vetting of that other Party to determine whether or not that other Party is sufficiently trustworthy.<br><br>A Claim must refer to its Subject, i.e. the Entity about which the Claim is made. This implies that each claim must contain a Digital Identifier (called the Subject Identifier) that refers to the Subject of the Claim. The Subject Identifier (i.e.: the identifying property – see the definition of ‘Digital Identity’) must be owned by the Party that issues the Claim. Note that this permits that the Subject Identifier symbol itself is created by another Party.|
| [Related terminology](#Related) | Many words exist in non-tech context that sometimes do, and sometimes don’t mean the same as what we define here. Such words include: statement, assertion, attestation. |
| [Standards](#Standards) | |
| [Miscellaneous](#Miscellaneous) | Claims about an Entity should (but theoretically need not) reflect a part of that Entities Digital Identity. Ideally, a Claim (that has been issued as part of a Credential) should be revoked at the moment that the Party detects that it no longer accurately reflects the corresponding part of the Digital Identity. Every Party that consequently does this thereby guarantees that every Claim (in any Credential) accurately represents the corresponding part of the Digital Identity, provided that it is verified that (a) it has been issued by that Party, (b) it has not been modified since it was issued, (c) it has not expired and (d) it has not been revoked. This is a very powerful guarantee to be able to provide. |

------

[[Term]](#Term) The word or phrase that is being defined. If the defined word depends on other concepts, make this a phrase that includes such concepts, as in: Identity (of an Entity).

[[Colloquial Definition]](#ColloquialDefinition) a non-authoritative description of the term that provides the casual reader with a rough idea about the meaning of the term.

[[Formal Definition]](#FormalDefinition) provide a statement (as formal as possible) that allows readers to determine whether or not something is an instance of the term, formulated in such a way that the likelihood that any two readers (that belong to the intended audience of this document) conclude differently in the same case, is minimized.

[[Example(s)]](#Examples) give one or two examples of the term/phrase that readers can think about when reading the other definition texts so as to help them understand it.

[[Relevance]](#Relevance) describe the relevance of having the definition, thus providing purpose to having it.

[[Properties]](#Properties) further elaboration of the term, listing properties that an instance of the term must, should, or may have, and that are important for a reader to be aware of.

[[Specializations]](#Specializations) (optional) field, where you can identify any other term that is a specializatios of the defined term, and provide criteria that allows the user to determine whether or not something that qualifies as an instance of the term also qualifies as such a specialization.

[[Pitfalls]](#Pitfalls) identify pitfalls that users have been known to fall into when applying the term (within its scope), implicitly warning the users to avoid that.

[[Related terminology]](#Related) mention relations that this term may have with terms that readers might (commonly) use in other contexts, such as, for example, W3C contexts.

[[Standards]](#Standards) reference(s) to standards documents that define the term in sufficiently the same way. Standards that define the term in a different way may be listed under ‘Pitfalls’.

[[Miscellaneous]](#Miscellaneous1) any other texts that may be relevant for most readers.
