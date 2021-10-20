# Aries RFC 0446: Aries Rich Schema Credential Definition
- Author: [Alexander Shcherbakov](mailto:alexander.shcherbakov@evernym.com), [Ken Ebert](mailto:ken@sovrin.org), [Brent Zundel](mailto:brent.zundel@evernym.com)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2020-03-16
- Status Note: Part of proposed Rich Schema capabilities for credentials 
- Supersedes:
- Start Date: 2019-03-16
- Tags: [feature](/tags.md#feature), [rich-schemas](/tags.md#rich-schemas)

## Summary

Credential Definition can be used by the Issuer to set public keys for a particular
 [Rich Schema](../0281-rich-schemas/README.md)
  and [Mapping](../0445-rich-schema-mapping/README.md).
The public keys can be used for signing the credentials by the Issuer according to the order and encoding of attributes
defined by the referenced Mapping.

Credential Definition objects are processed in a generic way defined in 
[Rich Schema Objects Common](https://github.com/hyperledger/aries-rfcs/tree/main/concepts/0420-rich-schemas-common).


## Motivation


The current format for Indy credential definitions provides a method for
issuers to specify a schema and provide public key data for credentials
they issue. This ties the schema and public key data values to the issuer's
DID. The verifier uses the credential definition to check the validity of
each signed credential attribute presented to the verifier.

The new credential definition object that uses rich schemas is a minor
modification of the current Indy credential definition. The new format has
the same public key data. In addition to referencing a schema, the new
credential definition can also reference a mapping object.

## Tutorial


### Intro to Credential Definition
Credential definitions are written to the ledger so they can be used by holders and verifiers 
in presentation protocol.

A Credential Definition can reference a single Mapping and a single Rich Schema only.

Credential Definition is a JSON object.

Credential Definition should be immutable in most of the cases.
Some application may consider it as a mutable object since the Issuer may rotate
keys present there.
However, rotation of Issuer's keys should be done carefully as it will invalidate all
credentials issued for this key.

### Properties
Credential definition's properties follow the generic template defined in 
[Rich Schema Common](https://github.com/hyperledger/aries-rfcs/tree/main/concepts/0420-rich-schemas-common#how-rich-schema-objects-are-stored-in-the-data-registry).

Credential Definition's `content` field is a JSON-serialized string with the following fields:

#### signatureType
Type of the signature. ZKP scheme `CL` (Camenisch-Lysyanskaya) is the only type currently
supported in Indy. Other signature types, even those that do not support ZKPs, may still
make use of the credential definition to link the issuer's public keys with the rich schema
against which the verifiable credential was constructed.

#### mapping
An `id` of the corresponding Mapping

#### schema
An `id` of the corresponding Rich Schema. The `mapping` must reference the same Schema.

#### publicKey
Issuer's public keys. Consists of `primary` and `revocation` keys.

### Example Credential Definition
An example of the `content` field of a Credential Definition object:
```
"signatureType": "CL",
"mapping": "did:sov:UVj5w8DRzcmPVDpUMr4AZhJ",
"schema": "did:sov:U5x5w8DRzcmPVDpUMr4AZhJ",
"publicKey": {
    "primary": "...",
    "revocation": "..."
}
```

### Use in Verifiable Credentials
A ZKP credential created according to the `CL` signature scheme must reference a Credential Definition used 
for signing. A Credential Definition is referenced in the [credentialSchema](https://www.w3.org/TR/vc-data-model#data-schemas)
property. A Credential Definition is referenced by its `id`.

### Data Registry Storage
Aries will provide a means for writing contexts to and reading contexts
from a verifiable data registry (such as a distributed ledger).

A Credential Definition object will be written to the ledger in a generic way defined in 
[Rich Schema Objects Common](https://github.com/hyperledger/aries-rfcs/tree/main/concepts/0420-rich-schemas-common#how-rich-schema-objects-are-stored-in-the-data-registry).


### Aries Data Registry Interface
Aries Data Registry Interface methods for adding and retrieving a Credential Definition object from the
ledger comply with the generic approach described in [Rich Schema Objects Common](https://github.com/hyperledger/aries-rfcs/tree/main/concepts/0420-rich-schemas-common#aries-data-registry-interface).

This means the following methods can be used:
- `write_rich_schema_object`
- `read_rich_schema_object_by_id`
- `read_rich_schema_object_by_metadata`

## Reference
[reference]: #reference

The following is a 
[reference implementation of various transformation algorithms](https://github.com/sovrin-foundation/aries-credx-framework-rs/blob/master/src/encoding/mod.rs).

[Here](https://www.researchgate.net/publication/220922101_A_Signature_Scheme_with_Efficient_Protocols) is the paper that defines Camenisch-Lysyanskaya signatures.

- [0250: Rich Schema Objects](https://github.com/hyperledger/aries-rfcs/tree/main/concepts/0250-rich-schemas)
- [0420: Rich Schema Objects Common](https://github.com/hyperledger/aries-rfcs/tree/main/concepts/0420-rich-schemas-common) 


## Drawbacks
[drawbacks]: #drawbacks

This increases the complexity of issuing verifiable credentials and
verifiying the accompanying verifiable presentations. 

## Rationale and alternatives

- A `credentialSchema` object is supported by the W3C Verifiable Credentials Data
Model specification.
- It supports rich schema capabilities for credentials.

## Prior art

Indy already has a Credential Definition support. 

What the prior effort lacked was a corresponding enhancement of schema
infrastructure which would have provided the necessary typing of attribute
values.

## Unresolved questions
- Is the proposed interface generic enough to support other data
registries?
- Of all the Rich Schema objects, the CredDef most closely fits the format of a DID DOC.
- However, we are not defining Rich Schema objects as DID DOCs for now. We may re-consider this in future once DID DOC format
is finalized.
- It may make sense to extend DID specification to include using DID for referencing Rich Schema objects.
- The proposed canonicalization form of a content to be used for DID's id-string generation is in a Draft version, so we 
may find a better way to do it.
  
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

