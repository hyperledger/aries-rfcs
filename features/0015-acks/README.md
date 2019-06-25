# 0015: ACKs
- Author: Daniel Hardman <daniel.hardman@gmail.com>
- Start Date: 2018-12-26

## Status
- Status: [PROPOSED](/README.md#rfc-lifecycle)
- Status Date: 2019-12-26
- Status Note: Broadly socialized and beginning to be implemented. Several
  protocols assume ACK behavior. May be nearing the maturity and uptake
  appropriate for ACCEPTED status. Note: this RFC supersedes [Indy HIPE
  PR #77](https://github.com/hyperledger/indy-hipe/pull/77).

## Summary

Explains how one party can request, and another party can send, acknowledgment
messages (ACKs) to confirm receipt and clarify the status of complex processes.

## Motivation
[motivation]: #motivation

An __acknowledgment__ or __ACK__ is one of the most common procedures in protocols
of all types. We need a flexible, powerful, and easy way to request and send such
messages in agent-to-agent interactions.

## Tutorial

Confirming a shared understanding matters whenever independent parties interact.
We buy something on Amazon; moments later, our email client chimes to tell us of
a new message with subject "Thank you for your recent order." We verbally accept
a new job, but don't rest easy until we've also faxed the signed offer letter
back to our new boss. We change a password on an online account, and get a text
at our recovery phone number so both parties know the change truly originated
with the account's owner.

When formal acknowledments are missing, we get nervous. And rightfully so; most
of us have a story of a package that was lost in the mail, or a web form
that didn't submit the way we expected.

Agents interact in very complex ways. They may use multiple transport mechanisms,
across varied protocols, through long stretches of time. While we usually expect
messages to arrive as sent, and to be processed as expected, a vital tool in the
agent communication repertoire is the ability to request and receive
acknowledgments to confirm a shared understanding.

### Implicit ACKs

[Message threading](../../concepts/0008-message-id-and-threading/README.md) includes
a lightweight, automatic sort of ACK in the form of the `~thread.received_orders` field.
This allows Alice to report that she has received Bob's recent message that had
`~thread.sender_order` = N. We expect threading to be best practice in many use cases,
and we expect interactions to often happen reliably enough and quickly enough that
implicit ACKs provide high value. If you are considering ACKs but are not familiar
with that mechanism, make sure you understand it, first. This RFC offers a
supplement, not a replacement.

### Explicit ACKs

Despite the goodness of implicit ACKs, there are many circumstances where a
reply will not happen immediately. Explicit ACKs can be vital here.

Explicit ACKS may also be vital at the end of an interaction, when work is finished:
a credential has been issued, a proof has
been received, a payment has been made. In such a flow, an implicit ACK meets the
needs of the party who received the final message, but the other party may want
explicit closure. Otherwise they can't know with confidence about the final
outcome of the flow.

Rather than inventing a new "interaction has been completed successfully" message
for each protocol, an all-purpose `ack` message type is recommended. It looks like
this:

[![sample ack](ack1.png)](ack1.json)

It may also be appropriate to send an ack at other key points in an interaction
(e.g., when a key rotation notice is received).

#### Requesting an ack (`~please_ack`)

A protocol may stipulate that an ack is always necessary in certain circumstances.
Launch mechanics for spacecraft do this, because the stakes for a miscommunication
are so high. In such cases, there is no need to request an ack, because it is
hard-wired into the protocol definition. However, acks make a channel more chatty,
and in doing so they may lead to more predictability and correlation for
point-to-point communications. Requiring an ack is not always the right choice.
For example, an ack should probably be optional at the end of credential issuance
("I've received your credential. Thanks.") or proving ("I've received your proof,
and it satisfied me. Thanks.").

In addition, circumstances at a given moment may make an ad hoc ack desirable even
when it would normally NOT be needed. Suppose Alice likes to bid at online auctions.
Normally she may submit a bid and be willing to wait for the auction to unfold
organically to see the effect. But if she's bidding on a high-value item and
is about to put her phone in airplane mode because her plane's ready to take off,
she may want an immediate ACK that the bid was accepted.

The dynamic need for acks is expressed with the `~please_ack` message [decorator](
../../concepts/0011-decorators/README.md). In its simplest form, it looks
like this: `"~please_ack": {}`.

This says, "Please send me an ack as soon as you receive this message."

#### Adopting acks

As discussed in [0003: Protocols](../../concepts/0003-protocols/README.md), a protocol can [adopt the ack message into
its own namespace](../../concepts/0003-protocols/template.md#adopted-messages).
This allows the type of an ack to change from:
    `did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/notification/1.0/ack`
to something like:
    `did:sov:protocolOwnersDID;spec/otherProtocol/2.0/ack`.
Thus, message routing
logic can see the ack as part of the other protocol, and send it to the relevant
handler--but still have all the standardization of generic acks.

#### Advanced Features (experimental)

(The features in this section are part of the 1.0 spec, but are not required to
be implemented to achieve 1.0 compliance. We describe them to show what may
be possible in the future.)

<blockquote>
A fancier version of `ack` might look like this:

[![sample ~please_ack](please_ack.png)](please_ack.json)

This says, "For the message that I already sent you, with 
@id=b271c889-a306-4737-81e6-6b2f2f8062ae,
please acknowledge that you've seen it as soon as you get this new message, and
please send me a new ack every 6 hours as long as status is still pending. Then
send me a final ack clarifying the outcome of the message once its outcome is
known."

This sort of `~please_ack` might make sense when Alice expected a quick resolution,
but got silence from Bob. She refers back to the message that she thought would
finalize their interaction, and she asks for ongoing status every 6 hours until
there's closure. A `message_id` is optional; normally it's omitted since the message
needing an ack is the same message where ack is requested. But including `message_id`
allows Alice to change her mind about an ack after she's sent a message.

The concept of "outcome" is relevant for interactions with a meaningful
delay between the final actions of one actor, and the time when the product of
those actions is known. Imagine Alice uses A2A messages to make an offer on a
house, and Bob, the homeowner, has 72 hours to accept or reject. The default ack
event, *message processing*, happens when Alice's offer arrives. The *outcome*
event for Alice's offer happens when the offer is accepted or rejected, and may
be delayed up to 72 hours. Similar situations apply to protocols where an
application is submitted, and probably to many other use cases.

The notion of "on receipt" matters if the message requesting the ack is not the same
as the message that needs acknowledgment. This type of ack may help compensate for
transmission errors, among other things.
</blockquote>

### When an ack doesn't come

All ack behaviors are best effort unless a protocol stipulates otherwise. This is
why the decorator name begins with `please`. A party that requests an explicit ack
cannot reason strongly about status when the ack doesn't come. The other party may
be offline, may be unable or unwilling to support fancy acks (or even simple ones),
or may be communicating through a channel that's unreliable.

However, a party that receives a `~please_ack` can, in an `ack` response, indicate that
it is not going to comply with everything that was requested. This is best practice if
a misalignment is known in advance, as it allows the ack requester to adjust
expectations. For example, the fancier `~please_ack` shown above could trigger the
following ack on receipt:

[![ack with ack_deny](ack2.png)](ack2.json)

Here, `deny` tells the recipient that, although the `receipt` request in the
previous `~please_ack.on` was honored, and the `outcome` request will probably be
honored as well, the recipient cannot expect an ack every 6 hours. (The sender may
still send acks at their discretion; the denial just says that this behavior can't
be counted on.)

### ack status

The `status` field in an ack tells whether the ack is final or not with respect to
the message being acknowledged. It has 3 predefined values: `OK` (which means an
outcome has occurred, and it was positive); `FAIL` (an outcome has occurred, and
it was negative); and `PENDING`, which acknowledges that no outcome is yet known.
In addition, more advanced usage is possible. See the [details in the Reference
section](#status).

### Relationship to `problem-report`

Negative outcomes do not necessarily mean that something bad happened; perhaps
Alice comes to hope that Bob rejects her offer to buy his house because she's
found something better--and Bob does that, without any error occurring. This
is not a FAIL in a problem sense; it's a FAIL in the sense that the offer to
buy did not lead to the outcome Alice intended when she sent it.

This raises the question of errors. Any time an unexpected *problem*
arises, best practice is to report it to the sender of the message that
triggered the problem. This is the subject of the [problem reporting mechanism](
https://github.com/hyperledger/indy-hipe/blob/459a055/text/error-reporting/README.md).

A `problem_report` is inherently a sort of ACK. In fact, the `ack` message type
and the `problem_report` message type are both members of the same `notification`
message family. Both help a sender learn about status. Therefore, a request or
requirement for an `ack` can *often* be satisfied by a `problem_report` message.
Where this is truly the case, it is recommended, as it decreases chattiness.

But notice the hedge word "often." We are hedging for at least three reasons.
First, some `ack`s may be sent before a final outcome, so a final `problem_report`
may not be enough. Second, some `problem_report`s are warnings that do not report
a definitive outcome; messages like this aren't final and thus don't satisfy the
`on: [OUTCOME]` ack request. Third, an ack request may be sent after a previous
`ack` or `problem_report` was lost in transit. Because of these caveats, developers
whose code creates or consumes acks should be thoughtful about where the two message
types overlap, and where they do not. Carelessness here is likely to cause subtle,
hard-to-duplicate surprises from time to time.

### Signed (Non-repudiable) acks
[TODO: how do you ask for an ACK that commits its sender to the acknowledgment in
a way that's provable to third parties? Open email to Mike Lodder...]

### Muliplexed acks
[TODO: how do you ask for, and supply, an ACK to all of Alice's agents instead
of just to the one who sent the ACK? Does each agent need to request the ACK
separately? Are there denial-of-service or other security issues?]

### Custom ACKs

This mechanism cannot address all possible ACK use cases. Some ACKs may
require custom data to be sent, and some acknowledgment schemes may be more
sophisticated or fine-grained that the simple settings offered here.
In such cases, developers should write their own ACK message type(s) and
maybe their own decorators. However, reusing the field names and conventions
in this RFC may still be desirable, if there is significant overlap in the
concepts. 

# Reference
[reference]: #reference

### `~please_ack` decorator

##### __`message_id`__
Asks for an acknowledgment of a message other than the one
that's decorated. Usually omitted, since most requests for an
ACK happen in the same message that wants acknowledgment.

##### __`on`__
Describes the circumstances under which an ack is desired. Possible
values in this array include `RECEIPT`, `OUTCOME`, and strings that express a
time interval, as [documented in the RFC that discusses date- and time-related conventions](
../../concepts/0074-didcomm-best-practices/README.md#_dur).
Support for acks on a time interval is an advanced feature and should not be
depended upon in the general case.

In addition, it is possible to name protocol states in this array. To understand this, let's
return to the example of Alice making an offer on a house. Suppose that the `home-buy`
protocol names and defines the following states for the owner who receives an offer:
`waiting-for-other-offers`, `evaluating-all-offers`, `picking-best-offer`. All of
these states would be passed through by Bob after Alice sends her message, and
she could request an ack to be sent with each state, or with just some of them:

```JSON
"on": ["evaluating-all-offers", "OUTCOME"]
```
  
The order of items in the `on` array is not significant, and any unrecognized
values in it should be ignored.
  
### `ack` message

##### __`status`__

Required. As discussed [above](#ack-status), this tells whether the ack is final
or not with respect to the message being acknowledged. Besides the 3 predefined
values, protocol states may be named, with the same semantics as used in the
`on` array of an `~please_ack` decorator (see just above). That is, the status
may contain 'evaluating-all-offers' to tell Alice that Bob has now entered that
phase.

##### __`~thread.thid`__

Required. This links the `ack` back to the message that requested it.

All other fields in an `ack` are present or absent per requirements of ordinary
messages.

### Examples

Suppose AliceCorp and Bob are involved in credential issuance. Alice is an issuer;
Bob wants to hold the issued credential.

##### Happy Path

In the final required message of the `issue-credential` protocol, AliceCorp sends
the credential to Bob. But AliceCorp wants to know for sure that Bob has received it,
for its own accounting purposes. So it decorates the final message with an ack
request:

```JSON
"~please_ack: {}"
```

Bob honors this request and returns an `ack` as soon as he receives it. The
interesting field is `status`, which look like this: `"status": "OK"` (or,
if the `issue-credential` protocol defines a final state for the holder called
`now-holding`, Bob could be more explicit and send '"status": "now-holding"'.

##### Delayed Issuance

Suppose instead that partway through the issuance protocol, a message gets
dropped or delayed. Bob has sent his `credential-request` message with `@id:abc123`,
but he's been waiting for a response for AliceCorp for a long time. He now sends
a new message, requesting an ack. The message type is `problem-report` and the 
severity is `WARN`, because Bob is unsure what the slow response means. `~thread.thid`
points back to the message that began the issuance protocol, which was probably
AliceCorp's `credential-offer`. `~thread.myindex` shows that this is the second
message Bob is sending on the thread, not the first--and that Bob has seen only
one message from AliceCorp on the thread, which was the offer to issue. This
should help AliceCorp recognize that it's missed a `credential-request` from Bob,
or if Bob has missed AliceCorp's response instead. Most importantly, this new
message from Bob is decorated with `~please_ack`:

```JSON
{
  "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/notification/1.0/problem-report",
  "@id": "06d474e0-20d3-4cbf-bea6-6ba7e1891240",
  "~thread": {
    "thid": "abc123",
    "pthid": "xyz234",
    "sender_order": 1,
    "received_orders": [{"<key for AliceCorp's issuing agent>": -1}]
  },
  "~please_ack": { "message_id": "abc123" }
}
```

[TODO: How does Bob say that he hasn't seen any response to abc123 on the xyz234 thread,
instead of saying that he hasn't seen any response to abc123 on the abc123 thread?]

If AliceCorp saw Bob's `credential-request` but has simply been slow to respond, then
one possible response is to send Bob a message that says, "Yes, I know you asked for a
credential. I'm working on it." Such an `ack` would look like this:

```JSON
{
  "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/notification/1.0/ack",
  "@id": "a7e174e0-032d-bf4c-a6eb-9126b84006d4",
  "status": "PENDING",
  "~thread": {
    "thid": "abc123",
    "pthid": "xyz234",
    "sender_order": 0,
    "received_orders": [{"<key for Bob's agent>": 0}]
  }
}
```

Notice that `~thread.thid` has changed; the topic is now the missing message, not the
larger interaction.

If, on the other hand, AliceCorp is ready to issue the credential by the time the ack
request arrives, it could respond with a credential. As long as the credential
reply contains `~thread.received_orders: { <key for Bob's agent>: 1 }`, then it is an implicit
ACK because it tells Bob that the ack request was seen, and Bob can discover the status.

If AliceCorp has never seen Bob's `credential-request`, then AliceCorp can reply with
a `problem-report` where the `~thread` object looks like this:

```JSON
{
  "thid": "abc123",
  "received_orders": [{"<key for Bob's agent>": -1}]
}
```
This says, "I'm sorry, Bob. I haven't seen any message from you on a thread with that
`@id`. (The code and comment in the `problem-report` message would probably clarify that
as well, but it is the `-1` in `~thread.received_orders` that tells Bob what he needs to know.)
Bob can now fix the problem by resending his `credential_request`. [TODO: what does the
resend look like? Does it have a `replaces_myindex` property in `~thread` that clarifies
how it is plugging the gap?]

If AliceCorp has already issued the credential to Bob, it can reply with an `ack` that
documents the outcome as far as it is concerned:

```JSON
{
  "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/notification/1.0/ack",
  "@id": "a7e174e0-032d-bf4c-a6eb-9126b84006d4",
  "status": "OK",
  "~thread": {
    "thid": "xyz234",
    "sender_order": 2,
    "received_orders": [{"<key for Bob's agent>": 1}]
  }
}
```

Because `status` is OK, Bob knows that AliceCorp thinks the interaction associated
with his message "abc123", is over. Because `~thread.sender_order` is 2 instead of 1, Bob
knows that this `ack` is the 3rd message in the interaction (credential-offer=0,
credential=1, ack=2). Bob can now ask AliceCorp to resend. [TODO: how is this done?]

# Drawbacks and Alternatives
[drawbacks]: #drawbacks

This mechanism is more complex than what developers might assume
at first glance. Isn't an ACK just a dirt-simple message that says "Your
message is acknowledged"?

It could be. However, if we left it that simple, then we would not have a
standard way to ask for fancier ACK semantics. This would probably not
be fatal to the ecosystem, but it would lead to a proliferation of message
types that all do more or less the same thing. A [pattern would be
ungeneralized](https://codecraft.co/2015/09/02/on-forests-and-trees/),
causing lots of wasted code and documentation and learning time.

# Prior art
[prior-art]: #prior-art

See notes above about the [implicit ACK mechanism in `~thread.lrecs`](#implicit-acks).

# Unresolved questions
[unresolved]: #unresolved-questions

- Security and privacy implications of ACKs. Could they be used to mount
a denial-of-service attack or to sniff info that's undesirable?
