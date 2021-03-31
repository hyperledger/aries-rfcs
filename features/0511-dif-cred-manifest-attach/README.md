# Aries RFC 0511: Credential-Manifest Attachment format for requesting and presenting credentials
- Authors: George Aristy (SecureKey Technologies)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2020-07-22
- Status Note:
- Supersedes:
- Start Date: 2020-07-22
- Tags: [feature](/tags.md#feature), [protocol](/tags.md#protocol), [credentials](/tags.md#credentials), [test-anomaly](/tags.md#test-anomaly)


## Summary

This RFC registers an attachment format for use in the [issue-credential V2](../0453-issue-credential-v2/README.md) based on
the Decentralized Identity Foundation's (DIF) [*Credential Manifest specification*](https://identity.foundation/credential-manifest/).
*Credental Manifest* describes a data format that specifies the inputs an Issuer requires for issuance of a credential. It relies on the closely-related
[*Presentation Exchange specification*](https://identity.foundation/presentation-exchange/) to describe the required inputs and
the format in which the Holder submits those inputs (a verifiable presentation).


## Motivation

The *Credential Manifest* specification lends itself well to several transport mediums due to its limited scope as a data format,
and is easily transported over DIDComm.

It is furthermore desirable to make use of specifications developed in an open standards body.


## Tutorial

Complete examples of messages are provided in the [reference section](#reference).

Credential Manifests MAY be acquired by the Holder via out of band means, such as from a well-known location on the Issuer's website.
This allows the Holder to initiate the `issue-credential` protocol with a `request-message` providing they also possess the requisite
`challenge` and `domain` values. If they do not possess these values then the Issuer MAY respond with an `offer-credential` message.

Otherwise the Holder MAY initiate the protocol with `propose-credential` in order to discover the Issuer's requirements.


## Reference

### `propose-credential` attachment format

Format identifier: `dif/credential-manifest@v1.0`

The contents of the attachment is the minimal form of the Issuer's credential manifest describing the credential the Holder desires.
It SHOULD contain the `issuer` and `credential` properties and no more.

Complete message example:

```json
{
    "@id": "8639505e-4ec5-41b9-bb31-ac6a7b800fe7",
    "@type": "https://didcomm.org/issue-credential/%VER/propose-credential",
    "comment": "<some comment>",
    "formats" : [{
        "attach_id": "b45ca1bc-5b3c-4672-a300-84ddf6fbbaea",
        "format": "dif/credential-manifest@v1.0"
    }],
    "filters~attach": [{
        "@id": "b45ca1bc-5b3c-4672-a300-84ddf6fbbaea",
        "mime-type": "application/json",
        "data": {
            "json": {
                "issuer": "did:example:123",
                "credential": {
                    "name": "Washington State Class A Commercial Driver License",
                    "schema": "ipfs:QmPXME1oRtoT627YKaDPDQ3PwA8tdP9rWuAAweLzqSwAWT"
                }
            }
        }
    }]
}
```


### `offer-credential` attachment format

Format identifier: `dif/credential-manifest@v1.0`

The contents of the attachment is a JSON object containing the Issuer's credential manifest, a challenge and domain.
All three attributes are REQUIRED.

Example:

```jsonc
{
    "@id": "dfedaad3-bd7a-4c33-8337-fa94a547c0e2",
    "@type": "https://didcomm.org/issue-credential/%VER/offer-credential",
    "comment": "<some comment>",
    "formats" : [{
        "attach_id" : "76cd0d94-8eb6-4ef3-a094-af45d81e9528",
        "format" : "dif/credential-manifest@v1.0"
    }],
    "offers~attach": [{
        "@id": "76cd0d94-8eb6-4ef3-a094-af45d81e9528",
        "mime-type": "application/json",
        "data": {
            "json": {
                "challenge": "1f44d55f-f161-4938-a659-f8026467f126",
                "domain": "us.gov/DriverLicense",
                "credential_manifest": {
                    // credential manifest object
                }
            }
        }
    }]
}
```


### `request-credential` attachment format

Format identifier: `dif/credential-manifest@v1.0`

The contents of the attachment is a JSON object that describes the credential requested and provides the inputs the Issuer requires
from the Holder before proceeding with issuance:

```jsonc
{
    "credential-manifest": {
        "issuer": "did:example:123",
        "credential": {
            "name": "Washington State Class A Commercial Driver License",
            "schema": "ipfs:QmPXME1oRtoT627YKaDPDQ3PwA8tdP9rWuAAweLzqSwAWT"
        }
    },
    "presentation-submission": {
        // presentation submission object
    }
}
```

* `credential-manifest`: OPTIONAL. Required if the Holder starts the protocol with `request-credential`.
* `presentation-submission`: OPTIONAL. Required as a response to the `presentation_definition` attribute in the Issuer's credential manifest, if present.

If the Issuer's credential manifest does not include the `presentation_definition` attribute, and the Holder has initiated
the protocol with `propose-credential`, then this attachment MAY be omitted entirely as the message thread provides sufficient context
for this request.

Implementors are STRONGLY discouraged from allowing BOTH `credential-manifest` and `presentation-submission`.
The latter requires the Holder's knowledge of the necessary `challenge` and `domain`, both of which SHOULD provide sufficient context
to the Issuer as to which credential is being requested.

The following example shows a `request-credential` with a presentation submission.
Notice the presentation's `proof` includes the `challenge` and `domain` acquired either through out-of-band means or
via an `offer-credential` message.:

```json
{
    "@id": "cf3a9301-6d4a-430f-ae02-b4a79ddc9706",
    "@type": "https://didcomm.org/issue-credential/%VER/request-credential",
    "comment": "<some comment>",
    "formats": [{
        "attach_id": "7cd11894-838a-45c0-a9ec-13e2d9d125a1",
        "format": "dif/credential-manifest@v1.0"
    }],
    "requests~attach": [{
        "@id": "7cd11894-838a-45c0-a9ec-13e2d9d125a1",
        "mime-type": "application/json",
        "data": {
            "json": {
                "presentation-submission": {
                    "@context": [
                        "https://www.w3.org/2018/credentials/v1",
                        "https://identity.foundation/presentation-exchange/submission/v1"
                    ],
                    "type": [
                        "VerifiablePresentation",
                        "PresentationSubmission"
                    ],
                    "presentation_submission": {
                        "descriptor_map": [{
                            "id": "citizenship_input",
                            "path": "$.verifiableCredential.[0]"
                        }]
                    },
                    "verifiableCredential": [{
                        "@context": "https://www.w3.org/2018/credentials/v1",
                        "id": "https://us.gov/claims/Passport/723c62ab-f2f0-4976-9ec1-39992e20c9b1",
                        "type": ["USPassport"],
                        "issuer": "did:foo:123",
                        "issuanceDate": "2010-01-01T19:73:24Z",
                        "credentialSubject": {
                            "id": "did:example:ebfeb1f712ebc6f1c276e12ec21",
                            "birth_date": "2000-08-14"
                        },
                        "proof": {
                            "type": "EcdsaSecp256k1VerificationKey2019",
                            "created": "2017-06-18T21:19:10Z",
                            "proofPurpose": "assertionMethod",
                            "verificationMethod": "https://example.edu/issuers/keys/1",
                            "jws": "..."
                        }
                    }],
                    "proof": {
                        "type": "RsaSignature2018",
                        "created": "2018-09-14T21:19:10Z",
                        "proofPurpose": "authentication",
                        "verificationMethod": "did:example:ebfeb1f712ebc6f1c276e12ec21#keys-1",
                        "challenge": "1f44d55f-f161-4938-a659-f8026467f126",
                        "domain": "us.gov/DriverLicense",
                        "jws": "..."
                    }
                }
            }
        }
    }]
}
```

### `issue-credential` attachment format

This specification does not register any format identifier for the `issue-credential` message. The Issuer SHOULD set the `format` to the value
that corresponds to the format the credentials are issued in.


## Drawbacks

N/A


## Rationale and alternatives

- The `hlindy-zkp-v1.0` format is an alternative restricted to the Hyperledger Indy network.


## Prior art

N/A


## Unresolved questions

N/A
   
   
## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

Name / Link | Implementation Notes
--- | ---
 | 

