# Aries RFC 0470: Role Request 0.1
- Authors: [Sam Curren](telegramsam@gmail.com)
- Since: 2020-05-06
- Status Note: initial proposal
- Start Date: 2018-05-05 
- Tags: feature, protocol

## Summary

This protocol requests the recipient to play a specified role in another protocol.

## Motivation

It is sometimes desirable to ask the other party to play a role within another protocol. Although some protocols already have a way to do this as an existing feature of the protocol, it is desirable have a general purpose way to communicate that intent.

## Tutorial

### Protocol Role Request 0.1

URI: https://didcomm.org/protocol_role_request/0.1/<messageType>

### Key Concepts

This protocol is intentionally simple: further interactions either involve a message from the requested protocol or a problem report.

### Roles

**requester**: Sends the `please_play_role` message to the `requestee`

**requestee**: Receives the `please_play_role` message from the `requestee`. Responds with a message from the specified protocol and role, or a `problem_report` indicating why that will not be done.

### States

**requested**: The _requester_ enters this state after sending a `please_play_role` message to the _requestee_.

**accepted**: Both parties enter this state after the _requestee_ responds with a message from the indicated protocol and role.

**rejected**: Both parties enter this state after the _requestee_ responds with a `problem_report` message.

### Messages

#### please_play_role

```json
{
    "@type": "https://didcomm.org/protocol_role_request/0.1/please_play_role",
    "@id": "<messageID>",
    "protocol": "<ProtocolURI>",
    "role": "<name of role within ProtocolURI>"
}
```



**protocol**: The Protocol URI

**role**: The role name specified in the specified protocol.

Note that no other information is present in this message. If information is required to start the protocol in the role, it likely warrants a message within the protocol itself.

When responding to this message, the `@id` of this message is used as a parent thread id. This applies both for messages sent as part of the requested protocol, as well as a `problem_report` message.

A `problem-report` may be sent for the following reasons:

- protocol not supported
- role not supported
- I just don't want to

## Drawbacks

Why should we *not* do this?

## Rationale and alternatives

- Creating a standard message prevents the need for similar messages in other protocols without specialized requirements.

## Unresolved questions

- Is using the `problem-report` message as described the right answer? Should it be adopted?
## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

Name / Link | Implementation Notes
--- | ---
 | 

