### Semver Rules for Protocols

[Semver](https://semver.org) rules apply to protocols, with the version of a protocol is expressed
in the `semver` portion of its [identifying URI](#message-type-and-protocol-identifier-uris).
The ["ingredients"](#ingredients) of a protocol combine to form a
[public API in the semver sense](https://semver.org/#spec-item-1). Core Aries protocols
specify only major and minor elements in a version; the patch component is not used.

The major and minor versions of protocols match semvar semantics:

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

- specify a minimum minor version supported, defaulting to "0"
- specify a current minor version that is fully supported and used by default

This leads to the following received message handling rules:

- message types received with a minor versions below the minimum may be answered with a `report-problem` with code `version-not-supported`
- message types received with a minor version at or higher than the minimum supported and less than the current minor version are processed, ideally with a response using the same minor version of the received message
  - The recipient may want to send a warning `report-problem` with code `version-with-degraded-features`
- message types received with a minor version higher than the current minor version are processed with any unrecognized fields ignored
  - The recipient may want to send a warning `report-problem` with code `fields-ignored-due-to-version-mismatch` 

As documented in the semvar documentation, these requirements may not apply when
major version 0 is used. Specific rules associated each v0 protocol are left to
the discretion of the community.

Agents may support multiple major versions and select which major version to
use when initiating an instance of the protocol.

The [discover features](../../features/0031-discover-features/README.md) protocol
can be used by one agent to query the versions of protocols supported by another agent,
informing the selection of which version of a protocol to use in initiating an
instance of a protocol. Agent receiving a discover features request may respond with a list of
preferred protocols they support, as described in that protocol.

An agent should reject messages from protocols or unsupported protocol major versions with
a `report-problem` with code `version-not-supported`. Agents that receive such a
`report-problem` message may use the [discover features protocol](../../features/0031-discover-features/README.md)
to resolve the mismatch.
