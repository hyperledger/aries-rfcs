# 0000: DID Resolution Protocol
- Author: Markus Sabadello (markus@danubetech.com)
- Start Date: 2019-07-08

## Status
- Status: [PROPOSED](/README.md#rfc-lifecycle)
- Status Date: 2019-07-08
- Status Note: Not implemented, but has been discussed as part of the Aries [DID Resolution work](https://github.com/hyperledger/aries-rfcs/issues/101)

## Summary

Describes a DIDComm **request-response** protocol that can send a request to a remote DID Resolver
service to resolve DIDs and dereference DID URLs.

## Motivation

DID Resolution is an important feature of Aries. It is a prerequisite for the `unpack()` function in
[DIDComm](https://github.com/hyperledger/aries-rfcs/tree/master/concepts/0005-didcomm), especially in
[Cross-Domain Messaging](../../concepts/0094-cross-domain-messaging/README.md), since cryptographic
keys must be discovered from DIDs in order to enable trusted communication between the
[agents](https://github.com/hyperledger/aries-rfcs/tree/master/concepts/0004-agents) associated with DIDs.
DID Resolution is also required for other operations, e.g. for discovering
[DIDComm service endpoints](../../features/0067-didcomm-diddoc-conventions).

Ideally, DID Resolution should be implemented as a local API (**TODO:** link to other RFC?). In some
cases however, the DID Resolution function may be provided by a remote service. This RFC describes
a DIDComm request-response protocol for such a remote DID Resolution service.

## Tutorial

DID Resolution is a function that returns a DID Document for a DID. This function
can be accessed via "local" bindings (e.g. SDK calls, command line tools) or "remote"
bindings (e.g. HTTP(S), DIDComm).

A DID Resolver MAY invoke another DID Resolver in order to delegate (part of) the
DID Resolution and DID URL Dereferencing algorithms. For example, a DID Resolver
may be invoked via a "local" binding (such as an Aries library call), which in turn
invokes another DID Resolver via a "remote" binding (such as HTTP(S) or DIDComm).

[![DID Resolver Bindings](binding-chained.png)](https://w3c-ccg.github.io/did-resolution/#binding-architectures)

**TODO:** More details and explanation

### Name and Version

This defines the `did_resolution` protocol, version 0.1, as identified by the
following [PIURI](https://github.com/hyperledger/aries-rfcs/blob/master/concepts/0003-protocols/uris.md#piuri):

    did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/did_resolution/0.1

### Key Concepts

DID Resolution is the process of obtaining a DID Document for a given DID. This is one of four required operations that can be performed on any DID ("Read"; the other ones being "Create", "Update", and "Deactivate"). The details of these operations differ depending on the DID method. Building on top of *DID Resolution*, *DID URL Dereferencing* is the process of obtaining a resource for a given DID URL. Software and/or hardware that is able to execute these processes is called a DID Resolver. 

- **DID Resolver**: Software and/or hardware that is capable of DID Resolution and optionally DID URL Dereferencing for at least one DID method.
- **DID Resolution**: An algorithm that takes a DID plus additional options as input and produces a DID Document or a DID Resolution Result as output. This algorithm relies on the "Read" operation of the applicable DID method.
- **DID URL Dereferencing**: An algorithm that takes a DID URL plus additional options as input and produces a DID Document, a DID Resolution Result, or various other types of resources as output. This algorithm relies on DID Resolution.
- **DID Method**: A definition of how a specific DID scheme can be implemented on a specific distributed ledger or network, including the precise method(s) by which DIDs are resolved and deactivated and DID Documents are written and updated. 

### Roles

There are two *parties* and two *roles* (one for each party) in the `did_resolution` protocol: A `requester` and `resolver`. 

The `requester` wishes to resolve DIDs or dereference DID URLs.

The `resolver` conforms with the [DID Resolution Specification](https://w3c-ccg.github.io/did-resolution/). It is capable of
resolving DIDs for at least one DID method.

### States

##### States for `requester` role

|                      | EVENTS:         | send `resolve`                      | receive `resolve_result` |
| -------------------- | --------------- | ------------------------------------ | -------------------------- |
| **STATES**           |                 |                                      |                            |
| preparing-request    |                 | transition to "awaiting_response"    | *different interaction*    |
| awaiting-response    |                 | *impossible*                         | transition to "done"       |
| done                 |                 |                                      |                            |

##### States for `resolver` role

|                      | EVENTS:         | receive `resolve`                   | send `resolve_result`    |
| -------------------- | --------------- | ------------------------------------ | -------------------------- |
| **STATES**           |                 |                                      |                            |
| awaiting-request     |                 | transition to "resolving"            | *impossible*               |
| resolving            |                 | *new interaction*                    | transition to "done"       |
| done                 |                 |                                      |                            |

### Messages

All messages in this protocol are part of the "did_resolution 0.1" message
family uniquely identified by this DID reference: `did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/did_resolution/0.1`

##### `resolve` message

The protocol begins when the `requester` sends a `resolve` message
to the `resolver`. It looks like this:

	{
		"@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/did_resolution/0.1/resolve",
		"@id": "xhqMoTXfqhvAgtYxUSfaxbSiqWke9t",
		"did": "did:sov:WRfXPg8dantKVubE3HX8pw",
		"input_options": {
			"result_type": "did-document",
			"no_cache": false
		}
	}

`@id` is required here, as it establishes a [message thread](../../concepts/0008-message-id-and-threading)
that makes it possible to connect a subsequent response to this request.

`did` is required.

`input_options` is optional. 

For further details on the `did` and `input_options` fields, see
[Resolving a DID](https://w3c-ccg.github.io/did-resolution/#resolving) in the DID Resolution Spec.

##### `resolve_result` message

The `resolve_result` is the only allowed direct response to the `resolve` message.
It represents the result of the [DID Resolution](https://w3c-ccg.github.io/did-resolution/#resolving) function and contains a DID Document.

It looks like this:

	{
		"@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/did_resolution/0.1/resolve_result",
		"@thread": { "thid": "xhqMoTXfqhvAgtYxUSfaxbSiqWke9t" },
		"did_document": {
			"@context": "https://w3id.org/did/v0.11",
			"id": "did:sov:WRfXPg8dantKVubE3HX8pw",
			"service": [{
				"type": "did-communication",
				"serviceEndpoint": "https://agent.example.com/"
			}],
			"publicKey": [{
				"id": "did:sov:WRfXPg8dantKVubE3HX8pw#key-1",
				"type": "Ed25519VerificationKey2018",
				"publicKeyBase58": "~P7F3BNs5VmQ6eVpwkNKJ5D"
			}],
			"authentication": ["did:sov:WRfXPg8dantKVubE3HX8pw#key-1"]
		}
	}

If the `input_options` field of the `resolve` message contains an entry `result_type` with value `resolution-result`, then the
`resolve_result` message contains a more extensive [DID Resolution Result](https://w3c-ccg.github.io/did-resolution/#did-resolution-result),
which includes a DID Document plus additional metadata: 

	{
		"@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/did_resolution/0.1/resolve_result",
		"@thread": { "thid": "xhqMoTXfqhvAgtYxUSfaxbSiqWke9t" },
		"did_document": {
			"@context": "https://w3id.org/did/v0.11",
			"id": "did:sov:WRfXPg8dantKVubE3HX8pw",
			"service": [{
				"type": "did-communication",
				"serviceEndpoint": "https://agent.example.com/"
			}],
			"publicKey": [{
				"id": "did:sov:WRfXPg8dantKVubE3HX8pw#key-1",
				"type": "Ed25519VerificationKey2018",
				"publicKeyBase58": "~P7F3BNs5VmQ6eVpwkNKJ5D"
			}],
			"authentication": ["did:sov:WRfXPg8dantKVubE3HX8pw#key-1"]
		},
		"resolver_metadata": {
			"driverId": "did:sov",
			"driver": "HttpDriver",
			"retrieved": "2019-07-09T19:73:24Z",
			"duration": 1015
		},
		"method_metadata": {
			"nymResponse": { ... },
			"attrResponse": { ... }
		}
	}

### Constraints

**TODO**

## Reference

- [DID Spec](https://w3c-ccg.github.io/did-spec/)
- [DID Resolution Spec](https://github.com/w3c-ccg/did-resolution)

### Messages

### Examples

### Collateral

### Localization

### Message Catalog

## Drawbacks

Using a remote DID Resolver service should only be considered a fallback when a local DID Resolver
cannot be used. See [Binding Architectures](https://w3c-ccg.github.io/did-resolution/#binding-architectures)
and [w3c-ccg/did-resolution#28](https://github.com/w3c-ccg/did-resolution/issues/28).

**TODO:** Add more details and explanation.

## Rationale and alternatives

**TODO**

## Prior art

**TODO:** Mention HTTP(S) binding for DID Resolution, supported e.g. by DIF Universal Resolver,
explain why a DIDComm binding is preferable.

**TODO:** Discuss other (historic) discovery protocols, e.g. Webfinger, XRI Resolution

## Unresolved questions

**TODO:** Decide whether the DID Resolution and DID URL Dereferencing functions should
be exposed as the same message type, or as two different message types (including responses).
