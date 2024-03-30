# 0804: DIDComm Remote Procedure Call (DRPC)

- Authors: [Clecio Varjao](mailto:clecio.varjao@gov.bc.ca) (BC Gov), [Stephen Curran](mailto:swcurran@cloudcompass.ca) (BC Gov), [Akiff Manji](mailto:amanji@petridish.dev) (BC Gov)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2023-11-29
- Status Note: An evolution of the HTTP over DIDComm protocol to enable an Agent to request an arbitrary service from a connected Agent and get a response.
- Supersedes:
- Start Date: 2023-11-29
- Tags: [feature](/tags.md#feature), [protocol](/tags.md#protocol)

## Summary

The DIDComm Remote Procedure Call (DRPC) protocol enables a [JSON-RPC]-based
request-response interaction to be carried out across a DIDComm channel. The
protocol is designed to enable custom interactions between connected agents, and
to allow for the rapid prototyping of experimental DIDComm protocols. An agent
sends a DIDComm message to request a [JSON-RPC] service be invoked by another
agent, and gets back the [JSON-RPC]-format response in subsequent DIDComm
message. The protocol enables any request to be conveyed that the other agent
understands. Out of scope of this protocol is how the requesting agent discovers
the services available from the responding agent, and how the two agents know
the semantics of the specified [JSON-RPC] requests and responses. By using
DIDComm between the requesting and responding agents, the security and privacy
benefits of DIDComm are accomplished, and the generic parameters of the requests
allow for flexibility in how and where the protocol can be used.

[JSON-RPC]: https://www.jsonrpc.org/specification

## Motivation

There are several use cases that are driving the initial need for this protocol.

### App Attestation

A mobile wallet needs to get an [app attestation] verifiable credential from
the wallet publisher. To do that, the wallet and publisher need to exchange
information specific to to the attestation process with the Google and Apple
stores. The sequence is as follows:

- The wallet decides (for some reason) it needs an App Attestation credential
  from its publisher.
- If not already available, a DIDComm connection between the wallet and the
  attestation service is created.
- The wallet uses the DRPC protocol to request a nonce from the service to be
  used in the attestation. The service responds with the nonce.
- The wallet uses a new instance of the DRPC protocol to request the attestation
  be performed. The service responds with the status of the attestation process.
- The service completes the business process by initiating an Issue Credential
  process to issue an attestation verifiable credential.

The wallet and service are using instances of three protocols (two DRPC and one
Issue Credential) to carry out a full business process. Each participant must
have knowledge of the full business process--there is nothing inherent in the
DRPC protocol about this process, or how it is being used. The DRPC protocol is
included to provide a generic request-response mechanism that alleviates the
need for formalizing special purpose protocols.

> App attestation is a likely candidate for a having its own DIDComm protocol.
> This use of DRPC is ideal for developing and experimenting with the necessary
> agent interactions before deciding on if a use-specific protocol is needed and
> its semantics.

[app attestation]: https://developer.apple.com/documentation/devicecheck

### Video Verification Service

A second example is using the DRPC protocol is to implement a custom video
verification service that is used by a specific mobile wallet implementation and
a proprietary backend service prior to issuing a credential to the wallet. Since
the interactions are to a proprietary service, so an open specification does not
make sense, but the use of DIDComm is valuable. In this example, the wallet
communicates over DIDComm to a Credential Issuer agent that (during
verification) proxies the requests/responses to a backend ("behind the
firewall") service. The wallet is implemented to use DRPC protocol instances to
initiate the verification and receive the actions needed to carry out the steps
of the verification (take picture, take video, instruct movements, etc.),
sending to the Issuer agent the necessary data. The Issuer conveys the requests
to the verification service and the responses back to the mobile wallet. At the
end of the process, the Issuer can see the result of the process, and decide on
the next actions between it and the mobile wallet, such as issuing a credential.

Again, after using the DRPC protocol for developing and experimenting with the
implementation, the creators of the protocol can decide to formalize their own
custom, end-to-end protocol, or continue to use the DRPC protocol instances.
Important is that they can begin development without doing any Aries frameworks
customizations or plugins by using DRPC.

## Tutorial

### Name and Version

This is the DRPC protocol. It is uniquely identified by the URI:

    "https://didcomm.org/drpc/1.0"

### Key Concepts

> This RFC assumes that you are familiar with [DID communication].

[DID communication]: /concepts/0005-didcomm/README.md

The protocol consists of a DIDComm `request` message carrying an arbitrary
[JSON-RPC] request to a responding agent, and a second message that carries the
result of processing the request back to the client of the first message. The
interpretation of the request, how to carry out the request, the content of the
response, and the interpretation of the response, are all up to the business
logic (controllers) of the participating agents. There is no discovery of remote
services offered by agents--it is assumed that the two participants are aware of
the DRPC capabilities of one another through some other means. For example, from
the [App Attestation use case](#app-attestation), functionality to carry out the
app attestation process, and the service to use it is built into the mobile wallet.

Those unfamiliar with [JSON-RPC], the `<tl;dr>` is that it is a very simple
request response protocol using JSON where the only data shared is:

- a `method` that defines what needs to be done,
- some `params` in JSON that are up to the requester/server to agree on, and
- an (optional) `id` to connect the response to the request.

The response is likewise simple:

- a `result` item if the invocation completed successful containing the return results,
- an `error` item if the invocation failed, containing details about the failure, and
- the `id` from the request.

An example of a simple [JSON-RPC] request/response pair from the specification is:

```json
--> {"jsonrpc": "2.0", "method": "subtract", "params": [42, 23], "id": 1}
<-- {"jsonrpc": "2.0", "result": 19, "id": 1}
```

A [JSON-RPC] request may be a batch of requests, each with a different `id` value,
and the response a similar array, with an entry for each of the requests.

[JSON-RPC] follows a similar "parameters defined by the message type" pattern as
DIDComm. As a result, in this protocol we do not need to add any special
handling around the `params` such as Base64 encoding, signing, headers and so
on, as the parties interacting with the protocol by definition must have a
shared understanding of the content of the `params` and can define any special
handling needed amongst themselves.

It is expected (although not required) that an Aries Framework receiving a DRPC
message will simply pass to its associated "business logic" (controller) the
request from the client, and wait on the controller to provide the response
content to be sent back to the original client. Apart from the messaging processing
applied to all inbound and outbound messages, the Aries Framework will not
perform any of the actual processing of the request.

### Roles

There are two roles, adopted from the [JSON-RPC] specification, in the protocol
`client` and `server`:

- The `client` initiates the protocol, sending a request to the `server`.
- The `server` carries out the request however they see fit. The `server`
  may process the request themselves, or might invoke another service to process
  the request. The `server` might be unable or unwilling to carry out the
  request.
- The `server` returns the response from the request in a message to the `client`.

### States

#### Client States

The `client` agent goes through the following states:

- request-sent
- completed

The state transition table for the `client` is:

| State / Events          | Send Request                       | Receive Response                |
| ----------------------- | ---------------------------------- | ------------------------------- |
| *Start*                 | Transition to <br>**request-sent** |                                 |
| request-sent            |                                    | Transition to <br>**complete**  |
| completed               |                                    |                                 |
| problem-report received |                                    | Transition to <br>**abandoned** |
| abandoned               |                                    |                                 |

#### Server States

The `server` agent goes through the following states:

- request-received
- completed

The state transition table for the `server` is:

| State / Events   | Receive Request                        | Send Response or Problem Report |
| ---------------- | -------------------------------------- | ------------------------------- |
| *Start*          | Transition to <br>**request-received** |                                 |
| request-received |                                        | Transition to <br>**complete**  |
| completed        |                                        |                                 |

### Messages

The following are the messages in the DRPC protocol. The `response` message
handles all positive responses, so the `ack` ([RFC 0015 ACKs]) message is
**NOT** adopted by this protocol. The [RFC 0035 Report Problem] is adopted by
this protocol in the event that a `request` is not recognizable as a [JSON-RPC]
message and as such, a [JSON-RPC] response message cannot be created. See the
details below in the [Problem Report Message](#problem-report-message) section.

[RFC 0015 ACKs]: ../features/0015-acks/README.md
[RFC 0035 Report Problem]: ../features/0035-report-problem/README.md

#### Request Message

The `request` message is sent by the `client` to initiate the protocol. The
message contains the [JSON-RPC] information necessary for the `server` to
process the request, prepare the response, and send the response message back to
the `client`. It is assumed the `client` knows what types of requests the
`server` is prepared to receive and process. If the `server` does not know how
to process the error, [JSON-RPC] has a standard response, outlined in the
[response message](#response-message) section below. How the `client` and
`server` coordinate that understanding is out of scope of this protocol.

The `request` message uses the same JSON items as [JSON-RPC], skipping the
`id` in favor of the existing DIDComm `@id` and thread handling.

```jsonc
  {
    "@type": "https://didcomm.org/drpc/1.0/request",
    "@id": "2a0ec6db-471d-42ed-84ee-f9544db9da4b",
    "request" : {"jsonrpc": "2.0", "method": "subtract", "params": [42, 23], "id": 1}
  }
```

The items in the message are as follows:

- `@type` -- required, must be as above
- `@id` -- required, must be as defined in [RFC 0005 DIDComm]
- `request` -- **required**, an item containing a [JSON-RPC] request JSON structure.
  - `request` **MUST** be either a single [JSON-RPC] request, or an array of [JSON-RPC] requests.
  - Each [JSON-RPC] request **MUST** have the `jsonrpc` and `method` items.
  - Each [JSON-RPC] request **MAY** have the `params` and `id` items.
    - See the details below about the handling of `notification` [JSON-RPC] requests, requests where the `id` field is omitted.
  - See the [JSON-RPC] specification for details about the `jsonrpc`, `method`, `params` and `id` JSON items.

Per the [JSON-RPC] specification, if the `id` field of a [JSON-RPC] request is omitted, the `server` should not respond. In this DRPC DIDComm protocol, the `server` is always expected to send a `response`, but **MUST NOT** include
a [JSON-RPC] response for any [JSON-RPC] request for which the `id` is omitted. This is covered further
in the [response message](#response-message) section (below).

#### Response Message

A `response` message is sent by the `server` to following the
processing of the request to convey the output of the processing to the
`client`. As with the `request` the format mostly exactly that of a
[JSON-RPC] response.

If the `request` is unrecognizable as a [JSON-RPC] message such that a
[JSON-RPC] message cannot be generated, the `server` SHOULD send a [RFC 0035
Report Problem] message to the `client`.

It is assumed the `client` understands what the contents of the
`response` message means in the context of the protocol instance. How the
`client` and `server` coordinate that understanding is out of scope of this
protocol.

```jsonc

  {
    "@type": "https://didcomm.org/drpc/1.0/response",
    "@id": "63d6f6cf-b723-4eaf-874b-ae13f3e3e5c5",
    "response": {"jsonrpc": "2.0", "result": 19, "id": 1}
  }
```

The items in the message are as follows:

- `@type` -- required, must be as above
- `@id` -- required, must be as defined in [RFC 0005 DIDComm]
- `response` -- **required**, an item containing a [JSON-RPC] response JSON structure.
  - `response` **MUST** be either single (possibly empty) [JSON-RPC] response,
    or an array of [JSON-RPC] responses.
    - If all of the [JSON-RPC] requests in the `request` message are
      *notifications* (e.g., the `id` item is omitted), the DIDComm `response`
      message **MUST** be sent back with the value: `"response" : {}`.
  - Each [JSON-RPC] response **MUST** have the `jsonrpc` and `id` items, and either a `result` or `error` item.
    - See the [JSON-RPC] specification for details about the `jsonrpc`, `id`, `result` and `error` JSON items.

As with all DIDComm messages that are not the first in a protocol instance, a
`~thread` decorator **MUST** be included in the `response` message.

The special handling of the "all [JSON-RPC] requests are notifications"
described above is to simplify the DRPC handling to know when a DRPC protocol
instance is complete. If a `response` message is not always required, the DRPC
handler would have to inspect the `request` message to look for `id`s to
determine when the protocol completes.

If the `server` does not understand how to process a given [JSON-RPC] request, a
`response` error **SHOULD** be returned (as per the [JSON-RPC] specification) with:

- `error.code` value `-32601`,
- `error.message` set to `Method not found`, and
- no `error.data` item.

#### Problem Report Message

A [RFC 0035 Report Problem] message **SHOULD** be sent by the `server` instead
of a `response` message only if the `request` is unrecognizable as a [JSON-RPC] message.
An [JSON-RPC] errors **MUST** be provided to the `client` by the `server` via the
`response` message, not a `problem-report`. The `client` **MUST NOT**
respond to a `response` message, even if the `response` message is not a valid
[JSON-RPC] response.  This is because once the `server` sends the `response`, the
protocol is in the `completed` state (from the `server`'s perspective) and so
is subject to deletion. As such, a follow up `problem-report` message would have
an invalid `thid` (thread ID) and (at best) be thrown away by the `server`.

### Constraints

The primary constraint with this protocol is that the two parties using the
protocol must understand one another--what [JSON-RPC] request(s) to use, what
parameters to provide, how to process the those requests, what the `response`
means, and so on. It is not a protocol to be used between arbitrary parties, but
rather one where the parties have knowledge outside of DIDComm of one another
and their mutual capabilities.

On the other hand, that constraint enables great flexibility for explicitly
collaborating agents (such as a mobile wallet and the agent of its manufacturer)
to accomplish request-response transactions over DIDComm without
needing to define additional DIDComm protocols. More complex interactions can be
accomplished by carrying out a sequence of DRPC protocol instances between
agents.

The flexibility the DRPC protocol allows for experimenting with specific
interactions between agents that could later evolve into formal DIDComm "fit for
purpose" protocols.

## Reference

### Codes Catalog

A [JSON-RPC] request codes catalog *could* be developed over time and be
included in this part of the RFC. This might an intermediate step in transitioning
a given interaction implemented using DRPC into formally specified interaction.
On the other hand, simply defining a full DIDComm protocol will often be a far
better approach.

At this time, there are no codes to be cataloged.

## Drawbacks

Anything that can be done by using the DRPC protocol can be accomplished by a
formally defined protocol specific to the task to be accomplished. The advantage
of the DRPC protocol is that pairs of agent instances that are explicitly
collaborating can use this protocol without having to first define a
task-specific protocol.

## Rationale and alternatives

We considered not supporting the *notification* and *batch* forms of the
[JSON-RPC] specification, and decided it made sense to allow for the full
support of the [JSON-RPC] specification, including requests of those forms. That
said, we also found that the concept of **not** having a DRPC `response` message
in some (likely, rare) cases based on the contents of the `request` JSON item
(e.g., when all of the `id`s are omitted from the [JSON-RPC] requests) would
unnecessarily complicate the DIDComm protocol instance handling about when it is
complete. As a result, a DRPC `response` message is always required.

This design builds on the experience of implementations of this kind of feature
using [RFC 0095 Basic Message] and [RFC 0335 HTTP Over DIDComm]. This design
tries to build off the learnings gained from both of those implementations.

Based on feedback to an original version of the RFC, we looked as well at
using [gRPC] as the core of this protocol, versus [JSON-RPC]. Our assessment
was that [gRPC] was a much heavier weight mechanism that required more effort
between parties to define and implement what will often be a very simple
request-response transaction -- at the level of defining a DIDComm protocol.

[gRPC]: https://grpc.io/

The use of `params` and leaving the content and semantics of the params up to
the `client` and `server` means that they can define the appropriate handling of
the parameters. This eliminates the need for the protocol to define, for
example, that some data needs to be Base64 encoding for transmission, or if some
values need to be cryptographically signed. Such details are left to the
participants and how they are using the protocol.

## Prior art

This protocol has similar goals to the [RFC 0335 HTTP Over DIDComm] protocol,
but takes a lighter weight, more flexible approach. We expect that implementing
HTTP over DIDComm using this protocol will be as easy as using [RFC 0335 HTTP
Over DIDComm], where the [JSON-RPC] request's `params` data structure holds the
`headers` and `body` elements for the HTTP request. On the other hand, using the
explicit [RFC 0335 HTTP Over DIDComm] is might be a better choice if it is
available and exactly what is needed.

[RFC 0335 HTTP Over DIDComm]: /features/0335-http-over-didcomm/README.md

One of the example use cases for this protocol has been implemented by "hijacking" the
[RFC 0095 Basic Message] protocol to carry out the needed request/response actions. This
approach is less than ideal in that:

- That is not the intended use of [RFC 0095 Basic Message], which is to send a
  basic, human consumable message to the other agent.
- The request method and parameters have to be encoded into the basic message.
- The [RFC 0095 Basic Message] protocol is a single message protocols, so each
  request-response interaction requires two instances of the protocol, and for
  the controllers to manage connecting the interactions together.

[RFC 0095 Basic Message]: /features/0095-basic-message/README.md

## Unresolved questions

- Should we include the idea of a `request` having a goal code ([RFC 0519 Goal Codes])?

[RFC 0519 Goal Codes]: /concepts/0519-goal-codes/README.md

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

*Implementation Notes* [may need to include a link to test results](README.md).

Name / Link | Implementation Notes
--- | ---
 | 
