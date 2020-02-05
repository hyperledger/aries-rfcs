# Aries RFC 0036: Issue Credential Protocol 1.0

- Authors: Nikita Khateev
- Status: [ACCEPTED](/README.md#accepted)
- Since: 2019-05-28
- Status Note:  See [RFC 0037](../0037-present-proof/README.md) for the presentation part of using credentials.
- Supersedes: [Indy HIPE PR #89]( https://github.com/hyperledger/indy-hipe/blob/2e85595e9a948a2fbfd58400191d112caff5a14b/text/credential-exchange-message-family/README.md); also [Credential Exchange 0.1 -- IIW 2019](https://hackmd.io/@QNKW9ANJRy6t81D7IfgiZQ/HkklVzww4?type=view)
- Start Date: 2019-01-30
- Tags: [feature](/tags.md#feature), [decorator](/tags.md#decorator), [protocol](/tags.md#protocol), [credentials](/tags.md#credentials), [test-anomaly](/tags.md#test-anomaly)

## Version Change Log

### 1.1/propose-credential

In version 1.1 of the propose-credential message, the following optional fields were added:
schema_name, schema_version, and issuer_did.

The previous version is [1.0/propose-credential](https://github.com/hyperledger/aries-rfcs/blob/527849e/features/0036-issue-credential/README.md#propose-credential).

## Summary

Formalizes messages used to issue a credential--whether the credential is JWT-oriented, JSON-LD-oriented, or ZKP-oriented. The general flow is similar, and this protocol intends to handle all of them. If you are using a credential type that doesn't fit this protocol, please [raise a Github issue](/github-issues.md).

## Motivation

We need a standard protocol for issuing credentials. This is the basis of interoperability between Issuers and Holders.

## Tutorial

### Roles

There are two roles in this protocol: Issuer and Holder. Technically, the latter role is only potential until the protocol completes; that is, the second party becomes a Holder of a credential by completing the protocol. However, we will use the term Holder throughout, to keep things simple.

>Note: When a holder of credentials turns around and uses those credentials to prove something, they become a Prover. In the sister RFC to this one, [0037: Present Proof](../0037-present-proof/README.md), the Holder is therefore renamed to Prover. Sometimes in casual conversation, the Holder role here might be called "Prover" as well, but more formally, "Holder" is the right term at this phase of the credential lifecycle.

### States

The choreography diagrams shown below detail how state evolves in this protocol, in a "happy path."

Errors might occur in various places. For example, an Issuer might offer a credential for a price that the Holder is unwilling to pay. All errors are modeled with a `problem-report` message. Easy-to-anticipate errors reset the flow as shown in the diagrams, and use the code `issuance-abandoned`; more exotic errors (e.g., server crashed at Issuer headquarters in the middle of a workflow) may have different codes but still cause the flow to be abandoned in the same way.

### Messages

The Issue Credential protocol consists of these messages:

* `propose-credential` - potential Holder to Issuer (optional). Tells what the Holder hopes to receive.
* `offer-credential` - Issuer to potential Holder (optional for some credential implementations; required for Hyperledger Indy). Tells what the Issuer intends to issue, and possibly, the price the Issuer expects to be paid.
* `request-credential` - potential Holder to Issuer. If neither of the previous message types is used, this is the message that begins the protocol.
* `issue-credential` - Issuer to new Holder. Attachment payload contains the actual credential.

In addition, the [`ack`](../0015-acks/README.md) and [`problem-report`](../0035-report-problem/README.md) messages are adopted into the protocol for confirmation and error handling.

>Note: This protocol is about the messages that must be exchanged to issue verifiable credentials, NOT about the specifics of particular verifiable credential schemes. [DIDComm attachments](../../concepts/0017-attachments/README.md) are deliberately used in messages to isolate the protocol flow/semantics from the credential artifacts themselves as separate constructs. Attachments allow credential formats and this protocol to evolve through versioning milestones independently instead of in lockstep. Links are provided in the message descriptions below, to describe how the protocol adapts to specific verifiable credential implementations.

#### Choreography Diagram

<blockquote>
Note: This diagram was made in draw.io. To make changes:

- upload the drawing HTML from this folder to the [draw.io](https://draw.io) site (Import From...GitHub), 
- make changes,
- export the picture and HTML to your local copy of this repo, and
- submit a pull request.
</blockquote>

The protocol has 3 alternative beginnings:

1. The Issuer can begin with an offer.
2. The Holder can begin with a proposal.
3. the Holder can begin with a request.

The offer and proposal messages are part of an optional negotiation phase and may trigger back-and-forth counters. A request is not subject to negotiation; it can only be accepted or rejected.

![issuance](credential-issuance.png)

#### Propose Credential

An optional message sent by the potential Holder to the Issuer to initiate the protocol or in response to a `offer-credential` message when the Holder wants some adjustments made to the credential data offered by Issuer.

>Note: In Hyperledger Indy, where the `request-credential` message can **only** be sent in response to an `offer-credential` message, the `propose-credential` message is the only way for a potential Holder to initiate the workflow.
 
 Schema:

```json
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/issue-credential/1.1/propose-credential",
    "@id": "<uuid-of-propose-message>",
    "comment": "some comment",
    "credential_proposal": <json-ld object>,
    "schema_issuer_did": "DID of the proposed schema issuer",
    "schema_id": "Schema ID string",
    "schema_name": "Schema name string",
    "schema_version": "Schema version string",
    "cred_def_id": "Credential Definition ID string"
    "issuer_did": "DID of the proposed issuer"
}
```

Description of attributes:

* `comment` -- an optional field that provides human readable information about this Credential Proposal, so the proposal can be evaluated by human judgment. Follows [DIDComm conventions for l10n](../0043-l10n/README.md).
* `credential_proposal` -- an optional JSON-LD object that represents the credential data that Prover wants to receive. It matches the schema of [Credential Preview](#preview-credential).
* `schema_issuer_did` -- optional filter to request credential based on a particular Schema issuer DID.
* `schema_id` -- optional filter to request credential based on a particular Schema. This might be helpful when requesting a version 1 passport instead of a version 2 passport, for example.
* `schema_name` -- optional filter to request credential based on a schema name. This is useful to allow a more user-friendly experience of requesting a credential by schema name.
* `schema_version` -- optional filter to request credential based on a schema version. This is useful to allow a more user-friendly experience of requesting a credential by schema name and version.
* `cred_def_id` -- optional filter to request credential based on a particular Credential Definition. This might be helpful when requesting a commercial driver's license instead of an ordinary driver's license, for example.
* `issuer_did` -- optional filter to request a credential issued by the owner of a particular DID.

#### Offer Credential

A message sent by the Issuer to the potential Holder, describing the credential they intend to offer and possibly the price they expect to be paid. In Hyperledger Indy, this message is required, because it forces the Issuer to make a cryptographic commitment to the set of fields in the final credential and thus prevents Issuers from inserting spurious data. In credential implementations where this message is optional, an Issuer can use the message to negotiate the issuing following receipt of a `request-credential` message.

Schema:

```json
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/issue-credential/1.0/offer-credential",
    "@id": "<uuid-of-offer-message>",
    "comment": "some comment",
    "credential_preview": <json-ld object>,
    "offers~attach": [
        {
            "@id": "libindy-cred-offer-0",
            "mime-type": "application/json",
            "data": {
                "base64": "<bytes for base64>"
            }
        }
    ]
}
```

Description of fields:

* `comment` -- an optional field that provides human readable information about this Credential Offer, so the offer can be evaluated by human judgment. Follows [DIDComm conventions for l10n](../0043-l10n/README.md).
* `credential_preview` -- a JSON-LD object that represents the credential data that Issuer is willing to issue. It matches the schema of [Credential Preview](#preview-credential);
* `offers~attach` -- an array of attachments that further define the credential being offered. This might be used to clarify which formats or format versions will be issued.
  * For Indy, the attachment includes a nonce and key correctness proof to facilitate integrity checks. It is a base64-encoded version of the data returned from [`indy_issuer_create_credential_offer()`](https://github.com/hyperledger/indy-sdk/blob/57dcdae74164d1c7aa06f2cccecaae121cefac25/libindy/src/api/anoncreds.rs#L280).

The Issuer may add a [`~payment-request` decorator](../0075-payment-decorators/README.md#payment_request) to this message to convey the need for payment before issuance. See the [payment section below](#payments-during-credential-exchange) for more details.

It is possible for an Issuer to add a [`~timing.expires_time` decorator](../0032-message-timing/README.md#tutorial) to this message to convey the idea that the offer will expire at a particular point in the future. Such behavior is not a special part of this protocol, and support for it is not a requirement of conforming implementations; the `~timing` decorator is simply a general possibility for any DIDComm message. We mention it here just to note that the protocol can be enriched in composable ways.

#### Request Credential

This is a message sent by the potential Holder to the Issuer, to request the issuance of a credential. Where circumstances do not require a preceding Offer Credential message (e.g., there is no cost to issuance that the Issuer needs to explain in advance, and there is no need for cryptographic negotiation), this message initiates the protocol. In Hyperledger Indy, this message can only be sent in response to an Offer Credential message.

Schema:

```json
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/issue-credential/1.0/request-credential",
    "@id": "<uuid-of-request-message>",
    "comment": "some comment",
    "requests~attach": [
        {
            "@id": "attachment id",
            "mime-type": "application/json",
            "data": {
                "base64": "<bytes for base64>"
            }
        },
    ]
}
```

Description of Fields:

* `comment` -- an optional field that provides human readable information about this Credential Request, so it can be evaluated by human judgment. Follows [DIDComm conventions for l10n](../0043-l10n/README.md).
* `requests~attach` -- an array of [attachments](../../concepts/0017-attachments/README.md) defining the requested formats for the credential.
  * For Indy, the attachment is a base64-encoded version of the data returned from [`indy_prover_create_credential_req()`](https://github.com/hyperledger/indy-sdk/blob/57dcdae74164d1c7aa06f2cccecaae121cefac25/libindy/src/api/anoncreds.rs#L658).

This message may have a [`~payment-receipt` decorator](../0075-payment-decorators/README.md#payment_receipt) to prove to the Issuer that the potential Holder has satisfied a payment requirement. See the [payment section below](#payments-during-credential-exchange).

#### Issue Credential

This message contains as [attached payload](../../concepts/0017-attachments/README.md) the credentials being issued and is sent in response to a valid Request Credential message.

Schema:

```json
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/issue-credential/1.0/issue-credential",
    "@id": "<uuid-of-issue-message>",
    "comment": "some comment",
    "credentials~attach": [
        {
            "@id": "libindy-cred-0",
            "mime-type": "application/json",
            "data": {
                "base64": "<bytes for base64>"
            }
        }
    ]
}
```

Description of fields:

* `comment` -- an optional field that provides human readable information about the issued credential, so it can be evaluated by human judgment. Follows [DIDComm conventions for l10n](../0043-l10n/README.md).
* `credentials~attach` -- an array of attachments containing the issued credentials.
  * For Indy, the attachment contains data from libindy about credential to be issued, base64-encoded, as returned from `libindy`. For more information see the [Libindy API](https://github.com/hyperledger/indy-sdk/blob/57dcdae74164d1c7aa06f2cccecaae121cefac25/libindy/src/api/anoncreds.rs#L338).
  
If the issuer wants an acknowledgement that the issued credential was accepted, this message must be decorated with `~please-ack`, and it is then best practice for the new Holder to respond with an explicit `ack` message as described in [0317: Please ACK Decorator](../0317-please-ack/README.md).

##### Encoding Claims for Indy-based Verifiable Credentials

Claims in Hyperledger Indy-based verifiable credentials are put into the credential in two forms, `raw` and `encoded`. `raw` is the actual data value, and `encoded` is the (possibly derived) integer value that is used in presentations. At this time, Indy does not take an opinion on the method used for encoding the raw value. This will change with the Rich Schema work that is underway in the Indy/Aries community, where the encoding method will be part of the credential metadata available from the public ledger.

Until the Rich Schema mechanism is deployed, Aries issuers and verifiers must agree on the encoding method so that the verifier can check that the `raw` value returned in a presentation corresponds to the proven `encoded` value. The following is the encoding algorithm that MUST be used by Issuers when creating credentials and SHOULD be verified by Verifiers receiving presentations:

- keep any 32-bit integer as is
- for data of any other type:
  - convert to string (use string "None" for null)
  - encode via utf-8 to bytes
  - apply SHA-256 to digest the bytes
  - convert the resulting digest bytes, big-endian, to integer
  - stringify the integer as a decimal.

An example implementation in Python can be found [here](https://github.com/hyperledger/aries-cloudagent-python/blob/0000f924a50b6ac5e6342bff90e64864672ee935/aries_cloudagent/messaging/util.py#L106).

A gist of test value pairs can be found [here](https://gist.github.com/swcurran/78e5a9e8d11236f003f6a6263c6619a6).

#### Preview Credential

This is not a message but an inner object for other messages in this protocol. It is used construct a preview of the data for the credential that is to be issued. Its schema follows:

```jsonc
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/issue-credential/1.0/credential-preview",
    "attributes": [
        {
            "name": "<attribute name>",
            "mime-type": "<type>",
            "value": "<value>"
        },
        // more attributes
    ]
}
```

The main element is `attributes`. It is an array of (object) attribute specifications; the subsections below outline their semantics.

##### Attribute Name

The mandatory `"name"` key maps to the attribute name as a string.

##### MIME Type and Value

The optional `mime-type` advises the issuer how to render a binary attribute, to judge its content for applicability before issuing a credential containing it. Its value parses case-insensitively in keeping with MIME type semantics of [RFC 2045](https://tools.ietf.org/html/rfc2045). If `mime-type` is missing, its value is null.

The mandatory `value` holds the attribute value:

* if `mime-type` is missing (null), then `value` is a string. In other words, implementations interpret it the same as any other key+value pair in JSON
* if `mime-type` is not null, then `value` is always a base64-encoded string that represents a binary BLOB, and `mime-type` tells how to interpret the BLOB after base64-decoding.

## Threading

Threading can be used to initiate a [sub-protocol](../../concepts/0003-protocols/README.md#composable) during an issue credential protocol instance. For example, during credential issuance, the Issuer may initiate a child message thread to execute the `Present Proof` sub-protocol to have the potential Holder (now acting as a Prover) prove attributes about themselves before issuing the credential. Depending on circumstances, this might be a best practice for preventing credential fraud at issuance time.

If threading were added to all of the above messages, a `~thread` decorator would be present, and later messages in the flow would reference the `@id` of earlier messages to stitch the flow into a single coherent sequence. Details about threading can be found in the [0008: Message ID and Threading](../../concepts/0008-message-id-and-threading/README.md) RFC.

## Payments during credential exchange

Credentialing ecosystems may wish to associate credential issuance with payments by fiat currency or tokens. This is common with non-digital credentials today; we pay a fee when we apply for a passport or purchase a plane ticket. Instead or in addition, some circumstances may fit a mode where payment is made each time a credential is *used*, as when a Verifier pays a Prover for verifiable medical data to be used in research, or when a Prover pays a Verifier as part of a workflow that applies for admittance to a university. For maximum flexibility, we mention payment possibilities here as well as in the sister [0037: Present Proof](../0037-present-proof/README.md) RFC.

### Payment decorators
Wherever they happen and whoever they involve, payments are accomplished with optional payment decorators. See [0075: Payment Decorators](../0075-payment-decorators/README.md).

### Payment flow

A `~payment-request` may decorate a Credential Offer from Issuer to Holder. When they do, a corresponding `~payment-receipt` should be provided on the Credential Request returned to the Issuer.

During credential presentation, the Verifier may pay the Holder as compensation for Holder for disclosing data. This would require a `~payment-request` in a Presentation Proposal message, and a corresponding `~payment-receipt` in the subsequent Presentation Request. If such a workflow begins with the Presentation Request, the Prover may sending back a Presentation (counter-)Proposal with appropriate decorator inside it.

### Limitations

Smart contracts may be missed in ecosystem, so operation "issue credential after payment received" is not atomic. It’s possible case that malicious issuer will charge first and then will not issue credential in fact. But this situation should be easily detected and appropriate penalty should be applied in such type of networks.


## Negotiation and Preview

Negotiation prior to issuing the credential can be done using the `offer-credential` and `propose-credential` messages. A common negotiation use case would be about the data to go into the credential. For that, the `credential_preview` element is used.

## Reference

* [VCX](https://github.com/hyperledger/indy-sdk/tree/master/vcx/libvcx/src/api) -- this implementation might not be perfect and needs to be improved, you can gather some info on parameters' purpose from it
* A pre-RFC (labelled version 0.1) implementation of the protocol was implemented by a number of groups in the Hyperledger Indy community leading up to IIW28 in April 2019. The protocol defined and implemented can be reviewed [here](https://hackmd.io/@QNKW9ANJRy6t81D7IfgiZQ/HkklVzww4?type=view). It was the basis of the [IIWBook demo](https://vonx.io/how_to/iiwbook) from BC Gov and collaborators.

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

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

Name / Link | Implementation Notes
--- | ---
 |  |
