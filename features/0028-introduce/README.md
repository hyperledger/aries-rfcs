# Aries RFC 0028: Introduce Protocol 1.0

- Authors: Daniel Hardman, Sam Curren, Stephen Curran, Tobias Looker, George Aristy
- Status: [PROPOSED](/README.md#proposed)
- Since: 2019-04-15
- Status Note: Referenced in some discussions about the peer DID method spec and n-wise DIDs, but not yet implemented.
- Start Date: 2019-03-27
- Tags: [feature](/tags.md#feature), [protocol](/tags.md#protocol)

## Summary

Describes how a go-between can introduce two parties that
it already knows, but that do not know each other.

## Motivation

Introductions are a fundamental activity in human relationships. They allow
us to bootstrap contact information and trust. They are also a source of
virality. We need a standard way to do introductions in an SSI ecosystem,
and it needs to be flexible, secure, privacy-respecting, and well documented.

## Tutorial

### Name and Version

This is the Introduce 1.0 protocol. It is uniquely identified by the URI:

    "https://didcomm.org/introduce/1.0"

### Key Concepts

##### Basic Use Case

Introductions target scenarios like this:

>Alice knows Bob and Carol, and can talk to each of them. She
wants to introduce them in a way that allows a relationship to form.

![scenario diagram](scenario.png)

This use case is worded carefully; it is far more adaptable than it may
appear at first glance. The [Advanced Use Cases](#advanced-use-cases)
section later in the doc explores many variations. But the early part
of this document focuses on the simplest reading of the use case.

##### Goal

When we introduce two friends, we may hope that a new friendship ensues.
But technically, the introduction is complete when we provide the
opportunity for a relationship--what the parties do with that opportunity
is a separate question.

Likewise, the goal of our formal introduction protocol should be crisply
constrained. Alice wants to gather consent and contact information
from Bob and Carol; then she wants to invite them to connect. What they
do with her invitation after that is not under her control, and is outside
the scope of the introduction.

This suggests an important insight about the relationship between the
introduce protocol and the [Out-Of-Band protocols](
../0434-outofband/README.md):
*they overlap*. The invitation to form a relationship, which
begins the Out-Of-Band protocols, is also the final step in an
introduction.

Said differently, *the goal of the introduce protocol is to start the
Out-Of-Band* protocols.

##### Transferring Trust

[TODO: talk about how humans do introductions instead of just introducing
themselves to strangers because it raises trust. Example of Delta Airlines
introducing you to Heathrow Airport; you trust that you're really talking
to Heathrow based on Delta's asertion.]

### Roles

There are three [TODO:do we want to support introducing more than 2 at a time?]
participants in the protocol, but only two roles.

The __introducer__ begins the process and must know the other two parties.
Alice is the introducer in the diagram above. The other two participants
are both __introducees__.

### States

In a successful introduction, the introducer state progresses from
`[start] -> arranging -> delivering -> confirming (optional) -> [done]`. Confirming is accomplished with an ACK to an introducee to let them know that their out-of-band message was forwarded.

Meanwhile, each introducee progresses from `[start] -> deciding -> waiting
-> [done]`.

Of course, errors and optional choices complicate the possibilities. The
full state machine for each party are:

[![state machine matrix](states.png)](https://docs.google.com/spreadsheets/d/1jjLQMCXWCN3nuXUg8mSpJQlzXGlYeo1n0W9yNuYJQLM/edit)

The subtleties are explored in the [Advanced Use Cases](#advanced-use-cases)
section.

### Messages

##### `proposal`

This message informs an introducee that an introducer wants to perform
an introduction, and requests approval to do so. It works the same way
that proposals do in [double-opt-in introductions](
https://avc.com/2009/11/the-double-optin-introduction/) in the
non-agent world:

![sample introduction email](double-opt-in.png)

The DIDComm message looks like this:

```jsonc
{
  "@type": "https://didcomm.org/introduce/1.0/proposal",
  "@id": "df3b699d-3aa9-4fd0-bb67-49594da545bd",
  "to": {
    "name": "Bob"
  }
}
```

The `to` field contains an __introducee descriptor__ that provides
context about the introduction, helping the party receiving the proposal
to evaluate whether they wish to accept it. Depending on how much context
is available between introducer and introducee independent of the formal
proposal message, this can be as simple as a name, or something fancier (see
[Advanced Use Cases](#advanced-use-cases) below).

##### `response`

A standard example of the message that an introducee sends in response
to an introduction proposal would be:

```jsonc
{
  "@type": "https://didcomm.org/introduce/1.0/response",
  "@id": "283e15b5-a3f7-43e7-bac8-b75e4e7a0a25",
  "~thread": {"thid": "df3b699d-3aa9-4fd0-bb67-49594da545bd"},
  "approve": true,
  "oob-message": {
    "@type": "https://didcomm.org/oob-invitation/1.0/invitation",
    "@id": "12345678900987654321",
    "label": "Robert",
    "goal": "To issue a Faber College Graduate credential",
    "goal-code": "issue-vc",
    "protocols": [
      "https://didcomm.org/didexchange/1.0",
      "https://didcomm.org/connections/1.0"
    ],
    "service": ["did:sov:LjgpST2rjsoxYegQDRm7EL"]
  }
}
```

A simpler response, also valid, might look like this:

```jsonc
{
  "@type": "https://didcomm.org/introduce/1.0/response",
  "@id": "283e15b5-a3f7-43e7-bac8-b75e4e7a0a25",
  "~thread": {"thid": "df3b699d-3aa9-4fd0-bb67-49594da545bd"},
  "approve": true
}
```

The difference between the two forms is whether the response contains
a valid out-of-band message (see [RFC 0434](../0434-outofband/README.md)).
Normally, it should--but sometimes, an introducee may not be able to (or may
not want to) share a DIDComm endpoint to facilitate the introduction. In such
cases, the stripped-down variant may be the right choice. See the
[Advanced Use Cases](#advanced-use-cases) section for more details.

At least one of the more complete variants must be received by an
introducer to successfully complete the introduction, because the final step in
the protocol is to begin one of the [Out-Of-Band protocols](../0434-outofband/README.md)
by forwarding the message from one introducee to the other.

###### Note on the ouf-of-band messages

These messages are not a member of the `introductions/1.0` protocol;
they are not even adopted. They belong to the out-of-band protocols, and
are no different from the message that two parties would generate when one
invites the other with no intermediary, except that:

* It is delivered by the introducer, not by either of the introducees.
* It has a `~thread` decorator that identifies the introduction as
its parent thread.
* If introducees already have DIDComm capabilities, it can be delivered over
standard DIDComm channels. If one of the introducees does NOT have a DID-based
channel with the introducer, then the message must be delivered to that
introducee using the non-DIDComm channel. [TODO: is there a way for
the introducer, rather than the other introducee, to "sponsor" the introducee
that needs SSI onboarding?]
* If the message is delivered over a DIDComm channel, it is unusual
in that it is from a party other than the one that owns the channel.

##### `request`

This message asks for an introduction to be made. This message also uses the
`introducee descriptor` block, to tell the potential introducer which
introducee is the object of the sender's interest:

```jsonc
{
  "@type": "https://didcomm.org/introduce/1.0/request",
  "@id": "df3b699d-3aa9-4fd0-bb67-49594da545bd",
  "please_introduce_to": {
    "name": "Carol",
    "description": "The woman who spoke after you at the PTA meeting last night.",
    "expected": true
  },
  "nwise": false,
  "~timing": { "expires_time": "2019-04-23 18:00Z" }
}
```

The recipient can choose whether or not to honor it in their own way, on
their own schedule. However, a `~please_ack` decorator could be used to make
it more interactive, and a `problem_report` could be returned if the
recipient chooses not to honor it.

### Advanced Use Cases

Any of the parties can be an organization or thing instead of a person.

![any identity owner type](any-identity-owner-type.png)

Bob and Carol may actually know each other already, without Alice realizing
it. The introduction may be rejected. It may create a new pairwise
relationship between Bob and Carol that is entirely invisible to Alice.
Or it may create an n-wise relationship in which Alice, Bob, and Carol know
one another by the same identifiers.

Some specific examples follow.

#### One introducee can't do DIDComm

The [Out-Of-Band Protocols]( ../0434-outofband/README.md)
allow the invited party to be onboarded (acquire software and an agent)
as part of the workflow.

![diagram](uneven.png)

Introductions support this use case, too. In such a case, the introducer
sends a standard `proposal` to the introducee that DOES have DIDComm
capabilities, but conveys the equivalent of a `proposal` over a
non-DIDComm channel to the other introducee. The `response` from the
DIDComm-capable introducee must include an out-of-band message with
a deep link for onboarding, and this is sent to the introducee that needs
onboarding.

#### Neither introducee can do DIDComm

In this case, the introducer first goes through onboarding via one of the
Out-Of-Band protocols with one introducee. Once that introducee can do DIDComm,
the previous workflow is used.

#### Introducer doesn't have DIDComm capabilities

This might happen if AliceCorp wants to connect two of its customers.
AliceCorp may not be able to talk to either of its customers over
DIDComm channels, but it doesn't know whether they can talk to each
other that way.

![introducer doesn't have DIDComm capabilities](introducer-no-did.png)

In this case, the introducer conveys the same information that a
`proposal` would contain, using non-DIDComm channels. As long as one
of the introducees sends back some kind of response that includes
approval and an out-of-band message, the message can be
delivered. The entire interaction is DIDComm-less.

#### One introducee has a public DID with a standing invitation

This might happen if Alice wants to introduce Bob to CarolCorp, and
CarolCorp has published a `connection-invitation` for general use.

![public DID, standing invitation](public-invitation.png)

As introducer, Alice simply has to forward CarolCorp's `connection-invitation`
to Bob. No `proposal` message needs to be sent to CarolCorp;
this is the `skip proposal` event shown in the introducer's
state machine.

#### Introducee requests introduction

Alice still acts as the introducer, but Bob now asks Alice to introduce him to a candidate introducee discovered *a priori* with the [`help-me-discover`](../0214-help-me-discover/README.md) protocol:

```jsonc
{
  "@type": "https://didcomm.org/introduce/1.0/request",
  "@id": "df3b699d-3aa9-4fd0-bb67-49594da545bd",
  "please_introduce_to": {
      "discovered": "didcomm:///5f2396b5-d84e-689e-78a1-2fa2248f03e4/.candidates%7B.id+%3D%3D%3D+%22Carol%22%7D"
  },
  "~timing": { "expires_time": "2019-04-23 18:00Z" }
}
```

This `request` message includes a `discovered` property with a [linkable message path](../../concepts/0217-linkable-message-paths/README.md) that uniquely identifies the candidate introducee.

#### Requesting confirmation

[TODO: A field in the `response` where an introducee asks to be notified
that the introduction has been made?]

#### Other stuff

* Using acks to report status of introduction efforts.
* Timeouts.
* Introducing multiple parties at the same time?

[TODO: What if Alice is introducing Bob, a public entity with no connection to
her, to Carol, a private person? Can she just relay Bob's invitation that
he published on his website? Are there security or privacy implications?
What if she is introducing 2 public entities and has a connection to neither?]

## Reference

### `proposal`

In the tutorial narrative, only a simple proposal was presented. A
fancier version might be:

```jsonc
{
  "@type": "https://didcomm.org/introduce/1.0/proposal",
  "@id": "df3b699d-3aa9-4fd0-bb67-49594da545bd",
  "to": {
    "name": "Kaiser Hospital",
    "description": "Where I want to schedule your MRI. NOTE: NOT the one downtown!",
    "description~l10n": { "locale": "en", "es": "Donde se toma el MRI; no en el centro"},
    "where": "@34.0291739,-118.3589892,12z",
    "img~attach": {
      "description": "view from Marina Blvd",
      "mime-type": "image/png",
      "filename": "kaiser_culver_google.jpg",
      "content": {
        "link": "http://bit.ly/2FKkby3",
        "byte_count": 47738,
        "sha256": "cd5f24949f453385c89180207ddb1523640ac8565a214d1d37c4014910a4593e"
      }
    },
    "proposed": false
  },
  "nwise": true,
  "~timing": { "expires_time": "2019-04-23 18:00Z" }
}
```

This adds a number of fields to the introducee descriptor. Each is optional
and may be appropriate in certain circumstances. Most should be self-explanatory,
but the `proposed` field deserves special comment. This tells whether the
described introducee has received a proposal of their own, or will be
introduced without that step.

This example also adds the `nwise` field to the proposal. When `nwise` is
present and its value is `true`, the proposal is to establish an nwise
relationship in which the introducer participates, as opposed to a pairwise
relationship in which only the introducees participate.

[TODO: do we care about having a response signed? Security? MITM?]

### Errors

[TODO: What can go wrong.]

### Localization

[TODO: the `description` field in an introducee descriptor. Error codes/catalog.]

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
into consideration that Indy sometimes intentionally diverges from common
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

Name / Link | Implementation Notes
--- | ---
 |  |
