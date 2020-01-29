# 0302: Aries Interop Profile

- Authors: [Stephen Curran](mailto:swcurran@cloudcompass.ca), [John Jordan](mailto:john.jordan@gov.bc.ca) Province of British Columbia
- Status: [ACCEPTED](https://github.com/hyperledger/aries-rfcs/blob/master/README.md#accepted)
- Since: 2019-11-09
- Status Note: This RFC proposes an Aries Interop Profile process and Aries Interop Profile v1.0.0
- Supersedes:
- Start Date: 2018-11-06
- Tags: concept

## Summary

This RFC defines the process for the community of Aries agent builders to:

- enumerate a versioned set of Aries concept and feature RFCs which are collectively referred to as 'Aries Interop Profile Vx.y.z'
- track Aries Interop Profile versions.

"Agent builders" are organizations or teams that are developing open source code upon which agents can be built (e.g. [aries-framework-dotnet](https://github.com/hyperledger/aries-framework-dotnet)), or deployable agents (e.g. [OSMA Mobile App](https://github.com/mattrglobal/osma)), or commercially available agents.

An Aries Interop Profile (AIP) version provides a clearly defined set of RFCs for Aries agent builders to target their agent implementation when they wish it to be interoperable with other agents supporting the same Aries Interop Profile version. The Aries Interop Profile versioning process is intended to provide clarity and predictability for Aries agent builders and others in the broader Aries community. The process is not concerned with proposing new, or evolving existing, RFCs, nor with the development of Aries code bases.

At all times, the [Reference](#reference) section of this RFC defines one or more current Aries Interop Profile versions -- a number and set of links to specific commits of concept and features RFCs, along with a list of all previous Aries Interop Profile versions. Several current Aries Interop Profile versions can coexist during periods when multiple major Aries Interop Profile versions are in active use (e.g. 1.x.x and 2.x.x). Each entry in the previous versions list includes a link to the commit of this RFC associated with that Aries Interop Profile version. The [Reference](#reference) section MAY include one "<major>.next" version for each existing current major Aries Interop Profile versions. Such "next" versions are proposals for what is to be included in the next minor/patch AIP version.

Once a suitably populated Aries test suite is available, each Aries Interop Profile version will include a link to the relevant subset of test cases. The test cases will include only those targeting the specific versions of the concepts and features RFCs in that version of Aries Interop Profile. A process for maintaining the link between the Aries Interop Profile version and the test cases will be defined in this RFC once the Aries test suite is further evolved.

This RFC includes a [section](#aries-agent-builders-and-agents) maintained by Aries agent builders listing their Aries agents or agent deployments (whether open or closed source). This list SHOULD include the following information for each listed agent:

- The name, version and link to the agent (code or deployment)
- The type of the agent (see below)
- The name and link to the builder(s)
- The version of Aries Interop Profile supported
- A link to the test suite results or a summary of caveats/details about the agent's AIP support
- Notes about the agent

An Aries agent builder SHOULD include an entry in the table per major version
supported. Until there is a sufficiently rich test suite that produces linkable
results, builders SHOULD link to and maintain a page that summarizes any exceptions and
extensions to the agent's AIP support.

The type of the agent MUST be selected from an enumerated list above the table of builder agents.

## Motivation

The establishment of Aries Interop Profile versions defined by the Aries agent builder community allows the independent creation of interoperable Aries agents by different Aries agent builders. Whether building open or closed source implementations, an agent that aligns with the set of RFC versions listed as part of an Aries Interop Profile version should be interoperable with any other agent built to align with that same version.

## Tutorial

This RFC MUST contain the current Aries Interop Profile versions as defined by a version number and a set of links to concept and feature RFCs which have been agreed to by a community of Aries agent builders. "Agreement" is defined as when the community agrees to merge a Pull Request (PR) to this RFC that affects an Aries Interop Profile version number and/or any of the links to concept and feature RFCs. PRs that do not impact the Aries Interop Profile version number or links can (in general) be merged with less community scrutiny.

Each link to a concept or feature RFCs MUST be to a specific commit of that RFC. RFCs in the list MAY be flagged as deprecated.

Aries Interop Profile versions SHOULD have a link (or links) to a version (specific commit) of a test suite (or test cases) which SHOULD be used to verify compliance with the corresponding version of Aries Interop Profile. Aries agent builders MAY self-report their test results as part of their entries in the list of agents.

Aries Interop Profile versions MUST evolve at a pace determined by the Aries agent builder community. This pace SHOULD be at a regular time interval so as to facilitate the independent but interoperable release of Aries Agents. Aries agent builders are encouraged to propose either updates to the list of RFCs supported by Aries Interop Profile through GitHub Issues or via a Pull Request. Such updates MAY trigger a change in the Aries Interop Profile version number.

All previous versions of Aries Interop Profile MUST be listed in the [Previous Versions](#previous-versions) section of the RFP and must include a link to the latest commit of this RFC at the time that version was active.

A script in the `/code` folder of this repo can be run to list RFCs within an AIP
version that have changed since the AIP version was set. For script usage information
run the following from the root of the repo:

`python code/aipUpdates.py --help`

## Reference

The Aries Interop Profile version number and links to other RFCs in this section SHOULD only be updated with the agreement of the Aries agent builder community. There MAY be multiple active major Aries Interop Profile versions. A list of previous versions of Aries Interop Profile are [listed after](#previous-versions) the current version(s).

### Aries Interop Profile Version: 1.0.0

The initial version of Aries Interop Profile, based on the existing implementations such as [aries-cloudagent-python](https://github.com/hyperledger/aries-cloudagent-python), [aries-framework-dotnet](https://github.com/hyperledger/aries-framework-dotnet), [Open Source Mobile Agent](https://github.com/mattrglobal/osma) and [Streetcred.id](https://streetcred.id)'s IOS agent. Agents adhering to AIP 1.0.0 should be able to establish connections, exchange credentials and complete a connection-less proof-request/proof transaction.

 RFC Type | RFC/Link to RFC Version
--- | ---
Concept | [0003-protocols](https://github.com/hyperledger/aries-rfcs/tree/9b7ab9814f2e7d1108f74aca6f3d2e5d62899473/concepts/0003-protocols)
Concept | [0004-agents](https://github.com/hyperledger/aries-rfcs/tree/f1e420f76abd9ff4af5c15d375fa6cf8c2cacb33/concepts/0004-agents)
Concept | [0005-didcomm](https://github.com/hyperledger/aries-rfcs/tree/f1e420f76abd9ff4af5c15d375fa6cf8c2cacb33/concepts/0005-didcomm)
Concept | [0008-message-id-and-threading](https://github.com/hyperledger/aries-rfcs/tree/64e5e55c123b2efaf38f4b0911a71a1c40a7f29d/concepts/0008-message-id-and-threading)
Concept | [0011-decorators](https://github.com/hyperledger/aries-rfcs/tree/965a975f953d72e370d2b6fb28eec538ec756c6d/concepts/0011-decorators)
Concept | [0017-attachments](https://github.com/hyperledger/aries-rfcs/tree/64e5e55c123b2efaf38f4b0911a71a1c40a7f29d/concepts/0017-attachments)
Concept | [0020-message-types](https://github.com/hyperledger/aries-rfcs/tree/64e5e55c123b2efaf38f4b0911a71a1c40a7f29d/concepts/0020-message-types)
Concept | [0046-mediators-and-relays](https://github.com/hyperledger/aries-rfcs/tree/64e5e55c123b2efaf38f4b0911a71a1c40a7f29d/concepts/0046-mediators-and-relays)
Concept | [0047-json-LD-compatibility](https://github.com/hyperledger/aries-rfcs/tree/53c2e7accc8394c9c7b09563c0eec3c564c133c6/concepts/0047-json-ld-compatibility)
Concept | [0050-wallets](https://github.com/hyperledger/aries-rfcs/tree/64e5e55c123b2efaf38f4b0911a71a1c40a7f29d/concepts/0050-wallets)
Concept | [0094-cross-domain messaging](https://github.com/hyperledger/aries-rfcs/tree/64e5e55c123b2efaf38f4b0911a71a1c40a7f29d/concepts/0094-cross-domain-messaging)
Feature | [0015-acks](https://github.com/hyperledger/aries-rfcs/tree/5cc750f0fe18e3918401489066566f22474e25a8/features/0015-acks)
Feature | [0019-encryption-envelope](https://github.com/hyperledger/aries-rfcs/tree/9b0aaa39df7e8bd434126c4b33c097aae78d65bf/features/0019-encryption-envelope)
Feature | [0160-connection-protocol](https://github.com/hyperledger/aries-rfcs/tree/9b0aaa39df7e8bd434126c4b33c097aae78d65bf/features/0160-connection-protocol)
Feature | [0025-didcomm-transports](https://github.com/hyperledger/aries-rfcs/tree/b490ebe492985e1be9804fc0763119238b2e51ab/features/0025-didcomm-transports)
Feature | [0035-report-problem](https://github.com/hyperledger/aries-rfcs/tree/89d14c15ab35b667e7a9d04fe42d4d48b10468cf/features/0035-report-problem)
Feature | [0036-issue-credential](https://github.com/hyperledger/aries-rfcs/tree/bb42a6c35e0d5543718fb36dd099551ab192f7b0/features/0036-issue-credential)
Feature | [0037-present-proof](https://github.com/hyperledger/aries-rfcs/tree/3d378a9bec123a64bc59d7eeaf0499aa5e704222/features/0037-present-proof)
Feature | [0056-service-decorator](https://github.com/hyperledger/aries-rfcs/tree/527849ec3aa2a8fd47a7bb6c57f918ff8bcb5e8c/features/0056-service-decorator)

#### Test Suite

> To Do: Link(s) to version(s) of the test suite/test cases applicable to this Aries Interop Profile version.

### Previous Versions

- None

> Will be the version number as a link to the latest commit of this RFC while the version was current.

## Aries Agent Builders and Agents

A list of agents that claim compatibility with versions of Aries Interop Profile. A entry can be included per agent and per major Aries Interop Profile version.

The agent type MUST be one of the following:

- **Mobile** - A mobile agent; does not require mediator routing capabilities, credential issuing capabilities.
- **I/V** - A cloud-based Issuer/Verifier agent; does not require credential holding support.
- **Mediator** - A mediator/relay agent; does not require verifiable credential exchange protocol capabilities.
- **Holder** - A cloud-based holder/prover agent; does not require credential issuing capabilities.
- **Framework** - A general purpose agent code base for an agent that is the basis for deployments of agents; typically supports all AIP protocols.

Name / Version / Link | Agent Type | Builder / Link | Aries Interop Profile Version | Test Results | Notes
--- | --- | --- | --- | --- | ---
 |  |  |  |  | 

## Drawbacks

It may be difficult to agree on the exact list of RFCs to support in a given version.

## Rationale and alternatives

Continuing with the current informal discussions of what agents/frameworks should support and when is an ineffective way of enabling independent building of interoperable agents.

## Prior art

This is a typical approach to creating an early protocol certification program.

## Unresolved questions

- The community agreement process for setting Aries Interop Profile versions needs to be tried and adjusted as appropriate.
- The tracking of who is part of the Aries agent builders community needs to be defined so we know who should have the strongest say in the setting of Aries Interop Profile versions.
- Should the Implementations table in all RFCs (below) be used for the agent builders table (above)?  Or, should we eliminate the per RFC “implementations table (below and in all RFCs) and just use this RFC to track implementations?

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

_Implementation Notes_ [may need to include a link to test results](https://github.com/hyperledger/aries-rfcs/blob/master/README.md#accepted).


Name / Link | Implementation Notes
--- | ---
 |  | 
