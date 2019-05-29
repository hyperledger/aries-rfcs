# Title (Ex. 0000: Template)
- Author: Nikita Khateev
- Start Date: 2019-01-30

## Status
- Status: [PROPOSED](/README.md#rfc-lifecycle)
- Status Date: 2019-05-28
- Status Note: This supersedes the Issue Credential part of [Indy HIPE PR #89](https://github.com/hyperledger/indy-hipe/blob/2e85595e9a948a2fbfd58400191d112caff5a14b/text/credential-exchange-message-family/README.md). See [Aries RFC 0037](../0037-present-proof) for the presentation part of the same Indy HIPE PR.

## Summary

Formalization and generalization of existing message formats used for issuing a credential according to existing RFCs about message formats.

## Motivation

We need to define standard protocols for credential issuance.

## Tutorial

The Issue Credential protocol consists of these messages:

* Propose Credential - Prover to Issuer (optional)
* Offer Credential - Issuer to Prover (optional for some credential implementations; required for Hyperledger Indy)
* Request Credential - Prover to Issuer
* Issue Credential - Issuer to Prover

In addition, the [ack](#) and [problem report](#) messages are adopted into the protocol for confirmation and error handling.

#### Choreography Diagram:

![issuance](credential-issuance.png)

#### Credential Proposal

This optional message is sent by the Prover to the Issuer to initiate credential issuance or in response to a Credential Offer when the Prover wants some fixes or changes to the credential data offered by Issuer. In Hyperledger Indy, where the Request Credential message can **only** be sent in response to an Offer Credential message, the Propose Credential message must be used by the Prover to initiate the protocol. Schema:

```json
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/issue-credential/1.0/propose-credential",
    "@id": "<uuid-propose-credential>",
    "comment": "some comment",
    "credential_proposal": <json-ld object>,
    "schema_id": "Schema ID string",
    "cred_def_id": "Credential Definition ID string"
}
```

Description of attributes:

* `comment` -- a field that provides some human readable information about this Credential Proposal;
* `credential_proposal` -- a JSON-LD object that represents the credential data that Prover wants to receive. It matches the schema of [Credential Preview](#preview_credential);
* `schema_id` -- optional filter to request credential based on particular Schema
* `cred_def_id` -- optional filter to request credential based on particular Credential Definition

#### Offer Credential

This message is sent by the Issuer to the Prover to initiate credential issuance when required by the Credential flow. In Hyperledger Indy, this message is required. Schema:

```json
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/issue-credential/1.0/offer-credential",
    "@id": "<uuid-offer>",
    "comment": "some comment",
    "credential_preview": <json-ld object>,
    "offers~attach": [
        {
            "nickname": "libindy-offer",
            "mime-type": "application/json",
            "content": {
                "base64": "<bytes for base64>"
            }
        }
    ]
}
```

Description of fields:

* `comment` -- a field that provides some human readable information about this Credential Offer;
* `credential_preview` -- a JSON-LD object that represents the credential data that Issuer is willing to issue. It matches the schema of [Credential Preview](#preview_credential);
* `offers~attach` -- an array of attachments defining the offered formats for the credential.
  * For Indy, the attachment contains data from libindy about the credential offer, base64 encoded. The following JSON is an example of the `libindy-offer` attachment content. For more information see the [Libindy API](https://github.com/hyperledger/indy-sdk/blob/57dcdae74164d1c7aa06f2cccecaae121cefac25/libindy/src/api/anoncreds.rs#L280).

```json
{
   "schema_id": string,
   "cred_def_id": string,
   "nonce": string,
   "key_correctness_proof" : <key_correctness_proof>
}
```

#### Request Credential

This message is sent by the Prover to the Issuer to request the issuance of a Credential. Where supported by the Credential implementation, this message initiates the protocol. In Hyperledger Indy, this message can only be sent in response to an Offer Credential message. Schema:

```json
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/issue-credential/1.0/request-credential",
    "@id": "<uuid-request>",
    "comment": "some comment",
    "requests~attach": [
        {
            "nickname": "libindy_cred_req",
            "mime-type": "application/json",
            "content": {
                "base64": "<bytes for base64>"
            }
        },
    ]
}
```

Description of Fields:

* `comment` -- a field that provides some human readable information about this request.
* `requests~attach` -- an array of attachments defining the requested formats for the credential.
  * For Indy, the attachment contains data from libindy about the credential request, base64 encoded. The following JSON is an example of the `libindy_cred_req` attachment content. For more information see the [Libindy API](https://github.com/hyperledger/indy-sdk/blob/57dcdae74164d1c7aa06f2cccecaae121cefac25/libindy/src/api/anoncreds.rs#L658).

```json
{
  "prover_did" : string,
  "cred_def_id" : string,
  "blinded_ms" : <blinded_master_secret>,
  "blinded_ms_correctness_proof" : <blinded_ms_correctness_proof>,
  "nonce": string
}
```

#### Issue Credential

This message contains the credentials being issued and is sent in response to a valid Request Credential message. Schema:

```json
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/issue-credential/1.0/issue-credential",
    "@id": "<uuid-credential>",
    "comment": "some comment",
    "credentials~attach": [
        {
            "nickname": "libindy-cred",
            "mime-type": "application/json",
            "content": {
                "base64": "<bytes for base64>"  
            }
        }
    ]
}
```

Description of fields:

* `comment` -- a field that provides some human readable information about the issued Credential.
* `credentials~attach` -- an array of attachments containing the issued credentials.
  * For Indy, the attachment contains data from libindy about credential to be issued, base64 encoded. The following JSON is an example of the `libindy-cred` attachment content. For more information see the [Libindy API](https://github.com/hyperledger/indy-sdk/blob/57dcdae74164d1c7aa06f2cccecaae121cefac25/libindy/src/api/anoncreds.rs#L338).

```json
{
    "schema_id": string,
    "cred_def_id": string,
    "rev_reg_def_id": Optional<string>,
    "values": <see cred_values_json above>,
    "signature": <signature>,
    "signature_correctness_proof": <signature_correctness_proof>
}
```

#### Preview Credential

This is not a message but an inner object for other messages in this protocol. It is used construct a preview of the data for the credential that is to be issued. Schema:

```json
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/issue-credential/1.0/credential-preview",
    "attributes": [
        {
            "name": "attribute name",
            "mime-type": "type",
            "value": "value"
        },
        ...
    ]
}
```

The main field here is `attributes`. It is an array of objects with three fields in it:

* `name` -- string with attribute name;
* `mime-type` -- type of attribute
* `value` -- value of credential

## Threading

Threading can be used to initiate a sub-protocol during an issue credential protocol instance. For example, during credential issuance, the Issuer may initiate a child thread to execute the `Present Proof` sub-protocol to have the Prover prove attributes about themselves before issuing the credential.

Details about threading can be found in the [message id and threading](../../concepts/0008-message-id-and-threading/README.md) RFC.

## Negotiation and Preview

Negotiation prior to issuing the credential can be done using the `offer-credential` and `propose-credential` messages. A common negotiation use case would be about the data to go into the credential. For that, the `credential_preview` element is used.

## Reference

* [VCX](https://github.com/hyperledger/indy-sdk/tree/master/vcx/libvcx/src/api) -- this implementation might not be perfect and needs to be improved, you can gather some info on parameters purpose from it
* A pre-RFC (labelled version 0.1) implementation of the protocol was implemented by a number of groups in the Hyperledger Indy community leading up to IIW28 in April 2019. The protocol defined and implemented can be reviewed [here](https://hackmd.io/s/HkklVzww4). It was the basis of the [IIWBook demo](https://vonx.io/how_to/iiwbook) from BC Gov and collaborators.

## Drawbacks

Why should we *not* do this?

## Rationale and alternatives

- Why is this design the best in the space of possible designs?
- What other designs have been considered and what is the rationale for not
choosing them?
- What is the impact of not doing this?

## Prior art

Similar (but simplified) credential exchanged was already implemented in [von-anchor](https://von-anchor.readthedocs.io/en/latest/).

## Unresolved questions

- We might need to propose a new MIME type for credential (the same way as .docx is not processed as generic xml). The issue in W3C/vc-data-model: https://github.com/w3c/vc-data-model/issues/421
- It is a common practice when changing some attributes in credential to revoke the old credential and issue a new one. It might be useful to have an element in the `offer-credential` message to indicate a connection between a now revoked credential and the new credential being offered.
- We might need some explicit documentation for nested `@type` fields.
- There should be a way to ask for some payment with `offer-credential` and to send a payment (or payment receipt) in the request-credential.
