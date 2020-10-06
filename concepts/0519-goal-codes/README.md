# 0519: Goal Codes
- Authors: [Daniel Hardman](daniel.hardman@gmail.com)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2020-07-24
- Status Note: surfaces thinking first used in [0434 OOB Protocol](../../features/0434-outofband/README.md) and in [Co-protocols](https://docs.google.com/presentation/d/17hk6QqLW5M9E4TBPZwXIUBu9eEinMNXReceyZTF4LpA/edit)
- Start Date: 2020-01-01
- Tags: [concept](/tags.md#concept)

## Summary

Explain how different parties in an SSI ecosystem can communicate about their intentions in a way that is understandable by humans and by automated software.

## Motivation

[Agents](../0004-agents/README.md) exist to achieve the intents of their owners. Those intents largely unfold through [protocols](../0003-protocols/README.md). Sometimes intelligent action in these protocols depends on a party declaring their intent. We need a standard way to do that.

## Tutorial

Our early learnings in SSI focused on VC-based proving with a very loose, casual approach to context. We did demos where Alice connects with a potential employer, Acme Corp -- and we assumed that each of the interacting parties had a shared understanding of one another's needs and purposes.

But in a mature SSI ecosystem, where unknown agents can contact one another for arbitrary reasons, this context is not always easy to deduce. Acme Corp's agent may support many different protocols, and Alice may interact with Acme in the capacity of customer or potential employee or vendor. Although we have [feature discovery](../../features/0031-discover-features/README.md) to learn what's possible, and we have [machine-readable governance frameworks](../0430-machine-readable-governance-frameworks/README.md) to tell us what rules might apply in a given context, we haven't had a way to establish the context in the first place. When Alice contacts Acme, a context is needed before a governance framework is selectable, and before we know which features are desirable.

The key ingredient in context is __intent__. If Alice says to Acme, "I'd like to connect,", Acme wants to be able to trigger different behavior depending on whether Alice's intent is to be a customer, apply for a job, or audit Acme's taxes. This is the purpose of a goal code.

### The goal code datatype

To express intent, this RFC formally introduces the goal code datatype. When a field in a [DIDComm](../0005-didcomm/README.md) message contains a goal code, its semantics and format match the description given here. (Goal codes are often declared via the `~thread` decorator, but may also appear in ordinary message fields. See the [Scope section](#scope) below. Convention is to name this field "goal_code" where possible; however, this is only a convention, and individual protocols may adapt to it however they wish.)

>TODO: should we make a decorator out of this, so protocols don't have to declare it, and so any message can have a goal code? Or should we just let protocols declare a field in whatever message makes sense?

Protocols use fields of this type as a way to express the intent of the message sender, thus coloring the larger context. In a sense, goal codes are to DIDComm what the `subject:` field is to email -- except that goal codes have formalized meanings to make them recognizable to automation.

Goal codes use a standard format. They are lower-cased, kebab-punctuated strings. ASCII and English are recommended, as they are intended to be read by the software developer community, not by human beings; however, full UTF-8 is allowed. They support hierarchical dotted notation, where more general categories are to the left of a dot, and more specific categories are to the right. Some example goal codes might be:

* `aries.sell.consumer.fitness`
* `meetupcorp.personal.date`
* `dif.employment.check-references`
* `cci.healthcare.arrange`

Goals are inherently self-attested. Thus, goal codes don't represent objective fact that a recipient can rely upon in a strong sense; subsequent interactions can always yield surprises. Even so, goal codes let agents triage interactions and find misalignments early; there's no point in engaging if their goals are incompatible. This has significant benefits for spam prevention, among other things.

### Verbs

Notice the verbs in the examples: `sell`, `date`, `hire`, and `arrange`. Goals typically involve action; a complete goal code should have one or more verbs in it somewhere. Turning verbs into nouns (e.g., `employment.references` instead of `employment.check-references`) is considered bad form. (Some namespaces may put the verbs at the end; some may put them in the middle. That's a purely stylistic choice.)

### Directionality

Notice, too, that the verbs may imply directionality. A goal with the `sell` verb implies that the person announcing the goal is a would-be seller, not a buyer. We could imagine a more general verb like `engage-in-commerce` that would allow either behavior. However, that would often be a mistake. The value of goal codes is that they let agents align around intent; announcing that you want to engage in general commerce without clarifying whether you intend to sell or buy may be too vague to help the other party make decisions. 

It is conceivable that this would lead to parallel branchs of a goal ontology that differ only in the direction of their verb. Thus, we could imagine `sell.A` and `sell.B` being shadowed by `buy.A` and `buy.B`. This might be necessary if a family of protocols allow either party to initiate an interaction and declare the goal, and if both parties view the goals as perfect mirror images. However, practical considerations may make this kind of parallelism unlikely. A random party contacting an individual to sell something may need to be quite clear about the type of selling they intend, to make it past a spam filter. In contrast, a random individual arriving at the digital storefront of a mega retailer may be quite vague about the type of buying they intend. Thus, the `buy.*` side of the namespace may need much less detail than the `sell.*` side.

### Goals for others

Related to directionality, it may occasionally be desirable to propose goals to others, rather than adovcating your own: "Let &lt;parties = us = Alice, Bob, and Carol> &lt;goal = hold an auction&gt; -- I nominate Carol to be the &lt;role = auctioneer&gt; and get us started." The difference between a normal message and an unusual one like this is not visible in the goal code; it should be exposed in additional fields that associate the goal with a particular identifier+role pair. Essentially, you are proposing a goal to another party, and these extra fields clarify who should receive the proposal, and what role/perspective they might take with respect to the goal.

Making proposals like this may be a feature in some protocols. Where it is, the protocols determine the message field names for the goal code, the role, and the DID associated with the role and goal.

### Matching

The goal code `cci.healthcare` is considered a more general form of the code `cci.healthcare.procedure`, which is more general than `cci.healthcare.procedure.schedule`. Because these codes are hierarchical, wildcards and fuzzy matching are possible for either a sender or a recipient of a message. Filename-style globbing semantics are used.

A sender agent can specify that their owner's goal is just `meetupcorp.personal` without clarifying more; this is like specifying that a file is located under a folder named "meetupcorp/personal" without specifying where; any file "under" that folder -- or the folder itself -- would match the pattern. A recipient agent can have a policy that says, "Reject any attempts to connect if the goal code of the other party is `aries.sell.*`. Notice how this differs from `aries.sell*`; the first looks for things "inside" `aries.sell`; the latter looks for things "inside" `aries` that have names beginning with `sell`.

### Scope

When is a declared goal known to color interactions, and when is it undefined? 

We previously noted that goal codes are a bit like the `subject:` header on an email; they contextualize everything that follows *in that thread.* We don't generally want to declare a goal outside of a thread context, because that would prevent an agent from engaging in two goals at the same time.

Given these two observations, we can say that a goal applies as soon as it is declared, and it continues to apply to all messages in the same thread. It is also inherited by implication through a thread's `pthid` field; that is, a parent thread's goal colors the child thread unless/until overridden.

### Namespacing

To avoid collision and ambiguity in code values, we need to support namespacing in our goal codes. Since goals are only a coarse-grained alignment mechanism, however, we don't need perfect decentralized precision. Confusion isn't much more than an annoyance; the worst that could happen is that two agents discover one or two steps into a protocol that they're not as aligned as they supposed. They need to be prepared to tolerate that outcome in any case.

Thus, we follow the same general approach that's used in java's packaging system, where organizations and communities use a self-declared prefix for their ecosystem as the leftmost segment or segments of a family of identifiers (goal codes) they manage. Unlike java, though, these need not be tied to DNS in any way. We recommend a single segment namespace that is a unique string, and that is an alias for a URI identifying the origin ecosystem. (In other words, you don't need to start with "com.yourcorp.yourproduct" -- "yourcorp" is probably fine.)

The `aries` namespace alias is reserved for goal codes defined in Aries RFCs. The URI aliased by this name is TBD. See the [Reference section](#reference) for more details.

### Versioning

Semver-style semantics don't map to goals in an simple way; it is not obvious what constitutes a "major" versus a "minor" difference in a goal, or a difference that's not worth tracking at all. The content of a goal &mdash; the only thing that might vary across versions &mdash; is simply its free-form description, and that varies according to human judgment. Many different versions of a protocol are likely to share the goal to make a payment or to introduce two strangers. A goal is likely to be far more stable than the details of how it is accomplished.

Because of these considerations, goal codes do not impose an explicit versioning mechanism. However, one is reserved for use, in the unusual cases where it may be helpful. It is to append `-v` plus a numeric suffix: `my-goal-code-v1`, `my-goal-code-v2`, etc. Goal codes that vary only by this suffix should be understood as ordered-by-numeric-suffix evolutions of one another, and goal codes that do not intend to express versioning should not use this convention for something else. A variant of the goal code without any version suffix is equivalent to a variant with the `-v1` suffix. This allows human intuition about the relatedness of different codes, and it allows useful wildcard matching across versions. It also treats all version-like changes to a goal as breaking (semver "major") changes, which is probably a safe default.

Families of goal codes are free to use this convention if they need it, or to invent a non-conflicting one of their own. However, we repeat our observation that versioning in goal codes is often inappropriate and unnecessary.

### Declaring goal codes

#### Standalone RFCs or Similar Sources

Any URI-referencable document can declare famlies or ontologies of goal codes. In the context of Aries, we encourage standalone RFCs for this purpose if the goals seem likely to be relevant in many contexts. Other communities may of course document goal codes in their own specs -- either dedicated to goal codes, or as part of larger topics. The following block is a sample of how we recommend that such goal codes be declared. Note that each code is individually hyperlink-able, and each is associated with a brief human-friendly description in one or more languages. This description may be used in menuing mechanisms such as the one described in [Action Menu Protocol](../../features/0509-action-menu/README.md).

>#### goal codes
>##### `aries.sell`
>__en__: Sell something. Assumes two parties (buyer/seller).
>__es__: Vender algo. Asume que dos partes participan (comprador/vendedor).
>##### `aries.sell.goods.consumer`
>en: Sell tangible goods of interest to general consumers.
>##### `aries.sell.services.consumer`
>en: Sell services of interest to general consumers.
>##### `aries.sell.services.enterprise`
>en: Sell services of interest to enterprises.

#### In DIDComm-based Protocol Specs

Occasionally, goal codes may have meaning only within the context of a specific protocol. In such cases, it may be appropriate to declare the goal codes directly in a protocol spec. This can be done using a section of the RFC as described above.

More commonly, however, a protocol will *accomplish* one or more goals (e.g., when the protocol is fulfilling a co-protocol interface), or will require a participant to *identify* a goal at one or more points in a protocol flow. In such cases, the goal codes are probably declared external to the protocol. If they can be enumerated, they should still be referenced (hyperlinked to their respective definitions) in the protocol RFC.

#### In Governance Frameworks
Goal codes can also be (re-)declared in a [machine-readable governance framework](../0430-machine-readable-governance-frameworks/README.md). 

## Reference

#### Known Namespace Aliases

No central registry of namespace aliases is maintained; you need not register with an authority to create a new one. Just pick an alias with good enough uniqueness, and socialize it within your community. For convenience of collision avoidance, however, we maintain a table of aliases that are typically used in global contexts, and welcome PRs from anyone who wants to update it.

alias | used by | URI
-- | -- | --
aries | Hyperledger Aries Community | TBD

#### Well-known goal codes

The following goal codes are defined here because they already have demonstrated utility, based on early SSI work in Aries and elsewhere.

##### `aries.vc`
Participate in some form of VC-based interaction. 
##### `aries.vc.issue`
Issue a verifiable credential. 
##### `aries.vc.verify`
Verify or validate VC-based assertions.
##### `aries.vc.revoke`
Revoke a VC.
##### `aries.rel`
Create, maintain, or end something that humans would consider a relationship. This should not to be confused with building a DIDComm channel. (Building a DIDComm channel is a low-level procedure, not a high-level goal.)
##### `aries.rel.build`
Create a relationship. Carries the meaning implied today by a LinkedIn invitation to connect or a Facebook "Friend" request.

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

*Implementation Notes* [may need to include a link to test results](/README.md#accepted).

Name / Link | Implementation Notes
--- | ---
 | 

