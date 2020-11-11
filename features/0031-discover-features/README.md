# Aries RFC 0031: Discover Features Protocol 1.0

- Authors: Daniel Hardman
- Status: [ACCEPTED](/README.md#accepted) (may be RETIRED when [v2.0](README.md) of the protocol has enough gravitas)
- Since: 2019-05-01
- Status Note: One of our earliest DIDComm protocols; reached FCP (standards track) status in Indy, and implemented in at least two codebases there. Converted to an Aries RFC Implemented in a handful of Aries codebases. With the advent of DIDComm v2 at DIF, it became clear that we wanted to discover features beyond just protocol support, so this version of the protocol is now superseded by [v2.0 in RFC 0557](../0557-discover-features-v2/README.md).
- Supersedes: [Indy HIPE PR #73](https://github.com/hyperledger/indy-hipe/pull/73).
- Start Date: 2018-12-17
- Tags: [feature](/tags.md#feature), [protocol](/tags.md#protocol), [test-anomaly](/tags.md#test-anomaly)

## Summary

Describes how agents can query one another to discover which features
it supports, and to what extent.

## Motivation

Though some agents will support just one protocol and will be
statically configured to interact with just one other party, many
exciting uses of agents are more dynamic and unpredictable. When
Alice and Bob meet, they won't know in advance which features are
supported by one another's agents. They need a way to find out.

## Tutorial

This RFC introduces a protocol for discussing the protocols an agent
can handle. The identifier for the message family used by this protocol is
`discover-features`, and the fully qualified URI for its definition is:

    https://didcomm.org/discover-features/1.0
    
>This protocol is now superseded by [v2.0 in RFC 0557](../0557-discover-features-v2/README.md). Prefer the new version where practical.  

### Roles

There are two roles in the `discover-features` protocol: `requester` and
`responder`. The requester asks the responder about the protocols it
supports, and the responder answers. Each role uses a single message type.

### States

This is a classic two-step request~response interaction, so it uses the
predefined state machines for any `requester` and `responder`:

[![state machines](state-machines.png)](https://docs.google.com/spreadsheets/d/1smY8qhG1qqGs0NH9g2hV4b7mDqrM6MIsmNI93tor2qk/edit)

### Messages

##### `query` Message Type

A `discover-features/query` message looks like this:

```json
{
  "@type": "https://didcomm.org/discover-features/1.0/query",
  "@id": "yWd8wfYzhmuXX3hmLNaV5bVbAjbWaU",
  "query": "https://didcomm.org/tictactoe/1.*",
  "comment": "I'm wondering if we can play tic-tac-toe..."
}
```

Query messages say, "Please tell me what your capabilities are with
respect to the protocols that match this string." This particular example
asks if another agent knows any 1.x versions of the [tictactoe protocol](
../../concepts/0003-protocols/tictactoe/README.md
).

The `query` field may use the * wildcard. By itself, a query with just
the wildcard says, "I'm interested in anything you want to share with
me." But usually, this wildcard will be to match a prefix that's a little
more specific, as in the example that matches any 1.x version.

Any agent may send another agent this message type at any time.
Implementers of agents that intend to support dynamic relationships
and rich features are *strongly* encouraged to implement support
for this message, as it is likely to be among the first messages
exchanged with a stranger.

##### `disclose` Message Type

A `discover-features/disclose` message looks like this:

```json
{
  "@type": "https://didcomm.org/discover-features/1.0/disclose",
  "~thread": { "thid": "yWd8wfYzhmuXX3hmLNaV5bVbAjbWaU" },
  "protocols": [
    {
      "pid": "https://didcomm.org/tictactoe/1.0",
      "roles": ["player"]
    }
  ]
}
```

The `protocols` field is a JSON array of __protocol support descriptor__
objects that match the query. Each descriptor has a `pid` that contains
a protocol version (fully qualified message family identifier such as
`https://didcomm.org/tictactoe/1.0`), plus a `roles`
array that enumerates the roles the responding agent
can play in the associated protocol.

Response messages say, "Here are some protocols I support that matched
your query, and some things I can do with each one."

##### Sparse Responses

Responses do not have to contain exhaustive detail. For example, the following
response is probably just as good:

```json
{
  "@type": "https://didcomm.org/discover-features/1.0/disclose",
  "~thread": { "thid": "yWd8wfYzhmuXX3hmLNaV5bVbAjbWaU" },
  "protocols": [
    {"pid": "https://didcomm.org/tictactoe/1.0"}
  ]
}
```

The reason why less detail probably suffices is that agents do not need to
know everything about one another's implementations in order to start an
interaction--usually the flow will organically reveal what's needed. For
example, the `outcome` message in the `tictactoe` protocol isn't needed
until the end, and is optional anyway. Alice can start a tictactoe game
with Bob and will eventually see whether he has the right idea about
`outcome` messages.

The missing `roles` in this response does not say, "I support no roles
in this protocol." It says, "I support the protocol but
I'm providing no detail about specific roles."

Even an empty `protocols` map does not say, "I support no protocols
that match your query." It says, "I'm not telling you that I support any
protocols that match your query." An agent might not tell another that
it supports a protocol for various reasons, including: the trust that
it imputes to the other party based on cumulative interactions so far,
whether it's in the middle of upgrading a plugin, whether it's currently
under high load, and so forth. And responses to a `discover-features` request are
not guaranteed to be true forever; agents can be upgraded or downgraded,
although they probably won't churn in their protocol support from moment
to moment.

### Privacy Considerations

Because the regex in a `request` message can be very inclusive, the `discover-features`
protocol could be used to mine information suitable for agent fingerprinting,
in much the same way that browser fingerprinting works. This is antithetical
to the ethos of our ecosystem, and represents bad behavior. Agents should
use `discover-features` to answer legitimate questions, and not to build detailed
profiles of one another. However, fingerprinting may be attempted
anyway.

For agents that want to maintain privacy, several best practices are
recommended:

##### Follow selective disclosure.

Only reveal supported features based on trust in the relationship.
Even if you support a protocol, you may not wish to use it in
every relationship. Don't tell others about protocols you do
not plan to use with them.

Patterns are easier to see in larger data samples. However, a pattern
of ultra-minimal data is also a problem, so use good judgment about
how forthcoming to be.

##### Vary the format of responses.

Sometimes, you might prettify your agent plaintext message one way,
sometimes another.

##### Vary the order of items in the `protocols` array.

If more than one key matches a query, do not always return them in
alphabetical order or version order. If you do return them in order,
do not always return them in ascending order.

##### Consider adding some spurious details.

If a query could match multiple message families, then occasionally
you might add some made-up message family names as matches. If a regex
allows multiple versions of a protocol, then sometimes you might use some
made-up *versions*. And sometimes not. (Doing this too aggressively
might reveal your agent implementation, so use sparingly.)

##### Vary how you query, too.

How you ask questions may also be fingerprintable.

## Reference

### Localization

The `query` message contains a `comment` field that is localizable.
This field is optional and may not be often used, but when it is,
it is to provide a human-friendly justification for the query. An
agent that consults its master before answering a query could present
the content of this field as an explanation of the request.

All message types in this family thus have the following implicit
decorator:

```json
{

  "~l10n": {
    "locales": { "en": ["comment"] },
    "catalogs": ["https://github.com/hyperledger/aries-rfcs/blob/a9ad499/features/0031-discover-features/catalog.json"]
  }

}
```

### Message Catalog

As shown in the above `~l10n` decorator, all agents using this protocol have
[a simple message catalog](catalog.json) in scope. This allows agents to
send [`problem-report`s](
../0035-report-problem/README.md#the-problem-report-message-type
) to complain about something related to `discover-features` issues.
The catalog looks like this (see [catalog.json](catalog.json)):

```json
{
  "query-too-intrusive": {
    "en": "Protocol query asked me to reveal too much information."
  }
}

```

For more information, see the [localization RFC](../0043-l10n/README.md).

## Unresolved questions

- Do we want to support the discovery of features that are not protocol-related?

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

Name / Link | Implementation Notes
--- | ---
[Streetcred.id](https://streetcred.id/) | Commercial mobile and web app built using Aries Framework - .NET [MISSING test results](/tags.md#test-anomaly)
[Aries Protocol Test Suite](https://github.com/hyperledger/aries-protocol-test-suite) |
