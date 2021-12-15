# 0646: W3C Credential Exchange using BBS+ Signatures

- Authors: [Timo Glastra](mailto:timo@animo.id) (Animo Solutions), [Brent Zundel](mailto:brent.zundel@evernym.com) (Evernym)
- Status: [ACCEPTED](/README.md#accepted)
- Since: 2021-04-28
- Status Note:
- Supersedes:
- Start Date: 2021-04-15
- Tags: [feature](/tags.md#feature)

## Summary

This RFC describes how the Hyperledger Aries community should use [BBS+ Signatures](https://w3c-ccg.github.io/ldp-bbs2020/) that conform with the [Linked-Data Proofs Specification](https://w3c-ccg.github.io/ld-proofs/) to perform exchange of credentials that comply with the [W3C Verifiable Credential specification](https://www.w3.org/TR/vc-data-model/).

Key features include:

- zero-knowledge proofs (ZKPs),
- selective disclosure,
- private holder binding,
- signature blinding,
- compatibility with privacy preserving revocation.

This RFC sets guidelines for their safe usage and describes privacy-enabling features that should be incorporated.

The usage of zero-knowledge proofs, selective disclosure and signature blinding are already supported using the specifications as described in this document. Support for private holder binding and privacy preserving revocation will be added in the future.

## Motivation

Aries currently supports credential formats used by Indy (Anoncreds based on JSON) and Aries-Framework-Go. BBS+ signatures with JSON-LD Proofs provide a unified credential format that includes strong privacy protecting anti-correlation features and wide interoperability with verifiable credentials outside the Aries ecosystem.

## Tutorial

### Issuing Credentials

This section highlights the process of issuing credentials with BBS+ signatures. The first section ([Creating BBS+ Credentials](#creating-bbs-credentials)) highlights the process of **creating** credentials with BBS+ signatures, while the next section focusses on the the process of **exchanging** credentials with BBS+ signatures ([Exchanging BBS+ Credentials](#exchanging-bbs-credentials)).

#### Creating BBS+ Credentials

The process to create verifiable credentials with BBS+ signatures is mostly covered by the [VC Data Model](https://www.w3.org/TR/vc-data-model) and [BBS+ LD-Proofs](https://w3c-ccg.github.io/ldp-bbs2020) specifications. At the date of writing this RFC, the BBS+ LD-Proofs specification still has some unresolved issues. The issues are documented in the [Issues with the BBS+ LD-Proofs specification](#issues-with-the-bbs-ld-proofs-specification) section below.

Aries implementations MUST use the [BBS+ Signature Suite 2020](https://w3c-ccg.github.io/ldp-bbs2020/#the-bbs-signature-suite-2020) to create verifiable credentials with BBS+ signatures, identified by the `BbsBlsSignature2020` proof type.

> NOTE: Once the signature suites for bound signatures (private holder binding) are defined in the [BBS+ LD-Proofs](https://w3c-ccg.github.io/ldp-bbs2020) spec, the use of the `BbsBlsSignature2020` suite will be deprecated and superseded by the `BbsBlsBoundSignature2020` signature suite. See [Private Holder Binding](#private-holder-binding) below for more information.

##### Identifiers in Issued Credentials

It is important to note that due to limitations of the underlying RDF canonicalization scheme, which is used by [BBS+ LD-Proofs](https://w3c-ccg.github.io/ldp-bbs2020/), issued credentials SHOULD NOT have any `id` properties, as the value of these properties will be revealed during the RDF canonicalization process, regardless of whether or not the holder chooses to disclose them.

Credentials can make use of other identifier properties to create selectively disclosable identifiers. An example of this is the `identifier` property from the [Citizenship Vocabulary](https://w3c-ccg.github.io/citizenship-vocab/#identifier)

##### Private Holder Binding

A private holder binding allows the holder of a credential to authenticate itself without disclosing a correlating identifier (such as a DID) to the verifier. The current [BBS+ LD-Proofs](https://w3c-ccg.github.io/ldp-bbs2020/) specification does not describe a mechanism yet to do private holder binding, but it is expected this will be done using two new signature suites: `BbsBlsBoundSignature2020` and `BbsBlsBoundSignatureProof2020`. Both suites feature a commitment to a private key held by the credential holder, for which they prove knowledge of when deriving proofs without ever directly revealing the private key, nor a unique identifier linked to the private key (e.g its complementary public pair).

##### Usage of Credential Schema

The [zero-knowledge proof section](https://www.w3.org/TR/vc-data-model/#zero-knowledge-proofs) of the VC Data Model requires verifiable credentials used in zero-knowledge proof systems to include a credential definition using the `credentialSchema` property. Due to the nature of how BBS+ LD proofs work, it is NOT required to include the `credentialSchema` property. See [Issue 726](https://github.com/w3c/vc-data-model/issues/726) in the VC Data Model.

##### Example BBS+ Credential

Below is a complete example of a Verifiable Credential with BBS+ linked data proof.

```jsonc
{
  "@context": [
    "https://www.w3.org/2018/credentials/v1",
    "https://w3id.org/citizenship/v1",
    "https://w3id.org/security/bbs/v1" // <-- BBS+ context
  ],
  "id": "https://issuer.oidp.uscis.gov/credentials/83627465",
  "type": ["VerifiableCredential", "PermanentResidentCard"],
  "issuer": "did:example:489398593",
  "identifier": "83627465", // <-- `identifier` property allows for seletively disclosable id property
  "name": "Permanent Resident Card",
  "description": "Government of Example Permanent Resident Card.",
  "issuanceDate": "2019-12-03T12:19:52Z",
  "expirationDate": "2029-12-03T12:19:52Z",
  "credentialSubject": {
    "id": "did:example:b34ca6cd37bbf23",
    "type": ["PermanentResident", "Person"],
    "givenName": "JOHN",
    "familyName": "SMITH",
    "gender": "Male",
    "image": "data:image/png;base64,iVBORw0KGgokJggg==",
    "residentSince": "2015-01-01",
    "lprCategory": "C09",
    "lprNumber": "999-999-999",
    "commuterClassification": "C1",
    "birthCountry": "Bahamas",
    "birthDate": "1958-07-17"
  },
  "proof": {
    "type": "BbsBlsSignature2020", // <-- type must be `BbsBlsSignature2020`
    "created": "2020-10-16T23:59:31Z",
    "proofPurpose": "assertionMethod",
    "proofValue": "kAkloZSlK79ARnlx54tPqmQyy6G7/36xU/LZgrdVmCqqI9M0muKLxkaHNsgVDBBvYp85VT3uouLFSXPMr7Stjgq62+OCunba7bNdGfhM/FUsx9zpfRtw7jeE182CN1cZakOoSVsQz61c16zQikXM3w==",
    "verificationMethod": "did:example:489398593#test"
  }
}
```

#### Exchanging BBS+ Credentials

While the process of creating credentials with BBS+ signatures is defined in specifications outside of Aries, the process of exchanging credentials with BBS+ signatures is defined within Aries.

Credentials with BBS+ signatures can be exchanged by following [RFC 0453: Issue Credential Protocol 2.0](https://github.com/hyperledger/aries-rfcs/tree/main/features/0453-issue-credential-v2). The Issue Credential 2.0 provides a registry of attachment formats that can be used for credential exchange. Currently, agents are expected to use the format as described in RFC 0593 (see below).

> NOTE: Once [Credential Manifest](https://identity.foundation/credential-manifest/) v1.0 is released, RFC 0593 is expected to be deprecated and replaced by an updated version of [RFC 0511: Credential-Manifest Attachment format](https://github.com/hyperledger/aries-rfcs/blob/main/features/0511-dif-cred-manifest-attach/README.md)

##### 0593: JSON-LD Credential Attachment format

[RFC 0593: JSON-LD Credential Attachment format for requesting and issuing credentials](https://github.com/hyperledger/aries-rfcs/blob/main/features/0593-json-ld-cred-attach/README.md) defines a very simple, feature-poor attachment format for issuing JSON-LD credentials.

The only requirement for exchanging BBS+ credentials, in addition to the requirements as specified in [Creating BBS+ Credentials](#creating-bbs-credentials) and [RFC 0593](https://github.com/hyperledger/aries-rfcs/blob/main/features/0593-json-ld-cred-attach/README.md), is the `options.proofType` in the [`ld-proof-vc-detail`](https://github.com/hyperledger/aries-rfcs/blob/main/features/0593-json-ld-cred-attach/README.md#ld-proof-vc-detail-attachment-format) MUST be `BbsBlsSignature2020`.

### Presenting Derived Credentials

This section highlights the process of creating and presenting derived BBS+ credentials containing a BBS+ proof of knowledge.

#### Deriving Credentials

Deriving credentials should be done according to the [BBS+ Signature Proof Suite 2020](https://w3c-ccg.github.io/ldp-bbs2020/#the-bbs-signature-proof-suite-2020)

##### Disclosing Required Properties

> A verifiable presentation MUST NOT leak information that would enable the verifier to correlate the holder across multiple verifiable presentations.

The above section from the VC Data Model may give the impression that it is allowed to omit required properties from a derived credential if this prevents correlation. However things the holder chooses to reveal are in a different category than things the holder MUST reveal. Derived credentials MUST disclose required properties, even if it can correlate them.

E.g. a credential with `issuanceDate` of `2017-12-05T14:27:42Z` could create a correlating factor. However it is against the VC Data Model to not include the property. Take this into account when issuing credentials.

##### Transforming Blank Node Identifiers

> This section will be removed once [Issue 10](https://github.com/w3c-ccg/ldp-bbs2020/issues/10) in the LD Proof BBS+ spec is resolved.

For the verifier to be able to verify the signature of a derived credential it should be able to deterministically normalize the credentials statements for verification. RDF Dataset Canonicalization defines a way in which to allocate identifiers for blank nodes deterministically for normalization. However, the algorithm does not guarantee that the same blank node identifiers will be allocated in the event of modifications to the graph. Because selective disclosure of signed statements modifies the graph as presented to the verifier, the blank node identifiers must be transformed into actual node identifiers when presented to the verifier.

The [BBS+ LD-Proofs](https://w3c-ccg.github.io/ldp-bbs2020) specification does not define a mechanism to transform blank node identifiers into actual identifiers. Current implementations use the mechanism as described in this [Issue Comment](https://github.com/w3c-ccg/ldp-bbs2020/issues/10#issuecomment-616216278). Some reference implementations:

- [Aries Framework Go](https://github.com/hyperledger/aries-framework-go/blob/d83e137/pkg/doc/signature/jsonld/processor.go#L451-L452)
- [JSON-LD Signatures BBS](https://github.com/mattrglobal/jsonld-signatures-bbs/blob/01000b4bf48932a47d7c8c889d2201f8e8085d46/src/BbsBlsSignatureProof2020.ts#L116-L132)
- [Aries Cloud Agent Python](https://github.com/hyperledger/aries-cloudagent-python/blob/eb3fd94ffaf623e4207ec1c8cb140345a489599d/aries_cloudagent/vc/ld_proofs/suites/BbsBlsSignatureProof2020.py#L314-L345)

#### Verifying Presented Derived Credentials

##### Transforming Back into Blank Node Identifiers

> This section will be removed once [Issue 10](https://github.com/w3c-ccg/ldp-bbs2020/issues/10) in the LD Proof BBS+ spec is resolved.

Transforming the blank node identifiers into actual node identifiers in the derived credential means the verification data will be different from the verification data at issuance, invalidating the signature. Therefore the blank node identifier placeholders should be transformed back into blank node identifiers before verification.

Same as with [Transforming Blank Node Identifiers](#transforming-blank-node-identifiers), current implementations use the mechanism as described in this [Issue Comment](https://github.com/w3c-ccg/ldp-bbs2020/issues/10#issuecomment-616216278). Some reference implementations:

- [Aries Framework Go](https://github.com/hyperledger/aries-framework-go/blob/b1b076db898fe8c922c6dc093d3fa52d448f0c30/pkg/doc/signature/verifier/public_key_verifier.go#L434)
- [JSON-LD Signatures BBS](https://github.com/mattrglobal/jsonld-signatures-bbs/blob/01000b4bf48932a47d7c8c889d2201f8e8085d46/src/BbsBlsSignatureProof2020.ts#L254-L267)
- [Aries Cloud Agent Python](https://github.com/hyperledger/aries-cloudagent-python/blob/main/aries_cloudagent/vc/ld_proofs/suites/BbsBlsSignatureProof2020.py#L347-L381)

#### Exchanging Derived Credentials

The presentation of credentials with BBS+ signatures can be exchanged by following [RFC 0454: Present Proof Protocol 2.0](https://github.com/hyperledger/aries-rfcs/blob/main/features/0454-present-proof-v2). The Present Proof Protocol 2.0 provides a registry of attachment formats that can be used for presentation exchange. Although agents can use any attachment format they want, agents are expected to use the format as described in RFC 0510 (see below).

##### 0510: Presentation-Exchange Attachment format

[RFC 0510: Presentation-Exchange Attachment format for requesting and presenting proofs](https://github.com/hyperledger/aries-rfcs/blob/main/features/0510-dif-pres-exch-attach/README.md) defines an attachment format based on the [DIF Presentation Exchange](https://identity.foundation/presentation-exchange/) specification.

The following part of this section describes the requirements of exchanging derived credentials using the Presentation Exchange Attachment format, in addition to the requirements as specified above and in [RFC 0510](https://github.com/hyperledger/aries-rfcs/blob/main/features/0510-dif-pres-exch-attach/README.md).

The Presentation Exchange MUST include the `ldp_vp` [Claim Format Designation](https://identity.foundation/presentation-exchange/#claim-format-designations). In turn the `proof_type` property of the `ldp_vp` claim format designation MUST include the `BbsBlsSignatureProof2020` proof type.

#### Example BBS+ Derived Credential

```jsonc
{
  "@context": [
    "https://www.w3.org/2018/credentials/v1",
    "https://w3id.org/citizenship/v1",
    "https://w3id.org/security/bbs/v1" // BBS + Context
  ],
  "id": "https://issuer.oidp.uscis.gov/credentials/83627465",
  "type": ["PermanentResidentCard", "VerifiableCredential"],
  "description": "Government of Example Permanent Resident Card.",
  "identifier": "83627465",
  "name": "Permanent Resident Card",
  "credentialSubject": {
    "id": "did:example:b34ca6cd37bbf23",
    "type": ["Person", "PermanentResident"],
    "familyName": "SMITH",
    "gender": "Male",
    "givenName": "JOHN"
  },
  "expirationDate": "2029-12-03T12:19:52Z",
  "issuanceDate": "2019-12-03T12:19:52Z",
  "issuer": "did:example:489398593",
  "proof": {
    "type": "BbsBlsSignatureProof2020", // <-- type must be `BbsBlsSignatureProof2020`
    "nonce": "wrmPiSRm+iBqnGBXz+/37LLYRZWirGgIORKHIkrgWVnHtb4fDe/4ZPZaZ+/RwGVJYYY=",
    "proofValue": "ABkB/wbvt6213E9eJ+aRGbdG1IIQtx+IdAXALLNg2a5ENSGOIBxRGSoArKXwD/diieDWG6+0q8CWh7CViUqOOdEhYp/DonzmjoWbWECalE6x/qtyBeE7W9TJTXyK/yW6JKSKPz2ht4J0XLV84DZrxMF4HMrY7rFHvdE4xV7ULeC9vNmAmwYAqJfNwY94FG2erg2K2cg0AAAAdLfutjMuBO0JnrlRW6O6TheATv0xZZHP9kf1AYqPaxsYg0bq2XYzkp+tzMBq1rH3tgAAAAIDTzuPazvFHijdzuAgYg+Sg0ziF+Gw5Bz8r2cuvuSg1yKWqW1dM5GhGn6SZUpczTXuZuKGlo4cZrwbIg9wf4lBs3kQwWULRtQUXki9izmznt4Go98X/ElOguLLum4S78Gehe1ql6CXD1zS5PiDXjDzAAAACWz/sbigWpPmUqNA8YUczOuzBUvzmkpjVyL9aqf1e7rSZmN8CNa6dTGOzgKYgDGoIbSQR8EN8Ld7kpTIAdi4YvNZwEYlda/BR6oSrFCquafz7s/jeXyOYMsiVC53Zls9KEg64tG7n90XuZOyMk9RAdcxYRGligbFuG2Ap+rQ+rrELJaW7DWwFEI6cRnitZo6aS0hHmiOKKtJyA7KFbx27nBGd2y3JCvgYO6VUROQ//t3F4aRVI1U53e5N3MU+lt9GmFeL+Kv+2zV1WssScO0ZImDGDOvjDs1shnNSjIJ0RBNAo2YzhFKh3ExWd9WbiZ2/USSyomaSK4EzdTDqi2JCGdqS7IpooKSX/1Dp4K+d8HhPLGNLX4yfMoG9SnRfRQZZQ==",
    "verificationMethod": "did:example:489398593#test",
    "proofPurpose": "assertionMethod",
    "created": "2020-10-16T23:59:31Z"
  }
}
```

### Privacy Considerations

Private Holder Binding is an evolution of CL Signatures Linked Secrets.

- `id` properties are always disclosed in derived credentials due to how JSON-LD works.
- Required properties from the VC Data Model MUST be disclosed in derived credentials.
- BBS+ credentials SHOULD not be used in conjunction with non-ZKP signature as this removes the privacy features of BBS.

## Reference

### Interoperability with Existing Credential Formats

We expect that many issuers will choose to shift exclusively to BBS+
credentials for the benefits described here. Accessing these benefits will
require reissuing credentials that were previously in a different format.

An issuer can issue duplicate credentials with both signature formats.

A holder can hold both types of credentials. The holder wallet could display the two credentials as a single entry in their credential list if the data is the same (it’s “enhanced” with both credential formats).

A verifier can send a proof request for the formats that they choose to support.

- The holder wallet can provide the credential that fulfills that proof restriction. This allows old credentials to continue being used without being reissued.
- The verifier may accept credentials of multiple formats.

### Issues with the BBS+ LD-Proofs specification

- `requiredRevealStatements` will be removed ([Issue 50](https://github.com/w3c-ccg/ldp-bbs2020/issues/50))
- `proofValue` and `nonce` must be base64 encoded ([Issue 51](https://github.com/w3c-ccg/ldp-bbs2020/issues/51))
- `signature` must be updated to `proofValue` for the `BbsBlsSignature2020` suite ([Issue 52](https://github.com/w3c-ccg/ldp-bbs2020/issues/52))
- The application of blank node identifiers ([Issue 10](https://github.com/w3c-ccg/ldp-bbs2020/issues/10))
- Private holder binding ([Issue 37](https://github.com/w3c-ccg/ldp-bbs2020/issues/37))

## Drawbacks

Existing implementations of BBS+ Signatures do not support ZKP proof predicates, but it is theoretically possible to support numeric date predicates. ZKP proof predicates are considered a key feature of CL signatures, and a migration to BBS+ LD-Proofs will lose this capability. The Indy maintainers consider this a reasonable trade-off to get the other benefits of BBS+ LD-Proofs. A mechanism to support predicates can hopefully be added in future work.

As mentioned in the [Private Holder Binding](#private-holder-binding) section, the [BBS+ LD-Proofs](https://w3c-ccg.github.io/ldp-bbs2020/) specification does not define a mechanism for private holder binding yet. This means implementing this RFC does not provide all privacy-enabling features that should be incorporated until the `BbsBlsBoundSignature2020` and `BbsBlsBoundSignatureProof2020` signature suites are formally defined.

## Rationale and alternatives

BBS+ LD-Proofs is a reasonable evolution of CL Signatures, as it supports most of the same features (with the exception of ZKP Proof Predicates), while producing smaller credentials that require less computation resources to validate (a key requirement for mobile use cases).

BBS+ LD-Proofs are receiving broad support across the verifiable credentials implementation community, so supporting this signature format will be strategic for interoperability and allow Aries to promote the privacy preserving capabilities such as zero knowledge proofs and private holder binding.

## Prior art

Indy Anoncreds used CL Signatures to meet many of the use cases currently envisioned for BBS+ LD-Proofs.

BBS+ Signatures were [originally proposed by Boneh, Boyen, and Shacham in 2004](https://crypto.stanford.edu/~xb/crypto04a/groupsigs.pdf).

The approach was [improved by Au, Susilo, and Mu in 2006](http://web.cs.iastate.edu/~wzhang/teach-552/ReadingList/552-14.pdf).

It was then further refined by
[Camenisch, Drijvers, and Lehmann in section 4.3 of this paper from 2016](https://eprint.iacr.org/2016/663.pdf).

In 2019, Evernym and Sovrin proposed [BBS+ Signatures as the foundation for Indy Anoncreds 2.0](https://github.com/hyperledger/ursa-docs/tree/main/specs/anoncreds2),
which in conjunction with [Rich Schemas](https://github.com/hyperledger/aries-rfcs/tree/main/concepts/0250-rich-schemas)
addressed a similar set of goals and capabilities as those addressed here, but were ultimately too heavy a solution.

In 2020, Mattr provided [a draft specification for BBS+ LD-Proofs](https://w3c-ccg.github.io/ldp-bbs2020/) that comply with [the Linked Data proof specification](https://w3c-ccg.github.io/ld-proofs/) in the W3C Credentials Community Group. The authors acknowledged that their approach did not support two key Anoncreds features: proof predicates and link secrets.

[Aries RFC 593](https://github.com/hyperledger/aries-rfcs/tree/main/features/0593-json-ld-cred-attach) describes the JSON-LD credential format.

## Unresolved questions

See the above note in [the Drawbacks Section](#drawbacks) about ZKP predicates.

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

_Implementation Notes_ [may need to include a link to test results](/README.md#accepted).

| Name / Link | Implementation Notes |
| ----------- | -------------------- |
|             |
