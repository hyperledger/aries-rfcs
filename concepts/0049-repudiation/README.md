# 0049: Repudiation
- Daniel Hardman <daniel.hardman@gmail.com>
- Start Date: 2018-03-01 (backdated)

## Status
- Status: [ACCEPTED](/README.md#rfc-lifecycle)
- Status Date: 2019-03-01
- Status Note: Well understood and baked into various protocol
  designs and DIDComm processes--but not yet ratified by the larger
  Aries community. This supersedes [Indy HIPE 0037](
  https://github.com/hyperledger/indy-hipe/tree/master/text/0037-repudiation).

## Summary
[summary]: #summary

Explain DID Communication's perspective on repudiation,
and how this influences the DIDComm approach to digital signatures.

## Motivation
[motivation]: #motivation

A very common mistake among newcomers to cryptography is to
assume that digital signatures are the best way to prove the
origin of data. While it is true that digital signatures can
be used in this way, over-signing creates a digital exhaust
that can lead to serious long-term privacy problems. We _do_ use
digital signatures, but we want to be very deliberate about
when and why--and by default, we want to use a more limited
technique called __authenticated encryption__. This doc
explains the distinction and its implications.

## Tutorial
[tutorial]: #tutorial

If Carol receives a message that purports to come from Alice, she may naturally ask:

>Do I know that this really came from Alice?

This is a fair question, and an important one. There are two ways to
answer it:

* Alice can send in a way that's __repudiable__
* Alice can send in a way that's __non-repudiable__

Both of these approaches can answer Carol's question, but they differ
  in _who can trust the answer_. If Carol knows Alice is the sender,
 but can't prove it to anybody else, then we say the
 message is publicly _repudiable_; if Carol can prove the origin
 to others, then we say the message is _non-repudiable_.

The repudiable variant is accomplished with a technique called
__authenticated encryption__.

The non-repudiable variant is accomplished with digital signatures.

#### How Authenticated Encryption Works

Repudiable sending may sound mysterious, but it's actually quite simple.
 Alice and Carol can negotiate a shared secret and trust one another not to
 leak it. Thereafter, if Alice sends Carol a message that uses the shared
 secret (e.g., it's encrypted by a negotiated symmetric
 encryption key), then Carol knows the sender must be Alice. However,
 she can't prove it to anyone, because Alice's immediate counter-response
 could be, "Carol could have encrypted this herself. She knows the key, too."
 Notice that this only works in a pairwise channel.

#### Signatures

Non-repudiable messages are typically accomplished with digital
 signatures. With signatures, everyone can examine a signature to verify
 its provenance.

Fancy signature schemes such as ring signatures may represent intermediate
 positions, where the fact that a signature was provided by a member of
 a group is known--but not which specific member did the signing.

#### Why and When To Use Each Strategy

A common mistake is to assume that digital signatures should be used
everywhere because they give the most guarantees. This is a misunderstanding
of who needs which guarantees under which conditions.

__If Alice tells a secret to Carol, who should decide whether the secret
is reshared--Alice, or Carol?__

[![photo by Wassim Loumi, CC SA 2.0, Flickr](whisper-secret.jpg)](https://www.flickr.com/photos/sophotow/16559284088)

__In an SSI paradigm, the proper, desirable default is that a sender of
secrets should retain the ability to decide if their secrets are shareable,
not give that guarantee away.__

If Alice sends a repudiable message, she gets a guarantee that Carol
can't reshare it in a way that damages Alice. On the other hand, if
she sends a message that's digitally signed, she has no control over
where Carol shares the secret and proves its provenance. Hopefully Carol has Alice's
best interests at heart, and has good judgment and solid cybersecurity...

There are certainly cases where non-repudiation is appropriate. If
 Alice is entering into a borrower:lender relationship with Carol,
 Carol needs to prove to third parties that Alice, and only Alice,
 incurred the legal obligation.

DIDComm supports both modes of communication. However, properly modeled
 interactions tend to favor repudiable messages; non-repudiation must be
 a deliberate choice. For this reason, we assume repudiable until
 an explicit signature is required (in which case the `sign()` crypto
 primitive is invoked). This matches the physical world, where most
 communication is casual and does not carry the weight of legal
 accountability--and should not.

#### Unknown Recipients

Imagine that Alice wants to broadcast a message. She doesn't know who will receive
it, so she can't use authenticated encryption. Yet she wants anyone who receives
it to know that it truly comes from her.

In this situation, digital signatures are required. Note, however, that Alice
is trading some privacy for her ability to publicly prove message origin.

## Reference
[reference]: #reference

Authenticated encryption is not something we invented. It is well described
in the [documentation for libsodium](
https://libsodium.gitbook.io/doc/public-key_cryptography/authenticated_encryption).
It is implemented there, and also in the pure javascript port, [TweetNacl](
https://tweetnacl.js.org/#/). 

## Drawbacks
[drawbacks]: #drawbacks

The main reason not to emphasize authenticated encryption over digital signatures
is that we seem to encounter a steady impedance from people who are signature-oriented.
It is hard and time-consuming to reset expectations. However, we have concluded that
the gains in privacy are worth the effort.
