# Aries RFC 0281: Aries Rich Schemas
- Authors: [Brent Zundel](mailto:mailto:brent.zundel@evernym.com), [Ken Ebert](mailto:mailto:ken@sovrin.org), [Alexander Shcherbakov](mailto:mailto:alexander.shcherbakov@evernym.com)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2019-10-30
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

Schema objects are processed in a generic way defined in 
[Rich Schema Objects Common](https://github.com/hyperledger/aries-rfcs/tree/main/concepts/0420-rich-schemas-common).

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

### Intro to Schemas
`schema` objects are used to enforce structure and semantic meaning on a
set of data. They allow Issuers to assert, and Holders and Verifiers to
understand, a particular semantic meaning for the properties in a
credential.

Rich schemas are JSON-LD objects. Examples of the type of schemas supported
here may be found at [schema.org](https://schema.org/docs/schemas.html). At this time we
do not support other schema representations such as RDFS, JSON Schema, XML
Schema, OWL, etc.

### Properties
Rich Schema properties follow the generic template defined in
[Rich Schema Common](https://github.com/hyperledger/aries-rfcs/tree/main/concepts/0420-rich-schemas-common#how-rich-schema-objects-are-stored-in-the-data-registry).

Rich Schema's `content` field is a JSON-LD-serialized string with the following fields:

#### @id
A rich schema must have an `@id` property. The value of this property must
be equal to the `id` field which is a DID (see [Identification of Rich Schema Objects](https://github.com/hyperledger/aries-rfcs/tree/main/concepts/0420-rich-schemas-common#identification-of-rich-schema-objects)). 

A [rich schema](README.md) may refer to the `@id` of another rich schema to
define a parent schema. A property of a rich schema may use the `@id` of
another rich schema as the value of its `@type` or `@id` property.

A [mapping object](../../concepts/0250-rich-schemas/README.md#mappings)
will contain the `@id` of the rich schema being mapped.

A [presentation definition](../../concepts/0250-rich-schemas/README.md#presentation-definitions)
will contain the `@id` of any schemas a holder may use to present proofs to
a verifier.

#### @type
A rich schema must have a `@type` property. The value of this property must
be (or map to, via a context object) a URI. 

#### @context
A rich schema may have a `@context` property. If present, the value of this
property must be a
[context object](../0249-rich-schema-contexts/README.md) or a URI which can
be dereferenced to obtain a context object.

### Use in Verifiable Credentials
These schemas will be used in conjunction with the JSON-LD representation
of the verifiable credentials data model to specify which properties may be
included as part of the verifiable credential's `credentialSubject`
property, as well as the types of the property values.

The `@id` of a rich schema may be used as an additional value of the 
[type property](https://www.w3.org/TR/vc-data-model#types) property of a
verifiable credential. Because the `type` values of a verifiable credential
are not required to be dereferenced, in order for the rich schema to
support assertion of the structure and semantic meaning of the claims in
the credential, an additional reference to the rich schema should be made
through the 
[credentialSchema](https://www.w3.org/TR/vc-data-model#data-schemas)
property. This may be done as a direct reference to the rich schema `@id`,
or via another rich schema object which references the rich schema `@id`
such as a 
[credential definition](../../concepts/0250-rich-schemas/README.md#credential-definitions) 
as would 
[be the case](https://www.w3.org/TR/vc-data-model#zero-knowledge-proofs) 
for anonymous credentials, as discussed in the
[mapping section](../../concepts/0250-rich-schemas/README.md#mappings) of
the rich schema overview RFC.

### Data Registry Storage
Aries will provide a means for writing `schema` objects to and reading
`schema` objects from a verifiable data registry (such as a distributed
ledger).

As discussed [previously](#immutability), the ability to specify the exact
schema that was used to issue a verifiable credential, and the assurance 
that the meaning of that schema has not changed, may be critical for the
trust framework. Verifiable data registries which provide immutability
guarantees provide this assurance. Some alternative storage mechanisms do
not. Hashlinks, which may be used to verify the hash of web-based schemas,
are one example. These can be used inform a verifier that a schema has
changed, but do not provide access to the original version of the schema in
the event the original schema has been updated.

### Example Schema
An example of the `content` field of a Rich Schema object:
```
   "@id": "did:sov:2f9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
   "@type": "rdfs:Class",
   "@context": {
    "schema": "http://schema.org/",
    "bibo": "http://purl.org/ontology/bibo/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "dcat": "http://www.w3.org/ns/dcat#",
    "dct": "http://purl.org/dc/terms/",
    "dcterms": "http://purl.org/dc/terms/",
    "dctype": "http://purl.org/dc/dcmitype/",
    "eli": "http://data.europa.eu/eli/ontology#",
    "foaf": "http://xmlns.com/foaf/0.1/",
    "owl": "http://www.w3.org/2002/07/owl#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfa": "http://www.w3.org/ns/rdfa#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "schema": "http://schema.org/",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "snomed": "http://purl.bioontology.org/ontology/SNOMEDCT/",
    "void": "http://rdfs.org/ns/void#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "xsd1": "hhttp://www.w3.org/2001/XMLSchema#"
  },
  "@graph": [
    {
      "@id": "schema:recipeIngredient",
      "@type": "rdf:Property",
      "rdfs:comment": "A single ingredient used in the recipe, e.g. sugar, flour or garlic.",
      "rdfs:label": "recipeIngredient",
      "rdfs:subPropertyOf": {
        "@id": "schema:supply"
      },
      "schema:domainIncludes": {
        "@id": "schema:Recipe"
      },
      "schema:rangeIncludes": {
        "@id": "schema:Text"
      }
    },
    {
      "@id": "schema:ingredients",
      "schema:supersededBy": {
        "@id": "schema:recipeIngredient"
      }
    }
  ]
```
recipeIngredient schema from 
[schema.org](https://schema.org/recipeIngredient.jsonld).

### Data Registry Storage
Aries will provide a means for writing contexts to and reading contexts
from a verifiable data registry (such as a distributed ledger).

A Schema will be written to the ledger in a generic way defined in 
[Rich Schema Objects Common](https://github.com/hyperledger/aries-rfcs/tree/main/concepts/0420-rich-schemas-common#how-rich-schema-objects-are-stored-in-the-data-registry).


### Aries Data Registry Interface
Aries Data Registry Interface methods for adding and retrieving a Schema from the
ledger comply with the generic approach described in [Rich Schema Objects Common](https://github.com/hyperledger/aries-rfcs/tree/main/concepts/0420-rich-schemas-common#aries-data-registry-interface).

This means the following methods can be used:
- `write_rich_schema_object`
- `read_rich_schema_object_by_id`
- `read_rich_schema_object_by_metadata`

## Reference
[reference]: #reference

More information on the Verifiable Credential data model use of `schemas`
may be found [here](https://w3c.github.io/vc-data-model/#data-schemas).

- [0250: Rich Schema Objects](https://github.com/hyperledger/aries-rfcs/tree/main/concepts/0250-rich-schemas)
- [0420: Rich Schema Objects Common](https://github.com/hyperledger/aries-rfcs/tree/main/concepts/0420-rich-schemas-common) 

## Drawbacks

Rich schema objects introduce more complexity.

## Rationale and alternatives

- A `schema` object is supported by the W3C Verifiable Credentials Data
Model specification.
- It supports rich schema capabilities for credentials.

## Unresolved questions

- Is the proposed interface generic enough to support other data
registries?
- We are not defining Rich Schema objects as DID DOCs for now. We may re-consider this in future once DID DOC format
is finalized.
- It may make sense to extend DID specification to include using DID for referencing Rich Schema objects.
- The proposed canonicalization form of a content to be used for DID's id-string generation is in a Draft version, so we 
may find a better way to do it.
- We don't check if the specified `@context` is valid by resolving all external links.
- We may introduce more discovery features in future.
- Future work may include methods for anchoring to Indy a Rich Schema which is immutably stored elsewhere.

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

