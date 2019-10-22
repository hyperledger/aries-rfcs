# Aries RFC 0217: Linkable Message Paths
- Authors: [Daniel Hardman](daniel.hardman@gmail.com)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2019-09-10
- Status Note: Purely theoretical at this point, but may be relevant to efforts to join subprotocols to superprotocols. Mentioned in [RFC 0214 "Help Me Discover" Protocol](../../features/0214-help-me-discover/README.md).
- Start Date: 2019-08-26
- Tags: [concept](/tags.md#concept)

## Summary

Describes how to hyperlink to specific elements of specific DIDComm messages.

## Motivation

It must be possible to refer to specific pieces of data in specific DIDComm messages. This allows a message later in a protocol to refer to data in a message that preceded it, which is useful for stitching together subprotocols, debugging, error handling, logging, and various other scenarios.

## Tutorial

There are numerous approaches to the general problem of referencing/querying a piece of data in a JSON document. We have chosen [JSPath](https://github.com/dfilatov/jspath#quick-example) as our solution to that part of the problem; see [Prior Art](#prior-art) for a summary of that option and a comparison to alternatives.

What we need, over and above JSPath, is a URI-oriented way to refer to an individual message, so the rest of the referencing mechanism has a JSON document to start from.

### DIDComm Message URIs

A __DIDComm message URI__ (__DMURI__) is a string that references a sent/received message, using [standard URI syntax as specified in RFC 3986](https://tools.ietf.org/html/rfc3986). It takes one of the following forms:

1. `didcomm://<thid>/<msgid>`
2. `didcomm://./<msgid>` or `didcomm://../<msgid>`
3. `didcomm:///<msgid>` (note 3 slashes)
4. `didcomm://<sender>@<thid>/<senderorder>`

Here, `<msgid>` is replaced with the value of the `@id` property of a plaintext DIDComm message; `<thid>` is replaced with the `~thread.thid` property, `<sender>` is replaced with a DID, and `<senderorder>` is replaced with a zero-based index (the Nth message emitted in the thread by that sender). 

Form 1 is called __absolute form__, and is the prefered form of DMURI to use when talking about messages outside the context of an active thread (e.g., in log files)

Form 2 is called __relative form__, and is a convenient way for one message to refer to another within an ongoing interaction. It is relatively explicit and terse. It uses 1 or 2 dots to reference the current or parent thread, and then provides the message id with that thread as context. Referencing more distant parent threads is done with absolute form.

Form 3 is called __simple form__. It omits the thread id entirely. It is maximally short and usually clear enough. However, it is slightly less preferred than forms 1 and 2 because it is possible that some senders might not practice good message ID hygeine that guarantees global message ID uniqueness. When that happens, a message ID could get reused, making this form ambiguous. The most recent message that is known to match the message id must be assumed.

Form 4 is called __ordered form__. It is useful for referencing a message that was never received, making the message's internal `@id` property unavailable. It might be used to request a resend of a lost message that is uncovered by the gap detection mechanism in DIDComm's message threading.

Only parties who have sent or received messages can dereference DMURIs. However, the URIs should be transmittable through any number of third parties who do not understand them, without any loss of utility.

### Combining a DMURI with a JSPath

A JSPath is concatenated to a DMURI by using an intervening slash delimiter:

`didcomm:///e56085f9-4fe5-40a4-bf15-6438751b3ae8/.~timing.expires_time`

[If a JSPath uses characters from RFC 3986's __reserved characters__ list in a context where they have special meaning, they must be percent-encoded](https://en.wikipedia.org/wiki/Percent-encoding).

## Reference

Provide guidance for implementers, procedures to inform testing,
interface definitions, formal function prototypes, error codes,
diagrams, and other technical details that might be looked up.
Strive to guarantee that:

- Interactions with other features are clear.
- Implementation trajectory is well defined.
- Corner cases are dissected by example.

## Drawbacks

Why should we *not* do this?

## Rationale and alternatives

- Why is this design the best in the space of possible designs?
- What other designs have been considered and what is the rationale for not
choosing them?
- What is the impact of not doing this?

## Prior art

* [JSPath](https://github.com/dfilatov/jspath): the one we're using. Simple and relatively current, with clean syntax.
* [JSONPath](https://github.com/json-path/JsonPath): superseded by JSONQuery
* [JSONQuery](https://dojotoolkit.org/reference-guide/1.10/dojox/json/query.html): also looks a bit old
* [JSONSelect](https://github.com/lloyd/JSONSelect): old. More like CSS selectors
* [JSONiq](http://jsoniq.com/): powerful and current, but focuses more on querying; may be overkill for just referencing a subobject

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

