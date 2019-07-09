# 0114: Predefined Identities
- Author: Daniel Hardman
- Start Date: 2019-07-10

## Status
- Status: [PROPOSED](/README.md#rfc-lifecycle)
- Status Date: (date of first submission or last status change)
- Status Note: (explanation of current status; if adopted, 
  links to impls or derivative ideas; if superseded, link to replacement)

## Summary

Documents some keys, DIDs, and DID Docs that may be useful for testing,
simulation, and spec writing. The fake ones are the DIDComm / identity analogs to the
reserved domain "example.com" that was allocated for testing purposes with
DNS and other internet systems -- or to Microsoft's example Contoso database and
website used to explore and document web development concepts.

## Real Identities

The following real--NOT fake--identities are worth publicly documenting.

#### Aries community

The collective Aries developer community is represented by:

```
did:sov:BzCbsNYhMrjHiqZDTUASHg -- verkey = 6zJ9dboyug451A8dtLgsjmjyguQcmq823y7vHP6vT2Eu
```

This DID is currently allocated, but not actually registered on Sovrin's mainnet.
You will see this DID in a number of RFCs, as the basis of a [PIURI](
 ../../concepts/0003-protocols/uris.md#piuri) that identifies
a community-defined protocol. You DO NOT have to actually resolve this DID or relate
to a Sovrin identity to use Aries or its RFCs; think of this more like the opaque
URNs that are sometimes used in XML namespacing. At some point it may be registered,
but nothing else in the preceding summary will change.

The community controls a second DID that is useful for defining message families
that are not canonical (e.g., in the [sample tic-tac-toe protocol](
../../concepts/0003-protocols/tictactoe/README.md)). It is:

```
did:sov:SLfEi9esrjzybysFxQZbfq -- verkey = Ep1puxjTDREwEyz91RYzn7arKL2iKQaDEB5kYDUUUwh5
``` 

This community may create DIDs for itself from other DID methods, too. If so,
we will publish them here.

#### Subgroups

The Aries community may create subgroups with their own DIDs. If so,
we may publish such information here.

#### Allied communities

Other groups such as [DIF](https://identity.foundation), the [W3C Crecentials Community Group](
https://github.com/w3c-ccg), and so forth may wish to define identities and announce
their associated DIDs here. 


### Fake Identities

The identity material shown below is not registered anywhere. This is because sometimes
our tests or demos are _about_ registering or connecting, and because the identity material
is intended to be somewhat independent of a specific blockchain instance. Instead, we define values and give them
names, permalinks, and semantics in this RFC. This lets us have a shared understanding of
how we expect them to behave in various contexts.

WARNING: Below you will see some published secrets. By disclosing private keys
and/or their seeds, we are compromising the keypairs. This fake identity material is
thus NOT trustworthy for anything; the world knows the secrets, and now you do, too.
`:-)` You can test or simulate workflows with these keys. You might use them in
debugging and development. __But you should never use them as the basis of real
trust.__

### DIDs

#### alice-sov-1

This DID, the `alice-sov-1` DID with value `did:sov:UrDaZsMUpa91DqU3vrGmoJ`, is
associated with a very simplistic Indy/Sovrin identity. It has a single keypair
([Key 1](#key-1-ed25519) below) that it uses for everything.
In demos or tests, its genesis DID Doc looks like this:

```
{
    "@context": "https://w3id.org/did/v0.11",
    "id": "did:sov:UrDaZsMUpa91DqU3vrGmoJ",
    "service": [{
        "type": "did-communication",
        "serviceEndpoint": "https://localhost:23456"
    }],
    "publicKey": [{
        "id": "key-1",
        "type": "Ed25519VerificationKey2018",
        "publicKeyBase58": "GBMBzuhw7XgSdbNffh8HpoKWEdEN6hU2Q5WqL1KQTG5Z"
    }],
    "authentication": ["#key-1"]
}
```

#### bob-many-1

This DID, the `bob-many-1` DID with value `did:sov:T9nQQ8CjAhk2oGAgAw1ToF`, is
associated with a much more flexible, complex identity than `alice-sov-1`. It
places every test keypair *except* Key 1 in the `authentication` section of its
DID Doc. This means you should be able to talk to Bob using the types of crypto
common in many communities, not just Indy/Sovrin. Its genesis DID doc
looks like this:

```
{
    "@context": "https://w3id.org/did/v0.11",
    "id": "did:sov:T9nQQ8CjAhk2oGAgAw1ToF",
    "service": [{
        "type": "did-communication",
        "serviceEndpoint": "https://localhost:23457"
    }],
    "publicKey": [{
        "id": "key-2",
        "type": "Ed25519VerificationKey2018",
        "controller": "#id",
        "publicKeyBase58": "FFhViHkJwqA15ruKmHQUoZYtc5ZkddozN3tSjETrUH9z"
      },
      {
        "id": "key-3",
        "type": "Secp256k1VerificationKey2018",
        "controller": "#id",
        "publicKeyHex": "3056301006072a8648ce3d020106052b8104000a03420004a34521c8191d625ff811c82a24a60ff9f174c8b17a7550c11bba35dbf97f3f04392e6a9c6353fd07987e016122157bf56c487865036722e4a978bb6cd8843fa8"
      },
      {
        "id": "key-4",
        "type": "RsaVerificationKey2018",
        "controller": "#id",
        "publicKeyPem": "-----BEGIN PUBLIC KEY-----\r\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDlOJu6TyygqxfWT7eLtGDwajtN\r\nFOb9I5XRb6khyfD1Yt3YiCgQWMNW649887VGJiGr/L5i2osbl8C9+WJTeucF+S76\r\nxFxdU6jE0NQ+Z+zEdhUTooNRaY5nZiu5PgDB0ED/ZKBUSLKL7eibMxZtMlUDHjm4\r\ngwQco1KRMDSmXSMkDwIDAQAB\r\n-----END PUBLIC KEY-----"
      },
      {
        "id": "key-5",
        "type": "RsaVerificationKey2018",
        "controller": "#id",
        "publicKeyPem": "-----BEGIN PUBLIC KEY-----\r\nMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAoZp7md4nkmmFvkoHhQMw\r\nN0lcpYeKfeinKir7zYWFLmpClZHawZKLkB52+nnY4w9ZlKhc4Yosrw/N0h1sZlVZ\r\nfOQBnzFUQCea6uK/4BKHPhiHpN73uOwu5TAY4BHS7fsXRLPgQFB6o6iy127o2Jfb\r\nUVpbNU/rJGxVI2K1BIzkfrXAJ0pkjkdP7OFE6yRLU4ZcATWSIPwGvlF6a0/QPC3B\r\nbTvp2+DYPDC4pKWxNF/qOwOnMWqxGq6ookn12N/GufA/Ugv3BTVoy7I7Q9SXty4u\r\nUat19OBJVIqBOMgXsyDz0x/C6lhBR2uQ1K06XRa8N4hbfcgkSs+yNBkLfBl7N80Q\r\n0Wkq2PHetzQU12dPnz64vvr6s0rpYIo20VtLzhYA8ZxseGc3s7zmY5QWYx3ek7Vu\r\nwPv9QQzcmtIQQsUbekPoLnKLt6wJhPIGEr4tPXy8bmbaThRMx4tjyEQYy6d+uD0h\r\nXTLSjZ1SccMRqLxoPtTWVNXKY1E84EcS/QkqlY4AthLFBL6r+lnm+DlNaG8LMwCm\r\ncz5NMag9ooM9IqgdDYhUpWYDSdOvDubtz1YZ4hjQhaofdC2AkPXRiQvMy/Nx9WjQ\r\nn4z387kz5PK5YbadoZYkwtFttmxJ/EQkkhGEDTXoSRTufv+qjXDsmhEsdaNkvcDP\r\n1uiCSY19UWe5LQhIMbR0u/0CAwEAAQ==\r\n-----END PUBLIC KEY-----"
      },
    ],
    "authentication": ["#key-2", "#key-3", "#key-4", "#key-5", "#key-6"]
}
```

[TODO: define DIDs from other ecosystems that put the same set of keys in
their DID docs -- maybe `bob-many-2` is a did:eth using these same keys, and
`bob-many-3` is a did:btc using them...]

### Keys
 
#### Key 1 (Ed25519)

This key is used by the [`alice-sov-1`](#alice-sov-1) DID, but could also
be used with other DIDs defined elsewhere.

```
signing key (private)
Ga3v3SyNsvv1QhSCrEAQfJiyxQYUdZzQARkCosSWrXbT

hex seed (private; in a form usable by Indy CLI)
e756c41c1b5c48d3be0f7b5c7aa576d2709f13b67c9078c7ded047fe87c8a79e

verkey (public)
GBMBzuhw7XgSdbNffh8HpoKWEdEN6hU2Q5WqL1KQTG5Z

as a Sovrin DID
did:sov:UrDaZsMUpa91DqU3vrGmoJ
```

#### Key 2 (Ed25519)

This key is used by the [`bob-many-1`](#bob-many-1) DID, but could also
be used with other DIDs defined elsewhere.

```
signing key (private)
FE2EYN25vcQmCU52MkiHuXHKqR46TwjFU4D4TGaYDRyd

hex seed (private)
d3598fea152e6a480faa676a76e545de7db9ac1093b9cee90b031d9625f3ce64

verkey (public)
FFhViHkJwqA15ruKmHQUoZYtc5ZkddozN3tSjETrUH9z

as a Sovrin DID
did:sov:T9nQQ8CjAhk2oGAgAw1ToF
```

#### Key 3 (Secp256k1)

This key is used by the [`bob-many-1`](#bob-many-1) DID, but could also
be used with other DIDs defined elsewhere.

```
-----BEGIN EC PRIVATE KEY-----
MHQCAQEEIMFcUvDujXt0/C48vm1Wfj8ADlrGsHCHzp//2mUARw79oAcGBSuBBAAK
oUQDQgAEo0UhyBkdYl/4EcgqJKYP+fF0yLF6dVDBG7o12/l/PwQ5LmqcY1P9B5h+
AWEiFXv1bEh4ZQNnIuSpeLts2IQ/qA==
-----END EC PRIVATE KEY-----

-----BEGIN PUBLIC KEY-----
MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEo0UhyBkdYl/4EcgqJKYP+fF0yLF6dVDB
G7o12/l/PwQ5LmqcY1P9B5h+AWEiFXv1bEh4ZQNnIuSpeLts2IQ/qA==
-----END PUBLIC KEY-----

public key as hex
3056301006072a8648ce3d020106052b8104000a03420004a34521c8191d625ff811c82a24a60ff9f174c8b17a7550c11bba35dbf97f3f04392e6a9c6353fd07987e016122157bf56c487865036722e4a978bb6cd8843fa8
```

#### Key 4 (1024-bit RSA)

This key is used by the [`bob-many-1`](#bob-many-1) DID, but could also
be used with other DIDs defined elsewhere.

```
-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQDlOJu6TyygqxfWT7eLtGDwajtNFOb9I5XRb6khyfD1Yt3YiCgQ
WMNW649887VGJiGr/L5i2osbl8C9+WJTeucF+S76xFxdU6jE0NQ+Z+zEdhUTooNR
aY5nZiu5PgDB0ED/ZKBUSLKL7eibMxZtMlUDHjm4gwQco1KRMDSmXSMkDwIDAQAB
AoGAfY9LpnuWK5Bs50UVep5c93SJdUi82u7yMx4iHFMc/Z2hfenfYEzu+57fI4fv
xTQ//5DbzRR/XKb8ulNv6+CHyPF31xk7YOBfkGI8qjLoq06V+FyBfDSwL8KbLyeH
m7KUZnLNQbk8yGLzB3iYKkRHlmUanQGaNMIJziWOkN+N9dECQQD0ONYRNZeuM8zd
8XJTSdcIX4a3gy3GGCJxOzv16XHxD03GW6UNLmfPwenKu+cdrQeaqEixrCejXdAF
z/7+BSMpAkEA8EaSOeP5Xr3ZrbiKzi6TGMwHMvC7HdJxaBJbVRfApFrE0/mPwmP5
rN7QwjrMY+0+AbXcm8mRQyQ1+IGEembsdwJBAN6az8Rv7QnD/YBvi52POIlRSSIM
V7SwWvSK4WSMnGb1ZBbhgdg57DXaspcwHsFV7hByQ5BvMtIduHcT14ECfcECQATe
aTgjFnqE/lQ22Rk0eGaYO80cc643BXVGafNfd9fcvwBMnk0iGX0XRsOozVt5Azil
psLBYuApa66NcVHJpCECQQDTjI2AQhFc1yRnCU/YgDnSpJVm1nASoRUnU8Jfm3Oz
uku7JUXcVpt08DFSceCEX9unCuMcT72rAQlLpdZir876
-----END RSA PRIVATE KEY-----

-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDlOJu6TyygqxfWT7eLtGDwajtN
FOb9I5XRb6khyfD1Yt3YiCgQWMNW649887VGJiGr/L5i2osbl8C9+WJTeucF+S76
xFxdU6jE0NQ+Z+zEdhUTooNRaY5nZiu5PgDB0ED/ZKBUSLKL7eibMxZtMlUDHjm4
gwQco1KRMDSmXSMkDwIDAQAB
-----END PUBLIC KEY-----
```

#### Key 5 (4096-bit RSA)

This key is used by the [`bob-many-1`](#bob-many-1) DID, but could also
be used with other DIDs defined elsewhere.

```
-----BEGIN RSA PRIVATE KEY-----
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
-----END RSA PRIVATE KEY-----

-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAoZp7md4nkmmFvkoHhQMw
N0lcpYeKfeinKir7zYWFLmpClZHawZKLkB52+nnY4w9ZlKhc4Yosrw/N0h1sZlVZ
fOQBnzFUQCea6uK/4BKHPhiHpN73uOwu5TAY4BHS7fsXRLPgQFB6o6iy127o2Jfb
UVpbNU/rJGxVI2K1BIzkfrXAJ0pkjkdP7OFE6yRLU4ZcATWSIPwGvlF6a0/QPC3B
bTvp2+DYPDC4pKWxNF/qOwOnMWqxGq6ookn12N/GufA/Ugv3BTVoy7I7Q9SXty4u
Uat19OBJVIqBOMgXsyDz0x/C6lhBR2uQ1K06XRa8N4hbfcgkSs+yNBkLfBl7N80Q
0Wkq2PHetzQU12dPnz64vvr6s0rpYIo20VtLzhYA8ZxseGc3s7zmY5QWYx3ek7Vu
wPv9QQzcmtIQQsUbekPoLnKLt6wJhPIGEr4tPXy8bmbaThRMx4tjyEQYy6d+uD0h
XTLSjZ1SccMRqLxoPtTWVNXKY1E84EcS/QkqlY4AthLFBL6r+lnm+DlNaG8LMwCm
cz5NMag9ooM9IqgdDYhUpWYDSdOvDubtz1YZ4hjQhaofdC2AkPXRiQvMy/Nx9WjQ
n4z387kz5PK5YbadoZYkwtFttmxJ/EQkkhGEDTXoSRTufv+qjXDsmhEsdaNkvcDP
1uiCSY19UWe5LQhIMbR0u/0CAwEAAQ==
-----END PUBLIC KEY-----
```

#### Key 6 (Ed25519)

This key is used by the [`bob-many-1`](#bob-many-1) DID, but could also
be used with other DIDs defined elsewhere.

```
signing key (private)
9dTU6xawVQJprz7zYGCiTJCGjHdW5EcZduzRU4z69p64

hex seed (private; in a form usable by Indy CLI)
803454c9429467530b17e8e571df5442b6620ac06ab0172d943ab9e01f6d4e31

verkey (public)
4zZJaPg26FYcLZmqm99K2dz99agHd5rkhuYGCcKntAZ4

as a Sovrin DID
did:sov:8KrDpiKkHsFyDm3ZM36Rwm
```

### Tools to generate your own identity material

* Digital Bazaar's DID tool
* uPort tool
* [Ed25519 and Indy-compatible DIDs in pure client-side javascript](
https://github.com/sovrin-foundation/launch/blob/master/sovrin-keygen.zip)
* [Hyperledger Indy CLI](https://github.com/hyperledger/indy-sdk/tree/master/cli)


