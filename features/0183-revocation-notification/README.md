# Aries RFC 0183: Revocation Notification 1.0
- Authors: [Keith Smith]
- Status: [PROPOSED](/README.md#proposed)
- Since: 2019-08-12
- Status Note: Initial proposal after discussion on rocketchat
- Supersedes:
- Start Date: 2018-08-12
- Tags: [feature](/tags.md#feature), [protocol](/tags.md#protocol)

## Summary

This RFC defines the message format which an issuer uses to notify a holder that a previously issued credential has been revoked.

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

The `revoke` message sent by the `issuer` to the `holder` is as follows:

```JSON
{
  "@type": "https://didcomm.org/revocation_notification/1.0/revoke",
  "@id": "<uuid-revocation-notification>",
  "~please_ack": ["RECEIPT","OUTCOME"],
  "thread_id": "<thread_id>",
  "comment": "Some comment"
}
```

Description of fields:

* `~please_ack` (optional) -- as described by the [Please ACK Decorator RFC](https://github.com/hyperledger/aries-rfcs/tree/master/features/0317-please-ack).  If `OUTCOME` is specified, the `holder` SHOULD send an ack when the holder's agent has successfully notified the holder of the revocation.

* `thread_id` (required) -- the [thread ID](https://github.com/hyperledger/aries-rfcs/tree/master/concepts/0008-message-id-and-threading#thread-id-thid) of the [issue-credential-v2](https://github.com/hyperledger/aries-rfcs/tree/master/features/0453-issue-credential-v2) protocol which was used to issue one or more credentials that have been revoked by the issuer.  If multiple credentials were issued, each credential has a different credential format but contains the same claims as described [here](https://github.com/hyperledger/aries-rfcs/tree/b982c24b9083dd5dddff6343dbf534cd1cfe36a6/features/0453-issue-credential-v2#message-attachments); therefore, this message notifies the holder that all of these credentials have been revoked.

* `comment` (optional) -- a field that provides some human readable information about the revocation notification.  This is typically the reason for the revocation as deemed appropriate by the issuer.

## Reference

* See the [issue-credential-v2](https://github.com/hyperledger/aries-rfcs/tree/master/features/0453-issue-credential-v2) protocol.
* See the [thread ID](https://github.com/hyperledger/aries-rfcs/tree/master/concepts/0008-message-id-and-threading#thread-id-thid) description.
* See the [Please ACK Decorator RFC](https://github.com/hyperledger/aries-rfcs/tree/master/features/0317-please-ack).

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

