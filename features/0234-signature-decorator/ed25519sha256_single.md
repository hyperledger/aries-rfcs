# The `ed25519sha256_single` signature scheme

## Tutorial

### Application

This scheme computes a single [ed25519](https://ed25519.cr.yp.to/) digital signature over the input message. Its output is a `~sig` object with the following contents:

```jsonc
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/signature/1.0/ed25519Sha512_single",
    "sig_data": "base64URL(64bit_integer_from_unix_epoch|msg)",
    "signature": "base64URL(ed25519 signature)",
    "signers": "base64URL(inlined_ed25519_signing_verkey)"
}
```

* `@type` MUST be `did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/signature/1.0/ed25519Sha512_single`
* `sig_data` MUST be the base64URL encoding of a 64-bit integer prepended to the message
* `signature` MUST be the base64URL encoding of the resulting ed25519 digital signature over `sig_data`
* `signers` MUST be the base64URL encoding of the corresponding ed25519 public key used to sign `sig_data`

### Verification

The successful outcome of this scheme is the `plaintext`.

1. base64URL-decode `signers`
2. base64URL-decode `signature`
3. Verify the ed25519 signature over `sig_data` with the key provided in `signers`
   1. Further processing is halted if verification fails and an "authentication failure" error is returned
4. base64URL-decode the `sig_data`
5. Strip out the first 8 bytes
6. Return the remaining bytes