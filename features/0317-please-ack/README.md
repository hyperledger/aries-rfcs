# Aries RFC 0317: Please ACK Decorator

- Authors: [Daniel Hardman](daniel.hardman@gmail.com)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2019-12-26
- Status Note: Separated from the ACK protocol 
- Supersedes: [0015-ACKs](https://github.com/hyperledger/aries-rfcs/tree/527849ec3aa2a8fd47a7bb6c57f918ff8bcb5e8c/features/0015-acks)
- Start Date: 2018-12-26
- Tags: [feature](/tags.md#feature), [decorator](/tags.md#decorator)

## Summary

Explains how one party can request an acknowledgment
to and clarify the status of complex processes.

## Motivation

An __acknowledgment__ or __ACK__ is one of the most common procedures in protocols
of all types. The ACK message is defined in Aries RFC [0015-acks](../0015-acks/README.md) and is adopted into other protocols for use at explicit points in the execution of a protocol. In addition to receiving ACKs at predefined places in a protocol, agents also need the ability to request additional ACKs at other points in an instance of a protocol. Such requests may or may not be answered by the other party, hence the "please" in the name of decorator.

## Tutorial

If you are not familiar with the [tutorial section of the ACK message](../0015-acks/README.md#tutorial),please review that first.

Agents interact in very complex ways. They may use multiple transport mechanisms,
across varied protocols, through long stretches of time. While we usually expect
messages to arrive as sent, and to be processed as expected, a vital tool in the
agent communication repertoire is the ability to request and receive
acknowledgments to confirm a shared understanding.

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
like this: 

``` jsonc
"~please_ack": {}
```

This says, "Please send me an ack as soon as you receive this message."

#### Advanced Features (experimental)

<blockquote>
(The features in this section are part of the 1.0 spec, but are not required to
be implemented to achieve 1.0 compliance. We describe them to show what may
be possible in the future.)
</blockquote>

A fancier version of `~please_ack` might look like this:

``` jsonc
{
  "~please_ack": {
    "message_id": "b271c889-a306-4737-81e6-6b2f2f8062ae",
    "on": [
      "RECEIPT",
      "6h",
      "OUTCOME"
    ]
  }
}
```

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

``` jsonc
{
  "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/notification/1.0/ack",
  "@id": "06d474e0-20d3-4cbf-bea6-6ba7e1891240",
  "status": "PENDING",
  "deny": ["6h"],
  "~thread": {
    "thid": "b271c889-a306-4737-81e6-6b2f2f8062ae",
    "myindex": 4,
    "lrecs": {"2fQvCXfgvxz4dtBDDwcj2PJdG5qDrEsrQVjvWRhg9uhd": 3}
  }
}
```

Here, `deny` tells the recipient that, although the `receipt` request in the
previous `~please_ack.on` was honored, and the `outcome` request will probably be
honored as well, the recipient cannot expect an ack every 6 hours. (The sender may
still send acks at their discretion; the denial just says that this behavior can't
be counted on.)

## Reference

### `~please_ack` decorator

#### __`message_id`__

Asks for an acknowledgment of a message other than the one
that's decorated. Usually omitted, since most requests for an
ACK happen in the same message that wants acknowledgment.

#### __`on`__

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

``` jsonc
"on": ["evaluating-all-offers", "OUTCOME"]
```

The order of items in the `on` array is not significant, and any unrecognized
values in it should be ignored.

### Examples

Suppose AliceCorp and Bob are involved in credential issuance. Alice is an issuer;
Bob wants to hold the issued credential.

#### Happy Path

In the final required message of the `issue-credential` protocol, AliceCorp sends
the credential to Bob. But AliceCorp wants to know for sure that Bob has received it,
for its own accounting purposes. So it decorates the final message with an ack
request:

```JSON
"~please_ack: {}"
```

Bob honors this request and returns an `ack` as soon as he receives it and stores its
payload. The interesting field is `status`, which look like this: `"status": "OK"` (or,
if the `issue-credential` protocol defines a final state for the holder called
`now-holding`, Bob could be more explicit and send '"status": "now-holding"'.

#### Delayed Issuance

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

``` jsonc
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

``` jsonc
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

``` jsonc
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

``` jsonc
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

## Drawbacks and Alternatives

This mechanism is more complex than what developers might assume
at first glance. Isn't it enough for the ~please_ack to be just the simple version?

It could be. However, if we left it that simple, then we would not have a
standard way to ask for fancier ACK semantics. This would probably not
be fatal to the ecosystem, but it would lead to a proliferation of message
types that all do more or less the same thing. A [pattern would be
ungeneralized](https://codecraft.co/2015/09/02/on-forests-and-trees/),
causing lots of wasted code and documentation and learning time.

## Prior art

None specified.

## Unresolved questions

- Security and privacy implications of `~please_ack` decorators. Could they be used to mount
a denial-of-service attack or to sniff info that's undesirable?
- Signed (Non-repudiable) acks. How do you ask for an ACK that commits its sender to the acknowledgment in a way that's provable to third parties?
- Multiplexed acks. How do you ask for, and supply, an ACK to all of Alice's agents instead of just to the one who sent the ACK? Does each agent need to request the ACK separately? Are there denial-of-service or other security issues?

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

Name / Link | Implementation Notes
--- | ---
 | 
