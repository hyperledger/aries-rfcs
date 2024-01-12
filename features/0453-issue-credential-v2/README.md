# Aries RFC 0453: Issue Credential Protocol 2.0

- Authors: Nikita Khateev, Stephen Klump, Stephen Curran
- Status: [ACCEPTED](/README.md#accepted)
- Since: 2021-04-15
- Status Note:  See [RFC 0454](../0454-present-proof-v2/README.md) for the presentation part of using credentials. Version 2.1 adds issuing multiple credentials in one protocol instance.
- Supersedes: [RFC 0036 Issue Credential v1.x](../0036-issue-credential/README.md)
- Start Date: 2020-03-23
- Tags: [feature](/tags.md#feature), [decorator](/tags.md#decorator), [protocol](/tags.md#protocol), [credentials](/tags.md#credentials), [test-anomaly](/tags.md#test-anomaly)

## Version Change Log

### 2.2 - Addition of Supplements

An optional mechanism for providing credential supplements during issuance. Supplements are also used in credential presentation.

### 2.1 - Add ability to issue multiple credentials

A minor update to add a mechanism for an Issuer to indicate to the Holder that multiple credentials of the same type but with different claim values are available to be issued as part of the execution of the protocol instance.

An example use of this capability is a University (Issuer) offering multiple "proof of diploma" credentials to an alumni (Holder) with multiple degrees. A second example is a Bank (Issuer) offering a customer (Holder) a series of "bank account" verifiable credentials, one per bank account the customer has with the bank.

As with all DIDComm protocols and as described in [RFC 0003 Protocols](../../concepts/0003-protocols/README.md#semver-examples), an agent should accept and process any `2.x` version of this protocol by ignoring any unrecognized parameters and
responding with messages that explicit state the minor version of the protocol supported by the agent. An agent supporting a later version of the protocol may have to compensate. Specific places in this protocol where the agent needs
to detect the minor version of the other agent and respond accordingly are called out in the [Messages](#messages) section of this RFC.

### 2.0/propose-credential and identifiers

Version 2.0 of the protocol is introduced because of a breaking changes in the propose-credential message, replacing the (indy-specific) filtration criteria with a generalized filter attachment to align with the rest of the messages in the protocol. The previous version is [1.1/propose-credential](../0036-issue-credential/README.md).
Version 2.0 also uses &lt;angle brackets&gt; explicitly to mark all values that may vary between instances, such as identifiers and comments.

The "formats" field is added to all the messages to enable the linking the specific attachment IDs with the the format (credential format and version) of the attachment.

The details that are part of each message type about the different attachment formats serves as a registry of the known formats and versions.

## Summary

Formalizes messages used to issue a credential--whether the credential is JWT-oriented, JSON-LD-oriented, or ZKP-oriented. The general flow is similar, and this protocol intends to handle all of them. If you are using a credential type that doesn't fit this protocol, please [raise a Github issue](/github-issues.md).

## Motivation

We need a standard protocol for issuing credentials. This is the basis of interoperability between Issuers and Holders.

## Tutorial

### Name and Version

`issue-credential`, version 2.1

### Roles

There are two roles in this protocol: Issuer and Holder. Technically, the latter role is only potential until the protocol completes; that is, the second party becomes a Holder of a credential by completing the protocol. However, we will use the term Holder throughout, to keep things simple.

>Note: When a holder of credentials turns around and uses those credentials to prove something, they become a Prover. In the sister RFC to this one, [0454: Present Proof Protocol 2.0](../0454-present-proof-v2/README.md), the Holder is therefore renamed to Prover. Sometimes in casual conversation, the Holder role here might be called "Prover" as well, but more formally, "Holder" is the right term at this phase of the credential lifecycle.

### Goals

When the goals of each role are not available because of context, goal codes may be specifically included in protocol messages. This is particularly helpful to differentiate between credentials passed between the same parties for several different reasons. A goal code included should be considered to apply to the entire thread and is not necessary to be repeated on each message. Changing the goal code may be done by including the new code in a message. All goal codes are optional, and without default.

### States

The choreography diagram [below](#choreography-diagram) details how state evolves in this protocol, in a "happy path." The states include

#### Issuer States

* proposal-received
* offer-sent
* request-received
* credential-issued
* done

#### Holder States

* proposal-sent
* offer-received
* request-sent
* credential-received
* done

Errors might occur in various places. For example, an Issuer might offer a credential for a price that the Holder is unwilling to pay. All errors are modeled with a `problem-report` message. Easy-to-anticipate errors reset the flow as shown in the diagrams, and use the code `issuance-abandoned`; more exotic errors (e.g., server crashed at Issuer headquarters in the middle of a workflow) may have different codes but still cause the flow to be abandoned in the same way. That is, in this version of the protocol, all errors cause the state of both parties (the sender and the receiver of the `problem-report`) to revert to `null` (meaning it is no longer engaged in the protocol at all). Future versions of the protocol may allow more granular choices (e.g., requesting and receiving a (re-)send of the `issue-credential` message if the Holder times out while waiting in the `request-sent` state).

For the most part, these states map onto the transitions shown in the choreography diagram ([below](#choreography-diagram)) in obvious ways. However, a few subtleties are worth highlighting:

* The Issuer may indicate in the `offer-credential` message that multiple verifiable credentials are available to be issued.
* If multiple verifiable credentials are available, the Issuer may indicate in the `issue-credential` message that one or more verifiable credentials are still to be issued.
* If in the `issue-credential` message the Issuer indicates that one or more verifiable credentials are still to be issued:
  * The Holder may send a `request-credential` message to trigger the sending of the next credential.
  * The Holder may indicate it is not interested in being issued more verifiable credentials by sending a `problem-report` to indicate the end of the protocol.
* The final states for both the prover and verifier is `done` and once reached, no further updates to the protocol instance are expected.

### Messages

The Issue Credential protocol consists of these messages:

* `propose-credential` - potential Holder to Issuer (optional). Tells what the Holder hopes to receive.
* `offer-credential` - Issuer to potential Holder (optional for some credential implementations; required for Hyperledger Indy). Tells what the Issuer intends to issue, and possibly, the price the Issuer expects to be paid.
* `request-credential` - potential Holder to Issuer. If neither of the previous message types is used, this is the message that begins the protocol.
* `issue-credential` - Issuer to new Holder. Attachment payload contains the actual credential.

In addition, the [`ack`](../0015-acks/README.md) and [`problem-report`](../0035-report-problem/README.md) messages are adopted into the protocol for confirmation and error handling.

#### Message Attachments

This protocol is about the messages that must be exchanged to issue verifiable credentials, NOT about the specifics of particular verifiable credential schemes. [DIDComm attachments](../../concepts/0017-attachments/README.md) are deliberately used in messages to isolate the protocol flow/semantics from the credential artifacts themselves as separate constructs. Attachments allow credential formats and this protocol to evolve through versioning milestones independently instead of in lockstep. Links are provided in the message descriptions below, to describe how the protocol adapts to specific verifiable credential implementations.

The attachment items in the messages are arrays. The arrays are provided to support the issuing of different credential formats (e.g. ZKP, JSON-LD JWT, or other) containing the same data (claims). The arrays are not to be used for issuing credentials with different claims. The `formats` field of each message associates each attachment with the format (and version) of the attachment.

A registry of attachment formats is provided in this RFC within the message type sections. A sub-section should be added for each attachment format type (and optionally, each version). Updates to the attachment type formats does **NOT** impact the versioning of the Issue Credential protocol. Formats are flexibly defined. For example, the first definitions are for `hlindy/cred-abstract@v2.0` et al., assuming that all Hyperledger Indy implementations and ledgers will use a common format. However, if a specific instance of Indy uses a different format, another format value can be documented as a new registry entry.

Any of the [0017-attachments RFC](../../concepts/0017-attachments/README.md#json) embedded inline attachments can be used. In the examples below, `base64` is used in most cases, but implementations MUST expect any of the formats.

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

An optional message sent by the potential Holder to the Issuer to initiate the protocol or in response to an `offer-credential` message when the Holder wants some adjustments made to the credential data offered by Issuer.

<blockquote>
Note: In Hyperledger Indy, where the `request-credential` message can **only** be sent in response to an `offer-credential` message, the `propose-credential` message is the only way for a potential Holder to initiate the workflow.
</blockquote>

Message format:

```json
{
    "@type": "https://didcomm.org/issue-credential/%VER/propose-credential",
    "@id": "<uuid of propose-message>",
    "goal_code": "<goal-code>",
    "comment": "<some comment>",
    "credential_preview": <json-ld object>,
    "formats" : [
        {
            "attach_id" : "<attach@id value>",
            "format" : "<format-and-version>"
        }
    ],
    "filters~attach": [
        {
            "@id": "<attachment identifier>",
            "mime-type": "application/json",
            "data": {
                "base64": "<bytes for base64>"
            }
        }
    ],
    "supplements": [
        {
            "type": "hashlink-data",
            "ref": "<attachment identifier>",
            "attrs": [{
                "key": "field",
                "value": "<fieldname>"
            }]
        },
        {
            "type": "issuer-credential",
            "ref": "<attachment identifier>",
        }
    ],
    "~attach" : [] //attachments referred to in supplements
}
```

Description of attributes:

* `goal_code` -- optional field that indicates the goal of the message sender. 
* `comment` -- an optional field that provides human readable information about this Credential Proposal, so the proposal can be evaluated by human judgment. Follows [DIDComm conventions for l10n](../0043-l10n/README.md).
* `credential_preview` -- an optional JSON-LD object that represents the credential data that Prover wants to receive. It matches the schema of [Credential Preview](#preview-credential).
* `formats` -- contains an entry for each `filters~attach` array entry, providing the the value of the attachment `@id` and the verifiable credential format and version of the attachment. Accepted values for the `format` items are provided in the per format "Attachment" sections immediately below.
* `filters~attach` -- an array of attachments that further define the credential being proposed. This might be used to clarify which formats or format versions are wanted.
* `supplements` -- an optional array of attachment descriptors detailing credential supplements. See the [Supplements Section](#supplements) for details.
* `~attach` -- optional attachments related to the proposed credential. Each attachment should be detailed in a `supplements` entry, referenced by attachment identifier.

##### Propose Attachment Registry

Credential Format | Format Value | Link to Attachment Format | Comment |
--- | --- | --- | --- | 
DIF Credential Manifest | `dif/credential-manifest@v1.0` | [`propose-credential` attachment format](../0511-dif-cred-manifest-attach/README.md#propose-credential-attachment-format) | 
Linked Data Proof VC Detail  | `aries/ld-proof-vc-detail@v1.0` | [`ld-proof-vc-detail` attachment format](../0593-json-ld-cred-attach/README.md#ld-proof-vc-detail-attachment-format) |
Hyperledger Indy Credential Filter | `hlindy/cred-filter@v2.0` | [`cred filter` format](../0592-indy-attachments/README.md#cred-filter-format)|
Hyperledger AnonCreds Credential Filter | `anoncreds/credential-filter@v1.0` | [`Credential Filter` format](../0771-anoncreds-attachments/README.md#credential-filter-format)|

#### Offer Credential

A message sent by the Issuer to the potential Holder, describing the credential they intend to offer and possibly the price they expect to be paid. In Hyperledger Indy, this message is required, because it forces the Issuer to make a cryptographic commitment to the set of fields in the final credential and thus prevents Issuers from inserting spurious data. In credential implementations where this message is optional, an Issuer can use the message to negotiate the issuing following receipt of a `request-credential` message.

Message Format:

```json
{
    "@type": "https://didcomm.org/issue-credential/%VER/offer-credential",
    "@id": "<uuid of offer message>",
    "goal_code": "<goal-code>",
    "replacement_id": "<issuer unique id>",
    "comment": "<some comment>",
    "multiple_available": "<count>",
    "credential_preview": <json-ld object>,
    "formats" : [
        {
            "attach_id" : "<attach@id value>",
            "format" : "<format-and-version>",
        }
    ],
    "offers~attach": [
        {
            "@id": "<attach@id value>",
            "mime-type": "application/json",
            "data": {
                "base64": "<bytes for base64>"
            }
        }
    ],
    "supplements": [
        {
            "type": "hashlink-data",
            "ref": "<attachment identifier>",
            "attrs": [{
                "key": "field",
                "value": "<fieldname>"
            }]
        },
        {
            "type": "issuer-credential",
            "ref": "<attachment identifier>",
        }
    ],
    "~attach" : [] //attachments referred to in supplements
}
```

Description of fields:

* `goal_code` -- optional field that indicates the goal of the message sender. 
* `replacement_id` -- an optional field to help coordinate credential replacement. When this is present and matches the `replacement_id` of a previously issued credential, it may be used to inform the recipient that the offered credential is considered to be a replacement to the previous credential. This value is unique to the issuer. It must not be used in a credential presentation.
* `comment` -- an optional field that provides human readable information about this Credential Offer, so the offer can be evaluated by human judgment. Follows [DIDComm conventions for l10n](../0043-l10n/README.md).
* `multiple-available` -- an optional positive integer field defaulting to 1 (if absent) indicating that the Issuer has `<count>` verifiable credentials of the indicated type available for issuance to the Holder.
* `credential_preview` -- a JSON-LD object that represents the credential data that Issuer is willing to issue. It matches the schema of [Credential Preview](#preview-credential);
* `formats` -- contains an entry for each `offers~attach` array entry, providing the the value of the attachment `@id` and the verifiable credential format and version of the attachment. Accepted values for the `format` items are provided in the per format "Attachment" sections immediately below.
* `offers~attach` -- an array of attachments that further define the credential being offered. This might be used to clarify which formats or format versions will be issued.
* `supplements` -- an optional array of attachment descriptors detailing credential supplements. See the [Supplements Section](#supplements) for details.
* `~attach` -- optional attachments related to the offered credential. Each attachment should be detailed in a `supplements` entry, referenced by attachment identifier.

The Issuer may add a [`~payment-request` decorator](../0075-payment-decorators/README.md#payment_request) to this message to convey the need for payment before issuance. See the [payment section below](#payments-during-credential-exchange) for more details.

It is possible for an Issuer to add a [`~timing.expires_time` decorator](../0032-message-timing/README.md#tutorial) to this message to convey the idea that the offer will expire at a particular point in the future. Such behavior is not a special part of this protocol, and support for it is not a requirement of conforming implementations; the `~timing` decorator is simply a general possibility for any DIDComm message. We mention it here just to note that the protocol can be enriched in composable ways.

##### Offer Attachment Registry

Credential Format | Format Value | Link to Attachment Format | Comment |
--- | --- | --- | --- | 
DIF Credential Manifest | `dif/credential-manifest@v1.0` | [`offer-credential` attachment format](../0511-dif-cred-manifest-attach/README.md#offer-credential-attachment-format) | 
Hyperledger Indy Credential Abstract | `hlindy/cred-abstract@v2.0` | [`cred abstract` format](../0592-indy-attachments/README.md#cred-abstract-format)|
Linked Data Proof VC Detail  | `aries/ld-proof-vc-detail@v1.0` | [`ld-proof-vc-detail` attachment format](../0593-json-ld-cred-attach/README.md#ld-proof-vc-detail-attachment-format) |
Hyperledger AnonCreds Credential Offer | `anoncreds/credential-offer@v1.0` | [`Credential Offer` format](../0771-anoncreds-attachments/README.md#credential-offer-format)|
W3C VC - Data Integrity Proof Credential Offer | `didcomm/w3c-di-vc-offer@v0.1` | [`Credential Offer` format](../0809-w3c-data-integrity-credential-attachment/README.md#credential-offer-attachment-format)|

#### Request Credential

This is a message sent by the potential Holder to the Issuer, to request the issuance of a credential. Where circumstances do not require a preceding Offer Credential message (e.g., there is no cost to issuance that the Issuer needs to explain in advance, and there is no need for cryptographic negotiation), this message initiates the protocol. When using the Hyperledger Indy AnonCreds verifiable credential format, this message can only be sent in response to an `offer-credential` message.

This message can also be used by the Holder after a `issue-credential` message is received where the Issuer has set the `more_available` field to a positive integer, indicating that the Issuer has more credentials of the same type available to issue to the Holder.

Message Format:

```json
{
    "@type": "https://didcomm.org/issue-credential/%VER/request-credential",
    "@id": "<uuid of request message>",
    "goal_code": "<goal-code>",
    "comment": "<some comment>",
    "formats" : [
        {
            "attach_id" : "<attach@id value>",
            "format" : "<format-and-version>",
        }
    ],
    "requests~attach": [
        {
            "@id": "<attachment identifier>",
            "mime-type": "application/json",
            "data": {
                "base64": "<bytes for base64>"
            }
        },
    ],
    "supplements": [
        {
            "type": "hashlink-data",
            "ref": "<attachment identifier>",
            "attrs": [{
                "key": "field",
                "value": "<fieldname>"
            }]
        },
        {
            "type": "issuer-credential",
            "ref": "<attachment identifier>",
        }
    ],
    "~attach" : [] //attachments referred to in supplements
}
```

Description of Fields:

* `goal_code` -- optional field that indicates the goal of the message sender. 
* `comment` -- an optional field that provides human readable information about this Credential Request, so it can be evaluated by human judgment. Follows [DIDComm conventions for l10n](../0043-l10n/README.md).
* `formats` -- contains an entry for each `requests~attach` array entry, providing the the value of the attachment `@id` and the verifiable credential format and version of the attachment. Accepted values for the `format` items are provided in the per format "Attachment" sections immediately below.
* `requests~attach` -- an array of [attachments](../../concepts/0017-attachments/README.md) defining the requested formats for the credential.
* `supplements` -- an optional array of attachment descriptors detailing credential supplements. See the [Supplements Section](#supplements) for details.
* `~attach` -- optional attachments related to the requested credential. Each attachment should be detailed in a `supplements` entry, referenced by attachment identifier.

This message may have a [`~payment-receipt` decorator](../0075-payment-decorators/README.md#payment_receipt) to prove to the Issuer that the potential Holder has satisfied a payment requirement. See the [payment section below](#payments-during-credential-exchange).

If the protocol version of this message is `2.0` from the Holder, an Issuer that supports the 2.1 version of the protocol SHOULD NOT indicate that additional credentials are available (as they would by setting `more_available` to a positive integer in the `issue-credential` message) since the Holder is not capable of processing that information and requesting further credentials.

If the holder does support the `2.1` version, see the note in the section of this protocol on [`problem-report` adoption](#adopted-problem-report) for guidance on how a Holder can use a `problem-report` to end the protocol instance while the Issuer has more verifiable credentials to issue to the Holder.

##### Request Attachment Registry

Credential Format | Format Value | Link to Attachment Format | Comment |
--- | --- | --- | --- | 
DIF Credential Manifest | `dif/credential-manifest@v1.0` | [`request-credential` attachment format](../0511-dif-cred-manifest-attach/README.md#request-credential-attachment-format) | 
Hyperledger Indy Credential Request | `hlindy/cred-req@v2.0` | [`cred request` format](../0592-indy-attachments/README.md#cred-request-format)|
Linked Data Proof VC Detail  | `aries/ld-proof-vc-detail@v1.0` | [`ld-proof-vc-detail` attachment format](../0593-json-ld-cred-attach/README.md#ld-proof-vc-detail-attachment-format) |
Hyperledger AnonCreds Credential Request | `anoncreds/credential-request@v1.0` | [`Credential Request` format](../0771-anoncreds-attachments/README.md#credential-request-format)|
W3C VC - Data Integrity Proof Credential Request | `didcomm/w3c-di-vc-request@v0.1` | [`Credential Request` format](../0809-w3c-data-integrity-credential-attachment/README.md#credential-request-attachment-format)|

#### Issue Credential

This message contains verifiable credential being issued as an [attached payload](../../concepts/0017-attachments/README.md). It is sent in response to a valid Request Credential message.

Message Format:

```json
{
    "@type": "https://didcomm.org/issue-credential/%VER/issue-credential",
    "@id": "<uuid of issue message>",
    "goal_code": "<goal-code>",
    "replacement_id": "<issuer unique id>",
    "comment": "<some comment>",
    "more_available": "<count>",
    "formats" : [
        {
            "attach_id" : "<attachment identifier>",
            "format" : "<format-and-version>",
        }
    ],
    "credentials~attach": [
        {
            "@id": "<attachment identifier>",
            "mime-type": "application/json",
            "data": {
                "base64": "<bytes for base64>"
            }
        }
    ],
    "supplements": [
        {
            "type": "hashlink-data",
            "ref": "<attachment identifier>",
            "attrs": [{
                "key": "field",
                "value": "<fieldname>"
            }]
        },
        {
            "type": "issuer-credential",
            "ref": "<attachment identifier>",
        }
    ],
    "~attach" : [] //attachments referred to in supplements       
}
```

Description of fields:

* `replacement_id` -- an optional field that provides an identifier used to manage credential replacement. When this value is present and matches the `replacement_id` of a previously issued credential, this credential may be considered as a replacement for that credential. This value is unique to the issuer. It must not be used in a credential presentation.
* `comment` -- an optional field that provides human readable information about the issued credential, so it can be evaluated by human judgment. Follows [DIDComm conventions for l10n](../0043-l10n/README.md).
* `more_available` -- an optional field, defaulting to 0 if not specified, that when is a positive integer signals that the Issuer has "<count>" more instances of the verifiable credential type for the Holder that the Issuer is willing to issue. The field MUST NOT be included if the `request-credential` message indicates that the Holder is using the 2.0 version of the protocol.
  * If the `offer-credential` message was not used in the protocol instance, receipt of this field is the first indication to the Holder that this is a multiple credential issuance execution of the protocol.
  * If set to a positive integer, the Issuer will move to the `offer-sent` state while it waits on a `request-credential` message from the Holder, and the `~please-ack` decorator MUST NOT be included in the message.
  * If not present or set to 0, the Issuer will move to the `credential-issued` or `done` state, depending on whether or not the `~please-ack` decorator is included in the message (per the note below).
  * When the Holder receives this message with the field set to a positive integer, the Holder's state moves to the `offer-received` state.
* `formats` -- contains an entry for each `credentials~attach` array entry, providing the the value of the attachment `@id` and the verifiable credential format and version of the attachment. Accepted values for the `format` items are provided in the per format "Attachment" sections immediately below.
* `credentials~attach` -- an array of attachments containing the issued credential in the format(s) requested by the Holder.
* `supplements` -- an optional array of attachment descriptors detailing credential supplements. See the [Supplements Section](#supplements) for details.
* `~attach` -- optional attachments related to the issued credential. Each attachment should be detailed in a `supplements` entry, referenced by attachment identifier.

If the issuer wants an acknowledgement that the last issued credential was accepted, this message must be decorated with the `~please-ack` decorator using the `OUTCOME` acknowledgement request. Outcome in the context of this protocol means the acceptance of the credential in whole, i.e. the credential is verified and the contents of the credential are acknowledged. Note that this is different from the default behavior as described in [0317: Please ACK Decorator](../0317-please-ack/README.md). It is then best practice for the new Holder to respond with an explicit `ack` message as described in the please ack decorator RFC. 

##### Credentials Attachment Registry

Credential Format | Format Value | Link to Attachment Format | Comment |
--- | --- | --- | --- | 
Linked Data Proof VC  | `aries/ld-proof-vc@v1.0` | [`ld-proof-vc` attachment format](../0593-json-ld-cred-attach/README.md#ld-proof-vc-attachment-format) |
Hyperledger Indy Credential | `hlindy/cred@v2.0` | [credential format](../0592-indy-attachments/README.md#credential-format)|
Hyperledger AnonCreds Credential| `anoncreds/credential@v1.0` | [`Credential` format](../0771-anoncreds-attachments/README.md#credential-format)|
W3C VC - Data Integrity Proof Credential | `didcomm/w3c-di-vc@v0.1` | [`Credential` format](../0809-w3c-data-integrity-credential-attachment/README.md#credential-attachment-format)|

#### Adopted Problem Report

The [`problem-report message is adopted](../0035-report-problem/README.md) by this protocol. `problem-report` messages can be used by either party to indicate an error in the protocol.

If the Issuer has indicated in the messages (`offer-credential` and/or `issue-credential`) that multiple credentials are available, the Holder may send a `problem-report` message in place of a `request-credential` to indicate it wants to end the protocol without further issuances. This provides the Holder with the ability to end a multiple issuance sequence. The Issuer may end such a sequence by issuing a credential with the `more_available` field set to `0` (implicitly or explicitly).

#### Preview Credential

This is not a message but an inner object for other messages in this protocol. It is used construct a preview of the data for the credential that is to be issued. Its schema follows:

```jsonc
{
    "@type": "https://didcomm.org/issue-credential/%VER/credential-preview",
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
* if `mime-type` is not null, then `value` is always a base64url-encoded string that represents a binary BLOB, and `mime-type` tells how to interpret the BLOB after base64url-decoding.

#### Supplements
Supplements are used to provide information related to credentials. Each supplement must be included as a message attachment in the `~attach` array, and have a descriptor contained in the `supplements` array with the following structure:

```json
{
    "type": "<supplement_type>",
    "ref": "<attachment_id>",
    "attrs": [
        {
            "key": "<attr_key>",
            "value": "<attr_value>"
        }
    ]
}
```
- `type` SHOULD be from the following list. Compliance with this RFC indicates support of the official listed supplement types below.
- `ref` is the id of the attachment within the `~attach` list.
- `attrs` is a list of key/value pairs, used with supplement types that need additional information for processing. If no key/value pairs are needed, `attrs` may be omitted.

Official Supplement Types:
- `issuer-credential`
    - Contains a credential related to the Issuer of the credential being presented.
- `hashlink-data`
    - Contains binary data who's hashlink is contained within a presented credential.
    - This binary data MUST only be transmitted if the associated credential attribute containing the hashlink is also transmitted.
    - An attr key value pair of "field", and value of the attribute name must be sent in the attrs structure.
    - During presentation, the verifier MUST check the validity of the hashlink in the presented credential against the associated message attachment prior to use. If the verification fails, the verifier MUST consider the attachment invalid.
- `oca-bundle`
    - Contains an OCA Bundle as specified in [RFC 0755: OCA for Aries](../0755-oca-for-aries/README.md).

Holder Behavior

It is expected that a holder retain supplements provided during issuance, and present them as appropriate during presentation. Some supplements (such as `hashlink-data`) require understanding of when to include, as noted in the Supplement details. Supplements of an unknown type SHOULD NOT be automatically be presented.

> Note: Credential Supplements are a generalized form of the linked binary attachments detailed in [RFC 0641](../0641-linking-binary-objects-to-credentials/README.md). Though the methods of linking attributes differ, they may be used in combination by linking via ID _and_ the appropriate supplement metadata.

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

### Negotiation and Preview

Negotiation prior to issuing the credential can be done using the `offer-credential` and `propose-credential` messages. A common negotiation use case would be about the data to go into the credential. For that, the `credential_preview` element is used.

## Drawbacks

None documented

## Rationale and alternatives

- Attention should be paid by the Aries community to other credential issuance protocols being proposed/used in other communities to ensure this RFC could support those protocols.
- Digital Bazaar has proposed the [Credential Handler API (CHAPI)](https://w3c-ccg.github.io/credential-handler-api/) protocol that is being considered by the [W3C Credentials Community Group](https://www.w3.org/community/credentials/).

## Prior art

See [RFC 0036 Issue Credential, v1.x](../0036-issue-credential/README.md).

## Unresolved questions

- We might need to propose a new MIME type for credential (the same way as .docx is not processed as generic xml). See [this issue](https://github.com/w3c/vc-data-model/issues/421) against the W3C/vc-data-model.

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

Name / Link | Implementation Notes
--- | ---
 |  |
