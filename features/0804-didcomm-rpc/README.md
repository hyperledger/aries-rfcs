# 0335: DIDComm Remote Procedure Call DRPC

- Authors: [Stephen Curran](swcurran@cloudcompass.ca) (BC Gov), [Clecio Varjao](clecio.varjao@gov.bc.ca) (BC Gov)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2023-11-29
- Status Note: An evolution of the HTTP over DIDComm protocol to enable an Agent to request an arbitrary service from a connected Agent and get a response.
- Supersedes:
- Start Date: 2023-11-29
- Tags: [feature](/tags.md#feature), [protocol](/tags.md#protocol)

## Summary

The DIDComm RPC (DRPC) protocol allows a remote request-response interaction, a
Remote Procedure Call (RPC), to be carried out through a
DIDComm channel. The requesting Aries agent sends a DIDComm message to request the remote
service be invoked, and gets back the response in another DIDComm message. The
protocol enables any request to be conveyed, and the subsequent response to be
returned, with flexibility in the formats (JSON, Base64 encoded) sent and
received. Out of scope of this protocol is how the requesting agent
discovers the services available from the responding agent, and how the two
agents know about the semantics of the requests and responses. By using DIDComm
between the requesting and responding agents, the security and privacy benefits
of DIDComm are accomplished, and the generic payloads of the messages allows for
flexibility in how and where the protocol can be used.

## Motivation

There are several use cases that are driving the need for this protocol:

### App Attestation

- A mobile wallet needs to get an [app attestation] verifiable credential from
  the wallet publisher. To do that, the wallet and publisher need to exchange
  information specific to to the attestation process with the Google and Apple
  stores. The sequence is as follows:
  - The wallet decides (for some reason) it needs an App Attestation credential from its publisher.
  - If not already available, a DIDComm connection between the wallet and the attestation service is created.
  - The wallet uses the RPC protocol to request a nonce from the service to be used in the attestation. The service responds with the nonce.
  - The wallet uses a new instance of the RPC protocol to request the attestation be performed. The service responds with the status of the attestation process.
  - The service completes the business process by initiating an Issue Credential process to issue an attestation verifiable credential.

The wallet and service are using instances of three protocols (two RPC and one
Issue Credential) to carry out a full business process. Each must have knowledge
of the full business process--there is nothing inherent in the RPC protocol
about this process, or how it is being used. The RPC protocol is included to
provide a generic request-response mechanism that alleviates the need for building
many special purpose protocols.

[app attestation]: https://developer.apple.com/documentation/devicecheck

### Video Verification Service

A second example is using the RPC protocol is to implement a video verification
service that is performed prior to issuing a credential to a wallet. In this
example, the wallet communicates over DIDComm to a Credential Issuer agent that
(during verification) is a proxy to an HTTP-based video verification service.
Rather than establishing a separate, direct channel between the wallet and the
verification service, the DIDComm channel with the Issuer service is used, and
during video verification, the Issuer agent passes data between the wallet
collecting the video data and the verification service directing the process and
receiving/reviewing the data. The wallet implements the requests needed to carry
out the steps of the verification, sending to the Issuer agent the necessary
requests. The Issuer conveys the requests to the verification service and the
responses back to the mobile wallet. At the end of the process, the Issuer can
see the result of the process, and decides on next steps between it and the
mobile wallet.

## Tutorial

### Name and Version

This is the DRPC protocol. It is uniquely identified by the URI:

    "https://didcomm.org/drpc/1.0"

### Key Concepts

> This RFC assumes that you are familiar with [DID communication].

[DID communication]: /concepts/0005-didcomm/README.md

This protocol consists of a message type to carry an arbitrary request to a
responding agent, and a second message that carries the result of processing the
request back to the sender of the first message. The interpretation of the
request, how to carry out the request, the content of the response, and the
interpretation of the response, are all up to the business logic (controllers)
of the participating agents. There is no discovery of remote services offered by
agents--it is assumed that the two participants are aware of the RPC
capabilities of one another through some other means. For example, from the [App
Attestation use case](#app-attestation), functionality to carry out the app
attestation process, and the service to use is built into the mobile wallet.

It is expected (although not required) that an Aries Framework receiving a DRPC
message will simply pass to its associated "business logic" (controller) the
request from the sender, and waiting on the controller to provide the response
content to send back to the original sender. Apart from the messaging processing
applied to all inbound and outbound messages, the Aries Framework will not
perform any of the actual processing of the request.

### Roles

There are two roles in the protocol `sender` and `responder`:

- The `sender` initiates the protocol, sending a request to the `responder`.
- The `responder` carries out the request however they see fit. The `responder`
  may process the request themselves, or might invoke another service to process
  the request. The `responder` might be unable or unwilling to carry out the
  request.
- The `responder` returns the response from the request in a message to the `sender`.

### States

#### Sender

The `sender` agent goes through the following states:

- request-sent
- abandoned
- completed

The state transition table for the `sender` is:

| State / Events | Send Request                       | Receive Response               | Receive Ack                    | Receive Problem Report          |
| -------------- | ---------------------------------- | ------------------------------ | ------------------------------ | ------------------------------- |
| *Start*        | Transition to <br>**request-sent** |                                |                                |                                 |
| request-sent   |                                    | Transition to <br>**complete** | Transition to <br>**complete** | Transition to <br>**abandoned** |
| completed      |                                    |                                |                                |                                 |
| abandoned      |                                    |                                |                                |                                 |

#### Responder

The `responder` agent goes through the following states:

- request-received
- abandoned
- completed

The state transition table for the `responder` is:

| State / Events   | Receive Request                        | Send Response                  | Send Ack                       | Send Problem Report             |
| ---------------- | -------------------------------------- | ------------------------------ | ------------------------------ | ------------------------------- |
| *Start*          | Transition to <br>**request-received** |                                |                                |                                 |
| request-received |                                        | Transition to <br>**complete** | Transition to <br>**complete** | Transition to <br>**abandoned** |
| completed        |                                        |                                |                                |                                 |
| abandoned        |                                        |                                |                                |                                 |

### Messages

The following are the messages in the DRPC protocol, including the adopted messages.

#### Request Message

The `request` message is sent by the `sender` to initiate the protocol. The
message contains the information necessary for the `responder` to process the
request, prepare the response, and send the response message back. It is assumed
the `sender` knows what types of requests the `responder` is prepared to receive
and process. How the `sender` and `responder` coordinate that understanding is
out of scope of this protocol.

The `request` message items have been chosen to make putting an HTTP request
into the `request` message easy (borrowing directly from [RFC 0335 HTTP Over
DIDComm]), but an HTTP request is not required. As long as `request_type`
identifies the request being made, and the `responder` understands it, the
message can be processed.

[RFC 0335 HTTP Over DIDComm]: /features/0335-http-over-didcomm/README.md

```jsonc
{
  "@type": "https://didcomm.org/drpc/1.0/request",
  "@id": "2a0ec6db-471d-42ed-84ee-f9544db9da4b",
  "method": "<method>",
  "request": "<request>",
  "headers": [],
  "body": "<Data URL>"
}
```

The items in the message are as follows:

- `@type` -- required, must be as above
- `@id` -- required, must be as defined in [RFC 0005 DIDComm]
- `method` -- optional, can be used to indicate an HTTP operation (`GET`, `PUT`, etc.) or any other value understood by the `responder`.
- `request_type` -- **required**, an identifier indicating the type of the request. The value could be a URI, such as an HTTP URL, that the `sender` would like `responder` to resolve, or the value could be just a string understood by the `responder`.
- `headers` -- optional, a JSON array typically used for conveying HTTP headers to be used in the processing of a `request_type` that is an HTTP URL. As with all parts of this protocol, the meaning is up to the participants of an instance of the protocol.
  - When used for holding headers associated with an HTTP request, each element of the array is an object with two elements: `{"name": "<header-name>", "value": "<header-value>"}`.
- `body` -- optional, a [Data URL] containing the data to be included with the request.
  - The use of a [Data URL] provides the participants with some flexibility in sending the request data, providing a `mime-type` and giving the `sender` the option of providing [Base64 encoded] data.
  - `tl;dr` A [Data URL] allows for the inline sending of a variety of data formats. It is a string in the format:
    - `data:content/type;base64,<data>`, where `content/type` is an optional type of the data, `;base64` is optional and if present indicates the data has been [Base64 encoded], followed by the data.

[Data URL]: https://en.wikipedia.org/wiki/Data_URI_scheme
[Base64 encoded]: https://en.wikipedia.org/wiki/Base64

The `responder` processing an HTTP request may want to scan and account for the
HTTP headers defined by the `sender` For example, the `responder` might detect
and respect the timeout parameter provided in a keep-alive header if the request
header is a keep-alive connection.

#### Response Message

A `response` message is usually sent by the `responder` to following the
processing of the request to convey the output of the processing to the
`sender`. It is assumed the `sender` understands what the contents of the
`response` message means in the context of the protocol instance. How the
`sender` and `responder` coordinate that understanding is out of scope of this
protocol. In some cases the `responder` may choose to send an [Adopted
ACK](#adopted-ack) or an [Adopted Problem Report](#adopted-problem-report)
instead of the `response` message, as described below.

The message items have been chosen to make putting the response of an HTTP
request into the `response` message easy (borrowing directly from [RFC 0335 HTTP
Over DIDComm]), but an HTTP response is not required. As long as the `sender`
understands the contents of the items, the message can be processed.

```jsonc

{
  "@type": "https://didcomm.org/drpc/1.0/response",
  "@id": "63d6f6cf-b723-4eaf-874b-ae13f3e3e5c5",
  "status": {
      "code":"",
      "string":""
  },
  "headers": [],
  "body": "<Data URL>"
}
```

The items in the message are as follows:

- `@type` -- required, must be as above
- `@id` -- required, must be as defined in [RFC 0005 DIDComm]
- `status` -- optional, can be used to indicate the status of an HTTP request.
- `headers` -- optional, a JSON array typically used for conveying HTTP headers from the processing of a `request` by calling an HTTP URL. As with all parts of this protocol, the meaning is up to the participants of an instance of the protocol.
  - When used for holding headers associated with an HTTP request, each element of the array is an object with two elements:
    - `{"name": "<header-name>", "value": "<header-value>"}`.
- `body` -- optional, a [Data URL] containing the data from processing the request.
  - See the details about the `body` item in the [request](#request-message)

As with all DIDComm messages that are not the first in a protocol instance, a
`~thread` decorator **MUST** be included in the `response` message.

#### Adopted ACK

Since all of the items in the [Response Message](#response-message) are
optional, in some cases it might be easier for a `responder` to simply respond
to a `request` with an adopted [RFC 0015 ACKs] message, indicating without
further detail that the `request` was processed successfully.

[RFC 0015 ACKs]: /features/0015-acks/README.md)

```jsonc

  {
    "@type": "https://didcomm.org/notification/1.0/ack",
    "@id": "06d474e0-20d3-4cbf-bea6-6ba7e1891240",
    "status": "OK"
  }

```

#### Adopted Problem Report

In some cases, a `responder` may be unwilling or unable to complete the
`request` from the `sender`. For example, if the `responder` does not understand
the `request_type`, they obviously cannot process the request. In such cases,
the `responder` **SHOULD** send a [RFC 0035 Report Problem] problem report, with
as much detail as needed.

In other cases, the `responder` may try to process the `request` and get an
error in the processing. The `responder` has the option of sending a `response`
message with the available details of the processing error or sending a [RFC
0035 Report Problem]. For example, if the `request` was to resolve an HTTP URL,
and the HTTP `request` failed, the best response might be to send the HTTP
response that was received in a DRPC `response` messages. In other cases where
the `responder` itself processed the `request`, a problem report might be a more
useful to the `sender`.

[RFC 0035 Report Problem]: /features/0035-report-problem/README.md

### Constraints

The primary constraint with this protocol is that the two parties using the
protocol must understand one another--what `request_type` to use, what to
provide in the `headers` and `body`, how to process the `request`, what the
`response` means, and so on. It is not a protocol to be used between arbitrary
parties, but rather one where the parties have knowledge outside of DIDComm of
one another and their mutual capabilities.

On the other hand, that constrain enables great flexibility, allowing
collaborating agents to accomplish almost any request-response transaction over
DIDComm without needing to define additional DIDComm protocols. More complex
interactions can be accomplished by carrying out a sequence of DRPC protocol
instances between agents.

The flexibility DRPC protocol allows for experimenting with interactions between
agents that could later evolve into formal DIDComm protocols designed for a
specific purpose.

## Reference

### Codes Catalog

A `request_type` codes catalog *could* be developed over time and included
in this part of the RFC. This might the first step in transitioning a given
interaction implemented using DRPC into formally specified interaction.

At this time, there are no codes to be cataloged.

## Drawbacks

Anything that can be done by using the DRPC protocol can be accomplished by a
formally defined protocol specific to the task to be accomplished. The advantage
of the DRPC protocol is that pairs of agent instances that are collaborating can
use the protocol to collaborate without having to first define a task-specific
protocol.

## Rationale and alternatives

This design builds on the experience of implementations of this kind of feature
using [RFC 0095 Basic Message] and [RFC 0335 HTTP Over DIDComm]. This design
tries to build off the learnings gained from both of those implementations.

## Prior art

This protocol is very similar to the [RFC 0335 HTTP Over DIDComm] protocol,
borrowing heavily from its design and concepts. The motivations for adding this protocol versus
simply using that existing protocol are as follows.

- To enable other types of requests, beyond HTTP, to be handled using the protocol.
- To relieve the Aries Framework from any role in the execution of the protocol.
  With [RFC 0335 HTTP Over DIDComm], it is possible that the Aries Framework
  could handle the HTTP request/response, without engaging the business logic
  (controller) of the agent. This protocol strongly recommends that the
  controller handle the processing.
- Enables, when processing requests to resolve HTTP URLs, the controller to
  handle any necessary authorizations with the HTTP-based service being called.
- It is not clear what role the `~purpose` item (based on [RFC 0351 Purpose
  Decorator]) plays and how it should be used in the relatively simple use cases
  envisioned being implemented using this protocol.

[RFC 0351 Purpose Decorator]: /concepts/0351-purpose-decorator/README.md

One of the example use cases for this protocol has been implemented by "hijacking" the
[RFC 0095 Basic Message] protocol to carry out the needed request/response actions. This
approach is less than ideal in that:

- That is not the intended use of [RFC 0095 Basic Message], which is to send a
  basic, human consumable, message to the other agent.
- The `request_type` and all of the parameters for the request have to be encoded into the basic message.
- The [RFC 0095 Basic Message] protocol is a single message protocols, so each
  request-response interaction requires tow instances of the protocol, and for
  the controllers to manage connecting the interactions together.

[RFC 0095 Basic Message]: /features/0095-basic-message/README.md

Since this protocol can be used in place of [RFC 0335 HTTP Over DIDComm], its
prior art comments likewise apply to the DRPC protocol:

- VPNs and onion routing (like Tor) provide solutions for similar use cases, but none so far use DIDs, which enable more complex use cases with privacy preservation.
  - TLS/HTTPS, being HTTP over TLS, provides a similar transport-layer secure channel to HTTP over DIDComm. Note, this is why this RFC doesn't specify a means to perform HTTPS over DIDComm - DIDComm serves the same role as TLS does in HTTPS, but offers additional benefits:
    - Verifiable yet anonymous authentication of the client, for example, using delegated credentials.
    - Access to DIDComm mechanisms, such as using the introduce protocol to connect the client and server.

## Unresolved questions

- Should we include the idea of a `request` having a goal code ([RFC 0519 Goal Codes])?
- Should we simply use [RFC 0335 HTTP Over DIDComm]?

[RFC 0519 Goal Codes]: /concepts/0519-goal-codes/README.md
   
## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

*Implementation Notes* [may need to include a link to test results](README.md).

Name / Link | Implementation Notes
--- | ---
 | 
