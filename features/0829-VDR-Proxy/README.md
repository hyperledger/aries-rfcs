# 0829: VDR Proxy

- Authors: [Stephen Curran](mailto:swcurran@cloudcompass.ca) (BC Gov)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2024-05-09
- Status Note: Proposed
- Supersedes: N/A
- Start Date: 2024-05-09
- Tags: [feature](/tags.md#feature), [protocol](/tags.md#protocol)

## Summary

A VDR ([verifiable data registry]) is a place where DIDs and objects related to
DIDs (such as [Hyperledger AnonCreds] objects) are stored such that they can be
resolved. The VDR Proxy protocol defined by this RFC is a DIDComm protocol that
can be used by a DIDComm agent to request another agent resolve VDR URIs
([Uniform Resource Identifier]s) and return the resolved objects to the
requesting agent. The protocol is a simple client/server protocol, supporting
the ability to request and receive back multiple resolutions in a single exchange.

[VDR]: https://www.w3.org/TR/did-core/#dfn-verifiable-data-registry
[verifiable data registry]: https://www.w3.org/TR/did-core/#dfn-verifiable-data-registry
[Hyperledger AnonCreds]: https://www.hyperledger.org/projects/anoncreds
[Uniform Resource Identifier]: https://en.wikipedia.org/wiki/Uniform_Resource_Identifier

## Motivation

There are several use cases that are driving the initial need for this protocol.

### Firewall Issues for Agents Accessing Indy Networks

Directly accessing an Indy network requires an Aries agent to use [ZMQ] which in
turn uses an atypical set of IP ports (in the 9700 range). Since an Aries agent
makes an outbound request to interact with the ledger, that is normally not a
problem. However, some enterprises, and even some [ISPs], prevent the use of
"non-standard" ports, blocking them with at an outbound firewall. Such
organizations only permit the outbound use of the HTTP/HTTPS ports of 80 and
443. When an Aries user, such as someone with a mobile wallet, is on a network
that limits outbound port access they cannot access the Indy networks to
retrieve ledger objects needed to process the credentials and presentations they
are receiving/generating. When direct access to the ledger is blocked, an agent
can detect the problem and fallback to use a configured VDR Proxy service using
this protocol. The initial use is for a mobile agent to use its DIDComm mediator
as a proxy, but the protocol is not restricted to that case.

[ZMQ]: https://zeromq.org/
[ISPs]: https://en.wikipedia.org/wiki/Internet_service_provider

### Fetching Revocation Data

Another use case for this protocol is when a holder needs verification data when
preparing a verifiable presentation. Some VDRs, such as the [did:web DID Method]
can be setup with the issuer hosting such data, especially the
revocation-related data. When the holder is required to collect revocation
data for preparing a verifiable presentation, as is the case with [Hyperledger
AnonCreds], we don't want the holder directly contacting the issuer to get the
necessary data. That enables either tracking or the perception of tracking by
the issuer, which is undesirable. By using the VDR Proxy protocol, the holder
can have another party, such as the verifier, the holder's mediator, or another
agent altogether, resolve the revocation data and provide it to the holder.

[did:web DID Method]: https://w3c-ccg.github.io/did-method-web/

## Tutorial

### Name and Version

This is the VDR Proxy protocol. It is uniquely identified by the URI:

    "https://didcomm.org/vdrproxy/1.0"

### Key Concepts

> This RFC assumes that the reader is familiar with [DID communication].

[DID communication]: /concepts/0005-didcomm/README.md

The protocol consists of a DIDComm `request` message from a client carrying an
array of URIs to be resolved by the proxy server, and a second message that
carries the result of resolving those URIs back to the client. The intention is
that the URIs refer to resolvable objects held in a [VDR].

The server may or may not be able to resolve the requested URI(s). For example,
the server will be configured to resolve certain DID and AnonCreds methods
(types of VDRs) and will only resolve URIs for those methods/VDRs.

On receipt of a request, the server **SHOULD** attempt to resolve each URI
passed, returning for each an array entry containing either the resolved content, encoded as a
[data URI], or an error status. A server **MAY** be configured to not to
resolve some requested URIs, either because they can't or don't want to for some
business reason. In such cases, the server **SHOULD** respond with an error
code per unprocessed URI.  If the `request` itself is incorrectly structured,
the server **SHOULD** send a [Problem Report] to the client.

[data URI]: https://datatracker.ietf.org/doc/html/rfc2397

### Role

There are two roles in the protocol `client` and `server`:

- The `client` initiates the protocol, sending a request message to the `server`.
- The `server` carries out the request however they see fit. The `server`
  **SHOULD** resolve the URIs. The `server` might be unable or unwilling to
  resolve some or all of the URIs.
- The `server` returns the resolution objects in a message to the `client`.

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

The following are the messages in the VDR Proxy protocol. The `response` message
handles all completed responses, so the `ack` ([RFC 0015 ACKs]) message is
**NOT** adopted by this protocol. The [RFC 0035 Report Problem] is adopted by
this protocol in the event that a `request` is not recognizable as a VDR Proxy
message and as such, a response message cannot be created. See the
details below in the [Problem Report Message](#problem-report-message) section.

[RFC 0015 ACKs]: ../features/0015-acks/README.md
[RFC 0035 Report Problem]: ../features/0035-report-problem/README.md

#### Request Message

The `request` message is sent by the `client` to initiate the protocol. The
message contains the array of URIs for the `server` to resolve and send the
resolved objects back to the `client`. It is assumed the `client` knows what
types of URIs the `server` is prepared to resolve. The `server` returns an error
status for any URIs it does not know how to resolve. 

The `request` message uses the following format:

```jsonc
  {
    "@type": "https://didcomm.org/vdrproxy/1.0/request",
    "@id": "2a0ec6db-471d-42ed-84ee-f9544db9da4b",
    "request" : [
      {
        "id": "<id>",
        "uri" : "<uri>"
      }
    ]
  }
```

The items in the message are as follows:

- `@type` -- required, must be as above
- `@id` -- required, must be as defined in [RFC 0005 DIDComm]
- `request` -- **required**, an item containing an array of URIs to be resolved.
  - `request` **MUST** be an array of requests.
  - Each request item **MUST** have an `id`, that is unique with the `request` item, typically the index of the array ("1", "2", "3", etc.).
  - Each request items **MUST** have a URI to be resolved.

On receipt, the server verifies the format of the request, and iterates through the `request` array,
resolving (or not) each URI and preparing the response message.

#### Response Message

A `response` message is sent by the `server` to following the
processing of the request to convey the output of the processing to the
`client`.

If the `request` content is unrecognizable, the `server` SHOULD send a [RFC 0035
Report Problem] message to the `client`.

```jsonc

  {
    "@type": "https://didcomm.org/vdrproxy/1.0/response",
    "@id": "63d6f6cf-b723-4eaf-874b-ae13f3e3e5c5",
    "response": [
      {
        "id": "<id>",
        "status" : "<status code>",
        "result" : "<data uri>"
      }
    ]
  }
```

The items in the message are as follows:

- `@type` -- required, must be as above
- `@id` -- required, must be as defined in [RFC 0005 DIDComm]
- `response` -- **required**, an item containing an array of resolution results.
  - `response` **MUST** be an array of resolution results the same length and with the same `id`s as the request.
  - `id` -- the `id` from the `request` message from the corresponding `request` item.
  - `status` -- either a `501` (meaning "Service Unavailable") if the server refuses to `resolve` the URI, or the status code resulting from attempting to resolve the URI.
  - `result` -- optional, included only if the resolution was attempted, and the resolution returned a result. If included, the value **MUST** be the result of the resolution in [data URI] format. For example, if the result of the resolution is a JSON object, the data URL would likely look like this: `data:application/json;base64,<base64 encoded JSON data>`.

As with all DIDComm messages that are not the first in a protocol instance, a
`~thread` decorator **MUST** be included in the `response` message.

Caching of resolved objects may be done by both the client and the server as they see fit to improve the
performance of using (or not needing to use) a VDR Proxy. Caching strategies depend by the proxied VDR and
are out of scope of this protocol.

#### Problem Report Message

A [RFC 0035 Report Problem] message **SHOULD** be sent by the `server` instead
of a `response` message only if the `request` is not an array of URIs.
All resolution errors **MUST** be provided to the `client` by the `server` via the
`response` message, not a `problem-report`. The `client` **MUST NOT**
respond to a `response` message, even if the `response` message is not a valid
response.  This is because once the `server` sends the `response`, the
protocol is in the `completed` state (from the `server`'s perspective) and so
is subject to deletion. As such, a follow up `problem-report` message would have
an invalid `thid` (thread ID) and (at best) be thrown away by the `server`.

### Constraints

The primary constraint with this protocol is that the two parties using the
protocol must understand what types of VDRs the server is willing to proxy.

## Reference

None.

## Drawbacks

None defined.

## Rationale and alternatives

None defined.

## Prior art

This protocol borrows much from the [RFC 0809 DIDComm Remote Producer Call], including
the request/response handling, arrays of requests, and the Problem Report handling.

[RFC 0804 DIDComm RPC]: ../0804-didcomm-rpc/README.md

## Unresolved questions

What status should be returned from the server if it refuses to resolve a URI?
The chosen status is listed. It would be helpful if the client could differentiate
between a status returned directly from the server or one proxied from the VDR.

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

*Implementation Notes* [may need to include a link to test results](README.md).

Name / Link | Implementation Notes
--- | ---
 | 
