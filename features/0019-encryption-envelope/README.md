# 0019: Encryption Envelope
- Author: Kyle Den Hartog(kyle.denhartog@evernym.com), Stephen Curran (swcurran@gmail.com), Sam Curren (sam@sovrin.org), Mike Lodder (mike@sovrin.org)
- Start Date: 2018-07-10 (approximate, backdated)

## Status

- Status: [ACCEPTED](/README.md#rfc-lifecycle)
- Status Date: 2019-05-04
- Status Note: Supersedes [INDY 0028 Wire Level Format](https://github.com/hyperledger/indy-hipe/tree/master/text/0028-wire-message-format)

## Summary

There are two layers of messages that combine to enable **interoperable** self-sovereign agent-to-agent communication. At the highest level are [Agent Plaintext Messages](https://github.com/hyperledger/indy-hipe/tree/master/text/0026-agent-file-format#agent-plaintext-messages-ap) - messages sent between identities to accomplish some shared goal (e.g., establishing a connection, issuing a verifiable credential, sharing a chat). Agent Plaintext Messages are delivered via the second, lower layer of messaging - Wire. An [Agent Wire Message](https://github.com/hyperledger/indy-hipe/tree/master/text/0026-agent-file-format#agent-wire-messages-aw) is a wrapper (envelope) around a plaintext message to permit secure sending and routing. A plaintext message going from its sender to its receiver passes through many agents, and a wire message envelope is used for each hop of the journey.

This HIPE describes the wire format and the functions in Aries SDK that implement it.

# Motivation

Wire messages use a standard format built on [JSON Web Encryption - RFC 7516](
https://tools.ietf.org/html/rfc7516). This format is not captive to Aries; it requires
no special Aries worldview or Aries dependencies to implement. Rather, it is a
general-purpose solution to the question of how to encrypt, decrypt, and route
messages as they pass over any transport(s). By documenting the format here, we
hope to provide a point of interoperability for developers of agents inside and
outside the Aries ecosystem.

We also document how Aries SDK implements its support for wire format through the
`pack()` and `unpack()` functions. For developers of Aries SDK, this is a sort of
design doc; for those who want to implement the format in other tech stacks, it
may be a useful reference.

## Tutorial

## Assumptions

We assume that each sending agent knows:

- Its intended recipient(s).
- What encryption (if any) is appropriate.
- If encryption will be used, a public key of the receiving agent.
- The physical endpoint to use for the receiver, and the appropriate transport protocol (https, zmq, etc.).

The assumptions can be made because either the message is being sent to an agent within the sending agent's domain and so the sender knows the internal configuration of agents, or the message is being sent outside the sending agent's domain and interoperability requirements are in force to define the sending agent's behaviour.

## Example Scenario

The example of Alice and Bob's [sovereign domains](https://docs.google.com/document/d/1gfIz5TT0cNp2kxGMLFXr19x1uoZsruUe_0glHst2fZ8/edit#heading=h.pufsrf9ucjvv) is used for illustrative purposes in defining this HIPE.

![Example Domains: Alice and Bob](domains.jpg)

In the diagram above:

- Alice has
  - 1 Edge agent - "1"
  - 1 Routing agent - "2"
  - 1 Domain Endpoint - "8"
- Bob has
  - 3 Edge Agents - "4", "5" and "6"
    - "6" is an Edge agent in the cloud, "4" and "5" are physical devices.
  - 1 Routing agent - "3"
  - 1 Domain Endpoint - "9"

For the purposes of this discussion we are defining the Wire Message agent message flow to be:

> 1 --> 2 --> 8 --> 9 --> 3 --> 4

However, that flow is just one of several that could match this configuration. What we know for sure is that:

- 1 is the Sender agent in this case and so must send the first or original message.
- 9 is the Domain Endpoint of Bob's domain and so must receive the message as a wire message
- 4 is the Receiver in this case and so must receive (and should be able to read) the first or original message.

## Wire Messages

A wire wessage is used to transport any plaintext message from one agent directly to another. In our example message flow above, there are five wire messages sent, one for each hop in the flow. The process to send a wire message consists of the following steps:

- Call the standard function `pack()` (implemented in the Aries-SDK) to wrap the plaintext message
- Send the wire message using the transport protocol defined by the receiving endpoint
- Receive the wire message
- Call the standard function `unpack()` to retrieve the plaintext message (and possibly its provenance) from the wire message

This is repeated with each hop, but the wire messages are nested, such that the plaintext is never visible until
it reaches its final recipient.  

## Implementation

We will describe the pack and unpack algorithms, and their output, in terms of
Aries' initial implementation, which may evolve over time. Other implementations
could be built, but they would need to emit and consume similar inputs and
outputs.

The data structures emitted and consumed by these algorithms are described
in a formal [schema](schema.md).

### Authcrypt mode vs. Anoncrypt mode

When packing and unpacking are done in a way that the sender is anonymous,
we say that we are in __anoncrypt mode__. When the sender is revealed, we
are in __authcrypt mode__. Authcrypt mode reveals the sender *to the recipient
only*; it is not the same as a non-repudiable signature. See the [HIPE about
signing](https://github.com/hyperledger/indy-hipe/pull/79), and [this
discussion about the theory of non-repudiation](https://github.com/sovrin-foundation/protocol/blob/d1039cd793a801abdc5fdfdc25ef071778039075/janus/repudiation.md).

### Pack Message

#### pack_message() interface

packed_message = pack_message(wallet_handle, message, receiver_verkeys, sender_verkey)

#### pack_message() Params: 
- wallet_handle: handle to the wallet that contains the sender's secrets.
- message: the message (plaintext, or nested wire message) as a string. If it's JSON object it should be in string format first
- receiver_verkeys: a list of recipient verkeys as string containing a JSON array
- sender_verkey: the sender's verkey as a string. This verkey is used to look up the sender's private key so the wallet can put supply it as input to the encryption algorithm. When an empty string ("") is passed in this parameter, anoncrypt mode is used

#### pack_message() return value (Authcrypt mode)
This is an example of an outputted message encrypting for two verkeys using Authcrypt.

```json
{
    "protected": "eyJlbmMiOiJ4Y2hhY2hhMjBwb2x5MTMwNV9pZXRmIiwidHlwIjoiSldNLzEuMCIsImFsZyI6IkF1dGhjcnlwdCIsInJlY2lwaWVudHMiOlt7ImVuY3J5cHRlZF9rZXkiOiJMNVhEaEgxNVBtX3ZIeFNlcmFZOGVPVEc2UmZjRTJOUTNFVGVWQy03RWlEWnl6cFJKZDhGVzBhNnFlNEpmdUF6IiwiaGVhZGVyIjp7ImtpZCI6IkdKMVN6b1d6YXZRWWZOTDlYa2FKZHJRZWpmenRONFhxZHNpVjRjdDNMWEtMIiwiaXYiOiJhOEltaW5zdFhIaTU0X0otSmU1SVdsT2NOZ1N3RDlUQiIsInNlbmRlciI6ImZ0aW13aWlZUkc3clJRYlhnSjEzQzVhVEVRSXJzV0RJX2JzeERxaVdiVGxWU0tQbXc2NDE4dnozSG1NbGVsTThBdVNpS2xhTENtUkRJNHNERlNnWkljQVZYbzEzNFY4bzhsRm9WMUJkREk3ZmRLT1p6ckticUNpeEtKaz0ifX0seyJlbmNyeXB0ZWRfa2V5IjoiZUFNaUQ2R0RtT3R6UkVoSS1UVjA1X1JoaXBweThqd09BdTVELTJJZFZPSmdJOC1ON1FOU3VsWXlDb1dpRTE2WSIsImhlYWRlciI6eyJraWQiOiJIS1RBaVlNOGNFMmtLQzlLYU5NWkxZajRHUzh1V0NZTUJ4UDJpMVk5Mnp1bSIsIml2IjoiRDR0TnRIZDJyczY1RUdfQTRHQi1vMC05QmdMeERNZkgiLCJzZW5kZXIiOiJzSjdwaXU0VUR1TF9vMnBYYi1KX0pBcHhzYUZyeGlUbWdwWmpsdFdqWUZUVWlyNGI4TVdtRGR0enAwT25UZUhMSzltRnJoSDRHVkExd1Z0bm9rVUtvZ0NkTldIc2NhclFzY1FDUlBaREtyVzZib2Z0d0g4X0VZR1RMMFE9In19XX0=",
    "iv": "ZqOrBZiA-RdFMhy2",
    "ciphertext": "K7KxkeYGtQpbi-gNuLObS8w724mIDP7IyGV_aN5AscnGumFd-SvBhW2WRIcOyHQmYa-wJX0MSGOJgc8FYw5UOQgtPAIMbSwVgq-8rF2hIniZMgdQBKxT_jGZS06kSHDy9UEYcDOswtoLgLp8YPU7HmScKHSpwYY3vPZQzgSS_n7Oa3o_jYiRKZF0Gemamue0e2iJ9xQIOPodsxLXxkPrvvdEIM0fJFrpbeuiKpMk",
    "tag": "kAuPl8mwb0FFVyip1omEhQ=="
}
```

The base64URL encoded `protected` decodes to this:
```json
{
    "enc": "xchacha20poly1305_ietf",
    "typ": "JWM/1.0",
    "alg": "Authcrypt",
    "recipients": [
        {
            "encrypted_key": "L5XDhH15Pm_vHxSeraY8eOTG6RfcE2NQ3ETeVC-7EiDZyzpRJd8FW0a6qe4JfuAz",
            "header": {
                "kid": "GJ1SzoWzavQYfNL9XkaJdrQejfztN4XqdsiV4ct3LXKL",
                "iv": "a8IminstXHi54_J-Je5IWlOcNgSwD9TB",
                "sender": "ftimwiiYRG7rRQbXgJ13C5aTEQIrsWDI_bsxDqiWbTlVSKPmw6418vz3HmMlelM8AuSiKlaLCmRDI4sDFSgZIcAVXo134V8o8lFoV1BdDI7fdKOZzrKbqCixKJk="
            }
        },
        {
            "encrypted_key": "eAMiD6GDmOtzREhI-TV05_Rhippy8jwOAu5D-2IdVOJgI8-N7QNSulYyCoWiE16Y",
            "header": {
                "kid": "HKTAiYM8cE2kKC9KaNMZLYj4GS8uWCYMBxP2i1Y92zum",
                "iv": "D4tNtHd2rs65EG_A4GB-o0-9BgLxDMfH",
                "sender": "sJ7piu4UDuL_o2pXb-J_JApxsaFrxiTmgpZjltWjYFTUir4b8MWmDdtzp0OnTeHLK9mFrhH4GVA1wVtnokUKogCdNWHscarQscQCRPZDKrW6boftwH8_EYGTL0Q="
            }
        }
    ]
}
```

#### pack output format (Authcrypt mode)

``` 
    {
        "protected": "b64URLencoded({
            "enc": "xchachapoly1305_ietf",
            "typ": "JWM/1.0",
            "alg": "Authcrypt",
            "recipients": [
                {
                    "encrypted_key": base64URLencode(libsodium.crypto_box(my_key, their_vk, cek, cek_iv))
                    "header": {
                          "kid": "base58encode(recipient_verkey)",
                           "sender" : base64URLencode(libsodium.crypto_box_seal(their_vk, base58encode(sender_vk)),
                            "iv" : base64URLencode(cek_iv)
                }
            },
            ],
        })",
        "iv": <b64URLencode(iv)>,
        "ciphertext": b64URLencode(encrypt_detached({'@type'...}, protected_value_encoded, iv, cek),
        "tag": <b64URLencode(tag)>
    }
```

#### Authcrypt pack algorithm

1. generate a content encryption key (symmetrical encryption key)
2. encrypt the CEK for each recipient's public key using Authcrypt (steps below)
    1. set `encrypted_key` value to base64URLencode(libsodium.crypto_box(my_key, their_vk, cek, cek_iv))
        * Note it this step we're encrypting the cek, so it can be decrypted by the recipient
    2. set `sender` value to base64URLencode(libsodium.crypto_box_seal(their_vk, sender_vk_string))
        * Note in this step we're encrypting the sender_verkey to protect sender anonymity
    3. base64URLencode(cek_iv) and set to `iv` value in the header 
        * Note the cek_iv in the header is used for the `encrypted_key` where as `iv` is for ciphertext
3. base64URLencode the `protected` value
4. encrypt the `message` using libsodium.crypto_aead_chacha20poly1305_ietf_encrypt_detached(message, protected_value_encoded, iv, cek) this is the ciphertext.
5. base64URLencode the iv, ciphertext, and tag then serialize the format into the output format listed above.

For a reference implementation, see https://github.com/hyperledger/indy-sdk/blob/master/libindy/src/commands/crypto.rs

#### pack_message() return value (Anoncrypt mode)
This is an example of an outputted message encrypted for two verkeys using Anoncrypt.

```json
{
    "protected": "eyJlbmMiOiJ4Y2hhY2hhMjBwb2x5MTMwNV9pZXRmIiwidHlwIjoiSldNLzEuMCIsImFsZyI6IkFub25jcnlwdCIsInJlY2lwaWVudHMiOlt7ImVuY3J5cHRlZF9rZXkiOiJYQ044VjU3UTF0Z2F1TFcxemdqMVdRWlEwV0RWMFF3eUVaRk5Od0Y2RG1pSTQ5Q0s1czU4ZHNWMGRfTlpLLVNNTnFlMGlGWGdYRnZIcG9jOGt1VmlTTV9LNWxycGJNU3RqN0NSUHNrdmJTOD0iLCJoZWFkZXIiOnsia2lkIjoiR0oxU3pvV3phdlFZZk5MOVhrYUpkclFlamZ6dE40WHFkc2lWNGN0M0xYS0wifX0seyJlbmNyeXB0ZWRfa2V5IjoiaG5PZUwwWTl4T3ZjeTVvRmd0ZDFSVm05ZDczLTB1R1dOSkN0RzRsS3N3dlljV3pTbkRsaGJidmppSFVDWDVtTU5ZdWxpbGdDTUZRdmt2clJEbkpJM0U2WmpPMXFSWnVDUXY0eVQtdzZvaUE9IiwiaGVhZGVyIjp7ImtpZCI6IjJHWG11Q04ySkN4U3FNUlZmdEJITHhWSktTTDViWHl6TThEc1B6R3FRb05qIn19XX0=",
    "iv": "M1GneQLepxfDbios",
    "ciphertext": "iOLSKIxqn_kCZ7Xo7iKQ9rjM4DYqWIM16_vUeb1XDsmFTKjmvjR0u2mWFA48ovX5yVtUd9YKx86rDVDLs1xgz91Q4VLt9dHMOfzqv5DwmAFbbc9Q5wHhFwBvutUx5-lDZJFzoMQHlSAGFSBrvuApDXXt8fs96IJv3PsL145Qt27WLu05nxhkzUZz8lXfERHwAC8FYAjfvN8Fy2UwXTVdHqAOyI5fdKqfvykGs6fV",
    "tag": "gL-lfmD-MnNj9Pr6TfzgLA=="
}
```

The protected data decodes to this:

```json
{
    "enc": "xchacha20poly1305_ietf",
    "typ": "JWM/1.0",
    "alg": "Anoncrypt",
    "recipients": [
        {
            "encrypted_key": "XCN8V57Q1tgauLW1zgj1WQZQ0WDV0QwyEZFNNwF6DmiI49CK5s58dsV0d_NZK-SMNqe0iFXgXFvHpoc8kuViSM_K5lrpbMStj7CRPskvbS8=",
            "header": {
                "kid": "GJ1SzoWzavQYfNL9XkaJdrQejfztN4XqdsiV4ct3LXKL"
            }
        },
        {
            "encrypted_key": "hnOeL0Y9xOvcy5oFgtd1RVm9d73-0uGWNJCtG4lKswvYcWzSnDlhbbvjiHUCX5mMNYulilgCMFQvkvrRDnJI3E6ZjO1qRZuCQv4yT-w6oiA=",
            "header": {
                "kid": "2GXmuCN2JCxSqMRVftBHLxVJKSL5bXyzM8DsPzGqQoNj"
            }
        }
    ]
}
```

#### pack output format (Anoncrypt mode)
```
    {
         "protected": "b64URLencoded({
            "enc": "xchachapoly1305_ietf",
            "typ": "JWM/1.0",
            "alg": "Anoncrypt",
            "recipients": [
                {
                    "encrypted_key": base64URLencode(libsodium.crypto_box_seal(their_vk, cek)),
                    "header": {
                        "kid": base58encode(recipient_verkey),
                    }
                },
            ],
         })",
         "iv": b64URLencode(iv),
         "ciphertext": b64URLencode(encrypt_detached({'@type'...}, protected_value_encoded, iv, cek),
         "tag": b64URLencode(tag)
    }
```

#### Anoncrypt pack algorithm

1. generate a content encryption key (symmetrical encryption key)
2. encrypt the CEK for each recipient's public key using Anoncrypt (steps below)
    1. set `encrypted_key` value to base64URLencode(libsodium.crypto_box_seal(their_vk, cek))
        * Note it this step we're encrypting the cek, so it can be decrypted by the recipient
3. base64URLencode the `protected` value
4. encrypt the message using libsodium.crypto_aead_chacha20poly1305_ietf_encrypt_detached(message, protected_value_encoded, iv, cek) this is the ciphertext.
5. base64URLencode the iv, ciphertext, and tag then serialize the format into the output format listed above.

For a reference implementation, see https://github.com/hyperledger/indy-sdk/blob/master/libindy/src/commands/crypto.rs

### Unpack Message

#### unpack_message() inteface

unpacked_message = unpack_message(wallet_handle, jwe)

#### unpack_message() Params

- wallet_handle: wallet handle that contains the sender_verkey
- jwe: a message which was returned from a pack_message() and follows the scheme format described below


#### Unpack Algorithm

1. seralize data, so it can be used
    * For example, in rust-lang this has to be seralized as a struct.
2. Lookup the `kid` for each recipient in the wallet to see if the wallet possesses a private key associated with the public key listed
3. Check if a `sender` field is used.
    * If a sender is included use auth_decrypt to decrypt the `encrypted_key` by doing the following:
        1. decrypt sender verkey using libsodium.crypto_box_seal_open(my_private_key, base64URLdecode(sender))
        2. decrypt cek using libsodium.crypto_box_open(my_private_key, sender_verkey, encrypted_key, cek_iv)
        3. decrypt ciphertext using libsodium.crypto_aead_chacha20poly1305_ietf_open_detached(base64URLdecode(ciphertext_bytes), base64URLdecode(protected_data_as_bytes), base64URLdecode(nonce), cek)
        4. return `message`, `recipient_verkey` and `sender_verkey` following the authcrypt format listed below
    * If a sender is NOT included use anon_decrypt to decrypt the `encrypted_key` by doing the following:
        1. decrypt `encrypted_key` using libsodium.crypto_box_seal_open(my_private_key, encrypted_key)
        2. decrypt ciphertext using libsodium.crypto_aead_chacha20poly1305_ietf_open_detached(base64URLdecode(ciphertext_bytes), base64URLdecode(protected_data_as_bytes), base64URLdecode(nonce), cek)
        3. return `message` and `recipient_verkey` following the anoncrypt format listed below



For a reference implementation, see https://github.com/hyperledger/indy-sdk/blob/master/libindy/src/commands/crypto.rs

#### unpack_message() return values (authcrypt mode)

```json
{
    "message": "{ \"@id\": \"123456780\",\"@type\":\"did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/basicmessage/1.0/message\",\"sent_time\": \"2019-01-15 18:42:01Z\",\"content\": \"Your hovercraft is full of eels.\"}",
    "recipient_verkey": "HKTAiYM8cE2kKC9KaNMZLYj4GS8uWCYMBxP2i1Y92zum",
    "sender_verkey": "DWwLsbKCRAbYtfYnQNmzfKV7ofVhMBi6T4o3d2SCxVuX"
}
```

#### unpack_message() return values (anoncrypt mode)
```json
{
    "message": "{ \"@id\": \"123456780\",\"@type\":\"did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/basicmessage/1.0/message\",\"sent_time\": \"2019-01-15 18:42:01Z\",\"content\": \"Your hovercraft is full of eels.\"}",
    "recipient_verkey": "2GXmuCN2JCxSqMRVftBHLxVJKSL5bXyzM8DsPzGqQoNj"
}
```

# Additional Notes

* All `kid` values used currently are base58 encoded ed25519 keys. If other keys types are used, say secp256k1, base58 encoding should also be used here for interoperability.

* All algorithm APIs which use libsodium are from [sodiumoxide](https://crates.io/crates/sodiumoxide) rust wrapping of the original C implementation.

# Drawbacks

The current implementation of the `pack()` message is currently Hyperledger Aries specific. It is based on common crypto libraries ([NaCl](https://nacl.cr.yp.to/)), but the wrappers are not commonly used outside of Aries. There's currently work being done to fine alignment on a cross-ecosystem interoperable protocol, but this hasn't been achieved yet. This work will hopefully bridge this gap.



# Rationale and alternatives

As the [JWE](https://tools.ietf.org/html/rfc7516) standard currently stands, it does not follow this format. We're actively working with the lead writer of the JWE spec to find alignment and are hopeful the changes needed can be added.

We've also looked at using the [Message Layer Security (MLS) specification](https://datatracker.ietf.org/wg/mls/about/). This specification shows promise for adoption later on with more maturity. Additionally because they aren't hiding metadata related to the sender (Sender Anonymity), we would need to see some changes made to the specification before we could adopt this spec.

# Prior art

The [JWE](https://tools.ietf.org/html/rfc7516) family of encryption methods.

# Unresolved questions

- How transport protocols (https, zmq, etc.) will be be used to send Wire Messages?
    - These will need to be defined using seperate HIPEs. For example, HTTP might POST a message and place it in the body of the HTTP POST.
- How will the wire messages work with routing tables to pass a message through a domain, potentially over various transport protocols?
    - There's not much certainty whether routing tables or some other mechanism will be used. This needs to be defined in another HIPE.
- If the wire protocol fails, how is that failure passed back to those involved in the transmission?
    - This should be handled using the error-reporting mechanism which is currently proposed HIPE #65 by Stephen Curran.
