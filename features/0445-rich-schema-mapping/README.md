# Aries RFC 0445: Aries Rich Schema Mapping
- Author: [Alexander Shcherbakov](mailto:alexander.shcherbakov@evernym.com), [Ken Ebert](mailto:ken@sovrin.org), [Brent Zundel](mailto:brent.zundel@evernym.com)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2020-03-16
- Status Note: Part of proposed Rich Schema capabilities for credentials 
- Supersedes:
- Start Date: 2019-03-16
- Tags: [feature](/tags.md#feature), [rich-schemas](/tags.md#rich-schemas)

## Summary
Mappings serve as a bridge between rich schemas and the flat array of
signed integers. A mapping specifies the order in which attributes are
transformed and signed. It consists of a set of graph paths and the
encoding used for the attribute values specified by those graph paths. Each
claim in a mapping has a reference to an encoding, and those encodings are
defined in encoding objects.

Mapping objects are processed in a generic way defined in 
[Rich Schema Objects Common](https://github.com/hyperledger/aries-rfcs/tree/master/concepts/0420-rich-schemas-common).

## Motivation

Rich schemas are complex, hierarchical, and possibly nested objects. The
[Camenisch-Lysyanskaya signature][CL-signatures] scheme used by Indy
requires the attributes to be represented by an array of 256-bit integers.
Converting data specified by a rich schema into a flat array of integers
requires a mapping object.

## Tutorial


### Intro to Mappings
Mappings are written to the ledger so they can be shared by multiple
credential definitions. 
A Credential Definition may only reference a single Mapping.

One or more Mappings can be referenced by a Presentation Definition.
The mappings serve as a vital part of the verification process. The
verifier, upon receipt of a presentation must not only check that the array
of integers signed by the issuer is valid, but that the attribute values
were transformed and ordered according to the mapping referenced in the
credential definition.

A Mapping references one and only one Rich Schema object. If there is no Schema Object 
a Mapping can reference, a new Schema must be created on the ledger.
If a Mapping needs to map attributes from multiple Schemas, then a new Schema embedding the multiple Schemas 
must be created and stored on the ledger.    

Mappings need to be discoverable.

Mapping is a JSON-LD object following the same structure (attributes and graph pathes) 
as the corresponding Rich Schema.
A Mapping may contain only a subset of the original Rich Schema's attributes.

The value of every schema attribute in a Mapping object is an array of the following pairs:
- encoding object (referenced by its `id`) to be used for representation of the attribute as an integer
- rank of the attribute to define the order in which the attribute is signed by the Issuer.

The value is an array as the same attribute may be used in Credential Definition multiple times
with different encodings. 




Note: The anonymous credential signature scheme currently used by Indy is
[Camenisch-Lysyanskaya signatures][CL-signatures]. It is the use of this
signature scheme in combination with rich schema objects that necessitates
a mapping object. If another signature scheme is used which does not have
the same requirements, a mapping object may not be necessary or a different
mapping object may need to be defined.

### Properties
Mapping's properties follow the generic template defined in 
[Rich Schema Common](https://github.com/hyperledger/aries-rfcs/tree/master/concepts/0420-rich-schemas-common#how-rich-schema-objects-are-stored-in-the-data-registry).

Mapping's `content` field is a JSON-LD-serialized string with the following fields:

#### @id
A Mapping must have an `@id` property. The value of this property must
be equal to the `id` field which is a DID (see [Identification of Rich Schema Objects](https://github.com/hyperledger/aries-rfcs/tree/master/concepts/0420-rich-schemas-common#identification-of-rich-schema-objects)). 

#### @type
A Mapping must have a `@type` property. The value of this property must
be (or map to, via a context object) a URI. 

#### @context
A Mapping may have a `@context` property. If present, the value of this
property must be a
[context object](../0249-rich-schema-contexts/README.md) or a URI which can
be dereferenced to obtain a context object.

#### schema

An `id` of the corresponding Rich Schema

#### Values
The value of every schema attribute in a Mapping object is an array of the following pairs:

- `enc` (string): Encoding object (referenced by its `id`) to be used for representation of the attribute as an integer. 
- `rank` (int): Rank of the attribute to define the order in which the attribute is signed by the Issuer. It is important that no two `rank` values may be identical.



### Example Mapping
Let's consider a Rich Schema object with the following `content`:
```
    '@id': "did:sov:4e9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
    '@context': "did:sov:2f9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
    '@type': "rdfs:Class",
    "rdfs:comment": "ISO18013 International Driver License",
    "rdfs:label": "Driver License",
    "rdfs:subClassOf": {
        "@id": "sch:Thing"
    },
    "driver": "Driver",
    "dateOfIssue": "Date",
    "dateOfExpiry": "Date",
    "issuingAuthority": "Text",
    "licenseNumber": "Text",
    "categoriesOfVehicles": {
        "vehicleType": "Text",
        "dateOfIssue": "Date",
        "dateOfExpiry": "Date",
        "restrictions": "Text",
    },
    "administrativeNumber": "Text"
```

Then the corresponding Mapping object may have the following `content`. 
 Please note that we used all attributes from the
original Schema except `dateOfExpiry`, `categoriesOfVehicles/dateOfExpiry` and `categoriesOfVehicles/restrictions`.
Also, the `licenseNumber` attribute is used twice, but with different encodings. 
It is important that no two `rank` values may be identical. 
```
    '@id': "did:sov:5e9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
    '@context': "did:sov:2f9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
    '@type': "rdfs:Class",
    "schema": "did:sov:4e9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
    "driver": [{
        "enc": "did:sov:1x9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
        "rank": 5
    }],
    "dateOfIssue": [{
        "enc": "did:sov:2x9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
        "rank": 4
    }],
    "issuingAuthority": [{
        "enc": "did:sov:3x9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
        "rank": 3
    }],
    "licenseNumber": [
        {
            "enc": "did:sov:4x9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
            "rank": 1
        },
        {
            "enc": "did:sov:5x9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
            "rank": 2
        },
    ],
    "categoriesOfVehicles": {
        "vehicleType": [{
            "enc": "did:sov:6x9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
            "rank": 6
        }],
        "dateOfIssue": [{
         "enc": "did:sov:7x9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
            "rank": 7
        }],
    },
    "administrativeNumber": [{
        "enc": "did:sov:8x9F8ZmxuvDqRiqqY29x6dx9oU4qwFTkPbDpWtwGbdUsrCD",
        "rank": 8
    }]
```

### Data Registry Storage
Aries will provide a means for writing contexts to and reading contexts
from a verifiable data registry (such as a distributed ledger).

A Mapping object will be written to the ledger in a generic way defined in 
[Rich Schema Objects Common](https://github.com/hyperledger/aries-rfcs/tree/master/concepts/0420-rich-schemas-common#how-rich-schema-objects-are-stored-in-the-data-registry).


### Aries Data Registry Interface
Aries Data Registry Interface methods for adding and retrieving a Mapping object from the
ledger comply with the generic approach described in [Rich Schema Objects Common](https://github.com/hyperledger/aries-rfcs/tree/master/concepts/0420-rich-schemas-common#aries-data-registry-interface).

This means the following methods can be used:
- `write_rich_schema_object`
- `read_rich_schema_object_by_id`
- `read_rich_schema_object_by_metadata`

## Reference
[reference]: #reference

The following is a 
[reference implementation of various transformation algorithms](https://github.com/sovrin-foundation/aries-credx-framework-rs/blob/master/src/encoding/mod.rs)
Here is the paper that defines
[Camenisch-Lysyanskaya signatures.][CL-signatures] 
[CL-signatures]: (https://groups.csail.mit.edu/cis/pubs/lysyanskaya/cl02b.pdf)

- [0250: Rich Schema Objects](https://github.com/hyperledger/aries-rfcs/tree/master/concepts/0250-rich-schemas)
- [0420: Rich Schema Objects Common](https://github.com/hyperledger/aries-rfcs/tree/master/concepts/0420-rich-schemas-common) 


## Drawbacks
[drawbacks]: #drawbacks

This increases the complexity of issuing verifiable credentials and
verifiying the accompanying verifiable presentations. 

## Rationale and alternatives

- A `schema` object is supported by the W3C Verifiable Credentials Data
Model specification.
- It supports rich schema capabilities for credentials.

A possible alternative to this work has been presented by Workday.

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

