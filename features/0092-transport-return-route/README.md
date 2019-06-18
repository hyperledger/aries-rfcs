# 0092: Transports Return Route
- Author: Sam Curren sam@sovrin.org
- Start Date: 2019-03-04

## Status
- Status: [PROPOSED](/README.md#rfc-lifecycle)
- Status Date: 2019-06-18
- Status Note: Supersedes [INDY HIPE PR 116](https://github.com/hyperledger/indy-hipe/pull/116)

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

Outbound messages can return the `~transport` decorator as well, with a `queued_message_count` attribute. This is useful for HTTP transports which can only receive one return message at a time. When a client sees this decorator on a message, they can use it to immediately reconnect to receive another queued message. The number of messages returned depends on the properties of the transport used.

```json
{
    "~transport": {
        "queued_message_count": 7
    }
}
```

If transport decorators are desired but no message needs to be sent, a `noop` message can be sent. This is useful if making a request to an agent just to establish a return route.

```json
{
    "@type": "?/1.0/noop",
    "~transport": {
        "return_route": "thread",
        "return_route_thread": "1234567899876543"
    }
}
```

## Reference

- `return_route` has the following acceptable values:

  - `none`: Default. No messages should be returned over this connection.
  - `all`: Send all messages for this cryptographic key over the connection.
  - `thread`: Send all messages matching the cryptographic key and thread specified in the `return_route_thread` attribute.

  The `~transport` decorator should be processed after unpacking and prior to routing the message to a message handler.

  For HTTP transports, the presence of this message decorator indicates that the receiving agent MAY hold onto the connection and use it to return messages as designated. HTTP transports will only be able to receive at most one message at a time. Receiving subsequent messages can be accomplished by sending any other message with the same decorator. If you have no message to send, you may use the `noop` message type.

  Websocket transports are capable of receiving multiple messages. 

  Compliance with this indicator is optional for agents generally, but required for agents wishing to connect with client based agents. 

## Drawbacks

- Application varies between transports, adding complexity to agent development.
- Requiring outbound message queuing has agent architectural implications.

## Rationale and alternatives

- Using a transport level decorator makes this behavior transport agnostic.

## Prior art

The [Decorators RFC](../../concepts/0011-decorators/README.md) describes scope of decorators. Transport isn't one of the scopes listed.

## Unresolved questions

- Is `transport` the right name?
- Should `~transport` be a bundle of related attributes, or should the be identified individually?
- What family should `noop` be in?
- Should the receiving agent indicate what type of support is present, like a `call_back_in_seconds`: 5 attribute?
