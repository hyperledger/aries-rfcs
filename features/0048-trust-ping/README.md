# 0048: Trust Ping Protocol 1.0
- Authors: Daniel Hardman <daniel.hardman@gmail.com>
- Start Date: 2018-12-11

## Status
- Status: [ACCEPTED](/README.md#rfc-lifecycle)
- Status Date: 2019-02-01
- Status Note: Numerous implementations.
  This supersedes [Indy HIPE 0032](https://github.com/hyperledger/indy-hipe/tree/master/text/0032-trust-ping).

## Summary

Describe a standard way for agents to test connectivity,
responsiveness, and security of a pairwise channel.

## Motivation

Agents are distributed. They are not guaranteed to be
connected or running all the time. They support a
variety of transports, speak a variety of protocols,
and run software from many different vendors.

This can make it very difficult to prove that two
agents have a functional pairwise channel. Troubleshooting
connectivity, responsivenes, and security is vital.

## Tutorial

This protocol is analogous to the familiar `ping`
command in networking--but because it operates
over agent-to-agent channels, it is transport
agnostic and asynchronous, and it can produce insights
into privacy and security that a regular ping
cannot.

### Roles

There are two parties in a trust ping: the `sender`
and the `receiver`. The sender initiates the trust
ping. The receiver responds. If the receiver wants
to do a ping of their own, they can, but this is a
new interaction in which they become the sender.

### Messages

The trust ping interaction begins when `sender`
creates a `ping` message like this:

```JSON
{
  "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/trust_ping/1.0/ping",
  "@id": "518be002-de8e-456e-b3d5-8fe472477a86",
  "~timing": {
    "out_time": "2018-12-15 04:29:23Z",
    "expires_time": "2018-12-15 05:29:23Z",
    "delay_milli": 0
  },
  "comment": "Hi. Are you listening?",
  "response_requested": true
}
```

Only `@type` and `@id` are required; `~timing.out_time`, `~timing.expires_time`, and `~timing.delay_milli`
are optional [message timing decorators](
../0032-message-timing/README.md), and `comment`
follows the conventions of [localizable message fields](
../0043-l10n/README.md). If present, it may
be used to display a human-friendly description of the ping to a user
that gives approval to respond. (Whether an agent responds to a trust
ping is a decision for each agent owner to make, per policy and/or
interaction with their agent.)

The `response_requested` field deserves special mention. The normal
expectation of a trust ping is that it elicits a response. However, it
may be desirable to do a unilateral trust ping at times--communicate
information without any expecation of a reaction. In this case,
`"response_requested": false` may be used. This might be useful, for
example, to defeat correlation between request and response (to generate
noise). Or agents A and B might agree that periodically A will ping B
without a response, as a way of evidencing that A is up and functional.
If `response_requested` is false, then the receiver MUST NOT respond.

When the message arrives at the receiver, assuming that `response_requested`
is not `false`, the receiver should reply as quickly as possible with a
`ping_response` message that looks like this:

```JSON
{
  "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/trust_ping/1.0/ping_response",
  "@id": "e002518b-456e-b3d5-de8e-7a86fe472847",
  "@thread": { "thid": "518be002-de8e-456e-b3d5-8fe472477a86" },
  "~timing": { "in_time": "2018-12-15 04:29:28Z", "out_time": "2018-12-15 04:31:00Z"},
  "comment": "Hi yourself. I'm here."
}
```

Here, `@type` and `~thread` are required, and the rest is optional.

### Trust

This is the "**trust** ping protocol", not just the "ping protocol."
The "trust" in its name comes from several features that the interaction
gains by virtue of its use of standard agent-to-agent conventions:

1. Messages should be associated with a [__message trust context__](
../../concepts/0029-message-trust-contexts/README.md)
that allows sender and receiver to evaluate how much trust can be placed
in the channel. For example, both sender and receiver can check whether
messages are encrypted with suitable algorithms and keys.

2. Messages may be targeted at any known agent in the other party's sovereign
domain, using [cross-domain routing conventions](
https://github.com/hyperledger/indy-hipe/blob/master/text/0022-cross-domain-messaging/README.md),
and may be encrypted and
packaged to expose exactly and only the information desired, at each hop
along the way. This allows two parties to evaluate the completeness of
a channel and the alignment of all agents that maintain it.

3. This interaction may be traced using the general [message tracing
mechanism](../0034-message-tracing/README.md).
