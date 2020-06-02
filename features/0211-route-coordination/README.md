# 0211: Mediator Coordination Protocol
- Authors: [Sam Curren](telegramsam@gmail.com)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2019-09-03
- Status Note: Initial version, still under discussion. Previously named `Route Coordination Protocol`.
- Start Date: 2019-09-03
- Tags: [feature](/tags.md#feature), [protocol](/tags.md#protocol)

## Summary

A protocol to coordinate mediation configuration between a mediating agent and the recipient.

## Application Scope

This protocol is needed when using an edge agent and a mediator agent from different vendors. Edge agents and mediator agents from the same vendor may use whatever protocol they wish without sacrificing interoperability. 

## Motivation

Use of the forward message in the Routing Protocol requires an exchange of information. The Recipient must know which endpoint and routing key(s) to share, and the Mediator needs to know which keys should be routed via this relationship.

## Protocol

**Name**: coordinatemediation

**Version**: 1.0

**Base URI**: `https://didcomm.org/coordinatemediation/1.0/`

### Roles

**mediator** - The agent that will be receiving `forward` messages on behalf of the _recipient_.
**recipient** - The agent for whom the `forward` message payload is intended.

### Flow
A recipient may discover an agent capable of routing using the Feature Discovery Protocol. If protocol is supported with the _mediator_ role, a _recipient_ may send a `route_request` to initiate a routing relationship.

First, the _recipient_ sends a `route_request` message to the _mediator_. If the _mediator_ is willing to route messages, it will respond with a `route_grant` message. The _recipient_ will share the routing information in the grant message with other contacts.

When a new key is used by the _recipient_, it must be registered with the _mediator_ to enable route identification. This is done with a `keylist_update` message.

The `keylist_update` and `keylist_query` methods are used over time to identify and remove keys that are no longer in use by the _recipient_.

### Terms

The protocol allows for term agreement between the _mediator_ and _recipient_. 

**mediator_terms** indicate terms that the _mediator_ requires the _recipient_ to agree to.

**recipient_terms** indicate terms that the _recipient_ requires the _mediator_ to agree to.

If the _mediator_ requires the _recipient_  to agree to terms prior to service, a `mediate_deny` message will be returned listing the URIs of terms that the user must agree to. Term agreement is indicated by including the same URIs in the `mediator_terms` attribute of the `route_request` message. The *mediator* may indicate which user terms they support in the `recipient_terms` attribute of the `mediate_deny` message.

## Reference

### Mediation Request
This message serves as a request from the _recipient_ to the _mediator_, asking for the permission (and routing information) to publish the endpoint as a mediator.
```jsonc
{
    "@id": "123456781",
    "@type": "<baseuri>/mediate-request",
    "mediator_terms": [],
    "recipient_terms": []
}
```

### Mediation Deny

A mediator may require agreements prior to granting route coordination. If the agreements present in the request are not sufficient, a route deny message may be used to indicate which agreements are required.

```jsonc
{
    "@id": "123456781",
    "@type": "<baseuri>/mediate-deny",
    "mediator_terms": [],
    "recipient_terms": []
}
```

### Mediation Grant

A route grant message is a signal from the mediator to the recipient that permission is given to distribute the included information as an inbound route.
```jsonc
{
    "@id": "123456781",
    "@type": "<baseuri>/mediate-grant",
    "endpoint": "",
    "routing_keys": []
    
}
```
Questions:
- What about multiple endpoint options? http and ws?

### Keylist Update
Used to notify the _mediator_ of keys in use by the _recipient_.
```jsonc
{
    "@id": "123456781",
    "@type": "<baseuri>/keylist_update",
    "updates":[
        {
            "recipient_key": "",
            "action": "" // "add" or "remove"
        }
    ]
}
```
### Keylist Update Response
Confirmation of requested keylist updates.
```jsonc
{
    "@id": "123456781",
    "@type": "<baseuri>/keylist_update_response",
    "updated": [
        {
            "recipient_key": "",
            "action": "" // "add" or "remove"
            "result": "" // [client_error | server_error | no_change | success]
        }
    ]
}
```
Questions:
- What types of errors are possible here?
### Key List Query

```jsonc
{
    "@id": "123456781",
    "@type": "<baseuri>/key_list_query",
    "filter":{
        "": ["",""]
    }
    "paginate": {
        "limit": 30,
        "offset": 0
    }
}
```
Questions:
- Filters feels odd here. Asking to see if a key is registered makes sense, but what else to filter on?

### Key List

```jsonc
{
    "@id": "123456781",
    "@type": "<baseuri>/key_list",
    "keys": [
        {
            "recipient_key": ""
        }
    ]
    "pagination": {
    
    }
    
}
```

## Prior art

There was an Indy HIPE that never made it past the PR process that described a similar approach. That HIPE led to a partial implementation of this inside the Aries Cloud Agent Python



## Unresolved questions

- Still considering alternatives to convey the right meaning.
- Should we allow listing keys by date? You could query keys in use by date?
- How might payment be coordinated?
- Should key ownership be proved when registered? Is there a risk of people requesting other people's keys?
- We are missing a way to check a single key (or a few keys) without doing a full list.
- Additional questions in each section
  
## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

Name / Link | Implementation Notes
--- | ---
 |  | 
