# Aries RFC 0327: Crypto service Protocol 1.0

- Authors: Robert Mitwicki, Wolfgang Lamot
- Status: [PROPOSED](/README.md#proposed)
- Since: 2019-11-20 (date you submit your PR)
- Status Note: RFC under development
- Supersedes:
- Start Date: 2019-11-01
- Tags: feature, protocol

## Summary

Within decentralized data economy with user-centric approach the user is the one who should control data flows and all interaction even on 3rd parties platforms. To achieve that we start to talk about access instead of ownership of the data. Within the space we can identify some services which are dealing with the users data but they don't necessarily need to be able to see the data. In this category we have services like archive, data vaults, data transportation (IM, Email, Sent file), etc. To be able to better support privacy in such cases this document proposes a protocol which uses underlying security mechanisms within agents like `Lox` to provide an API for cryptographic operations like asymetric encryption/decryption, signature/verification, delegation (proxy re-encryption) to let those services provide an additional security layer on their platform within connection to SSI wallet agents.

## Motivation

Identity management and key management are complex topics with which even big players have problems. To help companies and their products build secure and privacy preserving services with SSI they need a simple mechanism to get access to the cryptographic operations within components of the wallets.

### Todays 'Best Practice' approach to cryptographically secured Services

Many 3rd party services today provide solutions like secure storage, encrypted communication, secure data transportation and to achieve that they are using secure keys to provide cryptography for their use cases. The problem is that in many cases those keys are generated and/or stored within the 3rd party Services - either in the Client App or in the Backend - which requires the users explicit trust into the 3rd parties good intentions.

Even in the case that a 3rd party has the best possible intentions in keeping the users secrets save and private. There is still the increased risk for the users keys of leakage or beeing compromised while beeing stored with a (centralized) 3rd party Service.

Last but not least the users usage of multiple such cryptografically secured services would lead to the distribution of the users secrets over different systems where the user needs to keep track of them and manage them via differnt 3rd party tools.

### Vision - seperation of Service-(Business-)Logic and Identity Artefacts

In the context of SSI and decentralized identity the ideal solution is that the keys are generated within user agent and that the private (secret) key never leaves that place. This would be a clear seperation of a services business logic and the users keys which we also count to the users unique sets of identifying information (identity artefacts).

After seperating these two domains their follows the obvious need for providing a general crypto API to the user wallet which allows to support generic use cases where a cryptographic layer is required in the 3rd party service business logic, for example:

- encrypted data in data vaults
- encrypted messages within 3rd party service
- additional security layers outside of Agent ecosystem, data transportation, messaging over non-DIDComm protocols.
- backup/restore systems

The desired outcome would be to have an Agent which is able to expose a standardized Crypto Services API to external 3rd party services which then can implement cryptographically secured aplications without the need to have access to the actual user secrets.

## Tutorial

### Name and Version

This defines the `crypto-service` protocol. version 1.0, as identified by the following PIURI:

    TODO: Add PIURI when ready

### Roles

The minimum amount of roles involved in the `crypto-service` protocol are: a `sender` and a `receiver`. The `sender` requests a specific cryptographic operation from the `receiver` and the `receiver` provides the result in a form of a payload or an error.
The protocol could include more roles (e.g. a `proxy`) which could be involved in processes like delegation (proxy re-encryption), etc.

### Constraints

Each message which is send to the agent requires an up front established relationship between sender and receiver in the form of an authorization. This means that the sender is allowed to use only the specific key which is meant for him. There should not be the case that the sender is able to trigger any operation with keys which where never used within his service.

## Reference

### Examples

Specific use case example:

A platform providing secure document transportation between parties and archiving functionality.

Actors:

- `Sender`: user sending document
- `Receiver`: user receiving document
- `DocuArch`: platform providing secure document transportation and archiving
- `DocuArchApp`: client side application allowing to up-/download and display documents

Here is how it could work:

- `Receiver` register to the services with his DID identity (via `DocuArchApp`)
- `Receiver` share his DID with the `Sender`
- `Sender` knowing DID of the `Receiver` encrypts the document with `Receiver` public key and sends document on the platform
- `DocuArch` securely transports that document to the `Receiver` at the same time archiving it for the `Sender` and `Receiver`
- `Receiver` is informed by the `DocuArchApp` that there is a new document to view.
- `Receiver` securely logs into `DocuArchApp` with his DID identity
- `Receiver` opens encrypted payload within `DocuArchApp`
- `DocuArchApp` sends request to the user Agent to decrypt the message for the `Receiver`
- Agent decrypts the message and sends back the decrypted payload
- `DocuArchApp` displays the decrypted payload within local app

In this scenario `DocuArch` has no way to learn about what is in the payload which is sent between `Sender` and `Receiver` as only the person who is in possession of the private key is able to decrypt the payload - which is the `Receiver`.
Therfore the decrypted payload is only available on the `Receivers` client side app which is in communication with the Agent on behalf of the users DID identity.

Such features within the Agent allow companies to build faster and more secure systems as the identity management and key management part comes from Agents and they just interact with it via API.

### Messages

Protocol: did:sov:1234;spec/crypto-service/1.0

**encrypt**

- payload - raw data which should be encrypted
- key_id - reference to the specific did key which was used to establish connection with the service.

```
    {
        "@id": "1234567889",
        "@type": "did:sov:1234;spec/crypto-service/1.0/encrypt",
        "payload": "Text to be encrypted",
        "key_id": "did:example:123456789abcdefghi#keys-1"

    }
```

**decrypt**

- encryptedPayload - encrypted payload to be decrypt
- key_id - reference to the specific did key which was used to establish connection with the service.

```
    {
        "@id": "1234567889",
        "@type": "did:sov:1234;spec/crypto-service/1.0/decrypt",
        "encryptedPayload": "ASDD@J(!@DJ!DASD!@F",
        "key_id": "did:example:123456789abcdefghi#keys-1"

    }
```

**sign**

- payload - payload to be signed
- key_id - reference to the specific did key which was used to establish connection with the service.

```
    {
        "@id": "1234567889",
        "@type": "did:sov:1234;spec/crypto-service/1.0/sign",
        "payload": "I say so!",
        "key_id": "did:example:123456789abcdefghi#keys-1"

    }
```

**verify**

- signature - signature to be verified
- key_id - reference to the specific did key which was used to establish connection with the service.

```
    {
        "@id": "1234567889",
        "@type": "did:sov:1234;spec/crypto-service/1.0/verify",
        "signature": "12312d8u182d812d9182d91827d179",
        "key_id": "did:example:123456789abcdefghi#keys-1"

    }
```

**delegate**

- delegate - DID of the delegate identity for which the proxy re-encryption token shall be generated
- key_id - reference to the specific did key which was used to establish connection with the service.

```
    {
        "@id": "1234567889",
        "@type": "did:sov:1234;spec/crypto-service/1.0/delegate",
        "delegate": "did:example:ihgfedcba987654321",
        "key_id": "did:example:123456789abcdefghi#keys-1"

    }
```

### Message Catalog

TODO: add error codes and response messages/statuses

### Responses

TODO

## Drawbacks

- Potentialy expose Agent for different types of attacts: e.g. someone would try to decrypt your private documents without you being notice of that.
-

## Rationale and alternatives

We can not expect that each services will switch directly to the DIDComm and other features of the agents. Not all features are even desier to have within agent. But if the Agent can exposer base API for identity management and crypto operations this would allow others to build on top of it much more richer ans secure applications and platforms.

We are not aware of any alternatives atm. Anyone?

## Prior art

Similar approach is taken within HSM world where API is expose to the outside world without exposing keys. Here we take same approach in the context of KMS within Agent.

## Unresolved questions

- How to check authorization that a given service is allowed to use a specific set of the keys?
- How to protect user against malicious requests?
- What other operations should be supported?
- What are the limitations in the context of payload?

## Implementations

_Implementation Notes_

| Name / Link | Implementation Notes |
| ----------- | -------------------- |
|             |
