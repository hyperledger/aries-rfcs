# Aries RFC 0020: Message Types

- Authors: Daniel Bluhm, Sam Curren
- Status: [ACCEPTED](/README.md#accepted)
- Since: 2019-05-24
- Status Note:  
- Supersedes: [HIPE 0021 Message Types](https://github.com/hyperledger/indy-hipe/tree/main/text/0021-message-types)
- Start Date: 2018-07-06
- Tags: [concept](/tags.md#concept)

## Summary

Define structure of message type strings used in agent to agent communication, describe their resolution to documentation URIs, and offer guidelines for protocol specifications.

## Motivation

A clear convention to follow for agent developers is necessary for interoperability and continued progress as a community.

## Tutorial

A "Message Type" is a required attribute of all communications sent between parties. The message type instructs the receiving agent how to interpret the content and what content to expect as part of a given message.

Types are specified within a message using the `@type` attribute:

```jsonc
{
    "@type": "<message type string>",
    // other attributes
}
```

Message types are URIs that may resolve to developer documentation for the message type, as described in [Protocol URIs](../0003-protocols/README.md#message-type-and-protocol-identifier-uris). We recommend that message type URIs be HTTP URLs.

### Aries Core Message Namespace

`https://didcomm.org/` is used to namespace protocols defined by the community as "core protocols" or protocols that agents should minimally support.

The `didcomm.org` [DNS entry](https://whois.whoisxmlapi.com/lookup-report/zjRXrYwV5r) is currently controlled by the [Decentralized Identity Foundation (DIF)](https://identity.foundation) based on their role in standardizing the [DIDComm Messaging specification](https://identity.foundation/didcomm-messaging/spec/).

### Protocols

Protocols provide a logical grouping for message types. These protocols, along with each type belonging to that protocol, are to be defined in future RFCs or through means appropriate to subprojects.

#### Protocol Versioning

Version numbering should essentially follow [Semantic Versioning 2.0.0](https://semver.org/), excluding patch version
number. To summarize, a change in the major protocol version number indicates a breaking change while the minor protocol version number indicates non-breaking additions.

## Message Type Design Guidelines

These guidelines are guidelines on purpose. There will be situations where a good design will have to choose between conflicting points, or ignore all of them. The goal should always be clear and good design.

### Respect Reserved Attribute Names

Reserved attributes are prefixed with an `@` sign, such as `@type`. Don't use this prefix for an attribute, even if use of that specific attribute is undefined.

### Avoid ambiguous attribute names

Data, id, and package, are often terrible names. Adjust the name to enhance meaning. For example, use  `message_id` instead of `id`.

### Avoid names with special characters

Technically, attribute names can be any valid json key (except prefixed with @, as mentioned above). Practically, you should avoid using special characters, including those that need to be escaped. Underscores and dashes [_,-] are totally acceptable, but you should avoid quotation marks, punctuation, and other symbols.

### Use attributes consistently within a protocol

Be consistent with attribute names between the different types within a protocol. Only use the same attribute name for the same data. If the attribute values are similar, but not exactly the same, adjust the name to indicate the difference.

### Nest Attributes only when useful

Attributes do not need to be nested under a top level attribute, but can be to organize related attributes. Nesting all message attributes under one top level attribute is usually not a good idea.

### Design Examples

#### Example 1

```json
{
    "@type": "did:example:00000;spec/pizzaplace/1.0/pizzaorder",
    "content": {
        "id": 15,
        "name": "combo",
        "prepaid?": true,
        "ingredients": ["pepperoni", "bell peppers", "anchovies"]
    }
}
```

Suggestions: Ambiguous names, unnecessary nesting, symbols in names.

#### Example 1 Fixed

```json
{
    "@type": "did:example:00000;spec/pizzaplace/1.0/pizzaorder",
    "table_id": 15,
    "pizza_name": "combo",
    "prepaid": true,
    "ingredients": ["pepperoni", "bell peppers", "anchovies"]
}
```

## Reference

- [Daniel Hardman's Agent Summit Notes](https://docs.google.com/document/d/1TP_7MKfuIrlY3rz4cz_tuuCFi7hdUWifeKwr5h-QTYM/edit)
- [Stephen Curran's presentation summarizing the Agent Summit](https://docs.google.com/presentation/d/1l-po2IKVhXZHKlgpLba2RGq0Md9Rf19lDLEXMKwLdco/edit)
- [Semantic Versioning](../0003-protocols/README.md#semver-rules-for-protocols)
- [DIDComm Message Anatomy](../0021-didcomm-message-anatomy/README.md)

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

Name / Link | Implementation Notes
--- | ---
[Indy Cloud Agent - Python](https://github.com/hyperledger/indy-agent/python) | Reference agent implementation contributed by Sovrin Foundation and Community
[Aries Framework - .NET](https://github.com/hyperledger/aries-framework-dotnet) | .NET framework for building agents of all types
[Streetcred.id](https://streetcred.id/) | Commercial mobile and web app built using Aries Framework - .NET
[Aries Cloud Agent - Python](https://github.com/hyperledger/aries-cloudagent-python) | Contributed by the government of British Columbia.
[Aries Static Agent - Python](https://github.com/hyperledger/aries-staticagent-python) | Useful for cron jobs and other simple, automated use cases.
[Aries Framework - Go](https://github.com/hyperledger/aries-framework-go) | For building agents, hubs and other DIDComm features in GoLang.
[Connect.Me](https://www.evernym.com/blog/connect-me-sovrin-digital-wallet/) | Free mobile app from Evernym. Installed via app store on iOS and Android. 
[Verity](https://www.evernym.com/products/) | Commercially licensed enterprise agent, SaaS or on-prem. 
