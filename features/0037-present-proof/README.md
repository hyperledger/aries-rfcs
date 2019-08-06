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

#### Choreography Diagram:

![present proof](credential-presentation.png)

#### Propose Presentation

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

#### Request Presentation

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
  * For Indy, the attachment contains data from libindy about the presentation request, base64 encoded. The following JSON is an example of the `libindy-request-presentation-0` attachment content. For more information see the [Libindy API](https://github.com/hyperledger/indy-sdk/blob/57dcdae74164d1c7aa06f2cccecaae121cefac25/libindy/src/api/anoncreds.rs#L1214).

```json
{
     "name": string,
     "version": string,
     "nonce": string,
     "requested_attributes": {
          "<attr_referent>": <attr_info>
     },
     "requested_predicates": {
          "<predicate_referent>": <predicate_info>
     },
     "non_revoked": Optional<<non_revoc_interval>>
}
```

#### Presentation

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
  * For Indy, the attachment contains data from libindy that is the presentation, base64 encoded. The following JSON is an example of the `libindy-presentation-0` attachment content. For more information see the [Libindy API](https://github.com/hyperledger/indy-sdk/blob/57dcdae74164d1c7aa06f2cccecaae121cefac25/libindy/src/api/anoncreds.rs#L1404).

```json
{
     "requested_proof": {
         "revealed_attrs": {
             "requested_attr1_id": {sub_proof_index: number, raw: string, encoded: string},
             "requested_attr4_id": {sub_proof_index: number: string, encoded: string},
         },
         "unrevealed_attrs": {
             "requested_attr3_id": {sub_proof_index: number}
         },
         "self_attested_attrs": {
             "requested_attr2_id": self_attested_value,
         },
         "requested_predicates": {
             "requested_predicate_1_referent": {sub_proof_index: int},
             "requested_predicate_2_referent": {sub_proof_index: int},
         }
     },
     "proof": {
         "proofs": [ <credential_proof>, <credential_proof>, <credential_proof> ],
         "aggregated_proof": <aggregated_proof>
     },
     "identifiers": [{schema_id, cred_def_id, Optional<rev_reg_id>, Optional<timestamp>}]
}
```

#### Presentation Preview

This is not a message but an inner object for other messages in this protocol. It is used to construct a preview of the data for the presentation. Its schema follows:

```json
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/present-proof/1.0/presentation-preview",
    "attributes": {
        "<cred_def_id>": {
            "<attribute>": {
                "mime-type": "<type>",
                "encoding": "<encoding>",
                "value": "<value>"
            }
        },
        ...
    },
    "predicates": {
        "<cred_def_id>": {
            "<predicate>": {
                "<attribute>": "<threshold>",
                ...
            },
            ...
        },
        ...
    },
    "non_revocation_times": {
        "<cred_def_id>": "<iso_8601_datetime>",
        ...
    }
}
```

The preview identifies attributes, predicates, and non-revocation timestamps by credential definition identifier. Note that this composition assumes that any presentation can include information from at most one credential per credential definition; such an approach mitigates corroboration risk.

##### Attributes

The `"attributes"` key maps zero or more credential definition identifiers to one or more inner objects; each such inner object maps an attribute name to its respective MIME types, encodings, and values (all optional) for the presentation:

* the prover may include a MIME type and/or encoding per attribute in the preview for verifier information on how to interpret its value
* the value itself may be absent at this stage; its omission in the preview indicates its ultimate inclusion in the presentation itself.

Any attribute specified per credential definition identifier must belong to its corresponding credential definition. In this way the structure excludes a bait-and-switch where the prover has credentials on multiple credential definitions with common attribute names (e.g., `name`, `score`).

For consistency and completeness, an empty production `"{}"` as the value for the `"attributes"` key denotes that the preview specifies zero attributes.

##### Predicates

The `"predicates"` key maps zero or more credential definition identifiers to one or more inner objects; each such inner object maps predicate names to their respective attributes and thresholds for the presentation. Each predicate name identifies its comparison operator: `"<"`, `"<="`, `">"`, `">="`. Each attribute so specified per credential definition identifier must belong to its corresponding credential definition.

For consistency and completeness, an empty production `"{}"` as the value for the `"predicates"` key denotes that the preview specifies zero predicates.

##### Non-Revocation Timestamps

The `"non_revocation_times"` key maps zero or more credential definition identifiers to ISO 8601 datetimes, each of which offers an instant where the prover or verifier proposes inclusion of proof of the non-revocation of its corresponding credential in the presentation.

Non-revocation timestamps apply only to credentials on credential definitions that support revocation.

For consistency and completeness, an empty production `"{}"` as the value for the `"non_revocation_times"` key denotes that the preview specifies zero non-revocation timestamps.

## Negotiation and Preview

Negotiation prior to the presentation can be done using the `propose-presentation` and `request-presentation` messages. A common negotiation use case would be about the data to go into the presentation. For that, the `presentation-preview` element is used.

## Reference

* [VCX](https://github.com/hyperledger/indy-sdk/tree/master/vcx/libvcx/src/api) -- this implementation might not be perfect and needs to be improved, you can gather some info on parameters purpose from it
* A pre-RFC (labeled version 0.1) implementation of the protocol was implemented by a number of groups in the Hyperledger Indy community leading up to IIW28 in April 2019. The protocol can be found [here](https://hackmd.io/@QNKW9ANJRy6t81D7IfgiZQ/HkklVzww4?type=view). It was the basis of the [IIWBook demo](https://vonx.io/how_to/iiwbook) from BC Gov and collaborators.

## Drawbacks

The presentation preview as proposed above does not allow nesting of predicate logic along the lines of "A and either B or C if D, otherwise A and B", nor cross-credential-definition predicates such as proposing a legal name from either a financial institution or selected government entity.

The presentation preview may be indy-centric, as it assumes the inclusion of at most one credential per credential definition. In addition, it prescribes exactly four predicates and assumes mutual understanding of their semantics (e.g., could `">="` imply a lexicographic order for non-integer values, and if so, where to specify character collation algorithm?).

Finally, the inclusion of a non-revocation timestamp may be premature at the preview stage.

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

Diagrams were made in draw.io. To make some changes you can just upload the HTML from this repo to this site.

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

Name | Link | Implementation Notes
--- | --- | ---
 |  |
