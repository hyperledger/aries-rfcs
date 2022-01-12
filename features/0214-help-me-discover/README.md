# Aries RFC 0214: "Help Me Discover" Protocol
- Authors: [George Aristy](george.aristy@securekey.com), [Daniel Hardman](daniel.hardman@gmail.com)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2019-09-10
- Status Note: implementation is being explored by SecureKey  
- Start Date: 2018-08-20
- Tags: [feature](/tags.md#feature), [protocol](/tags.md#protocol)

## Summary

Describes how one party can ask another party for help discovering an unknown person, organization, thing, or chunk of data.

## Motivation

Asking a friend to help us discover something is an extremely common human interaction: "Dad, I need a good mechanic. Do you know one who lives near me?"

Similar needs exist between devices in highly automated environments, as when a drone lands in hangar and queries a dispatcher agent to find maintenance robots who can repair an ailing motor.

We need a way to perform these workflows with DIDComm.

## Tutorial

### Name and version

This is the "Help Me Discover" protocol, version 1.0. It is uniquely identified by the following [PIURI](../../concepts/0003-protocols/README.md#piuri):

    https://didcomm.org/help-me-discover/1.0


### Roles and States

This protocol embodies a standard request-response pattern, and therefore has __requester__ and __responder__ roles. A `request` message describes what's wanted. A `response` message conveys whatever knowledge the responder wants to offer to be helpful. Standard state evolution applies:

![diagram](https://github.com/hyperledger/aries-rfcs/raw/master/concepts/0003-protocols/request-response.png)

[![states](https://github.com/hyperledger/aries-rfcs/raw/master/features/0031-discover-features/state-machines.png)](https://docs.google.com/spreadsheets/d/1smY8qhG1qqGs0NH9g2hV4b7mDqrM6MIsmNI93tor2qk/edit#gid=1176419697)

### Requirements

The following requirements do not change this simple framework, but they introduce some complexity into the messages:

* It must be possible to describe what's wanted using rich criteria, combinable to arbitrary levels of detail with boolean operators.
* It is desirable that criteria should be expressed in a way that harmonizes with proof requests, which also need a criteria language. 
* It must be possible for the responder to give partial answers: "I do know a good mechanic, but not one that lives close to you."
* It must be possible for the responder to give compound answers: "Here's an item that satisfies critiera 1 and 3, and here's a different itme that satisfies criteria 2 and 4."
* It must be possible for this protocol to precede another protocol (e.g., [RFC 0028 Introduce Protocol](https://github.com/hyperledger/aries-rfcs/blob/main/features/0028-introduce/README.md)) in such a way that what follows can refer back to items in this protocol in an unambiguous way, as in "Here's an introduction to the party that I just told you about, that satisfies criteria 3 and 4 from the 'Help Me Discover' request you recently made."

### Messages

#### `request`

A simple request message looks like this:

```jsonc
{
    "@type": "https://didcomm.org/help-me-discover/1.0/request",
    "@id": "a2248fb5-d46e-4898-a781-2f03e5f23964"
    // human-readable, localizable, optional
    "comment": "any ideas?",
    // please help me discover match for this
    "desired": { 
        "all": [ // equivalent of boolean AND -- please match this list
            // first criterion: profession must equal "mechanic"
            {"profession": "mechanic", "id": "prof"},
            // second criterion in "all" list: any of the following (boolean OR)
            {
                "any": [
                    // average rating > 3.5
                    {"averageRating": 3.5, "op": ">", "id": "rating"},
                    // list of certifications contains "ASE"
                    {"certifications": "ASE", "op": "CONTAINS", "id": "cert"},
                    // zipCode must be in this list
                    {"zipCode": ["12345", "12346"], "op": "IN", "id": "where"}
                ], // end of "any" list
                "n": 2, // match at least 2 from the list
                "id": "2-of-3"
            }
        ],
        "id": "everything"
    }
}
```

In plain language, this particular request says:

>Please help me discover someone who's a mechanic, and who possesses at least 2 of the following 3 characteristis: they have an average rating of at least 3.5 stars; they have an ASE certification; they reside in zip code 12345 or 12346.

The data type of `desired` is a __criterion__ object. A criterion object can be of type `all` (boolean AND), type `any` (boolean OR), or `op` (a particular attribute is tested against a value with a specific operator). The `all` and `any` objects can nest one another arbitrarily deep.

Parsing these criteria, and performing matches against them, can be done with the SGL library, which has ports for JavaScript and python. Other ports should be trivial; it's only a couple hundred lines of code. The hardest part of the work is giving the library an object model that contains candidates against which matching can be done.

Notice that each criterion object has an `id` property. This is helpful because responses can now refer to the criteria by number to describe what they've matched.

See [Reference](#reference) for fancier examples of requests.

#### `response`

A `response` message looks like this:

```jsonc
{
    "@type": "https://didcomm.org/help-me-discover/1.0/response",
    "@id": "5f2396b5-d84e-689e-78a1-2fa2248f03e4"
    "~thread": { "thid": "a2248fb5-d46e-4898-a781-2f03e5f23964" }
    // human-readable, localizable, optional
    "comment": "here's the best I've got", 
    "candidates": [
        {
            "id": "Alice",
            "@type": "person",
            "matches": ["prof","rating","cert","2-of-3","everything"]
        },
        {
            "id": "Bob",
            "@type": "drone",
            "matches": ["prof","cert","where","2-of-3","everything"]
        },
        {
            "id": "Carol",
            "matches": ["rating","cert","where"]
        }
    ]
}
```

In plain language, this response says:

>I found 3 candidates for you. One that I'll call "Alice" matches everything except your `where` criterion. One called "Bob" matches everything except your `rating` criterion. Once called "Carol" matches your `rating`, `cert`, and `where` criteria, but because she didn't match `prof`, she wasn't an overall match.

### Using a "Help me discover" response in subsequent interactions

A `candidate` in a response message like the one shown above can be referenced in a subsequent interactions by using the [RFC 0xxx: Linkable DIDComm Message Paths](https://hackmd.io/e0goViUMQBmwcfoze2j6rA) mechanism. For example, if Fred wanted to ask for an introduction to Bob after engaging in the sample request-response sequence shown above, he could send a `request` message in the Introduce Protocol, where `to` (the party to whom he'd like to be introduced) included a `discovered` property that referenced the `candidate` with `id` equal to `"Bob"`:

```jsonc
{
  "@type": "https://didcomm.org/introduce/1.0/request",
  "@id": "df3b699d-3aa9-4fd0-bb67-49594da545bd",
  "to": {
    "discovered": "didcomm:///5f2396b5-d84e-689e-78a1-2fa2248f03e4/.candidates%7B.id+%3D%3D%3D+%22Bob%22%7D"
  }
}
```

### Accuracy, Trustworthiness, and Best Effort

As with these types of interactions in "real life", the "help me discover" protocol cannot make any guarantees about the suitability of the answers it generates. The responder could be malicious, misinformed, or simply lazy. The contract for the protocol is:

* Requesters should attempt to ask reasonable, respectful, answerable questions
* Responders who wish to be helpful should make a best effort to address criteria accurately
* There is likely to be a useful relationship between what the requester asks for and what the responder provides

The requester must verify results independently, if their need for trust is high.

### Privacy Considerations

Just because Alice knows that Bob is a political dissident who uses a particular handle in online forms does not mean Alice should divulge that information to anybody who engages in the "Help Me Discover" protocol with her. When matching criteria focus on people, Alice should be careful and use good judgment about how much she honors a particular request for discovery. In particular, if Alice possesses data about Bob that was shared with her in a previous Present Proof Protocol, the terms of sharing may not permit her to divulge what she knows about Bob to an arbitrary third party. See the Data Consent Receipt RFC.

These issues probably do not apply when the thing being discovered is not a private individual.

## Reference

### Discover someone who can prove

A `request` message can ask for someone that is capable of proving using verifiable credentials, as per [RFC 0037](../0037-present-proof/README.md):

```jsonc
{
    "@type": "https://didcomm.org/help-me-discover/1.0/request",
    "@id": "248fb52a-4898-a781-d46e-e5f239642f03"
    "desired": { 
        // either subjectRole or subjectDid:
        //   - subjectRole has value of role in protocol
        //   - subjectDid has value of a DID (useful in N-Wise settings)
        "verb": "prove", 
        "subjectRole": "introducer", 
        "car.engine.rating": "4", 
        "op": ">", 
        "id": "engineRating"
    }
}
```

In plain language, this particular request says:

>Please help me discover someone who can act as introducer in a protocol, and can prove that a car's rating > 4.

Another example might be:

```jsonc
{
    "@id": "a2248fb5-d46e-4898-a781-2f03e5f23964",
    "@type": "https://didcomm.org/help-me-discover/1.0/request",
    "comment": "blood glucose",
    "desired": {
        "all": [
            {
                "id": "prof",
                "profession": "medical-lab"
            },
            {
                "id": "glucose",
                "provides": {
                    "from": "bloodtests",
                    "just": [
                        "glucose"
                    ],
                    "subject": "did:peer:introducer"
                }
            }
        ],
        "id": "everything"
    }
}
```

This says:

>Please help me discover <x> that has profession = "medical-lab" and can provide measurements of the introducer's blood-glucose levels


## Drawbacks

If we are not careful, this protocol could be used to discover attributes about third parties in a way that subverts privacy. See [Privacy Considerations](#privacy-considerations).

## Unresolved questions

- Need to reconcile against general subprotocol/superprotocol communication.
   
## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

Name / Link | Implementation Notes
--- | ---
 |  | 

