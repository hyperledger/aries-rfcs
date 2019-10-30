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
allows credentials issued according to the proposed schemas to have a clear
semantic meaning, so that the verifier can know what the issuer intended.
They support explicitly typed properties and semantic inheritance. A schema
may include other schemas as property types, or extend another schema with
additional properties. For example a schema for "employee" may inherit from
the schema for "person."

## Motivation
[motivation]: #motivation

Many organizations, such as HL7 who publish the FHIR standard for heath
care data exchange, have invested time and effort into creating data
schemas that are already in use. Many schemas are shared publicly via web
sites such as https://schema.org/, whose mission is, "to create, maintain,
and promote schemas for structured data on the Internet, on web pages, in
email messages, and beyond."

These schemas ought to be usable as the basis for verifiable credentials.

Although verifiable credentials are the primary use case for schemas
considered in this document, other future uses may include defining message
formats or objects in a verifiable data registry.  

### Interoperability

Existing applications make use of schemas to organize and semantically
describe data. Using those same schemas within Aries verifiable credentials
provides a means of connecting existing applications with this emerging
technology. This allows for an easy migration path for those applications
to incorporate verifiable credentials and join the Aries ecosystem.

Aries is only one of several verifiable credentials ecosystems. Using
schemas which may be shared among these ecosystems allows for semantic
interoperability between them, and enables a path toward true multi-lateral
credential exchange.

Using existing schemas, created in accordance with widely-supported common
standards, allows Aries verifiable credentials to benefit from the decades
of effort and thought that went into those standards and to work with other
applications which also adhere to those standards.

### Re-use
Rich schemas can be re-used within the Aries credential ecosystem. Because
these schemas are hierarchical and composable, even unrelated schemas may
share partial semantic meaning due to the commonality of sub-schemas within
both. For example, a driver license schema and an employee record are not
related schemas, but both may include a person schema.

A schema that was created for a particular use-case and accepted within a
trust framework may be re-used within other trust frameworks for their
use-cases. The visibility of these schemas across trust boundaries
increases the ability of these schemas to be examined in greater detail and
evaluated for fitness of purpose. Over time the schemas will gain
reputation. 

### Extensibility
Applications that are built on top of the Aries frameworks can use these
schemas as a basis for complex data objects for use within the application,
or exposed through external APIs.

### Immutability
One important aspect of relying on schemas to provide the semantic meaning
of data within a verifiable credential, is that the meaning of the
credential properties should not change. It is not enough for entities
within the ecosystem to have a shared understanding of the data in the
present, it may be necessary for them to have an understanding of the
credential at the time it was issued and signed. This depends on the trust
framework within which the credential was issued and the needs of the
parties involved. A verifiable data registry can provide immutable storage
of schemas.

## Tutorial
[tutorial]: #tutorial

### Intro to schemas
`schema` objects are used to enforce structure and semantic meaning on a
set of data. They allow Issuers to assert, and Holders and Verifiers to
understand, a particular semantic meaning for the properties in a
credential.

Rich schemas are JSON-LD objects. Examples of the type of schemas supported
here may be found at https://schema.org/docs/schemas.html. At this time we
do not support other schema representations such as RDFS, JSON Schema, XML
Schema, OWL, etc.

### Properties
A rich schema must have an `@id` property. The value of this property must
be (or map to, via a context object) a URI. It is expected that rich
schemas stored in a verifiable data registry will be assigned a DID or
other identifier for identification within and resolution by that registry. 

The `@id` of a rich schema may be used as an additional value of the `type`
property of a verifiable credential. A [rich schema mapping](../../concepts/0250-rich-schemas/README.md#mappings)
will contain 

### Use in Verifiable Credentials

These schemas will be used in conjunction with the JSON-LD representation
of the verifiable credentials data model to specify which properties may be
included as part of the verifiable credential's `credentialSubject`
property, as well as the types of the property values.



some schema are living documents, need an immutable snapshot of which one is being used.

### Data Registry Storage
Aries-SDK will provide a means for writing `schema` objects to and reading
`schema` objects from a verifiable data registry (such as a distributed
ledger).

Why is this important?
possible alternative - anchor hash of web-based schema, just use web-based, etc.

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
    type: type of the schema
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

A possible alternative to this work has been presented by Workday

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

