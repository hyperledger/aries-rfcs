Table of Contents
=================

* [Authcrypt JWE Concrete examples](#authcrypt-jwe-concrete-examples)
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

# Authcrypt JWE Concrete examples

The following examples are for JWE **authcrypt** packer for encrypting the payload `secret message` and aad value set as the concatenation of recipients' KIDs (ASCII sorted) joined by `.` for non-compact serializations (JWE Compact serializations [don't have AAD](https://tools.ietf.org/html/rfc7516#section-7.1)).

#### Notes
- Since **autchrypt** requires the sender public key, it must be previously sent, out of band, to the recipient(s). For security reasons, the JWE envelope only includes the sender kid as `skid` in the protected headers. The recipient must be able to resolve the corresponding sender public key during unpack(JWE).
- all `x` and `y` key coordinates values below are raw (no padding) base64URL encoded.
- JWE envelopes with multi recipients use the [General JWE JSON Serialization](https://tools.ietf.org/html/rfc7516#section-7.2.1) format.
- JWE envelopes with a single recipient will be shown either as [JWE Compact](https://tools.ietf.org/html/rfc7516#section-3.1) or [Flattened JWE JSON](https://tools.ietf.org/html/rfc7516#section-7.2.2) serialization format.
- **General** JWE JSON Serialization format uses the above mentioned AAD value in their envelope.
- JWE **Compact** Serialization format does not support AAD values and therefore were built without it.
- all `apu` recipient header values are set with the raw (no padding) base64URL encoding of the corresponding sender's `kid` (`skid`) value since authcrypt reveals the sender.
- all `apv` recipient header values are set with the raw (no padding) base64URL encoding of the corresponding recipient's `kid` value.
- The final aad used to encrypt the payload is the concatenation of the raw (no padding) base64URL encoded protected headers and `aad` JWE header joined by a `.`.
- Even though flattened serialization do support `aad`, the field is omitted in the below examples to be consistent with compact JWE serialization format. Implementations should support `aad` for flattened serialization regardless.

## 1 A256GCM Content Encryption

### 1.1 Multi recipients JWEs

#### 1.1.1 NIST P-256 keys

The packer generates the following protected headers that includes the skid:
- Generated protected headers: `{"cty":"application/didcomm-plain+json","enc":"A256GCM","skid":"6PBTUbcLB7-Z4fuAFn42oC1PaMsNmjheq1FeZEUgV_8","typ":"application/didcomm-encrypted+json"}`
  - raw (no padding) base64URL encoded: `eyJjdHkiOiJhcHBsaWNhdGlvbi9kaWRjb21tLXBsYWluK2pzb24iLCJlbmMiOiJBMjU2R0NNIiwic2tpZCI6IjZQQlRVYmNMQjctWjRmdUFGbjQyb0MxUGFNc05tamhlcTFGZVpFVWdWXzgiLCJ0eXAiOiJhcHBsaWNhdGlvbi9kaWRjb21tLWVuY3J5cHRlZCtqc29uIn0`

- Sender key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-256",
  "x": "eFRTD4VaryfwIqLOpq7iuXmBbLjKPq5sVNzxwL7H1CI",
  "y": "cIeogn-pLJXlCepb9BqwNKKW4tmNea3Is8G47aPob6M",
  "d": "11NyNGrw4JoU7-_bwoZlVDTJi5vkMrSs4Nme_OHnx6Q"
}
```
- Sender kid (aka `skid`, jwk thumbprint raw base64 URL encoded): `6PBTUbcLB7-Z4fuAFn42oC1PaMsNmjheq1FeZEUgV_8`
- Recipient 1 key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-256",
  "x": "UP08dxIWu14HWRCI48Tnohm7jhaJ87fFdvYyf0w4lkg",
  "y": "ohZVfvhQViMGb_n-Y66TewBO2gtE_udG_DsNe8c-T8w",
  "d": "O0ikvlb4fh7daJpqd9JIgYk5e-twB0IYyKpoqmb7ZCc"
}
```
- Recipient 1 kid (jwk thumbprint raw base64 URL encoded): `D_kHovGtLUZ_ssw_vhZcqsx3LvQ6qC5JK74iPf9vqwk`
- Recipient 2 key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-256",
  "x": "XgkWXrogHmvx-wee7KAhi-eP6dpoyUcDKn224vpOshw",
  "y": "MAfbXLDMUOg6749jT0nDPZZIxfeozhdaKW6s3hutGHE",
  "d": "WIKKCdNWrddYbOtkOxHLfETps1cEBHsPhqGtQPxaLho"
}
```
- Recipient 2 kid (jwk thumbprint raw base64 URL encoded): `pXCqiUJ-A6Zlp6LAvkBWLOXPMuww5Hy_PljoODMsGTw`
- Recipient 3 key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-256",
  "x": "xdS1ON9UCKA3s7yOv55fvlegYR5GsLPbOZWi_zsFyEM",
  "y": "yeE__UlC9wEIbnCPjoOZa-nD2CN0uHtau7edhcmJiOg",
  "d": "Dry6DWrItSzhXS_ep5bvoWHkJEhKKJU-VTkFmNxZ7PI"
}
```
- Recipient 3 kid (jwk thumbprint raw, no padding, base64 URL encoded): `4CB-2PhtYR9WfjsFNb4rmvSmJozJAL4gRCg_am3oDhw`
- List of kids used for AAD for the above recipients (sorted `kid` values joined with `.`): `4CB-2PhtYR9WfjsFNb4rmvSmJozJAL4gRCg_am3oDhw.D_kHovGtLUZ_ssw_vhZcqsx3LvQ6qC5JK74iPf9vqwk.pXCqiUJ-A6Zlp6LAvkBWLOXPMuww5Hy_PljoODMsGTw`
- Resulting AAD value (sha256 of above list raw, no padding, base64 URL encoded): `vo7O9me-lVJv6Y_vjz-rL8eWaa0Xy1WHm2IOsR_UEpk`
- Finally, packing the payload outputs the following JWE (pretty printed for readability):
```json
{
  "protected": "eyJjdHkiOiJhcHBsaWNhdGlvbi9kaWRjb21tLXBsYWluK2pzb24iLCJlbmMiOiJBMjU2R0NNIiwic2tpZCI6IjZQQlRVYmNMQjctWjRmdUFGbjQyb0MxUGFNc05tamhlcTFGZVpFVWdWXzgiLCJ0eXAiOiJhcHBsaWNhdGlvbi9kaWRjb21tLWVuY3J5cHRlZCtqc29uIn0",
  "recipients": [
    {
      "header": {
        "alg": "ECDH-1PU+A256KW",
        "apu": "NlBCVFViY0xCNy1aNGZ1QUZuNDJvQzFQYU1zTm1qaGVxMUZlWkVVZ1ZfOA",
        "apv": "RF9rSG92R3RMVVpfc3N3X3ZoWmNxc3gzTHZRNnFDNUpLNzRpUGY5dnF3aw",
        "kid": "D_kHovGtLUZ_ssw_vhZcqsx3LvQ6qC5JK74iPf9vqwk",
        "epk": {
          "kty": "EC",
          "crv": "P-256",
          "x": "Vpj5VtHxMt5Xz3vnKA727nTMmJd4zbVcPmKjSyHvLvc",
          "y": "C7ZLlNCTduhf2qMXjrY907-OdMw_6ixC3UttKCVqgjk"
        }
      },
      "encrypted_key": "lIm78Z0OmYR5Jc5D416xjb9K3rkmcOgaEFVut4WyNDueoTnM9B86Ug"
    },
    {
      "header": {
        "alg": "ECDH-1PU+A256KW",
        "apu": "NlBCVFViY0xCNy1aNGZ1QUZuNDJvQzFQYU1zTm1qaGVxMUZlWkVVZ1ZfOA",
        "apv": "RF9rSG92R3RMVVpfc3N3X3ZoWmNxc3gzTHZRNnFDNUpLNzRpUGY5dnF3aw",
        "kid": "pXCqiUJ-A6Zlp6LAvkBWLOXPMuww5Hy_PljoODMsGTw",
        "epk": {
          "kty": "EC",
          "crv": "P-256",
          "x": "wDD9G8UK-I246qp6-A1qBPr6N2yX6nTfYb9Zotf898o",
          "y": "KIW0m4mOlWzwnW9y1R9314keHj5W8b7eqUs_dT3LBEw"
        }
      },
      "encrypted_key": "BjZsq3DwuggMu1YhSZIX7NydPNSIBOfHWVBEZ9t5yDzlt1am_LI8cg"
    },
    {
      "header": {
        "alg": "ECDH-1PU+A256KW",
        "apu": "NlBCVFViY0xCNy1aNGZ1QUZuNDJvQzFQYU1zTm1qaGVxMUZlWkVVZ1ZfOA",
        "apv": "RF9rSG92R3RMVVpfc3N3X3ZoWmNxc3gzTHZRNnFDNUpLNzRpUGY5dnF3aw",
        "kid": "4CB-2PhtYR9WfjsFNb4rmvSmJozJAL4gRCg_am3oDhw",
        "epk": {
          "kty": "EC",
          "crv": "P-256",
          "x": "CHaH39lqKhUQLcrmbL_sVBmVZQaLlDxNGI1WkcCB7ss",
          "y": "R36X6eJ2dwPz8T7eto0Uije3KLOGAwzLUVUKWj0SxHk"
        }
      },
      "encrypted_key": "YnLT86bjwgz4SsKUUiG6bf0AybQywN8k2wHa_E3hGLP3Nwo23CyekQ"
    }
  ],
  "aad": "vo7O9me-lVJv6Y_vjz-rL8eWaa0Xy1WHm2IOsR_UEpk",
  "iv": "mwMiQc4m9LaoqnIC",
  "ciphertext": "wQGUFlLz9fHpDoACWEQ",
  "tag": "Ma9X6kppUNUp5SYH74zXDw"
}
```

#### 1.1.2 NIST P-384 keys
The packer generates the following protected headers that includes the skid:
- Generated protected headers: `{"cty":"application/didcomm-plain+json","enc":"A256GCM","skid":"0Bz8yRwu9eC8Gi7cYOwAKMJ8jysInhAtwH8k8m9MX04","typ":"application/didcomm-encrypted+json"}`
  - raw (no padding) base64URL encoded: `eyJjdHkiOiJhcHBsaWNhdGlvbi9kaWRjb21tLXBsYWluK2pzb24iLCJlbmMiOiJBMjU2R0NNIiwic2tpZCI6IjBCejh5Und1OWVDOEdpN2NZT3dBS01KOGp5c0luaEF0d0g4azhtOU1YMDQiLCJ0eXAiOiJhcHBsaWNhdGlvbi9kaWRjb21tLWVuY3J5cHRlZCtqc29uIn0`
- Sender key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-384",
  "x": "UW1LtMXuZdFS0gyp0_F19uxHqECvCcJA7SmeeuRSSc_PQfsbZWXt5L0KyLYpNIQb",
  "y": "FBdPcUvanB7igwkX0NN5rOvH3OKZ1gQHhcad7cCy6QNYKKz7lBWUUOmzypee31pS",
  "d": "wrXW0wsFKjvpTWqOAd1mohRublQs4P014-U4_K-eTRFmzhkyLJqNn91dH_AHUc4-"
}
```
- Sender kid (jwk thumbprint raw base64 URL encoded): `0Bz8yRwu9eC8Gi7cYOwAKMJ8jysInhAtwH8k8m9MX04`
- Recipient 1 key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-384",
  "x": "k3W_RR59uUG3HFlhhqNNmBDyFdMtWHxKAsJaxLBqQgQer3d3aAN-lfdxzGnHtwj1",
  "y": "VMSy5zxFEGaGRINailLTUH6NlP0JO2qu0j0_UbS7Ng1b8JkzHDnDbjGgsLqVJaMM",
  "d": "iM5K8uqNvFYJnuToMDBguGwUIlu1erT-K0g7NYtJrQnHZOumS8yIC4MCNC60Ch91"
}
```
- Recipient 1 kid (jwk thumbprint raw base64 URL encoded): `obCHRLVDx634Cax_Kr3B8fd_-xj5kAj0r0Kvvvmq1z8`
- Recipient 2 key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-384",
  "x": "W3iUHCzh_PWzUKONKeHwIKcjWNN--c7OlL2H23lV13C9tlkqOleFUmioW-AeitEk",
  "y": "CIzVD6KsuDLyKQPm0r62LPZikkT2kiXJpLjcVO3op2kgePQkZ31xniKE0VbUBnTH",
  "d": "V_vQwOqHVCGxSjX_dN8H5VXvOGYDRTGI00mNXwB0I0mKDd8kqCJmNtGlf-eUrbub"
}
```
- Recipient 2 kid (jwk thumbprint raw base64 URL encoded): `PfuTIXG60dvOwnFOfMxJ0i59_L7vqNytROX_bLRR-3M`
- Recipient 3 key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-384",
  "x": "bsX8qtEtj5IDLp9iDUKlgdu_3nluupFtFBrfIK1nza1bGZQRlZ3JG3PdBzVAoePz",
  "y": "QX_2v0BHloNS7iWoB4CcO9UWHdtirMVmbNcB8ZGczCJOfUyjYcQxGr0RU_tGkFC4",
  "d": "rQ-4ZmWn09CsCqRQJhpQhDeUZXeZ3cy_Pei-fchVPFTa2FnAzvjwEF2Nsm2f3MmR"
}
```
- Recipient 3 kid (jwk thumbprint raw, no padding, base64 URL encoded): `VTVlkyBsoW4ey0sh7TMJBErLGeBeKQsOttFRrXD6eqI`
- List of kids used for AAD for the above recipients (sorted `kid` values joined with `.`): `PfuTIXG60dvOwnFOfMxJ0i59_L7vqNytROX_bLRR-3M.VTVlkyBsoW4ey0sh7TMJBErLGeBeKQsOttFRrXD6eqI.obCHRLVDx634Cax_Kr3B8fd_-xj5kAj0r0Kvvvmq1z8`
- Resulting AAD value (sha256 of above list raw, no padding, base64 URL encoded): `m72Q9j28hFk0imbFVzqY4KfTE77L8itJoX75N3hwiwA`
- Finally, packing the payload outputs the following JWE (pretty printed for readability):
```json
{
  "protected": "eyJjdHkiOiJhcHBsaWNhdGlvbi9kaWRjb21tLXBsYWluK2pzb24iLCJlbmMiOiJBMjU2R0NNIiwic2tpZCI6IjBCejh5Und1OWVDOEdpN2NZT3dBS01KOGp5c0luaEF0d0g4azhtOU1YMDQiLCJ0eXAiOiJhcHBsaWNhdGlvbi9kaWRjb21tLWVuY3J5cHRlZCtqc29uIn0",
  "recipients": [
    {
      "header": {
        "alg": "ECDH-1PU+A256KW",
        "apu": "MEJ6OHlSd3U5ZUM4R2k3Y1lPd0FLTUo4anlzSW5oQXR3SDhrOG05TVgwNA",
        "apv": "b2JDSFJMVkR4NjM0Q2F4X0tyM0I4ZmRfLXhqNWtBajByMEt2dnZtcTF6OA",
        "kid": "obCHRLVDx634Cax_Kr3B8fd_-xj5kAj0r0Kvvvmq1z8",
        "epk": {
          "kty": "EC",
          "crv": "P-384",
          "x": "cjJHtV4VkMCww9ig94-_4e4yMfo2WI4Rh4dZh6NkYFvz-EGylA7RLSO5TRC-JJ_G",
          "y": "RJe2QisAYpfuTWTV6KVeoLGshsJqYokbcSUqdMxrFGXSp4ZMNrW4yj410Xsn6hy6"
        }
      },
      "encrypted_key": "o0ZZ_xNtmUPcpQAK3kzjOLp8xWBJ31tr-ORQjXtwpqgTuvM_nvhk_w"
    },
    {
      "header": {
        "alg": "ECDH-1PU+A256KW",
        "apu": "MEJ6OHlSd3U5ZUM4R2k3Y1lPd0FLTUo4anlzSW5oQXR3SDhrOG05TVgwNA",
        "apv": "b2JDSFJMVkR4NjM0Q2F4X0tyM0I4ZmRfLXhqNWtBajByMEt2dnZtcTF6OA",
        "kid": "PfuTIXG60dvOwnFOfMxJ0i59_L7vqNytROX_bLRR-3M",
        "epk": {
          "kty": "EC",
          "crv": "P-384",
          "x": "u1HYhdUJGx49J6wSLYM_JLHTkJrkR7wMSm5uYZMH7ZpcC3qF8MUyKTuKN0FGCBcN",
          "y": "K-XI-KAGd2jHebNq44yQrDA6Ubs5M99mIlre0chzI13bSLDOuUG4RJ8yjYjXysWF"
        }
      },
      "encrypted_key": "iCV1_peiRwnsrrBQWmp7GOd-taee-Yk8t6XqJCZPGziglDpGBu_ZhA"
    },
    {
      "header": {
        "alg": "ECDH-1PU+A256KW",
        "apu": "MEJ6OHlSd3U5ZUM4R2k3Y1lPd0FLTUo4anlzSW5oQXR3SDhrOG05TVgwNA",
        "apv": "b2JDSFJMVkR4NjM0Q2F4X0tyM0I4ZmRfLXhqNWtBajByMEt2dnZtcTF6OA",
        "kid": "VTVlkyBsoW4ey0sh7TMJBErLGeBeKQsOttFRrXD6eqI",
        "epk": {
          "kty": "EC",
          "crv": "P-384",
          "x": "Twps_QU6ShP18uQFNCcdOx9sU9YrHBznNnSbhQD474tLUcnslq5Trubq3ogp-LTX",
          "y": "oSES1a5xve9e-lKQ3NMN5_CW9Sii9rTorqUMggDzodLsRGm0Jud3HAy2-uE956Xq"
        }
      },
      "encrypted_key": "dLDKyXeZJDcB_i1Tnn_EUxqCc2ukneaummXF_FwcbpnMH8B0eVizvA"
    }
  ],
  "aad": "m72Q9j28hFk0imbFVzqY4KfTE77L8itJoX75N3hwiwA",
  "iv": "nuuuri2fyNl3jBo6",
  "ciphertext": "DCWevJuEo5dx-MmqPvw",
  "tag": "Pyt1S_Smg9Pnd1u_5Z7nbA"
}
```

#### 1.1.3 NIST P-521 keys
The packer generates the following protected headers that includes the skid:
- Generated protected headers: `{"cty":"application/didcomm-plain+json","enc":"A256GCM","skid":"oq-WBIGQm-iHiNRj6nId4-E1QtY8exzp8C56SziUfeU","typ":"application/didcomm-encrypted+json"}`
  - raw (no padding) base64URL encoded: `eyJjdHkiOiJhcHBsaWNhdGlvbi9kaWRjb21tLXBsYWluK2pzb24iLCJlbmMiOiJBMjU2R0NNIiwic2tpZCI6Im9xLVdCSUdRbS1pSGlOUmo2bklkNC1FMVF0WThleHpwOEM1NlN6aVVmZVUiLCJ0eXAiOiJhcHBsaWNhdGlvbi9kaWRjb21tLWVuY3J5cHRlZCtqc29uIn0`
- Sender key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-521",
  "x": "AXKDGPnD6hlQIre8aEeu33bQffkfl-eQfQXgzNXQX7XFYt5GKA1N6w4-f0_Ci7fQNKGkQuCoAu5-6CNk9M_cHiDi",
  "y": "Ae4-APhoZAmM99MdY9io9IZA43dN7dA006wlFb6LJ9bcusJOi5R-o3o3FhCjt5KTv_JxYbo6KU4PsBwQ1eeKyJ0U",
  "d": "AP9l2wmQ85P5XD84CkEQVWHaX_46EDvHxLWHEKsHFSQYjEh6BDSuyy1TUNv68v8kpbLCDjvsBc3cIBqC4_T1r4pU"
}
```
- Sender kid (jwk thumbprint raw base64 URL encoded): `oq-WBIGQm-iHiNRj6nId4-E1QtY8exzp8C56SziUfeU`
- Recipient 1 key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-521",
  "x": "ALmUHkd9Gi2NApJojNzzA34Qdd1-KLnq6jd2UJ9wl-xJzTQ2leg8qi3-hrFs7NqNfxqO6vE5bBoWYFeAcf3LqJOU",
  "y": "AN-MutmkAXGzlgzSQJRnctHDcjQQNpRek-8BeqyUDXdZKNGKSMEAzw6Hnl3VdvsvihQfrxcajpx5PSnwxbbdakHq",
  "d": "AKv-YbKdI6y8NRMP-e17-RjZyRTfGf0Xh9Og5g7q7aq0xS2mO59ttIJ67XHW5SPTBQDbltdUcydKroWNUIGvhKNv"
}
```
- Recipient 1 kid (jwk thumbprint raw base64 URL encoded): `wax1T_hGUvM0NmlbFJi2RizQ_gWajumI5j0Hx7CbgAw`
- Recipient 2 key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-521",
  "x": "ALmUHkd9Gi2NApJojNzzA34Qdd1-KLnq6jd2UJ9wl-xJzTQ2leg8qi3-hrFs7NqNfxqO6vE5bBoWYFeAcf3LqJOU",
  "y": "AN-MutmkAXGzlgzSQJRnctHDcjQQNpRek-8BeqyUDXdZKNGKSMEAzw6Hnl3VdvsvihQfrxcajpx5PSnwxbbdakHq",
  "d": "AKv-YbKdI6y8NRMP-e17-RjZyRTfGf0Xh9Og5g7q7aq0xS2mO59ttIJ67XHW5SPTBQDbltdUcydKroWNUIGvhKNv"
}
```
- Recipient 2 kid (jwk thumbprint raw base64 URL encoded): `XmLVV-CqMkTGQIe6-KecWZWtZVwORTMP2y5aqMPV7P4`
- Recipient 3 key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-521",
  "x": "AHCbpo-299Q0Fk71CtBoPu-40-Z0UOu4cGZfgtHHwcu3ciMWVR8IWF4bgvFpAPfKG8Dqx7JJWO8uEgLE67A7aQOL",
  "y": "AQ_JBjS3lt8zz3njFhUoJwEdSJMyrSfGPCLpaWkKuRo25k3im-7IjY8T43gvzZXYwV3PKKR3iJ1jnQCrYmfRrmva",
  "d": "ACgCw3U3eWTYD5vcygoOpoGPost9TojYJH9FllyRuqwlS3L8dkZu7vKhFyoEg6Bo8AqcOUj5Mtgxhd6Wu02YvqK3"
}
```
- Recipient 3 kid (jwk thumbprint raw, no padding, base64 URL encoded): `pRJtTY7V1pClPu8WEgEZonzaHq3K0El9Vcb8qmjucSg`
- List of kids used for AAD for the above recipients (sorted `kid` values joined with `.`): `S8s7FFL7f0fUMXt93WOWC-3PJrV1iuAmB_ZlCDyjXqs.XmLVV-CqMkTGQIe6-KecWZWtZVwORTMP2y5aqMPV7P4.pRJtTY7V1pClPu8WEgEZonzaHq3K0El9Vcb8qmjucSg`
- Resulting AAD value (sha256 of above list raw, no padding, base64 URL encoded): `tOS8nLSCERw2V9WOZVo6cenGuM4DJvHse1dsvTk8_As`
- Finally, packing the payload outputs the following JWE (pretty printed for readability):
```json
{
  "protected": "eyJjdHkiOiJhcHBsaWNhdGlvbi9kaWRjb21tLXBsYWluK2pzb24iLCJlbmMiOiJBMjU2R0NNIiwic2tpZCI6Im9xLVdCSUdRbS1pSGlOUmo2bklkNC1FMVF0WThleHpwOEM1NlN6aVVmZVUiLCJ0eXAiOiJhcHBsaWNhdGlvbi9kaWRjb21tLWVuY3J5cHRlZCtqc29uIn0",
  "recipients": [
    {
      "header": {
        "alg": "ECDH-1PU+A256KW",
        "apu": "b3EtV0JJR1FtLWlIaU5SajZuSWQ0LUUxUXRZOGV4enA4QzU2U3ppVWZlVQ",
        "apv": "WG1MVlYtQ3FNa1RHUUllNi1LZWNXWld0WlZ3T1JUTVAyeTVhcU1QVjdQNA",
        "kid": "XmLVV-CqMkTGQIe6-KecWZWtZVwORTMP2y5aqMPV7P4",
        "epk": {
          "kty": "EC",
          "crv": "P-521",
          "x": "AP630J9yi2UFBfRWKucXB8eu9-SSKbbbD1fzFhLgbI3xTRTRNMGm-U5EGHbplMLsOfP2pNxtAgo2-d6abiZiD6gg",
          "y": "AE1Grtp1iFvySLN4yHVvE0kYWChqVfkO_kHEMujjL6vVu_AAOvl3aogquLv1zgduitCPbKRTno89r3rv0L0Kuj0M"
        }
      },
      "encrypted_key": "FSYpXFfgPlSfj91VFQ4zAs0Wb3CEpWcBcGeW4nld9szVfb_WRbqTtA"
    },
    {
      "header": {
        "alg": "ECDH-1PU+A256KW",
        "apu": "b3EtV0JJR1FtLWlIaU5SajZuSWQ0LUUxUXRZOGV4enA4QzU2U3ppVWZlVQ",
        "apv": "WG1MVlYtQ3FNa1RHUUllNi1LZWNXWld0WlZ3T1JUTVAyeTVhcU1QVjdQNA",
        "kid": "S8s7FFL7f0fUMXt93WOWC-3PJrV1iuAmB_ZlCDyjXqs",
        "epk": {
          "kty": "EC",
          "crv": "P-521",
          "x": "Acw0XM1IZl63ltysb-ivw8zBhZ-Wz54SaXM_vGGea8Sa5w6VWdZflp1tibzHkfu4novFFpNbKtnCKi-28AqQnOYZ",
          "y": "AajoBj0KMrlaIA17RKnShFNzIb1S81oLYZu5MXzAg-XvT8_q83dXajOCiYJLo3taUvHTlcPjkHMG3_8442DgWpU_"
        }
      },
      "encrypted_key": "3ct4awH6xyp9BjA74Q_j6ot6F32okEYXbS2e6NIkiAgs-JGyEPWoxw"
    },
    {
      "header": {
        "alg": "ECDH-1PU+A256KW",
        "apu": "b3EtV0JJR1FtLWlIaU5SajZuSWQ0LUUxUXRZOGV4enA4QzU2U3ppVWZlVQ",
        "apv": "WG1MVlYtQ3FNa1RHUUllNi1LZWNXWld0WlZ3T1JUTVAyeTVhcU1QVjdQNA",
        "kid": "pRJtTY7V1pClPu8WEgEZonzaHq3K0El9Vcb8qmjucSg",
        "epk": {
          "kty": "EC",
          "crv": "P-521",
          "x": "APu-ArpY-GUntHG7BzTvUauKVP_YpCcVnZFX6r_VvYY2iPbFSZYxvUdUbX3TGK-Q92rTHNaNnutjbPcrCaBpJecM",
          "y": "AONhGq1vGU20Wdrx1FT5SBdLOIvqOK_pxhTJZhS0Vwi_JYQdKN6PHrX9GyJ23ZhaY3bBKX6V2uzRJzV8Qam1FUbz"
        }
      },
      "encrypted_key": "U51txv9yfZASl8tlT7GbNtLjeAqTHUVT4O9MEqBKaYIdAcA7Qd7dnw"
    }
  ],
  "aad": "tOS8nLSCERw2V9WOZVo6cenGuM4DJvHse1dsvTk8_As",
  "iv": "LJl-9ygxPGMAmVHP",
  "ciphertext": "HOfi-W7mcQv93scr1z8",
  "tag": "zaM6OfzhVhYCsqD2VW5ztw"
}
```

#### 1.1.4 X25519 keys
The packer generates the following protected headers that includes the skid:
- Generated protected headers: `{"cty":"application/didcomm-plain+json","enc":"A256GCM","skid":"X5INSMIv_w4Q7pljH7xjeUrRAKiBGHavSmOYyyiRugc","typ":"application/didcomm-encrypted+json"}`
  - raw (no padding) base64URL encoded: `eyJjdHkiOiJhcHBsaWNhdGlvbi9kaWRjb21tLXBsYWluK2pzb24iLCJlbmMiOiJBMjU2R0NNIiwic2tpZCI6Ilg1SU5TTUl2X3c0UTdwbGpIN3hqZVVyUkFLaUJHSGF2U21PWXl5aVJ1Z2MiLCJ0eXAiOiJhcHBsaWNhdGlvbi9kaWRjb21tLWVuY3J5cHRlZCtqc29uIn0`
- Sender key JWK format:
```json
{
  "kty": "OKP",
  "crv": "X25519",
  "x": "WKkktGWkUB9hDITcqa1Z6MC8rcWy8fWtxuT7xwQF1lw",
  "d": "-LEcVt6bW_ah9gY7H_WknTsg1MXq8yc42SrSJhqP0Vo"
}
```
- Sender kid (jwk thumbprint raw base64 URL encoded): `X5INSMIv_w4Q7pljH7xjeUrRAKiBGHavSmOYyyiRugc`
- Recipient 1 key JWK format:
```json
{
  "kty": "OKP",
  "crv": "X25519",
  "x": "NJzDtIa7vjz-isjaI-6GKGDe2EUx26-D44d6jLILeBI",
  "d": "MEBNdr6Tpb0XfD60NeHby-Tkmlpgr7pvVe7Q__sBbGw"
}
```
- Recipient 1 kid (jwk thumbprint raw base64 URL encoded): `2UR-nzYjVhsq0cZakWjE38-wUdG0S2EIrLZ8Eh0KVO0`
- Recipient 2 key JWK format:
```json
{
  "kty": "OKP",
  "crv": "X25519",
  "x": "_aiA8rwrayc2k9EL-mkqtSh8onyl_-EzVif3L-q-R20",
  "d": "ALBfdypF_lAbBtWXhwvq9Rs7TGjcLd-iuDh0s3yWr2Y"
}
```
- Recipient 2 kid (jwk thumbprint raw base64 URL encoded): `dvDd4h1rHj-onj-Xz9O1KRIgkMhh3u23d-94brHbBKo`
- Recipient 3 key JWK format:
```json
{
  "kty": "OKP",
  "crv": "X25519",
  "x": "zuHJfrIarLGFga0OwZqDlvlI5P1bb9DFhAtdnI54pwQ",
  "d": "8BVFAqxPHXB5W-EBxr-EjdUmA4HqY1gwDjiYvt0UxUk"
}
```
- Recipient 3 kid (jwk thumbprint raw, no padding, base64 URL encoded): `hj57wbrmOygTc_ktMPqKMHdiL85FdiGJa5DKzoLIzeU`
- List of kids used for AAD for the above recipients (sorted `kid` values joined with `.`): `2UR-nzYjVhsq0cZakWjE38-wUdG0S2EIrLZ8Eh0KVO0.dvDd4h1rHj-onj-Xz9O1KRIgkMhh3u23d-94brHbBKo.hj57wbrmOygTc_ktMPqKMHdiL85FdiGJa5DKzoLIzeU`
- Resulting AAD value (sha256 of above list raw, no padding, base64 URL encoded): `L-QV1cHI5u8U9BQa8_S4CFW-LhKNXHCjmqydtQYuSLw`
- Finally, packing the payload outputs the following JWE (pretty printed for readability):
```json
{
  "protected": "eyJjdHkiOiJhcHBsaWNhdGlvbi9kaWRjb21tLXBsYWluK2pzb24iLCJlbmMiOiJBMjU2R0NNIiwic2tpZCI6Ilg1SU5TTUl2X3c0UTdwbGpIN3hqZVVyUkFLaUJHSGF2U21PWXl5aVJ1Z2MiLCJ0eXAiOiJhcHBsaWNhdGlvbi9kaWRjb21tLWVuY3J5cHRlZCtqc29uIn0",
  "recipients": [
    {
      "header": {
        "alg": "ECDH-1PU+A256KW",
        "apu": "WDVJTlNNSXZfdzRRN3Bsakg3eGplVXJSQUtpQkdIYXZTbU9ZeXlpUnVnYw",
        "apv": "MlVSLW56WWpWaHNxMGNaYWtXakUzOC13VWRHMFMyRUlyTFo4RWgwS1ZPMA",
        "kid": "2UR-nzYjVhsq0cZakWjE38-wUdG0S2EIrLZ8Eh0KVO0",
        "epk": {
          "kty": "OKP",
          "crv": "X25519",
          "x": "IcuAA7zPN0mLt4GSZLQJ6f8p3yPALQaSyupbSRpDnwA"
        }
      },
      "encrypted_key": "_GoKcbrlbPR8hdgpDdpotO4WvAKOzyOEXo5A2RlxVaEb0enFej2DFQ"
    },
    {
      "header": {
        "alg": "ECDH-1PU+A256KW",
        "apu": "WDVJTlNNSXZfdzRRN3Bsakg3eGplVXJSQUtpQkdIYXZTbU9ZeXlpUnVnYw",
        "apv": "MlVSLW56WWpWaHNxMGNaYWtXakUzOC13VWRHMFMyRUlyTFo4RWgwS1ZPMA",
        "kid": "dvDd4h1rHj-onj-Xz9O1KRIgkMhh3u23d-94brHbBKo",
        "epk": {
          "kty": "OKP",
          "crv": "X25519",
          "x": "_BVh0oInkDiqnTkHKLvNMa8cldr79TZS00MJCYwZo3Y"
        }
      },
      "encrypted_key": "gacTLNP-U5mYAHJLG9F97R52aG244NfLeWg_Dj4Fy0C96oIIN-3psw"
    },
    {
      "header": {
        "alg": "ECDH-1PU+A256KW",
        "apu": "WDVJTlNNSXZfdzRRN3Bsakg3eGplVXJSQUtpQkdIYXZTbU9ZeXlpUnVnYw",
        "apv": "MlVSLW56WWpWaHNxMGNaYWtXakUzOC13VWRHMFMyRUlyTFo4RWgwS1ZPMA",
        "kid": "hj57wbrmOygTc_ktMPqKMHdiL85FdiGJa5DKzoLIzeU",
        "epk": {
          "kty": "OKP",
          "crv": "X25519",
          "x": "alPo4cjEjondCmz8mw8tntYxlpGPSLaqe3SSI_wu11s"
        }
      },
      "encrypted_key": "q2RpqrdZA9mvVBGTvMNHg3P6SysnuCpfraLWhRseiQ1ImJWdLq53TA"
    }
  ],
  "aad": "L-QV1cHI5u8U9BQa8_S4CFW-LhKNXHCjmqydtQYuSLw",
  "iv": "J-OEJGFWvJ6rw9dX",
  "ciphertext": "BvFi1vAzq0Uostj0_ms",
  "tag": "C6itmqZ7ehMx9FF70fdGGQ"
}
```

### 1.2 Single Recipient JWEs

Packing a message with 1 recipient using the **Flattened JWE JSON serialization** and **Compact JWE serialization** formats as mentioned in the [notes](#notes) above.

#### 1.2.1 NIST P-256 key
- Sender key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-256",
  "x": "eFRTD4VaryfwIqLOpq7iuXmBbLjKPq5sVNzxwL7H1CI",
  "y": "cIeogn-pLJXlCepb9BqwNKKW4tmNea3Is8G47aPob6M",
  "d": "11NyNGrw4JoU7-_bwoZlVDTJi5vkMrSs4Nme_OHnx6Q"
}
```
- Sender kid (jwk thumbprint raw base64 URL encoded): `6PBTUbcLB7-Z4fuAFn42oC1PaMsNmjheq1FeZEUgV_8`
- Single Recipient key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-256",
  "x": "UP08dxIWu14HWRCI48Tnohm7jhaJ87fFdvYyf0w4lkg",
  "y": "ohZVfvhQViMGb_n-Y66TewBO2gtE_udG_DsNe8c-T8w",
  "d": "O0ikvlb4fh7daJpqd9JIgYk5e-twB0IYyKpoqmb7ZCc"
}
```
- Single Recipient kid (jwk thumbprint raw base64 URL encoded): `D_kHovGtLUZ_ssw_vhZcqsx3LvQ6qC5JK74iPf9vqwk`
- Finally, packing the payload outputs the following flattened serialized JWE JSON:
```json
{
  "protected": "eyJhbGciOiJFQ0RILTFQVStBMjU2S1ciLCJhcHUiOiJObEJDVkZWaVkweENOeTFhTkdaMVFVWnVOREp2UXpGUVlVMXpUbTFxYUdWeE1VWmxXa1ZWWjFaZk9BIiwiYXB2IjoiUkY5clNHOTJSM1JNVlZwZmMzTjNYM1pvV21OeGMzZ3pUSFpSTm5GRE5VcExOelJwVUdZNWRuRjNhdyIsImN0eSI6ImFwcGxpY2F0aW9uL2RpZGNvbW0tcGxhaW4ranNvbiIsImVuYyI6IkEyNTZHQ00iLCJlcGsiOnsiY3J2IjoiUC0yNTYiLCJrdHkiOiJFQyIsIngiOiJzODRGczRGeWRfSEVFQUN2R3dHak0wWDdGYUNwTlZ5cS1tM19MYXVwT2gwIiwieSI6IndsZzZoQnVnZElWMFlaekh1NHNQRnM0OXRtMGtXQlZjenQ0N25IenZ5UU0ifSwia2lkIjoiRF9rSG92R3RMVVpfc3N3X3ZoWmNxc3gzTHZRNnFDNUpLNzRpUGY5dnF3ayIsInNraWQiOiI2UEJUVWJjTEI3LVo0ZnVBRm40Mm9DMVBhTXNObWpoZXExRmVaRVVnVl84IiwidHlwIjoiYXBwbGljYXRpb24vZGlkY29tbS1lbmNyeXB0ZWQranNvbiJ9",
  "encrypted_key": "0L4GrPjXIy31JcEjV3sQj1Fbtb-dAtFPLng6mB0jyEyzDxzWcZZWag",
  "iv": "V26sXdaKTIo6SDMn",
  "ciphertext": "TJcEzgDbw5xDOMOwuuE",
  "tag": "vgtkaTIM407IG8ZqLLRk6Q"
}
```
- The compact serialization of this envelope is:
  `eyJhbGciOiJFQ0RILTFQVStBMjU2S1ciLCJhcHUiOiJObEJDVkZWaVkweENOeTFhTkdaMVFVWnVOREp2UXpGUVlVMXpUbTFxYUdWeE1VWmxXa1ZWWjFaZk9BIiwiYXB2IjoiUkY5clNHOTJSM1JNVlZwZmMzTjNYM1pvV21OeGMzZ3pUSFpSTm5GRE5VcExOelJwVUdZNWRuRjNhdyIsImN0eSI6ImFwcGxpY2F0aW9uL2RpZGNvbW0tcGxhaW4ranNvbiIsImVuYyI6IkEyNTZHQ00iLCJlcGsiOnsia3R5IjoiRUMiLCJjcnYiOiJQLTI1NiIsIngiOiJzODRGczRGeWRfSEVFQUN2R3dHak0wWDdGYUNwTlZ5cS1tM19MYXVwT2gwIiwieSI6IndsZzZoQnVnZElWMFlaekh1NHNQRnM0OXRtMGtXQlZjenQ0N25IenZ5UU0ifSwia2lkIjoiRF9rSG92R3RMVVpfc3N3X3ZoWmNxc3gzTHZRNnFDNUpLNzRpUGY5dnF3ayIsInNraWQiOiI2UEJUVWJjTEI3LVo0ZnVBRm40Mm9DMVBhTXNObWpoZXExRmVaRVVnVl84IiwidHlwIjoiYXBwbGljYXRpb24vZGlkY29tbS1lbmNyeXB0ZWQranNvbiJ9.0L4GrPjXIy31JcEjV3sQj1Fbtb-dAtFPLng6mB0jyEyzDxzWcZZWag.V26sXdaKTIo6SDMn.TJcEzgDbw5xDOMOwuuE.vgtkaTIM407IG8ZqLLRk6Q`
- The single recipient's headers are merged into the `protected` header, which base64 URL decoded equals to (pretty printed for readability):
```json
{
  "alg": "ECDH-1PU+A256KW",
  "apu": "NlBCVFViY0xCNy1aNGZ1QUZuNDJvQzFQYU1zTm1qaGVxMUZlWkVVZ1ZfOA",
  "apv": "RF9rSG92R3RMVVpfc3N3X3ZoWmNxc3gzTHZRNnFDNUpLNzRpUGY5dnF3aw",
  "cty": "application/didcomm-plain+json",
  "enc": "A256GCM",
  "epk": {
    "kty": "EC",
    "crv": "P-256",
    "x": "s84Fs4Fyd_HEEACvGwGjM0X7FaCpNVyq-m3_LaupOh0",
    "y": "wlg6hBugdIV0YZzHu4sPFs49tm0kWBVczt47nHzvyQM"
  },
  "kid": "D_kHovGtLUZ_ssw_vhZcqsx3LvQ6qC5JK74iPf9vqwk",
  "skid": "6PBTUbcLB7-Z4fuAFn42oC1PaMsNmjheq1FeZEUgV_8",
  "typ": "application/didcomm-encrypted+json"
}
```

#### 1.2.2 NIST P-384 key
- Sender key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-384",
  "x": "UW1LtMXuZdFS0gyp0_F19uxHqECvCcJA7SmeeuRSSc_PQfsbZWXt5L0KyLYpNIQb",
  "y": "FBdPcUvanB7igwkX0NN5rOvH3OKZ1gQHhcad7cCy6QNYKKz7lBWUUOmzypee31pS",
  "d": "wrXW0wsFKjvpTWqOAd1mohRublQs4P014-U4_K-eTRFmzhkyLJqNn91dH_AHUc4-"
}
```
- Sender kid (jwk thumbprint raw base64 URL encoded): `0Bz8yRwu9eC8Gi7cYOwAKMJ8jysInhAtwH8k8m9MX04`
- Single Recipient key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-384",
  "x": "k3W_RR59uUG3HFlhhqNNmBDyFdMtWHxKAsJaxLBqQgQer3d3aAN-lfdxzGnHtwj1",
  "y": "VMSy5zxFEGaGRINailLTUH6NlP0JO2qu0j0_UbS7Ng1b8JkzHDnDbjGgsLqVJaMM",
  "d": "iM5K8uqNvFYJnuToMDBguGwUIlu1erT-K0g7NYtJrQnHZOumS8yIC4MCNC60Ch91"
}
```
- Single Recipient kid (jwk thumbprint raw base64 URL encoded): `obCHRLVDx634Cax_Kr3B8fd_-xj5kAj0r0Kvvvmq1z8`
- Finally, packing the payload outputs the following flattened serialized JWE JSON:
```json
{
  "protected": "eyJhbGciOiJFQ0RILTFQVStBMjU2S1ciLCJhcHUiOiJNRUo2T0hsU2QzVTVaVU00UjJrM1kxbFBkMEZMVFVvNGFubHpTVzVvUVhSM1NEaHJPRzA1VFZnd05BIiwiYXB2IjoiYjJKRFNGSk1Wa1I0TmpNMFEyRjRYMHR5TTBJNFptUmZMWGhxTld0QmFqQnlNRXQyZG5adGNURjZPQSIsImN0eSI6ImFwcGxpY2F0aW9uL2RpZGNvbW0tcGxhaW4ranNvbiIsImVuYyI6IkEyNTZHQ00iLCJlcGsiOnsiY3J2IjoiUC0zODQiLCJrdHkiOiJFQyIsIngiOiJvZ1dJTHo4aXpDODNWNnFPNFVidHlSMTFadGdtRUMxQV9VM1JtVVV4dk9INE9lVW9xbUxXX295YjJXek5NTTZtIiwieSI6ImNobkphdHpRREJodzhqem5McUFmYWx3eFB3RmFKZjhVY2FzbjlmUWZyeUVWQ2FnRnRBYTNIb1FaSUxoeGxYSWUifSwia2lkIjoib2JDSFJMVkR4NjM0Q2F4X0tyM0I4ZmRfLXhqNWtBajByMEt2dnZtcTF6OCIsInNraWQiOiIwQno4eVJ3dTllQzhHaTdjWU93QUtNSjhqeXNJbmhBdHdIOGs4bTlNWDA0IiwidHlwIjoiYXBwbGljYXRpb24vZGlkY29tbS1lbmNyeXB0ZWQranNvbiJ9",
  "encrypted_key": "ojdzwycN1XFKuiwOmlgS4MHApmDAVKVZt1Zl7sgtJkafQRz81FUnZQ",
  "iv": "VqEJ6p5J0ZTIw2ts",
  "ciphertext": "jGznTL6ruVMXzV8xCA8",
  "tag": "YA_A4pjqqaAeUNvEFnCx8Q"
}
```
- The compact serialization of this envelope is:
  `eyJhbGciOiJFQ0RILTFQVStBMjU2S1ciLCJhcHUiOiJNRUo2T0hsU2QzVTVaVU00UjJrM1kxbFBkMEZMVFVvNGFubHpTVzVvUVhSM1NEaHJPRzA1VFZnd05BIiwiYXB2IjoiYjJKRFNGSk1Wa1I0TmpNMFEyRjRYMHR5TTBJNFptUmZMWGhxTld0QmFqQnlNRXQyZG5adGNURjZPQSIsImN0eSI6ImFwcGxpY2F0aW9uL2RpZGNvbW0tcGxhaW4ranNvbiIsImVuYyI6IkEyNTZHQ00iLCJlcGsiOnsia3R5IjoiRUMiLCJjcnYiOiJQLTM4NCIsIngiOiJvZ1dJTHo4aXpDODNWNnFPNFVidHlSMTFadGdtRUMxQV9VM1JtVVV4dk9INE9lVW9xbUxXX295YjJXek5NTTZtIiwieSI6ImNobkphdHpRREJodzhqem5McUFmYWx3eFB3RmFKZjhVY2FzbjlmUWZyeUVWQ2FnRnRBYTNIb1FaSUxoeGxYSWUifSwia2lkIjoib2JDSFJMVkR4NjM0Q2F4X0tyM0I4ZmRfLXhqNWtBajByMEt2dnZtcTF6OCIsInNraWQiOiIwQno4eVJ3dTllQzhHaTdjWU93QUtNSjhqeXNJbmhBdHdIOGs4bTlNWDA0IiwidHlwIjoiYXBwbGljYXRpb24vZGlkY29tbS1lbmNyeXB0ZWQranNvbiJ9.ojdzwycN1XFKuiwOmlgS4MHApmDAVKVZt1Zl7sgtJkafQRz81FUnZQ.VqEJ6p5J0ZTIw2ts.jGznTL6ruVMXzV8xCA8.YA_A4pjqqaAeUNvEFnCx8Q`
- The single recipient's headers are merged into the `protected` header, which base64 URL decoded equals to (pretty printed for readability):
```json
{
  "alg": "ECDH-1PU+A256KW",
  "apu": "MEJ6OHlSd3U5ZUM4R2k3Y1lPd0FLTUo4anlzSW5oQXR3SDhrOG05TVgwNA",
  "apv": "b2JDSFJMVkR4NjM0Q2F4X0tyM0I4ZmRfLXhqNWtBajByMEt2dnZtcTF6OA",
  "cty": "application/didcomm-plain+json",
  "enc": "A256GCM",
  "epk": {
    "kty": "EC",
    "crv": "P-384",
    "x": "ogWILz8izC83V6qO4UbtyR11ZtgmEC1A_U3RmUUxvOH4OeUoqmLW_oyb2WzNMM6m",
    "y": "chnJatzQDBhw8jznLqAfalwxPwFaJf8Ucasn9fQfryEVCagFtAa3HoQZILhxlXIe"
  },
  "kid": "obCHRLVDx634Cax_Kr3B8fd_-xj5kAj0r0Kvvvmq1z8",
  "skid": "0Bz8yRwu9eC8Gi7cYOwAKMJ8jysInhAtwH8k8m9MX04",
  "typ": "application/didcomm-encrypted+json"
}
```

#### 1.2.3 NIST P-521 key
- Sender key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-521",
  "x": "AXKDGPnD6hlQIre8aEeu33bQffkfl-eQfQXgzNXQX7XFYt5GKA1N6w4-f0_Ci7fQNKGkQuCoAu5-6CNk9M_cHiDi",
  "y": "Ae4-APhoZAmM99MdY9io9IZA43dN7dA006wlFb6LJ9bcusJOi5R-o3o3FhCjt5KTv_JxYbo6KU4PsBwQ1eeKyJ0U",
  "d": "AP9l2wmQ85P5XD84CkEQVWHaX_46EDvHxLWHEKsHFSQYjEh6BDSuyy1TUNv68v8kpbLCDjvsBc3cIBqC4_T1r4pU"
}
```
- Sender kid (jwk thumbprint raw base64 URL encoded): `oq-WBIGQm-iHiNRj6nId4-E1QtY8exzp8C56SziUfeU`
- Single Recipient key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-521",
  "x": "ALmUHkd9Gi2NApJojNzzA34Qdd1-KLnq6jd2UJ9wl-xJzTQ2leg8qi3-hrFs7NqNfxqO6vE5bBoWYFeAcf3LqJOU",
  "y": "AN-MutmkAXGzlgzSQJRnctHDcjQQNpRek-8BeqyUDXdZKNGKSMEAzw6Hnl3VdvsvihQfrxcajpx5PSnwxbbdakHq",
  "d": "AKv-YbKdI6y8NRMP-e17-RjZyRTfGf0Xh9Og5g7q7aq0xS2mO59ttIJ67XHW5SPTBQDbltdUcydKroWNUIGvhKNv"
}
```
- Single Recipient kid (jwk thumbprint raw base64 URL encoded): `XmLVV-CqMkTGQIe6-KecWZWtZVwORTMP2y5aqMPV7P4`
- Finally, packing the payload outputs the following flattened serialized JWE JSON:
```json
{
  "protected": "eyJhbGciOiJFQ0RILTFQVStBMjU2S1ciLCJhcHUiOiJiM0V0VjBKSlIxRnRMV2xJYVU1U2FqWnVTV1EwTFVVeFVYUlpPR1Y0ZW5BNFF6VTJVM3BwVldabFZRIiwiYXB2IjoiV0cxTVZsWXRRM0ZOYTFSSFVVbGxOaTFMWldOWFdsZDBXbFozVDFKVVRWQXllVFZoY1UxUVZqZFFOQSIsImN0eSI6ImFwcGxpY2F0aW9uL2RpZGNvbW0tcGxhaW4ranNvbiIsImVuYyI6IkEyNTZHQ00iLCJlcGsiOnsiY3J2IjoiUC01MjEiLCJrdHkiOiJFQyIsIngiOiJBRHdFcDBlZWJseGZhZHdkVFBlTV81b29MZGdHaWhLM3Bqd3AxakxXWmdxLUJrRV9IZDhnZFQ4RThOSFVvWjRFeWVvbWVKX3J0WGFlVnlHdjdoVzBPb1MtIiwieSI6IkFaY0Zzemg3RUstZ2lGQXRIZ2hPQ21uR3NNN1QzSzFjeUhBV0NwYXBqd2ZEclJjYnE5THdhQjFyRVVOdDMyYndLdWNNNG9idldkSndxVGE3SGVZYlNVOHUifSwia2lkIjoiWG1MVlYtQ3FNa1RHUUllNi1LZWNXWld0WlZ3T1JUTVAyeTVhcU1QVjdQNCIsInNraWQiOiJvcS1XQklHUW0taUhpTlJqNm5JZDQtRTFRdFk4ZXh6cDhDNTZTemlVZmVVIiwidHlwIjoiYXBwbGljYXRpb24vZGlkY29tbS1lbmNyeXB0ZWQranNvbiJ9",
  "encrypted_key": "9OyKH83g7RoS-ykrAoQpqn6FUUuYxeKukJbk6y2x9wfoe__rM8sP4w",
  "iv": "JO2ENu2k2O1OFgjl",
  "ciphertext": "wpomqxgGqQIWQ_lWCm4",
  "tag": "XgUX1EOGAePvjlcO7Dzb3A"
}
```
- The compact serialization of this envelope is:
  `eyJhbGciOiJFQ0RILTFQVStBMjU2S1ciLCJhcHUiOiJiM0V0VjBKSlIxRnRMV2xJYVU1U2FqWnVTV1EwTFVVeFVYUlpPR1Y0ZW5BNFF6VTJVM3BwVldabFZRIiwiYXB2IjoiV0cxTVZsWXRRM0ZOYTFSSFVVbGxOaTFMWldOWFdsZDBXbFozVDFKVVRWQXllVFZoY1UxUVZqZFFOQSIsImN0eSI6ImFwcGxpY2F0aW9uL2RpZGNvbW0tcGxhaW4ranNvbiIsImVuYyI6IkEyNTZHQ00iLCJlcGsiOnsia3R5IjoiRUMiLCJjcnYiOiJQLTUyMSIsIngiOiJBRHdFcDBlZWJseGZhZHdkVFBlTV81b29MZGdHaWhLM3Bqd3AxakxXWmdxLUJrRV9IZDhnZFQ4RThOSFVvWjRFeWVvbWVKX3J0WGFlVnlHdjdoVzBPb1MtIiwieSI6IkFaY0Zzemg3RUstZ2lGQXRIZ2hPQ21uR3NNN1QzSzFjeUhBV0NwYXBqd2ZEclJjYnE5THdhQjFyRVVOdDMyYndLdWNNNG9idldkSndxVGE3SGVZYlNVOHUifSwia2lkIjoiWG1MVlYtQ3FNa1RHUUllNi1LZWNXWld0WlZ3T1JUTVAyeTVhcU1QVjdQNCIsInNraWQiOiJvcS1XQklHUW0taUhpTlJqNm5JZDQtRTFRdFk4ZXh6cDhDNTZTemlVZmVVIiwidHlwIjoiYXBwbGljYXRpb24vZGlkY29tbS1lbmNyeXB0ZWQranNvbiJ9.9OyKH83g7RoS-ykrAoQpqn6FUUuYxeKukJbk6y2x9wfoe__rM8sP4w.JO2ENu2k2O1OFgjl.wpomqxgGqQIWQ_lWCm4.XgUX1EOGAePvjlcO7Dzb3A`
- The single recipient's headers are merged into the `protected` header, which base64 URL decoded equals to (pretty printed for readability):
```json
{
  "alg": "ECDH-1PU+A256KW",
  "apu": "b3EtV0JJR1FtLWlIaU5SajZuSWQ0LUUxUXRZOGV4enA4QzU2U3ppVWZlVQ",
  "apv": "WG1MVlYtQ3FNa1RHUUllNi1LZWNXWld0WlZ3T1JUTVAyeTVhcU1QVjdQNA",
  "cty": "application/didcomm-plain+json",
  "enc": "A256GCM",
  "epk": {
    "kty": "EC",
    "crv": "P-521",
    "x": "ADwEp0eeblxfadwdTPeM_5ooLdgGihK3pjwp1jLWZgq-BkE_Hd8gdT8E8NHUoZ4EyeomeJ_rtXaeVyGv7hW0OoS-",
    "y": "AZcFszh7EK-giFAtHghOCmnGsM7T3K1cyHAWCpapjwfDrRcbq9LwaB1rEUNt32bwKucM4obvWdJwqTa7HeYbSU8u"
  },
  "kid": "XmLVV-CqMkTGQIe6-KecWZWtZVwORTMP2y5aqMPV7P4",
  "skid": "oq-WBIGQm-iHiNRj6nId4-E1QtY8exzp8C56SziUfeU",
  "typ": "application/didcomm-encrypted+json"
}
```

#### 1.2.4 X25519 key
- Sender key JWK format:
```json
{
  "kty": "OKP",
  "crv": "X25519",
  "x": "WKkktGWkUB9hDITcqa1Z6MC8rcWy8fWtxuT7xwQF1lw",
  "d": "-LEcVt6bW_ah9gY7H_WknTsg1MXq8yc42SrSJhqP0Vo"
}
```
- Sender kid (jwk thumbprint raw base64 URL encoded): `X5INSMIv_w4Q7pljH7xjeUrRAKiBGHavSmOYyyiRugc`
- Single Recipient key JWK format:
```json
{
  "kty": "OKP",
  "crv": "X25519",
  "x": "NJzDtIa7vjz-isjaI-6GKGDe2EUx26-D44d6jLILeBI",
  "d": "MEBNdr6Tpb0XfD60NeHby-Tkmlpgr7pvVe7Q__sBbGw"
}
```
- Single Recipient kid (jwk thumbprint raw base64 URL encoded): `2UR-nzYjVhsq0cZakWjE38-wUdG0S2EIrLZ8Eh0KVO0`
- Finally, packing the payload outputs the following flattened serialized JWE JSON:
```json
{
  "protected": "eyJhbGciOiJFQ0RILTFQVStBMjU2S1ciLCJhcHUiOiJXRFZKVGxOTlNYWmZkelJSTjNCc2FrZzNlR3BsVlhKU1FVdHBRa2RJWVhaVGJVOVplWGxwVW5Wbll3IiwiYXB2IjoiTWxWU0xXNTZXV3BXYUhOeE1HTmFZV3RYYWtVek9DMTNWV1JITUZNeVJVbHlURm80Uldnd1MxWlBNQSIsImN0eSI6ImFwcGxpY2F0aW9uL2RpZGNvbW0tcGxhaW4ranNvbiIsImVuYyI6IkEyNTZHQ00iLCJlcGsiOnsiY3J2IjoiWDI1NTE5Iiwia3R5IjoiT0tQIiwieCI6InpxUDB0WHdqVVFxdnBvSVdqNS16U2Q0WVVZZjdmU2hta2dhR0dXRFFrbGsifSwia2lkIjoiMlVSLW56WWpWaHNxMGNaYWtXakUzOC13VWRHMFMyRUlyTFo4RWgwS1ZPMCIsInNraWQiOiJYNUlOU01Jdl93NFE3cGxqSDd4amVVclJBS2lCR0hhdlNtT1l5eWlSdWdjIiwidHlwIjoiYXBwbGljYXRpb24vZGlkY29tbS1lbmNyeXB0ZWQranNvbiJ9",
  "encrypted_key": "o_tprm3F-VJE2kHFrCBtgbCVDag0Y6AwLm1jD6S3MUS_rHphYy033w",
  "iv": "6GKRpv-Bs_2v_7a3",
  "ciphertext": "qlfWYkCE7zu-aRVP3R8",
  "tag": "oBDt6-tRYcLTMA7QhX0O2Q"
}
```
- The compact serialization of this envelope is:
  `eyJhbGciOiJFQ0RILTFQVStBMjU2S1ciLCJhcHUiOiJXRFZKVGxOTlNYWmZkelJSTjNCc2FrZzNlR3BsVlhKU1FVdHBRa2RJWVhaVGJVOVplWGxwVW5Wbll3IiwiYXB2IjoiTWxWU0xXNTZXV3BXYUhOeE1HTmFZV3RYYWtVek9DMTNWV1JITUZNeVJVbHlURm80Uldnd1MxWlBNQSIsImN0eSI6ImFwcGxpY2F0aW9uL2RpZGNvbW0tcGxhaW4ranNvbiIsImVuYyI6IkEyNTZHQ00iLCJlcGsiOnsia3R5IjoiT0tQIiwiY3J2IjoiWDI1NTE5IiwieCI6InpxUDB0WHdqVVFxdnBvSVdqNS16U2Q0WVVZZjdmU2hta2dhR0dXRFFrbGsifSwia2lkIjoiMlVSLW56WWpWaHNxMGNaYWtXakUzOC13VWRHMFMyRUlyTFo4RWgwS1ZPMCIsInNraWQiOiJYNUlOU01Jdl93NFE3cGxqSDd4amVVclJBS2lCR0hhdlNtT1l5eWlSdWdjIiwidHlwIjoiYXBwbGljYXRpb24vZGlkY29tbS1lbmNyeXB0ZWQranNvbiJ9.o_tprm3F-VJE2kHFrCBtgbCVDag0Y6AwLm1jD6S3MUS_rHphYy033w.6GKRpv-Bs_2v_7a3.qlfWYkCE7zu-aRVP3R8.oBDt6-tRYcLTMA7QhX0O2Q`
- The single recipient's headers are merged into the `protected` header, which base64 URL decoded equals to:
```json
{
  "alg": "ECDH-1PU+A256KW",
  "apu": "WDVJTlNNSXZfdzRRN3Bsakg3eGplVXJSQUtpQkdIYXZTbU9ZeXlpUnVnYw",
  "apv": "MlVSLW56WWpWaHNxMGNaYWtXakUzOC13VWRHMFMyRUlyTFo4RWgwS1ZPMA",
  "cty": "application/didcomm-plain+json",
  "enc": "A256GCM",
  "epk": {
    "kty": "OKP",
    "crv": "X25519",
    "x": "zqP0tXwjUQqvpoIWj5-zSd4YUYf7fShmkgaGGWDQklk"
  },
  "kid": "2UR-nzYjVhsq0cZakWjE38-wUdG0S2EIrLZ8Eh0KVO0",
  "skid": "X5INSMIv_w4Q7pljH7xjeUrRAKiBGHavSmOYyyiRugc",
  "typ": "application/didcomm-encrypted+json"
}
```

## 2 XC20P content encryption

### 2.1 Multi recipients JWEs

#### 2.1.1 NIST P-256 keys
The packer generates the following protected headers that includes the skid:
- Generated protected headers: `{"cty":"application/didcomm-plain+json","enc":"XC20P","skid":"T1jGtZoU-Xa_5a1QKexUU0Jq9WKDtS7TCowVvjoFH04","typ":"application/didcomm-encrypted+json"}`
  - raw (no padding) base64URL encoded: `eyJjdHkiOiJhcHBsaWNhdGlvbi9kaWRjb21tLXBsYWluK2pzb24iLCJlbmMiOiJYQzIwUCIsInNraWQiOiJUMWpHdFpvVS1YYV81YTFRS2V4VVUwSnE5V0tEdFM3VENvd1Z2am9GSDA0IiwidHlwIjoiYXBwbGljYXRpb24vZGlkY29tbS1lbmNyeXB0ZWQranNvbiJ9`
- Sender key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-256",
  "x": "46OXm1dUTO3MB-8zoxbn-9dk0khgeIqsKFO-nTJ9keM",
  "y": "8IlrwB-dl5bFd5RT4YAbgAdj5Y-a9zhc9wCMnXDZDvA",
  "d": "58GZDz9_opy-nEeaJ_cyEL63TO-l063aV5nLADCgsGY"
}
```
- Sender kid (jwk thumbprint raw base64 URL encoded): `T1jGtZoU-Xa_5a1QKexUU0Jq9WKDtS7TCowVvjoFH04`
- Recipient 1 key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-256",
  "x": "r9MRjEQ7CBxAgMyEG3ZjIlkGCuRX0rTaBdbkAcY17hA",
  "y": "MRSgHQycDFPdSABGv5V0Qd-2q7ebs_x0_fNFyabGgXU",
  "d": "LK9yfSxuET5n5uZDNO-64sJKWxJs7LTkqhA4mAuKQnE"
}
```
- Recipient 1 kid (jwk thumbprint raw base64 URL encoded): `dmfXisqWjRT-tFpODOD-G0CBF6zjHywNUjrrD3IFmcs`
- Recipient 2 key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-256",
  "x": "PMhlaU_KNEWou004AEyAFoJi8vNOnY75ROiRzzjhDR0",
  "y": "tEcJNRv2rqYlYWeRloRabcp2lRorRaZTLM0ZNBoEyN0",
  "d": "t1-QysBdkbkpqEBDo_JPsi-6YqD24UoAGBrruI2XNhA"
}
```
- Recipient 2 kid (jwk thumbprint raw base64 URL encoded): `2_Sf_YshIFhQ11NH9muAxLWwyFUvJnfXbYFOAC-8HTw`
- Recipient 3 key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-256",
  "x": "V9dWH69KZ_bvrxdWgt5-o-KnZLcGuWjAKVWMueiQioM",
  "y": "lvsUBieuXV6qL4R3L94fCJGu8SDifqh3fAtN2plPWX4",
  "d": "llg97kts4YxIF-r3jn7wcZ-zV0hLcn_AydIKHDF-HJc"
}
```
- Recipient 3 kid (jwk thumbprint raw, no padding, base64 URL encoded): `mKtrI7SV3z2U9XyhaaTYlQFX1ANi6Wkli8b3NWVq4C4`
- List of kids used for AAD for the above recipients (sorted `kid` values joined with `.`): `2_Sf_YshIFhQ11NH9muAxLWwyFUvJnfXbYFOAC-8HTw.dmfXisqWjRT-tFpODOD-G0CBF6zjHywNUjrrD3IFmcs.mKtrI7SV3z2U9XyhaaTYlQFX1ANi6Wkli8b3NWVq4C4`
- Resulting AAD value (sha256 of above list raw, no padding, base64 URL encoded): `PNKzNc6e0MtDtIGamjsx2fytSu6t8GygofQbzTrtMNA`
- Finally, packing the payload outputs the following JWE (pretty printed for readability):
```json
{
  "protected": "eyJjdHkiOiJhcHBsaWNhdGlvbi9kaWRjb21tLXBsYWluK2pzb24iLCJlbmMiOiJYQzIwUCIsInNraWQiOiJUMWpHdFpvVS1YYV81YTFRS2V4VVUwSnE5V0tEdFM3VENvd1Z2am9GSDA0IiwidHlwIjoiYXBwbGljYXRpb24vZGlkY29tbS1lbmNyeXB0ZWQranNvbiJ9",
  "recipients": [
    {
      "header": {
        "alg": "ECDH-1PU+XC20PKW",
        "apu": "VDFqR3Rab1UtWGFfNWExUUtleFVVMEpxOVdLRHRTN1RDb3dWdmpvRkgwNA",
        "apv": "ZG1mWGlzcVdqUlQtdEZwT0RPRC1HMENCRjZ6akh5d05VanJyRDNJRm1jcw",
        "kid": "dmfXisqWjRT-tFpODOD-G0CBF6zjHywNUjrrD3IFmcs",
        "epk": {
          "kty": "EC",
          "crv": "P-256",
          "x": "80NGcUh0mIy_XrcaAqD7GCHF0FU2W5j4Jt-wfwxvJVs",
          "y": "KpsNL9A-FGgL7S97ce8wcWYc9J1Q6_luxKAFIu7BNIw"
        }
      },
      "encrypted_key": "wGQO8LX7o9JmYI0PIGUruU7i6ybZYefsTanZuo7hIDyn21ix6fSFPOmvgjPxZ8q_-hZF2yGYtudfLiuPzXlybWJkmTlP9PcY"
    },
    {
      "header": {
        "alg": "ECDH-1PU+XC20PKW",
        "apu": "VDFqR3Rab1UtWGFfNWExUUtleFVVMEpxOVdLRHRTN1RDb3dWdmpvRkgwNA",
        "apv": "ZG1mWGlzcVdqUlQtdEZwT0RPRC1HMENCRjZ6akh5d05VanJyRDNJRm1jcw",
        "kid": "2_Sf_YshIFhQ11NH9muAxLWwyFUvJnfXbYFOAC-8HTw",
        "epk": {
          "kty": "EC",
          "crv": "P-256",
          "x": "4YrbAQCLLya1XqRvjfcYdonllWQulrLP7zE0ooclKXA",
          "y": "B3tI8lsWHRwBQ19pAFzXiBkLgpE6leTeQT6b709gllE"
        }
      },
      "encrypted_key": "5tY3t1JI8L6s974kmXbzKMaePHygNan2Qqpd1B0BiqBsjaHNUH2Unv1IMGiT3oQD0xXeVPAxQq7vNZgANitxBbgG_uxGiRld"
    },
    {
      "header": {
        "alg": "ECDH-1PU+XC20PKW",
        "apu": "VDFqR3Rab1UtWGFfNWExUUtleFVVMEpxOVdLRHRTN1RDb3dWdmpvRkgwNA",
        "apv": "ZG1mWGlzcVdqUlQtdEZwT0RPRC1HMENCRjZ6akh5d05VanJyRDNJRm1jcw",
        "kid": "mKtrI7SV3z2U9XyhaaTYlQFX1ANi6Wkli8b3NWVq4C4",
        "epk": {
          "kty": "EC",
          "crv": "P-256",
          "x": "-e9kPGp2rmtpFs2zzTaY6xfeXjr1Xua1vHCQZRKJ54s",
          "y": "Mc7b8U06KHV__1-XMaReilLxa63LcICqsPtkZGXEkEs"
        }
      },
      "encrypted_key": "zVQUQytYv4EmQS0zye3IsXiN_2ol-Qn2nvyaJgEPvNdwFuzTFPOupTl-PeOhkRvxPfuLlw5TKnSRyPUejP8zyHbBgUZ6gDmz"
    }
  ],
  "aad": "PNKzNc6e0MtDtIGamjsx2fytSu6t8GygofQbzTrtMNA",
  "iv": "UKgm1XTPf1QFDXoRWlf-KrsBRQKSwpBA",
  "ciphertext": "pbwy8HEnr1hPA0Jt5ho",
  "tag": "nUazXvxpMXGoL1__92CAyA"
}
```

#### 2.1.2 NIST P-384 keys
The packer generates the following protected headers that includes the skid:
- Generated protected headers: `{"cty":"application/didcomm-plain+json","enc":"XC20P","skid":"xXdnS3M4Bb497A0ko9c6H0D4NNbj1XpwGr4Tk9Fcw7k","typ":"application/didcomm-encrypted+json"}`
  - raw (no padding) base64URL encoded: `eyJjdHkiOiJhcHBsaWNhdGlvbi9kaWRjb21tLXBsYWluK2pzb24iLCJlbmMiOiJYQzIwUCIsInNraWQiOiJ4WGRuUzNNNEJiNDk3QTBrbzljNkgwRDROTmJqMVhwd0dyNFRrOUZjdzdrIiwidHlwIjoiYXBwbGljYXRpb24vZGlkY29tbS1lbmNyeXB0ZWQranNvbiJ9`
- Sender key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-384",
  "x": "bfuATmVQ_jxLIgfuhKNYrNRNu-VnK4FzTCCVRvycgekS8fIuC4rZS9uQi6Q2Ujwd",
  "y": "XkVJ93cLKpeZeCMEOsHRKk4rse1zXpzY6yUibEtwZG9nFWF05Ro8OQs5fZVK2TWC",
  "d": "OVzGxGyyaHGJpx1MoSwPjmWPas28sfq1tj7UkYFoK3ENsujmzUduAW6HwyaBlXRW"
}
```
- Sender kid (jwk thumbprint raw base64 URL encoded): `xXdnS3M4Bb497A0ko9c6H0D4NNbj1XpwGr4Tk9Fcw7k`
- Recipient 1 key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-384",
  "x": "xhk5K7x4xw9OJpkFhmsY39jceQqx57psvcZstiNZmKbXD7kT9ajfGKFA6YA-ali5",
  "y": "7Hj32-JDMNDYWRGy3f-0E9lbUGp6yURMaZ9M36Q_FPgljKgHa9i0Fn1ogr_zEmO3",
  "d": "Pc3r6eg15XZeKgTDMPcGjf_SvImZxG4bDzgCh3QShClAwMdmoNbzPZGhBByNrlvO"
}
```
- Recipient 1 kid (jwk thumbprint raw base64 URL encoded): `aIlhDTWJmT-_Atad5EBbvbZPkPnz2IYT85I6T44kcE4`
- Recipient 2 key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-384",
  "x": "wqW3DUkUAT0Cyk3hq0KVJbqtPSJOoqulp_Tqa29jBEPliIJ9rnq7cRkJyxArCYAj",
  "y": "ZfBtdTTVRh9SeQDCwsgAo15cCX2I-7J6xdyxDPyH8LBhbUA_8npHvNquKGta9p8x",
  "d": "krddjYsOD4YIIkNjWXTrYV9rOVlmLNaeoLHChJ5oUr4c21LHxGL4xTI1bEoXKgJ2"
}
```
- Recipient 2 kid (jwk thumbprint raw base64 URL encoded): `02WdA5ip_Amam611KA6fdoTs533yZH-ovfpt8t9zVjg`
- Recipient 3 key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-384",
  "x": "If6iEafrkcL53mVYCbm5rmnwAw3kjb13gUjBoDePggO7xMiSFyej4wbTabdCyfbg",
  "y": "nLX6lEce-9r19NA_nI5mGK3YFLiX9IYRgXZZCUd_Br91PaE8Mr1JR01utAPoGx36",
  "d": "jriJKFpQfzJtOrp7PhGvH0osHJQJbZrAKjD95itivioVawzMz9wcI_h9VsFV3ff0"
}
```
- Recipient 3 kid (jwk thumbprint raw, no padding, base64 URL encoded): `zeqnfYLFWtnJ_e5npBs7CtM5KkToyyM9kCKIFlcyId0`
- List of kids used for AAD for the above recipients (sorted `kid` values joined with `.`): `02WdA5ip_Amam611KA6fdoTs533yZH-ovfpt8t9zVjg.aIlhDTWJmT-_Atad5EBbvbZPkPnz2IYT85I6T44kcE4.zeqnfYLFWtnJ_e5npBs7CtM5KkToyyM9kCKIFlcyId0`
- Resulting AAD value (sha256 of above list raw, no padding, base64 URL encoded): `CftHmHttuxR6mRrHe-zBXV2UEvL2wvZEt5yeFDhYSF8`
- Finally, packing the payload outputs the following JWE (pretty printed for readability):
```json
{
  "protected": "eyJjdHkiOiJhcHBsaWNhdGlvbi9kaWRjb21tLXBsYWluK2pzb24iLCJlbmMiOiJYQzIwUCIsInNraWQiOiJ4WGRuUzNNNEJiNDk3QTBrbzljNkgwRDROTmJqMVhwd0dyNFRrOUZjdzdrIiwidHlwIjoiYXBwbGljYXRpb24vZGlkY29tbS1lbmNyeXB0ZWQranNvbiJ9",
  "recipients": [
    {
      "header": {
        "alg": "ECDH-1PU+XC20PKW",
        "apu": "eFhkblMzTTRCYjQ5N0Ewa285YzZIMEQ0Tk5iajFYcHdHcjRUazlGY3c3aw",
        "apv": "YUlsaERUV0ptVC1fQXRhZDVFQmJ2YlpQa1BuejJJWVQ4NUk2VDQ0a2NFNA",
        "kid": "aIlhDTWJmT-_Atad5EBbvbZPkPnz2IYT85I6T44kcE4",
        "epk": {
          "kty": "EC",
          "crv": "P-384",
          "x": "k7SRlQ7EwCR8VZ-LF92zOgvpFDAed0mN3mmZeCHHDznZp5TLQShFT9TdnwgsvJFP",
          "y": "ZHzkS9BD-I2DtNPhbXuTzf6vUnykdZPus9xZnRu1rWgxVtLQ8j-Jp4YoJgdQmcOu"
        }
      },
      "encrypted_key": "BO597Rs1RU3ZU-WdzWPgRnPmRULcFBihZxE7Jvl3qw3VUmR5RUXY0Xy9k_dWRnuRCh9Yzxef7tXlqVMaL4KBCfaAbAEOReQw"
    },
    {
      "header": {
        "alg": "ECDH-1PU+XC20PKW",
        "apu": "eFhkblMzTTRCYjQ5N0Ewa285YzZIMEQ0Tk5iajFYcHdHcjRUazlGY3c3aw",
        "apv": "YUlsaERUV0ptVC1fQXRhZDVFQmJ2YlpQa1BuejJJWVQ4NUk2VDQ0a2NFNA",
        "kid": "02WdA5ip_Amam611KA6fdoTs533yZH-ovfpt8t9zVjg",
        "epk": {
          "kty": "EC",
          "crv": "P-384",
          "x": "QT9Q_zU9VE3K9r_50mKh7iG8SxYeXVvwnhykphMAk8akfnTeB7FIRC2MzFat9JMT",
          "y": "3HeQPqQ_BS5vy2e2L7kgMhHNwNQ2K1pmL9LImrBg8XROuc9EaAGnFSQ439bZXg9y"
        }
      },
      "encrypted_key": "oKVlxrYhp8Bvr6s6CW7DxTSCMIFMkqLjDP9sCIkLoetHlXM5Mngq46CUqHusKTceHdSOL8sGUbeSBo6lXRKArywtjiVVyStW"
    },
    {
      "header": {
        "alg": "ECDH-1PU+XC20PKW",
        "apu": "eFhkblMzTTRCYjQ5N0Ewa285YzZIMEQ0Tk5iajFYcHdHcjRUazlGY3c3aw",
        "apv": "YUlsaERUV0ptVC1fQXRhZDVFQmJ2YlpQa1BuejJJWVQ4NUk2VDQ0a2NFNA",
        "kid": "zeqnfYLFWtnJ_e5npBs7CtM5KkToyyM9kCKIFlcyId0",
        "epk": {
          "kty": "EC",
          "crv": "P-384",
          "x": "GGFw14WnABx5S__MLwjy7WPgmPzCNbygbJikSqwx1nQ7APAiIyLeiAeZnAFQSr8C",
          "y": "Bjev4lkaRbd4Ery0vnO8Ox4QgIDGbuflmFq0HhL-QHIe3KhqxrqZqbQYGlDNudEv"
        }
      },
      "encrypted_key": "S8vnyPjW_19Hws3-igk-cVTSqVTY0_D9SWahnYnWBFBqTdx0b0e8hf06Oiou31Ww-Y3p8Z3O_okqQGzZMWUMLSxUPeCR2ZWx"
    }
  ],
  "aad": "CftHmHttuxR6mRrHe-zBXV2UEvL2wvZEt5yeFDhYSF8",
  "iv": "jTaCuNXs4QdX6HuWvl5AsqIEv4nh2JMP",
  "ciphertext": "7y463zoRKgVfpKh3EBw",
  "tag": "8YKdJpF2DnQQwEkBcbuEnw"
}
```

#### 2.1.3 NIST P-521 keys
The packer generates the following protected headers that includes the skid:
- Generated protected headers: `{"cty":"application/didcomm-plain+json","enc":"XC20P","skid":"bq3OI5517dSIMeD9K3lTqvkvvkmsRtifD6tvjlrKYsU","typ":"application/didcomm-encrypted+json"}`
  - raw (no padding) base64URL encoded: `eyJjdHkiOiJhcHBsaWNhdGlvbi9kaWRjb21tLXBsYWluK2pzb24iLCJlbmMiOiJYQzIwUCIsInNraWQiOiJicTNPSTU1MTdkU0lNZUQ5SzNsVHF2a3Z2a21zUnRpZkQ2dHZqbHJLWXNVIiwidHlwIjoiYXBwbGljYXRpb24vZGlkY29tbS1lbmNyeXB0ZWQranNvbiJ9`
- Sender key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-521",
  "x": "ACN9T83BbPNn1eRyo-TrL0GyC7kBNQvgUxk55fCeQKDSTVhbzCKia7WecCUshyEF-BOQbfEsOIUCq3g7xY3VEeth",
  "y": "APDIfDv6abLQ-Zb_p8PxwJe1x3U0-PdgXLNbtS7evGuUROHt79SVkpfXcZ3UaEc6cMoFfd2oMvbmUjCMM4-Sgipn",
  "d": "AXCGyR9uXY8vDr7D4HvMxep-d5biQzgHR6WsdOF4R5M9qYb8FhRIQCMbmDSZzCuqgGgXrPRMPm5-omvWVeYqwwa3"
}
```
- Sender kid (jwk thumbprint raw base64 URL encoded): `bq3OI5517dSIMeD9K3lTqvkvvkmsRtifD6tvjlrKYsU`
- Recipient 1 key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-521",
  "x": "AZi-AxJkB09qw8dBnNrz53xM-wER0Y5IYXSEWSTtzI5Sdv_5XijQn9z-vGz1pMdww-C75GdpAzp2ghejZJSxbAd6",
  "y": "AZzRvW8NBytGNbF3dyNOMHB0DHCOzGp8oYBv_ZCyJbQUUnq-TYX7j8-PlKe9Ce5acxZzrcUKVtJ4I8JgI5x9oXIW",
  "d": "AHGOZNkAcQCdDZOpQRdbH-f89mpjY_kGmtEpTExd51CcRlHhXuuAr6jcgb8YStwy9FN7vCU1y5LnJfKhGUGrP2a4"
}
```
- Recipient 1 kid (jwk thumbprint raw base64 URL encoded): `7icoqReWFlpF16dzZD3rBgK1cJ265WzfF9sJJXqOe0M`
- Recipient 2 key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-521",
  "x": "ASRvWU-d_XI2S1UQb7PoXIXTLXd8vgLmFb-9mmmIrzTMmIXFXpsDN9_1-Xg_r3qkEg-zBjTi327GIseWFGMa0Mrp",
  "y": "AJ0VyjDn4Rn6SKamFms4593mW5K936d4Jr7-J5OjJqTZtS6APgNkrwFjhKPHQfg7o8T4pmX7vlfFY5Flx7IOYJuw",
  "d": "ALzWMohuwSqkiqqEhijiBoH6kJ580Dtxe7CfgqEboc5DG0pMtAUf-a91VbmR1U8bQox-B4_YRXoFLRns2tI_wPYz"
}
```
- Recipient 2 kid (jwk thumbprint raw base64 URL encoded): `BUEVQ3FlDsml4JYrLCwwsL5BUZt-hYwb2B0SoJ6dzHc`
- Recipient 3 key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-521",
  "x": "AB2ke_2nVg95OP3Xb4Fg0Gg4KgfZZf3wBEYoOlGhXmHNCj56G10vnOe1hGRKIoD-JkPWuulcUtsIUO7r3Rz2mLP0",
  "y": "AJTaqfF8d4cFv_fP4Uoqq-uCCObmyPsD1CphbCuCZumarfzjA5SpAQCdfz3No4Nhn53OqdcTkm654Yvfj1vOp5t6",
  "d": "Af6Ba1x6i6glhRcR2RmZMZJ5BJXibpMB0TqjY_2Fe2LekS9QQK21JtrF20dj_gahxcrnfcn8oJ2xCrEMKaexgcsb"
}
```
- Recipient 3 kid (jwk thumbprint raw, no padding, base64 URL encoded): `C9iN-jkTFBbTz3Yv3FquR3dAsHYnAIg1_hT0jsefLDE`
- List of kids used for AAD for the above recipients (sorted `kid` values joined with `.`): `7icoqReWFlpF16dzZD3rBgK1cJ265WzfF9sJJXqOe0M.BUEVQ3FlDsml4JYrLCwwsL5BUZt-hYwb2B0SoJ6dzHc.C9iN-jkTFBbTz3Yv3FquR3dAsHYnAIg1_hT0jsefLDE`
- Resulting AAD value (sha256 of above list raw, no padding, base64 URL encoded): `VBNrffp39h1F6sg0dzkArcd2WjpKeqEvqt6HNXaVfKU`
- Finally, packing the payload outputs the following JWE (pretty printed for readability):
```json
{
  "protected": "eyJjdHkiOiJhcHBsaWNhdGlvbi9kaWRjb21tLXBsYWluK2pzb24iLCJlbmMiOiJYQzIwUCIsInNraWQiOiJicTNPSTU1MTdkU0lNZUQ5SzNsVHF2a3Z2a21zUnRpZkQ2dHZqbHJLWXNVIiwidHlwIjoiYXBwbGljYXRpb24vZGlkY29tbS1lbmNyeXB0ZWQranNvbiJ9",
  "recipients": [
    {
      "header": {
        "alg": "ECDH-1PU+XC20PKW",
        "apu": "YnEzT0k1NTE3ZFNJTWVEOUszbFRxdmt2dmttc1J0aWZENnR2amxyS1lzVQ",
        "apv": "N2ljb3FSZVdGbHBGMTZkelpEM3JCZ0sxY0oyNjVXemZGOXNKSlhxT2UwTQ",
        "kid": "7icoqReWFlpF16dzZD3rBgK1cJ265WzfF9sJJXqOe0M",
        "epk": {
          "kty": "EC",
          "crv": "P-521",
          "x": "ABd71Xomy3mv-mkAipKb18UQ-1xXt7tGDDwf0k5fpLADg1qK--Jhn8TdzyjTuve7rJQrlCJH4GjuQjCWVs4T7J_T",
          "y": "ANrWrk69QRi4cr8ZbU2vF_0jSjTIUn-fQCHJtxLg3uuvLtzGW7oIEkUFJq_sTZXL_gaPdFIWlI4aIjKRgzOUP_ze"
        }
      },
      "encrypted_key": "lZa-4LTyaDP01wmN8bvoD69MLl3VY2H_wNaNJ7kYzTFExlgYTPNrFJ5XL6T_h1DUULX0TYJVxbIWQeJ_x_7i-xSv7-BHbFcm"
    },
    {
      "header": {
        "alg": "ECDH-1PU+XC20PKW",
        "apu": "YnEzT0k1NTE3ZFNJTWVEOUszbFRxdmt2dmttc1J0aWZENnR2amxyS1lzVQ",
        "apv": "N2ljb3FSZVdGbHBGMTZkelpEM3JCZ0sxY0oyNjVXemZGOXNKSlhxT2UwTQ",
        "kid": "BUEVQ3FlDsml4JYrLCwwsL5BUZt-hYwb2B0SoJ6dzHc",
        "epk": {
          "kty": "EC",
          "crv": "P-521",
          "x": "ALGN2OH1_DKtEZ-990uL1kzHYhYmZD-stOdL6_NMReCKEPZil7Z1tsq0g9l0HNi6DWuMjNyiJCfDd1erWpByFAOX",
          "y": "AQgB2aE_3GltqbWzKbWbLa6Fdq6jO4A3LrYUnNDNIuHY6eRH9sRU0yWjmcmWCoukT98wksXJ3isHr9-NqFuZLehi"
        }
      },
      "encrypted_key": "bybMPkSjuSz8lLAPFJHrxjl1buE8cfONEzvQ2U64h8L0QEZPLK_VewbXVflEPNrOo3oTWlI_878GIKvkxJ8cJOD6a0kZmr87"
    },
    {
      "header": {
        "alg": "ECDH-1PU+XC20PKW",
        "apu": "YnEzT0k1NTE3ZFNJTWVEOUszbFRxdmt2dmttc1J0aWZENnR2amxyS1lzVQ",
        "apv": "N2ljb3FSZVdGbHBGMTZkelpEM3JCZ0sxY0oyNjVXemZGOXNKSlhxT2UwTQ",
        "kid": "C9iN-jkTFBbTz3Yv3FquR3dAsHYnAIg1_hT0jsefLDE",
        "epk": {
          "kty": "EC",
          "crv": "P-521",
          "x": "AZKyI6Mg8OdKUYqo3xuKjHiVrlV56_qGBzdwr86QSnebq3Y69Z0qETiTumQv5J3ECmZzs4DiETryRuzdHc2RkKBZ",
          "y": "ARJJT7MWjTWWB7leblQgg7PYn_0deScO7AATlcnukFsLbzly0LHs1msVXaerQUCHPg2t-sYGxDP7w0iaDHB8k3Tj"
        }
      },
      "encrypted_key": "nMGoNk1brn9uO9hlSa7NwVgFUMXnxpKKPkuFHSE2aM_N8q8wJbVBLC9rJ9sPIiSU20tq2sJXaAcoMteajOX6wj_Hzl1uRT1e"
    }
  ],
  "aad": "VBNrffp39h1F6sg0dzkArcd2WjpKeqEvqt6HNXaVfKU",
  "iv": "h0bbZygiAx9MMO2Huxym_QnwrXZHhdyQ",
  "ciphertext": "LABYmf_sfPNGgls0wvk",
  "tag": "z1rZOEgyryiW_3d5gxnMUQ"
}
```

#### 2.1.4 X25519 keys
The packer generates the following protected headers that includes the skid:
- Generated protected headers: `{"cty":"application/didcomm-plain+json","enc":"XC20P","skid":"j8E-tcw1Z_eOCoKEH-7a9T532r8zXfcavbPZlofN0Ek","typ":"application/didcomm-encrypted+json"}`
  - raw (no padding) base64URL encoded: `eyJjdHkiOiJhcHBsaWNhdGlvbi9kaWRjb21tLXBsYWluK2pzb24iLCJlbmMiOiJYQzIwUCIsInNraWQiOiJqOEUtdGN3MVpfZU9Db0tFSC03YTlUNTMycjh6WGZjYXZiUFpsb2ZOMEVrIiwidHlwIjoiYXBwbGljYXRpb24vZGlkY29tbS1lbmNyeXB0ZWQranNvbiJ9`
- Sender key JWK format:
```json
{
  "kty": "OKP",
  "crv": "X25519",
  "x": "g3Lpdd_DRgjK28qi0sR0-hI-zv7a1X52vpzKc6ZM1Qs",
  "d": "cPU_Io7RRHNb_xkQ_D6u3ER4vSjvsILDCKwOj8kVHXQ"
}
```
- Sender kid (jwk thumbprint raw base64 URL encoded): `j8E-tcw1Z_eOCoKEH-7a9T532r8zXfcavbPZlofN0Ek`
- Recipient 1 key JWK format:
```json
{
  "kty": "OKP",
  "crv": "X25519",
  "x": "VlhpUXj-oGs9ge-VLrmYF7Xuzy73YchIfckaYcQefBw",
  "d": "QFHCCy0wzgJ_AlGMnjetTd0tnDaZ_7yqJODSV0d-kkg"
}
```
- Recipient 1 kid (jwk thumbprint raw base64 URL encoded): `_DHSbVaMeZxriDJn5VoHXYXo6BJacwZx_fGIBfCiJ5c`
- Recipient 2 key JWK format:
```json
{
  "kty": "OKP",
  "crv": "X25519",
  "x": "y52sexwATOR5J5znNp94MFx19J0rkgzNyLESMVhkE2M",
  "d": "6NwEk3_8lKOwLaZM2YkLdW9MF2zDqMjAx_G-uDoAAkw"
}
```
- Recipient 2 kid (jwk thumbprint raw base64 URL encoded): `n2MxD23PaCkz7vptma_1j9X2JdUoCFLzrtYuDvOA0Kc`
- Recipient 3 key JWK format:
```json
{
  "kty": "OKP",
  "crv": "X25519",
  "x": "BYL51mNvx1LKD2wDfga_7GZc0YYI82HhRmHtXfiz_ko",
  "d": "MLd_nsRRb_CSzc6Ou8TZFm-A17ZpT1Aen6fIvC6ZuV8"
}
```
- Recipient 3 kid (jwk thumbprint raw, no padding, base64 URL encoded): `HHN2ZcES5ps7gCjK-06bCE4EjX_hh7nq2cWd-GfnI5s`
- List of kids used for AAD for the above recipients (sorted `kid` values joined with `.`): `HHN2ZcES5ps7gCjK-06bCE4EjX_hh7nq2cWd-GfnI5s._DHSbVaMeZxriDJn5VoHXYXo6BJacwZx_fGIBfCiJ5c.n2MxD23PaCkz7vptma_1j9X2JdUoCFLzrtYuDvOA0Kc`
- Resulting AAD value (sha256 of above list raw, no padding, base64 URL encoded): `K1oFStibrX4x6LplTB0-tO3cwGiZzMvG_6w0LfguVuI`
- Finally, packing the payload outputs the following JWE (pretty printed for readability):
```json
{
  "protected": "eyJjdHkiOiJhcHBsaWNhdGlvbi9kaWRjb21tLXBsYWluK2pzb24iLCJlbmMiOiJYQzIwUCIsInNraWQiOiJqOEUtdGN3MVpfZU9Db0tFSC03YTlUNTMycjh6WGZjYXZiUFpsb2ZOMEVrIiwidHlwIjoiYXBwbGljYXRpb24vZGlkY29tbS1lbmNyeXB0ZWQranNvbiJ9",
  "recipients": [
    {
      "header": {
        "alg": "ECDH-1PU+XC20PKW",
        "apu": "ajhFLXRjdzFaX2VPQ29LRUgtN2E5VDUzMnI4elhmY2F2YlBabG9mTjBFaw",
        "apv": "X0RIU2JWYU1lWnhyaURKbjVWb0hYWVhvNkJKYWN3WnhfZkdJQmZDaUo1Yw",
        "kid": "_DHSbVaMeZxriDJn5VoHXYXo6BJacwZx_fGIBfCiJ5c",
        "epk": {
          "kty": "OKP",
          "crv": "X25519",
          "x": "77VAbpx5xn2iavmhzZATXwGnxjRyxjBbtNzojdWP7wo"
        }
      },
      "encrypted_key": "dvBscDJj2H6kZJgfdqazZ9pXZxUzai-mcExsdr11-RNvxxPd4_Cy6rolLSsY6ugm1sCo9BgRhAW1e6vxgTnY3Ctv0_xZIhvr"
    },
    {
      "header": {
        "alg": "ECDH-1PU+XC20PKW",
        "apu": "ajhFLXRjdzFaX2VPQ29LRUgtN2E5VDUzMnI4elhmY2F2YlBabG9mTjBFaw",
        "apv": "X0RIU2JWYU1lWnhyaURKbjVWb0hYWVhvNkJKYWN3WnhfZkdJQmZDaUo1Yw",
        "kid": "n2MxD23PaCkz7vptma_1j9X2JdUoCFLzrtYuDvOA0Kc",
        "epk": {
          "kty": "OKP",
          "crv": "X25519",
          "x": "sZtHwxjaS51BR2SBGC32jFvUgVlABZ7rkBFqJk8ktXM"
        }
      },
      "encrypted_key": "2gIQKw_QpnfGbIOso_XesSGWC9ZKu4-ox1eqRu71aS-nBWAbFrdJPqSY7gzAOGUNqg_o6mC1q7coG69G9yen37DIjcoR6mD1"
    },
    {
      "header": {
        "alg": "ECDH-1PU+XC20PKW",
        "apu": "ajhFLXRjdzFaX2VPQ29LRUgtN2E5VDUzMnI4elhmY2F2YlBabG9mTjBFaw",
        "apv": "X0RIU2JWYU1lWnhyaURKbjVWb0hYWVhvNkJKYWN3WnhfZkdJQmZDaUo1Yw",
        "kid": "HHN2ZcES5ps7gCjK-06bCE4EjX_hh7nq2cWd-GfnI5s",
        "epk": {
          "kty": "OKP",
          "crv": "X25519",
          "x": "48AJF8kNoxfHXpUtBApRMUcTf8B0Ho4i_6CvGT4arGY"
        }
      },
      "encrypted_key": "o_toInYq_NP45UqqFg461O6ruUNSQNKrBXRDA06JQ-faMUUfMGRtzNHK-FzrhtodZLW5bRFFFry9aFjwg5aYloe2JG9-fEcw"
    }
  ],
  "aad": "K1oFStibrX4x6LplTB0-tO3cwGiZzMvG_6w0LfguVuI",
  "iv": "tcThx2bVV8jhteYknijC-vxSED_BKPF8",
  "ciphertext": "DUZLQAnWzApBFdwlZDg",
  "tag": "YLuHzCD4xSTDxe_0AWukyw"
}
```

### 2.2 Single Recipient JWEs

Packing a message with 1 recipient using the **Flattened JWE JSON serialization** and the **Compact JWE serialization** formats as mentioned in the [notes](#notes) above.

#### 2.2.1 NIST P-256 key
- Sender key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-256",
  "x": "46OXm1dUTO3MB-8zoxbn-9dk0khgeIqsKFO-nTJ9keM",
  "y": "8IlrwB-dl5bFd5RT4YAbgAdj5Y-a9zhc9wCMnXDZDvA",
  "d": "58GZDz9_opy-nEeaJ_cyEL63TO-l063aV5nLADCgsGY"
}
```
- Sender kid (jwk thumbprint raw base64 URL encoded): `T1jGtZoU-Xa_5a1QKexUU0Jq9WKDtS7TCowVvjoFH04`
- Single Recipient key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-256",
  "x": "r9MRjEQ7CBxAgMyEG3ZjIlkGCuRX0rTaBdbkAcY17hA",
  "y": "MRSgHQycDFPdSABGv5V0Qd-2q7ebs_x0_fNFyabGgXU",
  "d": "LK9yfSxuET5n5uZDNO-64sJKWxJs7LTkqhA4mAuKQnE"
}
```
- Single Recipient kid (jwk thumbprint raw base64 URL encoded): `dmfXisqWjRT-tFpODOD-G0CBF6zjHywNUjrrD3IFmcs`
- Finally, packing the payload outputs the following flattened serialized JWE JSON:
```json
{
  "protected": "eyJhbGciOiJFQ0RILTFQVStYQzIwUEtXIiwiYXB1IjoiVkRGcVIzUmFiMVV0V0dGZk5XRXhVVXRsZUZWVk1FcHhPVmRMUkhSVE4xUkRiM2RXZG1wdlJrZ3dOQSIsImFwdiI6IlpHMW1XR2x6Y1ZkcVVsUXRkRVp3VDBSUFJDMUhNRU5DUmpaNmFraDVkMDVWYW5KeVJETkpSbTFqY3ciLCJjdHkiOiJhcHBsaWNhdGlvbi9kaWRjb21tLXBsYWluK2pzb24iLCJlbmMiOiJYQzIwUCIsImVwayI6eyJjcnYiOiJQLTI1NiIsImt0eSI6IkVDIiwieCI6Ik5ZM3Zra04wYTFPRTBuZk1UaDR4U25IU1A2c0VianYycWp5T3J6Rm9TNnMiLCJ5IjoibUhOdnZYUmVmV0lHcU4zTC1ZWnctdElMTXZlUURWcEEzSk55V20tR21HUSJ9LCJraWQiOiJkbWZYaXNxV2pSVC10RnBPRE9ELUcwQ0JGNnpqSHl3TlVqcnJEM0lGbWNzIiwic2tpZCI6IlQxakd0Wm9VLVhhXzVhMVFLZXhVVTBKcTlXS0R0UzdUQ293VnZqb0ZIMDQiLCJ0eXAiOiJhcHBsaWNhdGlvbi9kaWRjb21tLWVuY3J5cHRlZCtqc29uIn0",
  "encrypted_key": "dXV4byLXvAHCGKSNqOT87cOwTmdlhn9665LvwXre0BJqSectrLZVQZ4udqKCccgdZAGwmIct5T-uwGYz_tLkOUQBbTXBxHDt",
  "iv": "ULEzDlTLgPXfS3a-SfspZmD02o53DfTB",
  "ciphertext": "8Z4TLHADLiuHmQEFMrU",
  "tag": "oJgQoovq__wSPgzco1udpA"
}
```
- The compact serialization of this envelope is:
  `eyJhbGciOiJFQ0RILTFQVStYQzIwUEtXIiwiYXB1IjoiVkRGcVIzUmFiMVV0V0dGZk5XRXhVVXRsZUZWVk1FcHhPVmRMUkhSVE4xUkRiM2RXZG1wdlJrZ3dOQSIsImFwdiI6IlpHMW1XR2x6Y1ZkcVVsUXRkRVp3VDBSUFJDMUhNRU5DUmpaNmFraDVkMDVWYW5KeVJETkpSbTFqY3ciLCJjdHkiOiJhcHBsaWNhdGlvbi9kaWRjb21tLXBsYWluK2pzb24iLCJlbmMiOiJYQzIwUCIsImVwayI6eyJrdHkiOiJFQyIsImNydiI6IlAtMjU2IiwieCI6Ik5ZM3Zra04wYTFPRTBuZk1UaDR4U25IU1A2c0VianYycWp5T3J6Rm9TNnMiLCJ5IjoibUhOdnZYUmVmV0lHcU4zTC1ZWnctdElMTXZlUURWcEEzSk55V20tR21HUSJ9LCJraWQiOiJkbWZYaXNxV2pSVC10RnBPRE9ELUcwQ0JGNnpqSHl3TlVqcnJEM0lGbWNzIiwic2tpZCI6IlQxakd0Wm9VLVhhXzVhMVFLZXhVVTBKcTlXS0R0UzdUQ293VnZqb0ZIMDQiLCJ0eXAiOiJhcHBsaWNhdGlvbi9kaWRjb21tLWVuY3J5cHRlZCtqc29uIn0.dXV4byLXvAHCGKSNqOT87cOwTmdlhn9665LvwXre0BJqSectrLZVQZ4udqKCccgdZAGwmIct5T-uwGYz_tLkOUQBbTXBxHDt.ULEzDlTLgPXfS3a-SfspZmD02o53DfTB.8Z4TLHADLiuHmQEFMrU.oJgQoovq__wSPgzco1udpA`
- The single recipient's headers are merged into the `protected` header, which base64 URL decoded equals to (pretty printed for readability):
```json
{
  "alg": "ECDH-1PU+XC20PKW",
  "apu": "VDFqR3Rab1UtWGFfNWExUUtleFVVMEpxOVdLRHRTN1RDb3dWdmpvRkgwNA",
  "apv": "ZG1mWGlzcVdqUlQtdEZwT0RPRC1HMENCRjZ6akh5d05VanJyRDNJRm1jcw",
  "cty": "application/didcomm-plain+json",
  "enc": "XC20P",
  "epk": {
    "kty": "EC",
    "crv": "P-256",
    "x": "NY3vkkN0a1OE0nfMTh4xSnHSP6sEbjv2qjyOrzFoS6s",
    "y": "mHNvvXRefWIGqN3L-YZw-tILMveQDVpA3JNyWm-GmGQ"
  },
  "kid": "dmfXisqWjRT-tFpODOD-G0CBF6zjHywNUjrrD3IFmcs",
  "skid": "T1jGtZoU-Xa_5a1QKexUU0Jq9WKDtS7TCowVvjoFH04",
  "typ": "application/didcomm-encrypted+json"
}
```

#### 2.2.2 NIST P-384 key
- Sender key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-384",
  "x": "bfuATmVQ_jxLIgfuhKNYrNRNu-VnK4FzTCCVRvycgekS8fIuC4rZS9uQi6Q2Ujwd",
  "y": "XkVJ93cLKpeZeCMEOsHRKk4rse1zXpzY6yUibEtwZG9nFWF05Ro8OQs5fZVK2TWC",
  "d": "OVzGxGyyaHGJpx1MoSwPjmWPas28sfq1tj7UkYFoK3ENsujmzUduAW6HwyaBlXRW"
}
```
- Sender kid (jwk thumbprint raw base64 URL encoded): `xXdnS3M4Bb497A0ko9c6H0D4NNbj1XpwGr4Tk9Fcw7k`
- Single Recipient key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-384",
  "x": "xhk5K7x4xw9OJpkFhmsY39jceQqx57psvcZstiNZmKbXD7kT9ajfGKFA6YA-ali5",
  "y": "7Hj32-JDMNDYWRGy3f-0E9lbUGp6yURMaZ9M36Q_FPgljKgHa9i0Fn1ogr_zEmO3",
  "d": "Pc3r6eg15XZeKgTDMPcGjf_SvImZxG4bDzgCh3QShClAwMdmoNbzPZGhBByNrlvO"
}
```
- Single Recipient kid (jwk thumbprint raw base64 URL encoded): `aIlhDTWJmT-_Atad5EBbvbZPkPnz2IYT85I6T44kcE4`
- Finally, packing the payload outputs the following flattened serialized JWE JSON:
```json
{
  "protected": "eyJhbGciOiJFQ0RILTFQVStYQzIwUEtXIiwiYXB1IjoiZUZoa2JsTXpUVFJDWWpRNU4wRXdhMjg1WXpaSU1FUTBUazVpYWpGWWNIZEhjalJVYXpsR1kzYzNhdyIsImFwdiI6IllVbHNhRVJVVjBwdFZDMWZRWFJoWkRWRlFtSjJZbHBRYTFCdWVqSkpXVlE0TlVrMlZEUTBhMk5GTkEiLCJjdHkiOiJhcHBsaWNhdGlvbi9kaWRjb21tLXBsYWluK2pzb24iLCJlbmMiOiJYQzIwUCIsImVwayI6eyJjcnYiOiJQLTM4NCIsImt0eSI6IkVDIiwieCI6Inp1TjJhYTZBdmRHVVdjaHNyMTdBMENvOWFmcnlnRll6TjRxZlM0dnlNS05BTF83dVVhR1d2ZVBMNkpoc25MMnYiLCJ5IjoiZTJva1U5VWUzbE9CUWxEZnFVczE5NjFQU2tMTkg1d3U1V2NRd2ZuYzdEdmhsU2tXSU9iQWpoekhoVUVZUjRBZSJ9LCJraWQiOiJhSWxoRFRXSm1ULV9BdGFkNUVCYnZiWlBrUG56MklZVDg1STZUNDRrY0U0Iiwic2tpZCI6InhYZG5TM000QmI0OTdBMGtvOWM2SDBENE5OYmoxWHB3R3I0VGs5RmN3N2siLCJ0eXAiOiJhcHBsaWNhdGlvbi9kaWRjb21tLWVuY3J5cHRlZCtqc29uIn0",
  "encrypted_key": "9bCR6CdqKSRLCFf_vShRhub1pNwoPRypHEqEMfamxy4ZcSp7y8SULzTs2rMmnBt8iJn1PiaBEYbsjsOgzgYamXQ-3OQeIg5z",
  "iv": "ryiQAsZiEVcDqJb1jQpG9nQ0p50cXJSM",
  "ciphertext": "xQiyTPTrLUFvTeVn9CI",
  "tag": "b65D-L5AybH327bWsEIRUg"
}
```
- The compact serialization of this envelope is:
  `eyJhbGciOiJFQ0RILTFQVStYQzIwUEtXIiwiYXB1IjoiZUZoa2JsTXpUVFJDWWpRNU4wRXdhMjg1WXpaSU1FUTBUazVpYWpGWWNIZEhjalJVYXpsR1kzYzNhdyIsImFwdiI6IllVbHNhRVJVVjBwdFZDMWZRWFJoWkRWRlFtSjJZbHBRYTFCdWVqSkpXVlE0TlVrMlZEUTBhMk5GTkEiLCJjdHkiOiJhcHBsaWNhdGlvbi9kaWRjb21tLXBsYWluK2pzb24iLCJlbmMiOiJYQzIwUCIsImVwayI6eyJrdHkiOiJFQyIsImNydiI6IlAtMzg0IiwieCI6Inp1TjJhYTZBdmRHVVdjaHNyMTdBMENvOWFmcnlnRll6TjRxZlM0dnlNS05BTF83dVVhR1d2ZVBMNkpoc25MMnYiLCJ5IjoiZTJva1U5VWUzbE9CUWxEZnFVczE5NjFQU2tMTkg1d3U1V2NRd2ZuYzdEdmhsU2tXSU9iQWpoekhoVUVZUjRBZSJ9LCJraWQiOiJhSWxoRFRXSm1ULV9BdGFkNUVCYnZiWlBrUG56MklZVDg1STZUNDRrY0U0Iiwic2tpZCI6InhYZG5TM000QmI0OTdBMGtvOWM2SDBENE5OYmoxWHB3R3I0VGs5RmN3N2siLCJ0eXAiOiJhcHBsaWNhdGlvbi9kaWRjb21tLWVuY3J5cHRlZCtqc29uIn0.9bCR6CdqKSRLCFf_vShRhub1pNwoPRypHEqEMfamxy4ZcSp7y8SULzTs2rMmnBt8iJn1PiaBEYbsjsOgzgYamXQ-3OQeIg5z.ryiQAsZiEVcDqJb1jQpG9nQ0p50cXJSM.xQiyTPTrLUFvTeVn9CI.b65D-L5AybH327bWsEIRUg`
- The single recipient's headers are merged into the `protected` header, which base64 URL decoded equals to (pretty printed for readability):
```json
{
  "alg": "ECDH-1PU+XC20PKW",
  "apu": "eFhkblMzTTRCYjQ5N0Ewa285YzZIMEQ0Tk5iajFYcHdHcjRUazlGY3c3aw",
  "apv": "YUlsaERUV0ptVC1fQXRhZDVFQmJ2YlpQa1BuejJJWVQ4NUk2VDQ0a2NFNA",
  "cty": "application/didcomm-plain+json",
  "enc": "XC20P",
  "epk": {
    "kty": "EC",
    "crv": "P-384",
    "x": "zuN2aa6AvdGUWchsr17A0Co9afrygFYzN4qfS4vyMKNAL_7uUaGWvePL6JhsnL2v",
    "y": "e2okU9Ue3lOBQlDfqUs1961PSkLNH5wu5WcQwfnc7DvhlSkWIObAjhzHhUEYR4Ae"
  },
  "kid": "aIlhDTWJmT-_Atad5EBbvbZPkPnz2IYT85I6T44kcE4",
  "skid": "xXdnS3M4Bb497A0ko9c6H0D4NNbj1XpwGr4Tk9Fcw7k",
  "typ": "application/didcomm-encrypted+json"
}
```

#### 2.2.3 NIST P-521 key
- Sender key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-521",
  "x": "ACN9T83BbPNn1eRyo-TrL0GyC7kBNQvgUxk55fCeQKDSTVhbzCKia7WecCUshyEF-BOQbfEsOIUCq3g7xY3VEeth",
  "y": "APDIfDv6abLQ-Zb_p8PxwJe1x3U0-PdgXLNbtS7evGuUROHt79SVkpfXcZ3UaEc6cMoFfd2oMvbmUjCMM4-Sgipn",
  "d": "AXCGyR9uXY8vDr7D4HvMxep-d5biQzgHR6WsdOF4R5M9qYb8FhRIQCMbmDSZzCuqgGgXrPRMPm5-omvWVeYqwwa3"
}
```
- Sender kid (jwk thumbprint raw base64 URL encoded): `bq3OI5517dSIMeD9K3lTqvkvvkmsRtifD6tvjlrKYsU`
- Single Recipient key JWK format:
```json
{
  "kty": "EC",
  "crv": "P-521",
  "x": "AZi-AxJkB09qw8dBnNrz53xM-wER0Y5IYXSEWSTtzI5Sdv_5XijQn9z-vGz1pMdww-C75GdpAzp2ghejZJSxbAd6",
  "y": "AZzRvW8NBytGNbF3dyNOMHB0DHCOzGp8oYBv_ZCyJbQUUnq-TYX7j8-PlKe9Ce5acxZzrcUKVtJ4I8JgI5x9oXIW",
  "d": "AHGOZNkAcQCdDZOpQRdbH-f89mpjY_kGmtEpTExd51CcRlHhXuuAr6jcgb8YStwy9FN7vCU1y5LnJfKhGUGrP2a4"
}
```
- Single Recipient kid (jwk thumbprint raw base64 URL encoded): `7icoqReWFlpF16dzZD3rBgK1cJ265WzfF9sJJXqOe0M`
- Finally, packing the payload outputs the following flattened serialized JWE JSON:
```json
{
  "protected": "eyJhbGciOiJFQ0RILTFQVStYQzIwUEtXIiwiYXB1IjoiWW5FelQwazFOVEUzWkZOSlRXVkVPVXN6YkZSeGRtdDJkbXR0YzFKMGFXWkVOblIyYW14eVMxbHpWUSIsImFwdiI6Ik4ybGpiM0ZTWlZkR2JIQkdNVFprZWxwRU0zSkNaMHN4WTBveU5qVlhlbVpHT1hOS1NsaHhUMlV3VFEiLCJjdHkiOiJhcHBsaWNhdGlvbi9kaWRjb21tLXBsYWluK2pzb24iLCJlbmMiOiJYQzIwUCIsImVwayI6eyJjcnYiOiJQLTUyMSIsImt0eSI6IkVDIiwieCI6IkFJemJtMzBZRGVIV21sXy1zeHE2c2NHbEdDS3ZuRmttR2pkc1hKOXN6bm5JQzFMSndvc1hqYmRRd29EX2NjbmtkcUtpaU4tNVVFZGtPTEZldDdXbG83bC0iLCJ5IjoiQVdDendGVjJtUFdYMnpaZzN0SHRpVE11SlhGaEtucWhUT0hPWXBzRF9uRlhGRFhrTlRyd0QyblpVNi1hU2g5Q0NLajF2N0x5VlJ0UE0ybzM5bkt3WEhXWiJ9LCJraWQiOiI3aWNvcVJlV0ZscEYxNmR6WkQzckJnSzFjSjI2NVd6ZkY5c0pKWHFPZTBNIiwic2tpZCI6ImJxM09JNTUxN2RTSU1lRDlLM2xUcXZrdnZrbXNSdGlmRDZ0dmpscktZc1UiLCJ0eXAiOiJhcHBsaWNhdGlvbi9kaWRjb21tLWVuY3J5cHRlZCtqc29uIn0",
  "encrypted_key": "-cL11h9eF6CRycMYxvJ6Ksmlf-97Vg2s_ziVnFF5RueiGrvKFmgQp09GIyxrMdTG2so6IRmifOlpwF0YPuzyThhmxToTyfpr",
  "iv": "Q0sk9bMraCAJhZyFi3sOAYMoTac4ZuGj",
  "ciphertext": "O6OlFqFMz587083_OMU",
  "tag": "TyXZ30wpVZ6nmj16evdBnA"
}
```
- The compact serialization of this envelope is:
  `eyJhbGciOiJFQ0RILTFQVStYQzIwUEtXIiwiYXB1IjoiWW5FelQwazFOVEUzWkZOSlRXVkVPVXN6YkZSeGRtdDJkbXR0YzFKMGFXWkVOblIyYW14eVMxbHpWUSIsImFwdiI6Ik4ybGpiM0ZTWlZkR2JIQkdNVFprZWxwRU0zSkNaMHN4WTBveU5qVlhlbVpHT1hOS1NsaHhUMlV3VFEiLCJjdHkiOiJhcHBsaWNhdGlvbi9kaWRjb21tLXBsYWluK2pzb24iLCJlbmMiOiJYQzIwUCIsImVwayI6eyJrdHkiOiJFQyIsImNydiI6IlAtNTIxIiwieCI6IkFJemJtMzBZRGVIV21sXy1zeHE2c2NHbEdDS3ZuRmttR2pkc1hKOXN6bm5JQzFMSndvc1hqYmRRd29EX2NjbmtkcUtpaU4tNVVFZGtPTEZldDdXbG83bC0iLCJ5IjoiQVdDendGVjJtUFdYMnpaZzN0SHRpVE11SlhGaEtucWhUT0hPWXBzRF9uRlhGRFhrTlRyd0QyblpVNi1hU2g5Q0NLajF2N0x5VlJ0UE0ybzM5bkt3WEhXWiJ9LCJraWQiOiI3aWNvcVJlV0ZscEYxNmR6WkQzckJnSzFjSjI2NVd6ZkY5c0pKWHFPZTBNIiwic2tpZCI6ImJxM09JNTUxN2RTSU1lRDlLM2xUcXZrdnZrbXNSdGlmRDZ0dmpscktZc1UiLCJ0eXAiOiJhcHBsaWNhdGlvbi9kaWRjb21tLWVuY3J5cHRlZCtqc29uIn0.-cL11h9eF6CRycMYxvJ6Ksmlf-97Vg2s_ziVnFF5RueiGrvKFmgQp09GIyxrMdTG2so6IRmifOlpwF0YPuzyThhmxToTyfpr.Q0sk9bMraCAJhZyFi3sOAYMoTac4ZuGj.O6OlFqFMz587083_OMU.TyXZ30wpVZ6nmj16evdBnA`
- The single recipient's headers are merged into the `protected` header, which base64 URL decoded equals to (pretty printed for readability):
```json
{
  "alg": "ECDH-1PU+XC20PKW",
  "apu": "YnEzT0k1NTE3ZFNJTWVEOUszbFRxdmt2dmttc1J0aWZENnR2amxyS1lzVQ",
  "apv": "N2ljb3FSZVdGbHBGMTZkelpEM3JCZ0sxY0oyNjVXemZGOXNKSlhxT2UwTQ",
  "cty": "application/didcomm-plain+json",
  "enc": "XC20P",
  "epk": {
    "kty": "EC",
    "crv": "P-521",
    "x": "AIzbm30YDeHWml_-sxq6scGlGCKvnFkmGjdsXJ9sznnIC1LJwosXjbdQwoD_ccnkdqKiiN-5UEdkOLFet7Wlo7l-",
    "y": "AWCzwFV2mPWX2zZg3tHtiTMuJXFhKnqhTOHOYpsD_nFXFDXkNTrwD2nZU6-aSh9CCKj1v7LyVRtPM2o39nKwXHWZ"
  },
  "kid": "7icoqReWFlpF16dzZD3rBgK1cJ265WzfF9sJJXqOe0M",
  "skid": "bq3OI5517dSIMeD9K3lTqvkvvkmsRtifD6tvjlrKYsU",
  "typ": "application/didcomm-encrypted+json"
}
```

#### 2.2.4 X25519 key
- Sender key JWK format:
```json
{
  "kty": "OKP",
  "crv": "X25519",
  "x": "g3Lpdd_DRgjK28qi0sR0-hI-zv7a1X52vpzKc6ZM1Qs",
  "d": "cPU_Io7RRHNb_xkQ_D6u3ER4vSjvsILDCKwOj8kVHXQ"
}
```
- Sender kid (jwk thumbprint raw base64 URL encoded): `j8E-tcw1Z_eOCoKEH-7a9T532r8zXfcavbPZlofN0Ek`
- Single Recipient key JWK format:
```json
{
  "kty": "OKP",
  "crv": "X25519",
  "x": "VlhpUXj-oGs9ge-VLrmYF7Xuzy73YchIfckaYcQefBw",
  "d": "QFHCCy0wzgJ_AlGMnjetTd0tnDaZ_7yqJODSV0d-kkg"
}
```
- Single Recipient kid (jwk thumbprint raw base64 URL encoded): `_DHSbVaMeZxriDJn5VoHXYXo6BJacwZx_fGIBfCiJ5c`
- Finally, packing the payload outputs the following flattened serialized JWE JSON:
```json
{
  "protected": "eyJhbGciOiJFQ0RILTFQVStYQzIwUEtXIiwiYXB1IjoiYWpoRkxYUmpkekZhWDJWUFEyOUxSVWd0TjJFNVZEVXpNbkk0ZWxobVkyRjJZbEJhYkc5bVRqQkZhdyIsImFwdiI6IlgwUklVMkpXWVUxbFduaHlhVVJLYmpWV2IwaFlXVmh2TmtKS1lXTjNXbmhmWmtkSlFtWkRhVW8xWXciLCJjdHkiOiJhcHBsaWNhdGlvbi9kaWRjb21tLXBsYWluK2pzb24iLCJlbmMiOiJYQzIwUCIsImVwayI6eyJjcnYiOiJYMjU1MTkiLCJrdHkiOiJPS1AiLCJ4IjoiWmdZTkJwcDlRZkZMZFpBT05LaUYxWGdRTkZCdW4tdkx4V25TeTF3ZDRRdyJ9LCJraWQiOiJfREhTYlZhTWVaeHJpREpuNVZvSFhZWG82QkphY3daeF9mR0lCZkNpSjVjIiwic2tpZCI6Imo4RS10Y3cxWl9lT0NvS0VILTdhOVQ1MzJyOHpYZmNhdmJQWmxvZk4wRWsiLCJ0eXAiOiJhcHBsaWNhdGlvbi9kaWRjb21tLWVuY3J5cHRlZCtqc29uIn0",
  "encrypted_key": "6AxohV0ygxzRGGxqKIMovkJf7rCyE1ymbVzxqVEVpioySTzd4Ociy8yTa4uo-wlVCFaKVxitFgD3bgtuidOw5J8r-CXjR42D",
  "iv": "AEv2DrMR4rMV8preS0zndED_u11QNnQx",
  "ciphertext": "c_RTSoNM5hFpOr3lEFU",
  "tag": "m9GKNsP05SKYS9qdTvnsfA"
}
```
- The compact serialization of this envelope is:
  `eyJhbGciOiJFQ0RILTFQVStYQzIwUEtXIiwiYXB1IjoiYWpoRkxYUmpkekZhWDJWUFEyOUxSVWd0TjJFNVZEVXpNbkk0ZWxobVkyRjJZbEJhYkc5bVRqQkZhdyIsImFwdiI6IlgwUklVMkpXWVUxbFduaHlhVVJLYmpWV2IwaFlXVmh2TmtKS1lXTjNXbmhmWmtkSlFtWkRhVW8xWXciLCJjdHkiOiJhcHBsaWNhdGlvbi9kaWRjb21tLXBsYWluK2pzb24iLCJlbmMiOiJYQzIwUCIsImVwayI6eyJrdHkiOiJPS1AiLCJjcnYiOiJYMjU1MTkiLCJ4IjoiWmdZTkJwcDlRZkZMZFpBT05LaUYxWGdRTkZCdW4tdkx4V25TeTF3ZDRRdyJ9LCJraWQiOiJfREhTYlZhTWVaeHJpREpuNVZvSFhZWG82QkphY3daeF9mR0lCZkNpSjVjIiwic2tpZCI6Imo4RS10Y3cxWl9lT0NvS0VILTdhOVQ1MzJyOHpYZmNhdmJQWmxvZk4wRWsiLCJ0eXAiOiJhcHBsaWNhdGlvbi9kaWRjb21tLWVuY3J5cHRlZCtqc29uIn0.6AxohV0ygxzRGGxqKIMovkJf7rCyE1ymbVzxqVEVpioySTzd4Ociy8yTa4uo-wlVCFaKVxitFgD3bgtuidOw5J8r-CXjR42D.AEv2DrMR4rMV8preS0zndED_u11QNnQx.c_RTSoNM5hFpOr3lEFU.m9GKNsP05SKYS9qdTvnsfA`
- The single recipient's headers are merged into the `protected` header, which base64 URL decoded equals to (pretty printed for readability):
```json
{
  "alg": "ECDH-1PU+XC20PKW",
  "apu": "ajhFLXRjdzFaX2VPQ29LRUgtN2E5VDUzMnI4elhmY2F2YlBabG9mTjBFaw",
  "apv": "X0RIU2JWYU1lWnhyaURKbjVWb0hYWVhvNkJKYWN3WnhfZkdJQmZDaUo1Yw",
  "cty": "application/didcomm-plain+json",
  "enc": "XC20P",
  "epk": {
    "kty": "OKP",
    "crv": "X25519",
    "x": "ZgYNBpp9QfFLdZAONKiF1XgQNFBun-vLxWnSy1wd4Qw"
  },
  "kid": "_DHSbVaMeZxriDJn5VoHXYXo6BJacwZx_fGIBfCiJ5c",
  "skid": "j8E-tcw1Z_eOCoKEH-7a9T532r8zXfcavbPZlofN0Ek",
  "typ": "application/didcomm-encrypted+json"
}
```
