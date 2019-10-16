# 0211: Route Coordination Protocol
- Authors: [Sam Curren](telegramsam@gmail.com)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2019-09-03
- Status Note: Initial version 
- Start Date: 2019-09-03
- Tags: [feature](/tags.md#feature), [protocol](/tags.md#protocol)

## Summary

A protocol to coordinate routing configuration between a routing agent and the recipient.

## Motivation

Use of the forward message in the Routing Protocol requires an exchange of information. The Recipient must know which endpoint and routing key(s) to share, and the Router needs to know which keys should be routed via this relationship.

## Tutorial

### Roles

**router** - The agent that will be receiving `forward` messages on behalf of the _recipient_.
**recipient** - The agent for whom the `forward` message payload is intended.

### Flow
A recipient may discover an agent capable of routing using the Feature Discovery Protocol. If protocol is supported with the _router_ role, a _recipient_ may send a `route_request` to initiate a routing relationship.

First, the _recipient_ sends a `route_request` message to the _router_. If the _router_ is willing to route messages, it will respond with a `route_grant` message. The _recipient_ will share the routing information in the grant message with other contacts.

When a new key is used by the _recipient_, it must be registered with the _router_ to enable route identitifcation. This is done with a `keylist_update` message.

The `keylist_update` and `keylist_query` methods are used over time to identify and remove keys that are no longer in use by the _recipient_.



## Reference

### Route Request
This message serves as a request from the recipient to the router, asking for the permission (and routing information) to publish the endpoint as a router.
```jsonc
{
    "@id": "123456781",
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/routecoordination/1.0/route-request"
}
```
### Route Grant
A route grant message is a signal from the router to the recipient that permission is given to distribute the included information as an inbound route.
```jsonc
{
    "@id": "123456781",
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/routecoordination/1.0/route-grant",
    "endpoint": "",
    "routing_keys": []
    
}
```
Questions:
- What about multiple endpoint options? http and ws?

### Keylist Update
Used to notify the _router_ of keys in use by the _recipient_.
```jsonc
{
    "@id": "123456781",
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/routecoordination/1.0/keylist_update",
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
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/routecoordination/1.0/keylist_update_response",
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
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/routecoordination/1.0/key_list_query",
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
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/routecoordination/1.0/key_list",
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

There was an Indy HIPE that never made it past the PR process that described a similar approach. That HIPE led to a partial implementaiton of this inside the Aries Cloudagent Python



## Unresolved questions

- Still considering alternatives to convey the right meaning.
- Should we allow listing keys by date? You could query keys in use by date?
- Additional questions in each section
  
## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

Name / Link | Implementation Notes
--- | ---
 |  | 
