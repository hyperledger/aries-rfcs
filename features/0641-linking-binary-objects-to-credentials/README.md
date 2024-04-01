# 0641: Linking binary objects to credentials using hash based references

- Authors: [Berend Sliedrecht](mailto:berend@animo.id) (Animo Solutions)
- Status: [STALLED](/README.md#stalled)
- Since: 2024-04-03
- Status Note: No implementations have been created.
- Start Date: 2021-03-17
- Tags: [feature](/tags.md#feature), [credentials](/tags.md#credentials)

## Summary

This RFC provides a solution for issuing and presenting credentials with external binary objects, after referred to as attachments. It is compatible with [0036: Issue Credential Protocol V1](https://github.com/hyperledger/aries-rfcs/tree/main/features/0036-issue-credential), [0453: Issue Credential Protocol V2](https://github.com/hyperledger/aries-rfcs/tree/main/features/0453-issue-credential-v2), [0037: Present Proof V1 protocol](https://github.com/hyperledger/aries-rfcs/tree/main/features/0037-present-proof) and [0454: Present Proof V2 Protocol](https://github.com/hyperledger/aries-rfcs/tree/main/features/0454-present-proof-v2). These external attachments could consist of images, PDFs, zip files, movies, etc. Through the use of `DIDComm attachments`, [0017: Attachments](https://github.com/hyperledger/aries-rfcs/tree/main/concepts/0017-attachments), the data can be embedded directly into the attachment or externally hosted. In order to maintain integrity over these attachments, hashlinks are used as the checksum.

## Motivation

Many use cases, such as a rental agreement or medical data in a verifiable credential, rely on attachments, small or large. At this moment, it is possible to issue credentials with accompanying attachments. When the attachment is rather small, this will work fine. However, larger attachments cause inconsistent timing issues and are resource intensive.

## Tutorial

It is already possible to issue and verify base64-encoded attachments in credentials. When a credential is getting larger and larger, it becomes more and more impractical as it has to be signed, which is time consuming and resource intensive. A solution for this is to use the attachments decorator. This decorator creates a way to externalize the attachment from the credential attributes. By allowing this, the signing will be faster and more consistent. However, DIDComm messages SHOULD stay small, like with SMTP or Bluetooth, as specified in [0017: Attachments](https://github.com/hyperledger/aries-rfcs/tree/main/concepts/0017-attachments). In the attachments decorator it is also possible to specify a list of URLs where the attachment might be located for download. This list of URLs is accompanied by a `sha256` tag that is a checksum over the file to maintain integrity. This `sha256` tag can only contain a sha256 hash and if another algorithm is preferred then the hashlink MUST be used as the checksum.

When issuing and verifying a credential, messages have to be sent between the holder, issuer and verifier. In order to circumvent additional complexity, such as looking at previously sent credentials for the attachment, the attachments decorator, when containing an attachment, MUST be sent at all of the following steps:

**Issue Credential V1 & V2**

1. Credential Proposal
2. Credential Offer
3. Credential Request
4. Credential

**Present Proof V1 & V2**

1. Presentation Proposal
2. Presentation Request
3. Presentation

### Linking

When a credential is issued with an attachment in the attachments decorator, be it a base64-encoded file or a hosted file, the link has to be made between the credential and the attachment. The link MUST be made with the `attribute.value` of the credential and the `@id` tag of the attachment in the attachments decorator.

### Hashlink

A hashlink, as specified in [IETF: Cryptographic Hyperlinks](https://tools.ietf.org/html/draft-sporny-hashlink-06), is a formatted hash that has a prefix of `hl:` and an optional suffix of metadata. The hash in the hashlink is a [multihash](https://tools.ietf.org/html/draft-multiformats-multihash-02), which means that according to the prefix of the hash it is possible to see which hashing algorithm and encoding algorithm has been chosen. An example of a hashlink would be:

`hl:zQmcWyBPyedDzHFytTX6CAjjpvqQAyhzURziwiBKDKgqx6R`

This example shows the prefix of `hl:` indicating that it is a hashlink and the hash after the prefix is a multihash.

The hashlink also allows for opional metadata, such as; a list of URLs where the attachment is hosted and a MIME-type. These metadata values are encoded in the CBOR data format using the specified algortihm from section 3.1.2 in the [IETF: Cryptographic Hyperlinks](https://tools.ietf.org/html/draft-sporny-hashlink-06).

When a holder receives a credential with hosted attachments, the holder MAY rehost these attachments. A holder would do this in order to prevent the phone-home problem. If a holder does not care about this issue, this is use case specific, this can be left out but should be considered.

### Inlined Attachments as a Credential Attribute

Attachments can be inlined in the credential attribute as a base64-encoded string. With this, there is no need for the attachment decorator. Below is an example of embedding a base64-encoded file as a string in a credential attribute.

```json
{
  "name": "Picture of a cat",
  "mime-type": "image/png",
  "value": "VGhpcyBpc ... (many bytes omitted) ... C4gSG93IG5pY2U="
}
```

### Attachments inlined in the Attachment Decorator

When the attachments decorator is used to issue a credential with a binary object, a link has to be made between the credential value and the corresponding attachment. This link MUST be a hash, specifically a hashlink based on the checksum of the attachment.

As stated in [0008: message id and threading](https://github.com/hyperledger/aries-rfcs/blob/main/concepts/0008-message-id-and-threading/README.md), the `@id` tag of the attachment MUST NOT contain a colon and MUST NOT be longer than 64 characters. because of this, the `@id` can not contain a hashlink and MUST contain the multihash with a maximum length of 64 characters. When a hash is longer than 64 character, use the first 64 characters.

```json
{
  "@type": "https://didcomm.org/issue-credential/%VER/issue-credential",
  "@id": "<uuid of issue message>",
  "goal_code": "<goal-code>",
  "replacement_id": "<issuer unique id>",
  "comment": "<some comment>",
  "formats": [
    {
      "attach_id": "<attach@id value>",
      "format": "hlindy/cred@v2.0"
    }
  ],
  "credentials~attach": [
    {
      "@id": "<attachment-id>",
      "mime-type": "application/json",
      "data": {
        "json": {
          "schema_id": "4RW6QK2HZhHxa2tg7t1jqt:2:catSchema:0.3.0",
          "cred_def_id": "4RW6QK2HZhHxa2tg7t1jqt:3:CL:58161:default",
          "values": {
            "pictureOfACat": {
              "raw": "hl:zQmcWyBPyedDzHFytTX6CAjjpvqQAyhzURziwiBKDKgqx6R",
              "encoded": "hl:zQmcWyBPyedDzHFytTX6CAjjpvqQAyhzURziwiBKDKgqx6R"
            }
          },
          "signature": "<signature>",
          "signature_correctness_proof": "<signature_correctness_proof>"
        }
      }
    }
  ],
  "~attach": [
    {
      "@id": "zQmcWyBPyedDzHFytTX6CAjjpvqQAyhzURziwiBKDKgqx6R",
      "mime-type": "image/png",
      "filename": "cat.png",
      "byte_count": 2181,
      "lastmod_time": "2021-04-20 19:38:07Z",
      "description": "Cute picture of a cat",
      "data": {
        "base64": "VGhpcyBpcyBhIGNv ... (many bytes omitted) ... R0ZXIgU0hJQkEgSU5VLg=="
      }
    }
  ]
}
```

## Hosted attachments

The last method of adding a binary object in a credential is by using the attachments decorator in combination with external hosting. In the example below the attachment is hosted at two locations. These two URLs MUST point to the same file and match the integrity check with the `sha256` value. It is important to note that when an issuer hosts an attachment, and issues a credential with this attachment, that the holder rehosts this attachment to prevent the phone-home assosiation.

```json
{
  "@type": "https://didcomm.org/issue-credential/%VER/issue-credential",
  "@id": "<uuid of issue message>",
  "goal_code": "<goal-code>",
  "replacement_id": "<issuer unique id>",
  "comment": "<some comment>",
  "formats": [
    {
      "attach_id": "<attach@id value>",
      "format": "hlindy/cred@v2.0"
    }
  ],
  "credentials~attach": [
    {
      "@id": "<attachment-id>",
      "mime-type": "application/json",
      "data": {
        "json": {
          "schema_id": "4RW6QK2HZhHxa2tg7t1jqt:2:catSchema:0.3.0",
          "cred_def_id": "4RW6QK2HZhHxa2tg7t1jqt:3:CL:58161:default",
          "values": {
            "pictureOfACat": {
              "raw": "hl:zQmcWyBPyedDzHFytTX6CAjjpvqQAyhzURziwiBKDKgqx6R",
              "encoded": "hl:zQmcWyBPyedDzHFytTX6CAjjpvqQAyhzURziwiBKDKgqx6R"
            }
          },
          "signature": "<signature>",
          "signature_correctness_proof": "<signature_correctness_proof>"
        }
      }
    }
  ],
  "~attach": [
    {
      "@id": "zQmcWyBPyedDzHFytTX6CAjjpvqQAyhzURziwiBKDKgqx6R",
      "mime-type": "application/zip",
      "filename": "cat.zip",
      "byte_count": 218187322,
      "lastmod_time": "2021-04-20 19:38:07Z",
      "description": "Cute pictures of multiple cats",
      "data": {
        "links": [
          "https://drive.google.com/kitty/cats.zip",
          "s3://bucket/cats.zip"
        ]
      }
    }
  ]
}
```

### Matching

Now that a link has been made between the attachment in the attachments decorator, it is possible to match the two together. When a credential is received and a value of an attribute starts with `hl:` it means that there is a linked attachment. To find the linked attachment to the credential attribute to following steps SHOULD be done:

1. Extract the multihash from the credential attribute value
2. Extract the first 64 characters of this multihash
3. Loop over the `@id` tag of all the attachments in the attachment decorator
4. Compare the value of the `@id` tag with the multihash
5. If the `@id` tag matches with the multihash, then there is a link
6. An integrity check can be done with the original, complete hashlink

## Reference

When an issuer creates a value in a credential attribute with a prefix of `hl:`, but there is no attachment, a warning SHOULD be thrown.

When DIDcomm V2 is implemented the attachment decorator will not contain the `sha256` tag anymore and it will be replaced by `hash` to allow for any algorithm. [DIDcomm messaging Attachments](https://identity.foundation/didcomm-messaging/spec/#reference-2)

## Drawbacks

- Hashlinks, multibase and multihash are not confirmed IETF RFCs yet
- Hosting some files at third party locations is not preferred

## Rationale and alternatives

The findings that large credentials are inconsistent and resource intensive are derived from issuing and verifying credentials of 100 kilobytes to 50 megabytes in Aries Framework JavaScript and Aries Cloudagent Python.

The Identity Foundation is currently working on confidential storage, a way to allow access to your files based on DIDs. This storage would be a sleek fix for the last drawback.

## Prior art

- [0017: Attachments](https://github.com/hyperledger/aries-rfcs/tree/main/concepts/0017-attachments) discusses the attachments in DIDcomm messaging and formulates the attachment decorator.
- [HIPE-0139: Image As Attribute Via Aries-0036 Issue-Credential Protocol](https://github.com/hyperledger/indy-hipe/blob/main/text/0139-image-as-cred-attr/README.md) has been written for the support of images in credentials. It points out that the attachment RFC and the issue credential RFC are separate and could drift apart.
- [Linking and Exchanging Attachments with Verifiable Credentials](https://sovrin.org/interoperability-series-linking-and-exchanging-attachments-with-verifiable-credentials/) describes the linking between the attachment the credential based on the `@id` tag.

## Unresolved questions

- N/A

## Implementations

| Name / Link | Implementation Notes |
| ----------- | -------------------- |
