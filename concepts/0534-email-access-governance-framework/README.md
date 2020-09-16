# 0534: Email Access Governance Framework
- Authors: [Sam Curren](telegramsam@gmail.com)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2020-09-16
- Status Note: Proposed, but in need of specifics to put into action.
- Start Date: 2020-07-14
- Tags: feature, protocol

## Summary

This Governance Framework is community managed.

When making connections from one person to another over DIDComm, it is useful to be able to gain proof of something to verify that the connection is with the right person and has not been subject to a MITM attack. We expect this Governance Framework to be one of many used for the purpose of helping to verify identity attributes in the creation of trusted channels.

This is an early attempt at the creation and use of of a practical governance framework. As Governance Framework technology improves, we expect this particular framework to be replaced.

## Purpose

To facilitate the verification of email access between two parties over DIDComm and related technologies.

## Details

### Roles

**issuer**: Responsible for issuing credentials according to the requirements of this governance framework.

### Schemas

<schemas listed here>

### Issuers

<list of issuers here>

### Issue Requirements

Issuers must validate email ownership by sending an email to the email address in question. The email MUST contain a link for the user to click, or a code to be entered in a verification step. After verifying that the clicked link or entered code matches, the credential may be issued.

Issued credentials should indicate an expiration date no longer than 6 months from the date of verification.

### Revocation

This framework does not currently use revocation, relying upon the expiration date to prevent widespread issues.

### Allowable Verification Purposes

Email addresses revealed in this manner may be used for the following purposes:

- Displaying to recipient.
- Checking against address book.

Use outside these purposes, including the following examples, violates the allowed uses as specified by this governance framework.

- Sending email to the address without explicit additional approval of the user.
- Sharing email address with any other party.

### Machine Readable Document

Located [here](data.json).

## Notes

- The machine readable document is as simple as possible by design. As related technology improves, the document will be updated to reflect these changes.
- Code for the indy email verification service: https://github.com/bcgov/indy-email-verification that could be used as a basis for an issuer.

## Unresolved questions

- Should redundant information be maintained between this human readable document and the machine readable file that accompanies it? More effort, but also more clear.
- Naming? Ownership/Control/Access?
- Which networks?
- Need Schemas and Issuers
- Does the Impl section below make sense for a governance framework?
## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

*Implementation Notes* [may need to include a link to test results](README.md#accepted).

Name / Link | Implementation Notes
--- | ---
 | 

