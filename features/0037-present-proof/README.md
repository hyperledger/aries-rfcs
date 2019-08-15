# Aries RFC 0037: Present Proof Protocol 1.0

- Authors: Nikita Khateev
- Status: [PROPOSED](/README.md#proposed)
- Since: 2019-05-28
- Status Note:  See [RFC 0036](../0036-issue-credential/README.md) for the issue credential part of the same Indy HIPE PR.
- Supersedes: [Indy HIPE PR #89](https://github.com/hyperledger/indy-hipe/blob/2e85595e9a948a2fbfd58400191d112caff5a14b/text/credential-exchange-message-family/README.md); also [Credential Exchange 0.1 -- IIW 2019](https://hackmd.io/@QNKW9ANJRy6t81D7IfgiZQ/HkklVzww4?type=view)
- Start Date: 2019-01-30
- Tags: feature, protocol

## Summary

Formalization and generalization of existing message formats used for presenting a proof according to existing RFCs about message formats.

## Motivation

We need to define a standard protocol for presenting a proof.

## Tutorial

The present proof protocol consists of these messages:

* Propose Proof - Prover to Verifier (optional)
* Request Proof - Verifier to Prover
* Present Proof - Prover to Verifier

In addition, the [`ack`](../0015-acks/README.md) and [`problem-report`](../0035-report-problem/README.md) messages are adopted into the protocol for confirmation and error handling.

This protocol is about the messages to support the presentation of verifiable claims, not about the specifics of particular verifiable presentation mechanisms. This is challenging since at the time of writing this version of the protocol, there is only one supported verifiable presentation mechanism(Hyperledger Indy). [DIDComm attachments](../../concepts/0017-attachments/README.md) are deliberately used in messages to try to make this protocol agnostic to the specific verifiable presentation mechanism payloads. Links are provided in the message data element descriptions to details of specific verifiable presentation implementation data structures.

Diagrams in this protocol were made in draw.io. To make changes:

- upload the drawing HTML from this folder to the [draw.io](https://draw.io) site (Import From...GitHub), 
- make changes,
- export the picture and HTML to your local copy of this repo, and
- submit a pull request.

### Choreography Diagram:

![present proof](credential-presentation.png)

### Propose Presentation

An optional message sent by the Prover to the verifier to initiate a proof presentation process, or in response to a `request-presentation` message when the Prover wants to propose using a different presentation format. Schema:

```json
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/present-proof/1.0/propose-presentation",
    "@id": "<uuid-propose-presentation>",
    "comment": "some comment",
    "presentation_proposal": <json-ld object>
}
```

Description of attributes:

* `comment` -- a field that provides some human readable information about the proposed presentation.
* `presentation_proposal` -- a JSON-LD object that represents the presentation example that Prover wants to provide. It should follow the schema of [Presentation Preview](#presentation-preview);

### Request Presentation

Request presentation is a message from a verifier to a prover that describes values that need to be revealed and predicates that need to be fulfilled. Schema:

```json
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/present-proof/1.0/request-presentation",
    "@id": "<uuid-request>",
    "comment": "some comment",
    "request_presentations~attach": [
        {
            "@id": "libindy-request-presentation-0",
            "mime-type": "application/json",
            "data":  {
                "base64": "<bytes for base64>"
            }
        }
    ]
}
```

Description of fields:

* `comment` -- a field that provides some human readable information about this request for a presentation.
* `request_presentations~attach` -- an array of attachments defining the acceptable formats for the presentation.
  * For Indy, the attachment contains data from libindy about the presentation request, base64 encoded, as returned from `libindy`. For more information see the [Libindy API](https://github.com/hyperledger/indy-sdk/blob/57dcdae74164d1c7aa06f2cccecaae121cefac25/libindy/src/api/anoncreds.rs#L1214).

### Presentation

This message is a response to a Presentation Request message and contains signed presentations. Schema:

```json
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/present-proof/1.0/presentation",
    "@id": "<uuid-presentation>",
    "comment": "some comment",
    "presentations~attach": [
        {
            "@id": "libindy-presentation-0",
            "mime-type": "application/json",
            "data": {
                "base64": "<bytes for base64>"
            }
        }
    ]
}
```

Description of fields:

* `comment` -- a field that provides some human readable information about this presentation.
* `presentations~attach` -- an array of attachments containing the presentation in the requested format(s).
  * For Indy, the attachment contains data from libindy that is the presentation, base64 encoded, as returned from `libindy`. For more information see the [Libindy API](https://github.com/hyperledger/indy-sdk/blob/57dcdae74164d1c7aa06f2cccecaae121cefac25/libindy/src/api/anoncreds.rs#L1404).

### Presentation Preview

This is not a message but an inner object for other messages in this protocol. It is used to construct a preview of the data for the presentation. Its schema follows:

```json
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/present-proof/1.0/presentation-preview",
    "attributes": [
        {
            "name": "<attribute_name>",
            "cred_def_id": "<cred_def_id>",
            "mime-type": "<type>",
            "encoding": "<encoding>",
            "value": "<value>"
        }
    ],
    "predicates": [
        {
            "name": "<attribute_name>",
            "cred_def_id": "<cred_def_id>",
            "predicate": "<predicate>",
            "threshold": <threshold>
        }
    ]
}
```

The preview identifies attributes and predicates to present.

#### Attributes

The mandatory `"attributes"` key maps to a list (possibly empty to propose a presentation with no attributes) of specifications, one per attribute. Each such specification proposes its attribute's characteristics for creation within a presentation.

##### Attribute Name

The mandatory `"name"` key maps to the name of the attribute.

##### Credential Definition Identifier

The optional `"cred_def_id"` key maps to the credential definition identifier of the credential with the current attribute. If the key is absent, the preview specifies attribute's posture in the presentation as a self-attested attribute.

##### Attribute Metadata (MIME Type and Encoding)

The optional `"mime-type"` and `"encoding"` keys specify any MIME type and encoding metadata pertaining to the attribute. Their values default to `"text/plain"` and `null` respectively.

##### Value

The `"value"` key maps to the proposed value of the attribute to reveal within the presentation. An attribute specification must specify a `"value"`, a `"cred_def_id"`, or both: 

* if the `"value"` key is present and the `"cred_def_id"` key is absent, the preview proposes a self-attested attribute;
* if the `"value"` key and the `"cred_def_id"` are both present, the preview proposes verifiable claim to reveal in the presentation;
* if the `"value"` key is absent and the `"cred_def_id"` key is present, the preview proposes verifiable claim not to reveal in the presentation.

#### Predicates

The mandatory `"predicates"` key maps to a list (possibly empty to propose a presentation with no predicates) of predicate specifications, one per predicate. Each such specification proposes its predicate's characteristics for creation within a presentation.

##### Attribute Name

The mandatory `"name"` key maps to the name of the attribute germane to the predicate.

##### Credential Definition Identifier

The mandatory `"cred_def_id"` key maps to the credential definition identifier of the credential with the current attribute.

##### Predicate

The mandatory `"predicate"` key maps to the predicate operator: `"<"`, `"<="`, `">="`, `">"`. 

##### Threshold Value

The mandatory `"threshold"` key maps to the threshold value for the predicate.

##### Filter

The mandatory `"filter"` key maps to an object with one or more criteria disjunctively (via "or") applicable to the attribute as a claim.

Filter keys include:

* `"cred_def_id"` to specify a credential definition identifier
* `"schema_id"` to specify a schema identifier
* any other criteria that both the holder and verifier understand in the context of presentation creation.

## Negotiation and Preview

Negotiation prior to the presentation can be done using the `propose-presentation` and `request-presentation` messages. A common negotiation use case would be about the data to go into the presentation. For that, the `presentation-preview` element is used.

## Reference

* [VCX](https://github.com/hyperledger/indy-sdk/tree/master/vcx/libvcx/src/api) -- this implementation might not be perfect and needs to be improved, you can gather some info on parameters purpose from it
* A pre-RFC (labeled version 0.1) implementation of the protocol was implemented by a number of groups in the Hyperledger Indy community leading up to IIW28 in April 2019. The protocol can be found [here](https://hackmd.io/@QNKW9ANJRy6t81D7IfgiZQ/HkklVzww4?type=view). It was the basis of the [IIWBook demo](https://vonx.io/how_to/iiwbook) from BC Gov and collaborators.

## Drawbacks

The presentation preview as proposed above does not allow nesting of predicate logic along the lines of "A and either B or C if D, otherwise A and B", nor cross-credential-definition predicates such as proposing a legal name from either a financial institution or selected government entity.

The presentation preview may be indy-centric, as it assumes the inclusion of at most one credential per credential definition. In addition, it prescribes exactly four predicates and assumes mutual understanding of their semantics (e.g., could `">="` imply a lexicographic order for non-integer values, and if so, where to specify character collation algorithm?).

Finally, the inclusion of non-revocation timestamps may become desirable at the preview stage; the standard as proposed does not accommodate such.

## Rationale and alternatives

- Why is this design the best in the space of possible designs?
- What other designs have been considered and what is the rationale for not
choosing them?
- What is the impact of not doing this?

## Prior art

Similar (but simplified) credential exchange was already implemented in [von-anchor](https://von-anchor.readthedocs.io/en/latest/).

## Unresolved questions

- We might need some explicit documentation for nested `@type` fields.
- There might need to be a way to associate a payment with the present proof protocol.

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

Name / Link | Implementation Notes
--- | ---
 |  |
