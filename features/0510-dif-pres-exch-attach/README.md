# Aries RFC 0510: Presentation-Exchange Attachment format for requesting and presenting proofs

- Authors: George Aristy (SecureKey Technologies)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2020-07-21
- Status Note:  
- Supersedes: 
- Start Date: 2020-07-21
- Tags: [feature](/tags.md#feature), [protocol](/tags.md#protocol), [credentials](/tags.md#credentials), [test-anomaly](/tags.md#test-anomaly)


## Summary

This RFC registers an attachment format for use in the [present-proof V2](../0454-present-proof-v2/README.md) protocol based on
the Decentralized Identity Foundation's (DIF) [Presentation Exchange specification](https://identity.foundation/presentation-exchange/).

*Presentation Exchange* defines a data format capable of articulating a rich set of proof requirements from Verifiers,
and also provides a means of describing the formats in which Provers must submit those proofs.

A Verifier's defines their requirements in a `presentation_definition` containing `input_descriptors` that describe
the credential(s) the proof(s) must be derived from as well as a rich set of operators that place `constraints` on those proofs
(eg. "must be issued from issuer X" or "`age` over X", etc.). The Verifier may optionally specify `submission_requirement`s
that layer set-membership requirements on top of `input_descriptors`.

The Verifiable Presentation format of [Presentation Submissions](https://identity.foundation/presentation-exchange/#presentation-submission)
is used as opposed to OIDC tokens or CHAPI objects. For an alternative on how to tunnel OIDC messages over DIDComm, see
[HTTP-Over-DIDComm](../0335-http-over-didcomm/README.md). CHAPI is an alternative transport to DIDComm.


## Motivation

The *Presentation Exchange* specification possesses a rich language for expressing a Verifier's criterion.

The *Presentation Exchange* specification lends itself well to several transport mediums due to its limited scope as a data format,
and is easily transported over DIDComm.

It is furthermore desirable to make use of specifications developed in an open standards body.


## Tutorial

Complete examples of messages are provided in the [reference section](#reference).

The Verifier sends a `request-presentation` to the Prover containing a
[`presentation_definition`](https://identity.foundation/presentation-exchange/#presentation-definition), along with a
`domain` and `challenge` the Prover must sign over in the proof.

The Prover can optionally respond to the Verifier's `request-presentation` with a `propose-presentation` message containing
"Input Descriptors" that describe the proofs they can provide. The contents of the attachment is just the
`input_descriptors` attribute of the `presentation_definitions` object.

The Prover responds with a `presentation` message containing a
[`presentation_submission`](https://identity.foundation/presentation-exchange/#presentation-submission).


## Reference

### `propose-presentation` attachment format

Format identifier: `dif/presentation-exchange/definitions@v1.0`

Complete message example:

```json
{
    "@type": "https://didcomm.org/present-proof/%VER/propose-presentation",
    "@id": "fce30ed1-96f8-44c9-95cf-b274288009dc",
    "comment": "some comment",
    "formats" : [{
        "attach_id" : "143c458d-1b1c-40c7-ab85-4d16808ddf0a",
        "format" : "dif/presentation-exchange/definitions@v1.0"
    }],
    "proposal~attach": [{
        "@id": "143c458d-1b1c-40c7-ab85-4d16808ddf0a",
        "mime-type": "application/json",
        "data": {
            "json": {
                "input_descriptors": [{
                    "id": "citizenship_input",
                    "group": ["A"],
                    "schema": {
                        "uri": ["hub://did:foo:123/Collections/schema.us.gov/passport.json"],
                        "name": "US Passport"
                    },
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


### `request-presentation` attachment format

Format identifier: `dif/presentation-exchange/definitions@v1.0`

The contents of the attachment is a JSON object containing the Verifier's presentation definitions, a challenge and a domain:

```jsonc
{
    "challenge": "...",
    "domain": "...",
    "presentation_definitions": {
        // presentation definitions object
    }
}
```

Complete message example:

```json
{
    "@type": "https://didcomm.org/present-proof/%VER/request-presentation",
    "@id": "0ac534c8-98ed-4fe3-8a41-3600775e1e92",
    "comment": "some comment",
    "formats" : [{
        "attach_id" : "ed7d9b1f-9eed-4bde-b81c-3aa7485cf947",
        "format" : "dif/presentation-exchange/definitions@v1.0"
    }],
    "request_presentations~attach": [{
        "@id": "ed7d9b1f-9eed-4bde-b81c-3aa7485cf947",
        "mime-type": "application/json",
        "data":  {
            "json": {
                "challenge": "23516943-1d79-4ebd-8981-623f036365ef",
                "domain": "us.gov/DriversLicense",
                "presentation_definitions": {
                    "input_descriptors": [{
                        "id": "citizenship_input",
                        "group": ["A"],
                        "schema": {
                            "uri": ["hub://did:foo:123/Collections/schema.us.gov/passport.json"],
                            "name": "US Passport"
                        },
                        "constraints": {
                            "fields": [{
                                "path": ["$.credentialSubject.birth_date", "$.vc.credentialSubject.birth_date", "$.birth_date"],
                                "filter": {
                                    "type": "date",
                                    "minimum": "1999-5-16"
                                }
                            }]
                        }
                    }],
                    "submission_requirement": {
                        "name": "Credential issuance requirements",
                        "purpose": "Verify banking, employment, and citizenship information.",
                        "rule": "all",
                        "from": [{
                            "name": "Citizenship Information",
                            "rule": "pick",
                            "count": 1,
                            "from": "A"
                        }]
                    } 
                }
            }
        }
    }]
}
```


### `presentation` attachment format

Format identifier: `dif/presentation-exchange/submission@v1.0`

The contents of the attachment is a Presentation Submission in a standard Verifiable Presentation format containing the proofs requested.

Complete message example:

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


## Drawbacks

N/A


## Rationale and alternatives

- The `hlindy-zkp-v1.0` format is an alternative restricted to the Hyperledger Indy network.


## Prior art

- [OAuth 2.0 Rich Authorization Requests](https://tools.ietf.org/html/draft-lodderstedt-oauth-rar):
  Provides a coarse object structure that implementers must extend to support their needs. Presentation Exchange
  provides a rich set of operators out of the box.


## Unresolved questions

> TODO it is assumed the Verifier will initiate the protocol if they can transmit their presentation definitions via an out-of-band channel
>  (eg. it is published on their website) with a `request-presentation` message, possibly delivered via an Out-of-Band invitation
>  (see [RFC0434](../0434-outofband/README.md)). For now, the Prover sends `propose-presentation` as a response to `request-presentation`.
  
  
## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the
implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent
in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

Name / Link | Implementation Notes
--- | ---
 | 

