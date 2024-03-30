# Aries RFC 0092: Transports Return Route

- Authors: [Sam Curren](mailto:sam@sovrin.org)
- Status: [ACCEPTED](/README.md#accepted)
- Since: 2019-12-06
- Status Note:  
- Supersedes: [INDY HIPE PR 116](https://github.com/hyperledger/indy-hipe/pull/116)
- Start Date: 2019-03-04
- Tags: [feature](/tags.md#feature)

## Summary

Agents can indicate that an inbound message transmission may also be used as a return route for messages. This allows for transports of increased efficiency as well as agents without an inbound route.

## Motivation

Inbound HTTP and Websockets are used only for receiving messages by default. Return messages are sent using their own outbound connections. Including a decorator allows the receiving agent to know that using the inbound connection as a return route is acceptable. This allows two way communication with agents that may not have an inbound route available. Agents without an inbound route include mobile agents, and agents that use a client (and not a server) for communication.

This decorator is intended to facilitate message communication between a client based agent (an agent that can only operate as a client, not a server) and the server based agents they communicate directly with. Use on messages that will be forwarded is not allowed.

## Tutorial

When you send a message through a connection, you can use the `~transport` decorator on the message and specify `return_route`. The value of `return_route` is discussed in the Reference section of this document.

```json
{
    "~transport": {
        "return_route": "all"
    }
}
```

## Reference

- `return_route` has the following acceptable values:

  - `none`: Default. No messages should be returned over this connection.
  - `all`: Send all messages for this cryptographic key over the connection.
  - `thread`: Send all messages matching the cryptographic key and thread specified in the `return_route_thread` attribute.

  The `~transport` decorator should be processed after unpacking and prior to routing the message to a message handler.

  For HTTP transports, the presence of this message decorator indicates that the receiving agent MAY hold onto the connection and use it to return messages as designated. HTTP transports will only be able to receive at most one message at a time. Websocket transports are capable of receiving multiple messages.

  Compliance with this indicator is optional for agents generally, but required for agents wishing to connect with client based agents.

## Drawbacks

- Application varies between transports, adding complexity to agent development.

## Rationale and alternatives

- Using a transport level decorator makes this behavior transport agnostic.

## Prior art

The [Decorators RFC](../../concepts/0011-decorators/README.md) describes scope of decorators. Transport isn't one of the scopes listed.

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

Name / Link | Implementation Notes
--- | ---
[Aries Cloud Agent - Python](https://github.com/hyperledger/aries-cloudagent-python) | Contributed by the government of British Columbia.
[Aries Protocol Test Suite](https://github.com/hyperledger/aries-protocol-test-suite) | Used in Tests
