Table of Contents
=================

* [Anoncrypt JWE Concrete examples](#anoncrypt-jwe-concrete-examples)
  * [Notes](#notes)
  * [1 A256GCM Content Encryption](#1-a256gcm-content-encryption)
    * [1.1 Multi recipients JWEs](#11-multi-recipients-jwes)
      * [1.1.1 NIST P-256 keys](#111-nist-p-256-keys)
      * [1.1.2 NIST P-384 keys](#112-nist-p-384-keys)
      * [1.1.3 NIST P-521 keys](#113-nist-p-521-keys)
      * [1.1.4 X25519 keys](#114-x25519-keys)
    * [1.2 Single Recipient JWEs](#12-single-recipient-jwes)
      * [1.2.1 NIST P-256 key](#121-nist-p-256-key)
      * [1.2.2 NIST P-384 key](#122-nist-p-384-key)
      * [1.2.3 NIST P-521 key](#123-nist-p-521-key)
      * [1.2.4 X25519 key](#124-x25519-key)
  * [2 XC20P content encryption](#2-xc20p-content-encryption)
    * [2.1 Multi recipients JWEs](#21-multi-recipients-jwes)
      * [2.1.1 NIST P-256 keys](#211-nist-p-256-keys)
      * [2.1.2 NIST P-384 keys](#212-nist-p-384-keys)
      * [2.1.3 NIST P-521 keys](#213-nist-p-521-keys)
      * [2.1.4 X25519 keys](#214-x25519-keys)
    * [2.2 Single Recipient JWEs](#22-single-recipient-jwes)
      * [2.2.1 NIST P-256 key](#221-nist-p-256-key)
      * [2.2.2 NIST P-384 key](#222-nist-p-384-key)
      * [2.2.3 NIST P-521 key](#223-nist-p-521-key)
      * [2.2.4 X25519 key](#224-x25519-key)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)

# Anoncrypt JWE Concrete examples

The following examples are for JWE **anoncrypt** packer for encrypting the payload `secret message` and aad value set as the concatenation of recipients' KIDs (ASCII sorted) joined by `.` for non-compact serializations (JWE Compact serializations [don't have AAD](https://tools.ietf.org/html/rfc7516#section-7.1)).

### Notes
- all `x` and `y` key coordinates values below are raw (no padding) base64URL encoded.
- JWE envelopes with multi recipients use the [General JWE JSON Serialization](https://tools.ietf.org/html/rfc7516#section-7.2.1) format.
- JWE envelopes with a single recipient will be shown in both serialization formats: as [JWE Compact](https://tools.ietf.org/html/rfc7516#section-3.1) or [Flattened JWE JSON](https://tools.ietf.org/html/rfc7516#section-7.2.2).
- **General** JWE JSON Serialization format use. the above mentioned AAD value in their envelope.
- JWE **Compact** Serialization format does not support AAD values and therefore were built without it.
- all `apu` recipient header values are set to the raw (no padding) base64URL encoding of the corresponding recipient's ephemeral key's `x` value since Anoncrypt dosen't reveal the sender.
- all `apv` recipient header values are set to the raw (no padding) base64URL encoding of the corresponding recipient's `kid` value.
- The final aad used to encrypt the payload is the concatenation of the raw (no padding) base64URL encoded protected headers and `aad` JWE header joined by a `.`.
- Even though flattened serialization do support `aad`, the field is omitted in the below examples to be consistent with compact JWE serialization format. Implementations should support `aad` for flattened serialization regardless.

## 1 A256GCM Content Encryption

The packer generates the following protected headers for A256GCM content encryption in the below examples:
- Generated protected headers: `{"cty":"application/didcomm-plain+json","enc":"A256GCM","typ":"application/didcomm-encrypted+json"}`
    - raw (no padding) base64URL encoded: `eyJjdHkiOiJhcHBsaWNhdGlvbi9kaWRjb21tLXBsYWluK2pzb24iLCJlbmMiOiJBMjU2R0NNIiwidHlwIjoiYXBwbGljYXRpb24vZGlkY29tbS1lbmNyeXB0ZWQranNvbiJ9`

### 1.1 Multi recipients JWEs

#### 1.1.1 NIST P-256 keys
- Recipient 1 key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-256",
  "x": "2fpy_fK5FCsap0EbU1Om7QXoVoyvBv8gfdHY3ufIS9w",
  "y": "TtVOc9c8ejMeqeaUs1CMS79w0-Al02Fw25WdVEb0DiI",
  "d": "kEWLCAyDL8mgDLNnlb1am_B8wcaGAe7ViXx1tqKWTVc"
}
```
- Recipient 1 kid (jwk thumbprint raw base64 URL encoded): `s6-ZhI1hpx0kM3pDgOrVQs6mRd_8KfEXUkLg8lK7XNA`
- Recipient 2 key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-256",
  "x": "S9JVfrKenXIMiEUha1k8yt7Zw8d5_bSxEt6RJesPt1g",
  "y": "KMWwZzb80uoAjCcuwQ3gSeyjMsbq02AyS7g1D2i7ZwM",
  "d": "bHnnqFSAFROp4kLbfBfihHUg6PIviwRCt5foN2Romw4"
}
```
- Recipient 2 kid (jwk thumbprint raw base64 URL encoded): `2NfcF400LLr9Wa6QbkUikYUUcdsAUkZBy6ifrrXYI0U`
- Recipient 3 key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-256",
  "x": "tqn3J0p752xWq2T4M11Q8ZcidyEWfaray-2B84hjehg",
  "y": "ewcqOkZtlGBfZmP9nr44tq7_vkBJ3fJe9u6TCEyMDh8",
  "d": "5XlB_SQXVpA6Id1PNL4SJfrMhCC36xa0hSHB7WpwA9Y"
}
```
- Recipient 3 kid (jwk thumbprint raw, no padding, base64 URL encoded): `xG9z3It37igQIB4Q9jbcKLVjcFvnXIvkuJdLNKFvRB4`
- List of kids used for AAD for the above recipients (sorted `kid` values joined with `.`): `2NfcF400LLr9Wa6QbkUikYUUcdsAUkZBy6ifrrXYI0U.s6-ZhI1hpx0kM3pDgOrVQs6mRd_8KfEXUkLg8lK7XNA.xG9z3It37igQIB4Q9jbcKLVjcFvnXIvkuJdLNKFvRB4`
- Resulting AAD value (sha256 of above list raw, no padding, base64 URL encoded): `YyqAtGX-dZTiXaZnGazezl-jBXS4uka1sOFv8cV42uM`
- Finally, packing the payload outputs the following JWE (pretty printed for readability):
```json
{
  "protected": "eyJjdHkiOiJhcHBsaWNhdGlvbi9kaWRjb21tLXBsYWluK2pzb24iLCJlbmMiOiJBMjU2R0NNIiwidHlwIjoiYXBwbGljYXRpb24vZGlkY29tbS1lbmNyeXB0ZWQranNvbiJ9",
  "recipients": [
    {
      "header": {
        "alg": "ECDH-ES+A256KW",
        "apu": "WVU3OHhXeVZLeC1WRVpIV2pWbFN3Z2NndFRtSjBfS09YOE9hTkdnQXNlUQ",
        "apv": "czYtWmhJMWhweDBrTTNwRGdPclZRczZtUmRfOEtmRVhVa0xnOGxLN1hOQQ",
        "kid": "s6-ZhI1hpx0kM3pDgOrVQs6mRd_8KfEXUkLg8lK7XNA",
        "epk": {
          "kty": "EC",
          "crv": "P-256",
          "x": "YU78xWyVKx-VEZHWjVlSwgcgtTmJ0_KOX8OaNGgAseQ",
          "y": "AiHDxtQBrba6g3_d0tic8LeLZRMz7rqnghQ2DvJh0Xk"
        }
      },
      "encrypted_key": "fnofbBoie-ywDVjd_Dcdw611KWabq0RptbEybN_AParPMI0qpOwm1Q"
    },
    {
      "header": {
        "alg": "ECDH-ES+A256KW",
        "apu": "NkN3ZEt3ZEotczdIZHFpUzExR0x6bS1scVhlUW1TYWJjNXBvRnBaakdZbw",
        "apv": "czYtWmhJMWhweDBrTTNwRGdPclZRczZtUmRfOEtmRVhVa0xnOGxLN1hOQQ",
        "kid": "2NfcF400LLr9Wa6QbkUikYUUcdsAUkZBy6ifrrXYI0U",
        "epk": {
          "kty": "EC",
          "crv": "P-256",
          "x": "6CwdKwdJ-s7HdqiS11GLzm-lqXeQmSabc5poFpZjGYo",
          "y": "mVsQl_AhZoHpC86UN49k6tAU5B2YLi0HIdWeaIvSQy8"
        }
      },
      "encrypted_key": "qN1WX7DK0k2GW4qHK0SfQFTRrOM0GFUgzqqy58QTRWi62r9iItmPxA"
    },
    {
      "header": {
        "alg": "ECDH-ES+A256KW",
        "apu": "aXZzeDhaVmowbEJ1c2pLNjZSS1dVN0JDRjJzal81QWlQb1VsS21KOHZkSQ",
        "apv": "czYtWmhJMWhweDBrTTNwRGdPclZRczZtUmRfOEtmRVhVa0xnOGxLN1hOQQ",
        "kid": "xG9z3It37igQIB4Q9jbcKLVjcFvnXIvkuJdLNKFvRB4",
        "epk": {
          "kty": "EC",
          "crv": "P-256",
          "x": "ivsx8ZVj0lBusjK66RKWU7BCF2sj_5AiPoUlKmJ8vdI",
          "y": "Ea6i7ahugWrTZoc9UMq1e3aPmHm0bkGqxTDmoEMyYMU"
        }
      },
      "encrypted_key": "Yds0G9wYyAaGf2ky9DAT0CITzoD4qHV1fUM-cH-mmGsx8TeFjYBVYw"
    }
  ],
  "aad": "YyqAtGX-dZTiXaZnGazezl-jBXS4uka1sOFv8cV42uM",
  "iv": "S9rOxQOd8H-gxZIv",
  "ciphertext": "w3kl_QixTanzflQHpuM",
  "tag": "4x5wmIBxrCjUpq4wxrWFDQ"
}
```

#### 1.1.2 NIST P-384 keys
- Recipient 1 key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-384",
  "x": "lb17x-OBz2i1kQbkRtSKD3TY1MwIfUMyM8YtqXZXMj884hLJH2QtxmUWKyXIprcn",
  "y": "PlT4CInTrA5zAroqwyww0BL6EipnEBTrtbWID8nADz6LFpf_27qlxIARy_iU5OcN",
  "d": "JJgpIqGS5JuiKRnsEgGNlYw39pz-XGrsrmniuxlSik0BLwdb8-0K8Xxuqo6yW6NE"
}
```
- Recipient 1 kid (jwk thumbprint raw base64 URL encoded): `8wPpWWlLiMBYltw6AoWG3Z_SfgWmXanBHSwZFpQJ0Q0`
- Recipient 2 public key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-384",
  "x": "ACZDXpzp6cKqsCcWq7sVOcCB_QZLd9ZfhoxhBKCbytrSKVKn7jV3Kv1XlsnH1RH7",
  "y": "FQy3qBV-bn4K_5bQXucEPIOupMhEJS7YXCbm-fUb9ZdC59b0-5lbo7l65fkEL3ZO",
  "d": "F4BlupNNnLfPOsml1MfBJgw6Oz89L6GnRiJnFi5ay5zVHTIcWzX81D060KsCjK9t"
}
```
- Recipient 2 kid (jwk thumbprint raw base64 URL encoded): `8l5z1lSVYFmv8QSboANWcj_UUh4bp3PlwEBNNHd2p3Q`
- Recipient 3 key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-384",
  "x": "msbHjsKVl0paXi-SWZ5_gEMgsMihBW9TEnfScKxfVlFMC6Hi5JIz1wgs58ugqaSX",
  "y": "ppzaqlmAjA_iBymA2iBH56mHeTxckL8YNfmcSNa8hJoD4XYZ-4_x9mip-dh8o4gI",
  "d": "YT0k8bBmPmecprG6tax6g00wG0JkprPcCqU1jvM86PAGGUU12fY7-Dfmqwhwv5U-"
}
```
- Recipient 3 kid (jwk thumbprint raw, no padding, base64 URL encoded): `t1KsLfBBTG9iXIzyga6xV7RAur2j34dLGB3jqTDuTMo`
- List of kids used for AAD for the above recipients (sorted `kid` values joined with `.`): `8l5z1lSVYFmv8QSboANWcj_UUh4bp3PlwEBNNHd2p3Q.8wPpWWlLiMBYltw6AoWG3Z_SfgWmXanBHSwZFpQJ0Q0.t1KsLfBBTG9iXIzyga6xV7RAur2j34dLGB3jqTDuTMo`
- Resulting AAD value (sha256 of above list raw, no padding, base64 URL encoded): `jgz9Cgt6lep5QPX0-GCkOMXujjRYgfiTslwut8BdX-0`
- JWE:
```json
{
  "protected": "eyJjdHkiOiJhcHBsaWNhdGlvbi9kaWRjb21tLXBsYWluK2pzb24iLCJlbmMiOiJBMjU2R0NNIiwidHlwIjoiYXBwbGljYXRpb24vZGlkY29tbS1lbmNyeXB0ZWQranNvbiJ9",
  "recipients": [
    {
      "header": {
        "alg": "ECDH-ES+A256KW",
        "apu": "OVdMemtDbjBlaEFxVTlwZjdvUEFZVUdOcHhkdTR2VWZUZVZxZzlVWEZUNVNPS0dTaDFwZ294aWhOb0tWZlpsNg",
        "apv": "OHdQcFdXbExpTUJZbHR3NkFvV0czWl9TZmdXbVhhbkJIU3daRnBRSjBRMA",
        "kid": "8wPpWWlLiMBYltw6AoWG3Z_SfgWmXanBHSwZFpQJ0Q0",
        "epk": {
          "kty": "EC",
          "crv": "P-384",
          "x": "9WLzkCn0ehAqU9pf7oPAYUGNpxdu4vUfTeVqg9UXFT5SOKGSh1pgoxihNoKVfZl6",
          "y": "Yuwe4x6Seue5pegwF9px-RQqSxARjf5mHSwVW7ft6dC5TgXdCPzm3bTRW4qxR41X"
        }
      },
      "encrypted_key": "Dj-4zbK_WbF_5nU1rfvT0dipMtwSUQvmluCrxwu-arKU2w59hN5ecQ"
    },
    {
      "header": {
        "alg": "ECDH-ES+A256KW",
        "apu": "Q2hxMTBxU0duM3JQdHVKaFcwcEF1TzIxanh4WkVFb0xVQ1hkajNTbERfelZMamQ4ZHdwSmp5UXhQeEVSQ2ZOTw",
        "apv": "OHdQcFdXbExpTUJZbHR3NkFvV0czWl9TZmdXbVhhbkJIU3daRnBRSjBRMA",
        "kid": "8l5z1lSVYFmv8QSboANWcj_UUh4bp3PlwEBNNHd2p3Q",
        "epk": {
          "kty": "EC",
          "crv": "P-384",
          "x": "Chq10qSGn3rPtuJhW0pAuO21jxxZEEoLUCXdj3SlD_zVLjd8dwpJjyQxPxERCfNO",
          "y": "9PkX3jqgkslA2Z8rijClt-1yX5uulFcbRl7dCaSgquCfYj0ZmOEVhQqdD9yh955n"
        }
      },
      "encrypted_key": "LpoFtDL4ac0bx16AkyE4HmpK-F_ibPm1LvyQVo-eFaPEo9HW8FWz_Q"
    },
    {
      "header": {
        "alg": "ECDH-ES+A256KW",
        "apu": "T0cyZUptVU05NENDS2w4U2lGVTJNQUhVUnJiRldRSm1xd25ya2VWUFN3NTMzX3lSakFMLVNscnhvZ29uSnBzbA",
        "apv": "OHdQcFdXbExpTUJZbHR3NkFvV0czWl9TZmdXbVhhbkJIU3daRnBRSjBRMA",
        "kid": "t1KsLfBBTG9iXIzyga6xV7RAur2j34dLGB3jqTDuTMo",
        "epk": {
          "kty": "EC",
          "crv": "P-384",
          "x": "OG2eJmUM94CCKl8SiFU2MAHURrbFWQJmqwnrkeVPSw533_yRjAL-SlrxogonJpsl",
          "y": "suMc0ckI46jPlM0dn7O_4fIpxFAD74LrkOUO_tEKeHD1opEoK7H2iE-1STzjflEm"
        }
      },
      "encrypted_key": "sAN-AeA0ZtInrhJYtzkNnWooDmXOOYo4mD1hMps8aV2Iw84GheOuMw"
    }
  ],
  "aad": "jgz9Cgt6lep5QPX0-GCkOMXujjRYgfiTslwut8BdX-0",
  "iv": "iHzMT8jUCFNsqsZY",
  "ciphertext": "IiPn4-09-MFtJggB5yE",
  "tag": "Na9kW8Fpw5j4IJ-fdf4jNA"
}
```

#### 1.1.3 NIST P-521 keys
- Recipient 1 key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-521",
  "x": "AHrw8TsyZzIkINFPCAS54Y7UoCI1XAlim95ROPykpjo4q2LvW_VWeBtJLU2SuqTFG4WX9VBzMg5Rq4gMj4oCpMFb",
  "y": "AUs4vywsYYuRP0LhFvyI_ippvSY6Tv1S8sEzojd41Ubo86bFlCj5c_wHX2N6hplMU01WAcebPWc24plqF39pkNrK",
  "d": "AEklgm76AbNl_nydbcINMgytfoZGRMI1mxfGcIiqw-KHENQMtlujImJrKMUd32njHS1M9e-WqAS8AHLoVdBZmkOo"
}
```
- Recipient 1 kid (jwk thumbprint raw base64 URL encoded): `9Miv3vUT2vQL0X80PyrLJm3bzGPuc_aKfPr4txRQIpA`
- Recipient 2 key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-521",
  "x": "AcJh1U3InkhEW5uvh9x3H_ZkzSRY9aoleTYH0a_ZgVKhGrQrttUgQhzvdj8Oyy389Muu0l5slkKfE_FpNXUoSlq8",
  "y": "AB8lDC62GR8b7lz_mboFcrBG4uAWNqQ-E-k4tYqBu8xJOV-v68FeuJKwC9WGFOiIUaCwSGUB4-cYeFPIxq9hxD7Y",
  "d": "AXTDpK0Eu6EEZliWHe-zgiY1s23sTepAgmP8KeVTOXeeCnCL12pK4mc-UR9NpEYrxBp_A5srbhzNR5x7mZ1G4kLf"
}
```
- Recipient 2 kid (jwk thumbprint raw base64 URL encoded): `l4-wvmALQDp4g-UpilwCHmLZ_zUGfNawYSWQMoLphIk`
- Recipient 3 key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-256",
  "x": "AA63cinH0aZ7e0sLBFx0s3MKQTfvdFjSMVMQHpp5qIF6pWaxV9TrqXkJYkR2fuMqvIRSlH5mMK73kNfEubrvsd7H",
  "y": "AY88QmJlRbAbCY9UyeDK0pYFHbSxgdMCauV2GC-W2w5uJekAWoeO9KxSY215W60whRHGRctrTc7LodcV8y7UKOyx",
  "d": "AU4kFJPY9rZA89-ZYvoZX_qKPglplaWZdFKU3ZzjZvNt7rBBUuKumsf_khTFF8q-LxJKd11B0rng3PIQRuob4JW-"
}
```
- Recipient 3 kid (jwk thumbprint raw, no padding, base64 URL encoded): `Ev1dKdei9chrjW2-l4bjdXXF5GDZ7CqTcQlGg1W_U24`
- List of kids used for AAD for the above recipients (sorted `kid` values joined with `.`): `9Miv3vUT2vQL0X80PyrLJm3bzGPuc_aKfPr4txRQIpA.Ev1dKdei9chrjW2-l4bjdXXF5GDZ7CqTcQlGg1W_U24.l4-wvmALQDp4g-UpilwCHmLZ_zUGfNawYSWQMoLphIk`
- Resulting AAD value (sha256 of above list raw, no padding, base64 URL encoded): `uLMTdeuniYvCFTQTamK0pZwFVgkJooGL37HZLm8PVkM`
- JWE:
```json
{
  "protected": "eyJjdHkiOiJhcHBsaWNhdGlvbi9kaWRjb21tLXBsYWluK2pzb24iLCJlbmMiOiJBMjU2R0NNIiwidHlwIjoiYXBwbGljYXRpb24vZGlkY29tbS1lbmNyeXB0ZWQranNvbiJ9",
  "recipients": [
    {
      "header": {
        "alg": "ECDH-ES+A256KW",
        "apu": "QWNnNWlNaUNjNkozMFg5R3lrTXl4R0dobFFrXzFhRlhJTDQ1cF9DT2l3ODVscFVyR1BOSnNKTVRrdTRHYnlMdndlam9jVHp5ZVZjMUxrX1RWa3o0UmZ4YQ",
        "apv": "OU1pdjN2VVQydlFMMFg4MFB5ckxKbTNiekdQdWNfYUtmUHI0dHhSUUlwQQ",
        "kid": "9Miv3vUT2vQL0X80PyrLJm3bzGPuc_aKfPr4txRQIpA",
        "epk": {
          "kty": "EC",
          "crv": "P-521",
          "x": "Acg5iMiCc6J30X9GykMyxGGhlQk_1aFXIL45p_COiw85lpUrGPNJsJMTku4GbyLvwejocTzyeVc1Lk_TVkz4Rfxa",
          "y": "AQgFgsVvOfebXZFk8TiBAJef9h6sVpQSJXed0xG3IolDYIllQ_OyQdlFpKHl2xCjgVxRihdf7mS_3SCzEtrcjEzy"
        }
      },
      "encrypted_key": "juXV2ZGX2MjF1FgjTWke3MTkODrdpqZ_k-5IVqZ568bvN12i8W_KaQ"
    },
    {
      "header": {
        "alg": "ECDH-ES+A256KW",
        "apu": "QVJLTGZTNWVoeUlacV9UWmJpbXdESndpYVBsckNMU2RqdG9aVFJSeTl0QVZQelQxbnlub1BYRWZIOHNNNklucDVKdWhvc3BHSVMxQzkzSk01Z1RkNzRtaQ",
        "apv": "OU1pdjN2VVQydlFMMFg4MFB5ckxKbTNiekdQdWNfYUtmUHI0dHhSUUlwQQ",
        "kid": "l4-wvmALQDp4g-UpilwCHmLZ_zUGfNawYSWQMoLphIk",
        "epk": {
          "kty": "EC",
          "crv": "P-521",
          "x": "ARKLfS5ehyIZq_TZbimwDJwiaPlrCLSdjtoZTRRy9tAVPzT1nynoPXEfH8sM6Inp5JuhospGIS1C93JM5gTd74mi",
          "y": "Ad5hB3rVVxTqvSsiN7NNbClumX-AWTV6r29CHz2Jbcgo5tunFz-5-CwP6EvQNkFrzrOxQ5ViOW5F3pYV-yoksLgO"
        }
      },
      "encrypted_key": "H-B3FBmwlGFIEtdfWti6tD8LwtuokxxPam5XO3V7wwWNoJ5sEy-LlA"
    },
    {
      "header": {
        "alg": "ECDH-ES+A256KW",
        "apu": "QWRTZUxrVWxadHpXRkNDODBvNVYtYTB3Mjl3MjM2OWtLRXlPbUtiQzItVlV4ZEo0OVdBUV9rTVhTempNaE1ON1VMc25mT3pEWFp1QkhwZUVRTU1zbWF5VA",
        "apv": "OU1pdjN2VVQydlFMMFg4MFB5ckxKbTNiekdQdWNfYUtmUHI0dHhSUUlwQQ",
        "kid": "Ev1dKdei9chrjW2-l4bjdXXF5GDZ7CqTcQlGg1W_U24",
        "epk": {
          "kty": "EC",
          "crv": "P-521",
          "x": "AdSeLkUlZtzWFCC80o5V-a0w29w2369kKEyOmKbC2-VUxdJ49WAQ_kMXSzjMhMN7ULsnfOzDXZuBHpeEQMMsmayT",
          "y": "AJKQo494spZjUW85ika3qNyLJJiv_J3FpsYnZt-Ml3q8IqXlHqQV_Nl3s7yn_pq8RWXl_yvo1NPiDWpoDMZ3sUNw"
        }
      },
      "encrypted_key": "53dtd9R0bbGK96jsPJRu2woQJC7-yBaN-xDw5xSp-pwpCKg1idnZ5w"
    }
  ],
  "aad": "uLMTdeuniYvCFTQTamK0pZwFVgkJooGL37HZLm8PVkM",
  "iv": "11_dMZoXv9OaPIR2",
  "ciphertext": "ofWv6sUZdYF3rX9A-jQ",
  "tag": "TyH-Abl3XTGlkUgjHCE-Vw"
}
```

#### 1.1.4 X25519 keys
- Recipient 1 key JWK format:
```json
{
  "kty": "OKP",
  "crv": "X25519",
  "x": "2kvTqkwVF-YSurN533fi-ZDF4PbLbqa7ohC--DJa0nA",
  "d": "sPUMndizynb_q6_u9fkbuU8V3I062-RlL114YnJ7KWY"
}
```
- Recipient 1 kid (jwk thumbprint raw base64 URL encoded): `eFf9x4K6jhnmAEvveQJo5rIQl32rZooOaNwlJsLf5JQ`
- Recipient 2 key JWK format:
```json
{
  "kty": "OKP",
  "crv": "X25519",
  "x": "cb-5cmxUy7xCfQCz0pEjYOGJOp0nf3cH7TU6siQ49wU",
  "d": "oCw27m5T-QPr48F_f-CRWWqFgtFxpPISExMhSYQJmF8"
}
```
- Recipient 2 kid (jwk thumbprint raw base64 URL encoded): `NaUTcaFDyI3Ss48zMmeg1Dal0vhUpOYpWdwfKd2T2S8`
- Recipient 3 key JWK format:
```json
{
  "kty": "OKP",
  "crv": "X25519",
  "x": "pW_fX347OhGgYURSvuM5-NSKw7CgHzCuOZt5ovQCa3E",
  "d": "sEZYN-iNbQ22ds1fC_hYgrp7PKbzAtiHqxPhvzon9HE"
}
```
- Recipient 3 kid (jwk thumbprint raw, no padding, base64 URL encoded): `hzSul1PikxGRl7k_QdDfCCRMZP4POmt5eNYN0pbjSzE`
- List of kids used for AAD for the above recipients (sorted `kid` values joined with `.`): `NaUTcaFDyI3Ss48zMmeg1Dal0vhUpOYpWdwfKd2T2S8.eFf9x4K6jhnmAEvveQJo5rIQl32rZooOaNwlJsLf5JQ.hzSul1PikxGRl7k_QdDfCCRMZP4POmt5eNYN0pbjSzE`
- Resulting AAD value (sha256 of above list raw, no padding, base64 URL encoded): `7iRNh25gyaA9Bpnx7axAbyyvbh-bXaPOz8SgvgGksNc`
- JWE:
```json
{
  "protected": "eyJjdHkiOiJhcHBsaWNhdGlvbi9kaWRjb21tLXBsYWluK2pzb24iLCJlbmMiOiJBMjU2R0NNIiwidHlwIjoiYXBwbGljYXRpb24vZGlkY29tbS1lbmNyeXB0ZWQranNvbiJ9",
  "recipients": [
    {
      "header": {
        "alg": "ECDH-ES+A256KW",
        "apu": "Q21aM1gzRFBnZFdQWjRKZFF4VVNMSjBKaEtRRXpJZWphV2cxT04tSE13WQ",
        "apv": "ZUZmOXg0SzZqaG5tQUV2dmVRSm81cklRbDMyclpvb09hTndsSnNMZjVKUQ",
        "kid": "eFf9x4K6jhnmAEvveQJo5rIQl32rZooOaNwlJsLf5JQ",
        "epk": {
          "kty": "OKP",
          "crv": "X25519",
          "x": "CmZ3X3DPgdWPZ4JdQxUSLJ0JhKQEzIejaWg1ON-HMwY"
        }
      },
      "encrypted_key": "ZFibn07y4G88HTB6haGfKJLQGWi2a25UVlioG93hgjs2BDIRaWRqzw"
    },
    {
      "header": {
        "alg": "ECDH-ES+A256KW",
        "apu": "cU9MdWVjZmdaamJkOVRQYV9qbG5CeFAyak9FQjdOVkZKaGZ6UEk1OFNWOA",
        "apv": "ZUZmOXg0SzZqaG5tQUV2dmVRSm81cklRbDMyclpvb09hTndsSnNMZjVKUQ",
        "kid": "NaUTcaFDyI3Ss48zMmeg1Dal0vhUpOYpWdwfKd2T2S8",
        "epk": {
          "kty": "OKP",
          "crv": "X25519",
          "x": "qOLuecfgZjbd9TPa_jlnBxP2jOEB7NVFJhfzPI58SV8"
        }
      },
      "encrypted_key": "EKpcwck9zE0WjEq9E60dm_OJY0U2e1UlUAZE8LYfURo_saE2yzxx_A"
    },
    {
      "header": {
        "alg": "ECDH-ES+A256KW",
        "apu": "RE1IOGFVVlpUZ2FXaFNaOUFtdFNDQ2M1aUZEbERCeDZnMC1URHpUTFZYUQ",
        "apv": "ZUZmOXg0SzZqaG5tQUV2dmVRSm81cklRbDMyclpvb09hTndsSnNMZjVKUQ",
        "kid": "hzSul1PikxGRl7k_QdDfCCRMZP4POmt5eNYN0pbjSzE",
        "epk": {
          "kty": "OKP",
          "crv": "X25519",
          "x": "DMH8aUVZTgaWhSZ9AmtSCCc5iFDlDBx6g0-TDzTLVXQ"
        }
      },
      "encrypted_key": "OeemM4fMI9538IcvG3OwhuVtugrRIoIJEB5iAVZBl7Q59yRr5VZTPQ"
    }
  ],
  "aad": "7iRNh25gyaA9Bpnx7axAbyyvbh-bXaPOz8SgvgGksNc",
  "iv": "9deRACZyiau7rIIc",
  "ciphertext": "ombMWgwtw2QSfALdiDk",
  "tag": "yRwaSiGsQCqYjIdMSwPPNg"
}
```

### 1.2 Single Recipient JWEs

Packing a message with 1 recipient using the **Flattened JWE JSON serialization** and **Compact JWE serialization** formats as mentioned in the [notes](#notes) above.

#### 1.2.1 NIST P-256 key
- Single Recipient key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-256",
  "x": "2fpy_fK5FCsap0EbU1Om7QXoVoyvBv8gfdHY3ufIS9w",
  "y": "TtVOc9c8ejMeqeaUs1CMS79w0-Al02Fw25WdVEb0DiI",
  "d": "kEWLCAyDL8mgDLNnlb1am_B8wcaGAe7ViXx1tqKWTVc"
}
```
- Single Recipient kid (jwk thumbprint raw base64 URL encoded): `s6-ZhI1hpx0kM3pDgOrVQs6mRd_8KfEXUkLg8lK7XNA`
- Finally, packing the payload outputs the following flattened serialized JWE JSON:
```json
{
  "protected": "eyJhbGciOiJFQ0RILUVTK0EyNTZLVyIsImFwdSI6IlJuY3lOa2RuVkZJME0ycHhORnB4Wm1GUlJqQkxjMk54U2poNlpFeFliMTlyVm0xZlNtRkJVbHBHVlEiLCJhcHYiOiJjell0V21oSk1XaHdlREJyVFROd1JHZFBjbFpSY3padFVtUmZPRXRtUlZoVmEweG5PR3hMTjFoT1FRIiwiY3R5IjoiYXBwbGljYXRpb24vZGlkY29tbS1wbGFpbitqc29uIiwiZW5jIjoiQTI1NkdDTSIsImVwayI6eyJjcnYiOiJQLTI1NiIsImt0eSI6IkVDIiwieCI6IkZ3MjZHZ1RSNDNqcTRacWZhUUYwS3NjcUo4emRMWG9fa1ZtX0phQVJaRlUiLCJ5IjoiNENfMk00V2dkcVp5cGdkaVVpMlZCQWsyVXFmYlJvU1AxaUQ3WHIzVGJJZyJ9LCJraWQiOiJzNi1aaEkxaHB4MGtNM3BEZ09yVlFzNm1SZF84S2ZFWFVrTGc4bEs3WE5BIiwidHlwIjoiYXBwbGljYXRpb24vZGlkY29tbS1lbmNyeXB0ZWQranNvbiJ9",
  "encrypted_key": "l99n6MvHGvUKRrPORElnlerqmmhQc1WMzJ2pxt6H5gaSWPPsj4Gp0A",
  "iv": "CKm9svwMrrXarfG2",
  "ciphertext": "k_eAXa-uMtMYSVgJO0A",
  "tag": "1cYhCprkvxYYfyNp_fJGUQ"
}
```
- The compact serialization of this envelope is:
`eyJhbGciOiJFQ0RILUVTK0EyNTZLVyIsImFwdSI6IlJuY3lOa2RuVkZJME0ycHhORnB4Wm1GUlJqQkxjMk54U2poNlpFeFliMTlyVm0xZlNtRkJVbHBHVlEiLCJhcHYiOiJjell0V21oSk1XaHdlREJyVFROd1JHZFBjbFpSY3padFVtUmZPRXRtUlZoVmEweG5PR3hMTjFoT1FRIiwiY3R5IjoiYXBwbGljYXRpb24vZGlkY29tbS1wbGFpbitqc29uIiwiZW5jIjoiQTI1NkdDTSIsImVwayI6eyJrdHkiOiJFQyIsImNydiI6IlAtMjU2IiwieCI6IkZ3MjZHZ1RSNDNqcTRacWZhUUYwS3NjcUo4emRMWG9fa1ZtX0phQVJaRlUiLCJ5IjoiNENfMk00V2dkcVp5cGdkaVVpMlZCQWsyVXFmYlJvU1AxaUQ3WHIzVGJJZyJ9LCJraWQiOiJzNi1aaEkxaHB4MGtNM3BEZ09yVlFzNm1SZF84S2ZFWFVrTGc4bEs3WE5BIiwidHlwIjoiYXBwbGljYXRpb24vZGlkY29tbS1lbmNyeXB0ZWQranNvbiJ9.l99n6MvHGvUKRrPORElnlerqmmhQc1WMzJ2pxt6H5gaSWPPsj4Gp0A.CKm9svwMrrXarfG2.k_eAXa-uMtMYSVgJO0A.1cYhCprkvxYYfyNp_fJGUQ`
- The single recipient's headers are merged into the `protected` header, which base64 URL decoded equals to (pretty printed for readability):
```json
{
  "alg": "ECDH-ES+A256KW",
  "apu": "RncyNkdnVFI0M2pxNFpxZmFRRjBLc2NxSjh6ZExYb19rVm1fSmFBUlpGVQ",
  "apv": "czYtWmhJMWhweDBrTTNwRGdPclZRczZtUmRfOEtmRVhVa0xnOGxLN1hOQQ",
  "cty": "application/didcomm-plain+json",
  "enc": "A256GCM",
  "epk": {
    "kty": "EC",
    "crv": "P-256",
    "x": "Fw26GgTR43jq4ZqfaQF0KscqJ8zdLXo_kVm_JaARZFU",
    "y": "4C_2M4WgdqZypgdiUi2VBAk2UqfbRoSP1iD7Xr3TbIg"
  },
  "kid": "s6-ZhI1hpx0kM3pDgOrVQs6mRd_8KfEXUkLg8lK7XNA",
  "typ": "application/didcomm-encrypted+json"
}
```

#### 1.2.2 NIST P-384 key
- Single Recipient key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-384",
  "x": "lb17x-OBz2i1kQbkRtSKD3TY1MwIfUMyM8YtqXZXMj884hLJH2QtxmUWKyXIprcn",
  "y": "PlT4CInTrA5zAroqwyww0BL6EipnEBTrtbWID8nADz6LFpf_27qlxIARy_iU5OcN",
  "d": "JJgpIqGS5JuiKRnsEgGNlYw39pz-XGrsrmniuxlSik0BLwdb8-0K8Xxuqo6yW6NE"
}
```
- Single Recipient kid (jwk thumbprint raw base64 URL encoded): `8wPpWWlLiMBYltw6AoWG3Z_SfgWmXanBHSwZFpQJ0Q0`
- Finally, packing the payload outputs the following flattened serialized JWE JSON:
```json
{
  "protected": "eyJhbGciOiJFQ0RILUVTK0EyNTZLVyIsImFwdSI6ImNWSkZUMncwWTI5bmJUUkZhWGd3TURGd04zSXpaREl5U0VaQ2FXcHZOV2hmT1RGRE9HOTNjVU5yU2pSdlZWZzFRemh6ZUdOd00zTlhTMXBEZEZaWU13IiwiYXB2IjoiT0hkUWNGZFhiRXhwVFVKWmJIUjNOa0Z2VjBjeldsOVRabWRYYlZoaGJrSklVM2RhUm5CUlNqQlJNQSIsImN0eSI6ImFwcGxpY2F0aW9uL2RpZGNvbW0tcGxhaW4ranNvbiIsImVuYyI6IkEyNTZHQ00iLCJlcGsiOnsiY3J2IjoiUC0zODQiLCJrdHkiOiJFQyIsIngiOiJxUkVPbDRjb2dtNEVpeDAwMXA3cjNkMjJIRkJpam81aF85MUM4b3dxQ2tKNG9VWDVDOHN4Y3Azc1dLWkN0VlgzIiwieSI6Im5FbmRyZXVPNVFEWFp5eGVmWkJWRDhJeU53WkJER1AwZlJHdXN1LWZXV0NmWlJBdUVsNkZIaXMtSFRNS1puY0UifSwia2lkIjoiOHdQcFdXbExpTUJZbHR3NkFvV0czWl9TZmdXbVhhbkJIU3daRnBRSjBRMCIsInR5cCI6ImFwcGxpY2F0aW9uL2RpZGNvbW0tZW5jcnlwdGVkK2pzb24ifQ",
  "encrypted_key": "OyvZQT0HdCIgDTQKgSbnMfX6iQvPVkOlurgNRqyZlyxj6XeZROYCEQ",
  "iv": "sGHLr4VNPKylOCn7",
  "ciphertext": "mfnbfoMx8LfXaWSY5po",
  "tag": "_FxUsJeY06_bzGJ9vaAtMA"
}
```
- The compact serialization of this envelope is:
  `eyJhbGciOiJFQ0RILUVTK0EyNTZLVyIsImFwdSI6ImNWSkZUMncwWTI5bmJUUkZhWGd3TURGd04zSXpaREl5U0VaQ2FXcHZOV2hmT1RGRE9HOTNjVU5yU2pSdlZWZzFRemh6ZUdOd00zTlhTMXBEZEZaWU13IiwiYXB2IjoiT0hkUWNGZFhiRXhwVFVKWmJIUjNOa0Z2VjBjeldsOVRabWRYYlZoaGJrSklVM2RhUm5CUlNqQlJNQSIsImN0eSI6ImFwcGxpY2F0aW9uL2RpZGNvbW0tcGxhaW4ranNvbiIsImVuYyI6IkEyNTZHQ00iLCJlcGsiOnsia3R5IjoiRUMiLCJjcnYiOiJQLTM4NCIsIngiOiJxUkVPbDRjb2dtNEVpeDAwMXA3cjNkMjJIRkJpam81aF85MUM4b3dxQ2tKNG9VWDVDOHN4Y3Azc1dLWkN0VlgzIiwieSI6Im5FbmRyZXVPNVFEWFp5eGVmWkJWRDhJeU53WkJER1AwZlJHdXN1LWZXV0NmWlJBdUVsNkZIaXMtSFRNS1puY0UifSwia2lkIjoiOHdQcFdXbExpTUJZbHR3NkFvV0czWl9TZmdXbVhhbkJIU3daRnBRSjBRMCIsInR5cCI6ImFwcGxpY2F0aW9uL2RpZGNvbW0tZW5jcnlwdGVkK2pzb24ifQ.OyvZQT0HdCIgDTQKgSbnMfX6iQvPVkOlurgNRqyZlyxj6XeZROYCEQ.sGHLr4VNPKylOCn7.mfnbfoMx8LfXaWSY5po._FxUsJeY06_bzGJ9vaAtMA`
- The single recipient's headers are merged into the `protected` header, which base64 URL decoded equals to (pretty printed for readability):
```json
{
  "alg": "ECDH-ES+A256KW",
  "apu": "cVJFT2w0Y29nbTRFaXgwMDFwN3IzZDIySEZCaWpvNWhfOTFDOG93cUNrSjRvVVg1QzhzeGNwM3NXS1pDdFZYMw",
  "apv": "OHdQcFdXbExpTUJZbHR3NkFvV0czWl9TZmdXbVhhbkJIU3daRnBRSjBRMA",
  "cty": "application/didcomm-plain+json",
  "enc": "A256GCM",
  "epk": {
    "kty": "EC",
    "crv": "P-384",
    "x": "qREOl4cogm4Eix001p7r3d22HFBijo5h_91C8owqCkJ4oUX5C8sxcp3sWKZCtVX3",
    "y": "nEndreuO5QDXZyxefZBVD8IyNwZBDGP0fRGusu-fWWCfZRAuEl6FHis-HTMKZncE"
  },
  "kid": "8wPpWWlLiMBYltw6AoWG3Z_SfgWmXanBHSwZFpQJ0Q0",
  "typ": "application/didcomm-encrypted+json"
}
```

#### 1.2.3 NIST P-521 key
- Single Recipient key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-521",
  "x": "AHrw8TsyZzIkINFPCAS54Y7UoCI1XAlim95ROPykpjo4q2LvW_VWeBtJLU2SuqTFG4WX9VBzMg5Rq4gMj4oCpMFb",
  "y": "AUs4vywsYYuRP0LhFvyI_ippvSY6Tv1S8sEzojd41Ubo86bFlCj5c_wHX2N6hplMU01WAcebPWc24plqF39pkNrK",
  "d": "AEklgm76AbNl_nydbcINMgytfoZGRMI1mxfGcIiqw-KHENQMtlujImJrKMUd32njHS1M9e-WqAS8AHLoVdBZmkOo"
}
```
- Single Recipient kid (jwk thumbprint raw base64 URL encoded): `9Miv3vUT2vQL0X80PyrLJm3bzGPuc_aKfPr4txRQIpAs`
- Finally, packing the payload outputs the following flattened serialized JWE JSON:
```json
{
  "protected": "eyJhbGciOiJFQ0RILUVTK0EyNTZLVyIsImFwdSI6ImRsRjZWRnBMWTFSS2JqUlROM0Z6Y0dGMFRGVldaR3hSVTB4clQyaDJUV2RuU0ZsaFRUaEZNRzFwZWpFemJtUXphRlEwUVVoR01XUm9WRWRPYTI5M09HUnlTVFZEU200dGRsbHdlbUZYWnkxcVoxSXRhWFEwIiwiYXB2IjoiT1UxcGRqTjJWVlF5ZGxGTU1GZzRNRkI1Y2t4S2JUTmlla2RRZFdOZllVdG1VSEkwZEhoU1VVbHdRUSIsImN0eSI6ImFwcGxpY2F0aW9uL2RpZGNvbW0tcGxhaW4ranNvbiIsImVuYyI6IkEyNTZHQ00iLCJlcGsiOnsiY3J2IjoiUC01MjEiLCJrdHkiOiJFQyIsIngiOiJBTDBNMDJTbkV5Wi1FdTZyS1dyUzFGWFpVRWk1RG9ieklJQjJHalBCTkpvczlkNTNkNFUtQUJ4ZFhZVXhqWktNUEhheU9RaVpfcjJLYzJsb1BvNEVmb3JlIiwieSI6IkFXSkxvVnNTS0l6SVF2VWtKVzIxakVmV2ZHTjhWck1tN2owSmtJb2JUVXlCSEJMa0o3SzFUU19zZ1FpOUkxb0tzRTJ5Mjh2WC1DREFKZGp3Z1FWNl9mLTIifSwia2lkIjoiOU1pdjN2VVQydlFMMFg4MFB5ckxKbTNiekdQdWNfYUtmUHI0dHhSUUlwQSIsInR5cCI6ImFwcGxpY2F0aW9uL2RpZGNvbW0tZW5jcnlwdGVkK2pzb24ifQ",
  "encrypted_key": "rK_MtxEobFF8pyYU8T26U7LRlEdjm1ndq8sZoZ2h9BaAyuhE7bcuAA",
  "iv": "X1V-4vkZ1qE3_Yhn",
  "ciphertext": "XDf5mmhlDaJfTOp1z_4",
  "tag": "se7e3wH5grcMEuJIAJbN9A"
}
```
- The compact serialization of this envelope is:
  `eyJhbGciOiJFQ0RILUVTK0EyNTZLVyIsImFwdSI6ImRsRjZWRnBMWTFSS2JqUlROM0Z6Y0dGMFRGVldaR3hSVTB4clQyaDJUV2RuU0ZsaFRUaEZNRzFwZWpFemJtUXphRlEwUVVoR01XUm9WRWRPYTI5M09HUnlTVFZEU200dGRsbHdlbUZYWnkxcVoxSXRhWFEwIiwiYXB2IjoiT1UxcGRqTjJWVlF5ZGxGTU1GZzRNRkI1Y2t4S2JUTmlla2RRZFdOZllVdG1VSEkwZEhoU1VVbHdRUSIsImN0eSI6ImFwcGxpY2F0aW9uL2RpZGNvbW0tcGxhaW4ranNvbiIsImVuYyI6IkEyNTZHQ00iLCJlcGsiOnsia3R5IjoiRUMiLCJjcnYiOiJQLTUyMSIsIngiOiJBTDBNMDJTbkV5Wi1FdTZyS1dyUzFGWFpVRWk1RG9ieklJQjJHalBCTkpvczlkNTNkNFUtQUJ4ZFhZVXhqWktNUEhheU9RaVpfcjJLYzJsb1BvNEVmb3JlIiwieSI6IkFXSkxvVnNTS0l6SVF2VWtKVzIxakVmV2ZHTjhWck1tN2owSmtJb2JUVXlCSEJMa0o3SzFUU19zZ1FpOUkxb0tzRTJ5Mjh2WC1DREFKZGp3Z1FWNl9mLTIifSwia2lkIjoiOU1pdjN2VVQydlFMMFg4MFB5ckxKbTNiekdQdWNfYUtmUHI0dHhSUUlwQSIsInR5cCI6ImFwcGxpY2F0aW9uL2RpZGNvbW0tZW5jcnlwdGVkK2pzb24ifQ.rK_MtxEobFF8pyYU8T26U7LRlEdjm1ndq8sZoZ2h9BaAyuhE7bcuAA.X1V-4vkZ1qE3_Yhn.XDf5mmhlDaJfTOp1z_4.se7e3wH5grcMEuJIAJbN9A`
- The single recipient's headers are merged into the `protected` header, which base64 URL decoded equals to (pretty printed for readability):
```json
{
  "alg": "ECDH-ES+A256KW",
  "apu": "dlF6VFpLY1RKbjRTN3FzcGF0TFVWZGxRU0xrT2h2TWdnSFlhTThFMG1pejEzbmQzaFQ0QUhGMWRoVEdOa293OGRySTVDSm4tdllwemFXZy1qZ1ItaXQ0",
  "apv": "OU1pdjN2VVQydlFMMFg4MFB5ckxKbTNiekdQdWNfYUtmUHI0dHhSUUlwQQ",
  "cty": "application/didcomm-plain+json",
  "enc": "A256GCM",
  "epk": {
    "kty": "EC",
    "crv": "P-521",
    "x": "AL0M02SnEyZ-Eu6rKWrS1FXZUEi5DobzIIB2GjPBNJos9d53d4U-ABxdXYUxjZKMPHayOQiZ_r2Kc2loPo4Efore",
    "y": "AWJLoVsSKIzIQvUkJW21jEfWfGN8VrMm7j0JkIobTUyBHBLkJ7K1TS_sgQi9I1oKsE2y28vX-CDAJdjwgQV6_f-2"
  },
  "kid": "9Miv3vUT2vQL0X80PyrLJm3bzGPuc_aKfPr4txRQIpA",
  "typ": "application/didcomm-encrypted+json"
}
```

#### 1.2.4 X25519 key
- Single Recipient key JWK format:
```json
{
  "kty": "OKP",
  "crv": "X25519",
  "x": "2kvTqkwVF-YSurN533fi-ZDF4PbLbqa7ohC--DJa0nA",
  "d": "sPUMndizynb_q6_u9fkbuU8V3I062-RlL114YnJ7KWY"
}
```
- Single Recipient kid (jwk thumbprint raw base64 URL encoded): `eFf9x4K6jhnmAEvveQJo5rIQl32rZooOaNwlJsLf5JQ`
- Finally, packing the payload outputs the following flattened serialized JWE JSON:
```json
{
  "protected": "eyJhbGciOiJFQ0RILUVTK0EyNTZLVyIsImFwdSI6IlluQldTM1IyVDJoWGJXOVRRMUJTV21oUk1HdFVaVzlYVDNFMWVrMXZTWGxhY0RCMVlrOU9XVTVXZHciLCJhcHYiOiJaVVptT1hnMFN6WnFhRzV0UVVWMmRtVlJTbTgxY2tsUmJETXljbHB2YjA5aFRuZHNTbk5NWmpWS1VRIiwiY3R5IjoiYXBwbGljYXRpb24vZGlkY29tbS1wbGFpbitqc29uIiwiZW5jIjoiQTI1NkdDTSIsImVwayI6eyJjcnYiOiJYMjU1MTkiLCJrdHkiOiJPS1AiLCJ4IjoiYnBWS3R2T2hXbW9TQ1BSWmhRMGtUZW9XT3E1ek1vSXlacDB1Yk9OWU5WdyJ9LCJraWQiOiJlRmY5eDRLNmpobm1BRXZ2ZVFKbzVySVFsMzJyWm9vT2FOd2xKc0xmNUpRIiwidHlwIjoiYXBwbGljYXRpb24vZGlkY29tbS1lbmNyeXB0ZWQranNvbiJ9",
  "encrypted_key": "Pe7sGWcXxY9V7xdKWdpa5GvVinr_YWITRIVY8ic7WmKwY-Lh-3OJdA",
  "iv": "Rx__OGcTo72Lv6jG",
  "ciphertext": "UEFI2_OqNMki1cXraJA",
  "tag": "Hc6WxwF2YGvewcWFmhzkrw"
}
```
- The compact serialization of this envelope is:
  `eyJhbGciOiJFQ0RILUVTK0EyNTZLVyIsImFwdSI6IlluQldTM1IyVDJoWGJXOVRRMUJTV21oUk1HdFVaVzlYVDNFMWVrMXZTWGxhY0RCMVlrOU9XVTVXZHciLCJhcHYiOiJaVVptT1hnMFN6WnFhRzV0UVVWMmRtVlJTbTgxY2tsUmJETXljbHB2YjA5aFRuZHNTbk5NWmpWS1VRIiwiY3R5IjoiYXBwbGljYXRpb24vZGlkY29tbS1wbGFpbitqc29uIiwiZW5jIjoiQTI1NkdDTSIsImVwayI6eyJrdHkiOiJPS1AiLCJjcnYiOiJYMjU1MTkiLCJ4IjoiYnBWS3R2T2hXbW9TQ1BSWmhRMGtUZW9XT3E1ek1vSXlacDB1Yk9OWU5WdyJ9LCJraWQiOiJlRmY5eDRLNmpobm1BRXZ2ZVFKbzVySVFsMzJyWm9vT2FOd2xKc0xmNUpRIiwidHlwIjoiYXBwbGljYXRpb24vZGlkY29tbS1lbmNyeXB0ZWQranNvbiJ9.Pe7sGWcXxY9V7xdKWdpa5GvVinr_YWITRIVY8ic7WmKwY-Lh-3OJdA.Rx__OGcTo72Lv6jG.UEFI2_OqNMki1cXraJA.Hc6WxwF2YGvewcWFmhzkrw`
- The single recipient's headers are merged into the `protected` header, which base64 URL decoded equals to (pretty printed for readability):
```json
{
  "alg": "ECDH-ES+A256KW",
  "apu": "YnBWS3R2T2hXbW9TQ1BSWmhRMGtUZW9XT3E1ek1vSXlacDB1Yk9OWU5Wdw",
  "apv": "ZUZmOXg0SzZqaG5tQUV2dmVRSm81cklRbDMyclpvb09hTndsSnNMZjVKUQ",
  "cty": "application/didcomm-plain+json",
  "enc": "A256GCM",
  "epk": {
    "kty": "OKP",
    "crv": "X25519",
    "x": "bpVKtvOhWmoSCPRZhQ0kTeoWOq5zMoIyZp0ubONYNVw"
  },
  "kid": "eFf9x4K6jhnmAEvveQJo5rIQl32rZooOaNwlJsLf5JQ",
  "typ": "application/didcomm-encrypted+json"
}
```

## 2 XC20P content encryption

### 2.1 Multi recipients JWEs

The packer generates the following protected headers for XC20P content encryption in the below examples with XC20P enc:
- Generated protected headers: `{"cty":"application/didcomm-plain+json","enc":"XC20P","typ":"application/didcomm-encrypted+json"}`
  - raw (no padding) base64URL encoded: `eyJjdHkiOiJhcHBsaWNhdGlvbi9kaWRjb21tLXBsYWluK2pzb24iLCJlbmMiOiJYQzIwUCIsInR5cCI6ImFwcGxpY2F0aW9uL2RpZGNvbW0tZW5jcnlwdGVkK2pzb24ifQ`

The same [notes](#notes) above apply here.

#### 2.1.1 NIST P-256 keys
- Recipient 1 key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-256",
  "x": "kdAHozUe6HOhNC9_jsOI60FuHa64zHSwcZa0l22rXX4",
  "y": "Sj3iIz_HimnXgLRWU-x_gXjVyF2R0rh6OhuD3gzhUMw",
  "d": "NTV27xYkYkwDNYePKHlh6CIYHunx-6rn80cSATOI7rI"
}
```
- Recipient 1 kid (jwk thumbprint raw base64 URL encoded): `Ivxk0K5tz7csR7MDXllXWd7YJTQF4pS8IHHkIdepgpk`
- Recipient 2 key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-256",
  "x": "sx1ZNsP2rUKuoN0Xe6m2_Zly8wM_-CpuCkDNaOjFYtA",
  "y": "lTti40XRekPxw4IfpheZDCxilwEoEWWxyO8d77W_sOo",
  "d": "WsHT1GiMy4mxsxQ7mPYtg5Mn18I8PU2wHPttVGEOnXk"
}
```
- Recipient 2 kid (jwk thumbprint raw base64 URL encoded): `tkAt85t250uQ3Q3d8W731YJfqF0t1cCwGwWqRxqyQhM`
- Recipient 3 key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-256",
  "x": "AQoZIqg1y0fZ1qvYM5YuinxRtOXa6dMSXfgdYBgsEks",
  "y": "JRxsX-U6go0VqWtMFCPFbUNSsLJYiQH7ij2i4-FVQh0",
  "d": "Joal2Lk5w6-_C_HpRr__ZtxtJccwjwHZ7RxZe1-CTjY"
}
```
- Recipient 3 kid (jwk thumbprint raw, no padding, base64 URL encoded): `SoySkmiLdE4c7Dp5URlH-DMVNq6-fGrkSpIgzLTYez0`
- List of kids used for AAD for the above recipients (sorted `kid` values joined with `.`): `Ivxk0K5tz7csR7MDXllXWd7YJTQF4pS8IHHkIdepgpk.SoySkmiLdE4c7Dp5URlH-DMVNq6-fGrkSpIgzLTYez0.tkAt85t250uQ3Q3d8W731YJfqF0t1cCwGwWqRxqyQhM`
- Resulting AAD value (sha256 of above list raw, no padding, base64 URL encoded): `uPokzMsXWxloZTnb2sXzz05KBc_SI1giMmHAenTyMjQ`
- Finally, packing the payload outputs the following JWE (pretty printed for readability):
```json
{
  "protected": "eyJjdHkiOiJhcHBsaWNhdGlvbi9kaWRjb21tLXBsYWluK2pzb24iLCJlbmMiOiJYQzIwUCIsInR5cCI6ImFwcGxpY2F0aW9uL2RpZGNvbW0tZW5jcnlwdGVkK2pzb24ifQ",
  "recipients": [
    {
      "header": {
        "alg": "ECDH-ES+XC20PKW",
        "apu": "R1NNbnFqcGFQMlltUlRNRTVrNVhYT3E2M3FzZjd2emVtbnY5NENVTm9faw",
        "apv": "SXZ4azBLNXR6N2NzUjdNRFhsbFhXZDdZSlRRRjRwUzhJSEhrSWRlcGdwaw",
        "kid": "Ivxk0K5tz7csR7MDXllXWd7YJTQF4pS8IHHkIdepgpk",
        "epk": {
          "kty": "EC",
          "crv": "P-256",
          "x": "GSMnqjpaP2YmRTME5k5XXOq63qsf7vzemnv94CUNo_k",
          "y": "tDCIMv5gZqyjZmHYvbHxUQO1zN7fH0n9athoWGlO8nI"
        }
      },
      "encrypted_key": "n63_NKMEy_KOb_34nrTX_Yvbx3Sliee9yh3ZSqs6nm5vhAuCoBMoU40fSpZMB07QLdXKfrRjB4A-WoL_MjTpcpOZnxc1v2s-"
    },
    {
      "header": {
        "alg": "ECDH-ES+XC20PKW",
        "apu": "N1ZNVG00NEFqc0J3amt6WU1STDk5SURRZUh6aWZaa0Q5Q0hSajJJdGtkOA",
        "apv": "SXZ4azBLNXR6N2NzUjdNRFhsbFhXZDdZSlRRRjRwUzhJSEhrSWRlcGdwaw",
        "kid": "tkAt85t250uQ3Q3d8W731YJfqF0t1cCwGwWqRxqyQhM",
        "epk": {
          "kty": "EC",
          "crv": "P-256",
          "x": "7VMTm44AjsBwjkzYMRL99IDQeHzifZkD9CHRj2Itkd8",
          "y": "NnVWH1gP7qdqzv4Go-1lT_U02i6fJHhmZO33jt4R0Ys"
        }
      },
      "encrypted_key": "V3Y_kLiogDKAa4p3MNyfh1IOfexv8rLJsZf5idwI2wJDngYzhNyzaV4kqJMMW6qyMaE4bX5LY-qRP4sPcYPwntMj70LUaC6I"
    },
    {
      "header": {
        "alg": "ECDH-ES+XC20PKW",
        "apu": "NzJQTnJ4a1A2V3JCcV9wUkU4VU42T0I3WHFKUXJuZEZHZ3dERVloR21kdw",
        "apv": "SXZ4azBLNXR6N2NzUjdNRFhsbFhXZDdZSlRRRjRwUzhJSEhrSWRlcGdwaw",
        "kid": "SoySkmiLdE4c7Dp5URlH-DMVNq6-fGrkSpIgzLTYez0",
        "epk": {
          "kty": "EC",
          "crv": "P-256",
          "x": "72PNrxkP6WrBq_pRE8UN6OB7XqJQrndFGgwDEYhGmdw",
          "y": "gDy2dRBTwt1tQBBSnztN0AqvzCu07yFN9FgG109ytsc"
        }
      },
      "encrypted_key": "2b4op-H7wPoyzno3Krv65rOal2HNmaiDHnjGTywcHAppz-EgHS7hiqANeRCipCNhPj7VvZqe1PWf2m0qLIdBuUv7ryo_nw9E"
    }
  ],
  "aad": "uPokzMsXWxloZTnb2sXzz05KBc_SI1giMmHAenTyMjQ",
  "iv": "KShKEagQokU3UTGeYXw7LwWFankH-zK7",
  "ciphertext": "6Z5YKgYQSmxSCtns064",
  "tag": "hhW1Y5WgRM2t8-NiUMmKJw"
}
```

#### 2.1.2 NIST P-384 keys
- Recipient 1 key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-384",
  "x": "5aCpGZXwubdOSedZl1wc5PHB175a990-bRo2QKzju6uyeXD6hBKcB6vUijQRILMr",
  "y": "TeUA_qsYU8YmbHPA58QJuAJiUe0BEbi8Vuq88ZEWLudhJa4Dp5mBKuFEeJQcOQCa",
  "d": "wTv7Yh4bZAfCfmz0qL_lKJNlMRYuXjWzE63p7y3mZW8DRtN5LgOE25QKO9v0xgKN"
}
```
- Recipient 1 kid (jwk thumbprint raw base64 URL encoded): `35E0yg0TinUSym5bQ5FnUgWirIrfK81p-QCxW7VzCrE`
- Recipient 2 key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-384",
  "x": "xYFotAHw0kaqsgkW-3ZirL2p3HC0tJCrrNsK-1MfgoUahWpoDiUpEapuLZrO_hz3",
  "y": "LLUQ5gRSwn5x0sQJrByWSdWdqojAhizpsx9GPjvPP9uM4gv7jKUEoi0A-2doNSQR",
  "d": "OLPQ8giwvg-pKMMaYTGB3O4RGNPtlX-tRZi3ltUb305nPMsuxplI71OQfTH3-Leq"
}
```
- Recipient 2 kid (jwk thumbprint raw base64 URL encoded): `wnJRuK09BydTKCPX9DEsf2hxSB1uzHdHrjLTtsiPUZw`
- Recipient 3 key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-384",
  "x": "DWdQi5HdkPpUEqHtQrLU8xR6hW3_IO-8RPcOY4_aI0VACCO9e8WNCFAcjAja5Q8Y",
  "y": "jTan4mkzX1uRU9FRIvZgE1NKS-fUe86cl_xmLJ2jPl-A-EXmTHExVT8q63iVnvSC",
  "d": "WnCGfWiiOCglkYWQh1t-KM_A8Pb_HXgUXEJFjg7iWT3SYUL2tgMQQ5w9IUNE-D0r"
}
```
- Recipient 3 kid (jwk thumbprint raw, no padding, base64 URL encoded): `j9ZMlUQX9m9t8_6RmshAfMwHTIOE9_0Mv5bd5bQ4nKw`
- List of kids used for AAD for the above recipients (sorted `kid` values joined with `.`): `35E0yg0TinUSym5bQ5FnUgWirIrfK81p-QCxW7VzCrE.j9ZMlUQX9m9t8_6RmshAfMwHTIOE9_0Mv5bd5bQ4nKw.wnJRuK09BydTKCPX9DEsf2hxSB1uzHdHrjLTtsiPUZw`
- Resulting AAD value (sha256 of above list raw, no padding, base64 URL encoded): `kOd8LfamiqCqZa4kZJPR0M3k11OjHo1dQgdgaI2HreU`
- JWE (pretty printed for readability):
```json
{
  "protected": "eyJjdHkiOiJhcHBsaWNhdGlvbi9kaWRjb21tLXBsYWluK2pzb24iLCJlbmMiOiJYQzIwUCIsInR5cCI6ImFwcGxpY2F0aW9uL2RpZGNvbW0tZW5jcnlwdGVkK2pzb24ifQ",
  "recipients": [
    {
      "header": {
        "alg": "ECDH-ES+XC20PKW",
        "apu": "Zmw3NTdwRFlKVE16YlcwVmdfUWgzTDlrZlRoQ25Dd25uaU81YlBmVkwwUFgxV19LbWpfRzVIT2VDV2NyMEdacQ",
        "apv": "MzVFMHlnMFRpblVTeW01YlE1Rm5VZ1dpcklyZks4MXAtUUN4VzdWekNyRQ",
        "kid": "35E0yg0TinUSym5bQ5FnUgWirIrfK81p-QCxW7VzCrE",
        "epk": {
          "kty": "EC",
          "crv": "P-384",
          "x": "fl757pDYJTMzbW0Vg_Qh3L9kfThCnCwnniO5bPfVL0PX1W_Kmj_G5HOeCWcr0GZq",
          "y": "moRQSUo5C95n_W5H79i_HWYAIcpmX9Iq2OcuBRe4R9pXmW_p1_dbz7YKSXbJLpEo"
        }
      },
      "encrypted_key": "fb6sCiAeFzPcfvHdIMKm051fkVioxgBKA6w3sIkw9t_mleCHe_bjFzK9_CfMA6E0aO8Y40WonGWYZ8oKIgRvItNWJsph6zr9"
    },
    {
      "header": {
        "alg": "ECDH-ES+XC20PKW",
        "apu": "ZlcyRHFxR25SaFZHOXlKckN2TWZVRmJlR1RZRl9JWjJYQ1pPcGNvei1vSDJ2aVlERU54Wi1leGJ6c0l1bkoyNQ",
        "apv": "MzVFMHlnMFRpblVTeW01YlE1Rm5VZ1dpcklyZks4MXAtUUN4VzdWekNyRQ",
        "kid": "wnJRuK09BydTKCPX9DEsf2hxSB1uzHdHrjLTtsiPUZw",
        "epk": {
          "kty": "EC",
          "crv": "P-384",
          "x": "fW2DqqGnRhVG9yJrCvMfUFbeGTYF_IZ2XCZOpcoz-oH2viYDENxZ-exbzsIunJ25",
          "y": "Pz-1Smflo-dAFZ0awotLqF0Qh5iurbbgcCJpN5ZnrrvBlnxiKuAD6o4ytxMS17f1"
        }
      },
      "encrypted_key": "gGqdDnlCuymQYRwIIHU0Cv4BxUYpby8cjohgbfNc-3kilzLIXN0x53amLz6sxuFvvGjPMv7BykQfoQPZgXj5B5rN--3StojC"
    },
    {
      "header": {
        "alg": "ECDH-ES+XC20PKW",
        "apu": "MTY0dUFMYXVkNmFLR29EMjF0NHd2dGN3QjRxUGNNRFlid3JWemVvY055Q05RelV1NlRTSVFEcExiT3pmMjJIeQ",
        "apv": "MzVFMHlnMFRpblVTeW01YlE1Rm5VZ1dpcklyZks4MXAtUUN4VzdWekNyRQ",
        "kid": "j9ZMlUQX9m9t8_6RmshAfMwHTIOE9_0Mv5bd5bQ4nKw",
        "epk": {
          "kty": "EC",
          "crv": "P-384",
          "x": "164uALaud6aKGoD21t4wvtcwB4qPcMDYbwrVzeocNyCNQzUu6TSIQDpLbOzf22Hy",
          "y": "SmS8y6E1V87EkDIQfZVJGdyWPRR5gSQXIhNKUF4vDB1OYcMtG4AGFhHlMVNjCipa"
        }
      },
      "encrypted_key": "ADkTont7J6MvkqtejyCZroaLhzBq6ehDlNJyiIsoV2L-vKOYWPfW2eyhk9_Q_Kc2mdfhsJeZ6S4YN2O1OVSvnGqho3zwKE_z"
    }
  ],
  "aad": "kOd8LfamiqCqZa4kZJPR0M3k11OjHo1dQgdgaI2HreU",
  "iv": "lhR0KWdWpo2TeiHgABGNLMYwGXmykQQX",
  "ciphertext": "LMVb7K1-YqLUS9JtE0s",
  "tag": "7UkWuQPffiWZIwS4sUc1Hg"
}
```

#### 2.1.3 NIST P-521 keys
- Recipient 1 key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-521",
  "x": "AIlOiZCrQMU83IOpoiMva75L_OqljXVakEJSjwAl5RaLmaNBZg-TXa0VKlAKTijGZAu_5gS_ZF82LRWDiltUHmX8",
  "y": "AFXxgSPOlCNnHtRQE7JmngrT5jgc5kHhMJE82wvMYlyrUdB1kgjN8zJDKkMDJ_dw1U2bEKXmcoCepN654HqmCeNJ",
  "d": "ASUBEC_crwIW50ke7p7EBjM0jnA3X7ziwT92TIVgHqTyFkEHKwuP_xbUSePfkhAgcEF2KHz48EgZJuDM6v4L2NXT"
}
```
- Recipient 1 kid (jwk thumbprint raw base64 URL encoded): `fr_FYdKBgF_lo1UzC133Tw382LhNDRk6TqwWUwYiytQ`
- Recipient 2 key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-521",
  "x": "AT71NCmSChOaf38XudcZFpb7eS6GS3rRgjIeXC5AWm9uqjgk3XloPINvlOkATR9syfonjONi4dvgu6ED0gDKyni2",
  "y": "AB6EuKG0Z5mnkw_Kk08EW1igFDoZ8tUzs67AoRrLM_CqufmehumGUBAAgPPyQ43HdZQRKn6UYaRn77JZ0kcUE8ZD",
  "d": "AMYS0X7aTtbFL8gcSH8h0AkH1kfgJxqe-vyahUoijuM3WtKp0z7C0j-kT717p8xV4NEnIrP7IP9ewCdh21TwCfdJ"
}
```
- Recipient 2 kid (jwk thumbprint raw base64 URL encoded): `z70hxN-69UU6IBsqxWMsKa5LqSnCGhd0BKMihYIeHYM`
- Recipient 3 key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-521",
  "x": "AcRZHKNmVZlxrKIcBsX-Z8KaGCJfPirBqOBWDylsVJCwvjEEMfJFS2GZtPwfQI5P561XAxjtb0ARPtucoyh5n4_Q",
  "y": "AaU8wdiQUItNWJnDrgMK84HhyloKQyXWEYZoDEjppL4kXvIV4CUhfYkTXnTWACUgnVG1uXdycmJ-XhgqPGfezQVb",
  "d": "AKfdXHWLY7WqaVVVLFBRyU7fd3EpfiQJW83IkuCk4tJ51PIO6Jzq17H0RI9XjK1YThz-cV1ZBXw9Q7ezDFusgL3k"
}
```
- Recipient 3 kid (jwk thumbprint raw, no padding, base64 URL encoded): `bU2CyYAuV1kJtU8vTE27PaOh20yTgKBSThtjrYHedf8`
- List of kids used for AAD for the above recipients (sorted `kid` values joined with `.`): `bU2CyYAuV1kJtU8vTE27PaOh20yTgKBSThtjrYHedf8.fr_FYdKBgF_lo1UzC133Tw382LhNDRk6TqwWUwYiytQ.z70hxN-69UU6IBsqxWMsKa5LqSnCGhd0BKMihYIeHYM`
- Resulting AAD value (sha256 of above list raw, no padding, base64 URL encoded): `gyaNc9X50RymOfupxfij36JjhkUG4SEiI4P8LQ0JCvI`
- JWE (pretty printed for readability):
```json
{
  "protected": "eyJjdHkiOiJhcHBsaWNhdGlvbi9kaWRjb21tLXBsYWluK2pzb24iLCJlbmMiOiJYQzIwUCIsInR5cCI6ImFwcGxpY2F0aW9uL2RpZGNvbW0tZW5jcnlwdGVkK2pzb24ifQ",
  "recipients": [
    {
      "header": {
        "alg": "ECDH-ES+XC20PKW",
        "apu": "QVdYTV9BOVF2WUZnUFYwMTRmUzk5LUNvX2dyS3BTZi1xbTJmeDdYRFpzekJrT2V3ZHlOSUp5S1gteFdQUUM1RWcwc0gtR0VnTGNWNXNRZThrNktuQWZYeA",
        "apv": "ZnJfRllkS0JnRl9sbzFVekMxMzNUdzM4MkxoTkRSazZUcXdXVXdZaXl0UQ",
        "kid": "fr_FYdKBgF_lo1UzC133Tw382LhNDRk6TqwWUwYiytQ",
        "epk": {
          "kty": "EC",
          "crv": "P-521",
          "x": "AWXM_A9QvYFgPV014fS99-Co_grKpSf-qm2fx7XDZszBkOewdyNIJyKX-xWPQC5Eg0sH-GEgLcV5sQe8k6KnAfXx",
          "y": "ANlcV5mvTqpzGF8loKsBjC_UFkfg260SFwrabuTBn_4oi1l5wKx7yootfvqrgGG1ivbuMIZ4NndJsbreyUywddQS"
        }
      },
      "encrypted_key": "SkZaMkjfoo-0PPQvWXottqV3dwOhcY7rCDckVkPRlxbj8jb_m4veIu-nx8jnkJMLUVqguKD_JhZ78MRAEikPg-gARUKyVRKV"
    },
    {
      "header": {
        "alg": "ECDH-ES+XC20PKW",
        "apu": "SElkUWNuaGluTUhhaEw1eDNsUGYxZWlrbW13NUFxNE9SSUpwTFhiQVV4NVJZbjF2dFVSeld4UHc0aU9nY1FOWjJCbEZVU21Md0FaUmhvdlFfb2J1MmZr",
        "apv": "ZnJfRllkS0JnRl9sbzFVekMxMzNUdzM4MkxoTkRSazZUcXdXVXdZaXl0UQ",
        "kid": "z70hxN-69UU6IBsqxWMsKa5LqSnCGhd0BKMihYIeHYM",
        "epk": {
          "kty": "EC",
          "crv": "P-521",
          "x": "AByHUHJ4YpzB2oS-cd5T39XopJpsOQKuDkSCaS12wFMeUWJ9b7VEc1sT8OIjoHEDWdgZRVEpi8AGUYaL0P6G7tn5",
          "y": "AFbfZdEiMwMy4rN0hzMl3XQgBpE98gE8A37bLLLZi-wAbyuNBhhGCWjxc2XSCRTn9IxBSV72Q8lttaIPWTRGsJPZ"
        }
      },
      "encrypted_key": "qgNULlqzY68vVzd07nuuuCSqDewr1mu45xhzCFriEdYNvoFmGl_elZua6r0gyknDsskbLOM_zAhg86Ieafn87YT-jOKZWXvB"
    },
    {
      "header": {
        "alg": "ECDH-ES+XC20PKW",
        "apu": "QWNJU1U1bVJwemJrYUs5TUs0ZVNHWXFBNFo5TFVwOF8yNHkwUnhmazExby1GazNvazZCUzk2X3REeWlfM0Y0bDhDU3VyanA3bUxhMGp4YVJ6M1NZbDRRMw",
        "apv": "ZnJfRllkS0JnRl9sbzFVekMxMzNUdzM4MkxoTkRSazZUcXdXVXdZaXl0UQ",
        "kid": "bU2CyYAuV1kJtU8vTE27PaOh20yTgKBSThtjrYHedf8",
        "epk": {
          "kty": "EC",
          "crv": "P-521",
          "x": "AcISU5mRpzbkaK9MK4eSGYqA4Z9LUp8_24y0Rxfk11o-Fk3ok6BS96_tDyi_3F4l8CSurjp7mLa0jxaRz3SYl4Q3",
          "y": "AYfx95SYdTrF5-FFJ6DX8YIQ3-kI3zA2huvwAoE5on4tczuZtRDxAnXocVXwydU_hYFICv4F1_U2wf2MZxu5EjgO"
        }
      },
      "encrypted_key": "N38f1rvfk00bHCRbAkMajaCmwIM6C96QNs5ck5i6EhoyONADKitu1E7FpMtwA7IBkLZXSPAz_2RRQg_yp494uh5unNgeIAsm"
    }
  ],
  "aad": "gyaNc9X50RymOfupxfij36JjhkUG4SEiI4P8LQ0JCvI",
  "iv": "y3t1nlPy-e5KlPZmhH6yvXweEnB50cW9",
  "ciphertext": "twYiHmEUk1QZw-XbLbY",
  "tag": "WsYbX9YDCcIAorqBbS2X_w"
}
```

#### 2.1.4 X25519 keys
- Recipient 1 key JWK format:
```json
{
  "kty": "OKP",
  "crv": "X25519",
  "x": "h5iIEBNlEHEhCgYLXAOXOofqYEA9Jo0Q1NUggjdwrVw",
  "d": "oEGk3DVSpzrZR6mcUF0EXmijrATej7xnPdlcPJDz53M"
}
```
- Recipient 1 kid (jwk thumbprint raw base64 URL encoded): `S-qQ_rRIsrscxdmzuplVLW5bqoxj08KO6BBkLZAxh-E`
- Recipient 2 key JWK format:
```json
{
  "kty": "OKP",
  "crv": "X25519",
  "x": "xawtbSFE5QYe7KDcYRBlnyozY9uPTzlRQ3gClzHzt2Q",
  "d": "yC7gzjKFdFwsCA4x7QL0S-eRhI2H966MjTdNA8IrMFw"
}
```
- Recipient 2 kid (jwk thumbprint raw base64 URL encoded): `m8EQ2XejsBRZ8sieSLapsS4-tO9ZQNjjxtjL6DOhP64`
- Recipient 3 key JWK format:
```json
{
  "kty": "OKP",
  "crv": "X25519",
  "x": "cvxZ6JaCIfmrTXiyHYNyqmxRSsUF8TEabuWOcZdgLT0",
  "d": "IM-XG4jc_Zyd5yWdv1i7vruFK4X2LzNTRicHvPZNznU"
}
```
- Recipient 3 kid (jwk thumbprint raw, no padding, base64 URL encoded): `oz3AtqUGnNpsT6OugQksyvY52HI36kCBtXqLE4joP3M`
- List of kids used for AAD for the above recipients (sorted `kid` values joined with `.`): `S-qQ_rRIsrscxdmzuplVLW5bqoxj08KO6BBkLZAxh-E.m8EQ2XejsBRZ8sieSLapsS4-tO9ZQNjjxtjL6DOhP64.oz3AtqUGnNpsT6OugQksyvY52HI36kCBtXqLE4joP3M`
- Resulting AAD value (sha256 of above list raw, no padding, base64 URL encoded): `Iri2F6uTNldPiiJNYNrlVb_Nt_c2XlPVdDKfmlnkBn4`
- JWE (pretty printed for readability):
```json
{
  "protected": "eyJjdHkiOiJhcHBsaWNhdGlvbi9kaWRjb21tLXBsYWluK2pzb24iLCJlbmMiOiJYQzIwUCIsInR5cCI6ImFwcGxpY2F0aW9uL2RpZGNvbW0tZW5jcnlwdGVkK2pzb24ifQ",
  "recipients": [
    {
      "header": {
        "alg": "ECDH-ES+XC20PKW",
        "apu": "eE9ZYmZrX0VLbmJaQmRoU1lPclI3NFVWWmlqZFU3LWg3ZF9aTkJ4VW1rMA",
        "apv": "Uy1xUV9yUklzcnNjeGRtenVwbFZMVzVicW94ajA4S082QkJrTFpBeGgtRQ",
        "kid": "S-qQ_rRIsrscxdmzuplVLW5bqoxj08KO6BBkLZAxh-E",
        "epk": {
          "kty": "OKP",
          "crv": "X25519",
          "x": "xOYbfk_EKnbZBdhSYOrR74UVZijdU7-h7d_ZNBxUmk0"
        }
      },
      "encrypted_key": "gPbf9-YZLPoEoKmaU70H8O9fsKiPy8rNiNuAvKog4AhGfy1axF4LuMdAZgO4EixyS4WC9V6JnfaYxmt3tFiCx80YXZrVlTBO"
    },
    {
      "header": {
        "alg": "ECDH-ES+XC20PKW",
        "apu": "eU9MMUM0blZzTzRTa1ROWDVRTlVCVl9iVmhJeVd1ZGdKOTlkRWdURDl5cw",
        "apv": "Uy1xUV9yUklzcnNjeGRtenVwbFZMVzVicW94ajA4S082QkJrTFpBeGgtRQ",
        "kid": "m8EQ2XejsBRZ8sieSLapsS4-tO9ZQNjjxtjL6DOhP64",
        "epk": {
          "kty": "OKP",
          "crv": "X25519",
          "x": "yOL1C4nVsO4SkTNX5QNUBV_bVhIyWudgJ99dEgTD9ys"
        }
      },
      "encrypted_key": "dsWHHkRbT9BWdgBl5MAUgNTenqiEjR4Z2cgaOLaraCDezRb051Z_muMo70-yJx1O9YDwLHq2V87dKQJX-byYtBeIR-5BubLm"
    },
    {
      "header": {
        "alg": "ECDH-ES+XC20PKW",
        "apu": "RkdtN2t4aGJFNGVBLWJpM1l2WTZPNVBCd2YtTlhEZ29YaWwzS19zLW5tSQ",
        "apv": "Uy1xUV9yUklzcnNjeGRtenVwbFZMVzVicW94ajA4S082QkJrTFpBeGgtRQ",
        "kid": "oz3AtqUGnNpsT6OugQksyvY52HI36kCBtXqLE4joP3M",
        "epk": {
          "kty": "OKP",
          "crv": "X25519",
          "x": "FGm7kxhbE4eA-bi3YvY6O5PBwf-NXDgoXil3K_s-nmI"
        }
      },
      "encrypted_key": "sEygr10dbgwHRy8-ktu8jLcACTKD1g7LfEkUSV_mAZNr1P06RhijZTRq47xesJuPWF8lfkAsK-UETLJ92KGRmbgCdSHQQwaG"
    }
  ],
  "aad": "Iri2F6uTNldPiiJNYNrlVb_Nt_c2XlPVdDKfmlnkBn4",
  "iv": "MWxpdCQBhVoiskZF7QD3bLzgI-iBEE3O",
  "ciphertext": "FtAX4yKH2a2dZqM6Zdk",
  "tag": "lR8OsOJieRydzSvI-qpy5w"
}
```

### 2.2 Single Recipient JWEs

Packing a message with 1 recipient using the **Flattened JWE JSON serialization** and the **Compact JWE serialization** formats as mentioned in the [notes](#notes) above.

#### 2.2.1 NIST P-256 key
- Single Recipient key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-256",
  "x": "kdAHozUe6HOhNC9_jsOI60FuHa64zHSwcZa0l22rXX4",
  "y": "Sj3iIz_HimnXgLRWU-x_gXjVyF2R0rh6OhuD3gzhUMw",
  "d": "NTV27xYkYkwDNYePKHlh6CIYHunx-6rn80cSATOI7rI"
}
```
- Single Recipient kid (jwk thumbprint raw base64 URL encoded): `Ivxk0K5tz7csR7MDXllXWd7YJTQF4pS8IHHkIdepgpk`
- Finally, packing the payload outputs the following flattened serialized JWE JSON:
```json
{
  "protected": "eyJhbGciOiJFQ0RILUVTK1hDMjBQS1ciLCJhcHUiOiJUWEl4TnpCM2JqSTJXa00wY0Y5SFVDMTBNazlyVFd0ZmExOVJVRkYxY1hObk5IUlFNV0pMU0hCdk1BIiwiYXB2IjoiU1haNGF6QkxOWFI2TjJOelVqZE5SRmhzYkZoWFpEZFpTbFJSUmpSd1V6aEpTRWhyU1dSbGNHZHdhdyIsImN0eSI6ImFwcGxpY2F0aW9uL2RpZGNvbW0tcGxhaW4ranNvbiIsImVuYyI6IlhDMjBQIiwiZXBrIjp7ImNydiI6IlAtMjU2Iiwia3R5IjoiRUMiLCJ4IjoiTXIxNzB3bjI2WkM0cF9HUC10Mk9rTWtfa19RUFF1cXNnNHRQMWJLSHBvMCIsInkiOiJ1MUMydEJuYlFwUS1YTWx0SHRFdWNJaFVod1FCeDBCbklLZFlkN3FLRVFFIn0sImtpZCI6Ikl2eGswSzV0ejdjc1I3TURYbGxYV2Q3WUpUUUY0cFM4SUhIa0lkZXBncGsiLCJ0eXAiOiJhcHBsaWNhdGlvbi9kaWRjb21tLWVuY3J5cHRlZCtqc29uIn0",
  "encrypted_key": "1k4IQgN6LIiV8mnNWUI2OyNXLRHvg75qZIyHf6_wtrBIYZlic1coUL3lekvesQpmLb1A9vip-pKi0yDKZOQIMtQS3TJ81EJJ",
  "iv": "6Qky6FL-Uzpi5nvaZHobo3_8xqv-LF4h",
  "ciphertext": "mqQ6nsR76RMLvNLkJgU",
  "tag": "5S99fa_S2c4XsVrzM2rPDw"
}
```
- The compact serialization of this envelope is:
  `eyJhbGciOiJFQ0RILUVTK1hDMjBQS1ciLCJhcHUiOiJUWEl4TnpCM2JqSTJXa00wY0Y5SFVDMTBNazlyVFd0ZmExOVJVRkYxY1hObk5IUlFNV0pMU0hCdk1BIiwiYXB2IjoiU1haNGF6QkxOWFI2TjJOelVqZE5SRmhzYkZoWFpEZFpTbFJSUmpSd1V6aEpTRWhyU1dSbGNHZHdhdyIsImN0eSI6ImFwcGxpY2F0aW9uL2RpZGNvbW0tcGxhaW4ranNvbiIsImVuYyI6IlhDMjBQIiwiZXBrIjp7Imt0eSI6IkVDIiwiY3J2IjoiUC0yNTYiLCJ4IjoiTXIxNzB3bjI2WkM0cF9HUC10Mk9rTWtfa19RUFF1cXNnNHRQMWJLSHBvMCIsInkiOiJ1MUMydEJuYlFwUS1YTWx0SHRFdWNJaFVod1FCeDBCbklLZFlkN3FLRVFFIn0sImtpZCI6Ikl2eGswSzV0ejdjc1I3TURYbGxYV2Q3WUpUUUY0cFM4SUhIa0lkZXBncGsiLCJ0eXAiOiJhcHBsaWNhdGlvbi9kaWRjb21tLWVuY3J5cHRlZCtqc29uIn0.1k4IQgN6LIiV8mnNWUI2OyNXLRHvg75qZIyHf6_wtrBIYZlic1coUL3lekvesQpmLb1A9vip-pKi0yDKZOQIMtQS3TJ81EJJ.6Qky6FL-Uzpi5nvaZHobo3_8xqv-LF4h.mqQ6nsR76RMLvNLkJgU.5S99fa_S2c4XsVrzM2rPDw`
- The single recipient's headers are merged into the `protected` header, which base64 URL decoded equals to (pretty printed for readability):
```json
{
  "alg": "ECDH-ES+XC20PKW",
  "apu": "TXIxNzB3bjI2WkM0cF9HUC10Mk9rTWtfa19RUFF1cXNnNHRQMWJLSHBvMA",
  "apv": "SXZ4azBLNXR6N2NzUjdNRFhsbFhXZDdZSlRRRjRwUzhJSEhrSWRlcGdwaw",
  "cty": "application/didcomm-plain+json",
  "enc": "XC20P",
  "epk": {
    "kty": "EC",
    "crv": "P-256",
    "x": "Mr170wn26ZC4p_GP-t2OkMk_k_QPQuqsg4tP1bKHpo0",
    "y": "u1C2tBnbQpQ-XMltHtEucIhUhwQBx0BnIKdYd7qKEQE"
  },
  "kid": "Ivxk0K5tz7csR7MDXllXWd7YJTQF4pS8IHHkIdepgpk",
  "typ": "application/didcomm-encrypted+json"
}
```

#### 2.2.2 NIST P-384 key
- Single Recipient key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-384",
  "x": "5aCpGZXwubdOSedZl1wc5PHB175a990-bRo2QKzju6uyeXD6hBKcB6vUijQRILMr",
  "y": "TeUA_qsYU8YmbHPA58QJuAJiUe0BEbi8Vuq88ZEWLudhJa4Dp5mBKuFEeJQcOQCa",
  "d": "wTv7Yh4bZAfCfmz0qL_lKJNlMRYuXjWzE63p7y3mZW8DRtN5LgOE25QKO9v0xgKN"
}
```
- Single Recipient kid (jwk thumbprint raw base64 URL encoded): `35E0yg0TinUSym5bQ5FnUgWirIrfK81p-QCxW7VzCrE`
- Finally, packing the payload outputs the following flattened serialized JWE JSON:
```json
{
  "protected": "eyJhbGciOiJFQ0RILUVTK1hDMjBQS1ciLCJhcHUiOiJkbkJCYkVKc1pXUXlWM0YzTUY5VVNYTk1iM1JLVmpBek4ydzNOMmxDYzA5Mk0xRnhiSEZSVWxaSGNHeGZkRWR2UVc5VFNXRnpVR0kwY0RjeGFIVTBiUSIsImFwdiI6Ik16VkZNSGxuTUZScGJsVlRlVzAxWWxFMVJtNVZaMWRwY2tseVprczRNWEF0VVVONFZ6ZFdla055UlEiLCJjdHkiOiJhcHBsaWNhdGlvbi9kaWRjb21tLXBsYWluK2pzb24iLCJlbmMiOiJYQzIwUCIsImVwayI6eyJjcnYiOiJQLTM4NCIsImt0eSI6IkVDIiwieCI6InZwQWxCbGVkMldxdzBfVElzTG90SlYwMzdsNzdpQnNPdjNRcWxxUVJWR3BsX3RHb0FvU0lhc1BiNHA3MWh1NG0iLCJ5IjoiU0Y3VEJDVnB5dTUwQ21vMzY0TWsyS2VyWGVwYnlYSklXZF8yTHNYMnNDMENWTkV1aFVJUHhFMmQtVjFVS1hwciJ9LCJraWQiOiIzNUUweWcwVGluVVN5bTViUTVGblVnV2lySXJmSzgxcC1RQ3hXN1Z6Q3JFIiwidHlwIjoiYXBwbGljYXRpb24vZGlkY29tbS1lbmNyeXB0ZWQranNvbiJ9",
  "encrypted_key": "y7jUbtMzOyerWyPhTgTutFH0r18Ug6uF3FYdTCyp2V-PacHeR8OTsNEh7dEOQk9o5P9mXvcGvfGr2xFNtoBw561TPv_Iw2ZK",
  "iv": "DOEADxox8cUL0jQ_H4hP67ymgscn8nQc",
  "ciphertext": "hSjiRkcMflJJK18cuXU",
  "tag": "SHN2rmcofMmnSqQ8htiCcQ"
}
```
- The compact serialization of this envelope is:
  `eyJhbGciOiJFQ0RILUVTK1hDMjBQS1ciLCJhcHUiOiJkbkJCYkVKc1pXUXlWM0YzTUY5VVNYTk1iM1JLVmpBek4ydzNOMmxDYzA5Mk0xRnhiSEZSVWxaSGNHeGZkRWR2UVc5VFNXRnpVR0kwY0RjeGFIVTBiUSIsImFwdiI6Ik16VkZNSGxuTUZScGJsVlRlVzAxWWxFMVJtNVZaMWRwY2tseVprczRNWEF0VVVONFZ6ZFdla055UlEiLCJjdHkiOiJhcHBsaWNhdGlvbi9kaWRjb21tLXBsYWluK2pzb24iLCJlbmMiOiJYQzIwUCIsImVwayI6eyJrdHkiOiJFQyIsImNydiI6IlAtMzg0IiwieCI6InZwQWxCbGVkMldxdzBfVElzTG90SlYwMzdsNzdpQnNPdjNRcWxxUVJWR3BsX3RHb0FvU0lhc1BiNHA3MWh1NG0iLCJ5IjoiU0Y3VEJDVnB5dTUwQ21vMzY0TWsyS2VyWGVwYnlYSklXZF8yTHNYMnNDMENWTkV1aFVJUHhFMmQtVjFVS1hwciJ9LCJraWQiOiIzNUUweWcwVGluVVN5bTViUTVGblVnV2lySXJmSzgxcC1RQ3hXN1Z6Q3JFIiwidHlwIjoiYXBwbGljYXRpb24vZGlkY29tbS1lbmNyeXB0ZWQranNvbiJ9.y7jUbtMzOyerWyPhTgTutFH0r18Ug6uF3FYdTCyp2V-PacHeR8OTsNEh7dEOQk9o5P9mXvcGvfGr2xFNtoBw561TPv_Iw2ZK.DOEADxox8cUL0jQ_H4hP67ymgscn8nQc.hSjiRkcMflJJK18cuXU.SHN2rmcofMmnSqQ8htiCcQ`
- The single recipient's headers are merged into the `protected` header, which base64 URL decoded equals to (pretty printed for readability):
```json
{
  "alg": "ECDH-ES+XC20PKW",
  "apu": "dnBBbEJsZWQyV3F3MF9USXNMb3RKVjAzN2w3N2lCc092M1FxbHFRUlZHcGxfdEdvQW9TSWFzUGI0cDcxaHU0bQ",
  "apv": "MzVFMHlnMFRpblVTeW01YlE1Rm5VZ1dpcklyZks4MXAtUUN4VzdWekNyRQ",
  "cty": "application/didcomm-plain+json",
  "enc": "XC20P",
  "epk": {
    "kty": "EC",
    "crv": "P-384",
    "x": "vpAlBled2Wqw0_TIsLotJV037l77iBsOv3QqlqQRVGpl_tGoAoSIasPb4p71hu4m",
    "y": "SF7TBCVpyu50Cmo364Mk2KerXepbyXJIWd_2LsX2sC0CVNEuhUIPxE2d-V1UKXpr"
  },
  "kid": "35E0yg0TinUSym5bQ5FnUgWirIrfK81p-QCxW7VzCrE",
  "typ": "application/didcomm-encrypted+json"
}
```

#### 2.2.3 NIST P-521 key
- Single Recipient key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-521",
  "x": "AIlOiZCrQMU83IOpoiMva75L_OqljXVakEJSjwAl5RaLmaNBZg-TXa0VKlAKTijGZAu_5gS_ZF82LRWDiltUHmX8",
  "y": "AFXxgSPOlCNnHtRQE7JmngrT5jgc5kHhMJE82wvMYlyrUdB1kgjN8zJDKkMDJ_dw1U2bEKXmcoCepN654HqmCeNJ",
  "d": "ASUBEC_crwIW50ke7p7EBjM0jnA3X7ziwT92TIVgHqTyFkEHKwuP_xbUSePfkhAgcEF2KHz48EgZJuDM6v4L2NXT"
}
```
- Single Recipient kid (jwk thumbprint raw base64 URL encoded): `fr_FYdKBgF_lo1UzC133Tw382LhNDRk6TqwWUwYiytQ`
- Finally, packing the payload outputs the following flattened serialized JWE JSON:
```json
{
  "protected": "eyJhbGciOiJFQ0RILUVTK1hDMjBQS1ciLCJhcHUiOiJOa3hhTFd0bGNtczNTWEYzV1hCeE5FOUpYemt0U2tGSGEyMVZUVEl0ZDB0a1VtUlhUV1JxY2sxNlV6ZDVRelpuVTFnMFdHOVJWM0ZRZEdWRE1UTjVTWGxXY2tKVGNuWlJOWGhSZGtVNFVEQllOVTA1UW1GQiIsImFwdiI6IlpuSmZSbGxrUzBKblJsOXNiekZWZWtNeE16TlVkek00TWt4b1RrUlNhelpVY1hkWFZYZFphWGwwVVEiLCJjdHkiOiJhcHBsaWNhdGlvbi9kaWRjb21tLXBsYWluK2pzb24iLCJlbmMiOiJYQzIwUCIsImVwayI6eyJjcnYiOiJQLTUyMSIsImt0eSI6IkVDIiwieCI6IkFPaTJmcEhxNU95S3NHS2F1RGlQX2ZpUUJwSmxETnZzQ25VWFZqSFk2ek0wdThndW9FbC1GNkVGcWo3WGd0ZDhpTWxhd1VxNzBPY1VMeFBEOUYtVFBRV2ciLCJ5IjoiQUVDX1VwU2poQzZlYnplSlBUc0JSb1YwNG9GdzZleDFRRzVpQW1OMm9hWVA3RVAtbU1YcEJRc2R3SEsyVFhpb1d5Q3ozZEU4d0JLUmZkcHFEaHdrRzFSaiJ9LCJraWQiOiJmcl9GWWRLQmdGX2xvMVV6QzEzM1R3MzgyTGhORFJrNlRxd1dVd1lpeXRRIiwidHlwIjoiYXBwbGljYXRpb24vZGlkY29tbS1lbmNyeXB0ZWQranNvbiJ9",
  "encrypted_key": "bsghnB_jpcD8E7k1Q2lEizymrCDatLiMH5w9MmWtP6PkpQuonoXXoLk0T-qmC3hK7pEBHdji9YKxPT2NQ-2x7F1Tzf-juieh",
  "iv": "SFKS4kMCTfU0tjUfn0YGh79rSWX9RGkP",
  "ciphertext": "Fg9hiOjUvP3WU5c0tco",
  "tag": "QJ2jlC_o-UiUvpFo7OF0Ew"
}
```
- The compact serialization of this envelope is:
  `eyJhbGciOiJFQ0RILUVTK1hDMjBQS1ciLCJhcHUiOiJOa3hhTFd0bGNtczNTWEYzV1hCeE5FOUpYemt0U2tGSGEyMVZUVEl0ZDB0a1VtUlhUV1JxY2sxNlV6ZDVRelpuVTFnMFdHOVJWM0ZRZEdWRE1UTjVTWGxXY2tKVGNuWlJOWGhSZGtVNFVEQllOVTA1UW1GQiIsImFwdiI6IlpuSmZSbGxrUzBKblJsOXNiekZWZWtNeE16TlVkek00TWt4b1RrUlNhelpVY1hkWFZYZFphWGwwVVEiLCJjdHkiOiJhcHBsaWNhdGlvbi9kaWRjb21tLXBsYWluK2pzb24iLCJlbmMiOiJYQzIwUCIsImVwayI6eyJrdHkiOiJFQyIsImNydiI6IlAtNTIxIiwieCI6IkFPaTJmcEhxNU95S3NHS2F1RGlQX2ZpUUJwSmxETnZzQ25VWFZqSFk2ek0wdThndW9FbC1GNkVGcWo3WGd0ZDhpTWxhd1VxNzBPY1VMeFBEOUYtVFBRV2ciLCJ5IjoiQUVDX1VwU2poQzZlYnplSlBUc0JSb1YwNG9GdzZleDFRRzVpQW1OMm9hWVA3RVAtbU1YcEJRc2R3SEsyVFhpb1d5Q3ozZEU4d0JLUmZkcHFEaHdrRzFSaiJ9LCJraWQiOiJmcl9GWWRLQmdGX2xvMVV6QzEzM1R3MzgyTGhORFJrNlRxd1dVd1lpeXRRIiwidHlwIjoiYXBwbGljYXRpb24vZGlkY29tbS1lbmNyeXB0ZWQranNvbiJ9.bsghnB_jpcD8E7k1Q2lEizymrCDatLiMH5w9MmWtP6PkpQuonoXXoLk0T-qmC3hK7pEBHdji9YKxPT2NQ-2x7F1Tzf-juieh.SFKS4kMCTfU0tjUfn0YGh79rSWX9RGkP.Fg9hiOjUvP3WU5c0tco.QJ2jlC_o-UiUvpFo7OF0Ew`
- The single recipient's headers are merged into the `protected` header, which base64 URL decoded equals to (pretty printed for readability):
```json
{
  "alg": "ECDH-ES+XC20PKW",
  "apu": "NkxaLWtlcms3SXF3WXBxNE9JXzktSkFHa21VTTItd0tkUmRXTWRqck16Uzd5QzZnU1g0WG9RV3FQdGVDMTN5SXlWckJTcnZRNXhRdkU4UDBYNU05QmFB",
  "apv": "ZnJfRllkS0JnRl9sbzFVekMxMzNUdzM4MkxoTkRSazZUcXdXVXdZaXl0UQ",
  "cty": "application/didcomm-plain+json",
  "enc": "XC20P",
  "epk": {
    "kty": "EC",
    "crv": "P-521",
    "x": "AOi2fpHq5OyKsGKauDiP_fiQBpJlDNvsCnUXVjHY6zM0u8guoEl-F6EFqj7Xgtd8iMlawUq70OcULxPD9F-TPQWg",
    "y": "AEC_UpSjhC6ebzeJPTsBRoV04oFw6ex1QG5iAmN2oaYP7EP-mMXpBQsdwHK2TXioWyCz3dE8wBKRfdpqDhwkG1Rj"
  },
  "kid": "fr_FYdKBgF_lo1UzC133Tw382LhNDRk6TqwWUwYiytQ",
  "typ": "application/didcomm-encrypted+json"
}
```

#### 2.2.4 X25519 key
- Single Recipient key JWK format:
```json
{
  "kty": "OKP",
  "crv": "X25519",
  "x": "h5iIEBNlEHEhCgYLXAOXOofqYEA9Jo0Q1NUggjdwrVw",
  "d": "oEGk3DVSpzrZR6mcUF0EXmijrATej7xnPdlcPJDz53M"
}
```
- Single Recipient kid (jwk thumbprint raw base64 URL encoded): `S-qQ_rRIsrscxdmzuplVLW5bqoxj08KO6BBkLZAxh-E`
- Finally, packing the payload outputs the following flattened serialized JWE JSON:
```json
{
  "protected": "eyJhbGciOiJFQ0RILUVTK1hDMjBQS1ciLCJhcHUiOiJjR1JKV1dNMlNVRm9SMnN3Unpsd1VHOUxPR1ZpYWtzM1QzbEpWMDlTV25oSVdsQm9hRmhWTWxoR1RRIiwiYXB2IjoiVXkxeFVWOXlVa2x6Y25OamVHUnRlblZ3YkZaTVZ6VmljVzk0YWpBNFMwODJRa0pyVEZwQmVHZ3RSUSIsImN0eSI6ImFwcGxpY2F0aW9uL2RpZGNvbW0tcGxhaW4ranNvbiIsImVuYyI6IlhDMjBQIiwiZXBrIjp7ImNydiI6IlgyNTUxOSIsImt0eSI6Ik9LUCIsIngiOiJwZElZYzZJQWhHazBHOXBQb0s4ZWJqSzdPeUlXT1JaeEhaUGhoWFUyWEZNIn0sImtpZCI6IlMtcVFfclJJc3JzY3hkbXp1cGxWTFc1YnFveGowOEtPNkJCa0xaQXhoLUUiLCJ0eXAiOiJhcHBsaWNhdGlvbi9kaWRjb21tLWVuY3J5cHRlZCtqc29uIn0",
  "encrypted_key": "VmgHr9mZuwN1dxRqd0B9n2yE4ErM14Mhri5XpYL93UVT5ZLGkUPKMG1-hdvLDhCUUdfJg5ronQke1HnOKcLgEgEO2Uh-jNHY",
  "iv": "M7A2POrqH_lcXV_fwYgYGp3any_9sKFt",
  "ciphertext": "gPNQD52uPxlA2881Ct4",
  "tag": "JHq2fnYwqUYc3hUgUWaMsw"
}
```
- The compact serialization of this envelope is:
  `eyJhbGciOiJFQ0RILUVTK1hDMjBQS1ciLCJhcHUiOiJjR1JKV1dNMlNVRm9SMnN3Unpsd1VHOUxPR1ZpYWtzM1QzbEpWMDlTV25oSVdsQm9hRmhWTWxoR1RRIiwiYXB2IjoiVXkxeFVWOXlVa2x6Y25OamVHUnRlblZ3YkZaTVZ6VmljVzk0YWpBNFMwODJRa0pyVEZwQmVHZ3RSUSIsImN0eSI6ImFwcGxpY2F0aW9uL2RpZGNvbW0tcGxhaW4ranNvbiIsImVuYyI6IlhDMjBQIiwiZXBrIjp7Imt0eSI6Ik9LUCIsImNydiI6IlgyNTUxOSIsIngiOiJwZElZYzZJQWhHazBHOXBQb0s4ZWJqSzdPeUlXT1JaeEhaUGhoWFUyWEZNIn0sImtpZCI6IlMtcVFfclJJc3JzY3hkbXp1cGxWTFc1YnFveGowOEtPNkJCa0xaQXhoLUUiLCJ0eXAiOiJhcHBsaWNhdGlvbi9kaWRjb21tLWVuY3J5cHRlZCtqc29uIn0.VmgHr9mZuwN1dxRqd0B9n2yE4ErM14Mhri5XpYL93UVT5ZLGkUPKMG1-hdvLDhCUUdfJg5ronQke1HnOKcLgEgEO2Uh-jNHY.M7A2POrqH_lcXV_fwYgYGp3any_9sKFt.gPNQD52uPxlA2881Ct4.JHq2fnYwqUYc3hUgUWaMsw`
- The single recipient's headers are merged into the `protected` header, which base64 URL decoded equals to (pretty printed for readability):
```json
{
  "alg": "ECDH-ES+XC20PKW",
  "apu": "cGRJWWM2SUFoR2swRzlwUG9LOGViaks3T3lJV09SWnhIWlBoaFhVMlhGTQ",
  "apv": "Uy1xUV9yUklzcnNjeGRtenVwbFZMVzVicW94ajA4S082QkJrTFpBeGgtRQ",
  "cty": "application/didcomm-plain+json",
  "enc": "XC20P",
  "epk": {
    "kty": "OKP",
    "crv": "X25519",
    "x": "pdIYc6IAhGk0G9pPoK8ebjK7OyIWORZxHZPhhXU2XFM"
  },
  "kid": "S-qQ_rRIsrscxdmzuplVLW5bqoxj08KO6BBkLZAxh-E",
  "typ": "application/didcomm-encrypted+json"
}
```
