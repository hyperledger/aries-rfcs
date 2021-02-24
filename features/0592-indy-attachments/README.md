# Aries RFC 0592: Indy Attachment Formats for Requesting and Presenting Credentials
- Authors: [Daniel Hardman](mailto:daniel.hardman@gmail.com)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2021-02-23
- Status Note:
- Supersedes: less formally documented Indy attachment formats documented in [Aries RFC 0036](../0036-issue-credential/README.md), [Aries RFC 0037](../0037-present-proof/README.md), etc.
- Start Date: 2017-01-01
- Tags: [feature](/tags.md#feature), [protocol](/tags.md#protocol), [credentials](/tags.md#credentials), [test-anomaly](/tags.md#test-anomaly)


## Summary

This RFC registers attachment formats used with Hyperledger Indy-style ZKP-oriented credentials in [Issue Credential Protocol 2.0](../0453-issue-credential-v2/README.md) and [Present Proof Protocol 2.0](../0454-present-proof-v2/README.md).


## Motivation

Allows Indy-style credentials to be used with credential-related protocols that take pluggable formats as payloads.


## Reference

### cred abstract format

This format is used to clarify the structure and semantics (but not the concrete data values) of a potential credential -- both in proposals sent from potential holder to issuer, and in offers sent from issuer to potential holder.

The identifier for this format is: `hlindy/cred-abstract@v2.0` It is a base64-encoded version of the data returned from [`indy_issuer_create_credential_offer()`](https://github.com/hyperledger/indy-sdk/blob/57dcdae74164d1c7aa06f2cccecaae121cefac25/libindy/src/api/anoncreds.rs#L280).

The JSON (non-base64-encoded) structure might look like this:

```json
{
    "schema_id": "4RW6QK2HZhHxa2tg7t1jqt:2:bcgov-mines-act-permit.bcgov-mines-permitting:0.2.0",
    "cred_def_id": "4RW6QK2HZhHxa2tg7t1jqt:3:CL:58160:default",
    "nonce": "57a62300-fbe2-4f08-ace0-6c329c5210e1",
    "key_correctness_proof" : <key_correctness_proof>
}
```

A complete [`propose-credential` message from the Issue Credential protocol 2.0](../0453-issue-credential-v2/README.md#propose-credential) embeds this format at `/filters~attach/data/base64`:

```json
{
    "@id": "8639505e-4ec5-41b9-bb31-ac6a7b800fe7",
    "@type": "https://didcomm.org/issue-credential/%VER/propose-credential",
    "comment": "<some comment>",
    "formats" : [{
        "attach_id": "b45ca1bc-5b3c-4672-a300-84ddf6fbbaea",
        "format": "hlindy/cred-abstract@v2.0"
    }],
    "filters~attach": [{
        "@id": "b45ca1bc-5b3c-4672-a300-84ddf6fbbaea",
        "mime-type": "application/indy-cred-abstract",
        "data": {
            "base64": "ewogICAgInNjaGVtYV9pZCI6ICI0Ulc2UUsySFpoS... (clipped)... jb3JyZWN0bmVzc19wcm9vZj4KfQ=="
        }
    }]
}
```

The same structure can be embedded at `/offers~attach/data/base64` in an [`offer-credential` message](../0453-issue-credential-v2/README.md#offer-credential). 

### cred request format

This format is used to formally request a credential. It differs from the credential abstract above in that it contains a cryptographic commitment to a link secret; an issuer can therefore use it to bind a concrete instance of an issued credential to the appropriate holder. (In contrast, the credential abstract describes the schema and cred def, but not enough information to actually issue to a specific holder.)

The identifier for this format is: `hlindy/cred-req@v2.0` It is a base64-encoded version of the data returned from [indy_prover_create_credential_req()](https://github.com/hyperledger/indy-sdk/blob/57dcdae74164d1c7aa06f2cccecaae121cefac25/libindy/src/api/anoncreds.rs#L658).

The JSON (non-base64-encoded) structure might look like this:

```jsonc
{
    "prover_did" : "did:sov:abcxyz123",
    "cred_def_id" : "4RW6QK2HZhHxa2tg7t1jqt:3:CL:58160:default",
    // Fields below can depend on Cred Def type
    "blinded_ms" : <blinded_master_secret>,
    "blinded_ms_correctness_proof" : <blinded_ms_correctness_proof>,
    "nonce": "fbe22300-57a6-4f08-ace0-9c5210e16c32"
}
```

A complete [`request-credential` message from the Issue Credential protocol 2.0](../0453-issue-credential-v2/README.md#request-credential) embeds this format at `/requests~attach/data/base64`:

```json
{
    "@id": "cf3a9301-6d4a-430f-ae02-b4a79ddc9706",
    "@type": "https://didcomm.org/issue-credential/%VER/request-credential",
    "comment": "<some comment>",
    "formats": [{
        "attach_id": "7cd11894-838a-45c0-a9ec-13e2d9d125a1",
        "format": "hlindy/cred-req@v2.0"
    }],
    "requests~attach": [{
        "@id": "7cd11894-838a-45c0-a9ec-13e2d9d125a1",
        "mime-type": "application/indy-cred-req",
        "data": {
            "base64": "ewogICAgInByb3Zlcl9kaWQiIDogImRpZDpzb3Y6YWJjeHl.. (clipped)... DAtNTdhNi00ZjA4LWFjZTAtOWM1MjEwZTE2YzMyIgp9"
        }
    }]
}
```

### credential format

A concrete, issued Indy credential may be transmitted over many protocols, but is specifically expected as the final message in [Issuance Protocol 2.0](../0453-issue-credential-v2/README.md). The identifier for its format is `hlindy/cred@v2.0`, and its media (MIME) type is `application/indy-cl-anoncred2`.

This is a credential that's designed to be _held_ but not _shared directly_. It is stored in the holder's wallet and used to [derive a novel ZKP](https://youtu.be/bnbNtjsKb4k?t=1280) or [W3C-compatible verifiable presentation](https://docs.google.com/document/d/1ntLZGMah8iJ_TWQdbrNNW9OVwPbIWkkCMiid7Be1PrA/edit#heading=h.vw0mboesl528) just in time for each sharing of credential material.

This is the format emitted by libindy's [indy_issuer_create_credential()](https://github.com/hyperledger/indy-sdk/blob/57dcdae74164d1c7aa06f2cccecaae121cefac25/libindy/src/api/anoncreds.rs#L383) function. It is JSON-based and might look like this:

```jsonc
{
"schema_id": "4RW6QK2HZhHxa2tg7t1jqt:2:bcgov-mines-act-permit.bcgov-mines-permitting:0.2.0",
"cred_def_id": "4RW6QK2HZhHxa2tg7t1jqt:3:CL:58160:default",
"rev_reg_def_id", "EyN78DDGHyok8qw6W96UBY:4:EyN78DDGHyok8qw6W96UBY:3:CL:56389:CardossierOrgPerson:CL_ACCUM:1-1000",
"values": {
    "attr1" : {"raw": "value1", "encoded": "value1_as_int" },
    "attr2" : {"raw": "value1", "encoded": "value1_as_int" }
},
// Fields below can depend on Cred Def type
"signature": <signature>,
"signature_correctness_proof": <signature_correctness_proof>
}
```

An exhaustive description of the format is out of scope here; it is more completely documented in whitepapers, source code, and other Indy materials.

### proof request format

This format is used to formally request a verifiable presenation (proof) derived from an Indy-style ZKP-oriented credential.

The identifier for this format is: `hlindy/proof-req@v2.0` It is a base64-encoded version of the data returned from [indy_prover_search_credentials_for_proof_req()](https://github.com/hyperledger/indy-sdk/blob/57dcdae74164d1c7aa06f2cccecaae121cefac25/libindy/src/api/anoncreds.rs#L1214).

Its JSON might look like this:

```jsonc
{
    "name": string,
    "version": string,
    "nonce": string,
    "requested_attributes": { // set of requested attributes
      "<attr_referent>": <attr_info>, // see below
      ...,
    },
    "requested_predicates": { // set of requested predicates
      "<predicate_referent>": <predicate_info>, // see below
      ...,
    },
    "non_revoked": Optional<<non_revoc_interval>>, // see below,
                // If specified prover must proof non-revocation
                // for date in this interval for each attribute
               // (can be overridden on attribute level)
}
```

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

Name / Link | Implementation Notes
--- | ---
 | 

