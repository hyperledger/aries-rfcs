# 0037: Present Proof

- Author: Nikita Khateev
- Start Date: 2019-01-30

## Status

- Status: [PROPOSED](/README.md#rfc-lifecycle)
- Status Date: 2019-05-28
- Status Note: This supersedes the Present Proof part of [Indy HIPE PR #89](https://github.com/hyperledger/indy-hipe/blob/2e85595e9a948a2fbfd58400191d112caff5a14b/text/credential-exchange-message-family/README.md). See [Aries RFC 0036](../0036-issue-credential) for the issue credential part of the same Indy HIPE PR.

## Summary

Formalization and generalization of existing message formats used for presenting a proof according to existing RFCs about message formats.

## Motivation

We need to define a standard protocol for presenting a proof.

## Tutorial

The present proof protocol consists of these messages:

* Propose Proof - Prover to Verifier (optional)
* Request Proof - Verifier to Prover
* Present Proof - Prover to Verifier

In addition, the [ack](../../features/0015-acks) and [report problem](../0035-report-problem) messages are adopted into the protocol for confirmation and error handling.

#### Choreography Diagram:

![present proof](present-proof.png)

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
          "<attr_referent>": <attr_info>,
     },
     "requested_predicates": {
          "<predicate_referent>": <predicate_info>,
     },
     "non_revoked": Optional<<non_revoc_interval>>,
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
        },
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
     }
     "proof": {
         "proofs": [ <credential_proof>, <credential_proof>, <credential_proof> ],
         "aggregated_proof": <aggregated_proof>
     }
     "identifiers": [{schema_id, cred_def_id, Optional<rev_reg_id>, Optional<timestamp>}]
}
```

#### Presentation Preview

This is not a message but an inner object for other messages in this protocol. It is used to construct a preview of the data for the presentation. Its schema follows:

```json
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/present-proof/1.0/presentation-preview",
    "<cred-def-id>": {
        "attributes": {
            "<attribute>": {
                "mime-type": "<type>",
                "encoding": "<encoding>",
                "value": "<value>"
            },
            ...
        },
        "predicates": {
            "<predicate>": {
                "<attribute>": "<threshold>"
            },
            ...
        },
        "non-revocation-time": "<ISO-8601 datetime>"
    },
    ...
```

Topmost keys (except `@type`) in the presentation preview identify credential definitions pertinent to the presentation under negotiation. Note that this composition assumes that any presentation can include information from at most one credential per credential definition; such an approach mitigates corroboration risk.

For each credential definition identifier, the structure includes either `"attributes"`, `"predicates"`, or both. To propose inclusion of non-revocation status, the structure includes a `"non-revocation-time"` timestamp.

##### Attributes

For each credential definition identifier, the `"attributes"` key maps zero or more attribute names to their respective MIME types, encodings, and values; all of which are optional:

* an empty object as the `"attributes"` value proposes no attribute inclusion from its
  credential definition, as does the omission of the `"attributes"` key itself
* the prover may include a MIME type and/or encoding per attribute in the preview for
  verifier information on how to interpret its value
* the value itself may be absent at this stage; its omission connotes the willingness
  of the prover to include its value in proof.

Any attribute specified per credential definition identifier must belong to its credential definition. In this way the structure excludes a bait-and-switch where the prover has credentials on multiple credential definitions with common attribute names (e.g., `name`, `score`).

##### Predicates

For each credential definition identifier, the `"predicates"` key maps zero or more predicates to their respective attributes and threshold values. Each predicate name identifies its comparison operator: `"<"`, `"<="`, `">"`, `">="`.

An empty production as the value for a credential definition's `"predicates"` connotes an absence of predicates on attributes of the credential definition, as does the omission of the `"predicates"` value itself.

##### Non-Revocation Timestamp

For each credential definition identifier, the `"non-revocation-time"` timestamp offers an instant where the prover proposes inclusion of proof of the non-revocation of its corresponding credential.

The non-revocation timestamp applies only to credentials on credential definitions that support revocation.

## Negotiation and Preview

Negotiation prior to the presentation can be done using the `propose-presentation` and `request-presentation` messages. A common negotiation use case would be about the data to go into the presentation. For that, the `presentation-preview` element is used.

## Reference

* [VCX](https://github.com/hyperledger/indy-sdk/tree/master/vcx/libvcx/src/api) -- this implementation might not be perfect and needs to be improved, you can gather some info on parameters purpose from it
* A pre-RFC (labeled version 0.1) implementation of the protocol was implemented by a number of groups in the Hyperledger Indy community leading up to IIW28 in April 2019. The protocol can be found [here](https://hackmd.io/s/HkklVzww4). It was the basis of the [IIWBook demo](https://vonx.io/how_to/iiwbook) from BC Gov and collaborators.

## Drawbacks

The presentation preview as proposed above does not allow nesting of predicate logic along the lines of "A and either B or C if D, otherwise A and B", nor cross-credential-definition predicates such as proposing a legal name from either a financial institution or selected government entity.

The presentation preview may be indy-centric, as it assumes the inclusion of at most one credential per credential definition. In addition, it prescribes exactly four predicates and assumes mutual understanding of their semantics (e.g., could '>=' imply a lexicographic order for non-integer values, and if so, where to specify character collation algorithm?).

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
