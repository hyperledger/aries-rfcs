# 0030: Sync Connection Protocol 1.0
- Authors: Daniel Hardman <daniel.hardman@gmail.com>, Devin Fisher <devin.fisher@evernym.com>, Sam Curren <sam@sovrin.org>

## Status
- Status: [PROPOSED](/README.md#rfc-lifecycle)
- Status Date: 2018-10-01
- Status Note: depended on by peer DID method spec. Not yet implemented.
  Supersedes [Indy HIPE PR #104](https://github.com/hyperledger/indy-hipe/pull/104).

## Summary

Define non-centralized protocols (that is, ones that do not involve a common
store of state like a blockchain), whereby parties synchronize the state of
their shared relationship by direct communication with one another.

## Motivation

For Alice and Bob to interact, they must establish and maintain state.
This state includes all the information in a DID Document: endpoint, keys, and
associated authorizations.

The [connect protocol](../0023-connect/README.md)
describes how these DID Docs are initially exchanged as a relationship is
built. However, its mandate ends when a connection is established. The
protocol described here focuses on how peers maintain their relationship
thereafter, as DID Docs evolve.

# Tutorial
[tutorial]: #tutorial

### Background Concepts

##### Setting Expectations

It is possible to have perfect synchronization of relationship state, both
within and across domains. However, doing so requires a central source of
truth. That is how traditional databases and source code control tools like
Subversion/CVS/Perforce work--everybody who wants to make a state change submits the change
to the central authority, and the central authority applies the change and requires
all clients to cope with it before they submit more changes. But it is not reasonable
to require everybody who has a self-sovereign identity to centralize their
own management of that identity in a cloud. There are excellent cybersecurity
reasons why centralization is dangerous, and there are privacy and robustness
and scale and cost reasons to avoid it as well.

This protocol takes a different path. It is inherently decentralized. This
means its behavior and outcomes are much more like git. All participants
in a relationship--all the agents owned by Alice and Bob--effectively have
their own state "repo", and each change is commited locally and then "pushed"
to a broader audience. As with git, it is possible to detect and silently,
automatically, and confidently merge divergent states. And as with git, it is
also possible to end up with a merge conflict. The potential for merge conflicts
is an unavoidable consequence of decentralization.

We could attempt to manage relationship state with byzantine consensus, as
some blockchains do. This route is fraught with problems, since the agents
owned by Alice and Bob are not guaranteed to be highly or reliably connected,
and they may not have the numbers required by certain algorithms. We could
do proof-of-work-based consensus--but this would burden the protocol with
time and computational load that we can ill afford.

Besides, any consensus protocol or blockchain-like mechanism arbitrating
between different views of state really represents a new centralization.
If we are serious about decentralization, we accept its drawbacks
along with its advantages, and we find a way to be robust, efficient, easy
to implement, and compatible with great UX. That is the goal, and this
protocol achieves it, just as git solves problems for millions of
developers every day. Merge conflicts should be quite rare, in practice
(see the [Best Practices](#best-practices) section), and even when they do
occur, they have straightforward resolutions.

TODO: discuss strong vs. weak ordering

##### Connection versus Non-Connection State

The state that's managed by this protocol is only the state that embodies
connection knowledge in a DID Doc. Plenty of other state may exist, such
as a history of credentials presented in either direction, a log of
other messages and interactions, rich policy configured in either
direction, and so forth. Such things are not managed in this protocol.
(TODO: see [this note](#applying-this-protocol-to-other-state) about
reusing the protocol for other problems.)

A particular type of state that may cause confusion is authorization
state. The authorization state that's present in DID Docs and that's
covered by this protocol is authorization to manage DID Doc operations
(see "[Types of Changes](#types-of-changes)" below for a list).
But there may be other types of authorization state as well. For
example, Alice may ask Bob to help her enforce spending limits on
her devices, and she may express these limits as authorizations. Maybe
her phone is only authorized to spend money up to $10 per day, whereas
her laptop can spend up to $1000, and three of her agents must agree to
spend any amount greater than $1000. This sort of authorization is not
encoded in a DID Doc. Instead, it should be represented with something
like a verifiable credential, or a simple digitally signed permission slip.
Therefore, it is out of scope here. 

##### Authentication versus Authorization

A manager, a teller, and a vice president may all be legitimate employees
of a bank. However, the actions that each is authorized to perform on
behalf of their employer may be different.

The `authentication` section of a DID Doc enumerates keys that can act as
the DID subject (what the DID identifies). When such a key is used, it is
like proving that they are an employee of the bank. A key from the
`authentication` section of a DID Doc
is able to exercise the identity of the DID subject.

_But what is that key authorized to do?_
Bank tellers can transact business, but probably not announce the appointment
of a new manager. Bank vice presidents may be able to appoint managers or
tellers, but for safety reasons may not be allowed to handle money
directly.

Delegating specific privileges is the job of the `authorization` section.

##### Types of Changes

All of the following __operations__ can be performed on a DID Doc, and must be
supported by the relationship management protocol:

* Adding, removing, or rotating keys (op codes = `add_key`, `rem_key`, and `update_key`)
* Adding and removing key references from the `authentication` or
  `authorization` section (this must be done at the same time as `add_key` or `rem_key`,
  since key privileges are immutable after creation)
* Adding, removing, or reconfiguring endpoints (op codes = `add_endpoint`, `rem_endpoint`, `update_endpoint`)

##### Authorizing Keys

All keys have the privilege of rotating themselves. Keys that have the privilege
of adding keys can only add keys with equal or lesser privileges than themselves.
All other authorizations on keys must be specified in the `authorization` section
of a DID doc. Its structure is:

* `“authorization”: [` list of __grants__ `]`
* __grant__ = `{ "let": ` __recipient__ `, “do”: ` __privs__ `}`
* __recipient block__ = one of the following:
    * `“key”:` _keyref_, e.g., `“#1”`
    * `"group":` 
    * `“and”: [` list of __recipient block__ `]`
    * `“or”: [` list of __recipient block__ `]`
    * `“m_of_n”: {“m”:` _number_`, “n”: [` list of __recipient block__ `]}`
* __privs__ = a string that enumerates the privileges being granted.
  This string is list-like, but is not modeled using a JSON list or dict
  because of some specialized syntax that conflicts with canonicalization
  requirements. Its format is space-delimited list of
  privileges, where each privilege is an op code name. The list must be
  sorted in ascending alphabetical order to aid normalization.

Basically, authorizations are a series of grants. Grants identify the recipient,
which is either a key or a combination of keys, and the privileges that the recipient
is receiving.

An example might be:

[![authorization sample](authorization.png)](authorization.json)

What this says is:

* Key #1 (`"let":"#1"`) can add keys, add key references to the authentication section, remove
keys, remove keys from the authentication section, and remove any authorization
from any key or group of keys.

* Adding authorizations to a key can be done in either (`"let":{"or"...`) of the following ways:
  * Key #1 and one other key can approve the change.
  * Any three (`"m_of_n":{"m":3...`) of keys #2-#5 can approve the change.

##### DID Doc Deltas

In traditional databases, the concept of a _transaction_ exists to
bundle changes in a way that guarantees that the whole set of changes either
succeeds or fails, as an indivisible unit. This allows funds to be
transferred out of one account, and into another--but never to be
lost in limbo with only one of the two transfers complete.

This same requirement exists in relationship management. Several
relationship operations may need to be performed as a unit on a DID Doc.
For example, an old key may need to be retired (op code = `rem_key`), a
new key may need to be announced (op code = `add_key`), and the new key
may need to be given authorizations (op code = `add_authz`), all as
an atomic unit of change.

To facilitate this, the relationship management protocol deals in 
a larger unit of change than an individual operation. This is a
DID Doc __delta__, and it consists of a list of operations that must
be applied in order. For security reasons, all operations in a delta
must share a common authorization. This means that it is illegal for
key 1 to authorize part of the list, and for key 2 to authorize another
part. All keys must authorize the complete delta, so each authorizer
knows the full scope of the change they are endorsing. (If key 2's authorization is only
relevant to part of the delta, it still endorses all of it. Having
redundant or unnecessary authorization on a particular operation is
never an error.)

##### Across Domains Versus Within A Domain

Most protocols between identity owners deal only with messages that cross
a domain boundary--what Alice sends to Bob, or vice versa. What Alice
does internally is generally none of Bob's business. Interoperability
is only a function of messages that get passed to external parties, not
things that happen inside one's own domain.

However, this protocol has some special requirements. Alice may have
multiple agents, and Bob's behavior must account for the possibility that
each of them has a different view of current relationship state. Alice
has a responsibility to share and harmonize the view of state
among her agents. Bob doesn't need to know exactly how she does it--but
he _does_ need to know that she's doing it, somehow--and he may need to
cooperate with Alice to intelligently resolve divergences.

For this reason, we are going to describe this protocol as if it involved
message passing _within_ a domain in addition to
message passing _across_ domains. This is a simplification. The true, precise
requirement for compliance with the protocol is that implementers must pass
messages _across_ domains as described here, and they must _appear to an
outside observer_ as if they were passing messages within their domain as
the protocol stipulates--but if they achieve the within-domain results
using some other mechanism besides DID Comm message passing, that is fine.

### Message Family

The messages used to establish, maintain, and end a relationship are members of
the `connection` message family. This family is identified by the following DID
reference (a form of URI [TODO: hyperlink to def of DID reference in DID spec]):

    did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/connections/1.0

Of course, subsequent evolutions of the message family will replace `1.0` with
an appropriate update per [semver](https://semver.org) rules.

Note that this is the same message family used in the [connect protocol](
../0023-connect/README.md).

Besides the messages used in the connection protocol, the following messages are
defined within this family: `read_state`, `state_response`, `sync_state` and `leave`.

##### `state_request`

This message asks the recipient to report the state it knows for a particular
relationship. It is essentially a request for a DID Doc, so it plays the same
role as DID resolution to a DID Doc when a ledger is queried. It looks like this:

[![sample state_request message](state_request.png)](state_request.json)

The properties of this message include:

* `@type` and `@id`: Required. Standard for DID Comm messages.
* `for`: Required. A DID that identifies which state is being queried.
* `as_of_time`: Optional. The timestamp for which state is being queried. If
this property is omitted or equal to `null`, and `as_of_hash` is also
omitted, then the state as of "now" is what the sender is asking for.
* `as_of_hash`: Optional, and mutually exclusive with `as_of_time`. Identifies
a specific state that is being queried, by
the [hash of that state](#state-hashes). Optional. Using this property
is somewhat unusual, because the sender of the message has to know
to know of a state's hash, without knowing the state itself. This may be
helpful for advanced use cases.

The two optional properties are rarely used. The simplest and most
common form of the message contains only `@type`, `@id`, and `for`.

Familiar DID Communications [decorators](
../../concepts/0011-decorators/README.md) can be used with this message.
For example, to note that the request will expire or grow stale if
not serviced quickly, [`~timing.expires_time` or `~timing.stale_time`](
../features/00xx-message-timing/README.md#tutorial)
can be added. Other decorators could be used to describe the preferred
route to use in the return response, and so forth.

##### `state_response`

This message is the response to a `state_request` message, and looks like this:

[![sample state_response message](state_response.png)](state_response.json)

##### State Machine

This is a classic two-step request~response interaction, so it uses the
predefined state machines for any `requester` and `responder`:

[![state machines](state-machines.png)](https://docs.google.com/spreadsheets/d/1smY8qhG1qqGs0NH9g2hV4b7mDqrM6MIsmNI93tor2qk/edit)
 
##### `sync_state`

This message announces that the sender wants to synchronize state with the
recipient. This could happen because the sender suspects they are out of sync,
 or because the sender wants to change the state by announcing new, never-before-seen
 information. The recipient can be another agent within the same sovereign
domain, or it can be an agent on the other side of the relationship. A
sample looks like this:

[![sample sync_state message](sync_state.png)](sync_state.json)

The properties in this message include:

*`for`: Identifies which state is being synchronized.
* `base_hash`: Identifies a __state hash__ that provides a reference against
  which deltas can be applied. The sender should select a state hash that
  it expects the recipient to recognize. For example, if this is the first
  change that Alice is making to her DID Doc since the relationship was
  established, then this is the hash of the normalized version of the DID
  Doc that she gave Bob at the end of the connection protocol. If this the
  hundredth change to Alice's state in a relationship that is years old, it
  may be a state hash from an hour or a day ago. Conceptually, this value is
  much like a a commit hash in git. See [State Hashes](#state-hashes) for
  details about how state hashes are computed.
* `base_hash_time`: An [ISO 8601-formatted UTC timestamp](
  ../../concepts/00xx-conventions/README.md#_time),
  identifying when the sender believes that the base hash became the
  current state. This value need not be highly accurate, and different agents in
  Alice and Bob's ecosystem may have different opinions about an appropriate
  timestamp for the selected base hash. Like timestamps in email headers, it merely
  provides a rough approximation of timeframe.
* `deltas`: Gives a list of deltas that should be applied to the
  DID Doc, beginning at the specified state.
  
  Each delta is a JSON object with properties `ops`, `delta_time`, `result_hash`,
  and `proofs`:
  
    * `ops` is an ordered list of operations, `ops`. Each operation
      is a JSON object that has an `op` code such as "add_key", and a `fragment`
      that provides the added data, or the key for removed data, or the key + new
      value for modified data.
    * `delta_time` tells when the delta was proposed.
    * `result_hash` is like a checksum; it verifies that both parties agree on the
      resulting state when the delta is applied.
    * `proofs` is an array that contains one
      or more signatures over `result_hash` that shows that the change is properly
      authorized. In this example, the key referenced by `#4` is apparently authorized
      to add and remove keys, so key 4 signs the result hash.

When this message is received, the following processing happens:

* The `base_hash`, `deltas`, `result_hash`, and `proofs` properties are checked for
consistency. If any errors are detected, a [`problem_report` message](
../00xx-report-problem/README.md)
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
* If the recipient detects a conflict, it attempts to merge states. If the
merge is successful, it sends a new `sync_state` that shows the merge. If the
merge is not successful, then a merge conflict exists, and the merge conflict
policy for the sovereign domain of the associated DID is invoked. See "[Merges
and Merge Conflicts](#merges-and-merge-conflicts)".

##### `leave`

This message is used to announce that a party is abandoning the relationship. In a self-sovereign
paradigm, abandoning a relationship can be done unilaterally, and does not require formal
announcement. Indeed, sometimes a formal announcement is impossible, if one of the parties
is offline. So while using this message is encouraged and best practice, it is not mandatory.

A `leave` message from Alice to Bob looks like this:

[![sample leave message](leave.png)](leave.json)

If Bob receives a message like this, he should assume that Alice no longer considers
herself part of "us", and take appropriate action. This could include destroying
data about Alice that he has accumulated over the course of their relationship,
removing her peer DID and its public key(s) and endpoints from his wallet, and so
forth. The nature of the relationship, the need for a historical audit trail, regulatory
requirements, and many other factors may influence what's appropriate; the protocol
simply requires that the message be understood to have permanent termination semantics.

It may be desirable to use the [`~please_ack` decorator](
../0015-acks/README.md#requesting-an-ack-please_ack)
to request acknowledgment that the severance has been processed. The example shows
this, but including it is optional.

### State Hashes

To reliably describe the state of a DID Doc at any given moment, we need a
quick way to characterize its content. We do this with a SHA256 hash of the
doc. However, we have to normalize the doc first, so irrelevant changes do
not cause an inaccurate view of differences. We normalize the DID Doc
according to the [JSON Canonicalization Scheme (draft RFC)](https://tools.ietf.org/id/draft-rundgren-json-canonicalization-scheme-00.html).
This is a very simple, deterministic algorithm that can be implemented in
a couple dozen lines of recursive code.

There is no requirement that DID Docs need to be stored or exchanged in normalized form--
only that when they are hashed, the input to the hash must be normalized first.

### Merges and Merge Conflicts

The main challenge with a protocol like this is that Alice and Bob may not have an internally
consistent view of their own domains. For example, if Alice has 3 agents (`A.1`, `A.2`, and `A.3`--
see [SSI Notation](../../concepts/0006-ssi-notation/README.md)),
`A.1` may be a phone that is only powered on about half the time. `A.1` may change its key and
report that fact to Bob's agents, then get lost in the couch cushions. Meanwhile, `A.3` may
rotate its key as well, without learning about the update from `A.1`.

In such a case, Bob's agents see two claims about Alice's current state. Let's use the notation
`A.state[A.1]` to represent the state asserted by `A.1`, and `A.state[A.3]` to represent the state
asserted by `A.3`.

Now, key rotations are relatively independent operations, and they do not interfere with one
another. They do not have any ordering constraints. Therefore, Bob's agents should be able to prove
the validity of a merge in this case, with the following algorithm:

##### Merge Algorithm

1. Verify that `A.state[A.1]` and `A.state[A.3]` share a common base hash, and that
`A.state[base] + A.state[A.1]` and `A.state[base] + A.state[A.3]` are each valid
sequences, when analyzed separately.
2. Perform the synthesized sequence: `A.state[base] + A.state[A.1~A.3]` and see
what state hash results. Here, the `~` operator represents the idea that the deltas from `A.3`
are applied, but instead of being applied to `A.state[base]` (as they would be in normal
processing of `sync_state`), they are applied to `A.state[A.1]`.
3. Perform the opposite synthesized sequence: `A.state[base] + A.state[A.3~A.1]` and see
what state hash results.
4. Compare the two state hashes from `A.state[A.3~A.1]` and `A.state[A.1~A.3]`.
5. If they are equal, then the order of
the two changes doesn't matter, and they do not conflict. Generate a new `sync_state`
message conveying `A.state[A.1~A.3]` (always pick the change from the lower-numbered
agent first) and send it back so the other agent can also do the
merge.
6. If they are not equal, then the order of the two changes matters, and/or the changes
conflict in some way. This could happen if one of the deltas revoked an authorization
upon which the other delta depends. In such a case, invoke the __merge conflict resolution
policy__ of the identity owner.

The _merge conflict resolution policy_ is something that each identity owner can specify.
[TODO: where is it specified? In a message, or in the DID Doc?] Some possible policies might be:

* Designate one agent (or a small quorum of agents ) that acts as a judge to decide how to
resolve the merge conflict.
* Hold a popular election, in which each agent submits its preferred view of the state to
all peers, and the peers all vote on which view they want. Whichever view gets the most
votes wins.
* Pick whichever hash is smaller.
* Leave the agents in stalemate until the relationship is abandoned.

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
[reference]: #reference

### State and Sequence Rules

[TODO: create state machine matrices that show which messages can be sent in
which states, causing which transitions]

### Message Type Detail

[TODO: explain every possible field of every possible message type]

### Localized Message Catalog

[TODO: define some localized strings that could be used with these messages,
in errors or at other generally useful points?]
