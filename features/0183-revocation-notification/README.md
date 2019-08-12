# Aries RFC 0183: Revocation Notification 1.0
- Authors: [Keith Smith]
- Status: [PROPOSED](/README.md#proposed)
- Since: 2019-08-12
- Status Note:
- Supersedes:
- Start Date: 2018-08-12
- Tags: feature, protocol

## Summary

This RFC defines the message format which an issuer uses to notify a holder that a previously issued credential has been revoked.

## Motivation

We need a standard protocol for an issuer to notify a holder that a previously issued credential has been revoked.

For example, suppose a passport agency revokes Alice's passport.
The passport agency (an issuer) may want to notify Alice (a holder) that her passport has been revoked so that she
knows that she will be unable to use her passport to travel.

## Tutorial

The Revocation Notification protocol is a very simple protocol consisting of a single message:

* Notify - issuer to holder

In addition, the [`ack`](../0015-acks/README.md) and [`problem-report`](../0035-report-problem/README.md) messages are adopted into the protocol for confirmation and error handling. 

This simple protocol allows an issuer to choose to notify a holder that a previously issued credential has been revoked.

It is the issuer's prerogative whether or not to notify the holder that a credential has been revoked.

### Roles

There are two parties involved in a Revocation Notification: `issuer` and `holder`.
The `issuer` sends the `revoke` message to the `holder`.

### Messages

The `revoke` message sent by the `issuer` to the `holder` is as follows:

```JSON
{
  "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/revocation_notification/1.0/revoke",
  "@id": "<uuid-revocation-notification>",
  "credential_id": "<uuid-credential>",
  "comment": "Some comment"
}
```

Description of fields:

* `credential_id` -- identifies the credential which is being revoked.  This is the <uuid-credential> value as sent in the [issue-credential](https://github.com/hyperledger/aries-rfcs/tree/master/features/0036-issue-credential#issue-credential) message.
* `comment`       -- a field that provides some human readable information about the revocation notification.  This is typically the reason for the revocation as deemed appropriate by the issuer.

## Reference

* See the [issue-credential](https://github.com/hyperledger/aries-rfcs/tree/master/features/0036-issue-credential#issue-credential) protocol.

## Drawbacks

If we later added support for a more general subscription and notification message flows, this would be redundant.

## Rationale and alternatives

- Why is this design the best in the space of possible designs?  It is simple.
- What other designs have been considered and what is the rationale for not
choosing them?  A more general subscribe and notification message flows were considered but chose to keep this simple as in the case of the basic message.
- What is the impact of not doing this?  There is no standard way of sending a revocation notification which will be common.

## Prior art

Discuss prior art, both the good and the bad, in relation to this proposal.
A few examples of what this can include are:

- Does this feature exist in other SSI ecosystems and what experience have
their community had?
- For other teams: What lessons can we learn from other attempts?
- Papers: Are there any published papers or great posts that discuss this?
If you have some relevant papers to refer to, this can serve as a more detailed
theoretical background.

This section is intended to encourage you as an author to think about the
lessons from other implementers, provide readers of your proposal with a
fuller picture. If there is no prior art, that is fine - your ideas are
interesting to us whether they are brand new or if they are an adaptation
from other communities.

Note that while precedent set by other communities is some motivation, it
does not on its own motivate an enhancement proposal here. Please also take
into consideration that Aries sometimes intentionally diverges from common
identity features.

## Unresolved questions

- What parts of the design do you expect to resolve through the
enhancement proposal process before this gets merged?
- What parts of the design do you expect to resolve through the
implementation of this feature before stabilization?
- What related issues do you consider out of scope for this 
proposal that could be addressed in the future independently of the
solution that comes out of this doc?
   
## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

Name / Link | Implementation Notes
--- | ---
 |  | 

