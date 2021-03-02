# Aries RFC 0593: JSON-LD Credential Attachment format for requesting and presenting credentials

- Authors: Timo Glastra (Animo Solutions)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2021-02-24
- Status Note:
- Supersedes:
- Start Date: 2021-02-17
- Tags: [feature](/tags.md#feature), [protocol](/tags.md#protocol), [credentials](/tags.md#credentials), [test-anomaly](/tags.md#test-anomaly)

## Summary

This RFC registers an attachment format for use in the [issue-credential V2](../0453-issue-credential-v2/README.md) protocol based on JSON-LD credentials with [Linked Data Proofs](https://w3c-ccg.github.io/ld-proofs/) from the [VC Data Model](https://www.w3.org/TR/vc-data-model/#linked-data-proofs).

It defines a minimal set of parameters needed to create a common understanding of the verifiable credential to issue. It is based on version [1.0 of the Data Model](https://www.w3.org/TR/vc-data-model/) which is a W3C recommendation since 19 November 2019.

## Motivation

The Issue Credential protocol needs an attachment format to be able to exchange JSON-LD credentials with Linked Data Proofs. It is desirable to make use of specifications developed in an open standards body, such as the [Credential Manifest](https://identity.foundation/credential-manifest/) for which the attachment format is described in [RFC 0511: Credential-Manifest Attachment format](../0511-dif-cred-manifest-attach/README.md). However, the _Credential Manifest_ is not finished and ready yet, and therefore there is a need to bridge the gap between standards.

## Tutorial

Complete examples of messages are provided in the [reference section](#reference).

## Reference

### `ld-proof-vc-proposal` attachment format

Format identifier: `aries/ld-proof-vc-proposal@v1.0`

The credential proposal allows the holder to initiate a credential exchange without fully specifying the contents of the credential. If all properties of the credential are already known, the protocol can also be initiated with a credential request. While the credential detail requires all fields to be present, the proposal allows for fields to be omitted.

The below `propose-credential` message shows an example of a credential proposal with the `@context`, `type`, `credentialSubject` and `credentialSubject` present. The issuer can then send a credential detail in a credential offer message adding extra properties required for issuance such as `issuer`, `credentialStatus.type`, `proofType`, etc..

```json
{
  "@id": "257363ab-a3f9-4bba-ad3f-9f69501135f5",
  "@type": "https://didcomm.org/issue-credential/%VER/propose-credential",
  "comment": "<some comment>",
  "formats": [
    {
      "attach_id": "35054fa5-112e-4ef7-93ab-7778f59eb4e3",
      "format": "aries/vc-ld-proof@v1.0"
    }
  ],
  "filter~attach": [
    {
      "@id": "35054fa5-112e-4ef7-93ab-7778f59eb4e3",
      "mime-type": "application/ld+json",
      "data": {
        "json": {
          "@context": [
            "https://www.w3.org/2018/credentials/v1",
            "https://www.w3.org/2018/credentials/examples/v1"
          ],
          "type": ["VerifiableCredential", "UniversityDegreeCredential"],
          "credentialSubject": {
            "id": "did:example:ebfeb1f712ebc6f1c276e12ec21",
            "degree": {
              "type": "BachelorDegree",
              "name": "Bachelor of Science and Arts"
            }
          },
          "credentialSchema": {
            "id": "https://example.org/examples/degree.json",
            "type": "JsonSchemaValidator2018"
          }
        }
      }
    }
  ]
}
```

- `credentialStatus.id` -- Credential Status may be omitted completely, but if present should contain the `type` property to indicate which mechanism to use. As the id can be closely tied to the issuance process the property is not required for the credential proposal.
- `proofType` -- This is not a property defined by the VC data model, but indicates the proof types the holder proposes for the credential. Entries match the `type` property of the [Proofs](https://www.w3.org/TR/vc-data-model/#proofs-signatures) object. Multiple entries indicate the holder proposes multiple proofs for the credential.

### `ld-proof-vc-detail` attachment format

Format identifier: `aries/ld-proof-vc-detail@v1.0`

This format is used to formally offer or request a credential. It should contain the credential as it is going to be issued, omitting properties that are only available after issuance.

```json
{
  "@id": "7293daf0-ed47-4295-8cc4-5beb513e500f",
  "@type": "https://didcomm.org/issue-credential/%VER/request-credential",
  "comment": "<some comment>",
  "formats": [
    {
      "attach_id": "13a3f100-38ce-4e96-96b4-ea8f30250df9",
      "format": "aries/vc-ld-proof-req@v1.0"
    }
  ],
  "requests~attach": [
    {
      "@id": "13a3f100-38ce-4e96-96b4-ea8f30250df9",
      "mime-type": "application/ld+json",
      "data": {
        "json": {
          "@context": [
            "https://www.w3.org/2018/credentials/v1",
            "https://www.w3.org/2018/credentials/examples/v1"
          ],
          "type": ["VerifiableCredential", "AlumniCredential"],
          "credentialSubject": {
            "id": "did:key:z6MkodKV3mnjQQMB9jhMZtKD9Sm75ajiYq51JDLuRSPZTXrr"
            // other attributes
          },
          "issuer": "did:key:z6MkodKV3mnjQQMB9jhMZtKD9Sm75ajiYq51JDLuRSPZTXrr",
          "issuanceDate": "2020-01-01T19:23:24Z",
          "expirationDate": "2020-01-01T19:23:24Z",
          "credentialStatus": {
            "type": "CredentialStatusList2017"
          },
          "credentialSchema": {
            "id": "https://example.org/examples/degree.json",
            "type": "JsonSchemaValidator2018"
          },
          "proofType": ["Ed25519Signature2018", "BbsBlsSignature2020"]
        }
      }
    }
  ]
}
```

An exhaustive description of the fields is out of scope here. Most fields are directly taken from the Verifiable Credential Data Model, and properties should align with the criteria described in the data model. A couple exceptions are made from the standard model:

- `id` -- May be omitted in credential detail, but this doesn't mean the issued credential won't include an identifier.
- `issuanceDate` -- Required in issued credential, but may be omitted in the credential detail. If present in the credential request it means the value will be used, otherwise a value will be picked by the issuer (most probably the current time).
- `credentialStatus.id` -- Credential Status may be omitted completely, but if present the `id` property is required in the issued credential. As the id can be closely tied to the issuance process the property is not required for the credential request. `credentialStatus.type` is required if the credential is revocable.
- `proofType` -- This is not a property defined by the VC data model, but indicates the proof types the holder requests for the credential. Entries match the `type` property of the [Proofs](https://www.w3.org/TR/vc-data-model/#proofs-signatures) object. Multiple entries indicate that the credential will contain multiple proofs.

### `ld-proof-vc` attachment format

Format identifier: `aries/ld-proof-vc@v1.0`

This format is used to transmit a verifiable credential with linked data proof. The contents of the attachment is a standard JSON-LD Verifiable Credential object with linked data proof. The exact contents of the attachments match the properties from the [Verifiable Credential Data Model](https://www.w3.org/TR/vc-data-model) and the [Linked Data Proofs](https://w3c-ccg.github.io/ld-proofs) specification.

```json
{
  "@id": "284d3996-ba85-45d9-964b-9fd5805517b6",
  "@type": "https://didcomm.org/issue-credential/%VER/issue-credential",
  "comment": "<some comment>",
  "formats": [
    {
      "attach_id": "5b38af88-d36f-4f77-bb7a-2f04ab806eb8",
      "format": "aries/vc-ld-proof@v1.0"
    }
  ],
  "requests~attach": [
    {
      "@id": "5b38af88-d36f-4f77-bb7a-2f04ab806eb8",
      "mime-type": "application/ld+json",
      "data": {
        "json": {
          "@context": "https://www.w3.org/2018/credentials/v1",
          "id": "https://eu.com/claims/DriversLicense",
          "type": ["EUDriversLicense"],
          "issuer": "did:foo:123",
          "issuanceDate": "2010-01-01T19:73:24Z",
          "credentialSubject": {
            "id": "did:example:ebfeb1f712ebc6f1c276e12ec21",
            "license": {
              "number": "34DGE352",
              "dob": "07/13/80"
            }
          },
          "proof": {
            "type": "RsaSignature2018",
            "created": "2017-06-18T21:19:10Z",
            "proofPurpose": "assertionMethod",
            "verificationMethod": "https://example.edu/issuers/keys/1",
            "jws": "..."
          }
        }
      }
    }
  ]
}
```

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
