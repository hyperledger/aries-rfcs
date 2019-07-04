# 0030: Sync Connection Protocol 1.0 (and related minor protocols)
- Authors: Daniel Hardman <daniel.hardman@gmail.com>, 
  Devin Fisher <devin.fisher@evernym.com>, Sam Curren <sam@sovrin.org>

## Status
- Status: [PROPOSED](/README.md#rfc-lifecycle)
- Status Date: 2018-10-01. Revised 2019-07-03.
- Status Note: used by the [peer DID method spec](https://openssi.github.io/peer-did-method-spec).
  Not yet implemented.
  Supersedes [Indy HIPE PR #104](https://github.com/hyperledger/indy-hipe/pull/104).

## Summary

Define a set of non-centralized protocols (that is, ones that do not involve a
common store of state like a blockchain), whereby parties using [peer DIDs](
https://openssi.github.io/peer-did-method-spec) can synchronize the state of
their shared relationship by direct communication with one another.

## Motivation

For Alice and Bob to interact, they must establish and maintain state.
This state includes all the information in a DID Document: endpoint, keys, and
associated authorizations.

The [DID exchange protocol](../0023-did-exchange/README.md)
describes how these DID Docs are initially exchanged as a relationship is built.
However, its mandate ends when a connection is established. This RFC focuses on
how peers maintain their relationship thereafter, as DID docs evolve.

## Tutorial

>__Note 1__: This RFC assumes you are thoroughly familiar with terminology and
constructs from the [peer DID method spec](
https://openssi.github.io/peer-did-method-spec). Check there if you need
background. 

>__Note 2__: Most protocols between identity owners deal only with messages that
cross a domain boundary--what Alice sends to Bob, or vice versa. What Alice
does internally is generally none of Bob's business, since interoperability
is a function of messages that are passed to external parties, not
events that happen inside one's own domain. However, this protocol has some
special requirements. Alice may have multiple agents, and Bob's behavior must
account for the possibility that each of them has a different view of current
relationship state. Alice has a responsibility to share and harmonize the view
of state among her agents. Bob doesn't need to know exactly how she does
it--but he _does_ need to know that she's doing it, somehow--and he may need to
cooperate with Alice to intelligently resolve divergences. For this reason, we
describe the protocol as if it involved message passing _within_ a domain in
addition to message passing _across_ domains. This is a simplification. The
true, precise requirement for compliance is that implementers must pass
messages _across_ domains as described here, and they must _appear to an
outside observer_ as if they were passing messages within their domain as the
protocol stipulates--but if they achieve the intra-domain results using some
other mechanism besides DIDComm message passing, that is fine.

### Name and Version

This RFC defines the `sync_connection` protocol, version 1.x, as identified by the
following [PIURI](../../concepts/0003-protocols/uris.md#piuri):

    did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/sync_connection/1.0

Of course, subsequent evolutions of the protocol will replace `1.0` with
an appropriate update per [semver](../../concepts/0003-protocols/semver.md)
rules.

Two related, minor protocols are also defined in subdocs of this RFC:

* [Query Connection State Protocol](query-connection-state-protocol/README.md)
* [Abandon Connection Protocol](abandon-connection-protocol/README.md)

### Roles

The only role defined in this protocol is `peer`. However, see [this note in the
peer DID method spec](https://dhh1128.github.io/peer-did-method-spec/#roles-and-agents)
for some subtleties.

### States

This is a steady-state protocol, meaning that the state of participants does
not change. Instead, all participants are continuously in a `syncing` state.

### Messages

##### `sync_state`

This message announces that the sender wants to synchronize state with the
recipient. This could happen because the sender suspects they are out of sync,
 or because the sender wants to change the state by announcing new, never-before-seen
 information. The recipient can be another agent within the same sovereign
domain, or it can be an agent on the other side of the relationship. A
sample looks like this:

```JSON
{
  "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/sync-connection/1.0/sync_state",
  "@id": "e61586dd-f50e-4ed5-a389-716a49817207",
  "for": "did:peer:11-479cbc07c3f991725836a3aa2a581ca2029198aa420b9d99bc0e131d9f3e2cbe",
  "base_hash": "d48f058771956a305e12a3b062a3ac81bd8653d7b1a88dd07db8f663f37bf8e0",
  "base_hash_time": "2019-07-23 18:05:06.123Z",
  "deltas": [
    {
      "id": "040aaa5e-1a27-40d8-8d53-13a00b82d235",
      "change": "ewogICJwdWJsaWNLZXkiOiBbCiAgICB...ozd1htcVBWcGZrY0pDd0R3biIKICAgIH0KICBdCn0=",
      "by": [ {"key": "H3C2AVvL", "sig": "if8ooA+32YZc4SQBvIDDY9tgTa...i4VvND87PUqq5/0vsNFEGIIEDA=="} ],
      "when": "2019-07-18T15:49:22.03Z"
    }
  ]
}
```

Note that the values in the `change` and `sig` fields have been shortened
for readability.

The properties in this message include:

*`for`: Identifies which state is being synchronized.
* `base_hash`: Identifies a shared state against which deltas should be
  applied. See [State Hashes](#state-hashes) for more details.
* `base_hash_time`: An [ISO 8601-formatted UTC timestamp](
  ../../concepts/0074-didcomm-best-practices/README.md#_time),
  identifying when the sender believes that the base hash became the
  current state. This value need not be highly accurate, and different agents in
  Alice and Bob's ecosystem may have different opinions about an appropriate
  timestamp for the selected base hash. Like timestamps in email headers, it merely
  provides a rough approximation of timeframe.
* `deltas`: Gives a list of deltas that should be applied to the
  DID doc, beginning at the specified state.

When this message is received, the following processing happens:

* The `base_hash`  and `deltas` properties are checked for
consistency. If any errors are detected, a [`problem_report` message](
../0035-report-problem/README.md)
is returned, using [message threading](
 ../../concepts/0008-message-id-and-threading/README.md)
 to pinpoint the message that triggered the problem. No further processing occurs.
* If the recipient already has the same state, it sends an [ACK](
../0015-acks/README.md).
* If the recipient knew about a subset of the delta, but not all of it, it
applies what is left of the delta, and sends an ACK.
* If the recipient has a more evolved state, the recipient sends a reply
that is a new `sync_state` message informing the sender of new information. As
with the ACKs, this new message is known to be a reply to the original `sync_state`
because its `~thread` decorator identifies the previous message's `@id` as its
`thid`.
* If the recipient does not recognize the `base_hash`, it selects a hash from
a point in time earlier than `base_hash_time` and sends back a new `sync_state`
message with that earlier base.
* Because of the nature of the CRDT rules in the peer DID spec, truly
problematic merge conflicts cannot occur. All objects in the DID doc that
have an `id` property are immutable, and ordering of operations does not
need to be highly consistent. Furthermore, an object in both deleted and
undeleted state must be deemed to be deleted. However, if the recipient
detects a trivial conflict, the delta with the `id` that sorts smaller/lower
is selected.

### State Hashes

To reliably describe the state of a DID doc at any given moment, we need a
quick way to characterize its content. We could do this with a merkle tree,
but the strong ordering of that structure is problematic--different participants
may receive different deltas in different orders, and this is okay. What matters
is whether they have applied the same set of deltas.

To achieve this goal, the `id` properties of all received deltas are sorted
and concatenated, and then the string undergoes a SHA256 hash. This produces
a state hash.

### Best Practices

The following best practices will dramatically improve the robustness of state
synchronization, both within and across domains. Software implementing this protocol
is not required to do any of these things, but they are strongly recommended.

##### The `~relstate` decorator

Agents should attach the `~relstate` decorator to messages to help each other discover when
state synchronization is needed. This decorator has the following format:

```JSON
"~relstate": [ 
  {"did": "<my did>", "state_hash": "<my state hash>"},
  {"did": "<your did>", "state_hash": "<your state hash>"}
]
```

In a message _within_ a domain, where "me" and "you" are synonyms, "them" should be used
instead of "you"; the goal is to always describe the current known state hashes for each
domain. It is also best practice for the recipient of the message to send a
`sync_state` message back to the sender any time it detects a discrepancy.

##### Pending Commits

Agents should never commit to a change of state until they know that at least one other
agent (on either side of the relationship) agrees to the change. This will significantly
decrease the likelihood of merge conflicts. For example, an agent that wants to rotate a key
should report the key rotation to _someone_, and receive an ACK, before it commits to use
the new key. This guarantees that there will be gravitas and confirmation of the change,
and is a reasonable requirement, since a change that nobody knows about is useless, anyway.

##### Routing (Cloud) Agent Rules

It is best practice for routing agents (typically in the cloud) to enforce the following
rules:

* Never deliver a message _to_ an edge agent that shouldn't receive it, according to state
 that the routing agent knows. Instead, reply with a `problem_report` about the state
 being out of sync, followed by a `sync_state` message to initiate a reconciliation of
 the differences.
* Never deliver a message _from_ an agent that shouldn't be sending it, according to state
that the routing agent knows. As with the previous rule, initiate a reconciliation first.
* Attempt to propagate state changes proactively.

##### Proactive Sync

Any time that an agent has reason to suspect that it may be out of sync, it should
attempt to reconcile. For example, if a mobile device has been turned off for an
extended period of time, it should check with other agents to see if state has evolved,
once it is able to communicate again.

### Test Cases

Because this protocol encapsulates a lot of potential complexity, and many corner
cases, it is particularly important that implementations exercise the full range
of scenarios in the [Test Cases doc](test_cases.md). Community members are encouraged
to submit new test cases if they find situations that are not covered.

## Reference

### State and Sequence Rules

[TODO: create state machine matrices that show which messages can be sent in
which states, causing which transitions]

### Message Type Detail

[TODO: explain every possible field of every possible message type]

### Localized Message Catalog

[TODO: define some localized strings that could be used with these messages,
in errors or at other generally useful points?]
