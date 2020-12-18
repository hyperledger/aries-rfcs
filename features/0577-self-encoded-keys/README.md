# Aries RFC 0577: Use self-encoded keys

- Authors: [George Aristy](mailto:george.aristy@securekey.com) (SecureKey)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2020-12-18
- Status Note: N/A
- Supersedes: [RFC0360](../0360-use-did-key/README.md)
- Start Date: 2020-12-09
- Tags: [feature](/tags.md#feature)

## Summary

A simple, lightweight format for a sender to encode cryptographic keys is introduced that unambiguously conveys the components required for their use: the key's curve, the key's value, and the associated algorithm. Further changes to RFCs with "naked" keys are proposed to disambiguate their purpose.

## Scope

This format is intended to replace the existing usage of `did:key` identifiers in certain Aries RFC protocols until a different or evolved solution is proposed that relies on standards and meets the community's requirements.

## Background

The Hyperledger Aries community standards for encoding of cryptographic keys between a sending a receiving party has gone through two iterations.

### First iteration

The Hyperledger Aries community has historically used only two key types for different purposes in the standard protocols: [Ed25519](https://ed25519.cr.yp.to/ed25519-20110926.pdf) for signatures and [Curve25519](https://cr.yp.to/ecdh/curve25519-20060209.pdf) for key exchange using the [Diffie-Hellman method](https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.364.5157). These are still the only key types employed by most if not all Hyperledger Aries implementations.

Due to the [birational equivalence](https://eprint.iacr.org/2007/286.pdf) between curves `Ed25519` and `Curve25519`, as well as a general desire to simplify key management, Aries protocol designers and implementers chose a convention whereby the sender transmits the `Ed25519` key only. The receiver assumes this key's purpose as the sender's verification key, and would convert it to the corresponding `Curve25519` key for key exchange with the sender. The `Ed25519` key's bytes were encoded in [Base58](https://en.bitcoinwiki.org/wiki/Base58) format by the sender before transmission.

The above conventions were captured in [RFC160-connection-protocol](https://github.com/hyperledger/aries-rfcs/blob/master/features/0160-connection-protocol/README.md) and [RFC0019-encryption-envelop](https://github.com/hyperledger/aries-rfcs/blob/master/features/0019-encryption-envelope/README.md).

### Second iteration

There was a growing awareness of the drawbacks to the convention implemented in the previous iteration. In particular, there was no support for other types of keys (see [cryptographic agility](https://en.wikipedia.org/wiki/Crypto-agility)), and the sender's purpose for them was not explicit.

[RFC0360-use-did-key](https://github.com/hyperledger/aries-rfcs/blob/master/features/0360-use-did-key/README.md) proposed the usage of the [`did:key`](https://w3c-ccg.github.io/did-method-key/) [DID method](https://www.w3.org/TR/did-core/) as a way of encoding cryptographic keys in a way that communicates the key's curve, value, and the sender's purpose for the key.

We pause here to note that the `did:key` method relies on the [Multibase Data Format](https://tools.ietf.org/html/draft-multiformats-multibase) draft that is on the standards track and that the codecs are registered [here](https://github.com/multiformats/multicodec/blob/master/table.csv). We also note that RFC0360 recommends the use of DID identifiers - not URLs - as the encoding format of the keys. It is this convention that allows the transmission of both an `Ed25519` key and its equivalent `Curve25519` key in a single DID URI.

Aries [RFC0023-did-exchange](https://github.com/hyperledger/aries-rfcs/blob/master/features/0023-did-exchange/README.md), [RFC0434-outofband](https://github.com/hyperledger/aries-rfcs/blob/master/features/0434-outofband/README.md) and [RFC0017-attachments](https://github.com/hyperledger/aries-rfcs/blob/master/concepts/0017-attachments/README.md) were updated to use `did:key` URIs following the proposal of RFC0360.

To date, no known Hyperledger Aries implementations are using keys other than `ED25519` and `Curve25519` for [DIDComm](https://github.com/hyperledger/aries-rfcs/blob/master/concepts/0005-didcomm/README.md).

## Motivation

While `did:key` URIs encode cryptographic keys with sufficient metadata to discern their type, and in a way that conveys their purpose, there are some downsides to this approach.

### Over-extended Key Purpose

The `did:key` method does not provide a way to constrain the sender's purpose for the key. Consider the following DID document that is the result of resolving the DID `did:key:z6MkpTHR8VNsBxYAAWHut2Geadd9jSwuBV8xRoAnwWsdvktH`:

```json=
{
  "@context": "https://w3id.org/did/v1",
  "id": "did:key:z6MkpTHR8VNsBxYAAWHut2Geadd9jSwuBV8xRoAnwWsdvktH",
  "publicKey": [{
    "id": "did:key:z6MkpTHR8VNsBxYAAWHut2Geadd9jSwuBV8xRoAnwWsdvktH#z6MkpTHR8VNsBxYAAWHut2Geadd9jSwuBV8xRoAnwWsdvktH",
    "type": "Ed25519VerificationKey2018",
    "controller": "did:key:z6MkpTHR8VNsBxYAAWHut2Geadd9jSwuBV8xRoAnwWsdvktH",
    "publicKeyBase58": "B12NYF8RrR3h41TDCTJojY59usg3mbtbjnFs7Eud1Y6u"
  }],
  "authentication": [ "did:key:z6MkpTHR8VNsBxYAAWHut2Geadd9jSwuBV8xRoAnwWsdvktH#z6MkpTHR8VNsBxYAAWHut2Geadd9jSwuBV8xRoAnwWsdvktH" ],
  "assertionMethod": [ "did:key:z6MkpTHR8VNsBxYAAWHut2Geadd9jSwuBV8xRoAnwWsdvktH#z6MkpTHR8VNsBxYAAWHut2Geadd9jSwuBV8xRoAnwWsdvktH" ],
  "capabilityDelegation": [ "did:key:z6MkpTHR8VNsBxYAAWHut2Geadd9jSwuBV8xRoAnwWsdvktH#z6MkpTHR8VNsBxYAAWHut2Geadd9jSwuBV8xRoAnwWsdvktH" ],
  "capabilityInvocation": [ "did:key:z6MkpTHR8VNsBxYAAWHut2Geadd9jSwuBV8xRoAnwWsdvktH#z6MkpTHR8VNsBxYAAWHut2Geadd9jSwuBV8xRoAnwWsdvktH" ],
  "keyAgreement": [{
    "id": "did:key:z6MkpTHR8VNsBxYAAWHut2Geadd9jSwuBV8xRoAnwWsdvktH#zBzoR5sqFgi6q3iFia8JPNfENCpi7RNSTKF7XNXX96SBY4",
    "type": "X25519KeyAgreementKey2019",
    "controller": "did:key:z6MkpTHR8VNsBxYAAWHut2Geadd9jSwuBV8xRoAnwWsdvktH",
    "publicKeyBase58": "JhNWeSVLMYccCk7iopQW4guaSJTojqpMEELgSLhKwRr"
  }]
}
```

This DID document is asserting that the Ed25519 key is to be used for authentication, assertion (when signing verifiable credentials), capability delegation and invocation. This is a much broader use than required for the standard Aries protocols.

There exists a proposal for a query parameter or fragment that the sender may attach to the DID URI - converting it to a DID URL instead - but those have yet to formally materialize. The mechanism in theory could be used to "patch" the resolved DID document to constrain its scope. If materialized, adoption of this mechanism would require more sophisticated processing of the `did:key` identifier than what is currently proposed.

### Attenuated Cryptographic Agility

A more flexible configuration is desired that allows dissociated types of keys for the different purposes. For example, it should be possible for an agent to use Ed25519 keys for authentication and P-256 for key agreement. Note that there is no cryptographic equivalence between RSA keys and P-256. `did:key` does not appear to support this level of flexibility within a single DID document.

## New DIDComm Format for Encoding Bare Keys

We make use of existing building blocks to enable an easier transition from the second iteration's format:

* Reuse identifiers registered in the IANA's JOSE registry to identify the key's associated algorithm
    * We also provide [additional algorithims](#additional-algorithms) in the registry for those have yet to be registered in the JOSE registry but that have useful properties desired by the community.
* Reuse the multibase/multicodec mechanism underlying the `did:key` method

### Syntax

The syntax for the new encoding format is:

```
algorithm_name|multibase(base58btc, multicodec(key_code, key_bytes))
```

* `algorithm_name`: the name of an algorithm registered in the [IANA's JOSE registry](https://www.iana.org/assignments/jose/jose.xhtml) **or** in the registry defined in this RFC below.
* `|`: the vertical pipe character (ASCII `7C`)
* `multibase`: the [multibase function](https://github.com/multiformats/multibase/blob/master/README.md) (see also [The Multibase Data Format](https://tools.ietf.org/html/draft-multiformats-multibase)). Use of the multibase function offers the flexibility to choose a different binary-to-text encoding scheme if required in the future.
* `base58btc`: the multibase identifier for the bitcoin binary-to-text encoding scheme (see [BitCoin Wiki](https://en.bitcoinwiki.org/wiki/Base58) and [The Base58 Encoding Scheme](https://tools.ietf.org/html/draft-msporny-base58)). We choose to fix this multibase parameter to ease the transition from the existing `did:key` format that also uses this fixed parameter for the multibase function. Note that additional multibase formats are registered [here](https://github.com/multiformats/multibase/blob/master/multibase.csv).
* `multicodec`: the [multicodec function](https://github.com/multiformats/multicodec/blob/master/README.md) (see also [Additional Multiformat Codec Registrations](https://tools.ietf.org/html/draft-snell-multicodec)). The multicodec function concatenates the the key_type and key_bytes.
* `key_code`: the multicodec code assigned to the key's type as defined [here](https://github.com/multiformats/multicodec/blob/master/table.csv). Examples: `ed25519-pub=>0xed`, `x25519-pub=>0xec`, `p256-pub=>0x1200`, `p384-pub=>0x1201`.
* `key_bytes`: the key's value converted to an octet-string

> **TODO:** clarify rules for conversion of keys to octet strings

## Additional Algorithms

Algorithm Name|Algorithm Description|Algorithm Usage Location(s)|DIDComm Implementation Requirements|Change Controller|Reference
--------------|---------------------|---------------------------|---------------------------------------|-----------------|---------
ECDH-1PU+A256KW|Authcrypt|alg|Recommended+|Aries Community|[Public Key Authenticated Encryption for JOSE: ECDH-1PU](https://tools.ietf.org/html/draft-madden-jose-ecdh-1pu)
Authcrypt|Legacy Authcrypt|alg|Optional|Aries Community|[RFC0019](https://github.com/hyperledger/aries-rfcs/blob/master/features/0019-encryption-envelope/README.md)
Anoncrypt|Legacy Anoncrypt|alg|Optional|Aries Community|[RFC0019](https://github.com/hyperledger/aries-rfcs/blob/master/features/0019-encryption-envelope/README.md)

### Examples

**Ed25519 (EdDSA):**

The algorithm for usage of Ed25519 keys identified in [RFC8037](https://tools.ietf.org/html/rfc8037#section-3.1) and registered in the JOSE registry is `EdDSA`.

The multicodec identifier for Ed25519 public keys is `ed25519-pub` therefore its code is `0xed`.

An example output from a function implementing the [syntax](#syntax) would be: `EdDSA|z6MkpTHR8VNsBxYAAWHut2Geadd9jSwuBV8xRoAnwWsdvktH`.

**Ed25519 (Authcrypt):**

The algorithm for usage of Ed25519 keys identified in RFC0019 for authenticated encryption is `Authcrypt`.

The multicodec identifier for Ed25519 public keys is `ed25519-pub` therefore its code is `0xed`.

An example output from a function implementing the [syntax](#syntax) would be: `Authcrypt|z6MkpTHR8VNsBxYAAWHut2Geadd9jSwuBV8xRoAnwWsdvktH`.

**X25519:**

Several algorithms are identified for use with X25519 keys as described in [RFC7518](https://tools.ietf.org/html/rfc7518#section-4.6) and registered the JOSE registry; this example will use `ECDH-ES+A256KW`.

The multicodec identifier for X25519 public keys is `x25519-pub` and its code is `0xec`.

An example output from a function implementing the [syntax](#syntax) would be: `ECDH-ES+A256KW|zBzoR5sqFgi6q3iFia8JPNfENCpi7RNSTKF7XNXX96SBY4`.

**P-256:**

The algorithm for usage of P-256 keys along with the SHA-256 hash function identified in [RFC7518](https://tools.ietf.org/html/rfc7518#section-3.4) and registered in the JOSE registry is `ES256`.

The multicodec identifier for P-256 public keys is `p256-pub` and its code is `0x1200`.

An example output from a function implementing the [syntax](#syntax) would be: `ES256|z3u1vAS3rWXpB1icR5Df5yUaVtn2Q2i1AMCKxBACNNqsxJa1`


**P-384:**

The algorithm for usage of P-384 keys along with the SHA-384 hash function identified in [RFC7518](https://tools.ietf.org/html/rfc7518#section-3.4) and registered in the JOSE registry is `ES384`.

The multicodec identifier for P-384 public keys is `p384-pub` and its code is `0x1201`.

An example output from a function implementing the [syntax](#syntax) would be: `ES384|z2bHnTFkhn3NLWvF4qei6cLBiL5xtvuY8wt74jvi7w9rA3W29i6st9YkmL8EYBsbARTrrN`.

## Changes to RFCs

Should this RFC be [ACCEPTED](https://github.com/hyperledger/aries-rfcs/blob/master/README.md#accepted), a [community-coordinated update](https://github.com/hyperledger/aries-rfcs/blob/master/concepts/0345-community-coordinated-update/README.md) will be used to apply updates to the agent code bases and impacted RFCs.

### RFC0067 DIDComm DIDDoc Conventions

* Switch to the new syntax for inlined keys
* Separate authentication keys (for signatures) from key agreement keys (for encryption)

This RFC proposes the addition of a new attribute to the [`service`](https://github.com/hyperledger/aries-rfcs/blob/master/features/0067-didcomm-diddoc-conventions/README.md#service-conventions) object: `authnKeys`.

Example with all keys inlined:

```diff
{
  "service": [{
     "id": "did:example:123456789abcdefghi#did-communication",
     "type": "did-communication",
     "priority" : 0,
-    "recipientKeys" : [ "did:example:123456789abcdefghi#1" ],
-    "routingKeys" : [ "did:example:123456789abcdefghi#1" ],
+    "authnKeys": ["ES384|z2bHnTFkhn3NLWvF4qei6cLBiL5xtvuY8wt74jvi7w9rA3W29i6st9YkmL8EYBsbARTrrN"],
+    "recipientKeys" : ["ECDH-1PU+A256KW|zBzoR5sqFgi6q3iFia8JPNfENCpi7RNSTKF7XNXX96SBY4"],
+    "routingKeys" : ["ECDH-ES+A256KW|zBzoR5sqFgi6q3iFia8JPNfENCpi7RNSTKF7XNXX96SBY4"],
     "serviceEndpoint": "https://agent.example.com/"
   }]
 }
```

### RFC0434 Out-of-Band

* Switch to the new syntax for inlined keys
* Separate authentication keys (for signatures) from key agreement keys (for encryption)

This RFC proposes the addition of a new attribute to the [`service`](https://github.com/hyperledger/aries-rfcs/blob/master/features/0067-didcomm-diddoc-conventions/README.md#service-conventions) object in the invitation message: `authnKeys`.

Example:

```diff
{
  "@type": "https://didcomm.org/out-of-band/%VER/invitation",
  "@id": "<id used for context as pthid>",
  "label": "Faber College"
  "handshake_protocols": ["https://didcomm.org/didexchange/1.0"]
  "service": [
    {
       {
         "id": "#inline"
         "type": "did-communication",
-        "recipientKeys": ["did:key:z6MkpTHR8VNsBxYAAWHut2Geadd9jSwuBV8xRoAnwWsdvktH"],
-        "routingKeys": [],
+        "authnKeys": ["ES384|z2bHnTFkhn3NLWvF4qei6cLBiL5xtvuY8wt74jvi7w9rA3W29i6st9YkmL8EYBsbARTrrN"],
+        "recipientKeys" : ["ECDH-1PU+A256KW|zBzoR5sqFgi6q3iFia8JPNfENCpi7RNSTKF7XNXX96SBY4"],
+        "routingKeys" : [],
         "serviceEndpoint": "https://example.com:5000"
       },
       "did:sov:LjgpST2rjsoxYegQDRm7EL"
    }
  ]
}
```

### RFC0023 DID-Exchange

* Switch to the new syntax for inlined keys in all the examples
* Attachments MUST be signed with a key contained in the corresponding invitation's `authnKeys` attribute

**Example: Request message**

```diff
{
  "@id": "5678876542345",
  "@type": "https://didcomm.org/didexchange/1.0/request",
  "~thread": { 
      "thid": "5678876542345",
      "pthid": "<id of invitation>"
  },
  "label": "Bob",
  "did": "B.did@B:A",
  "did_doc~attach": {
      "@id": "d2ab6f2b-5646-4de3-8c02-762f553ab804",
      "mime-type": "application/json",
      "data": {
         "base64": "eyJ0eXAiOiJKV1Qi... (bytes omitted)",
         "jws": {
            "header": {
-               "kid": "did:key:z6MkmjY8GnV5i9YTDtPETC2uUAW6ejw3nk5mXF5yci5ab7th"
+               "kid": "EdDSA|z6MkpTHR8VNsBxYAAWHut2Geadd9jSwuBV8xRoAnwWsdvktH"

            },
            "protected": "eyJhbGciOiJFZERTQSIsImlhdCI6MTU4Mzg4... (bytes omitted)",
            "signature": "3dZWsuru7QAVFUCtTd0s7uc1peYEijx4eyt5... (bytes omitted)"
         }
      }
   }
}
```

## Drawbacks

* The multibase/multicodec scheme is not a standard
    * However, `did:key` reuses this scheme and therefore this is not a step back.
    * We hope that both [multibase data format](https://tools.ietf.org/html/draft-multiformats-multibase-02#ref-6) and [multicodec format](https://tools.ietf.org/html/draft-snell-multicodec-00) are standardised at the IETF with registries.

## Rationale and alternatives

### JSON Web Key

Spec: [JSON Web Key](https://tools.ietf.org/html/rfc7517).

This format is standardised at by the RFC referenced above, has found widespread support in multiple programming languages, and supports a wider range of key types (eg. RSA).

However, it has been previously suggested that it is too verbose and only adds the type of the key (source: [Aries RFC 0360](https://github.com/hyperledger/aries-rfcs/blob/master/features/0360-use-did-key/README.md#rationale-and-alternatives)).

Aries RFC protocols and message formats explicitly require two kinds of usages for keys: signatures (for authentication and integrity) and key agreement (for encryption). Barring additional purposes such as `capabilityInvocation` and `capabilityDelegation` defined in [DID-CORE](https://www.w3.org/TR/did-core/) - as well as the nuances between `authentication` and `assertionMethod` described there - specifying the JWK's [`alg`](https://tools.ietf.org/html/rfc7517#section-4.4) value should be enough to discern between "signatures" and "key agreement" as the key's purpose.

Future explorations may further evaluate JWKs as a viable, standardised alternative to this RFC, and MUST consider the impact on the size of messages as part of the analysis.

## Prior art

* [Aries RFC0360 did:key Usage](https://github.com/hyperledger/aries-rfcs/blob/master/features/0360-use-did-key/README.md)
* [IETF RFC7517 JSON Web Key](https://tools.ietf.org/html/rfc7517)

## Unresolved questions

- Should `handshake_protocols` be moved into the `service` object in OOB invitations?
    - Having it as a top-level attribute means it applies across all `service` objects which means a smaller message
- What are the encoding rules for the raw keys before passing as arg into the `multicodec` function?

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

*Implementation Notes*

Name / Link | Implementation Notes
--- | ---
 | 
