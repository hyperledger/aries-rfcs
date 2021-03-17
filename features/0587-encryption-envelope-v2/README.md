# Aries RFC 0587: Encryption Envelope v2

- Authors: [Baha A. Shaaban](mailto:baha.shaaban@securekey.com) (SecureKey Technologies Inc.), [Troy Ronda](mailto:troy.ronda@securekey.com) (SecureKey Technologies Inc.)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2021-02-10
- Status Note:
- Supersedes:
- Start Date: 2021-02-10
- Tags: [feature](/tags.md#feature)

## Summary

This RFC proposes that we support the definition of envelopes from [DIDComm Messaging](https://identity.foundation/didcomm-messaging/spec).

## Motivation

This RFC defines ciphersuites for envelopes such that we can achieve better compatability with DIDComm Messaging being specified at DIF.
The ciphersuites defined in this RFC are a subset of the definitions in [Aries RFC 0334-jwe-envelope](https://github.com/hyperledger/aries-rfcs/tree/master/features/0334-jwe-envelope).

## Encryption Algorithms

[ECDH-1PU draft 03](https://tools.ietf.org/html/draft-madden-jose-ecdh-1pu-03) defines the JWE structure. The following sections summarize the supported algorithms.

### Curves

DIDComm Messaging (and this RFC) requires support for `X25519`, `P-256`, and `P-384`.

- P-256 (reference in [RFC4492](https://tools.ietf.org/search/rfc4492#appendix-A))
- P-384 (reference in [RFC4492](https://tools.ietf.org/search/rfc4492#appendix-A))
- P-521 (reference in [RFC4492](https://tools.ietf.org/search/rfc4492#appendix-A))
- X25519 (reference in [RFC7748](https://tools.ietf.org/html/rfc7748#section-5))

### Content Encryption Algorithms

DIDComm Messaging (and this RFC) requires support for both `XC20P` and `A256GCM`.

- XC20P (XChaCha20Poly1305 - reference in [xchacha draft 03](https://tools.ietf.org/html/draft-irtf-cfrg-xchacha-03))
- A256GCM (AES-GCM with a 256 bit key - reference in [RFC7518](https://tools.ietf.org/html/rfc7518#section-5.1))

### Key Wrapping Algorithms

DIDComm Messaing (and this RFC) requires support for `ECDH-1PU+A256KW`.

- ECDH-1PU+A256KW (defined in [ECDH-1PU draft 03](https://tools.ietf.org/html/draft-madden-jose-ecdh-1pu-03#section-2.2))

## Anoncrypt equivalent

For situations where the envelopes should be anonymous, we use a newly minted DID rather than a different Anoncrypt mechanism.
The newly minted DID is used once and then discarded.
This approach matches the DIDComm Messaging mechanism.

## Media Type

The media type associated to this envelope is `application/didcomm-encrypted+json`.
[RFC 0044](../0044-didcomm-file-and-mime-types/README.md) provides a general discussion of media (aka mime) types.

The media type of the envelope MUST be set in the `typ` [property](https://tools.ietf.org/html/rfc7516#section-4.1.11) of the JWE and the media type of the payload MUST be set in the `cty` [property](https://tools.ietf.org/html/rfc7516#section-4.1.12) of the JWE.

 For example, following the guidelines of [RFC 0044](../0044-didcomm-file-and-mime-types/README.md), an encrypted envelope with a plaintext DIDComm v1 payload contains the `typ` property with the value `application/didcomm-encrypted+json` and `cty` property with the value `application/json;flavor=didcomm-msg`.

## DIDComm v2 Transition

As this RFC specifies the same envelope format as will be used in DIDComm v2, an implementor should detect if the payload contains DIDComm v1 content or the JWM from DIDComm v2.
These payloads can be distinguished based on the `cty` [property](https://tools.ietf.org/html/rfc7516#section-4.1.12) of the JWE.

As discussed in [RFC 0044](../0044-didcomm-file-and-mime-types/README.md), the content type for the plaintext DIDComm v1 message is `application/json;flavor=didcomm-msg`.
When the `cty` property contains `application/json;flavor=didcomm-msg`, the payload is treated as DIDComm v1.
[DIDComm Messaging](https://identity.foundation/didcomm-messaging/spec) will specify appropriate media types for DIDComm v2.

## Drawbacks

The DIDComm v2 specification is a draft. However, the aries-framework-go project has already implemented the new envelope format.

## Rationale and alternatives

Our approach for Authcrypt compliance is to use the NIST approved `One-Pass Unified Model for ECDH` scheme described in [SP 800-56A Rev. 3](https://csrc.nist.gov/publications/detail/sp/800-56a/rev-3/final). The JOSE version is defined as `ECDH-1PU` in this [IETF draft](https://tools.ietf.org/html/draft-madden-jose-ecdh-1pu-03).

Aries agents currently use the envelope described in [RFC0019](/features/0019-encryption-envelope/README.md). This envelope uses libsodium (NaCl) encryption/decryption, which is based on Salsa20Poly1305 algorithm.

## Prior art

- The [JWE](https://tools.ietf.org/html/rfc7518) family of encryption methods.
- [Aries RFC 0019-encryption-envelope](https://github.com/hyperledger/aries-rfcs/tree/master/features/0019-encryption-envelope) suggested envelope formats will be superseded by this RFC.
- [Aries RFC 0025-didcomm-transports](https://github.com/hyperledger/aries-rfcs/tree/master/features/0025-didcomm-transports#reference) for the content type used in the proposed envelopes.
- [Aries RFC 0334-jwe-envelope](https://github.com/hyperledger/aries-rfcs/tree/master/features/0334-jwe-envelope).
- [DIDComm Messaging](https://identity.foundation/didcomm-messaging/spec).
- [minimal-cipher](https://github.com/digitalbazaar/minimal-cipher) implementation
- [Public Key Authenticated Encryption for JOSE: ECDH-1PU](https://tools.ietf.org/html/draft-madden-jose-ecdh-1pu-03)
- [NIST SP 800-56A Rev. 3 Recommendation for Pair-Wise Key-Establishment schemes Using Discrete Logarithm Cryptography](https://csrc.nist.gov/publications/detail/sp/800-56a/rev-3/final)

## Unresolved questions

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

| Name / Link | Implementation Notes |
| ----------- | -------------------- |
|             |                      |
