# 0004: Agents
- Author: Daniel Hardman <daniel.hardman@gmail.com>
- Start Date: 2017-11-01 (approx, backdated)

## Status
- Status: [ACCEPTED](/README.md#rfc-lifecycle)
- Status Date: 2019-01-15
- Status Note: On a standards track and beginning to influence many mental
  models, but not yet [ADOPTED](/README.md#rfc-lifecycle). This supersedes
  [Indy HIPE 0002](https://github.com/hyperledger/indy-hipe/tree/master/text/0002-agents).

## Summary
[summary]: #summary

Provide a high-level introduction to the concepts of agents in
the self-sovereign identity ecosystem.

## Tutorial
[tutorial]: #tutorial

Managing an identity is complex. We need tools to help us.

In the physical world, we often delegate complexity to trusted proxies
that can help. We hire an accountant to do our taxes, a real estate
agent to help us buy a house, and a talent agent to help us
pitch an album to a recording studio.

On the digital landscape, humans and organizations (and sometimes,
things) cannot directly consume and emit bytes, store and manage
data, or perform the crypto that self-sovereign identity demands.
They need delegates--__agents__--to help. [Agents are a vital
dimension across which we exercise sovereignty over identity](
https://medium.com/evernym/three-dimensions-of-identity-bc06ae4aec1c).

![agent](agent.png)

#### Essential Characteristics

When we use the term "agent" in the SSI community, we more properly mean
"an agent of self-sovereign identity." This means something more specific
than just a "user agent" or a "software agent." Such an agent has three
defining characteristics:

1. It acts as a fiduciary on behalf of a single [identity owner](
https://docs.google.com/document/d/1gfIz5TT0cNp2kxGMLFXr19x1uoZsruUe_0glHst2fZ8/edit#heading=h.2e5lma3u6c9g)
(or, for agents of things like IoT devices, pets, and similar things, a single _controller_). 
2. It holds cryptographic keys that uniquely embody its delegated authorization.
3. It interacts using interoperable [DID Comm protocols](
https://github.com/hyperledger/indy-hipe/pull/69).

These characteristics don't tie an agent to any particular blockchain.
It is possible to implement agents without any
use of blockchain at all (e.g., with [peer DIDs](
https://github.com/openssi/peer-did-method-spec)), and some efforts to do so are
quite active. 

#### Canonical Examples

Three types of agents are especially common:

1. A mobile app that Alice uses to manage credentials and to [connect
to others](https://github.com/hyperledger/indy-hipe/pull/54) is an
agent for Alice.
2. A cloud-based service that Alice uses to expose a stable endpoint
where other agents can talk to her is an agent for Alice.
3. A server run by Faber College, allowing it to issue credentials
to its students, is an agent for Faber.

Depending on your perspective, you might describe these agents in
various ways. #1 can correctly be called a "mobile" or "edge" or
"rich" agent. #2 can be called a "cloud" or "routing" agent. #3 can
be called an "on-prem" or "edge" or "advanced" agent. See
[Categorizing Agents](#categorizing-agents) for a discussion about
why multiple labels are correct.

Agents can be other things as well. They can big or small, complex or
simple. They can interact and be packaged in various ways.  They can
be written in a host of programming languages. [Some
are more canonical than others](#the-agent-ness-continuum). But all
the ones we intend to interact with in the self-sovereign identity
problem domain share the [three essential
characteristics](#essential-characteristics) described above.

#### How Agents Talk

[DID communication]( ../0005-didcomm/README.md)
(DIDComm), and the [protocols built atop it](../0003-protocols/README.md)
are each rich subjects unto themselves. Here, we will stay very high-level.

Agents can use many different communication transports: HTTP(S)
1.x and 2.0, WebSockets, IRC, Bluetooth, AMQP, NFC, Signal, email, push
notifications to mobile devices, ZMQ, and more. However, all A2A is
message-based, and is secured by modern, best-practice public key
cryptography. _How_ messages flow over a transport may vary--but their
security and privacy toolset, their links to the [DIDs and DID Docs of
identity owners](https://w3c-ccg.github.io/did-spec/), and [the ways
their messages are packaged and handled](../0005-didcomm/README.md)
are standard.

Agents connect to one another through a standard [connection
protocol](https://github.com/hyperledger/indy-hipe/pull/54),
discover one another's endpoints and keys through standard DID
Docs, [discover one another's features](
https://github.com/hyperledger/indy-hipe/pull/73) in a standard way,
and maintain relationships in a standard way. All of these points of
standardization are what makes them interoperable.

Because agents speak so many different ways, and because many of them
won't have a permanent, accessible point of presence on the network, they
can't all be thought of as web servers with a Swagger-compatible API
for request-response. The analog to an API construct in agent-land is
_protocols_. These are patterns for stateful interactions. They specify
things like, "If you want to negotiate a sale with an agent, send it a
message of type X. It will respond with a message of type Y or type Z,
or with an error message of type W. Repeat until the negotiation
finishes." Some interesting A2A protocols include the one where two
parties connect to one another to build a relationship, the one where
agents discover which protocols they each support, the one credentials
are issued, and the one where proof is requested and sent.
Hundreds of other protocols are being defined.

#### How to Get an Agent

As the ecosystem for self-sovereign identity matures, the average
person or organization will get an agent by downloading it
from the app store, installing it with their OS package manager, or
subscribing to it as a service. However, the availability of quality
pre-packaged agents is still limited today.

Agent providers are emerging in the marketplace, though. Some are
governments, NGOs, or educational institutions that offer agents for
free; others are for-profit ventures. If you'd like suggestions about
ready-to-use agent offerings, please describe your use case in
`#indy-agent` on [chat.hyperledger.org](https://chat.hyperledger.org).

There is also intense activity in the SSI community around building
custom agents and the tools and processes that enable them. Some of
this work is happening in the [indy-agent repo on github.com](
https://github.com/hyperledger/indy-agent); other efforts are driven
by the [Sovrin Foundation](https://sovrin.org) or other entities.

The indy-agent repo on github.com has _reference_ agents and a test
suite. These are intended to demonstrate agent techniques and possibly
to provide a foundation upon which fancier agents could be built; they
are not ready-to-use business solutions. 

#### How to Write an Agent

This is one of the most common questions that Aries newcomers ask.
It's a challenging one to answer, because it's so open-ended. It's
sort of like someone asking, "Can you give me a recipe for dinner?"
The obvious follow-up question would be, "What type of dinner did you
have in mind?"

Here are some thought questions to clarify intent:

* Do you need an agent for people or institutions (or an IoT thing)?
* Will the agent run on a mobile device, in a cloud, on a server,
  or elsewhere?
* Will the agent be on and connected to the internet constantly, or
  will it run only from time to time?
* Which protocols should your agent implement? (In other words, what
  sort of work do you want to delegate to it?)
* Will your agent talk, listen, or both? What channels/transports
  will it use?
* What interesting requirements does your agent have with respect to
  security, privacy, scale, and performance?

#### General Patterns

We said it's hard to provide a recipe for an agent without specifics.
However, the majority of agents _do_ have two things in common:
they listen to and process A2A messages, and they use a [wallet](
https://github.com/hyperledger/indy-hipe/blob/master/text/0013-wallets/README.md)
to manage keys, credentials, and other sensitive material. Unless you have
uses cases that involve IoT, cron jobs, or web hooks, your agent is
likely to fit this mold.

The heart of such an agent is probably a messaging handling
loop, with pluggable protocols to give it new capabilities, and
pluggable transports to let it talk in different ways. The
pseudocode for its main function might look like this:

###### Pseudocode for main()
```
1  While not done:
2      Get next message.
3      Verify it (decrypt, identify sender, check signature...).
3      Look at the type of the plaintext message.
4      Find a plugged in protocol handler that matches that type.
5      Give plaintext message and security metadata to handler.
```

Line 2 can be done via standard HTTP dispatch, or by checking
an email inbox, or in many other ways. Line 3 can be quite
sophisticated--the sender will not be Alice, but rather one of
the agents that she has authorized. Verification may involve
consulting cached information and/or a blockchain where
a DID and DID Doc are stored, among other things.

The pseudocode for each protocol handler it loads might look like:

###### Pseudocode for protocol handler
```
1  Check authorization against metadata. Reject if needed.
2  Read message header. Is it part of an ongoing interaction?
3  If yes, load persisted state.
4  Process the message and update interaction state.
5  If a response is appropriate:
6      Prepare response content.
7      Ask my outbound comm module to package and send it.
```

Line 4 is the workhorse. For example, if the interaction is
about issuing credentials and this agent is doing the issuance,
this would be where it looks up the material for the credential
in internal databases, formats it appopriately, and records the
fact that the credential has now been built. Line 6 might be
where that credential is attached to an outgoing message for
transmission to the recipient.

The pseudocode for the outbound communication module might be:

###### Pseudocode for outbound
```
1  Iterate through all pluggable transports to find best one to use
     with the intended recipient.
2  Figure out how to route the message over the selected transport.
3  Serialize the message content and encrypt it appropriately.
4  Send the message.
```

Line 2 can be complex. It involves looking up one or more endpoints
in the DID Doc of the recipient, and finding an intersection
between transports they use, and transports the sender can
speak. Line 3 requires the keys of the sender, which would
normally be held in a [wallet](
https://github.com/hyperledger/indy-hipe/blob/master/text/0013-wallets/README.md).

If you are building this sort of code using Aries technology, you
will certainly want to use [Aries Agent SDK](
https://github.com/hyperledger/indy-sdk/blob/master/README.md).
This gives you a ready-made,
highly secure wallet that can be adapted to many requirements.
It also provides easy functions to serialize and encrypt. Many
of the operations you need to do are demonstrated in the SDK's
[/doc/how-tos folder](
https://github.com/hyperledger/indy-sdk/blob/master/docs/how-tos/README.md),
or in its Getting Started Guide.

#### How to Learn More

* Hang out and ask questions on `#indy-agent` on [chat.hyperledger.org](https://chat.hyperledger.org).
* Use the mailing list: [hyperledger-indy@lists.hyperledger.org](mailto:hyperledger-indy@lists.hyperledger.org)
* Study the reference agents and agent test suite in the [indy-agent repo on github.com](https://github.com/hyperledger/indy-agent). 
* Study the sample mobile agent at [github.com/sovrin-foundation/connector-app](https://github.com/sovrin-foundation/connector-app).
* Browse other [RFCs](../../index.md).
* Attend the Aries working group on Wednesdays. (See [HL community calendar](https://wiki.hyperledger.org/display/HYP/Calendar+of+Public+Meetings) for details; note that the default timezone is GMT.)
* Review [this slide deck](
  https://docs.google.com/presentation/d/1w_5yf08wfqV0Z-WJLqE5Nh_IVgcMACLWyNw0XjrgTVI/edit)
  about integrating agents with familiar web development paradigms. 

## Reference
[reference]: #reference

#### Categorizing Agents

Agents can be categorized in various ways, and these categories
lead to terms you're likely to encounter in RFCs and other
documentation. Understanding the categories will help the
definitions make sense.

##### By Trust

A __trustable agent__ runs in an environment
that's under the direct control of its owner; the owner can
trust it without incurring much risk. A __semi-trustable
agent__ runs in an environment where others besides the owner
may have access, so giving it crucial secrets is less advisable.
(An untrustable delegate should never be an agent, by definition,
so we don't use that term.)

Note that these distinctions highlight what is _advisable_, not
how much trust the owner actually extends.

##### By Location

Two related but deprecated terms are __edge agent__ and
__cloud agent__. You will probably hear these terms in the
community or read them in docs. The problem with them is that
they suggest location, but were formally defined to imply levels of
trust. When they were chosen, location and levels of trust were
seen as going together--you trust your edge more, and your cloud
less. We've since realized that a trustable agent could exist in
the cloud, if it is directly controlled by the owner, and a
semi-trustable agent could be on-prem, if the owner's control
is indirect. Thus we are trying to correct usage and make "edge"
and "cloud" about location instead.

##### By Platform

* Mobile -- likely _trustable_
* Workstation -- likely _trustable_
* Server -- could be _trustable_ or _semi-trustable_
* Embedded -- _trustable_ or _semi-trustable_
* Browser (web assembly or javascript) -- likely _semi-trustable_
* Blockchain (embodied in smart contract -- trustable?)
* Mesh (IoT…)
* Paper?

##### By Complexity

We can arrange agents on a continuum, from simple to complex.
The simplest agents are __static__--they are preconfigured for
a single relationship. __Thin__ agents are somewhat fancier.
__Thick__ agents are fancier still, and __rich__ agents exhibit
the most sophistication and flexibility:

![agents by complexity](agents-by-complexity.png)

A nice visualization of several dimensions of agent category
has been built by Michael Herman:

[![agent matrix](https://raw.githubusercontent.com/mwherman2000/indy-arm/master/images/HBB-SSI-Agents%20v0.8.png)](
https://github.com/mwherman2000/indy-arm)

#### The Agent-ness Continuum

The tutorial above gives [three essential characteristics of
agents](#essential-characteristics), and lists some [canonical
examples](#canonical-examples). This may make it feel like
agent-ness is pretty binary. However, we've
learned that reality is more fuzzy.

Having a tight definition of an agent may not matter in all
cases. However, it is important when we are trying to understand
interoperability goals. We want agents to be able to interact
with one another. Does that mean they must interact with every
piece of software that is even marginally agent-like? Probably
not.

Some attributes that are not technically necessary in agents
include:

* Has a wallet _(common, but not universal)_
* Establishes new connections _(some may use only a small set of preconfigured connections)_
* Exchanges credentials and proofs _(some may not use these protocols)_
* Both listens and talks _(some may only listen or only talks)_

Agents that lack these characteristics can still be fully
interoperable.

Some interesting examples of less prototypical agents or
agent-like things include:

###### Identity Wallets
"Identity wallet" is a term that's [carefully defined](
https://github.com/hyperledger/indy-hipe/blob/master/text/0013-wallets/README.md#what-is-an-identity-wallet)
in our ecosystem, and in strict, technical usage it maps to a
concept much closer to "database" than "agent". This is because
it is an inert storage container, not an active interacter. However, in
casual usage, it may mean the software that uses a wallet to
do identity work--in which case it is definitely an agent.
 
###### Crypto Wallets
Cryptocurrency wallets are quite agent-like in that they hold
keys and represent a user. However, they diverge from the agent
definition in that they talk proprietary protocols to
blockchains, rather than A2A to other agents.

###### DIF Hubs
A [DIF Identity Hub](https://github.com/decentralized-identity/identity-hub/blob/master/explainer.md)
is an agent-like construct that focuses on the data-sharing aspects of identity.
Currently DIF Hubs do not use the protocols known to the Indy
community, and vice versa. However, there are efforts to bridge
that gap.

###### uPort
The [uPort app](https://www.uport.me/) is an edge agent. Here,
too, there are efforts to bridge a protocol gap.

###### Learning Machine
The credential issuance technology offered by [Learning Machine](
https://www.learningmachine.com/), and the app used
to share those credentials, are agents of institutions and
individuals, respectively. Again, there is a protocol gap to
bridge.

###### Cron Jobs
A cron job that runs once a night at Faber, scanning a database
and revoking credentials that have changes status during the day,
is an agent for Faber. This is true even though it doesn't listen
for incoming messages (it only talks [revocation protocol](
https://github.com/hyperledger/indy-hipe/tree/master/text/0011-cred-revocation) to the ledger). In order to
talk that protocol, it must hold keys delegated by Faber, and it
is surely Faber's fiduciary.

###### Operating Systems
The operating system on a laptop could be described as agent-like,
in that it works for a single owner and may have a keystore.
However, it doesn't talk A2A to other agents--at least not yet.
(OSes that service multiple users fit the definition less.)

###### Devices
A device can be thought of as an agent (e.g., Alice's phone as
an edge agent). However, strictly speaking, one device might
run multiple agents, so this is only casually correct.

###### Sovrin MainNet
The [Sovrin](https://sovrin.org) MainNet can be thought of
as an agent for the Sovrin community (but NOT the Sovrin
Foundation, which codifies the rules but leaves operation of
the network to its stewards). Certainly, the blockchain holds
keys, uses A2A protocols, and acts in a fiduciary capacity
toward the community to further its interests. The only challenge with this
perspective is that the Sovrin community has a very fuzzy
identity.

###### Validators
Validator nodes on a particular blockchain are agents of the stewards
that operate them.

###### Digital Assistants
Digital assistants like Alexa and Google Home are
somewhat agent-like. However, the Alexa in the home of the Jones family is probably not an agent for
either the Jones family or Amazon. It accepts delegated work from
anybody who talks to it (instead of a single controlling identity),
and all current implementations are totally antithetical to the
ethos of privacy and security required by self-sovereign identity.
Although it interfaces with Amazon to download data and features,
it isn't Amazon's fiduciary, either. It doesn't hold keys that allow
it to represent its owner. The protocols it uses are not interactions
with other agents, but with non-agent entities. Perhaps agents
and digtal assistants will converge in the future.

###### Doorbell
An doorbell that emits a simple signal each time it is pressed is
not an agent. It doesn't represent a fiduciary or hold keys. (However,
a fancy IoT doorbell that reports to Alice's mobile agent using an
A2A protocol _would_ be an agent.)

###### Microservices
A microservice run by AcmeCorp to integrate with its vendors is
not an agent for Acme's vendors. Depending on whether it holds
keys and uses A2A protocols, it may or may not be an agent
for Acme.

###### Human Delegates
A human delegate who proves empowerment through keys might be
thought of as an agent.

###### Paper
The keys for an agent can be stored on paper. This storage
basically constitutes a wallet. It isn't an agent. However, it can
be thought of as playing the role of an agent in some cases when
designing backup and recovery solutions.

## Prior art
[prior-art]: #prior-art

* [Alan Kay, the recipient of a Turing Award and the coiner of the
term "Object-Oriented Programming", has emphasized the value of
message-passing architectures in numerous places](
http://userpage.fu-berlin.de/~ram/pub/pub_jf47ht81Ht/doc_kay_oop_en).
What he called "objects" are conceptually similar to what we are
calling "agents." Not surprisingly, the agent ecosystem echoes
some aspects of the design of SmallTalk, Objective-C, Erlang
Actors, Akka Actors, and similar approaches.
* The design of the web includes the concept of browsers and
similar tech, and refers to them as "user agents" in various
RFCs. These are not true SSI agents, but they provide an
example of ubiquitous helper tech that is the forerunner of
the agents described here.
