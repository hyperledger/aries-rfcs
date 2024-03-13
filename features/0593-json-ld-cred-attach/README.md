# Aries RFC 0593: JSON-LD Credential Attachment format for requesting and issuing credentials

- Authors: Timo Glastra (Animo Solutions), George Aristy (SecureKey Technologies)
- Status: [ADOPTED](/README.md#adopted)
- Since: 2021-04-15
- Status Note: Included as part of the JSON-LD verifiable credentials subtarget of [AIP v2.0](../../concepts/0302-aries-interop-profile/README.md).
- Supersedes:
- Start Date: 2021-02-17
- Tags: [feature](/tags.md#feature), [protocol](/tags.md#protocol), [credentials](/tags.md#credentials), [test-anomaly](/tags.md#test-anomaly)

## Summary

This RFC registers an attachment format for use in the [issue-credential V2](../0453-issue-credential-v2/README.md) protocol based on JSON-LD credentials with [Linked Data Proofs](https://w3c-ccg.github.io/ld-proofs/) from the [VC Data Model](https://www.w3.org/TR/vc-data-model/#linked-data-proofs).

It defines a minimal set of parameters needed to create a common understanding of the verifiable credential to issue. It is based on version [1.0 of the Verifiable Credentials Data Model](https://www.w3.org/TR/vc-data-model/) which is a W3C recommendation since 19 November 2019.

## Motivation

The Issue Credential protocol needs an attachment format to be able to exchange JSON-LD credentials with Linked Data Proofs. It is desirable to make use of specifications developed in an open standards body, such as the [Credential Manifest](https://identity.foundation/credential-manifest/) for which the attachment format is described in [RFC 0511: Credential-Manifest Attachment format](../0511-dif-cred-manifest-attach/README.md). However, the _Credential Manifest_ is not finished and ready yet, and therefore there is a need to bridge the gap between standards.

## Tutorial

Complete examples of messages are provided in the [reference section](#reference).

## Reference

### `ld-proof-vc-detail` attachment format

Format identifier: `aries/ld-proof-vc-detail@v1.0`

This format is used to formally propose, offer, or request a credential. The `credential` property should contain the credential as it is going to be issued, without the `proof` and `credentialStatus` properties. Options for these properties are specified in the `options` object.

The JSON structure might look like this:

```json
{
  "credential": {
    "@context": [
      "https://www.w3.org/2018/credentials/v1",
      "https://www.w3.org/2018/credentials/examples/v1"
    ],
    "id": "urn:uuid:3978344f-8596-4c3a-a978-8fcaba3903c5",
    "type": ["VerifiableCredential", "UniversityDegreeCredential"],
    "issuer": "did:key:z6MkodKV3mnjQQMB9jhMZtKD9Sm75ajiYq51JDLuRSPZTXrr",
    "issuanceDate": "2020-01-01T19:23:24Z",
    "expirationDate": "2021-01-01T19:23:24Z",
    "credentialSubject": {
      "id": "did:key:z6MkpTHR8VNsBxYAAWHut2Geadd9jSwuBV8xRoAnwWsdvktH",
      "degree": {
        "type": "BachelorDegree",
        "name": "Bachelor of Science and Arts"
      }
    }
  },
  "options": {
    "proofPurpose": "assertionMethod",
    "created": "2020-04-02T18:48:36Z",
    "domain": "example.com",
    "challenge": "9450a9c1-4db5-4ab9-bc0c-b7a9b2edac38",
    "credentialStatus": {
      "type": "CredentialStatusList2017"
    },
    "proofType": "Ed25519Signature2018"
  }
}
```

A complete [`request credential` message form the Issue Credential protocol 2.0](../0453-issue-credential-v2/README.md#request-credential) might look like this:

```jsonc
{
  "@id": "7293daf0-ed47-4295-8cc4-5beb513e500f",
  "@type": "https://didcomm.org/issue-credential/%VER/request-credential",
  "comment": "<some comment>",
  "formats": [
    {
      "attach_id": "13a3f100-38ce-4e96-96b4-ea8f30250df9",
      "format": "aries/ld-proof-vc-detail@v1.0"
    }
  ],
  "requests~attach": [
    {
      "@id": "13a3f100-38ce-4e96-96b4-ea8f30250df9",
      "mime-type": "application/json",
      "data": {
        "base64": "ewogICJjcmVkZW50aWFsIjogewogICAgIkBjb250...(clipped)...IkVkMjU1MTlTaWduYXR1cmUyMDE4IgogIH0KfQ=="
      }
    }
  ]
}
```

- `credential` - Required. Detail of the JSON-LD Credential that will be issued. Properties MUST align with the [Verifiable Credentials Data Model](https://www.w3.org/TR/vc-data-model). This also means all properties required by the data model MUST be present. The properties listed below are formally supported, but additional properties MAY be included if it conforms with the data model.

  - `@context`
  - `id`
  - `type`
  - `issuer`
  - `issuanceDate`
  - `expirationDate`
  - `credentialSubject`

- `options` - Required. Options for specifying how the linked data proof is created.

  - `proofType` - Required string. The proof type used for the proof. Should match suites registered in the [Linked Data Cryptographic Suite Registry](https://w3c-ccg.github.io/ld-cryptosuite-registry/#signature-suites).
  - `proofPurpose` - Optional string, default `assertionMethod`. The proof purpose used for the proof. Should match proof purposes registered in the [Linked Data Proofs Specification](https://w3c-ccg.github.io/ld-proofs/#proof-purpose).
  - `created` - Optional string, default current system time. The date and time of the proof (with a maximum accuracy in seconds).
  - `challenge` - Optional string. A challenge to include in the proof. SHOULD be provided by the requesting party of the credential (=holder).
  - `domain` - Optional string. The intended domain of validity for the proof.
  - `credentialStatus` - Optional object. The credential status mechanism to use for the credential. Omitting the property indicates the issued credential will not include a credential status.
    - `type` - Required string. Credential status method type to use for the credential. Should match status method registered in the [Verifiable Credential Extension Registry](https://w3c-ccg.github.io/vc-extension-registry/#status-methods)

The format is closely related to the [Verifiable Credentials HTTP API](https://w3c-ccg.github.io/vc-http-api/), but diverts on some places. The main differences are:

- The types in the VC HTTP API are more restrictive (.e.g. `@context` must be array of strings). This format allows all fields to use the full syntax as described by the verifiable credentials data model.
- Instead of specifying the exact `verificationMethod`, the `proofType` that will be used for the credential can be specified.

### `ld-proof-vc` attachment format

Format identifier: `aries/ld-proof-vc@v1.0`

This format is used to transmit a verifiable credential with linked data proof. The contents of the attachment is a standard JSON-LD Verifiable Credential object with linked data proof as defined by the [Verifiable Credentials Data Model](https://www.w3.org/TR/vc-data-model) and the [Linked Data Proofs](https://w3c-ccg.github.io/ld-proofs) specification.

The JSON structure might look like this:

```json
{
  "@context": [
    "https://www.w3.org/2018/credentials/v1",
    "https://www.w3.org/2018/credentials/examples/v1"
  ],
  "id": "http://example.gov/credentials/3732",
  "type": ["VerifiableCredential", "UniversityDegreeCredential"],
  "issuer": {
    "id": "did:web:vc.transmute.world"
  },
  "issuanceDate": "2020-03-10T04:24:12.164Z",
  "credentialSubject": {
    "id": "did:example:ebfeb1f712ebc6f1c276e12ec21",
    "degree": {
      "type": "BachelorDegree",
      "name": "Bachelor of Science and Arts"
    }
  },
  "proof": {
    "type": "JsonWebSignature2020",
    "created": "2020-03-21T17:51:48Z",
    "verificationMethod": "did:web:vc.transmute.world#_Qq0UL2Fq651Q0Fjd6TvnYE-faHiOpRlPVQcY_-tA4A",
    "proofPurpose": "assertionMethod",
    "jws": "eyJiNjQiOmZhbHNlLCJjcml0IjpbImI2NCJdLCJhbGciOiJFZERTQSJ9..OPxskX37SK0FhmYygDk-S4csY_gNhCUgSOAaXFXDTZx86CmI5nU9xkqtLWg-f4cqkigKDdMVdtIqWAvaYx2JBA"
  }
}
```

A complete [`issue-credential` message from the Issue Credential protocol 2.0](../0453-issue-credential-v2/README.md#issue-credential) might look like this:

```json
{
  "@id": "284d3996-ba85-45d9-964b-9fd5805517b6",
  "@type": "https://didcomm.org/issue-credential/%VER/issue-credential",
  "comment": "<some comment>",
  "formats": [
    {
      "attach_id": "5b38af88-d36f-4f77-bb7a-2f04ab806eb8",
      "format": "aries/ld-proof-vc@v1.0"
    }
  ],
  "credentials~attach": [
    {
      "@id": "5b38af88-d36f-4f77-bb7a-2f04ab806eb8",
      "mime-type": "application/ld+json",
      "data": {
        "base64": "ewogICAgICAgICAgIkBjb250ZXogWwogICAgICAg...(clipped)...RNVmR0SXFXZhWXgySkJBIgAgfQogICAgICAgIH0="
      }
    }
  ]
}
```

### Supported Proof Types

Following are the [Linked Data proof](https://w3c-ccg.github.io/ld-proofs/) types on [Verifiable Credentials](https://www.w3.org/TR/vc-data-model/)
that MUST be supported for compliance with this RFC. All suites listed in the following table MUST be registered in the
[Linked Data Cryptographic Suite Registry](https://w3c-ccg.github.io/ld-cryptosuite-registry/):

Suite|Spec|Enables Selective disclosure?|Enables Zero-knowledge proofs?|Optional
-----|----|-----------------------------|------------------------------|----------
Ed25519Signature2018|[Link](https://w3c-ccg.github.io/lds-ed25519-2018/)|No|No|No
BbsBlsSignature2020**|[Link](https://w3c-ccg.github.io/ldp-bbs2020/)|Yes|No|No
JsonWebSignature2020***|[Link](https://w3c-ccg.github.io/lds-jws2020/)|No|No|Yes

> ** Note: see [RFC0646](../0646-bbs-credentials/README.md) for details on how BBS+ signatures are to be produced and
> consumed by Aries agents.

> *** Note: P-256 and P-384 curves are supported.

## Drawbacks

N/A

## Rationale and alternatives

- The `hlindy-zkp-v1.0` format is an alternative restricted to the Hyperledger Indy network. The `dif/credential-manifest@v1.0` allows to issue JSON-LD credentials but is not ready yet for usage.

## Prior art

N/A

## Unresolved questions

N/A

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

| Name / Link | Implementation Notes |
| ----------- | -------------------- |
|             |
