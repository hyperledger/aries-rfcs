# Aries RFC 0587: Encryption Envelope v2

- Authors: [Baha A. Shaaban](mailto:mailto:baha.shaaban@securekey.com) (SecureKey Technologies Inc.), [Troy Ronda](mailto:mailto:troy.ronda@securekey.com) (SecureKey Technologies Inc.)
- Status: [ACCEPTED](/README.md#accepted)
- Since: 2021-04-15
- Status Note: Included as part of the "prepare for DIDComm v2" subtarget of [AIP 2.0](../../concepts/0302-aries-interop-profile/README.md).
- Supersedes:
- Start Date: 2021-02-10
- Tags: [feature](/tags.md#feature)

## Summary

This RFC proposes that we support the definition of envelopes from [DIDComm Messaging](https://identity.foundation/didcomm-messaging/spec).

## Motivation

This RFC defines ciphersuites for envelopes such that we can achieve better compatability with DIDComm Messaging being specified at DIF.
The ciphersuites defined in this RFC are a subset of the definitions in [Aries RFC 0334-jwe-envelope](https://github.com/hyperledger/aries-rfcs/tree/main/features/0334-jwe-envelope).

## Encryption Algorithms

DIDComm defines both the concept of authenticated sender encryption (aka `Authcrypt`) and anonymous sender encryption (aka `Anoncrypt`).
In general, Aries RFCs and protocols use `Authcrypt` to exchange messages.
In some limited scenarios (e.g., mediator and relays), an Aries RFC or protocol may define usage of `Anoncrypt`.

[ECDH-1PU draft 04](https://tools.ietf.org/html/draft-madden-jose-ecdh-1pu-04) defines the JWE structure for `Authcrypt`.
`ECDH-ES` from [RFC 7518](https://tools.ietf.org/html/rfc7518#section-4.6) defines the JWE structure for `Anoncrypt`.
The following sections summarize the supported algorithms.

### Curves

DIDComm Messaging (and this RFC) requires support for `X25519`, `P-256`, and `P-384`.

- P-256 (reference in [RFC4492](https://tools.ietf.org/search/rfc4492#appendix-A))
- P-384 (reference in [RFC4492](https://tools.ietf.org/search/rfc4492#appendix-A))
- P-521 (optional, reference in [RFC4492](https://tools.ietf.org/search/rfc4492#appendix-A))
- X25519 (reference in [RFC7748](https://tools.ietf.org/html/rfc7748#section-5))

### Content Encryption Algorithms

DIDComm Messaging (and this RFC) requires support for both `XC20P` and `A256GCM` for Anoncrypt only and `A256CBC-HS512` for both Authcrypt and Anoncrypt.

- XC20P (XChaCha20Poly1305 - reference in [xchacha draft 03](https://tools.ietf.org/html/draft-irtf-cfrg-xchacha-03))
- A256GCM (AES-GCM with a 256 bits key - reference in [RFC7518 section 5.1](https://tools.ietf.org/html/rfc7518#section-5.1) and more specifically [RFC7518 section 5.3](https://tools.ietf.org/html/rfc7518#section-5.3))
- A256CBC-HS512 (AES256-CBC+HMAC-SHA512 with a 512 bits key - reference in [ECDH-1PU section 2.1](https://datatracker.ietf.org/doc/html/draft-madden-jose-ecdh-1pu-04#section-2.1) and [RFC 7518 section 5.2.5](https://datatracker.ietf.org/doc/html/rfc7518#section-5.2.5)) 

### Key Wrapping Algorithms

DIDComm Messaging (and this RFC) requires support for `ECDH-1PU+A256KW` and `ECDH-ES+A256KW`.

- ECDH-1PU+A256KW (defined in [ECDH-1PU draft 04](https://tools.ietf.org/html/draft-madden-jose-ecdh-1pu-04#section-2))
- ECDH-ES+A256KW (defined in [RFC 7518](https://tools.ietf.org/html/rfc7518#section-4.6))

## Key IDs `kid` and `skid` headers references in the DID document

Keys used by DIDComm envelopes MUST be sourced from the DIDs exchanged between two agents. Specifically, both sender and recipients keys MUST be retrieved from the DID document's `KeyAgreement` verification section as per the [DID Document Keys](https://identity.foundation/didcomm-messaging/spec/#did-document-keys) definition.

When Alice is preparing an envelope intended for Bob, the packing process should use a key from both hers and Bob's DID document's `KeyAgreement` section.

Assuming Alice has a DID Doc with the following `KeyAgreement` definition (source: [DID V1 Example 17](https://www.w3.org/TR/did-core/#example-17-key-agreement-property-containing-two-verification-methods)):
```jsonc
{
  "@context": "https://www.w3.org/ns/did/v1",
  "id": "did:example:123456789abcdefghi",
  ...
  "keyAgreement": [
    // this method can be used to perform key agreement as did:...fghi
    "did:example:123456789abcdefghi#keys-1",
    // this method is *only* approved for key agreement usage, it will not
    // be used for any other verification relationship, so its full description is
    // embedded here rather than using only a reference
    {
      "id": "did:example:123#zC9ByQ8aJs8vrNXyDhPHHNNMSHPcaSgNpjjsBYpMMjsTdS",
      "type": "X25519KeyAgreementKey2019", // external (property value)
      "controller": "did:example:123",
      "publicKeyBase58": "9hFgmPVfmBZwRvFEyniQDBkz9LmV7gDEqytWyGZLmDXE"
    }
  ],
  ...
}
```

The envelope packing process should set the `skid` header with value `did:example:123456789abcdefghi#keys-1` in the envelope's protected headers and fetch the underlying key to execute ECDH-1PU key derivation for content key wrapping.

Assuming she also has Bob's DID document which happens to include the following `KeyAgreement` section:

```jsonc
{
  "@context": "https://www.w3.org/ns/did/v1",
  "id": "did:example:jklmnopqrstuvwxyz1",
  ...
  "keyAgreement": [
    {
      "id": "did:example:jklmnopqrstuvwxyz1#key-1",
      "type": "X25519KeyAgreementKey2019", // external (property value)
      "controller": "did:example:jklmnopqrstuvwxyz1",
      "publicKeyBase58": "9hFgmPVfmBZwRvFEyniQDBkz9LmV7gDEqytWyGZLmDXE"
    }
  ],
  ...
}
```

There should be only 1 entry in the recipients of the envelope, representing Bob. The corresponding `kid` header for this recipient MUST have `did:example:jklmnopqrstuvwxyz1#key-1` as value. The packing process MUST extract the public key bytes found in `publicKeyBase58` of Bob's DID Doc `KeyAgreement[0]` to execute the ECDH-1PU key derivation for content key wrapping.

When Bob receives the envelope, the unpacking process on his end MUST resolve the `skid` protected header value using Alice's DID doc's `KeyAgreement[0]` in order to extract her public key. In Alice's DID Doc example above, `KeyAgreement[0]` is a reference id, it MUST be resolved from the main `VerificationMethod[]` of Alice's DID document (not shown in the example).

Once resolved, the unpacker will then execute ECDH-1PU key derivation using this key and Bob's own recipient key found in the envelope's `recipients[0]` to unwrap the content encryption key.

## Protecting the `skid` header
When the `skid` cannot be revealed in a plain-text JWE header (to avoid potentially leaking sender's key id), the `skid` MAY be encrypted for each recipient. In this case, instead of having a `skid` protected header in the envelope, each recipient MAY include an `encrypted_skid` header with a value based on the encryption of `skid` using ECDH-ES `Z` computation of the `epk` and the recipient's key as the encryption key.

For applications that don't require this protection, they MAY use `skid` protected header directly without any additional recipient headers.

Applications MUST use either `skid` protected header or `encrypted_skid` recipients header but not both in the same envelope.

## ECDH-1PU key wrapping and common protected headers
When using authcrypt, the 1PU draft [requires](https://datatracker.ietf.org/doc/html/draft-madden-jose-ecdh-1pu-04#section-2.1) mandates the use of AES_CBC_HMAC_SHA family of content encryption algorithms. To meet this requirement, JWE messages MUST use common `epk`, `apu`, `apv` and `alg` headers for all recipients. They MUST be set in the `protected` headers JWE section.

As per this requirement, the JWE building must first encrypt the payload then use the resulting `tag` as part of the key derivation process when wrapping the `cek`.

To meet this requirement, the above headers must be defined as follows:
* `epk`: generated once for all recipients. It MUST be of the same type and curve as all recipient keys since kdf with the sender key must be on the same curve.
 - Example: `"epk": {"kty": "EC","crv": "P-256","x": "BVDo69QfyXAdl6fbK6-QBYIsxv0CsNMtuDDVpMKgDYs","y": "G6bdoO2xblPHrKsAhef1dumrc0sChwyg7yTtTcfygHA"}`
* `apu`: similar to `skid`, this is the producer (sender) identifier, it MUST contain the `skid` value base64 RawURL (no padding) encoded. Note: this is base64URL(`skid` value).
 - Example for `skid` mentioned in an earlier [section](#key-ids-kid-and-skid-headers-references-in-the-did-document) above: `ZGlkOmV4YW1wbGU6MTIzNDU2Nzg5YWJjZGVmZ2hpI2tleXMtMQ`
* `apv`: this represents the recipients' `kid` list. The list must be alphanumerically sorted, `kid` values will then be concatenated with a `.` and the final result MUST be base64 URL (no padding) encoding of the SHA256 hash of concatenated list.
* `alg`: this is the key wrapping algorithm, ie: `ECDH-1PU+A256KW`.

A final note about `skid` header: since the 1PU draft [does not require](https://datatracker.ietf.org/doc/html/draft-madden-jose-ecdh-1pu-04#section-2.2.1) this header, authcrypt implementations MUST be able to resolve the sender kid from the `APU` header if `skid` is not set.

## Media Type

The media type associated to this envelope is `application/didcomm-encrypted+json`.
[RFC 0044](../0044-didcomm-file-and-mime-types/README.md) provides a general discussion of media (aka mime) types.

The media type of the envelope MUST be set in the `typ` [property](https://tools.ietf.org/html/rfc7516#section-4.1.11) of the JWE and the media type of the payload MUST be set in the `cty` [property](https://tools.ietf.org/html/rfc7516#section-4.1.12) of the JWE.

 For example, following the guidelines of [RFC 0044](../0044-didcomm-file-and-mime-types/README.md), an encrypted envelope with a plaintext DIDComm v1 payload contains the `typ` property with the value `application/didcomm-encrypted+json` and `cty` property with the value `application/json;flavor=didcomm-msg`.

 As specified in [IETF RFC 7515](https://tools.ietf.org/html/rfc7515) and referenced in [IETF RFC 7516](https://tools.ietf.org/html/rfc7516), implementations
 MUST also support media types that omit `application/`.
 For example, `didcomm-encrypted+json` and `application/didcomm-encrypted+json` are treated as equivalent media types.

As discussed in [RFC 0434](../0434-outofband/README.md) and [RFC 0067](../0067-didcomm-diddoc-conventions/README.md), the `accept` property is used to advertise supported media types.
The `accept` property may contain an envelope media type or a combination of the envelope media type and the content media type.
In cases where the content media type is not present, the expectation is that the appropriate content media type can be inferred.
For example, `application/didcomm-envelope-enc` indicates both Envelope v1 and DIDComm v1 and `application/didcomm-encrypted+json` indicates both Envelope v2 and DIDComm v2.
However, some agents may choose to support Envelope v2 with a DIDComm v1 message payload.

In case the `accept` property is set in both the DID service block and the out-of-band message, the out-of-band property takes precedence.

## DIDComm v2 Transition

As this RFC specifies the same envelope format as will be used in DIDComm v2, an implementor should detect if the payload contains DIDComm v1 content or the JWM from DIDComm v2.
These payloads can be distinguished based on the `cty` [property](https://tools.ietf.org/html/rfc7516#section-4.1.12) of the JWE.

As discussed in [RFC 0044](../0044-didcomm-file-and-mime-types/README.md), the content type for the plaintext DIDComm v1 message is `application/json;flavor=didcomm-msg`.
When the `cty` property contains `application/json;flavor=didcomm-msg`, the payload is treated as DIDComm v1.
[DIDComm Messaging](https://identity.foundation/didcomm-messaging/spec) will specify appropriate media types for DIDComm v2.
To advertise the combination of Envelope v2 with a DIDComm v1 message, the media type is `application/didcomm-encrypted+json;cty=application/json`.

## Additional AIP impacts

Implementors supporting an AIP sub-target that contains this RFC (e.g., `DIDCOMMV2PREP`) MAY choose to only support Envelope v2 without support for the original envelope declared in [RFC 0019](https://github.com/hyperledger/aries-rfcs/tree/main/features/0019-encryption-envelope). In these cases, the `accept` property will not contain `didcomm/aip2;env=rfc19` media type.

## Drawbacks

The DIDComm v2 specification is a draft. However, the aries-framework-go project has already implemented the new envelope format.

## Rationale and alternatives

Our approach for Authcrypt compliance is to use the NIST approved `One-Pass Unified Model for ECDH` scheme described in [SP 800-56A Rev. 3](https://csrc.nist.gov/publications/detail/sp/800-56a/rev-3/final). The JOSE version is defined as `ECDH-1PU` in this [IETF draft](https://tools.ietf.org/html/draft-madden-jose-ecdh-1pu-03).

Aries agents currently use the envelope described in [RFC0019](/features/0019-encryption-envelope/README.md). This envelope uses libsodium (NaCl) encryption/decryption, which is based on Salsa20Poly1305 algorithm.

## Prior art

- The [JWE](https://tools.ietf.org/html/rfc7518) family of encryption methods.
- [Aries RFC 0019-encryption-envelope](https://github.com/hyperledger/aries-rfcs/tree/main/features/0019-encryption-envelope) suggested envelope formats will be superseded by this RFC.
- [Aries RFC 0025-didcomm-transports](https://github.com/hyperledger/aries-rfcs/tree/main/features/0025-didcomm-transports#reference) for the content type used in the proposed envelopes.
- [Aries RFC 0334-jwe-envelope](https://github.com/hyperledger/aries-rfcs/tree/main/features/0334-jwe-envelope).
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
