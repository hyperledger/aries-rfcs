# Aries RFC 0510: Presentation-Exchange Attachment format for requesting and presenting proofs

- Authors: George Aristy (SecureKey Technologies)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2020-07-21
- Status Note:  
- Supersedes: 
- Start Date: 2020-07-21
- Tags: [feature](/tags.md#feature), [protocol](/tags.md#protocol), [credentials](/tags.md#credentials), [test-anomaly](/tags.md#test-anomaly)


## Summary

This RFC registers three attachment formats for use in the [present-proof V2](../0454-present-proof-v2/README.md) protocol based on
the Decentralized Identity Foundation's (DIF) [Presentation Exchange specification](https://identity.foundation/presentation-exchange/) (P-E).
Two of these formats define containers for a presentation-exchange request object and another _options_ object carrying
additional parameters, while the third format is just a vessel for the final `presentation_submission` verifiable
presentation transferred from the Prover to the Verifier.

*Presentation Exchange* defines a data format capable of articulating a rich set of proof requirements from Verifiers,
and also provides a means of describing the formats in which Provers must submit those proofs.

A Verifier's defines their requirements in a `presentation_definition` containing `input_descriptors` that describe
the credential(s) the proof(s) must be derived from as well as a rich set of operators that place `constraints` on those proofs
(eg. "must be issued from issuer X" or "`age` over X", etc.).

The Verifiable Presentation format of [Presentation Submissions](https://identity.foundation/presentation-exchange/#presentation-submission)
is used as opposed to OIDC tokens or CHAPI objects. For an alternative on how to tunnel OIDC messages over DIDComm, see
[HTTP-Over-DIDComm](../0335-http-over-didcomm/README.md). CHAPI is an alternative transport to DIDComm.


## Motivation

The *Presentation Exchange* specification (P-E) possesses a rich language for expressing a Verifier's criterion.

P-E lends itself well to several transport mediums due to its limited scope as a data format,
and is easily transported over DIDComm.

It is furthermore desirable to make use of specifications developed in an open standards body.


## Tutorial

Complete examples of messages are provided in the [reference section](#reference).

The Verifier sends a `request-presentation` to the Prover containing a
[`presentation_definition`](https://identity.foundation/presentation-exchange/#presentation-definition), along with a
`domain` and `challenge` the Prover must sign over in the proof.

The Prover can optionally respond to the Verifier's `request-presentation` with a `propose-presentation` message containing
"Input Descriptors" that describe the proofs they can provide. The contents of the attachment is just the
`input_descriptors` attribute of the `presentation_definition` object.

The Prover responds with a `presentation` message containing a
[`presentation_submission`](https://identity.foundation/presentation-exchange/#presentation-submission).


## Reference

### `propose-presentation` attachment format

Format identifier: `dif/presentation-exchange/definition@v1.0`

#### Examples: propose-presentation

<details><summary>Complete message example</summary>

```json
{
    "@type": "https://didcomm.org/present-proof/%VER/propose-presentation",
    "@id": "fce30ed1-96f8-44c9-95cf-b274288009dc",
    "comment": "some comment",
    "formats" : [{
        "attach_id" : "143c458d-1b1c-40c7-ab85-4d16808ddf0a",
        "format" : "dif/presentation-exchange/definition@v1.0"
    }],
    "proposal~attach": [{
        "@id": "143c458d-1b1c-40c7-ab85-4d16808ddf0a",
        "mime-type": "application/json",
        "data": {
            "json": {
                "input_descriptors": [{
                    "id": "citizenship_input",
                    "name": "US Passport",
                    "group": ["A"],
                    "schema": [{
                        "uri": "hub://did:foo:123/Collections/schema.us.gov/passport.json"
                    }],
                    "constraints": {
                        "fields": [{
                            "path": ["$.credentialSubject.birth_date", "$.vc.credentialSubject.birth_date", "$.birth_date"],
                            "filter": {
                                "type": "date",
                                "minimum": "1999-5-16"
                            }
                        }]
                    }
                }]
            }
        }
    }]
}
```
</details>


### `request-presentation` attachment format

Format identifier: `dif/presentation-exchange/definition@v1.0`

The contents of the attachment is a JSON object containing the Verifier's presentation definition and an _options_ object
with proof options:

```jsonc
{
    "options": {
        "challenge": "...",
        "domain": "...",
    },
    "presentation_definition": {
        // presentation definition object
    }
}
```

#### The _options_ object

_options_ is a container of additional parameters required for the Prover to fulfill the Verifier's request.

Available options are:

Name|Status|Description
----|------|-----------
`challenge`|RECOMMENDED (for LD proofs)|Random seed provided by the Verifier for [LD Proofs](https://w3c-ccg.github.io/ld-proofs/#dfn-challenge).
`domain`|RECOMMENDED (for LD proofs)|The operational domain of the requested [LD proof](https://w3c-ccg.github.io/ld-proofs/#dfn-domain).

#### Examples: request-presentation

<details><summary>Complete message example requesting a verifiable presentation with proof type Ed25519Signature2018</summary>

```json
{
    "@type": "https://didcomm.org/present-proof/%VER/request-presentation",
    "@id": "0ac534c8-98ed-4fe3-8a41-3600775e1e92",
    "comment": "some comment",
    "formats" : [{
        "attach_id" : "ed7d9b1f-9eed-4bde-b81c-3aa7485cf947",
        "format" : "dif/presentation-exchange/definition@v1.0"
    }],
    "request_presentations~attach": [{
        "@id": "ed7d9b1f-9eed-4bde-b81c-3aa7485cf947",
        "mime-type": "application/json",
        "data":  {
            "json": {
                "options": {
                    "challenge": "23516943-1d79-4ebd-8981-623f036365ef",
                    "domain": "us.gov/DriversLicense"
                },
                "presentation_definition": {
                    "input_descriptors": [{
                        "id": "citizenship_input",
                        "name": "US Passport",
                        "group": ["A"],
                        "schema": [{
                            "uri": "hub://did:foo:123/Collections/schema.us.gov/passport.json"
                        }],
                        "constraints": {
                            "fields": [{
                                "path": ["$.credentialSubject.birth_date", "$.birth_date"],
                                "filter": {
                                    "type": "date",
                                    "minimum": "1999-5-16"
                                }
                            }]
                        }
                    }],
                    "format": {
                        "ldp_vp": {
                            "proof_type": ["Ed25519Signature2018"]
                        }
                    }
                }
            }
        }
    }]
}
```
</details>

<details><summary>The same example but requesting the verifiable presentation with proof type BbsBlsSignatureProof2020 instead</summary>

```json
{
    "@type": "https://didcomm.org/present-proof/%VER/request-presentation",
    "@id": "0ac534c8-98ed-4fe3-8a41-3600775e1e92",
    "comment": "some comment",
    "formats" : [{
        "attach_id" : "ed7d9b1f-9eed-4bde-b81c-3aa7485cf947",
        "format" : "dif/presentation-exchange/definition@v1.0"
    }],
    "request_presentations~attach": [{
        "@id": "ed7d9b1f-9eed-4bde-b81c-3aa7485cf947",
        "mime-type": "application/json",
        "data":  {
            "json": {
                "options": {
                    "challenge": "23516943-1d79-4ebd-8981-623f036365ef",
                    "domain": "us.gov/DriversLicense"
                },
                "presentation_definition": {
                    "input_descriptors": [{
                        "id": "citizenship_input",
                        "name": "US Passport",
                        "group": ["A"],
                        "schema": [{
                            "uri": "hub://did:foo:123/Collections/schema.us.gov/passport.json"
                        }],
                        "constraints": {
                            "fields": [{
                                "path": ["$.credentialSubject.birth_date", "$.vc.credentialSubject.birth_date", "$.birth_date"],
                                "filter": {
                                    "type": "date",
                                    "minimum": "1999-5-16"
                                }
                            }],
                            "limit_disclosure": "required"
                        }
                    }],
                    "format": {
                        "ldp_vc": {
                            "proof_type": ["BbsBlsSignatureProof2020"]
                        }
                    }
                }
            }
        }
    }]
}
```
</details>


### `presentation` attachment format

Format identifier: `dif/presentation-exchange/submission@v1.0`

The contents of the attachment is a Presentation Submission in a standard Verifiable Presentation format containing the proofs requested.

#### Examples: presentation

<details><summary>Complete message example</summary>

```json
{
    "@type": "https://didcomm.org/present-proof/%VER/presentation",
    "@id": "f1ca8245-ab2d-4d9c-8d7d-94bf310314ef",
    "comment": "some comment",
    "formats" : [{
        "attach_id" : "2a3f1c4c-623c-44e6-b159-179048c51260",
        "format" : "dif/presentation-exchange/submission@v1.0"
    }],
    "presentations~attach": [{
        "@id": "2a3f1c4c-623c-44e6-b159-179048c51260",
        "mime-type": "application/ld+json",
        "data": {
            "json": {
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
                }],
                "proof": {
                    "type": "RsaSignature2018",
                    "created": "2018-09-14T21:19:10Z",
                    "proofPurpose": "authentication",
                    "verificationMethod": "did:example:ebfeb1f712ebc6f1c276e12ec21#keys-1",
                    "challenge": "1f44d55f-f161-4938-a659-f8026467f126",
                    "domain": "4jt78h47fh47",
                    "jws": "..."
                }
            }
        }
    }]
}
```
</details>


### Supported Features of Presentation-Exchange

Level of support for Presentation-Exchange features:

Feature|Notes
-------|-----
`presentation_definition.input_descriptors.id`|
`presentation_definition.input_descriptors.name`|
`presentation_definition.input_descriptors.purpose`|
`presentation_definition.input_descriptors.schema.uri`|URI for the credential's schema.
`presentation_definition.input_descriptors.constraints.fields.path`|Array of JSONPath string expressions as defined in [section 8](https://identity.foundation/presentation-exchange/#jsonpath-syntax-definition). REQUIRED as per the spec.
`presentation_definition.input_descriptors.constraints.fields.filter`|JSONSchema descriptor.
`presentation_definition.input_descriptors.constraints.limit_disclosure`|`preferred` or `required` as defined in [the spec](https://identity.foundation/presentation-exchange/#input-descriptor-object) and as supported by the Holder and Verifier proof mechanisms.<br>Note that the Holder MUST have credentials with cryptographic proof suites that are capable of selective disclosure in order to respond to a request with `limit_disclosure: "required"`.<br/>See [RFC0593](../0593-json-ld-cred-attach/README.md) for appropriate crypto suites.
`presentation_definition.input_descriptors.constraints.is_holder`|`preferred` or `required` as defined in [the spec](https://identity.foundation/presentation-exchange/#input-descriptor-object).<br>Note that this feature allows the Holder to present credentials with a different subject identifier than the DID used to establish the DIDComm connection with the Verifier.
`presentation_definition.format`|For JSONLD-based credentials: `ldp_vc` and `ldp_vp`.
`presentation_definition.format.proof_type`|For JSONLD-based credentials: `Ed25519Signature2018` and `BbsBlsSignature2020`.

### Proof Formats

#### Constraints

Verifiable Presentations MUST be produced and consumed using the [JSON-LD syntax](https://www.w3.org/TR/vc-data-model/#json-ld).

The proof types defined below MUST be registered in the [Linked Data Cryptographic Suite Registry](https://w3c-ccg.github.io/ld-cryptosuite-registry/).

The value of any `credentialSubject.id` in a credential MUST be a [Dentralized Identifier (DID)](https://w3c.github.io/did-core/)
conforming to the [DID Syntax](https://w3c.github.io/did-core/#did-syntax) if present. This allows the Holder to
authenticate as the credential's subject if required by the Verifier (see the `is_holder` property above). The Holder
authenticates as the credential's subject by attaching an LD Proof on the enclosing Verifiable Presentation.

#### Proof Formats on Credentials

Aries agents implementing this RFC MUST support the formats outlined in [RFC0593](../0593-json-ld-cred-attach/README.md#supported-proof-types)
for proofs on [Verifiable Credentials](https://www.w3.org/TR/vc-data-model/).

#### Proof Formats on Presentations

Aries agents implementing this RFC MUST support the formats outlined below for proofs on [Verifiable Presentations](https://www.w3.org/TR/vc-data-model/).

##### Ed25519Signature2018

[Specification](https://w3c-ccg.github.io/lds-ed25519-2018/).

**Request Parameters:**

* `presentation_definition.format`: `ldp_vp`
* `presentation_Definition.format.proof_type`: `Ed25519Signature2018`
* `options.challenge`: (Optional) a random string value generated by the Verifier
* `options.domain`: (Optional) a string value specified set by the Verifier

**Result:**

A [Verifiable Presentation](https://www.w3.org/TR/vc-data-model/#presentations-0) of type
[Presentation Submission](https://identity.foundation/presentation-exchange/#presentation-submission) containing the
credentials requested under the `verifiableCredential` property and a `proof` property of type `Ed25519Signature2018`.

<details><summary>Example</summary>

```json
{
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
        "id": "https://eu.com/claims/DriversLicense",
        "type": [
            "EUDriversLicense"
        ],
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
    }],
    "proof": {
      "type": "Ed25519Signature2018",
      "proofPurpose": "authentication",
      "created": "2017-09-23T20:21:34Z",
      "verificationMethod": "did:example:123456#key1",
      "challenge": "2bbgh3dgjg2302d-d2b3gi423d42",
      "domain": "example.org",
      "jws": "eyJ0eXAiOiJK...gFWFOEjXk"
  }
}
```
</details>

##### BbsBlsSignature2020

[Specification](https://w3c-ccg.github.io/ldp-bbs2020/).

Associated RFC: [RFC0646](../0646-bbs-credentials/README.md).

**Request Parameters**:
* `presentation_definition.format`: `ldp_vp`
* `presentation_Definition.format.proof_type`: `BbsBlsSignature2020`
* `options.challenge`: (Optional) a random string value generated by the Verifier
* `options.domain`: (Optional) a string value specified set by the Verifier

**Result:**

A [Verifiable Presentation](https://www.w3.org/TR/vc-data-model/#presentations-0) of type
[Presentation Submission](https://identity.foundation/presentation-exchange/#presentation-submission) containing the
credentials requested under the `verifiableCredential` property and a `proof` property of type `BbsBlsSignature2020`.

<details><summary>Example</summary>

```json
{
    "@context": [
        "https://www.w3.org/2018/credentials/v1",
        "https://w3id.org/security/v2",
        "https://w3id.org/security/bbs/v1",
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
           "type": "BbsBlsSignatureProof2020",
           "created": "2020-04-25",
           "verificationMethod": "did:example:489398593#test",
           "proofPurpose": "assertionMethod",
           "signature": "F9uMuJzNBqj4j+HPTvWjUN/MNoe6KRH0818WkvDn2Sf7kg1P17YpNyzSB+CH57AWDFunU13tL8oTBDpBhODckelTxHIaEfG0rNmqmjK6DOs0/ObksTZh7W3OTbqfD2h4C/wqqMQHSWdXXnojwyFDEg=="
       }
    }],
    "proof": {
        "type": "BbsBlsSignature2020",
        "created": "2020-04-25",
        "verificationMethod": "did:example:489398593#test",
        "proofPurpose": "authentication",
        "proofValue": "F9uMuJzNBqj4j+HPTvWjUN/MNoe6KRH0818WkvDn2Sf7kg1P17YpNyzSB+CH57AWDFunU13tL8oTBDpBhODckelTxHIaEfG0rNmqmjK6DOs0/ObksTZh7W3OTbqfD2h4C/wqqMQHSWdXXnojwyFDEg==",
        "requiredRevealStatements": [ 4, 5 ]
    }
}
```
</details>

> Note: The above example is for illustrative purposes. In particular, note that whether a Verifier requests a `proof_type`
> of `BbsBlsSignature2020` has no bearing on whether the Holder is required to present credentials with proofs of type
> `BbsBlsSignatureProof2020`. The choice of proof types on the credentials is constrained by a) the available types
> registered in RFC0593 and b) additional constraints placed on them due to other aspects of the proof requested by
> the Verifier, such as requiring limited disclosure with the `limit_disclosure` property. In such a case, a proof
> type of `Ed25519Signature2018` in the credentials is not appropriate whereas `BbsBlsSignatureProof2020` is capable
> of selective disclosure.

## Drawbacks

N/A


## Rationale and alternatives

- The `hlindy-zkp-v1.0` format is an alternative restricted to the Hyperledger Indy network.


## Prior art

- [OAuth 2.0 Rich Authorization Requests](https://tools.ietf.org/html/draft-lodderstedt-oauth-rar):
  Provides a coarse object structure that implementers must extend to support their needs. Presentation Exchange
  provides a rich set of operators out of the box.


## Unresolved questions

> TODO it is assumed the Verifier will initiate the protocol if they can transmit their presentation definition via an out-of-band channel
>  (eg. it is published on their website) with a `request-presentation` message, possibly delivered via an Out-of-Band invitation
>  (see [RFC0434](../0434-outofband/README.md)). For now, the Prover sends `propose-presentation` as a response to `request-presentation`.
  
  
## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the
implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent
in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

Name / Link | Implementation Notes
--- | ---
 | 

