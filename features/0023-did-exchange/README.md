# Aries RFC 0023: DID Exchange Protocol 1.0

- Authors: [Ryan West](ryan.west@sovrin.org), [Daniel Bluhm](daniel.bluhm@sovrin.org), Matthew Hailstone, Stephen Curran, [Sam Curren](sam@sovrin.org)
- Status: [DEMONSTRATED](/README.md#demonstrated)
- Since: 2019-05-27
- Status Note: This RFC is a work in progress designed to replace the [RFC 0160 - Connection Protocol](../../features/0160-connection-protocol/README.md) after all necessary changes have been made. This RFC is likely to change as discussions continue, and should not yet be built into production code.
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

The DID Exchange Protocol uses two roles: __inviter__ and __invitee__.

The _inviter_ is the party that initiates the protocol with an `invitation` message. This party
must already have an agent and be capable of creating DIDs and endpoints
at which they are prepared to interact. It is desirable but not strictly required that inviters
have the ability to help the invitee with the process and/or costs associated with acquiring
an agent capable of participating in the ecosystem. For example, inviters may often be sponsoring institutions. The inviter sends a `response` message at the end of the _share_ phase.

The _invitee_ has less preconditions; the only requirement is that this party be capable of
receiving invitations over traditional communication channels of some type, and acting on
it in a way that leads to successful interaction. The invitee sends a `request` message at the beginning of the _share_ phase.

In cases where both parties already possess SSI capabilities, deciding who plays the role of inviter and invitee might be a casual matter of whose phone is handier.

### States

#### null

No exchange exists or is in progress

#### invited

The invitation has been shared with the intended _invitee_(s), and they have not yet sent a _exchange_request_.

#### requested

A _exchange_request_ has been sent by the _invitee_ to the _inviter_ based on the information in the _invitation_.

#### responded

A _exchange_response_ has been sent by the _inviter_ to the _invitee_ based on the information in the _exchange_request_.

#### complete

The exchange has been completed.

![State Machine Tables](chrome_2019-01-29_07-59-38.png)

### Errors

There are no errors in this protocol during the invitation phase. For the request and response, there are two error messages possible for each phase: one for an active rejection and one for an unknown error. These errors are sent using a **problem_report** message type specific to the DID Exchange Protocol. The following list details `problem-code`s that may be sent:

**request_not_accepted** - The error indicates that the request has been rejected for a reason listed in the error_report. Typical reasons include not accepting the method of the provided DID, unknown endpoint protocols, etc. The request can be resent _after_ the appropriate corrections have been made.

**request_processing_error** - This error is sent when the inviter was processing the request with the intent to accept the request, but some processing error occurred. This error indicates that the request should be resent as-is.

**response_not_accepted** - The error indicates that the response has been rejected for a reason listed in the error_report. Typical reasons include not accepting the method of the provided DID, unknown endpoint protocols, invalid signature, etc. The response can be resent _after_ the appropriate corrections have been made.

**response_processing_error** - This error is sent when the invitee was processing the response with the intent to accept the response, but some processing error occurred. This error indicates that the response should be resent as-is.

No errors are sent in timeout situations. If the inviter or invitee wishes to retract the messages they sent, they record so locally and return a `request_not_accepted` or `response_not_accepted` error when the other party sends a request or response .

#### Error Message Example

```
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

The _inviter_ gives provisional information to the _invitee_ using an `invitation` message from the `out-of-band` protocol.
The _invitee_ uses provisional information to send a DID and DID Doc to the _inviter_ in a `request` message.
The _inviter_ uses sent DID Doc information to send a DID and DID Doc to the _invitee_ in a `response` message.
The *invitee* sends the *inviter* a `complete` message that confirms the response was received.

## Out-of-Band Invitation

The DID Exchange Protocol is proceeded by either knowledge of a resolvable DID, or by a `out-of-band/%VER/invitation` message from the [Out Of Band Protocols RFC](../0434-outofband/README.md). The information from either the resolved DID Document or the `service` attribute of the `invitation` message is used to construct the `request` message to start the protocol.

## 1. Exchange Request

The exchange request message is used to communicate the DID document of the _invitee_ to the _inviter_ using the provisional service information present in the _invitation_ message.

The _invitee_ will provision a new DID according to the DID method spec. For a Peer DID, this involves creating a matching peer DID and key. The newly provisioned DID and DID Doc is presented in the exchange_request message as follows:

#### Example

```json
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
```

#### Attributes

* The `@type` attribute is a required string value that denotes that the received message is an exchange request.
* The [`~thread`](../../concepts/0008-message-id-and-threading/README.md#thread-object) decorator MUST be included:
  * It MUST include the ID of the parent thread (`pthid`) such that the `request` can be correlated to the corresponding `invitation`. More on correlation [below](#correlating-requests-to-invitations).
  * It MAY include the `thid` property. In doing so, implementations MUST set its value to that of `@id` on the same request message. In other words, the values of `@id` and `~thread.thid` MUST be equal.
* The `label` attribute provides a suggested label for the DID being exchanged. This allows the user to tell multiple exchange requests apart. This is not a trusted attribute.
* The `did` indicates the DID being exchanged.
* The `did_doc~attach` contains the DID Doc associated with the DID as a [signed attachment](../../concepts/0017-attachments/README.md). If the DID method for the presented DID is not a peer method and the DID Doc is resolvable on a ledger, the `did_doc~attach` attribute is optional.

#### Correlating requests to invitations

An invitation is presented in one of two forms:

* An explicit [out-of-band invitation](../../features/0434-outofband/README.md#messages) with its own `@id`.
* An implicit invitation contained in a DID document's [`service`](https://w3c-ccg.github.io/did-spec/#service-endpoints) attribute that conforms to the [DIDComm conventions](../../features/0067-didcomm-diddoc-conventions/README.md#service-conventions).

When a `request` responds to an explicit invitation, its `~thread.pthid` MUST be equal to the `@id` property of the invitation [as described in the out-of-band RFC](../../features/0434-outofband/README.md#correlating-responses-to-out-of-band-messages).

When a `request` responds to an implicit invitation, its `~thread.pthid` MUST contain a [DID URL](https://w3c-ccg.github.io/did-spec/#dfn-did-url) that resolves to the specific `service` on a DID document that contains the invitation.

**Example referencing an explicit invitation**

```json
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
```

**Example referencing an implicit invitation**

```json
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
```


#### Request Transmission

The Request message is encoded according to the standards of the Encryption Envelope, using the `recipientKeys` present in the invitation.

If the `routingKeys` attribute was present and non-empty in the invitation, each key must be used to wrap the message in a forward request, then encoded in an Encryption Envelope. This processing is in order of the keys in the list, with the last key in the list being the one for which the `serviceEndpoint` possesses the private key.

The message is then transmitted to the `serviceEndpoint`.

We are now in the `requested` state.

#### Request processing

After receiving the exchange request, the _inviter_ evaluates the provided DID and DID Doc according to the DID Method Spec.

The _inviter_ should check the information presented with the keys used in the wire-level message transmission to ensure they match.

The _inviter_ MAY look up the corresponding invitation identified in the request's `~thread.pthid` to determine whether it should accept this exchange request.

If the _inviter_ wishes to continue the exchange, they will persist the received information in their wallet. They will then either update the provisional service information to rotate the key, or provision a new DID entirely. The choice here will depend on the nature of the DID used in the invitation.

The _inviter_ will then craft an exchange response using the newly updated or provisioned information.

#### Request Errors

See [Error Section](#errors) above for message format details.

**request_rejected**

Possible reasons:

- Unsupported DID method for provided DID
- Expired Invitation
- DID Doc Invalid
- Unsupported key type
- Unsupported endpoint protocol
- Missing reference to invitation

**request_processing_error**

- unknown processing error

## 2. Exchange Response

The exchange response message is used to complete the exchange. This message is required in the flow, as it updates the provisional information presented in the invitation.

#### Example

```json
{
  "@type": "https://didcomm.org/didexchange/1.0/response",
  "@id": "12345678900987654321",
  "~thread": {
    "thid": "<The Thread ID is the Message ID (@id) of the first message in the thread>"
  },
  "did": "B.did@B:A",
  "did_doc~attach": {
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
```

The key used in the signed attachment must be verified against the invitation's `recipientKeys` for continuity.

#### Attributes

* The `@type` attribute is a required string value that denotes that the received message is an exchange request.
* The `~thread` block contains a `thid` reference to the `@id` of the request message.
* The `did` attribute is a required string value and denotes DID in use by the _inviter_. Note that this may not be the same DID used in the invitation.
* The `did_doc~attach` contains the DID Doc associated with the DID as a [signed attachment](../../concepts/0017-attachments/README.md). If the DID method for the presented DID is not a peer method and the DID Doc is resolvable on a ledger, the `did_doc~attach` attribute is optional.

In addition to a new DID, the associated DID Doc might contain a new endpoint. This new DID and endpoint are to be used going forward in the relationship.

#### Response Transmission

The message should be packaged in the encrypted envelope format, using the keys from the request, and the new keys presented in the internal did doc.

When the message is transmitted, we are now in the `responded` state.

#### Response Processing

When the _invitee_ receives the `response` message, they will verify the `change_sig` provided. After validation, they will update their wallet with the new information. If the endpoint was changed, they may wish to execute a Trust Ping to verify that new endpoint.

#### Response Errors

See [Error Section](#errors) above for message format details.

**response_rejected**

Possible reasons:

- unsupported DID method for provided DID
- Expired Request
- DID Doc Invalid
- Unsupported key type
- Unsupported endpoint protocol
- Invalid Signature

**response_processing_error**

- unknown processing error

## 3. Exchange Complete

The exchange complete message is used to confirm the exchange to the _inviter_.  This message is required in the flow, as it marks the exchange complete. The _inviter_ may then invoke any protocols desired based on the context expressed via the `pthid` in the DID Exchange protocol.

#### Example

```json
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

After a message is sent, the *invitee* in the `complete` state. Receipt of a message puts the *inviter* into the `complete` state.

#### Next Steps

The exchange between the _inviter_ and the _invitee_ is now established. This relationship has no trust associated with it. The next step should be the exchange of proofs to build trust sufficient for the purpose of the relationship.

## Exchange Reuse

When an Out-of-Band Invitation (`invitation`)  is received containing a public DID for which the _invitee_ already has a connection, the _invitee_ may use the `reuse` message in the protocol sent over the existing connection. The `pthid` passed in the `reuse` message allows the _inviter_ to correlate the invitation with the identified existing connection and then invoke any protocols desired based on that context.

#### Reuse Example

```json
{
  "@type": "https://didcomm.org/didexchange/1.0/reuse",
  "@id": "12345678900987654321",
  "~thread": {
      "thid": "12345678900987654321",
      "pthid": "<The @id of the Out-of-Band invitation>"
  }
}
```

The `pthid` is required in this message. It provides the context link for the _inviter_ to prompt additional protocol interactions.

Sending or receiving this message does not change the state of the existing connection.

When the _inviter_ receives the `reuse` message, they must respond with a `reuse-accepted` message to notify that _invitee_ that the request to reuse the existing connection is successful.

#### Reuse Accepted Example

```json
{
  "@type": "https://didcomm.org/didexchange/1.0/reuse-accepted",
  "@id": "12345678900987654321",
  "~thread": {
    "thid": "<The Message @id of the reuse message>"
  }
}
```

If this message is not received by the _invitee_, they should use the regular exchange flow described above. This message is a mechanism by which the _invitee_ can detect a situation where the _inviter_ no longer has a record of the connection and is unable to decrypt and process the `reuse` message.

After sending this message, the _inviter_ may continue any desired protocol interactions based on the context matched by the `pthid` present in the `reuse` message.

#### Peer DID Maintenance

When Peer DIDs are used in an exchange, it is likely that both Alice and Bob will want to perform some relationship maintenance such as key rotations. Future RFC updates will add these maintenance features.

## Reference

* https://docs.google.com/document/d/1mRLPOK4VmU9YYdxHJSxgqBp19gNh3fT7Qk4Q069VPY8/edit#heading=h.7sxkr7hbou5i
* [Agent to Agent Communication Video](https://drive.google.com/file/d/1PHAy8dMefZG9JNg87Zi33SfKkZvUvXvx/view)
* [Agent to Agent Communication Presentation](https://docs.google.com/presentation/d/1H7KKccqYB-2l8iknnSlGt7T_sBPLb9rfTkL-waSCux0/edit#slide=id.p)
* Problem_report message adopted into message family, following form defined by the [Problem Report HIPE](https://github.com/hyperledger/indy-hipe/blob/6a5e4fe2d7e14953cd8e3aed07d886176332e696/text/error-handling/README.md)

## Drawbacks

* 

## Prior art

- This process is similar to other key exchange protocols.

## Unresolved questions

- 

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

Name / Link | Implementation Notes
--- | ---
[Streetcred.id](https://streetcred.id/) | Commercial mobile and web app built using Aries Framework - .NET [MISSING test results](/tags.md#test-anomaly)
