# Aries RFC 0015: ACKs

- Authors: [Daniel Hardman](daniel.hardman@gmail.com)
- Status: [ACCEPTED](/README.md#accepted)
- Since: 2021-04-15
- Status Note: Broadly implemented, adopted into many protocols and part of [AIP 1 and 2](../../concepts/0302-aries-interop-profile/README.md).
- Start Date: 2018-12-26
- Tags: [feature](/tags.md#feature)

## Summary

Explains how one party can send acknowledgment
messages (ACKs) to confirm receipt and clarify the status of complex processes.

## Change log

- Mar 22, 2022: Clarification that an Ack `Fail` must not be used, and that a [Report Problem](../0035-report-problem/README.md) must be used in its place. Remove Ack `Fail` from the RFC.

- Mar 25, 2020: In the ~thread decorator section of the sample in the [Explicit ACKs section](#explicit-acks), 'myindex' was changed to 'sender_order' and 'lrecs' to 'received_orders'. This is in accordance with the field names as defined in [RFC 0008](https://github.com/hyperledger/aries-rfcs/tree/64e5e55c123b2efaf38f4b0911a71a1c40a7f29d/concepts/0008-message-id-and-threading#threaded-messages).

## Motivation

An __acknowledgment__ or __ACK__ is one of the most common procedures in protocols
of all types. We need a flexible, powerful, and easy way to send such
messages in agent-to-agent interactions.

## Tutorial

Confirming a shared understanding matters whenever independent parties interact.
We buy something on Amazon; moments later, our email client chimes to tell us of
a new message with subject "Thank you for your recent order." We verbally accept
a new job, but don't rest easy until we've also emailed the signed offer letter
back to our new boss. We change a password on an online account, and get a text
at our recovery phone number so both parties know the change truly originated
with the account's owner.

When formal acknowledgments are missing, we get nervous. And rightfully so; most
of us have a story of a package that was lost in the mail, or a web form
that didn't submit the way we expected.

Agents interact in very complex ways. They may use multiple transport mechanisms,
across varied protocols, through long stretches of time. While we usually expect
messages to arrive as sent, and to be processed as expected, a vital tool in the
agent communication repertoire is the receipt of acknowledgments to confirm a
shared understanding.

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

``` jsonc
{
  "@type": "https://didcomm.org/notification/1.0/ack",
  "@id": "06d474e0-20d3-4cbf-bea6-6ba7e1891240",
  "status": "OK",
  "~thread": {
    "thid": "b271c889-a306-4737-81e6-6b2f2f8062ae",
    "sender_order": 4,
    "received_orders": {"did:sov:abcxyz": 3}
  }
}
```

It may also be appropriate to send an ack at other key points in an interaction
(e.g., when a key rotation notice is received).

### Adopting acks

As discussed in [0003: Protocols](../../concepts/0003-protocols/README.md), a protocol can [adopt the ack message into
its own namespace](../../0000-template-protocol.md#adopted-messages).
This allows the type of an ack to change from:
    `https://didcomm.org/notification/1.0/ack`
to something like:
    `https://didcomm.org/otherProtocol/2.0/ack`.
Thus, message routing
logic can see the ack as part of the other protocol, and send it to the relevant
handler--but still have all the standardization of generic acks.

### ack status

The `status` field in an ack tells whether the ack is final or not with respect
to the message being acknowledged. It has 2 predefined values: `OK` (which means
an outcome has occurred, and it was positive); and `PENDING`, which acknowledges
that no outcome is yet known.

There is not an ack `status` of `FAIL`. In the case of a protocol failure a
[Report Problem](../0035-report-problem/README.md) message must be used to
inform the other party(ies). For more details, see the [next
section](#relationship-to-problem-report).

In addition, more advanced ack usage is possible. See the [details in the
Reference section](#reference).

### Relationship to `problem-report`

Negative outcomes do not necessarily mean that something bad happened; perhaps
Alice comes to hope that Bob rejects her offer to buy his house because she's
found something better--and Bob does that, without any error occurring. This
is not a FAIL in a problem sense; it's a FAIL in the sense that the offer to
buy did not lead to the outcome Alice intended when she sent it.

This raises the question of errors. Any time an unexpected *problem*
arises, best practice is to report it to the sender of the message that
triggered the problem. This is the subject of the [problem reporting mechanism](../0035-report-problem/README.md).

A `problem_report` is inherently a sort of ACK. In fact, the `ack` message type
and the `problem_report` message type are both members of the same
`notification` message family. Both help a sender learn about status. Therefore,
a requirement for an `ack` is that a status of `FAIL` be satisfied by a
`problem_report` message.

However, there is some subtlety in the use of the two types of messages.
Some `ack`s may be sent before a final outcome, so a final `problem_report`
may not be enough. As well, an ack request may be sent after a previous
`ack` or `problem_report` was lost in transit. Because of these caveats, developers
whose code creates or consumes acks should be thoughtful about where the two message
types overlap, and where they do not. Carelessness here is likely to cause subtle,
hard-to-duplicate surprises from time to time.

### Custom ACKs

This mechanism cannot address all possible ACK use cases. Some ACKs may
require custom data to be sent, and some acknowledgment schemes may be more
sophisticated or fine-grained that the simple settings offered here.
In such cases, developers should write their own ACK message type(s) and
maybe their own decorators. However, reusing the field names and conventions
in this RFC may still be desirable, if there is significant overlap in the
concepts.

## Reference

### `ack` message

#### __`status`__

Required, values `OK` or `PENDING`. As discussed [above](#ack-status), this tells whether the ack is final
or not with respect to the message being acknowledged.

#### __`~thread.thid`__

Required. This links the `ack` back to the message that requested it.

All other fields in an `ack` are present or absent per requirements of ordinary
messages.

## Drawbacks and Alternatives

None identified.

## Prior art

See notes above about the [implicit ACK mechanism in `~thread.received_orders`](#implicit-acks).

## Unresolved questions

- Muliplexed acks. How do you supply an ACK to all of Alice's agents instead of just to the one who involved in the current protocol?

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

Name / Link | Implementation Notes
--- | ---
[RFC 0036: Issue Credential Protocol](../0036-issue-credential/README.md) | ACKs are [adopted](../../0000-template-protocol.md#adopted-messages) by this protocol.
[RFC 0037: Present Proof Protocol](../0037-present-proof/README.md) | ACKs are [adopted](../../0000-template-protocol.md#adopted-messages) by this protocol.
[RFC 0193: Coin Flip Protocol](../0193-coin-flip/README.md) | ACKs are [adopted](../../0000-template-protocol.md#adopted-messages) as a subprotocol.
[Aries Cloud Agent - Python](https://github.com/hyperledger/aries-cloudagent-python) | Contributed by the Government of British Columbia.
