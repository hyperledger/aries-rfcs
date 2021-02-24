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

It defines a minimal set of parameters needed to create a common understanding of the verifiable credential to issue.

## Motivation

The Issue Credential protocol needs an attachment format to be able to exchange JSON-LD credentials with Linked Data Proofs. It is desirable to make use of specifications developed in an open standards body, such as the [Credential Manifest](https://identity.foundation/credential-manifest/) for which the attachment format is described in [RFC 0511: Credential-Manifest Attachment format](../0511-dif-cred-manifest-attach/README.md). However, the _Credential Manifest_ is not finished and ready yet, and therefore there is a need to bridge the gap between standards.

## Tutorial

Complete examples of messages are provided in the [reference section](#reference).

## Reference

### `propose-credential` attachment format

Format identifier: `aries/vc-ld-proof@v1.0`

Complete message example:

```json
{
  "@id": "64f6518b-fede-43a7-ba45-4ba7e7af0e7b",
  "@type": "https://didcomm.org/issue-credential/%VER/propose-credential",
  "comment": "<some comment>",
  "formats": [
    {
      "attach_id": "64a11985-79a9-4daa-b0e3-0ae0531e7a14",
      "format": "aries/vc-ld-proof@v1.0"
    }
  ],
  "filter~attach": [
    {
      "@id": "64a11985-79a9-4daa-b0e3-0ae0531e7a14",
      "mime-type": "application/json",
      "data": {
        "json": {
          "@context": [
            "https://www.w3.org/2018/credentials/v1",
            "https://www.w3.org/2018/credentials/examples/v1"
          ],
          "type": ["VerifiableCredential", "AlumniCredential"],
          "issuer": "did:key:z6MkodKV3mnjQQMB9jhMZtKD9Sm75ajiYq51JDLuRSPZTXrr",
          "credentialStatusType": ["CredentialStatusList2017"],
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

Description of fields:

- `@context` -- An optional array of contexts indicating the contexts proposed by the holder to use for the credential. See [Contexts](https://www.w3.org/TR/vc-data-model/#contexts). The first context MUST always be `"https://www.w3.org/2018/credentials/v1"` per the VC data model.
- `type` -- An optional array of types indicating the types proposed by the holder to use for the credential. See [Types](https://www.w3.org/TR/vc-data-model/#types). The array MUST always contain `"VerifiableCredential"` per the VC data model.
- `issuer` -- An optional URI indicating the issuer id proposed by the holder to use for the credential. See [Issuer](https://www.w3.org/TR/vc-data-model/#issuer). Only the issuer URI (id) is supported at the moment.
- `credentialStatusType` -- An optional array of strings that indicates the credential status types the holder is willing to accept. See [Status](https://www.w3.org/TR/vc-data-model/#status). If no `credentialStatusType` is present it means no preference on the credential status mechanism is given by the holder. However, an empty array indicates the holder proposes a credential without credential status, i.e. the credential is not revocable.
- `credentialSchema` -- An optional object indicating the proposed schema to use for the credential. It matches the `credentialSchema` from [Data Schemas](https://www.w3.org/TR/vc-data-model/#data-schemas).
- `proofType` -- An optional array of strings indicating the proof types the holder is willing to accept. Entries match the `type` property of the [Proofs](https://www.w3.org/TR/vc-data-model/#proofs-signatures) object.

### `offer-credential` attachment format

Format identifier: `aries/vc-ld-proof@v1.0`

Complete message example:

```jsonc
{
  "@id": "2570ed16-91e7-49e7-bc61-b562d1ac2f18",
  "@type": "https://didcomm.org/issue-credential/%VER/offer-credential",
  "comment": "<some comment>",
  "formats": [
    {
      "attach_id": "d60c05ac-35c2-484c-af3e-8ef7f21baf0a",
      "format": "aries/vc-ld-proof@v1.0"
    }
  ],
  "offers~attach": [
    {
      "@id": "d60c05ac-35c2-484c-af3e-8ef7f21baf0a",
      "mime-type": "application/json",
      "data": {
        "json": {
          "@context": [
            "https://www.w3.org/2018/credentials/v1",
            "https://www.w3.org/2018/credentials/examples/v1"
          ],
          "type": ["VerifiableCredential", "AlumniCredential"],
          "issuer": "did:key:z6MkodKV3mnjQQMB9jhMZtKD9Sm75ajiYq51JDLuRSPZTXrr",
          "credentialStatusType": "CredentialStatusList2017",
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

Description of fields:

- `@context` -- An array of contexts indicating the contexts the issuer will use for the credential. See [Contexts](https://www.w3.org/TR/vc-data-model/#contexts). The first context MUST always be `"https://www.w3.org/2018/credentials/v1"` per the VC data model.
- `type` -- An array of types indicating the types the issuer will use for the credential. See [Types](https://www.w3.org/TR/vc-data-model/#types). The array MUST always contain `"VerifiableCredential"` per the VC data model.
- `issuer` -- An URI indicating the issuer id the issuer will use for the credential. See [Issuer](https://www.w3.org/TR/vc-data-model/#issuer). Only the issuer URI (id) is supported at the moment.
- `credentialStatusType` -- An optional string that indicates the credential status type the issuer will use for the credential. See [Status](https://www.w3.org/TR/vc-data-model/#status). If no `credentialStatusType` is present it means no `credentialStatus` will be included in the credential, i.e. the credential is not revocable.
- `credentialSchema` -- An optional object indicating the proposed schema to use for the credential. It matches the `credentialSchema` from [Data Schemas](https://www.w3.org/TR/vc-data-model/#data-schemas). If no `credentialSchema` is present it means no `credentialSchema` will be included in the credential.
- `proofType` -- An array of strings indicating the proof types the issuer will use for the credential. Entries match the `type` property of the [Proofs](https://www.w3.org/TR/vc-data-model/#proofs-signatures) object. Multiple entries indicate the issuer will attach multiple proofs to the credential.

### `request-credential` attachment format

Format identifier: `aries/vc-ld-proof@v1.0`

```json
{
  "@id": "7293daf0-ed47-4295-8cc4-5beb513e500f",
  "@type": "https://didcomm.org/issue-credential/%VER/request-credential",
  "comment": "<some comment>",
  "formats": [
    {
      "attach_id": "13a3f100-38ce-4e96-96b4-ea8f30250df9",
      "format": "aries/vc-ld-proof@v1.0"
    }
  ],
  "requests~attach": [
    {
      "@id": "13a3f100-38ce-4e96-96b4-ea8f30250df9",
      "mime-type": "application/json",
      "data": {
        "json": {
          "@context": [
            "https://www.w3.org/2018/credentials/v1",
            "https://www.w3.org/2018/credentials/examples/v1"
          ],
          "type": ["VerifiableCredential", "AlumniCredential"],
          "issuer": "did:key:z6MkodKV3mnjQQMB9jhMZtKD9Sm75ajiYq51JDLuRSPZTXrr",
          "credentialStatusType": "CredentialStatusList2017",
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

Description of fields:

- `@context` -- An array of contexts indicating the contexts the holder requests for the credential. See [Contexts](https://www.w3.org/TR/vc-data-model/#contexts). The first context MUST always be `"https://www.w3.org/2018/credentials/v1"` per the VC data model.
- `type` -- An array of types indicating the types the holder requests for the credential. See [Types](https://www.w3.org/TR/vc-data-model/#types). The array MUST always contain `"VerifiableCredential"` per the VC data model.
- `issuer` -- An URI indicating the issuer id the holder requests for the credential. See [Issuer](https://www.w3.org/TR/vc-data-model/#issuer). Only the issuer URI (id) is supported at the moment.
- `credentialStatusType` -- An optional string that indicates the credential status type holder requests for the credential. It must match the value of `credentialStatus.type` in the issued credential. See [Status](https://www.w3.org/TR/vc-data-model/#status). If no `credentialStatusType` is present it means no `credentialStatus` will be included in the credential, i.e. the credential is not revocable.
- `credentialSchema` -- An optional object indicating the requested schema to use for the credential. It matches the `credentialSchema` from [Data Schemas](https://www.w3.org/TR/vc-data-model/#data-schemas). If no `credentialSchema` is present it means no `credentialSchema` will be included in the credential.
- `proofType` -- An array of strings indicating the proof types the holder requests for the credential. Entries match the `type` property of the [Proofs](https://www.w3.org/TR/vc-data-model/#proofs-signatures) object. Multiple entries indicate the holder requests multiple proofs for the credential.

### `issue-credential` attachment format

Format identifier: `aries/vc-ld-proof@v1.0`

The contents of the attachment is a standard JSON-LD Verifiable Credential object with linked data proof.

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
      "mime-type": "application/json+ld",
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
