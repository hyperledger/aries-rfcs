# Aries RFC 0317: Please ACK Decorator

- Authors: [Daniel Hardman](daniel.hardman@gmail.com), [Timo Glastra](mailto:timo@animo.id)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2019-12-26
- Status Note: Separated from the ACK protocol. A lot of complex features were removed for inclusion in AIP 2.0 (see note at bottom)
- Start Date: 2018-12-26
- Tags: [feature](/tags.md#feature), [decorator](/tags.md#decorator)

## Summary

Explains how one party can request an acknowledgment to and clarify the status of processes.

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

### Requesting an ack (`~please_ack`)

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
../../concepts/0011-decorators/README.md). An example of the decorator looks like this:

``` json
{
  "~please_ack": {
    "on": "RECEIPT"
  }
}
```

This says, "Please send me an ack as soon as you receive this message."

### Examples

Suppose AliceCorp and Bob are involved in credential issuance. Alice is an issuer;
Bob wants to hold the issued credential.

#### On Receipt

In the final required message of the `issue-credential` protocol, AliceCorp sends
the credential to Bob. But AliceCorp wants to know for sure that Bob has received it,
for its own accounting purposes. So it decorates the final message with an ack
request:

```json
{
  "~please_ack": {
    "on": "RECEIPT"
  }
}
```

Bob honors this request and returns an `ack` as soon as he receives it and stores its payload.

#### On Outcome

Same as with the previous example, AliceCorp an acknowledgement from Bob. However, in contrast to the previous example that just requests an acknowledgement on receipt of message, this time AliceCorp wants to know for sure Bob acknowledges the contents of the credential. To do this AliceCorp decorates the `issue-credential` message with an ack request for the `OUTCOME`.

```json
{
  "~please_ack": {
    "on": "OUTCOME"
  }
}
```

Bob honors this request and returns an `ack` as soon as he has verified the contents of the issued credential.
## Reference

### `~please_ack` decorator

#### __`on`__

The only field for the please ack decorator. Required. Describes the circumstances under which an ack is desired. Possible values include `RECEIPT` and `OUTCOME`.

- `RECEIPT` - Request that an ack is sent on receipt of the message. This way of requesting an ack is to verify whether the other agent successfully received the message
- `OUTCOME` - Request that an ack is sent on outcome of the message. This way of requesting an ack is to verify whether the other agent acknowledges the outcome of the received message.

## Drawbacks

None specified.
## Rationale and alternatives

The first version of this RFC was a lot more advanced, but also introduced a lot of complexities. A lot of complex features have been removed so it could be included in AIP 2.0 in a simpler form. More advanced features [from the initial RFC](https://github.com/hyperledger/aries-rfcs/blob/2e6007b224f6888aec79b20bbddea3c4d533042a/features/0317-please-ack/README.md) can be added back in when needed.

## Prior art

None specified.

## Unresolved questions

- Security and privacy implications of `~please_ack` decorators. Could they be used to mount a denial-of-service attack or to sniff info that's undesirable?
- Signed (Non-repudiable) acks. How do you ask for an ACK that commits its sender to the acknowledgment in a way that's provable to third parties?
- Multiplexed acks. How do you ask for, and supply, an ACK to all of Alice's agents instead of just to the one who sent the ACK? Does each agent need to request the ACK separately? Are there denial-of-service or other security issues?

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

Name / Link | Implementation Notes
--- | ---
 | 
