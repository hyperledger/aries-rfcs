# Aries RFC 0351: Generic JSON Message
- Authors: [Filip Burlacu](filip.burlacu@securekey.com)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2019-12-16
- Status Note: implementation is being explored by SecureKey
- Supersedes:
- Start Date: 2018-12-05
- Tags: feature, protocol

## Summary

This protocol defines a format for sending arbitrary JSON payloads using DIDComm, for use cases where business logic or external (to agent) applications need to communicate over DIDComm.

## Motivation

Aries users may need to support communication that doesn't fit within a particular existing Aries protocol. In cases where machine-readable data needs to be transmitted, a defined format for sending such messages allows those users to transmit data over DIDComm, without making custom agents with custom DIDComm message formats that might collide with future, standard DIDComm message formats.

Beyond allowing agents to implement custom protocols, this protocol allows clients that aren't Aries agents to communicate JSON messages over DIDComm using Aries agents as [mediators or relays](/concepts/0046-mediators-and-relays/README.md). 

## Tutorial

#### Name and Version

This is the generic JSON message protocol, defined uniquely by the URI:

    "https://didcomm.org/json/1.0"

#### Key Concepts

> This RFC assumes familiarity with [mediators and relays](/concepts/0046-mediators-and-relays/README.md), [attachments](/concepts/0017-attachments/README.md), and [message threading](/concepts/0008-message-id-and-threading/README.md)

This protocol has two primary roles, the **sender** and the **receiver**. The sender constructs a message with a JSON payload, which the receiver parses. This protocol supports optional threading, so the receiver can send a response to the sender. 

Secondary roles/sub-roles: In a use-case where the *sender* is not a DIDComm-enabled agent, we introduce the role of **sender-agent**, which is the agent that relays messages to/from the sender, translating from DIDComm to non-DIDComm messaging. Similarly, for a *receiver* that is not a DIDComm-enabled agent, we introduce the role of **receiver-agent**, which serves the same purpose for the receiver. 

Note: if we refer to a sender-agent or receiver-agent, and an implementation doesn't have one, the relevant behaviour would instead be in the sender/receiver.

With JSON messaging, custom agents can communicate domain-specific information or implement domain-specific protocols without breaking compatibility with the wider DIDComm standards. Agents can also [relay](/concepts/0046-mediators-and-relays/README.md) messages between entities that are not DIDComm-enabled, allowing a wide range of communication protocols to use DIDComm to transport their messages.

This protocol does not define the format of the content of a message, except that it be an [embedded attachment](/concepts/0017-attachments/README.md). Specific implementations may specify the exact format they expect. To support this flexibility, this protocol defines that every message must contain a `data-type` field, so a sender can indicate the correct format which the receiver should use to parse a message.

#### Threading

This protocol supports but does not require the use of the `~thread` decorator to provide message threading.

## Reference

#### Message Format

This protocol defines one DIDComm message format, of type `https://didcomm.org/json/1.0/message`. A `message` only requires (in addition to the standard contents of DIDComm messages) a `data-type` field and a `content~attach` embedded JSON attachment. 

The `"data-type"` field indicates the type of data contained under the `content~attach` attachment. 

```json
{
  "@id": "123456780",
  "@type": "https://didcomm.org/json/1.0/message",
  "data-type": "",
  "content~attach": {}
}
```

##### `data-type`

The sender must provide a `data-type` identification string constant, which indicates, for the receiver, how the data is to be processed, and indicates, for the receiver-agent, which receiver(s) to send the message to.

The receiver registers on a particular data-type value with the receiver-agent, in which case the receiver-agent must relay any message with that data-type value to the receiver. Multiple receivers can register with a single receiver-agent on a single data-type value, and a receiver can register with multiple receiver-agents on a data-type value.

The receiver must be aware of the `data-type` value of a received message, whether by registering a specific handler for a specific `data-type` value, or by being sent the `data-type` value in addition to the content.

##### `content~attach`

The payload transported in this message is placed in an [embedded attachment](/concepts/0017-attachments/README.md#embedding). The receiver is provided with the entire attachment descriptor.

#### Threading

A protocol built on top of generic JSON messages can include [`~thread` decorators](/concepts/0008-message-id-and-threading/README.md) in the messages. For example, this allows the receiver-agent to relay a reply from the receiver, so the receiver is able to reply to a message.

For threading with senders or receivers that aren't aries agents, the sender-agent or receiver-agent must maintain context to correlate the DIDComm message thread, and the message thread of the communication protocol with the non-aries communicator. The lifetime of this context, for a custom protocol built on top of generic-JSON-message, is defined by the custom protocol.

## Drawbacks

## Rationale and alternatives

- Why don't we standardize data-type labels against content schemas and format definitions? The intent here is to allow custom protocols and messaging schemes to operate over DIDComm. For this we provide a message format that allows them to be constructed without a chance of collision (between message names, for example) with other DIDComm message types, and we allow custom formats to be designed without needing to standardize them through the RFC process. The data-type label allows implementors to ensure that they will not collide between any of their message types in their specific implementations. A custom schema could be defined in its own RFC.

## Prior art

- Compare against the [basic-message](/features/0095-basic-message/README.md) protocol, which uses aries agents as relays for person-person (or machine-person) communication. In contrast, this protocol uses aries agents as relays for machine-machine communication.
- The non-normative data type definition (as opposed to a standardized system like MIME types) is similar to Intents in Android development.

## Unresolved questions

- Do we need to enforce that the message content be an embedded attachment?
- Are there further semantics to define in this RFC rather than leave for specific implementations?
- Are there any standard data types that we should define identifiers and formats for, rather than leaving everything up to implementer's choice?

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

*Implementation Notes* [may need to include a link to test results](README.md).

Name / Link | Implementation Notes
--- | ---
 | 

