# [Term](#_Term): Identity (of an Entity, for some Party)

| | |
| --- | --- |
| [Colloquial Definition](#ColloquialDefinition) | everything that a Party knows about some Entity |
| [Formal Definition](#FormalDefinition) | the set of all characteristics and/or statements about an Entity that a specific Party knows (has stored somewhere) |
| [Example(s)](#Examples) | The identity of you for your father is everything your father knows about you. The identity of you for your self is everything you know about yourself. The identity of you for your government is everything your government knows about you. The identity of your father/government for you is everything you know about your father/government. |
| [Relevance](#Relevance) | The knowledge that a Party has about some entity determines the ways in which it interacts with that Entity. Such knowledge allows the Party to assess how it may use that Entity, how it can benefit from interacting with it or whether it better stay away, etc.<br>Digitally storing (part of) this knowledge allows the Party to manage its relation with that Entity, and to digitally interact with that Entity (if it has such capabilities).
We also need it because a trustworthy Party would only issue Claims about an Entity when that is part of its Digital Identity, and revoke any Verifiable Credentials when they contain data that is no longer congruent with the Digital Identity.|
| [Properties](#Properties) | A Party that has stored some Digital Identity considers all the characteristics and/or statements about the associated Entity to be true. |
| [Specializations](#Specializations) | **Digital Identity** – all knowledge of a Party about some Entity that is digitally stored. |
| [Pitfalls](#Pitfalls) | |
| [Related terminology](#Related) | Others may call this a ‘Partial Digital Identity’, because it is limited to the knowledge of one Party, and the (Total) Digital Identity of an Entity would then be the union of the Digital Identities of that Entity over all Parties.<br><br>The last [paper of Pfitzmann and Hansen](https://dud.inf.tu-dresden.de/literatur/Anon_Terminology_v0.34.pdf) has a terminology for talking about privacy by data minimization that specifies this and related terms.<br><br>Many words exist in non-tech context that sometimes do, and sometimes don’t mean the same as what we define here. Such words include: name, identifier, identity, social security number, customer-id, citizen-id, passport, identity document, ID-card, credential, reference. |
| [Standards](#Standards) | |
| [Miscellaneous](#Miscellaneous) | The quality of the processes for registering and maintaining the knowledge about an Entity obviously determine the Level of Assurance (LoA) of the (Digital) Identity of that Entity, and by consequence of any Claims or Credentials that are issued based on that.<br><br>Claims about an Entity should (but theoretically need not) reflect a part of that Entities Digital Identity. Ideally, a Claim (that has been issued as part of a Credential) should be revoked at the moment that the Party detects that it no longer accurately reflects the corresponding part of the Digital Identity. Every Party that consequently does this thereby guarantees that every Claim (in any Credential) accurately represents the corresponding part of the Digital Identity, provided that it is verified that (a) it has been issued by that Party, (b) it has not been modified since it was issued, (c) it has not expired and (d) it has not been revoked. This is a very powerful guarantee to be able to provide.<br><br>Some people consider the Identity (of an Entity) to consist of all knowledge that all Parties (including the Entity itself if it happens to be a Party) have about that Entity – i.e. the union of every Digital Identity (of that Entity). This is not very useful for us, because such an Identity cannot be (technically) constructed." |

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
