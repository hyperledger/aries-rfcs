# Aries RFC 0249: Aries Rich Schema Contexts
- Authors: [Brent Zundel](mailto:brent.zundel@evernym.com), [Ken Ebert](mailto:ken@sovrin.org), [Alexander Shcherbakov](mailto:alexander.shcherbakov@evernym.com)
- Status: [STALLED](/README.md#stalled)
- Since: 2024-04-03
- Status Note: No implementations have been created.
- Supersedes: 
- Start Date: 2019-06-07 
- Tags: [feature](/tags.md#feature), [rich-schemas](/tags.md#rich-schemas)

## Summary
[summary]: #summary

Every rich schema object may have an associated `@context`. Contexts are JSON or JSON-LD
objects. They are the standard mechanism for defining shared semantic
meaning among rich schema objects.


Context objects are processed in a generic way defined in 
[Rich Schema Objects Common](https://github.com/hyperledger/aries-rfcs/tree/main/concepts/0420-rich-schemas-common).

## Motivation
[motivation]: #motivation

`@context` is JSON-LD’s namespacing mechanism. Contexts allow rich schema
objects to use a common vocabulary when referring to common attributes,
i.e. they provide an explicit shared semantic meaning.

## Tutorial
[tutorial]: #tutorial

### Intro to @context
`@context` is a JSON-LD construct that allows for namespacing and the
establishment of a common vocabulary.

Context object is immutable, so it's not possible to update existing Context, 
If the Context needs to be evolved, a new Context with a new version or name needs to be created.

Context object may be stored in either JSON or JSON-LD format.

### Example Context
An example of the `content` field of a Context object:
```
{
    "@context": [
        "did:sov:UVj5w8DRzcmPVDpUMr4AZhJ",
        "did:sov:JjmmTqGfgvCBnnPJRas6f8xT",
        "did:sov:3FtTB4kzSyApkyJ6hEEtxNH4",
        {
            "dct": "http://purl.org/dc/terms/",
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
            "Driver": "did:sov:2mCyzXhmGANoVg5TnsEyfV8",
            "DriverLicense": "did:sov:36PCT3Vj576gfSXmesDdAasc",
            "CategoryOfVehicles": "DriverLicense:CategoryOfVehicles"
        }
    ]
}
```

### Data Registry Storage
Aries will provide a means for writing contexts to and reading contexts
from a verifiable data registry (such as a distributed ledger).

`@context` will be written to the ledger in a generic way defined in 
[Rich Schema Objects Common](https://github.com/hyperledger/aries-rfcs/tree/main/concepts/0420-rich-schemas-common#how-rich-schema-objects-are-stored-in-the-data-registry).

### Aries Data Registry Interface
Aries Data Registry Interface methods for adding and retrieving `@context` from the
ledger comply with the generic approach described in [Rich Schema Objects Common](https://github.com/hyperledger/aries-rfcs/tree/main/concepts/0420-rich-schemas-common#aries-data-registry-interface).

This means the following methods can be used:
- `write_rich_schema_object`
- `read_rich_schema_object_by_id`
- `read_rich_schema_object_by_metadata`


## Reference
[reference]: #reference

More information on the Verifiable Credential data model use of `@context`
may be found [here](https://w3c.github.io/vc-data-model/#contexts).

More information on `@context` from the JSON-LD specification may be found
[here](https://w3c.github.io/json-ld-syntax/#the-context) and
[here](https://w3c.github.io/json-ld-syntax/#advanced-context-usage).

- [0250: Rich Schema Objects](https://github.com/hyperledger/aries-rfcs/tree/main/concepts/0250-rich-schemas)
- [0420: Rich Schema Objects Common](https://github.com/hyperledger/aries-rfcs/tree/main/concepts/0420-rich-schemas-common) 

## Drawbacks

Requiring a `@context` for each rich schema object introduces more
complexity.

## Rationale and alternatives

- A context object is required by the W3C Verifiable Credentials Data
Model specification.
- It also supports rich schema capabilities for credentials.

## Unresolved questions
- Is the proposed interface generic enough to support other data
registries?
- We are not defining Rich Schema objects as DID DOCs for now. We may re-consider this in future once DID DOC format
is finalized.
- It may make sense to extend DID specification to include using DID for referencing Rich Schema objects.
- The proposed canonicalization form of a content to be used for DID's id-string generation is in a Draft version, so we 
may find a better way to do it.
- We don't check if the specified `@context` is valid by resolving all external links. 
 
   
## Implementations

The following lists the implementations (if any) of this RFC. Please do a
pull request to add your implementation. If the implementation is open
source, include a link to the repo or to the implementation within the
repo. Please be consistent in the "Name" field so that a mechanical
processing of the RFCs can generate a list of all RFCs supported by an
Aries implementation.

Name / Link | Implementation Notes
--- | ---
 |  | 

