# 0302: Aries Stable

* Authors: [Stephen Curran](mailto:swcurran@cloudcompass.ca), [John Jordan](mailto:john.jordan@gov.bc.ca)
* Status: [PROPOSED](https://github.com/hyperledger/aries-rfcs/blob/master/README.md#proposed)
* Since: 2019-11-09
* Status Note: This RFC proposes an Aries Stable process and Aries Stable v1.0.0
* Supersedes:
* Start Date: 2018-11-06
* Tags: concept

## Summary

This RFC defines the process for the community of Aries agent builders to 

* enumerate a versioned set of Aries concept and feature RFCs which are collectively referred to as ‘Aries Stable Vx.y.z’
* track Aries Stable versions.

"Agent builders" are organizations or teams that are developing open source code upon which agents can be built (e.g. [aries-framework-dotnet](https://github.com/hyperledger/aries-framework-dotnet)), or deployable agents (e.g. [OSMA Mobile App](https://github.com/mattrglobal/osma)), or commercially available agents.

An Aries Stable version provides a clearly defined set of RFCs for Aries agent builders to target their agent implementation when they wish it to be interoperable with other agents supporting the same Aries Stable version. The Aries Stable versioning process is intended to provide clarity and predictability for Aries agent builders and others in the broader Aries community. The process is not concerned with proposing new, or evolving existing, RFCs, nor with the development of Aries code bases.

At all times, the [Reference](#reference) section of this RFC defines one or more current Aries Stable versions -- a number and set of links to specific commits of concept and features RFCs, along with a list of all previous Aries Stable versions. Several Aries Stable versions can coexist during periods when multiple major Aries Stable versions are in active use (e.g. 1.x.x and 2.x.x). Each entry in the previous versions list includes a link to the commit of this RFC associated with that Aries Stable version.

Once a suitably populated Aries test suite is available, each Aries Stable version will include a link to the relevant subset of test cases. The test cases will include only those targeting the specific versions of the concepts and features RFCs in that version of Aries Stable. A process for maintaining the link between the Aries Stable version and the test cases will be defined in this RFC once the Aries test suite is further evolved.

This RFC includes a [section](#aries-agent-builders-and-agents) maintained by Aries agent builders listing their Aries agents or agent deployments (whether open or closed source). This list SHOULD include the following information for each listed agent:

* The name, version and link to the agent (code or deployment)
* The name and link to the builder(s)
* The version of Aries Stable supported
* A link to the test suite results
* Notes about the agent

An Aries agent builder SHOULD include an entry in the table per major version supported.

## Motivation

The establishment of Aries Stable versions defined by the Aries agent builder community allows the independent creation of interoperable Aries agents by different Aries agent builders. Whether building open or closed source implementations, an agent that aligns with the set of RFC versions listed as part of an Aries Stable version should be interoperable with any other agent built to align with that same version.

## Tutorial

This RFC MUST contain the current Aries Stable versions as defined by a version number and a set of links to concept and feature RFCs which have been agreed to by a community of Aries agent builders. "Agreement" is defined as when the community agrees to merge a Pull Request (PR) to this RFC that affects an Aries Stable version number and/or any of the links to concept and feature RFCs. PRs that do not impact the Aries Stable version number or links can (in general) be merged with less community scrutiny.

Each link to a concept or feature RFCs MUST be to a specific commit of that RFC. RFCs in the list MAY be flagged as deprecated.

Aries Stable versions SHOULD have a link (or links) to a version (specific commit) of a test suite (or test cases) which SHOULD be used to verify compliance with the corresponding version of Aries Stable. Aries agent builders MAY self-report their test results as part of their entries in the list of agents.

Aries Stable versions MUST evolve at a pace determined by the Aries agent builder community. This pace SHOULD be at a regular time interval so as to facilitate the independent but interoperable release of Aries Agents. Aries agent builders are encouraged to propose either updates to the list of RFCs supported by Aries Stable through GitHub Issues or via a Pull Request. Such updates MAY trigger a change in the Aries Stable version number.

All previous versions of Aries Stable MUST be listed in the [Previous Versions](#previous-versions) section of the RFP and must include a link to the latest commit of this RFC at the time that version was active.

## Reference

The Aries Stable version number and links to other RFCs in this section SHOULD only be updated with the agreement of the Aries agent builder community. There MAY be multiple active major Aries Stable versions. A list of previous versiins of Aries Stable are [listed after](#previous-versions) the current version(s).

### Aries Stable Version: 1.0.0

The initial version of Aries Stable, based on the existing implementations such as [aries-cloudagent-python](https://github.com/hyperledger/aries-cloudagent-python), [aries-framework-dotnet](https://github.com/hyperledger/aries-framework-dotnet), [Open Source Mobile Agent](https://github.com/mattrglobal/osma) and [Streetcred.id](https://streetcred.id)'s IOS agent.

> To Do - community evolution of this list until we agree on Aries 1.0.0.

#### Supported Aries RFC Concepts

* [0003-protocols](https://github.com/hyperledger/aries-rfcs/tree/64e5e55c123b2efaf38f4b0911a71a1c40a7f29d/concepts/0003-protocols)
* [0004-agents](https://github.com/hyperledger/aries-rfcs/tree/64e5e55c123b2efaf38f4b0911a71a1c40a7f29d/concepts/0004-agents)
* [0005-didcomm](https://github.com/hyperledger/aries-rfcs/tree/64e5e55c123b2efaf38f4b0911a71a1c40a7f29d/concepts/0005-didcomm)
* [0008-message-id-and-threading](https://github.com/hyperledger/aries-rfcs/tree/64e5e55c123b2efaf38f4b0911a71a1c40a7f29d/concepts/0008-message-id-and-threading)
* [0011-decorators](https://github.com/hyperledger/aries-rfcs/tree/64e5e55c123b2efaf38f4b0911a71a1c40a7f29d/concepts/0011-decorators)
* [0017-attachments](https://github.com/hyperledger/aries-rfcs/tree/64e5e55c123b2efaf38f4b0911a71a1c40a7f29d/concepts/0017-attachments)
* [0020-message-types](https://github.com/hyperledger/aries-rfcs/tree/64e5e55c123b2efaf38f4b0911a71a1c40a7f29d/concepts/0020-message-types)
* [0046-mediators-and-relays](https://github.com/hyperledger/aries-rfcs/tree/64e5e55c123b2efaf38f4b0911a71a1c40a7f29d/concepts/0046-mediators-and-relays)
* [0047-json-LD-compatibility](https://github.com/hyperledger/aries-rfcs/tree/64e5e55c123b2efaf38f4b0911a71a1c40a7f29d/concepts/0047-json-ld-compatibility)
* [0050-wallets](https://github.com/hyperledger/aries-rfcs/tree/64e5e55c123b2efaf38f4b0911a71a1c40a7f29d/concepts/0050-wallets)
* [0094-cross-domain messaging](https://github.com/hyperledger/aries-rfcs/tree/64e5e55c123b2efaf38f4b0911a71a1c40a7f29d/concepts/0094-cross-domain-messaging)

#### Supported Aries RFC Features

* [0019-encryption-envelope](https://github.com/hyperledger/aries-rfcs/tree/64e5e55c123b2efaf38f4b0911a71a1c40a7f29d/features/0019-encryption-envelope)
* [0160-connection-protocol](https://github.com/hyperledger/aries-rfcs/tree/64e5e55c123b2efaf38f4b0911a71a1c40a7f29d/features/0160-connection-protocol)
* [0035-didcomm-transports](https://github.com/hyperledger/aries-rfcs/tree/64e5e55c123b2efaf38f4b0911a71a1c40a7f29d/features/0025-didcomm-transports)
* [0031-discover-features](https://github.com/hyperledger/aries-rfcs/tree/64e5e55c123b2efaf38f4b0911a71a1c40a7f29d/features/0031-discover-features)
* [0032-message-timing](https://github.com/hyperledger/aries-rfcs/tree/64e5e55c123b2efaf38f4b0911a71a1c40a7f29d/features/0032-message-timing)
* [0035-report-problem](https://github.com/hyperledger/aries-rfcs/tree/64e5e55c123b2efaf38f4b0911a71a1c40a7f29d/features/0035-report-problem)
* [0036-issue-credential](https://github.com/hyperledger/aries-rfcs/tree/64e5e55c123b2efaf38f4b0911a71a1c40a7f29d/features/0036-issue-credential)
* To Do: Make and link to RFCs for the v0.1 credential exchange (issue and present)
* [0037-present-proof](https://github.com/hyperledger/aries-rfcs/tree/64e5e55c123b2efaf38f4b0911a71a1c40a7f29d/features/0037-present-proof)
* [0048-trust-ping](https://github.com/hyperledger/aries-rfcs/tree/64e5e55c123b2efaf38f4b0911a71a1c40a7f29d/features/0048-trust-ping)
* [0067-didcomm-diddoc-conventions](https://github.com/hyperledger/aries-rfcs/tree/64e5e55c123b2efaf38f4b0911a71a1c40a7f29d/features/0067-didcomm-diddoc-conventions)
* [0092-transport-return-route](https://github.com/hyperledger/aries-rfcs/tree/64e5e55c123b2efaf38f4b0911a71a1c40a7f29d/features/0092-transport-return-route)
* [0095-basic-message](https://github.com/hyperledger/aries-rfcs/tree/64e5e55c123b2efaf38f4b0911a71a1c40a7f29d/features/0095-basic-message)

#### Test Suite

To Do: Link(s) to version(s) of the test suite/test cases applicable to this Aries Stable version.

### Previous Versions

* None

> Will be the version number and a link to the latest commit of this RFC while this version was current.

## Aries Agent Builders and Agents

A list of agents that claim compatibility with versions of Aries Stable. A entry can be included per agent and per major Aries Stable version.

Name / Version / Link | Builder / Link | Aries Stable Version | Test Results | Notes
--- | --- | --- | --- | ---
 |  |  |  | 

## Drawbacks

It may be difficult to agree on the exact list of RFCs to support in a given version.

## Rationale and alternatives

Continuing with the current informal discussions of what agents/frameworks should support and when is an ineffective way of enabling independent building of interoperable agents.

## Prior art

This is a typical approach to creating an early protocol certification program.

## Unresolved questions

* The community agreement process for setting Aries Stable versions needs to be tried and adjusted as appropriate.
* The tracking of who is part of the Aries agent builders community needs to be defined so we know who should have the strongest say in the setting of Aries Stable versions.
* Should the Implementations table in all RFCs (below) be used for the agent builders table (above)?  Or, should we eliminate the per RFC “implementations table (below and in all RFCs) and just use this RFC to track implementations?

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

_Implementation Notes_ [may need to include a link to test results](https://github.com/hyperledger/aries-rfcs/blob/master/README.md#accepted).


Name / Link | Implementation Notes
--- | ---
 |  | 
