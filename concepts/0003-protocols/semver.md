### Semver Rules for Protocols

[Semver](https://semver.org) rules apply to protocols, with the version of a protocol is expressed
in the `semver` portion of its [identifying URI](#message-type-and-protocol-identifier-uris).
The ["ingredients"](#ingredients) of a protocol combine to form a
[public API in the semver sense](https://semver.org/#spec-item-1). Core Aries protocols
specify only major and minor elements in a version; the patch component is not used. Non-core
protocols may choose to use the patch element.

The major and minor versions of protocols match semver semantics:

- Clarification updates that do not change the "public API" of the protocol can be made
with community support _without_ changing the minor version of the protocol.
- An individual message type can add new optional fields, or deprecate
existing fields, [with only a change to its protocol's minor
version](https://semver.org/#spec-item-7). Similarly, a protocol can
add new or deprecate message types with only a change to the minor version.
- Changes that remove fields or message types, that make formerly optional
things required, or that alter the state machine in incompatible
ways, must result in an [increase of the major version of the protocol/primary
message family](https://semver.org/#spec-item-8).

Within a given major version of a protocol, an agent should:

- respond to a minimum supported minor version, defaulting to "0"
- respond with or initiate a protocol instance the current fully supported minor version

This leads to the following received message handling rules:

- message types received with a minor versions below the minimum may be answered with a `report-problem` message with code `version-not-supported`
- message types received with a minor version at or higher than the minimum supported and less than the current minor version are processed, ideally with a response using the same minor version of the received message
  - The recipient may want to send a warning `report-problem` message with code `version-with-degraded-features`
- message types received with a minor version higher than the current minor version are processed with any unrecognized fields ignored
  - The recipient may want to send a warning `report-problem` message with code `fields-ignored-due-to-version-mismatch` 

As documented in the semver documentation, these requirements are not applied when
major version 0 is used. In that case, minor version increments are considered breaking.

Agents may support multiple major versions and select which major version to
use when initiating an instance of the protocol.

An agent should reject messages from protocols or unsupported protocol major versions with
a `report-problem` message with code `version-not-supported`. Agents that receive such a
`report-problem` message may use the [discover features protocol](../../features/0031-discover-features/README.md)
to resolve the mismatch.

### Semver Examples

#### Initiator

Unless Alice's agent (the initiator of a protocol) knows from prior history
that it should do something different, it should begin a protocol using the
highest version number that it supports. For example, if A.1
supports versions 2.0 through 2.2 of protocol X, it should use 2.2 as the
version in the message type of its first message.

#### Recipient Rules

Agents for Bob (the recipient) should reject messages from protocols with major
versions different from those they support. For major version 0, they should also
reject protocols with minor versions they don't support, since semver stipulates
that [features are not stable before 1.0](https://semver.org/#spec-item-4). For
example, if B.1 supports only versions 2.0 and 2.1 of protocol X, it should reject
any messages from version 3 or version 1 or 0. In most cases, rejecting a message
means sending a `problem-report` that the message is unsupported. The `code` field
in such messages should be `version-not-supported`. Agents that receive such a
`problem-report` can then use the [Discover Features Protocol](
../../features/0031-discover-features/README.md) to resolve version problems.

Recipient agents should accept messages that differ from their own supported version
of a protocol only in the patch, prerelease, and/or build fields, whether these
differences make the message earlier or later than the version the recipient prefers.
These messages will be robustly compatible.

For major version >= 1, recipients should also accept messages that differ only in that
the message's minor version is earlier than their own preference. In such a case, the
recipient should degrade gracefully to use the earlier version of the protocol. If the
earlier version lacks important features, the recipient may optionally choose to send,
in addition to a response, a `problem-report` with code `version-with-degraded-features`.

If a recipient supports protocol X version 1.0, it should tentatively
accept messages with later minor versions (e.g., 1.2). Message types that
differ in only in minor version are guaranteed to be compatible *for the
feature set of the earlier version*. That is, a 1.0-capable agent can support
1.0 features using a 1.2 message, though of course it will lose any features
that 1.2 added. Thus, accepting such a message could have two possible outcomes:

1. The message at version 1.2 might look and behave exactly like it did at version
1.0, in which case the message will process without any trouble.

2. The message might contain some fields that are unrecognized and need to be ignored.

In case 2, it is best practice for the recipient to send a `problem-report` that
is a *warning*, not an *error*, announcing that some fields could not be processed
(code = `fields-ignored-due-to-version-mismatch`). Such a message is *in addition
to* any response that the protocol demands of the recipient.

If the recipient of a protocol's initial message generates a response, the response
should use the latest major.minor protocol version that both parties support and
know about. Generally, all messages after the first use only major.minor

[![version negotiation matrix](version-negotiation-matrix.png)](
https://docs.google.com/spreadsheets/d/1W5KYOqCCqmTeU4Z7XZQH9_6_0TeP5Vf5TtsOZmioyB0/edit#gid=0)
