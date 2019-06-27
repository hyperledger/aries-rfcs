# 0008: Message ID and Threading
- Authors: Daniel Bluhm <daniel.bluhm@sovrin.org>, Sam Curren (sam@sovin.org), Daniel Hardman (daniel.hardman@gmail.com)
- Start Date: 2018-08-03

## Status
- Status: [ACCEPTED](/README.md#rfc-lifecycle)
- Status Date: 2018-10-01
- Status Note: Implemented broadly in Indy, but not yet elsewhere.

## Summary
[summary]: #summary

Definition of the message @id field and the ~thread [decorator](
https://github.com/hyperledger/indy-hipe/pull/71).

## Motivation
[motivation]: #motivation

Referring to messages is useful in many interactions. A standard method of adding a message ID promotes good patterns in message families. When multiple messages are coordinated in a message flow, the threading pattern helps avoid having to re-roll the same spec for each message family that needs it.

## Tutorial
[tutorial]: #tutorial

### Message IDs

Message IDs are specified with the @id attribute, which [comes from JSON-LD](
../0047-json-ld-compatibility/README.md#id).
The sender of the message is responsible for creating the message ID, and any
message can be identified by the combination of the sender and the message ID.
Message IDs should be considered to be opaque identifiers by any recipients.

#### Message ID Requirements

- A short stream of characters matching regex `[-_./a-ZA-Z0-9]{8,64}` (Note the
  [special semantics of a dotted suffix on IDs](
  ../../features/0034-message-tracing/README.md#message-ids),
  as described in the message tracing HIPE proposal)
- Should be compared case-sensitive (no case folding)
- Sufficiently unique
- UUID recommended

#### Example

```json
{
    "@type": "did:example:12345...;spec/example_family/1.0/example_type",
    "@id": "98fd8d72-80f6-4419-abc2-c65ea39d0f38",
    "example_attribute": "stuff"
}
```

The following was pulled from [this document](https://raw.githubusercontent.com/sovrin-foundation/protocol/master/janus/message-packaging.md) written by Daniel Hardman and stored in the Sovrin Foundation's `protocol` repository.


### Threaded Messages
Message threading will be implemented as a [decorator](../0011-decorators/README.md) to messages, for example:

```json
{
    "@type": "did:example:12345...;spec/example_family/1.0/example_type",
    "@id": "98fd8d72-80f6-4419-abc2-c65ea39d0f38",
    "~thread": {
        "thid": "98fd8d72-80f6-4419-abc2-c65ea39d0f38",
        "pthid": "1e513ad4-48c9-444e-9e7e-5b8b45c5e325",
        "sender_order": 3,
        "received_orders": {"did:sov:abcxyz":1}
    },
    "example_attribute": "example_value"
}
```

The `~thread` decorator is generally required on any type of response, since
this is what connects it with the original request.

#### Thread object
A thread object has the following fields discussed below:

* `thid`: The ID of the message that serves as the thread start.
* `pthid`: An optional parent `thid`. Used when branching or nesting a new interaction off of an existing one.
* `sender_order`: A number that tells where this message fits in the sequence of all messages that *the current sender* has contributed to this thread.
* `received_orders`: Reports the highest `sender_order` value that the sender has seen
  from other sender(s) on the thread. (This value is often missing if it
  is the first message in an interaction, but should be used otherwise,
  as it provides an implicit ACK.)

#### Thread ID (`thid`)
Because multiple interactions can happen simultaneously, it's important to
differentiate between them. This is done with a Thread ID or `thid`.

The Thread ID is the Message ID (`@id`) of the first message in the thread. The
first message may or may not declare the `~thread` attribute block; it
does not, but carries an
implicit `thid` of its own `@id`. 

#### Sender Order (`sender_order`)
It is desirable to know how messages within a thread should be ordered.
However, it is very difficult to know with confidence the absolute
ordering of events scattered across a distributed system. Alice and Bob
may each *send* a message before receiving the other's response, but be
unsure whether their message was *composed* before the other's.
Timestamping cannot resolve an impasse. Therefore, there is no
unified absolute ordering of all messages within a thread--but there
*is* an ordering of all messages emitted by a each participant.

In a given thread, the first message from each party has a `sender_order` value
of 0, the second message sent from each party has a `sender_order` value of 1,
and so forth. Note that *both* Alice and Bob use 0 and 1, without regard
to whether the other party may be known to have used them. This gives a
strong ordering with respect to each party's messages, and it means that
any message can be uniquely identified in an interaction by its `thid`,
the sender DID and/or key, and the `sender_order`.

#### Received Orders (`received_orders`)
In an interaction, it may be useful for the recipient of a message to
know if their last message was received. A `received_orders` value
addresses this need, and could be included as a best practice to help
detect missing messages.

In the example above, if Alice is the sender, and Bob is identified by
`did:sov:abcxyz`, then Alice is saying, "Here's my message with
index 3 (`sender_order`=3), and I'm sending it in response to your message
1 (`received_orders: {<bob's DID>: 1}`. Apparently Alice has been more chatty than
Bob in this exchange.

The `received_orders` field is plural to acknowledge the possibility of multiple
parties. In [pairwise](
https://docs.google.com/document/d/1gfIz5TT0cNp2kxGMLFXr19x1uoZsruUe_0glHst2fZ8/edit#heading=h.eurb6x3u0443)
interactions, this may seem odd. However, [n-wise](
 https://docs.google.com/document/d/1gfIz5TT0cNp2kxGMLFXr19x1uoZsruUe_0glHst2fZ8/edit#heading=h.cn50pi7diqgj)
interactions are possible (e.g., in a doctor ~ hospital ~ patient n-wise
relationship). Even in pairwise, multiple agents on either side may introduce other
actors. This may happen even if an interaction is designed to be 2-party (e.g., an
intermediate party emits an error unexpectedly).

In an interaction with more parties, the `received_orders` object has a key/value pair
for each `actor`/`sender_order`, where `actor` is a DID or a key for an agent:

```json
"received_orders": {"did:sov:abcxyz":1, "did:sov:defghi":14}
```

Here, the `received_orders` fragment makes a claim about the last `sender_order`
that the sender observed from `did:sov:abcxyz` and `did:sov:defghi`. The sender of
this fragment is presumably some other DID, implying that 3 parties are participating.
Any parties unnamed in `received_orders` have an undefined value for `received_orders`.
This is NOT the same as saying that they have made no observable contribution to the
thread. To make that claim, use the special value `-1`, as in:

```json
"received_orders": {"did:sov:abcxyz":1, "did:sov:defghi":14, "did:sov:jklmno":-1}
```

##### Example
As an example, Alice is an issuer and she offers a credential to Bob.

* Alice sends a CRED_OFFER as the start of a new thread, `@id`=98fd8d72-80f6-4419-abc2-c65ea39d0f38, `sender_order`=0. 
* Bob responds with a CRED_REQUEST, `@id`=&lt;uuid2&gt;, `thid`=98fd8d72-80f6-4419-abc2-c65ea39d0f38, `sender_order`=0, `received_orders:{alice:0}`.
* Alice sends a CRED, `@id`=&lt;uuid3&gt;, `thid`=98fd8d72-80f6-4419-abc2-c65ea39d0f38, `sender_order`=1, `received_orders:{bob:0}`.
* Bob responds with an ACK, `@id`=&lt;uuid4&gt;, `thid`=98fd8d72-80f6-4419-abc2-c65ea39d0f38, `sender_order`=1, `received_orders:{alice:1}`.

#### Nested interactions (Parent Thread ID or `pthid`)
Sometimes there are interactions that need to occur with the same party, while an
existing interaction is in-flight.

When an interaction is nested within another, the initiator of a new interaction
can include a Parent Thread ID (`pthid`). This signals to the other party that this
is a thread that is branching off of an existing interaction.

##### Nested Example
As before, Alice is an issuer and she offers a credential to Bob. This time, she wants a bit more information before she is comfortable providing a credential.

* Alice sends a CRED_OFFER as the start of a new thread, `@id`=98fd8d72-80f6-4419-abc2-c65ea39d0f38, `sender_order`=0. 
* Bob responds with a CRED_REQUEST, `@id`=&lt;uuid2&gt;, `thid`=98fd8d72-80f6-4419-abc2-c65ea39d0f38, `sender_order`=0, `received_orders:{alice:0}`.
* **Alice sends a PROOF_REQUEST, `@id`=&lt;uuid3&gt;, `pthid`=98fd8d72-80f6-4419-abc2-c65ea39d0f38, `sender_order`=0.** Note the subthread, the parent thread ID, and the reset `sender_order` value.
* **Bob sends a PROOF, `@id`=&lt;uuid4&gt;, `thid`=&lt;uuid3&gt;,`sender_order`=0, `received_orders:{alice:0}`.**
* Alice sends a CRED, `@id`=&lt;uuid5&gt;, `thid`=98fd8d72-80f6-4419-abc2-c65ea39d0f38, `sender_order`=1, `received_orders:{bob:0}`.
* Bob responds with an ACK, `@id`=&lt;uuid6&gt;, `thid`=98fd8d72-80f6-4419-abc2-c65ea39d0f38, `sender_order`=1, `received_orders:{alice:1}`.

All of the steps are the same, except the two bolded steps that are part of a nested interaction.

#### Implicit Threads

Threads reference a Message ID as the origin of the thread. This allows _any_ message to be the start of a thread, even if not originally intended. Any message without an explicit `~thread` attribute can be considered to have the following `~thread` attribute implicitly present.

```
"~thread": {
    "thid": <same as @id of the outer message>,
    "sender_order": 0
}
```

#### Implicit Replies

A message that contains a `~thread` block with a `thid` different from the outer
message `@id`, but no `sender_order` is considered an implicit reply. Implicit replies
have a `sender_order` of `0` and an `received_orders:{other:0}`. Implicit replies should only be
used when a further message thread is not anticipated. When further messages in the
thread are expected, a full regular `~thread` block should be used.

Example Message with am Implicit Reply:

```json
{
    "@id': "<@id of outer message>",
    "~thread": {
    	"thid": "<different than @id of outer message>"
	}
}
```
Effective Message with defaults in place:
```json
{
    "@id': "<@id of outer message>",
    "~thread": {
    	"thid": "<different than @id of outer message>"
    	"sender_order": 0,
    	"received_orders": { "DID of sender":0 }
	}
}
```


## Reference

[reference]: #reference

- [Message Packaging document from Sovrin Foundation Protocol Repo](https://raw.githubusercontent.com/sovrin-foundation/protocol/master/janus/message-packaging.md)
- [Very brief summary of discussion from Agent Summit on Decorators](https://docs.google.com/presentation/d/1l-po2IKVhXZHKlgpLba2RGq0Md9Rf19lDLEXMKwLdco/edit#slide=id.g29a85e4573632dc4_58)

## Drawbacks
[drawbacks]: #drawbacks

Why should we *not* do this?

## Rationale and alternatives
[alternatives]: #alternatives

- Implement threading for each message type that needs it.

## Prior art
[prior-art]: #prior-art

If you're aware of relevant prior-art, please add it here.

## Unresolved questions
[unresolved]: #unresolved-questions

- Using a wrapping method for threading has been discussed but most seemed in favor of the annotated method. Any remaining arguments to be made in favor of the wrapping method?
