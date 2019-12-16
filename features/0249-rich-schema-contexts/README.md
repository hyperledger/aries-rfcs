# Aries RFC 0249: Aries Rich Schema Contexts
- Authors: [Brent Zundel](brent.zundel@evernym.com), [Ken Ebert](ken@sovrin.org)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2019-10-08
- Status Note: Part of proposed Rich Schema capabilities for credentials 
- Supersedes: 
- Start Date: 2019-06-07 
- Tags: [feature](/tags.md#feature), [rich-schemas](/tags.md#rich-schemas)

## Summary
[summary]: #summary

Every rich schema object has an associated `@context`. Contexts are JSON
objects. They are the standard mechanism for defining shared semantic
meaning among rich schema objects.

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

### Data Registry Storage
Aries will provide a means for writing `@context` objects to and reading
`@context` objects from a data registry (such as a distributed ledger).

### Example context
```
"@context": [
    "did:sov:UVj5w8DRzcmPVDpUMr4AZhJ:7:example:1.0",
    "did:sov:AZKWUJ3zArXPG36kyTJZZm:7:base-context:1.0",
    "did:sov:9TDvb9PPgKQUWNQcWAFMo4:7:new-person:3.5",
    {
          "dct": "http://purl.org/dc/terms/",
          "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
          "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
          "Driver": "did:sov:35qJWkTM7znKnicY7dq5Yk:8:driver:2.4",
          "DriverLicense": "did:sov:Q6kuSqnxE57waPFs2xAs7q:8:driver-license:3.5",
          "CategoryOfVehicles": "DriverLicense:CategoryOfVehicles"
    }
]
```

### Aries Data Registry Interface
We propose adding two Aries-Data-Registry-Interface methods for writing and
reading `@context` objects:
- `write_context`: a method to write a `@context` object to a data
registry. 
- `read_context`: a method to read a `@context` object from a data
registry.

#### write_context
```
Writes a context to a data registry.

#Params
submitter: {
    key: public key of the submitter,
    keystore: key manager where private key is stored
}, 
data: {
    id: identifier for the context,
    context: context object,
    name: context name string,
    version: context version string,
    ver: version of the context JSON format
},
registry: identifier for the registry

#Returns
registry_response: result as json,
error: {
    code: aries common error code,
    description:  aries common error description
}
```
#### read_context
```
Reads a context from a data registry.

#Params
submitter (optional): {
    key: public key of the submitter,
    keystore: key manager where private key is stored
}, 
id: identifier for the context,
registry: identifier for the registry

#Returns
registry_response: context object,
error: {
    code: aries common error code,
    description:  aries common error description
}
```

## Reference
[reference]: #reference

More information on the Verifiable Credential data model use of `@context`
may be found [here](https://w3c.github.io/vc-data-model/#contexts)

More information on `@context` from the JSON-LD specification may be found
[here](https://w3c.github.io/json-ld-syntax/#the-context) and
[here](https://w3c.github.io/json-ld-syntax/#advanced-context-usage).


## Drawbacks

There are no known drawbacks. 

## Rationale and alternatives

- A `@context` object is required by the W3C Verifiable Credentials Data
Model specification.
- It also supports rich schema capabilities for credentials.

## Unresolved questions

- Is the proposed interface generic enough to support other data
registries?
- 
   
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

