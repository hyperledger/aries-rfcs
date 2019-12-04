# Aries RFC 0334: JWE envelope 1.0

- Authors: [Baha A. Shaaban](mailto:baha.shaaban@securekey.com) (SecureKey Technologies Inc.), [Troy Ronda](mailto:troy.ronda@securekey.com) (SecureKey Technologies Inc.)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2019-11-28
- Status Note: RFC under development
- Supersedes:
- Start Date: 2019-11-01
- Tags: [feature](/tags.md#feature)

## Summary

Agents need to use a common set of algorithms when exchanging and persisting data. This RFC supplies a cipher suite and examples for DIDComm envelopes.

## Motivation

The goal of this RFC is define ciphersuites for Anoncrypt and Authcrypt such that we can achieve better compatability with JOSE. We also aim to supply both a compliant suite and a constrained device suite. The compliant suite is suitable for implementations that contain AES hardware acceleration or desire to use NIST / FIPS algorithms (where possible).

## Encryption Algorithms

The next two sub-sections describe the encryption algorithms that must be supported. On devices with AES hardware acceleration or requiring compliance, AES GCM is the recommended algorithm. Otherwise, XChacha20Poly1305 should be used.

### Content Encryption Algorithms

The following table defines the supported content encryption algorithms for DIDComm JWE envelopes:

 Content Encryption   | Encryption Algorithm identifier
 :------------------  | :-------------------
 AES-GCM (256 bit)    | A256GCM
 XChacha20Poly1305    | XC20P

### Key Encryption Algorithms

The following table defines the supported key wrapping encryption algorithms for DIDComm JWE envelopes:

 Key Encryption                 | Encryption algorithm identifier   | Anoncrypt/Authcrypt
 :----------------------------- | :-------------------------------- | :--------------------
 ECDH-ES + AES key wrap         | ECDH-ES+A256KW                    | Anoncrypt
 ECDH-1PU + AES key wrap        | ECDH-1PU+A256KW                   | Authcrypt


### Curves support

The following curves are supported:

 Curve Name                                                 | Curve identifier
 :--------------------------------------------------------- | :-----------------
 X25519 (aka Curve25519)                                    | X25519 (default)
 NIST P256 (aka SECG secp256r1 and ANSI X9.62 prime256v1, ref [here](https://tools.ietf.org/search/rfc4492#appendix-A))   | P-256

Other curves are optional.

#### Security Consideration for Curves

As noted in the ECDH-1PU [IETF draft](https://tools.ietf.org/html/draft-madden-jose-ecdh-1pu-02#section-4) security considerations section, all implementations must ensure the following:
```text
When performing an ECDH key agreement between a static private key
and any untrusted public key, care should be taken to ensure that the
public key is a valid point on the same curve as the private key.
Failure to do so may result in compromise of the static private key.
For the NIST curves P-256, P-384, and P-521, appropriate validation
routines are given in Section 5.6.2.3.3 of [NIST.800-56A]. For the
curves used by X25519 and X448, consult the security considerations
of [RFC7748].
```


### JWE Examples

AES GCM encryption and key wrapping examples are found in [Appendix C](https://tools.ietf.org/html/rfc7518#appendix-C) of the JSON Web Algorithm specs.

The Proposed [JWE Formats](#jwe-formats) below lists a combination of content encryption and key wrapping algorithms formats.

## Drawbacks

- All new algorithm identifiers should be registered at IANA.
  - XC20P
  - ECDH-1PU+A256KW (already in IETF draft)
- Security Considerations of [ECDH-1PU](https://tools.ietf.org/html/draft-madden-jose-ecdh-1pu-02) (Section 4)
- X25519 is not yet part of SP 800-56A. See [NIST post](https://csrc.nist.gov/News/2017/Transition-Plans-for-Key-Establishment-Schemes) for more information.

## Rationale and alternatives

Our approach for AuthCrypt compliance is to use the NIST approved `One-Pass Unified Model for ECDH` scheme described in [SP 800-56A Rev. 3](https://csrc.nist.gov/publications/detail/sp/800-56a/rev-3/final). The JOSE version is defined as `ECDH-1PU` in this [IETF draft](https://tools.ietf.org/html/draft-madden-jose-ecdh-1pu-02).

Aries agents currently use the envelope described in [RFC0019](/features/0019-encryption-envelope/README.md). This envelope uses libsodium (NaCl) encryption/decryption, which is based on Salsa20Poly1305 algorithm.

Another prior effort towards enhancing JWE compliance is to use XChacha20Poly1305 encryption and ECDH-SS key wrapping mode. See Aries-RFCs [issue-133](https://github.com/hyperledger/aries-rfcs/issues/133#issuecomment-535199768) and [Go JWE Authcrypt package](https://github.com/hyperledger/aries-framework-go/tree/v0.1.0/pkg/didcomm/packer/jwe/authcrypt) for an implementation detail. As ECDH-SS is not specified by JOSE, a new recipient header field, `spk`, was needed to contain the static encrypted public key of the sender. Additionally (X)Chacha20Poly1305 key wrapping is also not specified by JOSE. For these reasons, this option is mentioned here as reference only.

## JWE formats

### Anoncrypt using ECDH-ES key wrapping mode and XC20P content encryption

```json
 {
  "protected": base64url({
      "typ": "didcomm-envelope-enc",
      "enc": "XC20P", // or "A256GCM"
  }),
  "recipients": [
    {
      "header": {
        "kid": base64url(recipient KID), // e.g: base64url("urn:123")
        "alg": "ECDH-ES+A256KW",
        "epk": { // defining X25519 key as an example JWK, but this can be AES-GCM 256-bit key as well 
          "kty": "OKP",
          "crv": "X25519",
          "x": "-3bLMSHYDG3_LVNh-MJvoYs_a2sAEPr4jwFfFjTrmUo" // sender's ephemeral public key value base64url encoded
        },
        "apu": epk.x value above,
        "apv": base64url(recipient.kid)
      },
      "encrypted_key": "Sls6zrMW335GJsJe0gJU4x1HYC4TRBZS1kTS1GATEHfH_xGpNbrYLg"
    }
  ],
  "iv": "K0PfgxVxLiW0Dslx",
  "ciphertext": "Sg",
  "tag": "PP31yGbQGBz9zgq9kAxhCA"
}
```

`typ` header field is the DIDComm Transports value as mentioned in [RFC-0025](https://github.com/hyperledger/aries-rfcs/tree/master/features/0025-didcomm-transports#reference). This RFC states the prefix `application/` but according to [IANA Media types](https://www.iana.org/assignments/media-types/media-types.xhtml#application) the prefix is implied therefore not needed here.

### Anoncrypt using ECDH-ES key wrapping mode and A256GCM content encryption

```json
{
  "protected": base64url({
          "typ": "didcomm-envelope-enc",
          "enc": "A256GCM", // "XC20P"
  }),
  "recipients": [
    {
      "header": {
        "kid": base64url(recipient KID),
        "alg": "ECDH-ES+A256KW",
        "epk": {
          "kty": "OKP",
          "crv": "X25519",
          "x": "aOH-76BRwkHf0nbGokaBsO6shW9McEs6jqVXaF0GNn4" // sender's ephemeral public key value base64url encoded
        },
        "apu": epk.x value above,
        "apv": base64url(recipient.kid)
      },
      "encrypted_key": "wXzKi-XXb6fj_KSY5BR5hTUsZIiAQKrxblTo3d50B1KIeFwBR98fzQ"
    }
  ],
  "iv": "9yjR8zvgeQDZFbIS",
  "ciphertext": "EvIk_Rr6Nd-0PqQ1LGimSqbKyx_qZjGnmt6nBDdCWUcd15yp9GTeYqN_q_FfG7hsO8c",
  "tag": "9wP3dtNyJERoR7FGBmyF-w"
}
```

In the above two examples, `apu` is the encode ephemeral key used to encrypt the cek stored in `encrypted_key` and `apv` is the key id of the static public key of the recipient. Both are base64Url encoded.
`kid` is the value of a key ID in a DID document that should be resolvable to fetch the raw public key used.

### Authcrypt using ECDH-1PU key wrapping mode

```json
{
    "protected": base64url({
        "typ": "didcomm-envelope-enc",
        "enc":"XC20P", // or "A256GCM"
        "skid": base64url(sender KID),
    }),
    "recipients": [
        {
            "encrypted_key": "base64url(encrypted CEK)",
            "header": {
                "kid": base64url(recipient KID),
                "alg": "ECDH-1PU+A256KW",
                "enc": "A256GCM",
                "apu": base64url(senderID),
                "apv": base64url(recipientID),
                "epk": {
                  "kty": "OKP",
                  "crv": "X25519",
                  "x": "aOH-76BRwkHf0nbGokaBsO6shW9McEs6jqVXaF0GNn4"
                },
            }
        },
       ...
    ],
    "aad": "base64url(sha256(concat('.',sort([recipients[0].kid, ..., recipients[n].kid])))))",
    "iv": "base64url(content encryption IV)",
    "ciphertext": "base64url(XC20P(DIDComm payload, base64Url(json($protected)+'.'+$aad), content encryption IV, CEK))"
    "tag": "base64url(AEAD Authentication Tag)"
}
```

With the recipients headers representing an ephemeral key that can be used to derive the key to be used for AEAD decryption of the CEK following the [ECDH-1PU](https://tools.ietf.org/html/draft-madden-jose-ecdh-1pu-02) encryption scheme.

The function `XC20P` in the example above is defined as the XChahcha20Poly1035 cipher function. This can be replaced by the A256GCM cipher function.

## Prior art

- The [JWE](https://tools.ietf.org/html/rfc7518) family of encryption methods.
- [Aries RFC 0019-encryption-envelope](https://github.com/hyperledger/aries-rfcs/tree/master/features/0019-encryption-envelope) suggested envelope formats will be superseded by this RFC.
- [Aries RFC 0025-didcomm-transports](https://github.com/hyperledger/aries-rfcs/tree/master/features/0025-didcomm-transports#reference) for the content type used in the proposed envelopes.
- [minimal-cipher](https://github.com/digitalbazaar/minimal-cipher) implementation
- [Aries-Framework-Go](https://github.com/hyperledger/aries-framework-go/) has an experimental (X)Chacha20Poly1305 Packer implementation based on Aries-RFCs [issue-133](https://github.com/hyperledger/aries-rfcs/issues/133#issuecomment-535199768)
- [IANA Media Types](https://www.iana.org/assignments/media-types/media-types.xhtml#application)
- [Public Key Authenticated Encryption for JOSE: ECDH-1PU](https://tools.ietf.org/html/draft-madden-jose-ecdh-1pu-02)
- [NIST SP 800-56A Rev. 3 Recommendation for Pair-Wise Key-Establishment schemes Using Discrete Logarithm Cryptography](https://csrc.nist.gov/publications/detail/sp/800-56a/rev-3/final)
- [Appendix A of IETF 4492](https://tools.ietf.org/search/rfc4492#appendix-A) listing equivalent curve names.

## Unresolved questions

- What fields should Key identifiers in ES and 1PU key wrapping modes use? `kid` vs `id` (vs `skid` introduced in [ECDH-1PU](https://tools.ietf.org/html/draft-madden-jose-ecdh-1pu-02) IETF document) or any other combination of fields. There is a discussion about this [here](https://github.com/w3c/did-core/issues/131).
- What kind of keys to include in the JWE envelope? `Encryption` or `signing` keys? Currently the existing Aries agents include `signing` keys for the sender and recipients and convert them to encryption keys for encryption/decryption operations only. The drawback is the envelope transmitted by the agent contains signing keys. The aries-framework-go repo includes (an experimental) JWE implementation that expects `signing` keys from the API user and then fetches the corresponding `encryption` keys from the wallet (KMS) to build the envelope. `Signing` keys are not included in the envelope in this implementation. There is a need to separate them from `encryption` keys in the current Aries implementations as well.

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

| Name / Link | Implementation Notes |
| ----------- | -------------------- |
|             |                      |

Note: [Aries Framework - Go](https://github.com/hyperledger/aries-framework-go) will soon work on a first draft implementation of this RFC.
