# Aries RFC 0721: Revocation Notification 2.0
- Authors: Keith Smith, Daniel Bluhm, James Ebert
- Status: [PROPOSED](/README.md#proposed)
- Since: 2022-02-15
- Status Note: Updates the credential identifiers format after discussions while implementing [RFC 0183 Revocation Notification](../0183-revocation-notification/README.md)
- Supersedes: [RFC 0183 Revocation Notification](../0183-revocation-notification/README.md)
- Start Date: 2021-11-01
- Tags: [feature](/tags.md#feature), [protocol](/tags.md#protocol)

## Summary

This RFC defines the message format which an issuer uses to notify a holder that a previously issued credential has been revoked.

## Change Log

- 20240320: Clarification removing references to retired `~please_ack` decorator and RFC.

## Motivation

We need a standard protocol for an issuer to notify a holder that a previously issued credential has been revoked.

For example, suppose a passport agency revokes Alice's passport.
The passport agency (an issuer) may want to notify Alice (a holder) that her passport has been revoked so that she
knows that she will be unable to use her passport to travel.

## Tutorial

The Revocation Notification protocol is a very simple protocol consisting of a single message:

* Revoke - issuer to holder

This simple protocol allows an issuer to choose to notify a holder that a previously issued credential has been revoked.

It is the issuer's prerogative whether or not to notify the holder that a credential has been revoked.  It is not a security risk if the issuer does not notify the holder that the credential has been revoked, nor if the message is lost.  The holder will still be unable to use a revoked credential without this notification.

### Roles

There are two parties involved in a Revocation Notification: `issuer` and `holder`.
The `issuer` sends the `revoke` message to the `holder`.

### Messages

The `revoke` message sent by the `issuer` to the `holder`. The holder should verify that the `revoke` message came from the connection that was originally used to issue the credential.

Message format:

```JSON
{
  "@type": "https://didcomm.org/revocation_notification/2.0/revoke",
  "@id": "<uuid-revocation-notification>",
  "revocation_format": "<revocation_format>",
  "credential_id": "<credential_id>",
  "comment": "Some comment"
}
```

Description of fields:

* `revocation_format` (required) -- the format of the credential revocation. Accepted values for the revocation format are provided in the "Revocation Credential Identification Formats" section immediately below.

* `credential_id` (required) -- the individual credential identifier of a credential issued using the [issue-credential-v2](https://github.com/hyperledger/aries-rfcs/tree/main/features/0453-issue-credential-v2) protocol that has been revoked by the issuer. Accepted values for the credential id format are provided in the "Revocation Credential Identification Formats" section immediately below.

* `comment` (optional) -- a field that provides some human readable information about the revocation notification.  This is typically the reason for the revocation as deemed appropriate by the issuer.

#### Revocation Credential Identification Formats

In order to support multiple credential revocation formats, the following dictates the format of revocation formats and their credential ids. As additional credential revocation formats are determined their credential id formats should be added.

Revocation Format | Credential Identifier Format | Example |
--- | --- | --- |
`indy-anoncreds`  | `<revocation-registry-id>::<credential-revocation-id>` | `AsB27X6KRrJFsqZ3unNAH6:4:AsB27X6KRrJFsqZ3unNAH6:3:cl:48187:default:CL_ACCUM:3b24a9b0-a979-41e0-9964-2292f2b1b7e9::1` |
`anoncreds`  | `<revocation-registry-id>::<credential-revocation-id>` | `did:indy:sovrin:5nDyJVP1NrcPAttP3xwMB9/anoncreds/v0/REV_REG_DEF/56495/npdb/TAG1::1` |

## Reference

* See the [issue-credential-v2](https://github.com/hyperledger/aries-rfcs/tree/main/features/0453-issue-credential-v2) protocol.
* See the [Please ACK Decorator RFC](https://github.com/hyperledger/aries-rfcs/tree/main/features/0317-please-ack).

## Drawbacks

If we later added support for more general event subscription and notification message flows, this would be redundant.

## Rationale and alternatives

- Why is this design the best in the space of possible designs?  It is simple.
- What other designs have been considered and what is the rationale for not
choosing them?  A more general event subscription and notification mechanism was considered but chose to keep this simple for the same reasons that the basic message was kept simple.
- What is the impact of not doing this?  There is no standard way of sending a revocation notification which is a common scenario.

## Prior art

## Unresolved questions

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

Name / Link | Implementation Notes
--- | ---
 |  | 

