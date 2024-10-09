# Aries RFC 0592: Indy Attachment Formats for Requesting and Presenting Credentials

- Authors: [Daniel Hardman](mailto:daniel.hardman@gmail.com)
- Status: [ADOPTED](/README.md#adopted)
- Since: 2021-04-15
- Status Note: Formalizes the Indy AnonCreds attachments for issuing credentials and presenting proofs. A part of the Indy AnonCreds subtarget of [AIP v2.0](../../concepts/0302-aries-interop-profile/README.md).
- Supersedes: less formally documented Indy attachment formats documented in [Aries RFC 0036](../0036-issue-credential/README.md), [Aries RFC 0037](../0037-present-proof/README.md), etc.
- Start Date: 2017-01-01
- Tags: [feature](/tags.md#feature), [protocol](/tags.md#protocol), [credentials](/tags.md#credentials), [test-anomaly](/tags.md#test-anomaly)


## Summary

This RFC registers attachment formats used with Hyperledger Indy-style ZKP-oriented credentials in [Issue Credential Protocol 2.0](../0453-issue-credential-v2/README.md) and [Present Proof Protocol 2.0](../0454-present-proof-v2/README.md). These formats are generally considered v2 formats, as they align with the "anoncreds2" work in Hyperledger Ursa and are a second generation implementation. They began to be used in production in 2018 and are in active deployment in 2021.


## Motivation

Allows Indy-style credentials to be used with credential-related protocols that take pluggable formats as payloads.


## Reference

### cred filter format

The potential holder uses this format to propose criteria for a potential credential for the issuer to offer.

The identifier for this format is `hlindy/cred-filter@v2.0`. It is a base64-encoded version of the data structure specifying zero or more criteria from the following (non-base64-encoded) structure:

```jsonc
{
    "schema_issuer_did": "<schema_issuer_did>",
    "schema_name": "<schema_name>",
    "schema_version": "<schema_version>",
    "schema_id": "<schema_identifier>",
    "issuer_did": "<issuer_did>",
    "cred_def_id": "<credential_definition_identifier>"
}
```

The potential holder may not know, and need not specify, all of these criteria. For example, the holder might only know the schema name and the (credential) issuer DID. Recall that the potential holder may specify target attribute values and MIME types in the [credential preview](../0453-issue-credential-v2/README.md#preview-credential).

For example, the JSON (non-base64-encoded) structure might look like this:

```json
{
    "schema_issuer_did": "did:sov:4RW6QK2HZhHxa2tg7t1jqt",
    "schema_name": "bcgov-mines-act-permit.bcgov-mines-permitting",
    "issuer_did": "did:sov:4RW6QK2HZhHxa2tg7t1jqt"
}
```

A complete [`propose-credential` message from the Issue Credential protocol 2.0](../0453-issue-credential-v2/README.md#propose-credential) embeds this format at `/filters~attach/data/base64`:

```json
{
    "@id": "<uuid of propose message>",
    "@type": "https://didcomm.org/issue-credential/%VER/propose-credential",
    "comment": "<some comment>",
    "formats" : [{
        "attach_id": "<attach@id value>",
        "format": "hlindy/cred-filter@v2.0"
    }],
    "filters~attach": [{
        "@id": "<attach@id value>",
        "mime-type": "application/json",
        "data": {
            "base64": "ewogICAgInNjaGVtYV9pc3N1ZXJfZGlkIjogImRpZDpzb3Y... (clipped)... LMkhaaEh4YTJ0Zzd0MWpxdCIKfQ=="
        }
    }]
}
```

### cred abstract format

This format is used to clarify the structure and semantics (but not the concrete data values) of a potential credential, in offers sent from issuer to potential holder.

The identifier for this format is `hlindy/cred-abstract@v2.0`. It is a base64-encoded version of the data returned from [`indy_issuer_create_credential_offer()`](https://github.com/hyperledger/indy-sdk/blob/57dcdae74164d1c7aa06f2cccecaae121cefac25/libindy/src/api/anoncreds.rs#L280).

The JSON (non-base64-encoded) structure might look like this:

```json
{
    "schema_id": "4RW6QK2HZhHxa2tg7t1jqt:2:bcgov-mines-act-permit.bcgov-mines-permitting:0.2.0",
    "cred_def_id": "4RW6QK2HZhHxa2tg7t1jqt:3:CL:58160:default",
    "nonce": "57a62300-fbe2-4f08-ace0-6c329c5210e1",
    "key_correctness_proof" : <key_correctness_proof>
}
```

A complete [`offer-credential` message from the Issue Credential protocol 2.0](../0453-issue-credential-v2/README.md#offer-credential) embeds this format at `/offers~attach/data/base64`:

```json
{
    "@type": "https://didcomm.org/issue-credential/%VER/offer-credential",
    "@id": "<uuid of offer message>",
    "replacement_id": "<issuer unique id>",
    "comment": "<some comment>",
    "credential_preview": <json-ld object>,
    "formats" : [
        {
            "attach_id" : "<attach@id value>",
            "format": "hlindy/cred-abstract@v2.0"
        }
    ],
    "offers~attach": [
        {
            "@id": "<attach@id value>",
            "mime-type": "application/json",
            "data": {
                "base64": "ewogICAgInNjaGVtYV9pZCI6ICI0Ulc2UUsySFpoS... (clipped)... jb3JyZWN0bmVzc19wcm9vZj4KfQ=="
            }
        }
    ]
}
```

The same structure can be embedded at `/offers~attach/data/base64` in an [`offer-credential` message](../0453-issue-credential-v2/README.md#offer-credential). 

### cred request format

This format is used to formally request a credential. It differs from the credential abstract above in that it contains a cryptographic commitment to a link secret; an issuer can therefore use it to bind a concrete instance of an issued credential to the appropriate holder. (In contrast, the credential abstract describes the schema and cred def, but not enough information to actually issue to a specific holder.)

The identifier for this format is `hlindy/cred-req@v2.0`. It is a base64-encoded version of the data returned from [indy_prover_create_credential_req()](https://github.com/hyperledger/indy-sdk/blob/57dcdae74164d1c7aa06f2cccecaae121cefac25/libindy/src/api/anoncreds.rs#L658).

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
        "mime-type": "application/json",
        "data": {
            "base64": "ewogICAgInByb3Zlcl9kaWQiIDogImRpZDpzb3Y6YWJjeHl.. (clipped)... DAtNTdhNi00ZjA4LWFjZTAtOWM1MjEwZTE2YzMyIgp9"
        }
    }]
}
```

### credential format

A concrete, issued Indy credential may be transmitted over many protocols, but is specifically expected as the final message in [Issuance Protocol 2.0](../0453-issue-credential-v2/README.md). The identifier for its format is `hlindy/cred@v2.0`.

This is a credential that's designed to be _held_ but not _shared directly_. It is stored in the holder's wallet and used to [derive a novel ZKP](https://youtu.be/bnbNtjsKb4k?t=1280) or [W3C-compatible verifiable presentation](https://docs.google.com/document/d/1ntLZGMah8iJ_TWQdbrNNW9OVwPbIWkkCMiid7Be1PrA/edit#heading=h.vw0mboesl528) just in time for each sharing of credential material.

The encoded values of the credential MUST follow the encoding algorithm as described in [Encoding Claims](#encoding-claims).

This is the format emitted by libindy's [indy_issuer_create_credential()](https://github.com/hyperledger/indy-sdk/blob/57dcdae74164d1c7aa06f2cccecaae121cefac25/libindy/src/api/anoncreds.rs#L383) function. It is JSON-based and might look like this:

```jsonc
{
    "schema_id": "4RW6QK2HZhHxa2tg7t1jqt:2:bcgov-mines-act-permit.bcgov-mines-permitting:0.2.0",
    "cred_def_id": "4RW6QK2HZhHxa2tg7t1jqt:3:CL:58160:default",
    "rev_reg_id", "EyN78DDGHyok8qw6W96UBY:4:EyN78DDGHyok8qw6W96UBY:3:CL:56389:CardossierOrgPerson:CL_ACCUM:1-1000",
    "values": {
        "attr1" : {"raw": "value1", "encoded": "value1_as_int" },
        "attr2" : {"raw": "value2", "encoded": "value2_as_int" }
    },
    // Fields below can depend on Cred Def type
    "signature": <signature>,
    "signature_correctness_proof": <signature_correctness_proof>
    "rev_reg": <revocation registry state>
    "witness": <witness>
}
```

An exhaustive description of the format is out of scope here; it is more completely documented in white papers, source code, and other Indy materials.

### proof request format

This format is used to formally request a verifiable presenation (proof) derived from an Indy-style ZKP-oriented credential. It can also be used by a holder to _propose_ a presentation.

The identifier for this format is `hlindy/proof-req@v2.0`. It is a base64-encoded version of the data returned from [indy_prover_search_credentials_for_proof_req()](https://github.com/hyperledger/indy-sdk/blob/57dcdae74164d1c7aa06f2cccecaae121cefac25/libindy/src/api/anoncreds.rs#L1214).

Here is a sample proof request that embodies the following: "Using a government-issued ID, disclose the credential holder’s name and height, hide the credential holder’s sex, get them to self-attest their phone number, and prove that their age is at least 18":

```jsonc
{
    "nonce": “2934823091873049823740198370q23984710239847”, 
    "name":"proof_req_1",
    "version":"0.1",
    "requested_attributes":{
        "attr1_referent": {"name":"sex"},
        "attr2_referent": {"name":"phone"},
        "attr3_referent": {"names": ["name", "height"], "restrictions": <restrictions specifying government-issued ID>}
    },
    "requested_predicates":{
        "predicate1_referent":{"name":"age","p_type":">=","p_value":18}
    }
}
```

### proof format

This is the format of an Indy-style ZKP. It plays the same role as a W3C-style verifiable presentation (VP) and can be [mapped to one](https://docs.google.com/document/d/1ntLZGMah8iJ_TWQdbrNNW9OVwPbIWkkCMiid7Be1PrA/edit#heading=h.vw0mboesl528).

The raw values encoded in the presentation SHOULD be verified against the encoded values using the encoding algorithm as described below in [Encoding Claims](#encoding-claims).

The identifier for this format is `hlindy/proof@v2.0`. It is a version of the (JSON-based) data emitted by libindy's [indy_prover_create_proof()](https://github.com/hyperledger/indy-sdk/blob/57dcdae74164d1c7aa06f2cccecaae121cefac25/libindy/src/api/anoncreds.rs#L1404)) function. A proof that responds to the [previous proof request sample](#proof-request-format) looks like this:

```jsonc
{
  "proof":{
    "proofs":[
      {
        "primary_proof":{
          "eq_proof":{
            "revealed_attrs":{
              "height":"175",
              "name":"1139481716457488690172217916278103335"
            },
            "a_prime":"5817705...096889",
            "e":"1270938...756380",
            "v":"1138...39984052",
            "m":{
              "master_secret":"375275...0939395",
              "sex":"3511483...897083518",
              "age":"13430...63372249"
            },
            "m2":"1444497...2278453"
          },
          "ge_proofs":[
            {
              "u":{
                "1":"152500...3999140",
                "2":"147748...2005753",
                "0":"8806...77968",
                "3":"10403...8538260"
              },
              "r":{
                "2":"15706...781609",
                "3":"343...4378642",
                "0":"59003...702140",
                "DELTA":"9607...28201020",
                "1":"180097...96766"
              },
              "mj":"134300...249",
              "alpha":"827896...52261",
              "t":{
                "2":"7132...47794",
                "3":"38051...27372",
                "DELTA":"68025...508719",
                "1":"32924...41082",
                "0":"74906...07857"
              },
              "predicate":{
                "attr_name":"age",
                "p_type":"GE",
                "value":18
              }
            }
          ]
        },
        "non_revoc_proof":null
      }
    ],
    "aggregated_proof":{
      "c_hash":"108743...92564",
      "c_list":[ 6 arrays of 257 numbers between 0 and 255]
    }
  },
  "requested_proof":{
    "revealed_attrs":{
      "attr1_referent":{
        "sub_proof_index":0,
        "raw":"Alex",
        "encoded":"1139481716457488690172217916278103335"
      }
    },
    "revealed_attr_groups":{
      "attr4_referent":{
        "sub_proof_index":0,
        "values":{
          "name":{
            "raw":"Alex",
            "encoded":"1139481716457488690172217916278103335"
          },
          "height":{
            "raw":"175",
            "encoded":"175"
          }
        }
      }
    },
    "self_attested_attrs":{
      "attr3_referent":"8-800-300"
    },
    "unrevealed_attrs":{
      "attr2_referent":{
        "sub_proof_index":0
      }
    },
    "predicates":{
      "predicate1_referent":{
        "sub_proof_index":0
      }
    }
  },
  "identifiers":[
    {
      "schema_id":"NcYxiDXkpYi6ov5FcYDi1e:2:gvt:1.0",
      "cred_def_id":"NcYxi...cYDi1e:2:gvt:1.0:TAG_1",
      "rev_reg_id":null,
      "timestamp":null
    }
  ]
}
```

### Unrevealed Attributes

AnonCreds supports a holder responding to a proof request with some of the
requested claims included in an `unrevealed_attrs` array, as seen in the example
above, with `attr2_referent`. Assuming the rest of the proof is valid, AnonCreds
will indicate that a proof with unrevealed attributes has been successfully
verified. It is the responsibility of the verifier to determine if the purpose
of the verification has been met if some of the attributes are not revealed.

There are at least a few valid use cases for this approach:

- A verifier may ask for, but not require, that a prover provide all of the
  requested attributes.
- A verifier may ask for claims from several credentials, expecting holders to
  only have some of the credentials. The holders respond with claims from the
  credentials they have, and leave the other attributes unrevealed.
  - For example, a verifier may ask for a national identity card and an resident
    card, knowing that most holders will have one or the other.

### Encoding Claims

Claims in AnonCreds-based verifiable credentials are put into the credential in two forms, `raw` and `encoded`. `raw` is the actual data value, and `encoded` is the (possibly derived) integer value that is used in presentations. At this time, AnonCreds does not take an opinion on the method used for encoding the raw value.

AnonCreds issuers and verifiers must agree on the encoding method so that the verifier can check that the `raw` value returned in a presentation corresponds to the proven `encoded` value. The following is the encoding algorithm that MUST be used by Issuers when creating credentials and SHOULD be verified by Verifiers receiving presentations:

- keep any 32-bit integer as is
- convert any string integer (e.g. `"1234"`) to be a 32-bit integer (e.g. `1234`)
- for data of any other type:
  - convert to string (use string "None" for null)
  - encode via utf-8 to bytes
  - apply SHA-256 to digest the bytes
  - convert the resulting digest bytes, big-endian, to integer
  - stringify the integer as a decimal.

An example implementation in Python can be found [here](https://github.com/hyperledger/aries-cloudagent-python/blob/0000f924a50b6ac5e6342bff90e64864672ee935/aries_cloudagent/messaging/util.py#L106).

A gist of test value pairs can be found [here](https://gist.github.com/swcurran/78e5a9e8d11236f003f6a6263c6619a6).

#### Notes on Encoding Claims

- In converting any string integer to an integer, leading 0s in the string are (by definition) not part of the integer. The leading 0's remain in the (untouched) `raw` value.
- The use of AnonCreds predicates, such as proving "older than 21" based on a date of birth claim without sharing the date of birth, is based on an expression involving the `encoded` value. Thus, only `raw` integers or string integers can be used in AnonCreds predicates.

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

Name / Link | Implementation Notes
--- | ---
 | 

