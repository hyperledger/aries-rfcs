# Aries RFC 0586: Sign Attachment - "Please Sign This" Protocol 2.0

- Authors: Andrew Whitehead / Ian Costanzo / [Sam Curren](telegramsam@gmail.com)
- Status: [PROPOSED](/README.md#proposed)
- Since:  2021-02-09 
- Status Note: A refinement of previous work
- Start Date: 2020-08-18
- Tags: [feature](/tags.md#feature), [protocol](/tags.md#protocol)
- URI: http://didcomm.org/sign-attachment/%VER

## Summary
This protocol allows one agent to request another agent to sign an [attachment](https://github.com/hyperledger/aries-rfcs/tree/master/concepts/0017-attachments) and return the signature.

## Motivation

The attachment is likely to be an agreement or a request, the signature of which applies agreement or approval by the signing party. The contents and structure of the attachment are outside the scope of this RFC, and should be detailed elsewhere.

### Examples of application

For Indy, in order to submit transactions to the ledger, it is often necessary for agents to obtain signatures from one or more endorsers. This protocol allows Authors to request signatures from Endorsers using DIDComm, and enable the Authors to create Indy transactions that can be written to the ledger.

An agreement between two parties can be facilitated with this protocol. One party creates the agreement, and signs it. This protocol is used to get the signature from the other party, and the transaction described in the attachment is agreed to by both parties.

## Tutorial

### Name and Version

Sign Attachment 1.0

Also known as the "Please Sign This" protocol.

URI: http://didcomm.org/sign-attachment/<version>/<messageType>

## Key Concepts

Attachment to sign - may be any format recognizable to all parties.

Though this protocol can be used to gather signatures from multiple parties, each interaction is only between two parties. Multiple signatures are gathered by invoking the protocol once for each signer.

```plantuml
Coordinater --> Coordinater: Prepare Attachment
Coordinater -> Signer1: Signature Request
Signer1 -> Coordinater: Signature Response
group Additional Signers
    Coordinater -> SignerN: Signature Request
    SignerN -> Coordinater: Signature Response
end
```

## Roles

**Coordinator** - Provides the document to sign, and coordinates with the signer(s).

**Signer** - The party who's signature is requested. Evaluates the request from the coordinator, and either returns a signature as requested, or declines.

## States

**Requested** - The only state for both roles: This occurs after the signature_request has been sent/received, and before a response has been sent/received.

```plantuml
hide empty description
[*] -> Requested: Request
Requested -> [*] : Response (Signed)
Requested -> [*] : Response (Declined)
```
## Messages

### Signature Request

This message represents a request from a "coordinator" to a "signer" to provide a signature for the attachment(s) included in the request.  The request will indicate the attached message type as well as the requested signature type, and "goal codes" will be included to indicate the "goal" of the coordinator, and stated goal of the signer.

The message attachment will follow the structure defined in Aries RFC 0017 and *may* be signed (using a JWS signature, outside of the attachment itself).

```jsonc
{
  "@type": "http://didcomm.org/sign-attachment/%VER/signature-request",
  "@id": "fce30ed1-96f8-44c9-95cf-b274288009dc",
  "comment": "some comment",
  "signature_request": [{
      "attachment": "#1",
      "context": "did:sov", //why context?
      "method": "add-signature",
      "signature_type": "<requested signature type>",
      "signer_goal_code": "transaction.endorse",
      "author_goal_code": "ledger.transaction.write"
  }],
  "~attach": [{
    "@id": "1",
    "mime-type": "application/json", 
    "format": "indy/0.0", 
    "data": { 
      "base64": "..."
    }
  }]
}
```

**comment** - Human readable comment to accompany signing request.

**signature_request** - An array of structures, one per requested signature.

- **context**: context for signature use
- **method**: signature method
- **signature_type**: requested signature type
- **signer_goal_code**: The goal code that indicates the proposed goal of the signer. Signing the attachment(s) as requested will help accomplish that goal.
- **author_goal_code**: The goal code that indicates the purpose of the author of the signed attachment. This goal can be accomplished as signatures are gathered.

**~attach** - list of attachments to sign. messages requesting a signature

The attachment must be in base64 format unless using a signature method that supplies a canonicalization method for json data.

The attachment may be signed. if so, a `jws` signature will be present in the `data` attribute of the attachment. The signer may use this signature as part of their evaluation, but the signature they produce will be across the payload only.


### Signature Response

This message represents the response from the *signer* to the *coordinator* containing the response to the "please sign this" request.  The response will contain the requested signature(s), or an indicator that the signer can't or won't sign the request. The request can contain multiple attachments, so the response can contain multiple signatures (or refusals).  The response will *not* include the attachment(s) from the request, but each signature will include the `@id` of the associated attachment.

```jsonc
{
  "@type": "http://didcomm.org/sign-attachment/%VER/signature-response",
  "@id": "ece30ed1-96f8-44c9-95cf-b274288009dc",
  "~thread": {
    "thid": "fce30ed1-96f8-44c9-95cf-b274288009dc"
  },
  "signature_response": [{
      "message_id": "143c458d-1b1c-40c7-ab85-4d16808ddf0a",
      "context": "did:sov",
      "method": "add-signature",
      "signer_goal_code": "transaction.endorse" # or "transaction.refuse",
      "signature_type": "<requested signature type>",
      "signature": { ... structure determined by signature type ... }
  }]
}
```
**signature_response** - An array of signature responses. This should correlate to the number of requested signatures.
- **message_id**: Corresponds to the `@id` of the message 
- **context**: same as in request
- **method**: same as in request
- **signer_goal_code**: the same as the `signer_goal_code` of the request. If the signature is refused, a different suitable goal code should be used. 
- **signature_type"**: requested signature type
- **signature**: a structure, determined by the signature type.


In the case of an error, a problem report *should* be returned to the requesting agent instead of an endorsement response message.  (However if the endorser declines to endorse, they will return a response with that goal code.)

### Signature Present

This message presents gathered signatures to the message recipient, along with the attachment that was signed. This allows a witness to receive and verify the provided signatures.

```jsonc
{
  "@type": "http://didcomm.org/sign-attachment/%VER/signature-present",
  "@id": "ece30ed1-96f8-44c9-95cf-b274288009dc",
  "~thread": {
    "thid": "fce30ed1-96f8-44c9-95cf-b274288009dc"
  },
  "signatures": [{
      "message_id": "143c458d-1b1c-40c7-ab85-4d16808ddf0a",
      "context": "did:sov",
      "method": "add-signature",
      "signer_goal_code": "transaction.endorse" # or "transaction.refuse",
      "signature_type": "<requested signature type>",
      "signature": { ... structure determined by signature type ... }
  }],
  "messages~attach": [{
    "@id": "143c458d-1b1c-40c7-ab85-4d16808ddf0a",
    "mime-type": "application/json",
    "data": {
      "base64": {
        
      }
    }
  }]
}
```
**signatures** - An array of signature responses. This should correlate to the number of requested signatures.
- **message_id**: Corresponds to the `@id` of the message 
- **context**: same as in request
- **method**: same as in request
- **signer_goal_code**: the same as the `signer_goal_code` of the request. If the signature is refused, a different suitable goal code should be used. 
- **signature_type"**: requested signature type
- **messages~attach** - list of messages requesting a signature

In the case of an error, a problem report *should* be returned to the requesting agent instead of an endorsement response message.  (However if the endorser declines to endorse, they will return a response with that goal code.)

> Question: Is it useful for declined signatures to be presented? The sig is not there, so there is no proof of non-signature.

## Drawbacks

The downside of such a generic protocol is that the semantic meaning of the exchange is not provided by the protocol itself. Goal codes are used to add semantic meaning.

The result of this is that any application of this protocol requires another spec for the _application_ of this protocol. This presents an issue for compatibility detection and increases the complexity of handling these messages for agents.

## Rationale and alternatives

- Generalizing a protocol to ask for a signature allows for all sorts of applications.


## Prior art
This protocol was first proposed as a general way to gather signatures required for Indy transactions: https://hackmd.io/5LzMhfsMQBevB5V2tKz4hA?view



## Unresolved questions

- This protocol does not address the role of an observer, including the signers if they wish to observe the gathered signatures.
- The name 'author' in the `author_goal_code` attribute is unfortunate, as it implies the attachment author is the same as the party requesting the signature. This complicates situations where the signature is being requested from a different party than the attachment author. This also forces the role of `author` even though another name may be more accurate.
- Why is signature_request a list?

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

*Implementation Notes* [may need to include a link to test results](/README.md#accepted).

| Name / Link | Implementation Notes |
| ----------- | -------------------- |
|             |                      |