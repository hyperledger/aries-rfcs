# Aries RFC 0360: did:key Usage

- Authors: [Tobias Looker](tobias.looker@mattr.global), [Stephen Curran](mailto:swcurran@cloudcompass.ca)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2019-12-17
- Status Note: Socialized with mixed support; did:key method is a [W3C CCG work item](https://w3c-ccg.github.io/community/work_items.html)
- Supersedes:
- Start Date: 2019-12-17
- Tags: feature

## Summary

A number of RFCs that have been defined reference what amounts to a "naked" public key, such that the sender relies on the receiver knowing what type the key is and how it can be used. The application of this RFC will result in the replacement of "naked" verkeys (public keys) in some DIDComm/Aries protocols with the [did:key](https://digitalbazaar.github.io/did-method-key/) ledgerless DID method, a format that concisely conveys useful information about the use of the key, including the public key type. While `did:key` is less a DID method than a transformation from a public key and type to an opinionated DIDDoc, it provides a versioning mechanism for supporting new/different cryptographic formats and its use makes clear how a public key is intended to be used. The method also enables support for using standard [DID resolution](https://w3c-ccg.github.io/did-resolution/) mechanisms that may simplify the use of the key. The use of a DID to represent a public key is seen as odd by some in the community. Should a representation be found that is has better properties than a plain public key but is constrained to being "just a key", then we will consider changing from the `did:key` representation.

> To Do: Update link DID Key Method link (above) from Digital Bazaar to W3C repositories when they are created and populated.

While it is well known in the Aries community that `did:key` is fundamentally different from the [did:peer](https://identity.foundation/peer-did-method-spec/index.html) method that is the basis of Aries protocols, it must be re-emphasized here. This RFC does **NOT** imply any changes to the use of `did:peer` in Aries, nor does it change the content of a `did:peer` DIDDoc. This RFC only changes references to plain public keys in the JSON of some RFCs to use `did:key` in place of a plain text string.

Should this RFC be [ACCEPTED](/README.md#accepted), a [community coordinated update](../../concepts/0345-community-coordinated-update/README.md) will be used to apply updates to the agent code bases and impacted RFCs.

## Motivation

When one Aries agent inserts a public key into the JSON of an Aries message (for example, the `~service` decorator), it assumes that the recipient agent will use the key in the intended way. At the time this RFC is being written, this is easy because only one key type is in use by all agents. However, in order to enable the use of different cryptography algorithms, the public references must be extended to at least include the key type. The preferred and concise way to do that is the use of the [multicodec](https://github.com/multiformats/multicodec) mechanism, which provides a registry of encodings for known key types that are prefixed to the public key in a standard and concise way. [did:key](https://digitalbazaar.github.io/did-method-key) extends that mechanism by providing a templated way to transform the combination of public key and key type into a [DID-standard DIDDoc](https://digitalbazaar.github.io/did-method-key/#example-2-a-did-document-derived-from-a-did-key).

At the cost of adding/building a did:key resolver we get a DID standard way to access the key and key type, including specific information on how the key can be used. The resolver may be trivial or complex. In a trivial version, the key type is assumed, and the key can be easily extracted from the string. In a more complete implementation, the key type can be checked, and standard DID URL handling can be used to extract parts of the DIDDoc for specific purposes. For example, in the [ed25519 `did:key` DIDDoc](https://digitalbazaar.github.io/did-method-key/#example-2-a-did-document-derived-from-a-did-key), the existence of the `keyAgreement` entry implies that the key can be used in a Diffie-Hellman exchange, without the developer guessing, or using the key incorrectly.

Note that simply knowing the key type is not necessarily sufficient to be able to use the key. The cryptography supporting the processing data using the key must also be available in the agent. However, the multicodec and did:key capabilities will simplify adding support for new key types in the future.

## Tutorial

An example of the use of the replacement of a verkey with `did:key` can be found in the [~service decorator RFC](https://github.com/hyperledger/aries-rfcs/tree/master/features/0056-service-decorator). Notably in the example at the beginning of the [tutorial](https://github.com/hyperledger/aries-rfcs/tree/master/features/0056-service-decorator#tutorial) section, the verkeys in the `recipientKeys` and `routingKeys` items would be changed from native keys to use `did:key` as follows:

``` jsonc
{
    "@type": "somemessagetype",
    "~service": {
        "recipientKeys": ["did:key:z6MkmjY8GnV5i9YTDtPETC2uUAW6ejw3nk5mXF5yci5ab7th"],
        "routingKeys": ["did:key:z6MkmjY8GnV5i9YTDtPETC2uUAW6ejw3nk5mXF5yci5ab7th"]
        "serviceEndpoint": "https://example.com/endpoint"
    }
}
```

Thus, `8HH5gYEeNc3z7PYXmd54d4x6qAfCNrqQqEB3nS7Zfu7K` becomes `did:key:z6MkmjY8GnV5i9YTDtPETC2uUAW6ejw3nk5mXF5yci5ab7th` using the following transformations:

- Start with the original (presumably) base58 ed25519 public key
  - Since we have only a naked public key, we must assume the format
- Base58 decode the public key to get the hex version
- Multicodec: Prefix with the algorithm type. In this case, `ED01` as the key type is ed25519.
- Multibase: Base58 encode the result and prefix that with "z" to indicate base58 encoding
- DID: Prefix that with the DID Method prefix `did:key:`

The transformation above is **only for illustration within this RFC**. The [`did:key`](https://digitalbazaar.github.io/did-method-key) specification is the definitive source for the appropriate transformations.

The `did:key` method uses the strings that are the DID, public key and key type to construct ("resolve") a DIDDoc based on a template defined by the `did:key` specification. Further, the `did:key` resolver generates, in the case of an ed25519 public signing key, a key that can be used as part of a Diffie-Hellman exchange appropriate for encryption in the `keyAgreement` section of the DIDDoc. Presumably, as the `did:key` method supports other key types, similar DIDDoc templates will become part of the specification. Key types that don't support a signing/key exchange transformation would not have a `keyAgreement` entry in the resolved DIDDoc.

The following currently implemented RFCs would be affected by acceptance of this RFC. In these RFCs, the JSON items that currently contain naked public keys (mostly the items `recipientKeys` and `routingKeys`) would be changed to use `did:key` references where applicable. Note that in these items public DIDs could also be used if applicable for a given use case.

- [0023-did-exchange](https://github.com/hyperledger/aries-rfcs/tree/master/features/0023-did-exchange) - Invitation Message
- [0028-introduce](https://github.com/hyperledger/aries-rfcs/tree/master/features/0028-introduce)
- [0056-service-decorator](https://github.com/hyperledger/aries-rfcs/tree/master/features/0056-service-decorator)
- [0160-connection-protocol](https://github.com/hyperledger/aries-rfcs/tree/master/features/0160-connection-protocol)

Service entries in `did:peer` DIDDocs (such as in RFCs
[0094-cross-domain-messaging](https://github.com/hyperledger/aries-rfcs/tree/master/concepts/0094-cross-domain-messaging)
and
[0067-didcomm-diddoc-conventions](https://github.com/hyperledger/aries-rfcs/tree/master/features/0067-didcomm-diddoc-conventions))
should **NOT** use a `did:key` public key representation. Instead, service
entries in the DIDDoc should reference keys defined internally in the DIDDoc
where appropriate.

> To Do: Discuss the use of `did:key` (or not) in the context of [encryption envelopes](../0019-encryption-envelope/README.md). This will be part of the ongoing discussion about [JWEs](https://tools.ietf.org/html/rfc7516) and the upcoming discussions about JWMs&mdash;a soon-to-be-proposed specification. That conversation will likely go on in the DIF DIDComm Working Group.

## Reference

See the [`did:key`](https://digitalbazaar.github.io/did-method-key) specification. Note that the specification is still evolving.

## Drawbacks

The `did:key` standard is not finalized.

The DIDDoc "resolved" from a `did:key` probably has more entries in it than are needed for DIDComm. That said, the entries in the DIDDoc make it clear to a developer how they can use the public key.

## Rationale and alternatives

We should not stick with the status quo and assume that all agents will always know the type of keys being used and how to use them.

We should at minimum move to a scheme like multicodecs such that the key is self documenting and supports the versioning of cryptographic algorithms. However, even if we do that, we still have to document for developers how they should (and not should not) use the public key.

Another logical alternative is to use a [JWK](https://tools.ietf.org/html/rfc7517). However, that representation only adds the type of the key (same as multicodecs) at the cost of being significantly more [verbose](https://tools.ietf.org/html/rfc7517#section-3).

## Prior art

> To do - there are other instances of this pattern being used. Insert those here.

## Unresolved questions

- How to transition to the use of `did:key`.
- What will the initial accepted version of `did:key` look like?  It's probably close to its final form, with an expected resolution of the open question of what  a DIDDoc looks like if the key type is not ed25519.

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

*Implementation Notes*

Name / Link | Implementation Notes
--- | ---
 | 
