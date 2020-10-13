# Aries RFC 0023: DID Exchange Protocol 1.0

- Authors: [Ryan West](ryan.west@sovrin.org), [Daniel Bluhm](daniel.bluhm@sovrin.org), Matthew Hailstone, Stephen Curran, [Sam Curren](sam@sovrin.org), [Stephen Curran](swcurran@cloudcompass.ca), [George Aristy](george.aristy@securekey.com)
- Status: [DEMONSTRATED](/README.md#demonstrated)
- Since: 2019-05-27
- Status Note: This RFC is a work in progress (nearing completion) designed to replace the [RFC 0160 - Connection Protocol](../../features/0160-connection-protocol/README.md) after all necessary changes have been made.
- Supersedes: [RFC 0160 - Connection Protocol](../../features/0160-connection-protocol/README.md)
- Start Date: 2018-06-29
- Tags: [feature](/tags.md#feature), [protocol](/tags.md#protocol)

## Summary

This RFC describes the protocol to exchange DIDs between agents when establishing a DID based relationship.

## Motivation

Aries agent developers want to create agents that are able to establish relationships with each other and exchange secure information using keys and endpoints in DID Documents. For this to happen there must be a clear protocol to exchange DIDs.

## Tutorial

We will explain how DIDs are exchanged, with the roles, states, and messages required.

### Roles

The DID Exchange Protocol uses two roles: _requester_ and _responder_.

The _requester_ is the party that initiates this protocol after receiving an `invitation` message
(using [RFC 0434 Out of Band](../0434-outofband/README.md)) or by using an implied invitation from a public DID. For
example, a verifier might get the DID of the issuer of a credential they are verifying, and use information in the
DIDDoc for that DID as the basis for initiating an instance of this protocol.

Since the _requester_ receiving an explicit invitation may not have an Aries agent, it is desirable, but not strictly,
required that sender of the invitation (who has the _responder_ role in this protocol)
have the ability to help the _requester_ with the process and/or costs associated with acquiring
an agent capable of participating in the ecosystem. For example, the sender of an invitation may often be sponsoring institutions.

The _responder_, who is the sender of an explicit invitation or the publisher of a DID with an implicit invitation, must have
an agent capable of interacting with other agents via DIDComm.

In cases where both parties already possess SSI capabilities, deciding who plays the role of _requester_ and _responder_  might be a casual matter of whose phone is handier.

### States

#### Requester

The _requester_ goes through the following states per the State Machine Tables below

* start
* invitation-received
* request-sent
* response-received
* abandoned
* completed

#### Responder

The _responder_ goes through the following states per the State Machine Tables below

* start
* invitation-sent
* request-received
* response-sent
* abandoned
* completed

#### State Machine Tables

The following are the _requester_ and _responder_ state machines.

The `invitation-sent` and `invitation-received` are technically outside this protocol, but are useful to show in the state machine as the invitation is the trigger to start the protocol and is referenced from the protocol as the parent thread (`pthid`).  This is discussed in more detail below.

The `abandoned` and `completed` states are terminal states and there is no expectation that the protocol can be continued (or even referenced) after reaching those states.

[![State Machine Tables](did-exchange-states.png)](https://docs.google.com/spreadsheets/d/1NKfEdyebJWQGinRIAPtpXA1BVm8jgG8_i1RyeoNzzKE/edit?usp=sharing)

### Errors

After receiving an explicit invitation, the _requester_ may send a `problem-report` to the _responder_ using the information in the invitation to either restart the invitation process (returning to the `start` state) or to abandon the protocol. The `problem-report` may be an adopted  `Out of Band` protocol message or an adopted `DID Exchange` protocol message, depending on where in the processing of the invitation the error was detected.

During the `request` / `response` part of the protocol, there are two protocol-specific error messages possible: one for an active rejection and one for an unknown error. These errors are sent using a **problem_report** message type specific to the DID Exchange Protocol. These errors do not transition the protocol to the `abandoned` state. The following list details `problem-code`s that may be sent in these cases:

**request_not_accepted** - The error indicates that the `request` message has been rejected for a reason listed in the `error_report`. Typical reasons include not accepting the method of the provided DID, unknown endpoint protocols, etc. The `request` can be resent _after_ the appropriate corrections have been made.

**request_processing_error** - This error is sent when the _responder_ was processing the request with the intent to accept the request, but some processing error occurred. This error indicates that the `request` should be resent as-is.

**response_not_accepted** - The error indicates that the `response` has been rejected for a reason listed in the `error_report`. Typical reasons include not accepting the method of the provided DID, unknown endpoint protocols, invalid signature, etc. The `response` can be resent _after_ the appropriate corrections have been made.

**response_processing_error** - This error is sent when the _requester_ was processing the `response` with the intent to accept the response, but some processing error occurred. This error indicates that the `response` should be resent as-is.

If other errors occur, the corresponding party may send a `problem-report` to inform the other party they are abandoning the protocol.

No errors are sent in timeout situations. If the _requester_ or _responder_ wishes to retract the messages they sent, they record so locally and return a `request_not_accepted` or `response_not_accepted` error when the other party sends a `request` or `response`.

#### Error Message Example

``` jsonc
{
  "@type": "https://didcomm.org/didexchange/1.0/problem_report",
  "@id": "5678876542345",
  "~thread": { "thid": "<@id of message related to problem>" },
  "~l10n": { "locale": "en"},
  "problem-code": "request_not_accepted", // matches codes listed above
  "explain": "Unsupported DID method for provided DID."
}
```

#### Error Message Attributes

- The `@type` attribute is a required string value that denotes that the received message is a problem_report within the didexchange protocol.
- The `~thread` attribute provides a context for the problem, referring to the message which contains the problem.
- Use of `~l10n` is encouraged, with at least locale defined for the message.
- The `problem-code` attribute contains one of a fixed set of codes defined in the list above.
- The `explain` attribute contains a human readable message which indicates the problem.

### Flow Overview

- The _responder_ gives provisional information to the _requester_ using an explicit `invitation` message from the [`out-of-band` protocol](../0434-outofband/README.md) or an implicit invitation in a DID the _responder_ publishes.
  - In the `out-of-band` protocol, the _responder_ is called the _sender_, and the _requester_ is called the _receiver_.
- The _requester_ uses the provisional information to send a DID and DID Doc to the _responder_ in a `request` message.
- The _responder_ uses sent DID Doc information to send a DID and DID Doc to the _requester_ in a `response` message.
- The _requester_ sends the _responder_ a `complete` message that confirms the `response` message was received.

## Implicit and Explicit Invitations

The DID Exchange Protocol is preceded by either knowledge of a resolvable DID (an implicit invitation), or by a `out-of-band/%VER/invitation` message from the [Out Of Band Protocols RFC](../0434-outofband/README.md). The information from either the resolved DID Document or the `service` element of the `handshake_protocols` attribute of the `invitation` message is used to construct the `request` message to start the protocol.

## 1. Exchange Request

The `request` message is used to communicate the DID document of the _requester_ to the _responder_ using the provisional service information present in the (implicit or explicit) invitation.

The _requester_ may provision a new DID according to the DID method spec. For a Peer DID, this involves creating a matching peer DID and key. The newly provisioned DID and DID Doc is presented in the `request` message as follows:

### Request Message Example

```jsonc
{
  "@id": "5678876542345",
  "@type": "https://didcomm.org/didexchange/1.0/request",
  "~thread": { 
      "thid": "5678876542345",
      "pthid": "<id of invitation>"
  },
  "label": "Bob",
  "did": "B.did@B:A",
  "did_doc~attach": {
      "@id": "B.did@B:A",
      "mime-type": "application/json",
      "data": {
         "base64": "eyJ0eXAiOiJKV1Qi... (bytes omitted)",
         "jws": {
            "header": {
               "kid": "did:key:z6MkmjY8GnV5i9YTDtPETC2uUAW6ejw3nk5mXF5yci5ab7th"
            },
            "protected": "eyJhbGciOiJFZERTQSIsImlhdCI6MTU4Mzg4... (bytes omitted)",
            "signature": "3dZWsuru7QAVFUCtTd0s7uc1peYEijx4eyt5... (bytes omitted)"
            }
      }
   }
}
```

#### Request Message Attributes

* The `@type` attribute is a required string value that denotes that the received message is an exchange request.
* The [`~thread`](../../concepts/0008-message-id-and-threading/README.md#thread-object) decorator MUST be included:
  * It MUST include the ID of the parent thread (`pthid`) such that the `request` can be correlated to the corresponding (implicit or explicit) `invitation`. More on correlation [below](#correlating-requests-to-invitations).
  * It SHOULD include the `thid` property. In doing so, implementations MUST set its value to that of `@id` on the same `request` message. In other words, the values of `@id` and `~thread.thid` MUST be equal.
* The `label` attribute provides a suggested label for the DID being exchanged. This allows the user to tell multiple exchange requests apart. This is not a trusted attribute.
* The `did` indicates the DID being exchanged.
* The `did_doc~attach` contains the DID Doc associated with the DID as a [signed attachment](../../concepts/0017-attachments/README.md). If the DID method for the presented DID is not a peer method and the DID Doc is resolvable on a ledger, the `did_doc~attach` attribute is optional.

#### Correlating requests to invitations

An invitation is presented in one of two forms:

* An explicit [out-of-band invitation](../../features/0434-outofband/README.md#messages) with its own `@id`.
* An implicit invitation contained in a DID document's [`service`](https://w3c-ccg.github.io/did-spec/#service-endpoints) attribute that conforms to the [DIDComm conventions](../../features/0067-didcomm-diddoc-conventions/README.md#service-conventions).

When a `request` responds to an explicit invitation, its `~thread.pthid` MUST be equal to the `@id` property of the invitation [as described in the out-of-band RFC](../../features/0434-outofband/README.md#correlating-responses-to-out-of-band-messages).

When a `request` responds to an implicit invitation, its `~thread.pthid` MUST contain a [DID URL](https://w3c-ccg.github.io/did-spec/#dfn-did-url) that resolves to the specific `service` on a DID document that contains the invitation.

##### Example Referencing an Explicit Invitation

```jsonc
{
  "@id": "a46cdd0f-a2ca-4d12-afbf-2e78a6f1f3ef",
  "@type": "https://didcomm.org/didexchange/1.0/request",
  "~thread": { 
      "thid": "a46cdd0f-a2ca-4d12-afbf-2e78a6f1f3ef",
      "pthid": "032fbd19-f6fd-48c5-9197-ba9a47040470" 
  },
  "label": "Bob",
  "did": "B.did@B:A",
  "did_doc~attach": {
      "@id": "B.did@B:A",
      "mime-type": "application/json",
      "data": {
         "base64": "eyJ0eXAiOiJKV1Qi... (bytes omitted)",
         "jws": {
            "header": {
               "kid": "did:key:z6MkmjY8GnV5i9YTDtPETC2uUAW6ejw3nk5mXF5yci5ab7th"
            },
            "protected": "eyJhbGciOiJFZERTQSIsImlhdCI6MTU4Mzg4... (bytes omitted)",
            "signature": "3dZWsuru7QAVFUCtTd0s7uc1peYEijx4eyt5... (bytes omitted)"
            }
      }
   }
}
```

##### Example Referencing an Implicit Invitation

```jsonc
{
  "@id": "a46cdd0f-a2ca-4d12-afbf-2e78a6f1f3ef",
  "@type": "https://didcomm.org/didexchange/1.0/request",
  "~thread": { 
      "thid": "a46cdd0f-a2ca-4d12-afbf-2e78a6f1f3ef",
      "pthid": "did:example:21tDAKCERh95uGgKbJNHYp#didcomm" 
  },
  "label": "Bob",
  "did": "B.did@B:A",
  "did_doc~attach": {
      "@id": "B.did@B:A",
      "mime-type": "application/json",
      "data": {
         "base64": "eyJ0eXAiOiJKV1Qi... (bytes omitted)",
         "jws": {
            "header": {
               "kid": "did:key:z6MkmjY8GnV5i9YTDtPETC2uUAW6ejw3nk5mXF5yci5ab7th"
            },
            "protected": "eyJhbGciOiJFZERTQSIsImlhdCI6MTU4Mzg4... (bytes omitted)",
            "signature": "3dZWsuru7QAVFUCtTd0s7uc1peYEijx4eyt5... (bytes omitted)"
            }
      }
   }
}
```

#### Request Transmission

The `request` message is encoded according to the standards of the Encryption Envelope, using the `recipientKeys` present in the invitation.

If the `routingKeys` attribute was present and non-empty in the invitation, each key must be used to wrap the message in a forward request, then encoded in an Encryption Envelope. This processing is in order of the keys in the list, with the last key in the list being the one for which the `serviceEndpoint` possesses the private key.

The message is then transmitted to the `serviceEndpoint`.

The _requester_ is in the `request-sent` state. When received, the _responder_ is in the `request-received` state.

#### Request processing

After receiving the exchange request, the _responder_ evaluates the provided DID and DID Doc according to the DID Method Spec.

The responder should check the information presented with the keys used in the wire-level message transmission to ensure they match.

The responder MAY look up the corresponding invitation identified in the request's `~thread.pthid` to determine whether it should accept this exchange request.

If the responder wishes to continue the exchange, they will persist the received information in their wallet. They will then either update the provisional service information to rotate the key, or provision a new DID entirely. The choice here will depend on the nature of the DID used in the invitation.

The responder will then craft an exchange response using the newly updated or provisioned information.

#### Request Errors

See [Error Section](#errors) above for message format details.

##### Request Rejected

Possible reasons:

- Unsupported DID method for provided DID
- Expired Invitation
- DID Doc Invalid
- Unsupported key type
- Unsupported endpoint protocol
- Missing reference to invitation

##### Request Processing Error

- unknown processing error

## 2. Exchange Response

The exchange response message is used to complete the exchange. This message is required in the flow, as it updates the provisional information presented in the invitation.

### Response Message Example

```json
{
  "@type": "https://didcomm.org/didexchange/1.0/response",
  "@id": "12345678900987654321",
  "~thread": {
    "thid": "<The Thread ID is the Message ID (@id) of the first message in the thread>"
  },
  "did": "B.did@B:A",
  "did_doc~attach": {
      "@id": "B.did@B:A",
      "mime-type": "application/json",
      "data": {
         "base64": "eyJ0eXAiOiJKV1Qi... (bytes omitted)",
         "jws": {
            "header": {
               "kid": "did:key:z6MkmjY8GnV5i9YTDtPETC2uUAW6ejw3nk5mXF5yci5ab7th"
            },
            "protected": "eyJhbGciOiJFZERTQSIsImlhdCI6MTU4Mzg4... (bytes omitted)",
            "signature": "3dZWsuru7QAVFUCtTd0s7uc1peYEijx4eyt5... (bytes omitted)"
            }
      }
   }
}
```

The key used in the signed attachment must be verified against the invitation's `recipientKeys` for continuity.

#### Response Message Attributes

* The `@type` attribute is a required string value that denotes that the received message is an exchange request.
* The `~thread` block contains a `thid` reference to the `@id` of the request message.
* The `did` attribute is a required string value and denotes DID in use by the responder. Note that this MAY NOT be the same DID used in the invitation.
* The `did_doc~attach` contains the DID Doc associated with the DID as a [signed attachment](../../concepts/0017-attachments/README.md). If the DID method for the presented DID is not a peer method and the DID Doc is resolvable on a ledger, the `did_doc~attach` attribute is optional.
  * If the DID and DIDDoc being conveyed is different from that conveyed in the initial contact with the requester, the DIDDoc attachment should be signed by the earlier key. For example, if the requester sent the request to a DID service endpoint from a public DID or an out-of-band invitation, the signature on the DIDDoc should use the key from that interaction.

In addition to a new DID, the associated DID Doc might contain a new endpoint. This new DID and endpoint are to be used going forward in the relationship.

#### Response Transmission

The message should be packaged in the encrypted envelope format, using the keys from the request, and the new keys presented in the internal did doc.

When the message is sent, the _responder_ are now in the `response-sent` state. On receipt, the _requester_ is in the `response-received` state.

#### Response Processing

When the requester receives the `response` message, they will verify the signature on the DID Doc attachment. After validation, they will update their wallet with the new information, and use that information in sending the `complete` message.

#### Response Errors

See [Error Section](#errors) above for message format details.

##### Response Rejected

Possible reasons:

- unsupported DID method for provided DID
- Expired Request
- DID Doc Invalid
- Unsupported key type
- Unsupported endpoint protocol
- Invalid Signature

##### Response Processing Error

- unknown processing error

## 3. Exchange Complete

The exchange `complete` message is used to confirm the exchange to the _responder_. This message is **required** in the flow, as it marks the exchange complete. The _responder_ may then invoke any protocols desired based on the context expressed via the `pthid` in the DID Exchange protocol.

### Complete Message Example

```jsonc
{
  "@type": "https://didcomm.org/didexchange/1.0/complete",
  "@id": "12345678900987654321",
  "~thread": {
    "thid": "<The Thread ID is the Message ID (@id) of the first message in the thread>",
    "pthid": "<pthid used in request message>"
  }
}
```

The `pthid` is required in this message, and must be identical to the `pthid` used in the `request` message.

After a `complete` message is sent, the *requester* is in the `completed` terminal state. Receipt of the message puts the *responder* into the `completed` state.

#### Complete Errors

See [Error Section](#errors) above for message format details.

##### Complete Rejected

This is unlikely to occur with other than an unknown processing error (covered below), so no possible reasons are listed. As experience is gained with the protocol, possible reasons may be added.

##### Complete Processing Error

- unknown processing error

## Next Steps

The exchange between the _requester_ and the _responder_ has been completed. This relationship has no trust associated with it. The next step should be to increase the trust to a sufficient level for the purpose of the relationship, such as through an exchange of proofs.

## Peer DID Maintenance

When Peer DIDs are used in an exchange, it is likely that both the _requester_ and _responder_ will want to perform some relationship maintenance such as key rotations. Future RFC updates will add these maintenance features.

## Reference

* https://docs.google.com/document/d/1mRLPOK4VmU9YYdxHJSxgqBp19gNh3fT7Qk4Q069VPY8/edit#heading=h.7sxkr7hbou5i
* [Agent to Agent Communication Video](https://drive.google.com/file/d/1PHAy8dMefZG9JNg87Zi33SfKkZvUvXvx/view)
* [Agent to Agent Communication Presentation](https://docs.google.com/presentation/d/1H7KKccqYB-2l8iknnSlGt7T_sBPLb9rfTkL-waSCux0/edit#slide=id.p)
* Problem_report message adopted into message family, following form defined by the [Problem Report HIPE](https://github.com/hyperledger/indy-hipe/blob/6a5e4fe2d7e14953cd8e3aed07d886176332e696/text/error-handling/README.md)

## Drawbacks

 N/A at this time

## Prior art

- This process is similar to other key exchange protocols.

## Unresolved questions

- N/A at this time

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

Name / Link | Implementation Notes
--- | ---
trinsic.id | Commercial mobile and web app built using Aries Framework - .NET [MISSING test results](/tags.md#test-anomaly)
