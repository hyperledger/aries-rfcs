# Aries RFC ????: Aries SDK Rich Schema Schemas
- Authors: [Brent Zundel](brent.zundel@evernym.com), [Ken Ebert](ken@sovrin.org)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2019-10-??
- Status Note: Part of proposed Rich Schema capabilities for credentials 
- Supersedes: 
- Start Date: 2019-06-07 
- Tags: [feature](/tags.md#feature), [rich-schemas](/tags.md#rich-schemas)

## Summary
[summary]: #summary

The proposed schemas are [JSON-LD objects](https://json-ld.org/). This
allows credentials issued according to them to have a clear semantic
meaning, so that the verifier can know what the issuer intended. They also
support explicitly typed properties and semantic inheritance. A schema may
include other schemas as property types, or extend another schema with
additional properties. For example a schema for "employee" may inherit from
the schema for "person."

## Motivation
[motivation]: #motivation

Many organizations have invested time and effort into creating data schemas
that are already in use. Many schemas are shared publicly via web sites
such as https://schema.org/. These schemas ought to be usable as the basis
of a verifiable credential.

MORE HERE

## Tutorial
[tutorial]: #tutorial

### Intro to schemas
`schema` objects are used to enforce structure and semantic meaning on a
set of data. They allow Issuers to assert, and Holders and Verifiers to
understand, a particular semantic meaning for the properties in a
credential.

MORE HERE 

### Data Registry Storage
Aries-SDK will provide a means for writing `schema` objects to and reading
`schema` objects from a data registry (such as a distributed ledger).

### Example schema
```
"schema": {
 
 }
```

### Aries Data Registry Interface
We propose adding two Aries-Data-Registry-Interface methods for writing and
reading `schema` objects:
- `write_schema`: a method to write a `schema` object to a data registry. 
- `read_schema`: a method to read a `schema` object from a data registry.

#### write_schema
```
Writes a schema to a data registry.

#Params
submitter: {
    key: public key of the submitter,
    keystore: key manager where private key is stored
}, 
data: {
    id: identifier for the schema,
    schema: schema object,
    name: schema name string,
    version: schema version string,
    ver: version of the schema JSON format
},
registry: identifier for the registry

#Returns
registry_response: result as json,
error: {
    code: aries common error code,
    description:  aries common error description
}
```
#### read_schema
```
Reads a schema from a data registry.

#Params
submitter (optional): {
    key: public key of the submitter,
    keystore: key manager where private key is stored
}, 
id: identifier for the schema,
registry: identifier for the registry

#Returns
registry_response: schema object,
error: {
    code: aries common error code,
    description:  aries common error description
}
```

## Reference
[reference]: #reference

More information on the Verifiable Credential data model use of `schemas`
may be found [here](https://w3c.github.io/vc-data-model/#data-schemas)

## Drawbacks

There are no known drawbacks. 

## Rationale and alternatives

- A `schema` object is supported by the W3C Verifiable Credentials Data
Model specification.
- It supports rich schema capabilities for credentials.

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

