# Aries RFC 0530: Goal - Human Readable Verifiable Identifier

- Authors: [Sam Curren](telegramsam@gmail.com)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2020-08-26
- Status Note: Early Proposal
- Start Date: 2020-08-26
- Tags: goalcode

## Summary

DIDs are not human friendly. DIDComm provides a secure connection between two DIDs. This goal code seeks to provide a verifiable, human readable identifier from one party to another.

## Motivation

Presenting a Human Readable Verifiable Identifier over a DIDComm connection aids the user in positive connection identification. It also plays a role in Man-in-the-Middle (MitM) attack prevention.

## Reference

### Goal Code

`aries.receive.verifiable.identifier`

### Explanation

The party presenting this goal code has a goal of receiving a human readable verifiable identifier from the party it presents it to.

### Key Concepts

Human Readable implies that the identifier is meaningful to a human. This might be an identifier already used to communicate, such as an email address, phone number, website domain name, or social media account name.

A Verifiable identifier requires that some level of assurance is provided that control has been proven over the identifier. 

Governance Frameworks that serve this goal code must provide details about which identifiers are acceptable, and how they are to be verified.  

## Governance Frameworks 

The following Governance Frameworks are related to this goal code.

- Domain Control 
- Email Ownership

## Unresolved questions

- 

## Implementations

> NOTE: This section should remain in the RFC as is on first release. Remove this note and leave the rest of the text as is. Template text in all other sections should be removed before submitting your Pull Request.

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

*Implementation Notes* [may need to include a link to test results](README.md#accepted).

Name / Link | Implementation Notes
--- | ---
 |
