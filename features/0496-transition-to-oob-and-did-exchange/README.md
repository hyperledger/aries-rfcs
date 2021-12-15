# Aries RFC 0496: Transition to the Out of Band and DID Exchange Protocols

- Authors: [Stephen Curran](mailto:swcurran@cloudcompass.ca)
- Status: [ACCEPTED](/README.md#accepted)
- Since: 2021-11-24
- Status Note: In step 1 - update all implementations to accept Connection and OOB Invitations. **Target Completion Date: 2021.12.31**
- Supersedes:
- Start Date: 2020-06-07
- Tags: [feature](/tags.md#feature), [community-update](/tags.md#community-update), [test-anomaly](/tags.md#test-anomaly)

## Summary

The Aries community has agreed to transition from using the `invitation` messages in [RFC 0160 Connections](../0160-connection-protocol/README.md)
and [RFC 0023 DID Exchange](../0023-did-exchange/README.md) to using the plaintext `invitation` message in [RFC 0434 Out of Band](../0434-outofband/README.md) and from using RFC 0160 to RFC 0023 for establishing agent-to-agent connections.
As well, the community has agreed to transition from using [RFC 0056 Service Decorator](../0056-service-decorator/README.md) to execute connection-less instances of the [RFC 0037 Present Proof](../0037-present-proof/README.md) protocol to using the out-of-band invitation message.

This RFC follows the guidance in [RFC 0345](../../concepts/0345-community-coordinated-update/README.md) about
community-coordinated updates to (try to) ensure that independently deployed, interoperable agents remain interoperable throughout this transition.

The transition from the old to new messages will occur in four steps:

- **Pre-work**: Agent builders agree on the transition plan outlined in this RFC and the target date for completing Step 1.
  - Any RFC updates related to this transition needed before starting the transition are completed.
- **Step 1**: Agent builders update all agent code bases and deployments to accept incoming out-of-band messages requesting equivalent-to-current functionality.
  - Equivalent-to-current functionality includes:
    - RFC 160 Connections invitations
    - Connection-less Present Proof protocol instances using the service decorator
  - See the section below on [Step 1 out-of-band messages](#step-1-out-of-band-messages)
  - During Step 1, all agents should continue to send the current invitation and connection-less protocol messages.
  - Each agent builder SHOULD notify the community they have completed Step 1 by submitting a PR to update their entry in the [implementations](#implementations) section of this RFC.
- **Step 2**: Agent builders update all agent code bases and deployments to send out out-of-band invitations equivalent to the current invitation and connection-less protocol messages, and Agent builders add full out-of-band and did-exchange ([RFC 0023](../0023-did-exchange/README.md)) protocol support to all agent code bases and deployments.
  - Messages from existing RFCs being replaced by the out-of-band protocol are marked as `deprecated`.
  - Full out-of-band support is **NOT** required&mdash;just support for the out-of-band equivalents of the old `invitation` messages.
  - When sending or receiving `did:peer` DIDs, the DIDs MUST conform to [RFC 627 Static Peer DIDs](../0627-static-peer-dids/README.md).
  - Each agent builder SHOULD notify the community they have completed Step 2 by submitting a PR to update their entry in the [implementations](#implementations) section.
- **Step 3**: Support for the current invitation and connection-less protocol messages can be removed from all implementations and deployments, and all out-of-band `invitation` capabilities that align with the then current Aries Interop Profile (AIP) may be offered.

### Step 1 Out-of-Band Messages

The definition of Step 1 has been deliberately defined to limit the impact of the changes on existing code bases. An implementation may be able to do as little as convert an incoming out-of-band protocol message into its "current format" equivalent and process the message, thus deferring larger changes to the message handling code. The following examples show the equivalence between out-of-band and current messages and the constraints on the out-of-band invitations used in Step 2.

#### Connection Invitation&mdash;Inline DIDDoc Service Entry

The following is the out-of-band `invitation` message equivalent to an RFC 0160 Connections `invitation` message that may be used in Step 2.

```jsonc
{
  "@type": "https://didcomm.org/out-of-band/1.0/invitation",
  "@id": "1234-1234-1234-1234",
  "label": "Faber College",
  "goal_code": "establish-connection",
  "goal": "To establish a connection",
  "handshake_protocols": ["did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/connections/1.0/invitation"],
  "service": [
      {
        "id": "#inline"
        "type": "did-communication",
        "recipientKeys": ["did:key:z6MkpTHR8VNsBxYAAWHut2Geadd9jSwuBV8xRoAnwWsdvktH"],
        "routingKeys": [],
        "serviceEndpoint": "https://example.com:5000"
      }
  ]
}
```

The constraints on this form of the out-of-band `invitation` sent during Step 2 are:

- `goal_code` and `goal` are ignored.
- `handshake_protocols` MUST have exactly one entry and that entry must be `did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/connections/1.0/invitation`.
- `request~attach` MUST NOT be present.
- `service` MUST have exactly one entry and be in the form above or be a single DID (but not both).

This out-of-band message can be transformed to the following RFC 0160 Connection `invitation` message.

```jsonc
{
  "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/connections/1.0/invitation",
  "@id": "1234-1234-1234-1234",
  "label": "Faber College",
  "recipientKeys": ["6MkpTHR8VNsBxYAAWHut2Geadd9jSwuBV8xRoAnwWsdvktH"],
  "serviceEndpoint": "https://example.com:5000",
  "routingKeys": []
}
```

Note the use of `did:key` in the out-of-band message and the "naked" public key in the connection message. Ideally, full support for `did:key` will be added during Step 1. However, if there is not time for an agent builder to add full support, the transformation can be accomplished using simple text transformations between the `did:key` format and the (only) public key format used in current Aries agents.

#### Connection Invitation&mdash;DID Service Entry

If the out-of-band message `service` item is a single DID, the resulting transformed message is comparably different. For example, this out-of-band `invitation` message:

```jsonc
{
  "@type": "https://didcomm.org/out-of-band/%VER/invitation",
  "@id": "<id used for context as pthid>",
  "label": "Faber College",
  "goal_code": "issue-vc",
  "goal": "To issue a Faber College Graduate credential",
  "handshake_protocols": ["https://didcomm.org/connections/1.0"],
  "service": ["did:sov:LjgpST2rjsoxYegQDRm7EL"]
}
```

The `did` form of the connection invitation is implied, as shown here:

```jsonc
{
  "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/connections/1.0/invitation",
  "@id": "1234-1234-1234-1234",
  "label": "Faber College",
  "did": ["did:sov:LjgpST2rjsoxYegQDRm7EL"]
}
```

#### Connection-less Present Proof Request

The most common connection-less form being used in production is the `request-presentation` message from the [RFC 0037 Present Proof](../0037-present-proof/README.md) protocol. The out-of-band invitation for that request looks like this, using the inline form of the service entry.

```jsonc
{
  "@type": "https://didcomm.org/out-of-band/%VER/invitation",
  "@id": "1234-1234-1234-1234",
  "label": "Faber College",
  "goal_code": "present-proof",
  "goal": "Request proof of some claims from verified credentials",
  "request~attach": [
    {
        "@id": "request-0",
        "mime-type": "application/json",
        "data": {
            "json": {
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
        }
    }
  ],
  "service": [
      {
        "id": "#inline",
        "type": "did-communication",
        "recipientKeys": ["did:key:z6MkpTHR8VNsBxYAAWHut2Geadd9jSwuBV8xRoAnwWsdvktH"],
        "routingKeys": [],
        "serviceEndpoint": "https://example.com:5000"
      }
  ]
}
```

The constraints on this form of the out-of-band `invitation` sent during Step 2 are:

- `goal_code` is ignored and `goal` is used as the `comment`.
- `handshake_protocols` MUST NOT be present.
- `request~attach` MUST have exactly one entry and that entry must be a `request-presentation` message.
- `service` MUST have exactly one entry and be in the form above or be a single DID (but not both).

This out-of-band message can be transformed to the following RFC 0037 Present Proof `request-presentation` message with an [RFC 0056 Service Decorator](../0056-service-decorator/README.md) item.

```jsonc
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/present-proof/1.0/request-presentation",
    "@id": "1234-1234-1234-1234",
    "comment": "Request proof of some claims from verified credentials",
    "~service": {
        "recipientKeys": ["6MkpTHR8VNsBxYAAWHut2Geadd9jSwuBV8xRoAnwWsdvktH"],
        "routingKeys": [],
        "serviceEndpoint": "https://example.com:5000"
    },
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

If the DID form of the out-of-band `invitation` message `service` entry was used, the `~service` item would be comparably altered.

#### URL Shortener Handling

During Step 2 [URL Shortening](../0434-outofband/README.md#url-shortening) as defined in RFC 0434 Out of Band must be supported.

### Between Step Triggers

The community coordination triggers between the steps above will be as follows:

- **Pre-work to Step 1** - a PR to this RFC is merged that sets the RFC status to [ACCEPTED](/README.md#accepted).
- **Step 1 to Step 2** - the community agrees that the majority of the deployed agents have completed Step 1. A PR to this RFC is merged that sets the RFC status to [ADOPTED](/README.md#adopted).
  - Agent builders indicate completion of Step 1 by updating the [Implementations](#implementations) section of this RFC.
  - A PR to RFC 0160 Connections and RFC 0023 DID Exchange marks the `invitation` messages as deprecated.
  - The [ADOPTED](/README.md#adopted) version of this RFC is included in the then-current [Aries Interop Profile](/concepts/0302-aries-interop-profile/README.md) version.
- **Step 2 to Step 3** - the community agrees that the majority of the deployed agents have completed Step 2. A PR to this RFC is merged that sets the RFC status to [RETIRED](/README.md#retired).
  - Agent builders indicate completion of Step 2 by updating the [Implementations](#implementations) section of this RFC.

## Motivation

To enable agent builders to independently update their code bases and deployed agents to support the out-of-band protocol while maintaining interoperability.

## Tutorial

The general mechanism for this type of transition is documented in [RFC 0345](../../concepts/0345-community-coordinated-update/README.md) about
community-coordinated updates.

The specific sequence of events to make this particular transition is outlined in the [summary](#summary) section of this RFC.

## Reference

See the [summary](#summary) section of this RFC for the details of this transition.

## Drawbacks

None identified.

## Rationale and alternatives

This approach balances the speed of adoption with the need for independent deployment and ongoing interoperability.

## Prior art

The approach outlined in [RFC
0345](../../concepts/0345-community-coordinated-update/README.md) about
community-coordinated updates is a well-known pattern for using deprecation to
make breaking changes in an ecosystem. That said, this is the first attempt to
use this approach in Aries. Adjustments to the transition plan will be made as needed, and RFC 0345 will be updated based on lessons learned in executing this plan.

## Unresolved questions

- Are the constraints on the proposed "equivalent to existing" messages sufficiently clear?
- Does the community want to support the connection-less `Issue Credential` process to be supported in Step 2?

## Implementations

The following table lists the status of various agent code bases and deployments with respect to **Step 1** of this transition. Agent builders MUST update this table as they complete steps of the transition.

Name / Link | Implementation Notes
--- | ---
 |