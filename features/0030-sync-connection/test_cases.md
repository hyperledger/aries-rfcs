# Test Cases for Sync Connection Protocol

### Given

Let us assume that Alice and Bob each have 4 agents (A.1-A.4 and B.1-B.4, respectively),
and that each of these agents possesses one key pair that's authorized to authenticate
and do certain things in the DID Doc.

A.1 and B.1 are routing (cloud) agents, where A.2-4 and B.2-4 run on edge devices
that are imperfectly connected. A.1 and B.1 do not appear in the `authentication`
section of their respective DID Docs, and thus cannot login on Alice and Bob's behalf.

Let us further assume that Alice and Bob each have 
two "recovery keys": A.5 and A.6; B.5 and B.6. These keys are not held by agents, but
are printed on paper and held in a vault, or are sharded to friends. They are
highly privileged but very difficult to use, since they would have to be digitized or
unsharded and given to an agent before they would be useful.

"Admin" operations like adding keys and granting privileges to them require either
one of the privileged recovery keys, or 2 of the other agent keys to agree.

Let us further assume that the initial state of Alice's domain, as described above,
is known as A.state[0], and that Bob's state is B.state[0].

These states may be represented by the following `authorization` section of each
DID Doc:

[TODO]

### Scenarios (each starts over at the initial conditions)

1. A.1 attempts to rotate its key by sending a `sync_state` message to A.2.
__Expected outcome__: Should receive ACK, and A.2's state should be updated.
Once A.1 receives the ACK, it should commit the pending change in its own
 key. Until it receives the ACK, it should NOT commit the pending change.

2. Like #1, except that message goes to B.1 and B.1's state is what should be
updated.

3. A.1 attempts to send a message to B.1, using the `~relstate` decorator, claiming
states with `hash(A.state[0])` and `hash(B.state[0])`. __Expected outcome__:
B.1 accepts the message.

4. As #3, except that A.1 claims the current states are random hashes. __Expected
outcome__: B.1 sends back a problem report, plus two `sync_state` messages (one
with `who` = "me" and one with `who` = "you"). Each has an
empty `deltas` array and `base_state` = the correct base state hash.

5. A.1 attempts to rotate the key for A.2 by sending a `sync_state` message to
any other agent. __Expected outcome__: change is rejected with a __problem report__
that points out that A.1 is not authorized to rotate any key other than itself.

 