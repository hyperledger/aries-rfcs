# Aries RFC 0771: AnonCreds Attachment Formats for Requesting and Presenting Credentials

- Authors: [Timo Glastra](mailto:timo@animo.id), [Daniel Hardman](mailto:daniel.hardman@gmail.com)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2023-02-24
- Status Note: Formalizes the AnonCreds attachments for issuing credentials and presenting proofs over DIDComm.
- Supersedes: Hyperledger Indy specific AnonCreds attachment formats documented in [Aries RFC 0592](../0592-indy-attachments/README.md).
- Start Date: 2023-02-24
- Tags: [feature](/tags.md#feature), [protocol](/tags.md#protocol), [credentials](/tags.md#credentials), [test-anomaly](/tags.md#test-anomaly)

## Summary

This RFC registers attachment formats used with [Hyperledger AnonCreds](https://hyperledger.github.io/anoncreds-spec/) ZKP-oriented credentials in the [Issue Credential Protocol 2.0](../0453-issue-credential-v2/README.md) and [Present Proof Protocol 2.0](../0454-present-proof-v2/README.md). If not specified otherwise, this follows the rules as defined in the [AnonCreds Specification](https://hyperledger.github.io/anoncreds-spec/).

## Motivation

Allows AnonCreds credentials to be used with credential-related protocols that take pluggable formats as payloads.

## Reference

### Credential Filter format

The potential holder uses this format to propose criteria for a potential credential for the issuer to offer. The format defined here is not part of the AnonCreds spec, but is a Hyperledger Aries-specific message.

The identifier for this format is `anoncreds/credential-filter@v1.0`. The data structure allows specifying zero or more criteria from the following structure:

```jsonc
{
  "schema_issuer_id": "<schema_issuer_id>",
  "schema_name": "<schema_name>",
  "schema_version": "<schema_version>",
  "schema_id": "<schema_identifier>",
  "issuer_id": "<issuer_id>",
  "cred_def_id": "<credential_definition_identifier>"
}
```

The potential holder may not know, and need not specify, all of these criteria. For example, the holder might only know the schema name and the (credential) issuer id. Recall that the potential holder may specify target attribute values and MIME types in the [credential preview](../0453-issue-credential-v2/README.md#preview-credential).

For example, the JSON structure might look like this:

```json
{
  "schema_issuer_id": "did:sov:4RW6QK2HZhHxa2tg7t1jqt",
  "schema_name": "bcgov-mines-act-permit.bcgov-mines-permitting",
  "issuer_id": "did:sov:4RW6QK2HZhHxa2tg7t1jqt"
}
```

A complete [`propose-credential` message from the Issue Credential protocol 2.0](../0453-issue-credential-v2/README.md#propose-credential) embeds this format as an attachment in the `filters~attach` array:

```json
{
  "@id": "<uuid of propose message>",
  "@type": "https://didcomm.org/issue-credential/%VER/propose-credential",
  "comment": "<some comment>",
  "formats": [
    {
      "attach_id": "<attach@id value>",
      "format": "anoncreds/credential-filter@v1.0"
    }
  ],
  "filters~attach": [
    {
      "@id": "<attach@id value>",
      "mime-type": "application/json",
      "data": {
        "base64": "ewogICAgInNjaGVtYV9pc3N1ZXJfZGlkIjogImRpZDpzb3Y... (clipped)... LMkhaaEh4YTJ0Zzd0MWpxdCIKfQ=="
      }
    }
  ]
}
```

### Credential Offer format

This format is used to clarify the structure and semantics (but not the concrete data values) of a potential credential, in offers sent from issuer to potential holder.

The identifier for this format is `anoncreds/credential-offer@v1.0`. It must follow the [structure of a Credential Offer](https://hyperledger.github.io/anoncreds-spec/#credential-offer) as defined in the AnonCreds specification.

The JSON structure might look like this:

```json
{
    "schema_id": "4RW6QK2HZhHxa2tg7t1jqt:2:bcgov-mines-act-permit.bcgov-mines-permitting:0.2.0",
    "cred_def_id": "4RW6QK2HZhHxa2tg7t1jqt:3:CL:58160:default",
    "nonce": "57a62300-fbe2-4f08-ace0-6c329c5210e1",
    "key_correctness_proof" : <key_correctness_proof>
}
```

A complete [`offer-credential` message from the Issue Credential protocol 2.0](../0453-issue-credential-v2/README.md#offer-credential) embeds this format as an attachment in the `offers~attach` array:

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
            "format": "anoncreds/credential-offer@v1.0"
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

### Credential Request format

This format is used to formally request a credential. It differs from the Credential Offer above in that it contains a cryptographic commitment to a link secret; an issuer can therefore use it to bind a concrete instance of an issued credential to the appropriate holder. (In contrast, the credential offer describes the schema and cred definition, but not enough information to actually issue to a specific holder.)

The identifier for this format is `anoncreds/credential-request@v1.0`. It must follow the [structure of a Credential Request](https://hyperledger.github.io/anoncreds-spec/#credential-request) as defined in the AnonCreds specification.

The JSON structure might look like this:

```jsonc
{
    "entropy" : "e7bc23ad-1ac8-4dbc-92dd-292ec80c7b77",
    "cred_def_id" : "4RW6QK2HZhHxa2tg7t1jqt:3:CL:58160:default",
    // Fields below can depend on Cred Def type
    "blinded_ms" : <blinded_master_secret>,
    "blinded_ms_correctness_proof" : <blinded_ms_correctness_proof>,
    "nonce": "fbe22300-57a6-4f08-ace0-9c5210e16c32"
}
```

A complete [`request-credential` message from the Issue Credential protocol 2.0](../0453-issue-credential-v2/README.md#request-credential) embeds this format as an attachment in the `requests~attach` array:

```json
{
  "@id": "cf3a9301-6d4a-430f-ae02-b4a79ddc9706",
  "@type": "https://didcomm.org/issue-credential/%VER/request-credential",
  "comment": "<some comment>",
  "formats": [
    {
      "attach_id": "7cd11894-838a-45c0-a9ec-13e2d9d125a1",
      "format": "anoncreds/credential-request@v1.0"
    }
  ],
  "requests~attach": [
    {
      "@id": "7cd11894-838a-45c0-a9ec-13e2d9d125a1",
      "mime-type": "application/json",
      "data": {
        "base64": "ewogICAgInByb3Zlcl9kaWQiIDogImRpZDpzb3Y6YWJjeHl.. (clipped)... DAtNTdhNi00ZjA4LWFjZTAtOWM1MjEwZTE2YzMyIgp9"
      }
    }
  ]
}
```

### Credential format

A concrete, issued AnonCreds credential may be transmitted over many protocols, but is specifically expected as the final message in [Issuance Protocol 2.0](../0453-issue-credential-v2/README.md). The identifier for this format is `anoncreds/credential@v1.0`.

This is a credential that's designed to be _held_ but not _shared directly_. It is stored in the holder's wallet and used to [derive a novel ZKP](https://youtu.be/bnbNtjsKb4k?t=1280) or [W3C-compatible verifiable presentation](https://docs.google.com/document/d/1ntLZGMah8iJ_TWQdbrNNW9OVwPbIWkkCMiid7Be1PrA/edit#heading=h.vw0mboesl528) just in time for each sharing of credential material.

The encoded values of the credential MUST follow the encoding algorithm as described in [Encoding Attribute Data](https://hyperledger.github.io/anoncreds-spec/#encoding-attribute-data). It must follow the [structure of a Credential](https://hyperledger.github.io/anoncreds-spec/#constructing-a-credential) as defined in the AnonCreds specification.

The JSON structure might look like this:

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

An exhaustive description of the format is out of scope here; it is more completely documented in the [AnonCreds Specification](https://hyperledger.github.io/anoncreds-spec).

### Proof Request format

This format is used to formally request a verifiable presenation (proof) derived from an AnonCreds-style ZKP-oriented credential.

The format can also be used to _propose_ a presentation, in this case the `nonce` field MUST NOT be provided. The `nonce` field is required when the proof request is used to request a proof.

The identifier for this format is `anoncreds/proof-request@v1.0`. It must follow the [structure of a Proof](https://hyperledger.github.io/anoncreds-spec/#create-presentation-request) as defined in the AnonCreds specification.

Here is a sample proof request that embodies the following: "Using a government-issued ID, disclose the credential holder’s name and height, hide the credential holder’s sex, get them to self-attest their phone number, and prove that their age is at least 18":

```jsonc
{
    "nonce": "2934823091873049823740198370q23984710239847",
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

### Proof format

This is the format of an AnonCreds-style ZKP. The raw values encoded in the presentation MUST be verified against the encoded values using the encoding algorithm as described in [Encoding Attribute Data](https://hyperledger.github.io/anoncreds-spec/#encoding-attribute-data)

The identifier for this format is `anoncreds/proof@v1.0`. It must follow the [structure of a Presentation](https://hyperledger.github.io/anoncreds-spec/#generate-presentation) as defined in the AnonCreds specification.

A proof that responds to the [previous proof request sample](#proof-request-format) looks like this:

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

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

| Name / Link | Implementation Notes |
| ----------- | -------------------- |
|             |
