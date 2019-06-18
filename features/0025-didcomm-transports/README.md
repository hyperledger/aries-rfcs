# 0025: DIDComm Transports
- Author: Sam Curren <sam@sovrin.org>
- Start Date: 2019-02-26

## Status

- Status: [PROPOSED](/README.md#rfc-lifecycle)
- Status Date: 2019-05-27
- Status Note: Supersedes [INDY PR 94](https://github.com/hyperledger/indy-hipe/pull/94)

## Summary

This RFC Details how different transports are to be used for Agent Messaging.

## Motivation

Agent Messaging is designed to be transport independent, including message encryption and agent message format. Each transport does have unique features, and we need to standardize how the transport features are (or are not) applied. 

## Reference

Standardized transport methods are detailed here. 

### HTTP(S)

HTTP(S) is the first transport for DID Communication that has received heavy attention.

- Messages are transported via HTTP POST.
- The MIME Type for the POST request is `application/didcomm-envelope-enc`.
- A received message should be responded to with a 202 Accepted status code. This indicates that the request was received, but not necessarily processed. Accepting a 200 OK status code is allowed.
- POST requests are considered transmit only by default. No agent messages will be returned in the response. This behavior may be modified with additional signaling.
- Using HTTPS with TLS 1.2 or greater with a forward secret cipher will provide Perfect Forward Secrecy (PFS) on the transmission leg.

#### Known Implementations

[Python Reference Agent](https://github.com/hyperledger/indy-agent/tree/master/python)

[Indy Catalyst Agent](https://github.com/bcgov/indy-catalyst/tree/master/agent)

### Websocket

Websockets are an efficient way to transmit multiple messages without the overhead of individual requests. 

- Each message is transmitted individually in an Encryption Envelope.
- The trust of each message comes from the Encryption Envelope, not the socket connection itself.
- Websockets are considered transmit only by default. Messages will only flow from the agent that opened the socket. This behavior may be modified with additional signaling.
- Using Secure Websockets (wss://) with TLS 1.2 or greater with a forward secret cipher will provide Perfect Forward Secrecy (PFS) on the transmission leg.

#### Known Implementations

[Python Reference Agent](https://github.com/hyperledger/indy-agent/tree/master/python)


### Other Transports

Other transports may be used for Agent messaging. As they are developed, this RFC should be updated with appropriate standards for the transport method. A PR should be raised against this doc to facilitate discussion of the proposed additions and/or updates. New transports should highlight the common elements of the transport (such as an HTTP response code for the HTTP transport) and how they should be applied.

### Message Routing

The transports described here are used between two agents. In the case of [message routing](https://github.com/hyperledger/indy-hipe/tree/master/text/0022-cross-domain-messaging), a message will travel across multiple agent connections. Each intermediate agent (see [Mediators and Relays](../../concepts/0046-mediators-and-relays/README.md)) may use a different transport. These transport details are not made known to the sender, who only knows the keys of Mediators and the first endpoint of the route. 

### Message Context

The transport used from a previous agent can be recorded in the message trust context. This is particularly true of controlled network environments, where the transport may have additional security considerations not applicable on the public internet. The transport recorded in the message context only records the last transport used, and not any previous routing steps as described in the Message Routing section of this document.

### Transport Testing

Transports which operate on IP based networks can be tested by an Agent Test Suite through a transport adapter. Some transports may be more difficult to test in a general sense, and may need specialized testing frameworks. An agent with a transport not yet supported by any testing suites may have non-transport testing performed by use of a routing agent.

## Drawbacks

Setting transport standards may prevent some uses of each transport method.

## Rationale and alternatives

- Without standards for each transport, the assumptions of each agent may not align and prevent communication before each message can be unpacked and evaluated.

## Prior art

Several agent implementations already exist that follow similar conventions.

## Unresolved questions
