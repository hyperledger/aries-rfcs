# Aries RFC 0113: Question Answer Protocol 0.9

- Authors: Douglas Wightman <douglas.wightman@evernym.com>
- Status: [DEMONSTRATED](/README.md#demonstrated)
- Since: 2019-07-05
- Start Date: 2019-02-07
- Tags: feature, protocol

# Summary

A simple protocol where a questioner asks a responder a question with at least one valid answer.  The responder then replies with an answer or ignores the question.

    Note: While there is a need in the future for a robust negotiation protocol
    this is not it. This is for simple question/answer exchanges.

# Motivation

There are many instances where one party needs an answer to a specific question from another party. These can be related to consent, proof of identity, authentication, or choosing from a list of options. For example, when receiving a phone call a customer service representative can ask a question to the customer’s phone to authenticate the caller, “Are you on the phone with our representative?”. The same could be done to authorize transactions, validate logins (2FA), accept terms and conditions, and any other simple, non-negotiable exchanges.

# Tutorial

We'll describe this protocol in terms of a [Challenge/Response] https://en.wikipedia.org/wiki/Challenge%E2%80%93response_authentication) scenario where a customer service representative for Faber Bank questions its customer Alice, who is speaking with them on the phone, to answer whether it is really her.

### Interaction

Using an already established pairwise connection and agent-to-agent communication Faber will send a question to Alice with one or more valid responses with an optional deadline and Alice can select one of the valid responses or ignore the question. If she selects one of the valid responses she will respond with her answer.


### Roles

There are two parties in a typical question/answer interaction. The first party (Questioner) issues the question with its valid answers and the second party (Responder) responds with the selected answer. The parties must have already exchanged pairwise keys and created a connection. These pairwise can be used to encrypt and verify the response. When the answer has been sent questioner can know with a high level of certainty that it was sent by responder.

In this tutorial Faber (the questioner) initiates the interaction and creates and sends the question to Alice. The question includes the valid responses, which can optionally be signed for non-repudiability.

In this tutorial Alice (the responder) receives the packet and must respond to the question (or ignore it, which is not an answer) by encrypting either the positive or the negative response_code (signing both is invalid).

### Messages

All messages in this protocol are part of the "Question/Answer 1.0" message family uniquely identified by this DID reference:

    did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/questionanswer/1.0

The protocol begins when the questioner sends a `questionanswer` message to the responder:

```JSON
{
  "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/questionanswer/1.0/question",
  "@id": "518be002-de8e-456e-b3d5-8fe472477a86",
  "question_text": "Alice, are you on the phone with Bob from Faber Bank right now?",
  "question_detail": "This is optional fine-print giving context to the question and its various answers.",
  "nonce": "<valid_nonce>",
  "signature_required": true,
  "valid_responses" : [
    {"text": "Yes, it's me"},
    {"text": "No, that's not me!"}],
  "~timing": {
    "expires_time": "2018-12-13T17:29:06+0000"
  }
}
```

The responder receives this message and chooses the answer. If the signature is required then she uses her private pairwise key to sign  her response.

    Note: Alice should sign the following: the question, the chosen answer,
    and the nonce: HASH(<question_text>+<answer_text>+<nonce>), this keeps a
    record of each part of the transaction.

The response message is then sent using the ~sig message decorator:

```JSON
{
  "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/questionanswer/1.0/answer",
  "~thread": { "thid": "518be002-de8e-456e-b3d5-8fe472477a86", "seqnum": 0 },
  "response": "Yes, it's me",
  "response~sig": {
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/signature/1.0/ed25519Sha512_single"
    "signature": "<digital signature function output>",
    "sig_data": "<base64(HASH("Alice, are you on the phone with Bob?"+"Yes, it's me"+"<nonce>"))>",
    "signers": ["<responder_key>"],
    }
  "~timing": {
    "out_time": "2018-12-13T17:29:34+0000"
  }
}
```

The questioner then checks the signature against the sig_data.

### Optional Elements

The "question_detail" field is optional. It can be used to give "fine print"-like context around the question and all of its valid responses. While this could always be displayed, some UIs may choose to only make it available on-demand, in a "More info..." kind of way.

~timing.expires_time is optional
\~response~sig is optional when "signature_required" is false

### Business cases and auditing

In the above scenario, Faber bank can audit the reply and prove that only Alice's pairwise key signed the response  (a cryptographic API like Indy-SDK can be used to guarantee the responder's signature). Conversely, Alice can also use her key to prove or dispute the validity of the signature. The cryptographic guarantees central to agent-to-agent communication and digital signatures create a trustworthy protocol for obtaining a committed answer from a pairwise connection. This  protocol can be used for approving wire transfers, accepting EULAs, or even selecting an item from a food menu. Of course,  as with a real world signature, Alice should be careful about what she signs.

### Invalid replies

The responder may send an invalid, incomplete, or unsigned response. In this case the questioner must decide what to do. As with normal verbal communication, if the response is not understood the question can be asked again, maybe with increased emphasis. Or the questioner may determine the lack of a valid response is a response in and of itself. This depends on the parties involved and the question being asked. For example, in the exchange above, if the question times out or the answer is not "Yes, it's me" then Faber would probably choose to discontinue the phone call.

### Trust and Constraints

Using already established pairwise relationships allows each side to trust each other. The responder can know who sent the message and the questioner knows that only the responder could have encrypted the response. This response gives a high level of trust to the exchange.

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

Name | Link | Implementation Notes
--- | --- | ---
Connect.Me | https://www.evernym.com/blog/connect-me-sovrin-digital-wallet/ | Free mobile app from Evernym. Installed via app store on iOS and Android. 
Verity | https://www.evernym.com/products/ | Commercially licensed enterprise agent, SaaS or on-prem.
