# Aries RFC 0193: Coin Flip Protocol 1.0 

- Authors: [Daniel Hardman](daniel.hardman@gmail.com)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2019-08-19
- Status Note: recently proposed  
- Start Date: 2019-08-19
- Tags: [feature](/tags.md#feature), [protocol](/tags.md#protocol)

## Summary

Specifies a safe way for two parties who are remote from one another and who do not trust one another to pick a random, binary outcome that neither can manipulate.

## Motivation

To guarantee fairness, it is often important to pick one party in a protocol to make a choice about what to do next. We need a way to do this that more or less mirrors the randomness of flipping a coin.

## Tutorial

### Name and Version

This defines the `coinflip` protocol, version 1.x, as identified by the
following [PIURI](https://github.com/hyperledger/aries-rfcs/blob/master/concepts/0003-protocols/uris.md#piuri):

    https://github.com/hyperledger/aries-rfcs/features/0193-coin-flip/1.0
    
### Roles

There are 2 roles in the protocol: __Recorder__ and __Caller__. These role names parallel the roles in a physical coin flip: the _Recorder_ performs a process that freezes/records the state of a flipped coin, and the _Caller_ announces the state that they predict, before the state is known. If the caller predicts the state correctly, then the caller chooses what happens next; otherwise, the recorder chooses.

### Algorithm

Before describing the messages, let's review the algorithm that will be used. This algorithm is not new; it is a simple commitment scheme [described on wikipedia](https://en.wikipedia.org/wiki/Coin_flipping#Telecommunications) and implemented in various places. The RFC merely formalizes the algorithm for DIDComm.

1. Caller chooses a random [UUID](https://tools.ietf.org/html/rfc4122) and sends it to Recorder using the [`propose` message described below](#propose). A [version 4 UUID](https://tools.ietf.org/html/rfc4122#section-4.4) is recommended, though any UUID version should be accepted. Note that the UUID is represented in lower case, with hyphens, and without enclosing curly braces. Suppose this value is `01bf7abd-aa80-4389-bf8c-dba0f250bb1b`.

2. Recorder chooses a cooresponding random UUID -- say, `d96dfb58-60ba-4fcd-9ca0-a2be41181d6f`.

3. Recorder captures an outcome for an imaginary coin flip -- either the string `heads` or the string `tails`. Suppose Recorder captures `tails`. 

4. Recorder builds a __flip string__. This is single-space-separated concatenation of 3 inputs: `recorder-captured-state recorder-uuid caller-uuid`. Given the random numbers and tails state in our example, this string would be `tails d96dfb58-60ba-4fcd-9ca0-a2be41181d6f 01bf7abd-aa80-4389-bf8c-dba0f250bb1b`. Recorder then computes a SHA256 hash of the flip string, which is `B78DC2D94F6E92B69491F13DC8C866C0A31F896069D3DD69472D0D7740967011` for our example, and sends it to Caller using the [`flip` message described below](#flip). This hash commits Recorder to all inputs, without revealing Recorder's UUID, and it is the Recorder's way of posing to the Caller the question, "heads or tails?"

5. Caller announces their committed choice -- for instance, "heads", using the ['call' message described below](#call). This commits Caller to a particular prediction about the state of the virtual coin.

6. Recorder uses a ['reveal' message](#reveal) to reveal _flip string_. Both parties discover who won the coin flip. If Caller predicted the state correctly, the state at the beginning of _flip string_ will match the Caller's choice in step 6, and Caller wins. Otherwise, Recorder wins. Neither party is able to manipulate the outcome. This is guaranteed by both parties checking to see that their UUIDs appear in the correct position in _flip string_, and that _flip string_ does indeed hash to the value computed in step 4.

### States

The algorithm and the corresponding states are pictured in the following diagram:

![diagram](coin-flip.png)

<blockquote>
Note: This diagram was made in draw.io. To make changes:

- upload the drawing HTML from this folder to the [draw.io](https://draw.io) site (Import From... Device), 
- make changes,
- export the picture as PNG and HTML to your local copy of this repo, and
- submit a pull request.
</blockquote>

This diagram only depicts the so-called "happy path". It is possible to experience problems for various reasons. If either party detects such an event, they should abandon the protocol and emit a [`problem-report` message](../0035-report-problem/README.md) to the other party. The `problem-report` message is [adopted into this protocol](../../concepts/0003-protocols/template.md#adopted-messages) for that purpose. Some values of `code` that may be used in such messages include:

* `bad-message-sequence`: The message was sent out of order.
* `bad-field-value`: The message contained a field with an invalid value. The offending fields are named in the `problem_items` array. 

## Reference

### Messages

#### `propose`

The protocol begins when Caller sends to Recorder a `propose` message that embodies Step 1 in the [algorithm above](#algorithm). It looks like this:

```jsonc
{
  "@type": "https://github.com/hyperledger/aries-rfcs/features/0193-coin-flip/1.0/propose",
  "@id": "518be002-de8e-456e-b3d5-8fe472477a86",
  "caller-uuid": "d96dfb58-60ba-4fcd-9ca0-a2be41181d6f",
  "comment": "Let's flip to see who goes first.",
  "choice-id": "did:sov:SLfEi9esrjzybysFxQZbfq;spec/tictactoe/1.0/who-goes-first",
  "caller-wins": "did:example:abc123",  // Meaning of value defined in superprotocol
  "recorder-wins": "did:example:xyz456", // Meaning of value defined in superprotocol
  // Optional; connects to superprotocol
  "~thread": { 
    "pthid": "a2be4118-4f60-bacd-c9a0-dfb581d6fd96" 
  }
}
```

The `@type` and `@id` fields are standard for DIDComm. The `caller-uuid` field conveys the data required by Step 1 of the algorithm. The optional `comment` field follows [localization conventions](../0043-l10n/README.md) and is irrelevant unless the coin flip intends to invite human participation. The `~thread.pthid` [decorator](../../concepts/0011-decorators/README.md) is optional but should be common; it [identifies the thread of the parent interaction](../../concepts/0008-message-id-and-threading/README.md#threaded-messages) (the [superprotocol](../../concepts/0003-protocols/README.md#composable)).

The `choice-id` field formally names a choice that a superprotocol has defined, and tells how the string values of the `caller-wins` and `recorder-wins` fields will be interpreted. In the example above, the choice is defined in the [Tic-Tac-Toe Protocol](../../concepts/0003-protocols/tictactoe/README.md#key-concepts), which also specifies that `caller-wins` and `recorder-wins` will contain DIDs of the parties playing the game. Some other combinations that might make sense include:

* In an auction protocol that uses a coin flip to break a tie between two bids of equal value, `choice-id` might be a string like `prefix/myauctionproto/1.0/bid-tie-break`, and the values of the `*-wins` fields might be the `id` properties of specific bid messages.

* In a protocol that models an American football game, the `choice-id` might be a string like `prefix/amfootball/1.0/who-kicks-off`, and the values of the `*-wins` fields might be the strings "home" and "visitor".

* In a protocol that models radioactive halflife, the decay of a particular neutron might use `choice-id` of `prefix/halflife/1.0/should-decay`, and the `*-wins` fields might be the strings "yes" and "no".

The [`~timing.expires_time` decorator](../0032-message-timing/README.md#tutorial) may be used to impose a time limit on the processing of this message. If used, the protocol must restart if the subsequent `flip` message is not received by this time limit.

#### `flip`

This message is sent from Recorder to Caller. It embodies Step 2-5 of [the algorithm](#algorithm). It looks like this:

```jsonc
{
  "@type": "https://github.com/hyperledger/aries-rfcs/features/0193-coin-flip/1.0/flip",
  "@id": "7a86e002-8dee-b3d5-456e-8fe47247518b",
  "commitment": "B78DC2D94F6E92B69491F13DC8C866C0A31F896069D3DD69472D0D7740967011",
  "comment": "Here you go. Do you pick heads or tails?",
  "~thread": { 
    "thid": "518be002-de8e-456e-b3d5-8fe472477a86",
    "sender_order": 0
  }
}
```

Note the use of `~thread.thid` to connect this `flip` to the preceding `propose`. As before, `comment` is optional and only relevant for cases that involve human interaction.

The [`~timing.expires_time` decorator](../0032-message-timing/README.md#tutorial) may be used to impose a time limit on the processing of this message. If used, the protocol must restart if the subsequent `call` message is not received by this time limit.

#### `call`

This message is sent from Caller to Recorder, and embodies Step 6 of [the algorithm](#algorithm). It looks like this:

```jsonc
{
  "@type": "https://github.com/hyperledger/aries-rfcs/features/0193-coin-flip/1.0/call",
  "@id": "1173fe5f-86c9-47d7-911b-b8eac7d5f2ad",
  "called": "tails",
  "comment": "I pick tails.",
  "~thread": { 
    "thid": "518be002-de8e-456e-b3d5-8fe472477a86",
    "sender_order": 1 
  }
}
```

Note the use of `~thread.thid` and `sender_order: 1` to connect this `call` to the preceding `flip`.

The [`~timing.expires_time` decorator](../0032-message-timing/README.md#tutorial) may be used to impose a time limit on the processing of this message. If used, the protocol must restart if the subsequent `reveal` message is not received by this time limit.

#### `reveal`

This message is sent from Recorder to Caller, and embodies Step 7 of [the algorithm](#algorithm). It looks like this:

```jsonc
{
  "@type": "https://github.com/hyperledger/aries-rfcs/features/0193-coin-flip/1.0/reveal",
  "@id": "e2a9454d-783d-4663-874e-29ad10776115",
  "flip_string": "tails d96dfb58-60ba-4fcd-9ca0-a2be41181d6f 01bf7abd-aa80-4389-bf8c-dba0f250bb1b",
  "winner": "caller",
  "comment": "You win.",
  "~please_ack": {},
  "~thread": { 
    "thid": "518be002-de8e-456e-b3d5-8fe472477a86",
    "sender_order": 1 
  }
}
```

Note the use of `~thread.thid` and `sender_order: 1` to connect this `reveal` to the preceding `call`.

The Caller should validate this message as follows:

* Confirm that `flip_string` is a correctly formatted string consisting of 3 fields with no leading or trailing spaces, having exactly 1 space delimiter between each field, where the first field is the case-sensitive value "heads" or "tails", and the other two fields are correctly formatted UUIDs. This check is important because it eliminates the possibility that the Recorder could introduce variation to the commitment.
* Confirm that the third field in `flip_string` equals `caller-uuid` from the `propose` message.
* Confirm that `flip_string_hash` from the preceding `flip` equals the SHA256 hash of `flip_string`.

Having validated the message thus far, Caller determines the winner by checking to see if the value of the first field in `flip_string` equals the value of `called` from the preceding `call` message. If yes, then the value of the `winner` field must be `caller`; if no, then it must be `recorder`. The `winner` field must be present in the message, and its value must be correct, for the `reveal` message to be deemed fully valid. This confirms that both parties understand the outcome, and it prevents a Recorder from asserting a false outcome that is accepted by careless validation logic on the Caller side.

The [`~please_ack` decorator](../0317-please-ack/README.md) is optional. If a superprotocol specifies the next step after a Coin Flip with sufficient precision, it may be unnecessary. However, it should be supported by implementations. The resulting `ack` message, if sent, is hereby [adopted into the Coin Flip protocol](../0015-acks/README.md#adopting-acks).

The [`~timing.expires_time` decorator](../0032-message-timing/README.md#tutorial) may be used to impose a time limit on the processing of this message. If used, the protocol must restart if the subsequent `ack` or the next message in the superprotocol is not received before the time limit.

## Drawbacks

The protocol is a bit chatty.

## Rationale and alternatives

It may be desirable to pick among more than 2 alternatives. A separate protocol needs to be designed for that. 

## Prior art

As mentioned in the introduction, the algorithm used in this protocol is a simple and well known form of cryptographic commitment, and is documented on Wikipedia. It is not new to this RFC.

## Unresolved questions

- Do we need to use hashlink so we can move to a new hash algorithm if SHA256 is ever broken?
   
## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

Name / Link | Implementation Notes
--- | ---
 |  | 

