# Aries RFC 0351: Purpose Decorator
- Authors: [Filip Burlacu](filip.burlacu@securekey.com)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2019-12-16
- Status Note: implementation is being explored by SecureKey
- Supersedes:
- Start Date: 2019-12-05
- Tags: feature, decorator

## Summary

This RFC allows Aries agents to serve as mediators or relays for applications that don't use DIDComm.
It introduces:
- A new decorator, the `~purpose` decorator, which defines the intent, usage, or contents of a message
- A means for a recipient, who is not DIDComm-enabled, to register with an agent for messages with a particular purpose
- A means for a sender, who is not DIDComm-enabled, to send messages with a given purpose through its agent to a target agent
- Guidance for creating a protocol which uses the `~purpose` decorator to relay messages over DIDComm for non-DIDComm applications

## Motivation

This specification allows applications that aren't Aries agents to communicate JSON messages over DIDComm using Aries agents analogously to [mediators](/concepts/0046-mediators-and-relays/README.md). Any agent which implements this protocol can relay arbitrary new types of message for clients - without having to be updated and redeployed.

## Tutorial

> This RFC assumes familiarity with [mediators and relays](/concepts/0046-mediators-and-relays/README.md), [attachments](/concepts/0017-attachments/README.md), and [message threading](/concepts/0008-message-id-and-threading/README.md).

### The `~purpose` Decorator

The `~purpose` decorator is a JSON array which describes the *semantics* of a message - the role it plays within a protocol implemented using this RFC, for example, or the meaning of the data contained within.
The purpose is the mechanism for determining which recipient(s) should be sent a message.

Example: `"~purpose": ["team:01453", "delivery", "geotag", "cred"]`

Each element of the purpose array is a string. An agent provides some means for recipients to *register* on a purpose, or class of purposes, by indicating the particular string values they are interested in.

The particular registration semantics are TBD. Some possible formats include:
- A tagging system, where if a recipient registers on a list `"foo", "bar"`, it will be forwarded messages with purposes `["foo", "quux"]` and `["baz", "bar"]`
- A hierarchical system, where if a recipient registers on a list `"foo", "bar"`, it will receive any message with purpose `["foo", "bar", ...]` but not `["foo", "baz", ...]` or `["baz", "foo", "bar", ...]`
- A hierarchical system with wildcards: `"*", "foo"` might match any message with purpose `[..., "foo", ...]`

### Example Protocol

This is an example protocol which makes use of the `~purpose` decorator and other Aries concepts to provide a message format that can carry arbitrary payloads for non-DIDComm edge applications.

#### Key Concepts

This RFC allows messages to be sent over DIDComm by applications that are not DIDComm-enabled, by using Aries agents as intermediaries. Both the sender and the recipient can be non-DIDComm applications.

##### Non-DIDComm Sender
If the sender of the message is not a DIDComm-enabled agent, then it must rely on an agent as a trusted intermediary. This agent is assumed to have configured settings for message timing, communication endpoints, etc. 

1. The sender constructs a JSON message, and provides this to its agent, alongside specifying the *purpose*, and likely some indication of the *destination* of the message.
2. The agent determines the recipient agent - this could be by logic, for example, based on the purpose decorator, or a DID specified by the sender.
3. The agent wraps the sender's message and purpose in a DIDComm message, and sends it to the recipient agent.

##### Non-DIDComm Recipient
A non-DIDComm recipient relies on trusted agents to relay messages to it, and can register with any number of agents for any number of purposes.

1. The recipient registers with a trusted agent on certain purpose values.
2. The agent receives a DIDComm message, and sees it has a purpose decorator.
3. The agent looks through its recipient registry for all recipients which registered on a matching purpose.
3. The Agent reverses the wrapping done by the sender agent, and forwards the wrapped message to all matching registered recipients.

#### Message Format

A DIDComm message, for a protocol implemented using this RFC, requires:
 - A means to wrap the payload message
 - A `~purpose` decorator

This example protocol wraps the message within the `data` field. 

```json
{
  "@id": "123456789",
  "@type": "https://example.org/didcomm-message",
  "~purpose": [],
  "data" : {}
}
```

For example:
```json
{
  "@id": "123456789",
  "@type": "https://example.org/didcomm-message",
  "~purpose": ["metrics", "latency"],
  "data": {"mean": 346457, "median": 2344}
}
```

## Reference

This section provides guidance for implementing protocols using this decorator.

#### Threading & Timing

If a protocol implemented using this RFC requires back and forth communication, use the [`~thread`](/concepts/0008-message-id-and-threading/README.md) decorator and [transport return routing](/features/0092-transport-return-route/README.md). This allows the recipient's agent to relay replies from the recipient to the sender.

For senders and recipients that aren't aries agents, their respective agent must maintain context to correlate the DIDComm message thread, and the message thread of the communication protocol with the non-DIDComm application.

If a message is threaded, it can be useful to include a [`~timing`](/features/0032-message-timing/README.md) decorator for timing information. The sender's agent can construct this decorator from timing parameters (eg, timeout) in the communication channel with the sender, or have preconfigured settings.

#### Communication with Non-DIDComm Edge Applications

An organization using agents to relay messages for non-DIDComm edge applications is expected to secure the connections between their relay agents and their non-DIDComm edge applications. For example, running the agent as a service in the same container. If it is necessary for the organization to have a separate endpoint or mediator agent, it is recommended to have a thin relay agent as close as possible to the edge application, so internal messages sent to the mediator are also secured by DIDComm.

## Drawbacks
TODO

## Rationale and alternatives

- Alternative: defining a standard protocol for wrapping messages sent or received by non-DIDComm applications. This was the original design, but we've moved away from it because it was an unnecessary layer of specification, since custom protocols can use their own `@type` strings to specify their message formats, instead of using a two-layer system of `@type` and `data-type`.

## Prior art

- The DIF [Identity Hub](https://github.com/decentralized-identity/identity-hub/blob/master/explainer.md#actions) has a mechanism for sending objects with semantic descriptors to identities, whereas this RFC defines a method whereby agents can transact the sending and receiving of such objects on behalf of their non-aries edge apps.
- Compare against the [basic-message](/features/0095-basic-message/README.md) protocol, which uses aries agents as relays for person-person (or machine-person) communication. In contrast, this protocol uses aries agents as relays for machine-machine communication.
- The purpose decorator (as opposed to type enforcement like MIME) is similar to Intents in Android development.
- The hierarchical example for the purpose decorator is similar to Topics in MQTT.

## Unresolved questions

- We need to define the semantics of the purpose decorator - the examples provided above are potential directions the standard can go.
- Are there further semantics to define in this RFC rather than leave for specific implementations?

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

*Implementation Notes* [may need to include a link to test results](README.md).

Name / Link | Implementation Notes
--- | ---
 | 

