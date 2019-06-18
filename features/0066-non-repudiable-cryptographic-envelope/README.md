# 0066: Non-Repudiable Signature for Cryptographic Envelope
- Author: Kyle Den Hartog (indy@kyledenhartog.com)
- Start Date: 04/15/2019

## Status
- Status: [PROPOSED](/README.md#rfc-lifecycle)
- Status Date: 04/15/2019
- Status Note: This is a second attempt to integrate non-repudiable digital signatures based on learnings and discussions over the past few months. This focuses only on the signing of entire messages. Signature Decorators will be handled seperately.

## Summary

This HIPE is intended to highlight the ways that a non-repudiable signature could be added to a message field or message family through the use of [JSON Web Signatures](https://tools.ietf.org/html/rfc7515) format.

## Motivation

Non-repudiable digital signatures serve as a beneficial method to provide proof of provenance of a message. There's many use cases where non-repudiable signatures are necessary and provide value. Some examples may be for a bank to keep on record when a mortgage is being signed. Some of the early use cases where this is going to be of value is going to be in the connection initiate protocol and the ephemeral challenge protocol. The expected outcome of this RFC is to define a method for using non-repudiable digital signatures in the cryptographic envelope layer of DID Communications.

## Tutorial

### JSON Web Signatures

The JSON Web Signatures specification is written to define how to *represent content secured with digital signatures or Message Authentication Codes (MACs) using JavaScript Object Notation (JSON) based data structures.*

Our particular interest is in the use of non-repudiable digital signature using the ed25519 curve with edDSA signatures to sign invitation messages as well as sign full content layer messages.

### When should non-repudiable signatures be used?

As highlighted in the repudiation RFC #0049, non-repudiable signatures are not always necessary and *SHOULD NOT* be used by default. The primary instances where a non-repudiable digital signature should be used is when a signer expects and considers it acceptable that a receiver can prove the sender sent the message.

> If Alice is entering into a borrower:lender relationship with Carol, Carol needs to prove to third parties that Alice, and only Alice, incurred the legal obligation.

A good rule of thumb for a developer to decide when to use a non-repudiable signature is: 

> "Does the Receiver need to be able to prove who created the message to another person?"

In most cases, the answer to this is likely no. The few cases where it does make sense is when a message is establishing some burden of legal liability.

## Reference

Provide guidance for implementers, procedures to inform testing,
interface definitions, formal function prototypes, error codes,
diagrams, and other technical details that might be looked up.
Strive to guarantee that:

- Interactions with other features are clear.
- Implementation trajectory is well defined.
- Corner cases are dissected by example.

* Provide JWS structure format using predefined signature formats at the beginning (Curve25519 w/ edDSA)
* Show examples of Format of JWS we'll support

At a high level, the usage of a digital signature should occur before a message is encrypted. There's some cases where this may not make sense. This RFC will highlight a few different examples of how non-repudiable digital signatures could be used.

### Connect protocol example
Starting with an initial `connections/1.0/invitation` message like this:

```json
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/connections/1.0/invitation",
    "@id": "12345678900987654321",
    "label": "Alice",
    "recipientKeys": ["8HH5gYEeNc3z7PYXmd54d4x6qAfCNrqQqEB3nS7Zfu7K"],
    "serviceEndpoint": "https://example.com/endpoint",
    "routingKeys": ["8HH5gYEeNc3z7PYXmd54d4x6qAfCNrqQqEB3nS7Zfu7K"]
}
```

We would then bas64URL encode this message like this:

```
eyJAdHlwZSI6ImRpZDpzb3Y6QnpDYnNOWWhNcmpIaXFaRFRVQVNIZztzcGVjL2Nvbm5lY3Rpb25zLzEuMC9pbnZpdGF0aW9uIiwiQGlkIjoiMTIzNDU2Nzg5MDA5ODc2NTQzMjEiLCJsYWJlbCI6IkFsaWNlIiwicmVjaXBpZW50S2V5cyI6WyI4SEg1Z1lFZU5jM3o3UFlYbWQ1NGQ0eDZxQWZDTnJxUXFFQjNuUzdaZnU3SyJdLCJzZXJ2aWNlRW5kcG9pbnQiOiJodHRwczovL2V4YW1wbGUuY29tL2VuZHBvaW50Iiwicm91dGluZ0tleXMiOlsiOEhINWdZRWVOYzN6N1BZWG1kNTRkNHg2cUFmQ05ycVFxRUIzblM3WmZ1N0siXX0=
```

This base64URL encoded string would then become the payload in the JWS.

Using the compact serialization format, our JOSE Header would look like this:

```json
{
    "alg":"EdDSA",
    "kid":"FYmoFw55GeQH7SRFa37dkx1d2dZ3zUF8ckg7wmL7ofN4"
}
```

`alg`: specifies the signature algorithm used
`kid`: specifies the key identifier. In the case of DIDComm, this will be a base58 encoded ed25519 key.

To sign, we would combine the JOSE Header with the payload and separate it using a period. This would be the resulting data that would be signed:

```
ewogICAgImFsZyI6IkVkRFNBIiwKICAgICJraWQiOiJGWW1vRnc1NUdlUUg3U1JGYTM3ZGt4MWQyZFozelVGOGNrZzd3bUw3b2ZONCIKfQ==.eyJAdHlwZSI6ImRpZDpzb3Y6QnpDYnNOWWhNcmpIaXFaRFRVQVNIZztzcGVjL2Nvbm5lY3Rpb25zLzEuMC9pbnZpdGF0aW9uIiwiQGlkIjoiMTIzNDU2Nzg5MDA5ODc2NTQzMjEiLCJsYWJlbCI6IkFsaWNlIiwicmVjaXBpZW50S2V5cyI6WyI4SEg1Z1lFZU5jM3o3UFlYbWQ1NGQ0eDZxQWZDTnJxUXFFQjNuUzdaZnU3SyJdLCJzZXJ2aWNlRW5kcG9pbnQiOiJodHRwczovL2V4YW1wbGUuY29tL2VuZHBvaW50Iiwicm91dGluZ0tleXMiOlsiOEhINWdZRWVOYzN6N1BZWG1kNTRkNHg2cUFmQ05ycVFxRUIzblM3WmZ1N0siXX0=
```

and the resulting signature would be:

```
cwKY4Qhz0IFG9rGqNjcR-6K1NJqgyoGhso28ZGYkOPNI3C8rO6lmjwYstY0Fa2ew8jaFB-jWQN55kOTL5oHVDQ==
```

The final output would then produce this:

```
ewogICAgImFsZyI6IkVkRFNBIiwKICAgICJraWQiOiJGWW1vRnc1NUdlUUg3U1JGYTM3ZGt4MWQyZFozelVGOGNrZzd3bUw3b2ZONCIKfQ==.eyJAdHlwZSI6ImRpZDpzb3Y6QnpDYnNOWWhNcmpIaXFaRFRVQVNIZztzcGVjL2Nvbm5lY3Rpb25zLzEuMC9pbnZpdGF0aW9uIiwiQGlkIjoiMTIzNDU2Nzg5MDA5ODc2NTQzMjEiLCJsYWJlbCI6IkFsaWNlIiwicmVjaXBpZW50S2V5cyI6WyI4SEg1Z1lFZU5jM3o3UFlYbWQ1NGQ0eDZxQWZDTnJxUXFFQjNuUzdaZnU3SyJdLCJzZXJ2aWNlRW5kcG9pbnQiOiJodHRwczovL2V4YW1wbGUuY29tL2VuZHBvaW50Iiwicm91dGluZ0tleXMiOlsiOEhINWdZRWVOYzN6N1BZWG1kNTRkNHg2cUFmQ05ycVFxRUIzblM3WmZ1N0siXX0=.cwKY4Qhz0IFG9rGqNjcR-6K1NJqgyoGhso28ZGYkOPNI3C8rO6lmjwYstY0Fa2ew8jaFB-jWQN55kOTL5oHVDQ==
```

### Basic Message protocol example


#### Sign and encrypt process

Next is an example that showcases what a basic message would look like. Since this message would utilize a connection to encrypt the message, we will produce a JWS first, and then encrypt the outputted compact JWS.

We would first encode our JOSE Header which looks like this:

```json
{
    "alg": "edDSA", 
    "kid": "7XVZJUuKtfYeN1W4Dq2Tw2ameG6gC1amxL7xZSsZxQCK"
}
```

and when base64url encoded it would be converted to this:

```
eyJhbGciOiAiZWREU0EiLCAia2lkIjogIjdYVlpKVXVLdGZZZU4xVzREcTJUdzJhbWVHNmdDMWFteEw3eFpTc1p4UUNLIn0=
```

Next we'll take our content layer message which as an example is the JSON provided:

```json
{
    "@id": "123456780",
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/basicmessage/1.0/message",
    "~l10n": { "locale": "en" },
    "sent_time": "2019-01-15 18:42:01Z",
    "content": "Your hovercraft is full of eels."
}
```

and now we'll base64url encode this message which results in this output:

```
eyJjb250ZW50IjogIllvdXIgaG92ZXJjcmFmdCBpcyBmdWxsIG9mIGVlbHMuIiwgInNlbnRfdGltZSI6ICIyMDE5LTAxLTE1IDE4OjQyOjAxWiIsICJAdHlwZSI6ICJkaWQ6c292OkJ6Q2JzTlloTXJqSGlxWkRUVUFTSGc7c3BlYy9iYXNpY21lc3NhZ2UvMS4wL21lc3NhZ2UiLCAiQGlkIjogIjEyMzQ1Njc4MCIsICJ-bDEwbiI6IHsibG9jYWxlIjogImVuIn19
```

Next, they should be concatenated using a period (.) as a delimiter character which would produce this output:

```
eyJhbGciOiAiZWREU0EiLCAia2lkIjogIjdYVlpKVXVLdGZZZU4xVzREcTJUdzJhbWVHNmdDMWFteEw3eFpTc1p4UUNLIn0=.eyJjb250ZW50IjogIllvdXIgaG92ZXJjcmFmdCBpcyBmdWxsIG9mIGVlbHMuIiwgInNlbnRfdGltZSI6ICIyMDE5LTAxLTE1IDE4OjQyOjAxWiIsICJAdHlwZSI6ICJkaWQ6c292OkJ6Q2JzTlloTXJqSGlxWkRUVUFTSGc7c3BlYy9iYXNpY21lc3NhZ2UvMS4wL21lc3NhZ2UiLCAiQGlkIjogIjEyMzQ1Njc4MCIsICJ-bDEwbiI6IHsibG9jYWxlIjogImVuIn19
```

The signature for the signature data is:

```
FV7Yyz7i31EKoqS_cycQRr2pN59Q5Ojoxnr7uf6yZBqylnUZW2jCk_LesgWy5ZEux2K6dkrZh7q9pUs9dEsJBQ==
```

The signature should be concatenated to the signed data above resulting in this final string:

```
eyJhbGciOiAiZWREU0EiLCAia2lkIjogIjdYVlpKVXVLdGZZZU4xVzREcTJUdzJhbWVHNmdDMWFteEw3eFpTc1p4UUNLIn0=.eyJjb250ZW50IjogIllvdXIgaG92ZXJjcmFmdCBpcyBmdWxsIG9mIGVlbHMuIiwgInNlbnRfdGltZSI6ICIyMDE5LTAxLTE1IDE4OjQyOjAxWiIsICJAdHlwZSI6ICJkaWQ6c292OkJ6Q2JzTlloTXJqSGlxWkRUVUFTSGc7c3BlYy9iYXNpY21lc3NhZ2UvMS4wL21lc3NhZ2UiLCAiQGlkIjogIjEyMzQ1Njc4MCIsICJ-bDEwbiI6IHsibG9jYWxlIjogImVuIn19.FV7Yyz7i31EKoqS_cycQRr2pN59Q5Ojoxnr7uf6yZBqylnUZW2jCk_LesgWy5ZEux2K6dkrZh7q9pUs9dEsJBQ==
```

The last step is to encrypt this base64URL encoded string as the message in pack which will complete the cryptographic envelope.

The output of this message then becomes:

```
{"protected":"eyJlbmMiOiJ4Y2hhY2hhMjBwb2x5MTMwNV9pZXRmIiwidHlwIjoiSldNLzEuMCIsImFsZyI6IkF1dGhjcnlwdCIsInJlY2lwaWVudHMiOlt7ImVuY3J5cHRlZF9rZXkiOiJac2dYVWdNVGowUk9lbFBTT09lRGxtaE9sbngwMkVVYjZCbml4QjBESGtEZFRLaGc3ZlE1Tk1zcjU3bzA5WDZxIiwiaGVhZGVyIjp7ImtpZCI6IjRXenZOWjJjQUt6TXM4Nmo2S1c5WGZjMmhLdTNoaFd4V1RydkRNbWFSTEFiIiwiaXYiOiJsOWJHVnlyUnRseUNMX244UmNEakJVb1I3eU5sdEZqMCIsInNlbmRlciI6Imh4alZMRWpXcmY0RFplUGFsRGJnYzVfNmFMN2ltOGs1WElQWnBqTURlUzZaUS1jcEFUaGNzNVdiT25uaVFBM2Z0ZnlYWDJkVUc0dVZ3WHhOTHdMTXRqV3lxNkNKeDdUWEdBQW9ZY0RMMW1aaTJxd2xZMGlDQ2N0dHdNVT0ifX1dfQ==","iv":"puCgKCfsOb5gRG81","ciphertext":"EpHaC0ZMXQakM4n8Fxbedq_3UhiJHq6vd_I4NNz3N7aDbq7-0F6OXi--VaR7xoTqAyJjrOTYmy1SqivSkGmKaCcpFwC9Shdo_vcMFzIxu90_m3MG1xKNsvDmQBFnD0qgjPPXxmxTlmmYLSdA3JaHpEx1K9gYgGqv4X5bgWZqzFCoevyOlD5a2bDZBY5Mn__IT1pVzjbMbDeSgM2nOztWyF0baXwrqczBW-Msx-uP5HNlLdz02FPbMnRP6MYyw6q0wI0EqwzzwH81bZzHKrTVHT2-M_aIEQp9lKGLhnSW3-aIOpSzonGOriyDukfTpvsCUZEd_X1u0G3iZKxYCbIKaj_ARLbb6idlRngVGW9LYYaw7Xay83exp22gflvLmmN25Xzo1vLlaDaFr9h-J_QAvFebCHgWjl1kcodBRc2jhoMVSpEXJHoI5qMrlVvh45PLTEjxy7y5FHQ1L8klwWZN5EIwui3ExIOA8RwYDlp8-HLib_uqB7hNzVUYC0iPd1KTiNIcidYVdAoPpdtLDOh-KCmPB9RkjVUqSlwNYUAAnfY8OJXuBLHP2nWiYUDA6VDbvrv4npW88VMdsFDk_QzvDRvg7gkW8x8jNd8=","tag":"B4UilbBNSUr3QcALtVxTEw=="}
```

### Decrypt and Verify process

To Decrypt and verify the JWS first unpack the message, which provides this result:

```json
{
    "message":"eyJhbGciOiAiZWREU0EiLCAia2lkIjogIjdYVlpKVXVLdGZZZU4xVzREcTJUdzJhbWVHNmdDMWFteEw3eFpTc1p4UUNLIn0=.eyJjb250ZW50IjogIllvdXIgaG92ZXJjcmFmdCBpcyBmdWxsIG9mIGVlbHMuIiwgInNlbnRfdGltZSI6ICIyMDE5LTAxLTE1IDE4OjQyOjAxWiIsICJAdHlwZSI6ICJkaWQ6c292OkJ6Q2JzTlloTXJqSGlxWkRUVUFTSGc7c3BlYy9iYXNpY21lc3NhZ2UvMS4wL21lc3NhZ2UiLCAiQGlkIjogIjEyMzQ1Njc4MCIsICJ-bDEwbiI6IHsibG9jYWxlIjogImVuIn19.FV7Yyz7i31EKoqS_cycQRr2pN59Q5Ojoxnr7uf6yZBqylnUZW2jCk_LesgWy5ZEux2K6dkrZh7q9pUs9dEsJBQ==",
    "recipient_verkey":"4WzvNZ2cAKzMs86j6KW9Xfc2hKu3hhWxWTrvDMmaRLAb",
    "sender_verkey":"7XVZJUuKtfYeN1W4Dq2Tw2ameG6gC1amxL7xZSsZxQCK"
}
```

Parse the `message` field splitting on the second period `.` You should then have this as the payload:

```
eyJhbGciOiAiZWREU0EiLCAia2lkIjogIjdYVlpKVXVLdGZZZU4xVzREcTJUdzJhbWVHNmdDMWFteEw3eFpTc1p4UUNLIn0=.eyJjb250ZW50IjogIllvdXIgaG92ZXJjcmFmdCBpcyBmdWxsIG9mIGVlbHMuIiwgInNlbnRfdGltZSI6ICIyMDE5LTAxLTE1IDE4OjQyOjAxWiIsICJAdHlwZSI6ICJkaWQ6c292OkJ6Q2JzTlloTXJqSGlxWkRUVUFTSGc7c3BlYy9iYXNpY21lc3NhZ2UvMS4wL21lc3NhZ2UiLCAiQGlkIjogIjEyMzQ1Njc4MCIsICJ-bDEwbiI6IHsibG9jYWxlIjogImVuIn19
```

and the signature will be base64URL encoded and look like this:

```
FV7Yyz7i31EKoqS_cycQRr2pN59Q5Ojoxnr7uf6yZBqylnUZW2jCk_LesgWy5ZEux2K6dkrZh7q9pUs9dEsJBQ==
```

Now decode the signature and then convert the signature  and payload to bytes and use `crypto.crypto_verify()` API in IndySDK

Your message has now been verified.

To get the original message, you'll again parse the JWS this time taking the second section only which looks like this:

```
eyJjb250ZW50IjogIllvdXIgaG92ZXJjcmFmdCBpcyBmdWxsIG9mIGVlbHMuIiwgInNlbnRfdGltZSI6ICIyMDE5LTAxLTE1IDE4OjQyOjAxWiIsICJAdHlwZSI6ICJkaWQ6c292OkJ6Q2JzTlloTXJqSGlxWkRUVUFTSGc7c3BlYy9iYXNpY21lc3NhZ2UvMS4wL21lc3NhZ2UiLCAiQGlkIjogIjEyMzQ1Njc4MCIsICJ-bDEwbiI6IHsibG9jYWxlIjogImVuIn19
```

Now Base64URL decode that section and you'll get the original message:

```json
{
    "content": "Your hovercraft is full of eels.",
    "sent_time": "2019-01-15 18:42:01Z",
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/basicmessage/1.0/message",
    "@id": "123456780",
    "~l10n": {"locale": "en"}
}
```

### Modifications to pack()/unpack() API

 - Things to consider:
     - Combining this all into the pack/unpack API would require two additional APIs. One to handle signing, and one to indicate a message isn't encrypted.
     - I like the idea of combining the API. However, I'm not a fan of the idea of incorporating a plaintext message into pack to support the connect protocol. 
     - My preference would be to create a seperate API specifically for the connect protocol given that it's an edge case.
     - How would this affect the ephemeral challenge protocol as well as the "spectrum of trust" which was highlight by One of Daniel Hardman's previous posts? 

## Drawbacks

Through the choice of a JWS formatted structure we imply that an off the shelf library will support this structure. However, it's uncommon for libraries to support the edDSA signature algorithm even though it's a valid algorithm based on the [IANA registry](https://www.iana.org/assignments/jose/jose.xhtml). This means that most implementations that support this will either need to add this signature algorithm to another JWS library or 

## Rationale and alternatives

- Why is this design the best in the space of possible designs?
    - Given the support for ed25519 keys throughout the ecosystem, this seemed like the best fit for initial support. Over time, it may make sense to add additional support for other key types like Secp256k1 or RSA.
    - The rational for supporting JWS is that it contains the bare minimum information to deterministically verify the payload (given JSON doesn't need to be ordered, but a signature must have the same byte order) and self contain the key and algorithm used.
    - The compact serialization was chosen instead of the JSON serialization because it's assumed that senders will not be multi-signing messages at this time.
- What other designs have been considered and what is the rationale for not choosing them?
    - CBOR supports a signature scheme called CBOR Web Signatures, but was not chosen because the DIDComm protocol is largely JSON based.
    - JWTs were not chosen because they are a constrained form of JWS. This allows us to add JWT support if needed in the future, while not limiting ourselves early in the design process.
- What is the impact of not doing this?
    - By not using JWTs we move away from a common dependency that many other SSI ecosystems support already for their credentials. However, many JWT libraries do not support ed25519 which is currently the only key type used.

## Prior art

The majority of prior art discussions are mentioned above in the rationale and alternatives section. Some prior art that was considered when selecting this system is how closely it aligns with OpenID Connect systems. This has the possibility to converge with Self Issued OpenID Connect systems when running over HTTP, but doesn't specifically constrain to an particular transport mechanism. This is a distinct advantage for backward compatibility.


## Unresolved questions

- Was the usage of a JWT a better option for broader SSI adoption and backwards compatibility (e.g. Active directory and OpenID Connect)?
- Is limiting to only ed25519 key types an unnecessary restraint given the broad support needed for DIDComm?
- 