# Aries RFC 0234: Signature Decorator
- Authors: [Kyle Den Hartog](kyle.denhartog@evernym.com)
- Status: [DEMONSTRATED](/README.md#demonstrated)
- Since: 2019-09-27
- Status Note: Retroactive port of [this HIPE](https://github.com/kdenhartog/indy-hipe/blob/d421fc77bae87c780aad346d15c0c49939adc281/text/digital-signatures/README.md) (never merged) on which the `did-exchange` and `connection` protocols depend
- Supersedes: [this HIPE](https://github.com/kdenhartog/indy-hipe/blob/d421fc77bae87c780aad346d15c0c49939adc281/text/digital-signatures/README.md) (never merged)
- Start Date: 2019-01-07
- Tags: feature, decorator

## Summary

The `~sig` [field-level decorator](../../concepts/0011-decorators/README.md#decorator-scope) enables [non-repudiation](../../concepts/0049-repudiation/README.md) by allowing an Agent to add a digital signature over a portion of a DIDComm message.

## Motivation

While today we support a standard way of authenticating messages in a repudiable way, we also see the need for non-repudiable digital signatures for use cases where high authenticity is necessary such as signing a bank loan. There's additional beneficial aspects around having the ability to prove provenance of a piece of data with a digital signature. These are all use cases which would benefit from a standardized format for non-repudiable digital signatures.

This RFC outlines a field-level decorator that can be used to provide non-repudiable digital signatures in DIDComm messages. It also highlights a standard way to encode data such that it can be deterministically verified later.

## Tutorial

This RFC introduces a new field-level decorator named `~sig` and maintains a registry of standard [Signature Schemes](#signature-schemes) applicable with it.

The `~sig` field decorator may be used with any field of data. Its value MUST match the json object format of the chosen signature scheme. 

We'll use the following message as an example:

```jsonc
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/example/1.0/test_message",
    "@id": "df3b699d-3aa9-4fd0-bb67-49594da545bd",
    "msg": {
        "text": "Hello World!",
        "speaker": "Bob"
    }
}
```

Digitally signing the `msg` object with the `ed25519sha256_single` scheme results in a transformation of the original message to this:

```jsonc
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/example/1.0/test_message",
    "@id": "df3b699d-3aa9-4fd0-bb67-49594da545bd",
    "msg~sig": {
      "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/signature/1.0/ed25519Sha512_single",
      "sig_data": "base64URL(64bit_integer_from_unix_epoch|msg_object)",
      "signature": "base64URL(digital signature function output)",
      "signers": "base64URL(inlined_signing_verkey)"
    }
}
```

The original `msg` object has been replaced with its `~sig`-decorated counterpart in order to prevent message bloat.

When an Agent receives a DIDComm message with a field decorated with `~sig`, it runs the appropriate signature scheme algorithm and restores the DIDComm message's structure back to its original form.

## Reference

### Applying the digital signature

In general, the steps to construct a `~sig` are:

1. Choose a [signature scheme](#signature-schemes). This determines the `~sig` decorator's [message type URI](../../concepts/0003-protocols/uris.md#mturi) (the `@type` seen above) and the signature algorithm.
2. Serialize the JSON object to be authenticated to a sequence of bytes (`msg` in the example above). This will be the plaintext input to the signature scheme.
3. Construct the contents of the new `~sig` object according to the chosen signature scheme with the plaintext as input.
4. Replace the original object (`msg` in the example above) with the new `~sig` object. The new object's label MUST be equal to the label of the original object appended with "~sig".

### Verifying the digital signature

The outcome of a successful signature verification is the replacement of the `~sig`-decorated object with its original representation:

1. Select the signature scheme according to the message type URI (`ed25519sha256_single` in the example above)
2. Run the signature scheme's verification algorithm with the `~sig`-decorated object as input.
   1. The software MUST cease further processing of the DIDComm message if the verification algorithm fails.
3. Replace the `~sig`-decorated object with the output of the scheme's verification algorithm.

The end result MUST be semantically identical to the original DIDComm message before application of the signature scheme (eg. the original example message [above](#tutorial)).

### Additional considerations

The data to authenticate is base64URL-encoded and then embedded as-is so as to prevent false negative signature verifications that could potentially occur when sending JSON data which has no easy way to canonicalize the structure. Rather, by including the exact data in Base64URL encoding, the receiver can be certain that the data signed is the same as what was received. 

### Signature Schemes

This decorator should support a specific set of signatures while being extensible. The list of current supported schemes are outlined below.

| Signature Scheme | Scheme Spec |
|:----------------:|:-----------:|
|ed25519Sha512_single|[spec](ed25519sha256_single.md)|

> TODO provide template in this RFC directory. 

To add a new signature scheme to this registry, follow the template provided to detail the new scheme as well as provide some test cases to produce and verify the signature scheme is working.

## Drawbacks

Since digital signatures are non-repudiable, it's worth noting the privacy implications of using this functionality. In the event that a signer has chosen to share a message using a non-repudiable signature, they forgo the ability to prevent the verifier from sharing this signature on to other parties. This has potentially negative implications with regards to consent and privacy. 

**Therefore, this functionality should only be used if non-repudiable digital signatures are absolutely necessary.**

## Rationale and alternatives

[JSON Web Signatures](https://tools.ietf.org/html/rfc7515) are an alternative to this specification in widespread use. We diverged from this specification for the following reasons:

* Does not support our need for message decorators (sign only parts of a DIDComm message)
* Does not support signature-aggregation featured in schemes like [BLS signatures](https://en.wikipedia.org/wiki/Boneh%E2%80%93Lynn%E2%80%93Shacham).

## Prior art

[IETF RFC 7515 (JSON Web Signatures)](https://tools.ietf.org/html/draft-ietf-jose-json-web-signature-41)

## Unresolved questions

*Does there need to be an signature suite agreement protocol similar to TLS cipher suites?*
- No, rather the receiver of the message can send an error response if they're unable to validate the signature.

*How should multiple signatures be represented?*
- One solution is to do [<digital_sig1>, <digital_sig2>] for `signature` and do [<verkey1>, <verkey2>] for `signers`

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

Name / Link | Implementation Notes
--- | ---
[Aries Static Agent - Python](https://github.com/hyperledger/aries-staticagent-python) | `ed25519sha256_single`
[Aries Framework - .NET](https://github.com/hyperledger/aries-framework-dotnet) | `ed25519sha256_single`
[Aries Framework - Go](https://github.com/hyperledger/aries-framework-go) | `ed25519sha256_single`
