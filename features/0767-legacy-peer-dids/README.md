# 0767: did:legacypeer DID Method 
- Authors: Timo Glastra, [Sam Curren](telegramsam@gmail.com)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2023-02-08
- Status Note:  
- Start Date: 2018-12-26 
- Tags: [feature](/tags.md#feature)

## Summary

- The identifier part of the DID is calculated in the same way as a `did:sov` DID.
- `did:legacypeer` DIDs cannot be resolved without being provided a DID Document via the Aries Connections or DID Exchange Protocols.
- Allows transition to DIDComm v2 in read-only mode.

## Motivation

The formal definition of this legacypeer did method allows for a smooth transision between legacy aries behaviors and future technologies that are formally did spec based.

While this method cannot be fully used moving forward, it will allow adoption of newer patterns without abandoning existing connections.


## History

The unqualified DIDs in use in the Aries ecosystem originated from the [did:sov DID method](https://sovrin-foundation.github.io/sovrin/spec/did-method-spec-template.html), also in use prior to the finalization of the DID Core spec.

Some Sovrin DIDs were recorded on the ledger, but many were not. These DIDs became casually known as peer DIDs, but not in any formal sense.

Some conversation happened in the community about exchanging updates (such as key rotations), but these never materialized. Newer DID methods are designing modern approaches to this problem, and one of those methods may be useful going forward.

## Tutorial

Legacy Peer DIDs are created as detailed in the [did:sov DID Method Specification](https://sovrin-foundation.github.io/sovrin/spec/did-method-spec-template.html), with the exception that the DIDs are never recorded on any Indy ledger.

Unqualified legacy DIDs within the Aries ecosystem look like this:

`2wJPyULfLLnYTEFYzByfUR`

A convenient regex to match unqualifed DIDs is:

`^[1-9A-HJ-NP-Za-km-z]{21,22}$`


The same DID, qualified by this DID method, looks like this:

`did:legacypeer:2wJPyULfLLnYTEFYzByfUR`


Anytime you encounter a DID without a stated DID method, you can prefix it to turn it into a qualified DID.

With the adoption of this DID Method, all DIDs in the Aries ecosystem MUST be fully qualified.

Software implementations may store legacy peer DIDs in any way they choose, but any external transfer of that DID MUST be in fully qualified form.

## Resolution

Legacy Peer DIDs may only be resolved to a DID Document if the DID Document was presented using either the [Connections](https://github.com/hyperledger/aries-rfcs/blob/main/features/0160-connection-protocol/README.md) Protocol of the [DID Exchange](https://github.com/hyperledger/aries-rfcs/blob/main/features/0023-did-exchange/README.md) Protocol.



If you encounter a Legacy Peer DID for which the associated DID Document was not presented in the above mentioned protocols, there is no defined resolution method. 
   
## Transition

For `did:legacypeer` DIDs in systems that transition to DIDComm v2, there is a method of updating the DID used in a relationship. A DID may be rotated for another, even of another DID method. This allows for Legacy Peer DIDs to be transitioned to another method without disruption and without user involvement. 

This method may be used to eliminate the use of Legacy DIDs entirely via adoption of newer technologies.
	 
## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

*Implementation Notes* [may need to include a link to test results](/README.md#accepted).

Name / Link | Implementation Notes
--- | ---
 | 
