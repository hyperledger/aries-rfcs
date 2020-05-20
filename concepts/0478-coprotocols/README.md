# Aries RFC 0478: Coprotocols
- Authors: [Daniel Hardman](daniel.hardman@gmail.com)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2020-05-19
- Status Note: Socialized on Aries community call in Feb 2020, using [these slides](https://docs.google.com/presentation/d/17hk6QqLW5M9E4TBPZwXIUBu9eEinMNXReceyZTF4LpA/edit). Discussed again in May 2020.
- Start Date: 2020-02-03
- Tags: feature, protocol

![icon](icon.png)

(originals of graphics at https://j.mp/2XgyjH3)

## Summary

Explains how one protocol can invoke and influence others, giving inputs and receiving outputs and errors.

## Motivation

It's common for complex business workflows to be composed from smaller, configurable units of logic. It's also common for multiple processes to evolve in interrelated ways. Achieving flexible reuse like this is one of the major goals of protocols built atop DIDComm. We need a standard methodology for doing so.

## Tutorial

A [protocol is any recipe for a stateful interaction](../0003-protocols/README.md). [DIDComm](../0005-didcomm/README.md) itself is a protocol, as are many primitives atop which it is built, such as HTTP, Diffie-Hellman key exchange, and so forth. However, when we talk about protocols in decentralized identity, without any qualifiers, we usually mean application-level interactions like [credential issuance](../../features/0036-issue-credential/README.md), [feature discovery](../../features/0031-discover-features/README.md), [third-party introductions](../../features/0028-introduce/README.md), and so forth. These protocols are message-based interactions that use DIDComm.

We want these protocols to be __composable__. In the middle of issuing credentials, we want to negotiate payment -- and in the middle of negotiating payment, we want to handle a network brownout and reconnect. We could build payment into credential issuance, and network connection management into payment, but this runs counter to the [DRY principle](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself) and to general best practice in encapsulation. A good developer writing a script to issue credentials would probably isolate payment and connection management logic in separate functions or libraries, and would strive for [loose coupling](https://en.wikipedia.org/wiki/Loose_coupling) so each could evolve independently.

Agents that run protocols have similar goals to the script developer. How we achieve them is the subject of this RFC.

### Subroutines

In the world of computer science, a subroutine is a foundational abstraction. It breaks logic into small, reusable chunks that are easy for a human to understand and document, and it formalizes their interfaces. Code calls a subroutine by referencing it via name or address, and providing specified arguments as input. The subroutine computes on this input, eventually producing an output; the details don't interest the caller. While the subroutine is busy, the caller typically waits. Callers can often avoid recompilation when encapsulated details in subroutines change. Implementations of subroutines can come from pluggable libraries. These can be written by different programmers in different programming languages, as long as a calling convention is shared by both parties.

Thinking of protocols as analogs to subroutines suggests some interesting questions:  

* How do we invoke one protocol from another?
* How does a protocol emit an output?
* What is the calling convention?
* How do errors propagate (or exceptions get thrown and handled)?

### Coroutines

Before we answer these questions, let's think about a generalization of subroutines that's slightly less familiar to some programmers: __coroutines__. As a category, coroutines are more flexible and powerful than subroutines; subroutines are just their simplest variant. Coroutines may be, but aren't required to be, derivative call-stack "children" of their callers; they can have complex lifecycles that begin or end outside the caller's lifespan. Coroutines may receive inputs at multiple points, not just at launch. They may yield outputs at multiple points, too.

The flexiblity of coroutines gives options to programmers, and it explains why most programming languages evolve to offer them as first-class constructs when they encounter demanding requirements for asynchronicity, performance, or scale. For example, early versions of python lacked the concept of coroutines; if you wrote a loop over `range(1, 1000000)`, python allocated a container holding 1 million numbers, and then iterated over them. When generators (a type of coroutine) were added to the language, the underlying logic changed. Now `range(1, 1000000)` is a coroutine invocation that trades execution state back and forth with its sibling caller routine. The first time it is invoked, it receives and stores its input values, then produces one output (the lower bound of the range). Each subsequent time through the loop it is invoked again; it increments its internal state and yields a new output back to the caller. No allocations occur, and an early break from the loop wastes nothing.

If we want to choose one conceptual parallel for how protocols relate to one another, we should think of them a coroutines, not subroutines. Although payment as a subroutine inside credential issuance sounds plausible at first glance, it turns out to be clumsy under deeper analysis. A payment protocol yields more than one output -- typically a preauthorization at an intermediate stage, then a final outcome when it completes. At the preauthorization stage, it should accept graceful cancellation (a second input, after launch). And high-speed, bulk issuance of credentials is likely to benefit from payment and issuance being partly parallelized.

![diagram of payment as a coprotocol](payment-coprotocol.png)

Similarly, a handshake protocol like [DID Exchange](../../features/0023-did-exchange/README.md) or [Connection](../../features/0160/connection-protocol/README.md) is a coprotocol of [Introduce](../../features/0028-introduce/README.md); this makes it easy for Introduce to complete as soon as the handshake begins, instead of waiting for it to finish so it can contain its full lifecycle like a subroutine call.
 
 By thinking of protocols as coroutines, we can simplify to subroutines where that makes sense, but tap the added flexibility and power of coroutines where a design problem demands it.

### The simple answer that falls apart

When the DIDComm community first began thinking about one protocol invoking another, we imagined that the interface to the called coprotocol would simply be its first message. For example, if verfiable credential issuer Acme Corp wanted to demand payment for a credential during an issuance protocol with Bob, Acme would simply send to Bob a `request_payment` message that was the first message in a `make_payment` protocol. This would create an instance of the payment protocol running beside issuance; issuance could then wait until it completes before proceeding.

Unfortunately, this approach looks less attractive after study: 

* It creates a tight coupling between issuance and payment. The logic inside issuance must know exactly what data format, semantics, and versioning rules apply to the payment protocol, in order to generate its first message. If the payment protocol changes, the issuance protocol breaks. There is no room to discover a payment protocol from one of several alternatives that both parties mutually support.

* It doesn't explain how the payment protocol emits output that its caller can consume. Individual agents could code proprietary answers to this question, but interoperability would be lost.

* It doesn't offer a signalling mechanism that would let the two protocols proceed in parallel, syncing up ony when necessary.

* It doesn't explain how errors propagate, or how to decide what they mean for the calling protocol.

### General Interface

What we want, instead, is a formal declaration of a protocol's properties. Theoretically, it might resemble a function prototype in some ways, in that it would describe the inputs that launch the protocol, and it might also describe an output and/or error that the protocol emits when it finishes. But it must also be capable of describing errors, inputs, and outputs at other stages of the protocol's lifecycle.

Unlike normal functions in code, protocols nearly always involve another codebase running remotely (the other party in the protocol); thus, the interface also needs to include enough information to dynamically discover/bind pluggable implementations at run-time, like a `load_library()` call in Posix.

Also unlike functions, protocol interfaces need to be partitioned by role; the experience of a payer and a payee with respect to a payment protocol may be quite different, so the interface used by a coprotocol will vary by which role the coprotocol instance embodies.

Suppose we have an imaginary payment protocol with 2 roles, `payer` and `payee`, in which the payer goes through 3 states: `authorizing` (when it is seeking a pre-authorization), `uncommitted` (when it has a preauthorization but has not yet been told to finalize payment), and `done` (when the final outcome of the payment is known. The structure in the following example might constitutes a formal __coprotocol interface__ for the `payer` role:

```jsonc
{
    // Used in discovery. Takes the form: role@goal-name/goal-version.
    //
    // A protocol that needs to depend on a co-protocol should
    // consider being willing to bind to any protocol that implements
    // the role it needs, with the goal it has. This allows code on
    // one agent to find a list of implementations it might use, and
    // then negotiate with a remote party until a compatible co-protocol
    // is chosen on the other side.
    //
    // Goals should be defined in their own RFCs. Based on what appears
    // below, we'd expect to find an Aries RFC about a "make-payment"
    // goal. Goals have known semantics but stop short of the implementation
    // detail provided in protocol RFCs.
    "goal": "payer@make-payment/1.0",

    // A set of points at which the coprotocol can interact.
    "interactions": [
        {
            "state_name": null, // null defined to mean "at invocation"
            // To launch this as a co-protocol, you must provide 2 or 3
            // inputs: amount, currency, and note.
            "inputs": [
                {"name": "amount", "ex": 1.23},
                {"name": "currency", "ex": "INR"},
                {"name": "note", "ex": "For commercial driver's license credential.", optional: true}
            ]
        },
        {
            "state_name": "(END)" // reserved to mean "on termination"
        }
        {
            "state_name": "(END)" // reserved to mean "on termination"
        }
    ]
}
```


* How do we invoke one protocol from another?
* How does a protocol emit an output?
* What is the calling convention?
* How do errors propagate (or exceptions get thrown and handled)?

All of these answers are embodied in a protocol's formal __interface__. 

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

*Implementation Notes* [may need to include a link to test results](README.md#accepted).

Name / Link | Implementation Notes
--- | ---
 | 

