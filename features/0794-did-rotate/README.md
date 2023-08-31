# Aries RFC 0794: DID Rotate 1.0

- Authors: [Sam Curren](telegramsam@gmail.com)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2023-08-29 
- Status Note: 
- Start Date: 2023-08-18 
- Tags: [feature](/tags.md#feature), [protocol](/tags.md#protocol)
- URI: https://didcomm.org/did-rotate/1.0

## Summary

This protocol signals the change of DID in use between parties.

This protocol is only applicable to DIDComm v1 - in DIDComm v2 use the more efficient DID Rotation header.

## Motivation

This mechanism allows a party in a relationship to change the DID in use for the relationship. This may be used to switch DID methods,
but also to switch to a new DID within the same DID method. Inspired by (but different from) the DID rotation feature of the DIDComm Messaging (DIDComm v2) spec.

## Implications for Software Implementations

This protocol enables the identifiers used in a relationship to change. Implementations will need to consider how data related to the relationship is managed. If the relationship DIDs are used as identifiers, those identifiers may need to be updated during the rotation to maintain data integrity.

## Tutorial

### Name and Version

DID Rotate 1.0

URI: https://didcomm.org/did-rotate/1.0/<messageType>

### Roles

**rotating_party**: this party is rotating the DID in use for this relationship. They send the `rotate` message.

**observing_party**: this party is notified of the DID rotation

### Messages

#### Rotate 

Message Type URI: https://didcomm.org/did-rotate/1.0/rotate

`to_did`: The new DID to be used to identify the **rotating_party**

```json
{
    "@id": "123456780",
    "@type": "https://didcomm.org/did-rotate/1.0/rotate",
    "to_did": "did:example:newdid",

}
```

The **rotating_party** is expected to receive messages on both the existing and new DIDs and their associated keys for a reasonable period that MUST extend at least until the following `ack` message has been received.

This message MUST be sent using authcrypt or as a signed message in order to establish the provenance of the new DID. Proper provenance prevents injection attacks that seek to take over a relationship. Any rotate message received without being authcrypted or signed MUST be discarded and not processed.

DIDComm v1 uses public keys as the outer message identifiers. This means that rotation to a new DID using the same public key will not result in a change for new inbound messages. The **observing_party** must not assume that the new DID uses the same keys as the existing relationship.

#### Ack

Message Type URI: https://didcomm.org/did-rotate/1.0/ack

This message is still sent to the prior DID to acknowledge the receipt of the rotation. Following messages will be sent to the new DID.

In order to correctly process out of order messages, the The **observing_party** may choose to receive messages from the old did for a reasonable period. This allows messages sent before rotation but received after rotation in the case of out of order message delivery.

In this message, the `thid` (Thread ID) MUST be included to allow the `rotating_party` to correlate it with the sent `rotate` message.

```json
{
    "@id": "123456780",
    "@type": "https://didcomm.org/did-rotate/1.0/ack",
      "~thread"          : {
		"thid": "<id of rotate message>"
	},

}
```

#### Problem Report

If the **observing_party** receives a `rotate` message with a DID that they cannot resolve, they MUST return a problem-report message.

The `description` `code` must be set to one of the following:
- **e.did.unresolvable** - used for a DID who's method is supported, but will not resolve
- **e.did.method_unsupported** - used for a DID method for which the `observing_party` does not support resolution.

Upon receiving this message, the `rotating_party` must not complete the rotation and resolve the issue. Further rotation attempts must happen in a new thread.

```json
{
  "@type"            : "https://didcomm.org/did-rotate/1.0/problem-report",
  "@id"              : "an identifier that can be used to discuss this error message",
  "~thread"          : {
		"pthid": "<id of rotate message>"
	},
  "description"      : { "en": "DID Unresolvable", "code": "e.did.unresolvable" },
  "problem_items"    : [ {"did": "<did_passed_in_rotate>"} ],
}
```

#### Hangup

Message Type URI: https://didcomm.org/did-rotate/1.0/hangup

This message is sent by the **rotating_party** to inform the **observing_party** that they are done with the relationship and will no longer be responding.

There is no response message.

Use of this message does not require or indicate that all data has been deleted by either party, just that interaction has ceased.

```json
{
    "@id": "123456780",
    "@type": "https://didcomm.org/did-rotate/1.0/hangup"
}
```

## Prior art

This protocol is inspired buy the rotation feature of DIDComm Messaging (DIDComm v2). The implementation differs in important ways.
The DIDComm v2 method is a _post rotate_ operation: the first message sent AFTER the rotation contains the prior DID and a signature authorizing the rotation. This is efficient, but requires the use of a message header and a higher level of integration with message processing.
This protocol is a _pre rotate_ operation: notifying the other party of the new DID in advance is a less efficient but simpler approach. This was done to minimize adoption pain. The pending move to DIDComm v2 will provide the efficiency.

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

*Implementation Notes* [may need to include a link to test results](/README.md#accepted).

Name / Link | Implementation Notes
--- | ---
 |
