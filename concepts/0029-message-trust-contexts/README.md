# 0029: Message Trust Contexts

## Status
- Status: [PROPOSED](/README.md#rfc-lifecycle)
- Status Date: 2019-05-1
- Status Note: Only implemented in one codebase and in the sample code here.
  Supersedes [Indy HIPE PR #120](https://github.com/hyperledger/indy-hipe/pull/120).

## Summary

Introduces the concept of __Message Trust Contexts__ and describes how they are populated and used.

## Motivation

An important aim of DID Communication is to let parties achieve high trust. Such trust is vital in cases where money changes hands and identity is at stake. However, sometimes lower trust is fine; playing tic-tac-toe ought to be safe through agents, even with a malicious stranger.

We may intuitively understand the differences in these situations, but intuition isn't the best guide when designing a secure ecosystem. Trust is a complex, multidimensional phenomenon. We need a formal way to analyze it, and to test its suitability in particular circumstances.

## Tutorial

_When Alice sends a message to Bob, how much should Bob trust it?_

This is not a binary question, with possible answers of "completely" or "not at all". Rather, it is a nuanced question that should consider many factors. Some clarifying questions might include:

* How much does Bob know about Alice? And what evidence is behind that knowledge?

* Was the confidentiality and integrity of the message protected while it was in transit? If so:

    * How strong is the encryption algorithm?
    * How good are the protections on the keys?
    * Is [perfect forward secrecy](https://en.wikipedia.org/wiki/Forward_secrecy) being used?

* Does Bob have any kind of prior relationship to Alice, such that history increases (or decreases) trust?

* Is the message [repudiable](../0049-repudiation/README.md), or is Alice speaking "on the record"?

* Could Alice use a malformed message to attack Bob (e.g., with buffer overflows, numeric range errors, unexpected fields, and so forth)?

### Message Trust Contexts

The DID Communication ecosystem formalizes the idea of a __Message Trust Context__ (__MTC__) to expose such questions, make their answers explicit, and encourage thoughtful choices based on the answers.

An MTC is an object that holds trust context for a message. This context follows a message throughout its processing journey inside the agent that receives it, and it should be analyzed and updated for decision-making purposes throughout.

Protocols should be designed with standard MTCs in mind. Thus, it is desirable that all implementations share common names for certain concepts, so we can discuss them conveniently in design docs, error messages, logs, and so forth. The standard dimensions of trust tracked in an MTC break down into two groups:

#### Crypto-related
* __Confidentiality__: Could the plaintext content of the message I just received over this channel have been observed by another party?
* __Integrity__: Could the message have been tampered with since it was sent?
* __Authenticated Origin__: Can I know the identity of the original sender with confidence? And if so, on what basis--were multiple factors of auth required to use the keys that encrypted the message? Were biometrics at play?
* __Nonrepudiation__: Can I prove the identity of the sender to a third party? Note that this guarantee may or may not be a desirable quality.
* __PFS__: Is perfect forward secrecy active?
* __Uniqueness__: Can I know that this message is not being sent as part of a replay attack?
* __Limited Scope__: Does the sender identify me in a way that is only meaningful inside a narrow context (e.g., pairwise or nwise relationship), to preserve my privacy? Or did they use a published DID that would correlate me?

#### Input validations
* __Size OK__: Do I know that the message will not overflow internal buffers or persistent storage?
* __Deserialize OK__: Does the plaintext message deserialize into [native object representation](../../features/0044-didcomm-file-and-mime-types/README.md#native-object-representation)?
* __Keys OK__: As a native object, do the keys (property names) and structure match what was expected? In some approaches to deserialization, it may be combined with the previous question--but in languages that produce a loose dictionary from JSON, it is distinct.
* __Values OK__: As a native object, do the values for properties match the datatypes, sizes, and constraints that were expected?

In code, these types of trust are written using whatever naming convention matches the implementer's programming language, so `authenticated_origin` and `authenticatedOrigin` are synonyms of each other and of `Authenticated Origin`.

#### Notation

In protocol designs, the requirements of a message trust context should be declared when message types are defined. For example, the `credential_offer` message in the `credential_issuance` protocol should not be accepted unless it has `Integrity` and `Authenticated Origin` in its MTC (because otherwise a MITM could interfere). The definition of the message type should say this. Its RFC does this by notating:

    mtc: +integrity +authenticated_origin

When a loan is digitally signed, we probably need:

    mtc: +integrity +authenticated_origin +nonrepudiation

The labels for these trust types are long, but they can be shortened if they remain unambiguous. Notice, too, that all of the official MTC fields have unique intial letters. We can therefore abbreviate unambiguously:

    mtc: +i +a +n

Any type of trust that does not appear in MTC notation is assumed to be `undefined` (meaning no claim is made about it either way, perhaps because it hasn't been evaluated or because it doesn't matter). However, sometimes we need to make a lack of trust explicit. We might claim in a protocol definition that a particular type of trust is definitely not required. Or we might want to show that we evaluated a particular trust at runtime, and had a negative outcome. In such cases, we can do this:

    mtc: +i +a -n

Here, we are explicitly denying that `nonrepudiation` is part of the trust context.

For further terseness in our notation, spaces can be omitted:

    mtc: +i+a-n
    
Finally, an mtc that makes no explicit positive or negative claims (undefined) is written as:

    mtc: ?

This MTC notation is a supplement to [SSI Notation](../0006-ssi-notation/README.md) and should be treated as equally normative. Such notation might be useful in log files and error messages, among other things. See [Using a Message Trust Context at Runtime](#using-a-message-trust-context-at-runtime) below.

### Custom Trust

Specific agents may make trust distinctions that are helpful in their own problem domains. For example, some agents may evaluate trust on the physical location or IP address of a sender, or on the time of day that a message arrives. Others may use DIDComm for
internal processes that have unique trust requirements over and above those that matter in interoperable scenarios, such as whether a message emanates from a machine running endpoint compliance software, or whether it has passed through intrusion detection or data loss prevention filters.

Agent implementations are encouraged to add their own trust dimensions to their own implementations of a Message Trust Context, as long as they do not redefine the standard labels. In cases where custom trust types introduce ambiguity with trust labels, MTC notation requires enough letters to disambiguate labels. So if a complex custom MTC has fields named `intrusion_detect_ok`, `ipaddr_ok` (which both start like the standard `integrity`), and `endpoint_compliance` (which has no ambiguity with a standard token) it might be notated as:

    mtc: +c+a+inte+intr+ip-n-p-e

Here, `inte` matches the standard label `integrity`, whereas `intr` and `ip` are known to be custom because they don't match a standard label; `e` is custom but only a single letter because it is unambiguous.

### Populating a Message Trust Context at Runtime

A Message Trust Context comes into being when it arrives on the wire at the receiving agent and begins its processing flow.

The first step may be an input validation to confirm that the message doesn't exceed a max size. If so, the empty MTC is updated with `+s`.

Another early step is decryption. This should allow population of the `confidentiality` and `authenticated_origin` dimensions, at least.

Subsequent layers of code that do additional analysis should update the MTC as appropriate. For example, if a signature is not analyzed and validated until after the decryption step, the signature's presence or absence should cause `nonrepudiation` and maybe `integrity` to be updated. Similarly, once the plaintext of a message is known to be a valid enough to deserialize into an object, the MTC acquires `+deserialize_ok`. Later, when the fields of the message's [native object representation](../../features/0044-didcomm-file-and-mime-types/README.md#native-object-representation) have been analyzed to make sure they conform to a particular structure, it should be updated again with `+key_ok`. And so forth.

### Using a Message Trust Context at Runtime

As message processing happens, the MTC isn't just updated. It should constantly be queried, and decisions should be made on the basis of what the MTC says. These decisions can vary according to the preferences of agent developers and the policies of agent owners. Some agents may choose not to accept any messages that are `-a`, for example, while others may be content to talk with anonymous senders. The recommendations of protocol designers should never be ignored, however; it is probably wrong to accept a `-n` message that signs a loan, even if agent policy is lax about other things. Formally declared MTCs in a protocol design may be linked to security proofs...

Part of the intention with the terse MTC notation is that conversations about agent trust should be easy
and interoperable. When agents send one another [`problem-report` messages](../../features/0035-report-problem/README.md),
they can turn MTCs into human-friendly text, but also use this notation: "Unable to accept a payment from message that
lacks Integrity guarantees (-i)." This notation can help diagnose trust problems in logs. It may also be helpful with
[message tracing](../../features/0034-message-tracing/README.md), 
[feature discovery](../../features/0031-discover-features/README.md), and agent testing.

## Reference

A complete reference implementation of MTCs in python is attached to this RFC (see [mtc.py](mtc.py)).
It could easily be extended with custom trust dimensions, and it would be simple to port to other
programming languages. Note that the implementation includes unit tests written in pytest style,
and has only been tested on python 3.x.