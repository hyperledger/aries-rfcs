# 0696: Forget Me

- Authors: [Sam Curren](telegramsam@gmail.com)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2021-06-04
- Status Note: Initial version
- Start Date: 2021-06-04
- Tags: [feature](/tags.md#feature), [protocol](/tags.md#protocol)

## Summary

A protocol to arrange for another party to forget you and your data, in compliance with an established legal basis such as GDPR.

## Motivation

Legislation requires businesses and organizations to forget personal details of an individual upon their request.

There are limits to what must be deleted - discussion of such is outside the scope of this protocol. 

## Scope
There a wide variety of compliant 'forget me' flows. This one is intended to be simple. A request to forget is a request to forget all data completely, rather than a nuanced approach. It is the expectation that after executing this protocol, all data will be deleted (see details below) and the relationship fully terminated.

More nuanced needs should produce a new version of this protocol or a new protocol.


## Tutorial

### Roles

**Data Holder** - The agent that has data related to the _subject_.
**Subject** - The agent who is picking up messages.

### Flow

Subject sends a `removal_request` message to the _Data Holder_. The _Data Holder_ then responds with a `removal_receipt` message and and associated details

## Reference

### Removal Request

Sent by the _subject_ to the _data_holder_ to request a `status` message.

```json=
{
    "@id": "123456781",
    "@type": "https://didcomm.org/forgetme/1.0/removal_request",
    "legal_basis": "GDPR"
}
```

**legal_basis**: String. Must be one of [GDPR, CCPA]
(others may be added by updating this protocol)

### Removal Receipt

Sent by _data_holder_ to confirm the forget me request.

```json=
{
    "@id": "123456781",
    "@type": "https://didcomm.org/forgetme/1.0/removal_receipt",
    "legal_basis":"GDPR",
    "removed": [
        ""
    ],
    "remaining": [
        {
            "item":"",
            "removal_strategy": "",
            "removal_date": "YYYYMMDD",
            "removal_condition": ""
        }
    ]
    
}
```
**removed**: List of strings, each the name of an item removed
**remaining**: List of items not yet removed, with details about future removal.
**removal_strategy**: String, one of ["at_date","at_condition"].
**removal_date**: Datestring, in UTC format YYYYMMDD. Required when _removal_strategy_ is `at_date`.
**removal_condition**: Human readable description of the removal condition. Required when _removal_strategy_ is `at_condition`.

The _removal_date_ and _removal_condition_ should only be included when required, and should be ignored by the message recipient if inappropriately included.

## Prior art

None

## Unresolved questions

- 

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

| Name / Link | Implementation Notes |
| ----------- | -------------------- |
|             |                      |