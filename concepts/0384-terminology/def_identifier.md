# [Term](#_Term): Identifier


##  [Colloquial Definition](#ColloquialDefinition) 

 a text, graphic, bit-string, DID, … that a Party uses to identify some Entity with. We refer to this Party as the ‘Owner’ of the Digital Identifier’ 

##  [Formal Definition](#FormalDefinition) 

 a non-empty set of [symbols](#Symbols) (i.e. texts, graphics, bit-strings, …), that a Party (which we call the **‘Owner’ of the Identifier)** has decided to use for referring to a single Entity that it knows to exist. 

##  [Example(s)](#Examples) 

 

##  [Relevance](#Relevance) 

 the capability of a Party of reasoning and communicating about Entities requires that each of them is being attributed at least one symbol (reference, names) that together represent that entity in the context of that Party. A Party would use such attributed symbols to talk about the entity. Receiving such symbols allows a Party to find out which entity is being talked about. 

##  [Properties](#Properties) 

 A symbol(-set) can only represent an Entity (within the context of a Party) if that Party does not know about (the existence of) another Entity that has been attributed this symbol(-set). As a consequence, the term ‘Identifier’ is not a concept in its own right; it is a property that a symbol(-set) can have within the context of a specific Party.

The ultimate authority for dereferencing an Identifier (i.e. ‘translating it back’ to an Entity) is the Party that has attributed the Identifier to the Entity that it represents.

When we say that a Party is the Owner of (or: ‘owns’) an Identifier, this only means that the Party has decided to use it to represent an Entity. So the Party owns the property of being a Identifier, not necessarily the symbol(-set) itself.

| [Specializations](#Specializations) | **Digital Identifier**: a non-empty set of digital symbols (e.g. (ascii) texts, graphics, bit-strings) that is an Identifier.

**Subject Identifier**: a Digital Identifier that is used in a Claim to refer to the Subject of that Claim.

**Distributed Identifier (DID)** – a Digital Identifier [as specified by W3C](https://w3c-ccg.github.io/did-spec/).
|
##  [Pitfalls](#Pitfalls) 

 A common pitfall is to mistake an identifier for the entity that it refers to.

Another pitfall is to use a reference to an entity (e.g. the word 'Subject') where one intended to refer to an identifier for that entity (the 'Subject Identifier').

Strictly speaking, it is wrong to use the term ‘Digital Identifier’ as if it were a symbol rather than the property (of identifying an Entity within the context of some Party) of such a symbol. However, we will allow this use for as long as it does not cause any misunderstandings.

When multiple Parties use the same symbol (name) to refer to some Entity, chances are that they refer to different ones. Obvious examples are ‘Mama’, or ‘the government’. This also goes for social security numbers and the like. So, not knowing which Party is the ultimate authority for dereferencing a Digital Identifier is a pitfall.

A single Party may use multiple/different symbols as a Digital Identifier form some Entity. For example, a government agency might use a social security number, the serial number of the most recently issued passport, a DID, the attribute set {Name(s), Address, Date-of-Birth, Place-of-Birth, gender} etc. all as Digital Identifiers for a single citizen. 

##  [Related terminology](#Related) 

 Many words exist in other context that sometimes do, and sometimes don’t mean the same as what we define here. Such words include: name, identifier, identity, social security number, customer-id, citizen-id, passport, identity document, ID-card, reference. 

##  [Standards](#Standards) 

 

##  [Miscellaneous](#Miscellaneous) 

 A Digital Identifier may have the property of being persistent, which means that its owner continually ensures that this property is maintained. Parties can do this in various ways, e.g. by only assigning a symbol(set) to Entities (for the purpose of being able to later refer to that Entity) if it does not yet have the property of being a Digital Identifier.

Parties that do not use persistent Digital Identifiers may find themselves in a situation where one symbol(set) refers/applies to multiple Entities. A real-life example would be when a new person (say ‘John’) is admitted to a class and has the same name as a student that is already in the class. Such situations are often resolved by ‘renaming’ the entities (using ‘John1’ and ‘John2’ or something similar).

Decentralized Identifiers (DIDs) provide cryptographic mechanisms that allow Actors to determine whether or not some other Actor is an Agent of the DID’s Owner.

`Pairwise DIDs` is a mechanism that two Parties may use to establish a private relation between them, i.e. their mutual ability to set up secure communications links between their Agents for as long as the relation (i.e.: the DID pair) exists. This is done by first negotiating a DID pair (= registering/onboarding the relation) where each Party generates its own DID and proves to the other it has the corresponding (private) key material. Later, when Agents of both Parties connect, they can ascertain that the other is in fact an Agent of the other Party by checking that the other Agent has access to the private key material of the DIDs Owner. This is further specified in the DIDComm RFC.

See `Claim` and `Credential` for details about how Digital Identifiers are used in Claims and Credentials respectively. 


------

[[Symbols]](#Symbol) In semiotics the preferred word for this is ‘sign’. For our purposes, however, that seems a bit overkill.

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
