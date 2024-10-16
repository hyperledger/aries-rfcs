# Aries RFC 0095: Basic Message Protocol 1.0

- Authors: Sam Curren
- Status: [ADOPTED](/README.md#adopted)
- Since: 2019-08-06
- Status Note:  
- Supersedes: [Indy 0033](https://github.com/hyperledger/indy-hipe/edit/master/text/0033-basic-message/README.md)
- Start Date: 2019-01-16
- Tags: [feature](/tags.md#feature), [protocol](/tags.md#protocol), [test-anomaly](/tags.md#test-anomaly)

## Summary

The BasicMessage protocol describes a stateless, easy to support user message protocol. It has a single message type used to communicate.

## Motivation

It is a useful feature to be able to communicate human written messages. BasicMessage is the most basic form of this written message communication, explicitly excluding advanced features to make implementation easier.

## Tutorial

#### Roles

There are two roles in this protocol: **sender** and **receiver**. It is anticipated that both roles are supported by agents that provide an interface for humans, but it is possible for an agent to only act as a sender (do not process received messages) or a receiver (will never send messages).

#### States

There are not really states in this protocol, as sending a message leaves both parties in the same state they were before.

#### Out of Scope

There are many useful features of user messaging systems that we will not be adding to this protocol. We anticipate the development of more advanced and full-featured message protocols to fill these needs. Features that are considered out of scope for this protocol include:

- read receipts
- emojii responses
- typing indicators
- message replies (threading)
- multi-party (group) messages
- attachments

## Reference

**Protocol**: https://didcomm.org/basicmessage/1.0/

**message**

- sent_time - timestamp in ISO 8601 UTC
- content - content of the user intended message as a string.
- The `~l10n` block SHOULD be used, but only the `locale` presented.

Example:

```json
{
    "@id": "123456780",
    "@type": "https://didcomm.org/basicmessage/1.0/message",
    "~l10n": { "locale": "en" },
    "sent_time": "2019-01-15 18:42:01Z",
    "content": "Your hovercraft is full of eels."
}
```

## Drawbacks

- Creating this basicmessage may inhibit the creation of more advanced user messaging protocols.
- After more advanced user messaging protocols are created, the need to support this protocol may be annoying.

## Rationale and alternatives

- Basic user messaging creates an easy useful feature in the early days of agent messaging.
- Even in the presence of better protocols, it can still be useful for basic devices or service messaging.

## Prior art

BasicMessage has parallels to SMS, which led to the later creation of MMS and even the still-under-development RCS.

## Unresolved questions

- Receive receipts (NOT read receipts) may be implicitly supported by an ack decorator with pre-processing support.

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

Name / Link | Implementation Notes
--- | ---
[Indy Cloud Agent - Python](https://github.com/hyperledger/indy-agent/python) | Reference agent implementation contributed by Sovrin Foundation and Community; [MISSING test results](/tags.md#test-anomaly)
[Aries Framework - .NET](https://github.com/hyperledger/aries-framework-dotnet) | .NET framework for building agents of all types; [MISSING test results](/tags.md#test-anomaly)
[Streetcred.id](https://streetcred.id/) | Commercial mobile and web app built using Aries Framework - .NET; [MISSING test results](/tags.md#test-anomaly)
[Aries Cloud Agent - Python](https://github.com/hyperledger/aries-cloudagent-python) | Contributed by the government of British Columbia.; [MISSING test results](/tags.md#test-anomaly)
[Aries Static Agent - Python](https://github.com/hyperledger/aries-staticagent-python) | Useful for cron jobs and other simple, automated use cases.; [MISSING test results](/tags.md#test-anomaly)
[Aries Protocol Test Suite](https://github.com/hyperledger/aries-protocol-test-suite) | ; [MISSING test results](/tags.md#test-anomaly)

