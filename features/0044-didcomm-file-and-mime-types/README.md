# Aries RFC 0044: DIDComm File and MIME Types

- Authors: Daniel Hardman, Kyle Den Hartog
- Status: [PROPOSED](/README.md#proposed)
- Since: 2019-05-28
- Status Note: Socialized and accepted within Indy community, and used in several implementations of protocols that want to associate a media (MIME) type with an HTTP payload. However, the Aries version of the spec changes the type names of types slightly from Indy, so the status was reset from ACCEPTED to PROPOSED. Updated in Dec 2020 to include [information about detecting DIDComm v2](#detecting-didcomm-versions).
- Supersedes: [Indy HIPE 0026]( https://github.com/hyperledger/indy-hipe/blob/master/text/0026-agent-file-format/README.md)
- Start Date: 2018-11-13
- Tags: [feature](/tags.md#feature)

## Summary

Defines the media (MIME) types and file types that hold [DIDComm]( ../../concepts/0005-didcomm/README.md) messages in encrypted, signed, and plaintext forms. Covers DIDComm V1, plus a little of [V2](https://identity.foundation/didcomm-messaging/spec/) to clarify [how DIDComm versions are detected](#detecting-didcomm-versions).

## Motivation

Most work on DIDComm so far has assumed HTTP as a transport. However, we know
that DID communication is transport-agnostic. We should be able to
say the same thing no matter which channel we use.

An incredibly important channel or transport for messages is digital files. Files
can be attached to messages in email or chat, can be carried around on a thumb
drive, can be backed up, can be distributed via CDN, can be replicated on
distributed file systems like IPFS, can be inserted in an object store or
in content-addressable storage, can be viewed and modified in editors, and
support a million other uses.

We need to define how files and attachments can contain DIDComm messages, and what the
semantics of processing such files will be.
## Tutorial

### DIDComm v1 Encrypted Envelope (*.dee)

[![dee icon](dee-small.png)](dee-big.png)

The raw bytes of an [encrypted envelope](../0019-encryption-envelope/README.md)
may be persisted to a file without any modifications whatsoever. In such a case, the data
will be encrypted and packaged such that only specific receiver(s) can process it. However,
the file will contain a JOSE-style header that can be used by magic bytes algorithms to detect
its type reliably.

The file extension associated with this filetype is `dee`, giving a globbing pattern
 of `*.dee`; this should be be read as "STAR DOT D E E" or as "D E E" files.
 
The name of this file format is "DIDComm V1 Encrypted Envelope." We expect people to say,
"I am looking at a DIDComm V1 Encrypted Envelope", or "This file is in DIDComm V1 Encrypted Envelope format", or
"Does my editor have a DIDComm V1 Encrypted Envelope plugin?"

Although the format of encrypted envelopes is derived from JSON and the JWT/JWE family
of specs, no useful processing of these files will take place by viewing them as
JSON, and viewing them as generic JWEs will greatly constrain which semantics are
applied. Therefore, the recommended MIME type for *.dee files is
`application/didcomm-enc-env`, with `application/jwe` as a fallback, and
`application/json` as an even less desirable fallback. (In this, we are making
a choice similar to the one that views `*.docx` files primarily as
`application/msword` instead of `application/xml`.) If format evolution takes
place, the version could become a parameter as [described in RFC 1341](https://www.w3.org/Protocols/rfc1341/4_Content-Type.html):
`application/didcomm-enc-env;v=2`.

A recipient using the media type value MUST treat it as if `“application/”` were prepended to any `"typ"` or `"cty"` value not containing a ‘/’ in compliance 
with the [JWE](https://tools.ietf.org/html/rfc7516) /[JWS](https://tools.ietf.org/html/rfc7515)  family of specs.

The default action for DIDComm V1 Encrypted Envelopes (what happens when a user double-clicks one)
should be `Handle` (that is, process the message as if it had just arrived by some other transport),
if the software handling the message is an agent. In other types of software,
the default action might be to view the file. Other useful actions might include
`Send`, `Attach` (to email, chat, etc), `Open with agent`, and `Decrypt to *.dp`.

>NOTE: The analog to this content type in DIDComm v2 is called a "DIDComm Encrypted Message." Its format is slightly different. For more info, see [Detecting DIDComm Versions](#detecting-didcomm-versions) below.

### DIDComm V1 Signed Envelopes (*.dse)

[![dse icon](dse-small.png)](dse-big.png)

When DIDComm messages are signed, the signing uses a JWS signing envelope. Often
signing is unnecessary, since authenticated encryption proves the sender of the
message to the recipient(s), but sometimes when non-repudiation is required, this
envelope is used. It is also required when the recipient of a message is unknown,
but tamper-evidence is still required, as in the case of a public invitation.

By convention, DIDComm Signed Envelopes contain plaintext; if encryption is used
in combination with signing, the DSE goes inside the DEE.

The file extension associated with this filetype is `dse`, giving a globbing pattern
 of `*.dse`; this should be be read as "STAR DOT D S E" or as "D S E" files.

The name of this file format is "DIDComm V1 Signed Envelope." We expect people to say,
"I am looking at a DIDComm V1 Signed Envelope", or "This file is in DIDComm V1 Signed Envelope format", or
"Does my editor have a DIDComm V1 Signed Envelope plugin?"

As with *.dee files, the best way to hande *.dse files is to map them to a custom
MIME type. The recommendation is
`application/didcomm-sig-env`, with `application/jws` as a fallback, and
`application/json` as an even less desirable fallback.

A recipient using the media type value MUST treat it as if `“application/”` were prepended to any `"typ"` or `"cty"` value not containing a ‘/’ in compliance 
with the [JWE](https://tools.ietf.org/html/rfc7516) /[JWS](https://tools.ietf.org/html/rfc7515) family of specs.

The default action for DIDComm V1 Signed Envelopes (what happens when a user double-clicks one)
should be `Validate` (that is, process the signature to see if it is valid.

>NOTE: The analog to this content type in DIDComm v2 is called a "DIDComm Signed Message." Its format is slightly different. For more info, see [Detecting DIDComm Versions](#detecting-didcomm-versions) below.

### DIDComm V1 Messages (*.dm)

[![dm icon](dm-small.png)](dm-big.png)

The plaintext representation of a DIDComm message--something like a credential
offer, a proof request, a connection invitation, or anything else worthy of a [DIDComm protocol](
../../concepts/0003-protocols/README.md)--is JSON. As such, it should be editable by anything
that expects JSON.

However, all such files have some additional conventions, over and above the simple
requirements of JSON. For example, key decorators have special meaning (
[`@id`, `~thread`](../../concepts/0008-message-id-and-threading/README.md),
[`@trace`](../0034-message-tracing/README.md)
, etc). Nonces may be especially significant. The format of particular values
such as DID and DID+key references is important. Therefore, we refer to these messages
generically as JSON, but we also define a file
format for tools that are aware of the additional semantics.

The file extension associated with this filetype is `*.dm`, and should be read as
"STAR DOT D M" or "D M" files. If a format evolution takes place, a subsequent version could be
noted by appending a digit, as in `*.dm2` for second-generation `dm` files.

The name of this file format is "DIDComm V1 Message." We expect people to say,
"I am looking at a DIDComm V1 Message", or "This file is in DIDComm V1 Message format", or
"Does my editor have a DIDComm V1 Message plugin?" For extra clarity, it is acceptable
to add the adjective "plaintext", as in "DIDComm V1 Plaintext Message."

The most specific MIME type of *.dm files is `application/json;flavor=didcomm-msg`--or, if more generic handling is appropriate, just 
`application/json`.

A recipient using the media type value MUST treat it as if `“application/”` were prepended to any `"typ"` or `"cty"` value not containing a ‘/’ in compliance 
with the [JWE](https://tools.ietf.org/html/rfc7516) /[JWS](https://tools.ietf.org/html/rfc7515) family of specs.

The default action for DIDComm V1 Messages should be to
`View` or `Validate` them. Other interesting actions might be `Encrypt to *.dee`,
`Sign to *.dse`, and `Find definition of protocol`.

>NOTE: The analog to this content type in DIDComm v2 is called a "DIDComm Plaintext Message." Its format is slightly different. For more info, see [Detecting DIDComm Versions](#detecting-didcomm-versions) below.

As a general rule, DIDComm messages that are being sent in production use cases of DID communication should be stored
in encrypted form (`*.dee`) at rest. There are cases where this might not be preferred, e.g., providing documentation of the
format of message or during a debugging scenario using
[message tracing](../0034-message-tracing/README.md).
However, these are exceptional cases. Storing meaningful `*.dm` files
decrypted is not a security best practice, since it replaces all the privacy and
security guarantees provided by the DID communication mechanism with only
the ACLs and other security barriers that are offered by the container.

### Native Object representation

This is not a file format, but rather an in-memory form of a DIDComm Message
using whatever object hierarchy is natural for a programming language to map to and from
JSON. For example, in python, the natural Native Object format is a dict that contains properties
indexed by strings. This is the representation that python's `json` library expects when
converting to JSON, and the format it produces when converting from JSON. In Java, Native
Object format might be a bean. In C++, it might be a `std::map<std::string, variant>`...

There can be more than one Native Object representation for a given programming language.

Native Object forms are never rendered directly to files; rather, they are serialized to DIDComm Plaintext Format
and then persisted (likely after also encrypting to DIDComm V1 Encrypted Envelope).

### Detecting DIDComm Versions

Because media types differ from DIDComm V1 to V2, and because media types are easy to communicate in headers and message fields, they are a convenient way to detect which version of DIDComm applies in a given context:

Nature of Content | V1 | V2
--- | --- | ---
encrypted| `application/didcomm-enc-env`<br>DIDComm V1 Encrypted Envelope<br>*.dee | `application/didcomm-encrypted+json`<br>DIDComm Encrypted Message<br>*.dcem
signed| `application/didcomm-sig-env`<br>DIDComm V1 Signed Envelope<br>*.dse | `application/didcomm-signed+json`<br>DIDComm Signed Message<br>*.dcsm
plaintext| `application/json;flavor=didcomm-msg`<br>DIDComm V1 Message<br>*.dm | `application/didcomm-plain+json`<br>DIDComm Plaintext Message<br>*.dcpm

It is also recommended that agents implementing [Discover Features Protocol v2](../0557-discover-features-v2/README.md) respond to [queries about supported DIDComm versions](../0557-discover-features-v2/README.md#queries-message-type) using the `didcomm-version` feature name. This allows queries about what an agent is willing to support, whereas the media type mechanism describes what is in active use. The values that should be returned from such a query are URIs that tell where DIDComm versions are developed:

Version | URI
--- | ---
V1 | https://github.com/hyperledger/aries-rfcs
V2 | https://github.com/decentralized-identity/didcomm-messaging

### What it means to "implement" this RFC

For the purposes of [Aries Interop Profiles](../../concepts/0302-aries-interop-profile/README.md), an agent "implements" this RFC when:

* If it encounters references to DIDComm V1 media types (e.g., in HTTP headers, in attachments, or in the fields of DIDComm messages where a media type is expected), it imputes the meaning documented here.
* If it characterizes DIDComm V1 content in its own outbound communication or UI, it does so with the media type strings, friendly names, and file extensions documented here.

## Reference

The file extensions and MIME types described here are also accompanied by suggested graphics.
[Vector forms of these graphics are available](
https://docs.google.com/presentation/d/1QmKxuMz8KnqYbdGUEOaNqLtZSCZryQrwj9RRXMN4uAk/edit#slide=id.p).

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

Name / Link | Implementation Notes
--- | ---
 |  |
