# Aries RFC 0351: Generic JSON Message
- Authors: [Filip Burlacu](filip.burlacu@securekey.com)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2019-12-16
- Status Note: implementation is being explored by SecureKey
- Supersedes:
- Start Date: 2018-12-05
- Tags: feature, protocol

## Summary

This RFC allows Aries agents to serve as mediators or relays for applications that don't use DIDComm.
It introduces:
- A new decorator, the `~purpose` decorator, which defines the intent, usage, or contents of a message
- A protocol message format which uses the `~purpose` decorator to relay messages over DIDComm for non-DIDComm applications
- A means for a recipient, who is not DIDComm-enabled, to register with an agent for messages with a particular purpose
- A means for a sender, who is not DIDComm-enabled, to send messages with a given purpose through its agent to a target agent

## Motivation

This protocol allows clients that aren't Aries agents to communicate JSON messages over DIDComm using Aries agents as [mediators or relays](/concepts/0046-mediators-and-relays/README.md). Any agent which implements this protocol can relay arbitrary new types of message for clients - without having to be updated and redeployed.

## Tutorial

### The `~purpose` Decorator

The `~purpose` decorator is a JSON array which describes the *semantics* of a message - the role it plays within a protocol implemented using this RFC, for example, or the type or meaning of the data contained within.
The purpose is the mechanism for determining which recipient(s) should be sent a message.

Example: `"~purpose": ["team:01453", "delivery", "geotag", "cred"]`

Each element of the purpose array is a string. An agent provides some means for recipients to *register* on a purpose, or class of purposes, by indicating the particular string values they are interested in.

The particular registration semantics left to the implementation. Some possible examples include:
- A tagging system, where if a recipient registers on a list `"foo", "bar"`, it will be forwarded messages with purposes `["foo", "quux"]` and `["baz", "bar"]`
- A hierarchical system, where if a recipient registers on a list `"foo", "bar"`, it will receive any message with purpose `["foo", "bar", ...]` but not `["foo", "baz", ...]` or `["baz", "foo", "bar", ...]`
- A hierarchical system with wildcards: `"*", "foo"` might match any message with purpose `[..., "foo", ...]`

### The Generic JSON Message Protocol

This RFC provides a protocol which makes use of the `~purpose` decorator and other Aries concepts to provide a message format that can carry arbitrary payloads for non-DIDComm edge applications.

#### Name and Version

This is the generic JSON message protocol, defined uniquely by the URI:

    "https://didcomm.org/json/1.0"

#### Key Concepts

> This RFC assumes familiarity with [mediators and relays](/concepts/0046-mediators-and-relays/README.md), [attachments](/concepts/0017-attachments/README.md), and [message threading](/concepts/0008-message-id-and-threading/README.md)

This protocol has two primary roles, the **sender** and the **recipient**. The sender constructs a message with a JSON payload, which the recipient parses. This protocol supports optional threading, so the recipient can send a response to the sender, and optional timing decorators, so the sender can specify its response timeout. 

Secondary roles/sub-roles: In a use-case where the *sender* is not a DIDComm-enabled agent, we introduce the role of **sender-agent**, which is the agent that relays messages to/from the sender, translating from DIDComm to non-DIDComm messaging. Similarly, for a *recipient* that is not a DIDComm-enabled agent, we introduce the role of **recipient-agent**, which serves the same purpose for the recipient. 

Note: if we refer to a sender-agent or recipient-agent, and an implementation doesn't have one, the relevant behaviour would instead be in the sender/recipient.

With JSON messaging, custom agents can communicate domain-specific information or implement domain-specific protocols without breaking compatibility with the wider DIDComm standards. Agents can also [relay](/concepts/0046-mediators-and-relays/README.md) messages between entities that are not DIDComm-enabled, allowing a wide range of communication protocols to use DIDComm to transport their messages, without requiring the agents themselves to be modified.

This protocol does not define the format of the content of a message, except that it be an [attachment](/concepts/0017-attachments/README.md). Specific implementations may specify the exact format they expect. To support this flexibility, this protocol defines that every message must contain a `data-type` field, so a sender can indicate the correct format which the recipient should use to parse a message.

#### Threading & Timing

This protocol supports but does not require the use of the `~thread` decorator to provide message threading. If a message is threaded, it can be useful to include a [`~timing`](/features/0032-message-timing/README.md) decorator for timing information.

## Reference

#### DIDComm Message Format

This protocol defines one DIDComm message format, of type `https://didcomm.org/json/1.0/message`. A `message` only requires (in addition to the standard contents of DIDComm messages) a `~purpose` decorator, and some number of JSON attachments, under the optional fields `data`, `data~attach`, and `~attach`. 

The `"data-type"` field indicates the type of data contained under the attachments.

The attachment fields are all optional, though there should be at least one.

```json
{
  "@id": "123456780",
  "@type": "https://didcomm.org/json/1.0/message",
  "~purpose": [],
  "data": {},
  "data~attach": {},
  "~attach": []
}
```

#### `~purpose`



#### `data`, `data~attach`, `~attach`

These 3 fields are optional, although at least one must be present. They carry the data which the sender is sending to the recipient, which this message wraps, which the given agents relay.

The payload transported in this message is placed in an [attachment](/concepts/0017-attachments/README.md). If the attachment is embedded or appended, the recipient is provided with the entire attachment descriptor.

The recipient-agent must be able to process all three fields.

#### Threading

A protocol built on top of generic JSON messages can include the [`~thread` decorator](/concepts/0008-message-id-and-threading/README.md) in the messages. For example, this allows the recipient-agent to relay a reply from the recipient, so the recipient is able to reply to a message.

For threading with senders or recipients that aren't aries agents, the sender-agent or recipient-agent must maintain context to correlate the DIDComm message thread, and the message thread of the communication protocol with the non-aries communicator. The lifetime of this context, for a custom protocol built on top of generic-JSON-message, is defined by the custom protocol.

##### Timing

A threaded communication may make use of the [`~timing`](/features/0032-message-timing/README.md) decorator. 

#### Communication with Non-DIDComm Edge Applications

The message sent by the sender to the sender-agent and the message sent by the recipient-agent to the recipient are expected to have their own formats defined within a specific protocol built on top of this RFC. Some general principles can guide their implementation and translation to/from the DIDComm messages sent from sender-agent to recipient-agent.

- Headers and metadata can sometimes be translated into DIDComm decorators - HTTP keep-alive to DIDComm `~timing`, for example.
- The messages in your protocol may have a message-type identifier, which can be included in the attachment descriptor.

An organization using agents to relay messages for non-DIDComm edge applications is expected to secure the connections between their relay agents and their non-DIDComm edge applications. For example, running the agent as a service in the same container. If it is necessary for the organization to have a separate endpoint or mediator agent, it is recommended to have a thin relay agent as close as possible to the edge application, so internal messages sent to the mediator are also secured by DIDComm.

## Drawbacks

## Rationale and alternatives

- Why don't we standardize data-type labels against content schemas and format definitions? The intent here is to allow custom protocols and messaging schemes to operate over DIDComm. For this we provide a message format that allows them to be constructed without a chance of collision (between message names, for example) with other DIDComm message types, and we allow custom formats to be designed without needing to standardize them through the RFC process. The data-type label allows implementors to ensure that they will not collide between any of their message types in their specific implementations. A custom schema could be defined in its own RFC.

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

