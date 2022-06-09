# 0302: Aries Interop Profile

- Authors: [Stephen Curran](mailto:swcurran@cloudcompass.ca), [John Jordan](mailto:john.jordan@gov.bc.ca) Province of British Columbia
- Status: [ACCEPTED](https://github.com/hyperledger/aries-rfcs/blob/main/README.md#accepted)
- Since: 2021-01-06
- Status Note: This RFC defines an Aries Interop Profile process and Aries Interop Profile versions
- Supersedes:
- Start Date: 2019-11-06
- Tags: [concept](/tags.md#concept)

## Summary

This RFC defines the process for the community of Aries agent builders to:

- enumerate a versioned set of Aries concept and feature RFCs which are collectively referred to as 'Aries Interop Profile Vx.y'
- track Aries Interop Profile versions.

"Agent builders" are organizations or teams that are developing open source code upon which agents can be built (e.g. [aries-framework-dotnet](https://github.com/hyperledger/aries-framework-dotnet)), or deployable agents (e.g. [Aries Mobile Agent Xamarin](https://github.com/hyperledger/aries-mobileagent-xamarin)), or commercially available agents.

An Aries Interop Profile (AIP) version provides a clearly defined set of versions of RFCs for Aries agent builders to target their agent implementation when they wish it to be interoperable with other agents supporting the same Aries Interop Profile version. The Aries Interop Profile versioning process is intended to provide clarity and predictability for Aries agent builders and others in the broader Aries community. The process is not concerned with proposing new, or evolving existing, RFCs, nor with the development of Aries code bases.

At all times, the [Reference](#reference) section of this RFC defines one or more current Aries Interop Profile versions -- a number and set of links to specific commits of concept and features RFCs, along with a list of all previous Aries Interop Profile versions. Several current Aries Interop Profile versions can coexist during periods when multiple major Aries Interop Profile versions are in active use (e.g. 1.x and 2.x). Each entry in the previous versions list includes a link to the commit of this RFC associated with that Aries Interop Profile version. The [Reference](#reference) section MAY include one "<major>.next" version for each existing current major Aries Interop Profile versions. Such "next" versions are proposals for what is to be included in the next minor AIP version.

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

Each link to a concept or feature RFCs MUST be to a specific commit of that RFC. RFCs in the list MAY be flagged as deprecated. Linked RFCs that reference external specs or standards MUST refer to as specific a version of the external resource as possible. 

Aries Interop Profile versions SHOULD have a link (or links) to a version (specific commit) of a test suite (or test cases) which SHOULD be used to verify compliance with the corresponding version of Aries Interop Profile. Aries agent builders MAY self-report their test results as part of their entries in the list of agents.

Aries Interop Profile versions MUST evolve at a pace determined by the Aries agent builder community. This pace SHOULD be at a regular time interval so as to facilitate the independent but interoperable release of Aries Agents. Aries agent builders are encouraged to propose either updates to the list of RFCs supported by Aries Interop Profile through GitHub Issues or via a Pull Request. Such updates MAY trigger a change in the Aries Interop Profile version number.

All previous versions of Aries Interop Profile MUST be listed in the [Previous Versions](#previous-versions) section of the RFP and must include a link to the latest commit of this RFC at the time that version was active.

A script in the `/code` folder of this repo can be run to list RFCs within an AIP
version that have changed since the AIP version was set. For script usage information
run the following from the root of the repo:

`python code/aipUpdates.py --help`

### Sub-targets

AIP 2.0 is organized into a set of base requirements, and additional optional targets. These requirements are listed below. When indicating levels of support for AIP 2.0, subtargets are indicated in this format: `AIP 2.0/INDYCREDS/MEDIATE` with the subtargets listed in any order.

Any RFCs within a single AIP Version and it's subtargets MUST refer to the exact same version of the RFC.

### Discover Features Usage

AIP Targets can be disclosed in the discover_features protocol, using the `feature-type` of `aip`. The feature's `id` is `AIP<major>.<minor>` for base compatibility, and `AIP<major>.<minor>/<subtarget>` for subtargets, each subtarget being included individually.

Example:

```json
{
  "@type": "https://didcomm.org/discover-features/2.0/disclosures",
  "disclosures": [
    {
      "feature-type": "aip",
      "id": "AIP2.0",
    },
    {
      "feature-type": "aip",
      "id": "AIP2.0/INDYCRED"
    }
  ]
}
```

## Reference

The Aries Interop Profile version number and links to other RFCs in this section SHOULD only be updated with the agreement of the Aries agent builder community. There MAY be multiple active major Aries Interop Profile versions. A list of previous versions of Aries Interop Profile are [listed after](#previous-versions) the current version(s).

### Aries Interop Profile Version: 1.0

The initial version of Aries Interop Profile, based on the existing implementations such as [aries-cloudagent-python](https://github.com/hyperledger/aries-cloudagent-python), [aries-framework-dotnet](https://github.com/hyperledger/aries-framework-dotnet), [Open Source Mobile Agent](https://github.com/mattrglobal/osma) and [Streetcred.id](https://streetcred.id)'s IOS agent. Agents adhering to AIP 1.0 should be able to establish connections, exchange credentials and complete a connection-less proof-request/proof transaction.

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
Feature | [0160-connection-protocol](https://github.com/hyperledger/aries-rfcs/tree/4d9775490359e234ab8d1c152bca6f534e92a38d/features/0160-connection-protocol)
Feature | [0025-didcomm-transports](https://github.com/hyperledger/aries-rfcs/tree/b490ebe492985e1be9804fc0763119238b2e51ab/features/0025-didcomm-transports)
Feature | [0035-report-problem](https://github.com/hyperledger/aries-rfcs/tree/89d14c15ab35b667e7a9d04fe42d4d48b10468cf/features/0035-report-problem)
Feature | [0036-issue-credential](https://github.com/hyperledger/aries-rfcs/tree/bb42a6c35e0d5543718fb36dd099551ab192f7b0/features/0036-issue-credential)
Feature | [0037-present-proof](https://github.com/hyperledger/aries-rfcs/tree/4fae574c03f9f1013db30bf2c0c676b1122f7149/features/0037-present-proof)
Feature | [0056-service-decorator](https://github.com/hyperledger/aries-rfcs/tree/527849ec3aa2a8fd47a7bb6c57f918ff8bcb5e8c/features/0056-service-decorator)

#### Changelog - AIP 1.0

The original commit used in the definition of AIP 1.0 was: 64e5e55c123b2efaf38f4b0911a71a1c40a7f29d

The following clarifications have been made to RFCs that make up AIP 1.0:

- RFC 0160 Connection: `signers` was updated to `signer` in the Signature decorator example, following the RFC.

#### AIP v1.0 Test Suite

> To Do: Link(s) to version(s) of the test suite/test cases applicable to this Aries Interop Profile version.

### Aries Interop Profile Version: 2.0

The following are the goals used in selecting RFC versions for inclusion in AIP 2.0, and the RFCs added as a result of each goal:

- From AIP 1.0: Aries Agents must be able to establish connections, exchange credentials and complete a connection-less proof-request/proof transaction.

- Aries agents must be able to reuse connections.
  - RFCs 0434, 0023, 0519, 0360

- Enable access to actionable information in Mobile Agents to enable improvements in the user experience (vs. AIP 1.0-based mobile agents).
  - RFCs 0183, 0095, 0557

- Improve support for credential revocation use cases, independent of the revocation mechanism being used.
  - RFCs 0183

- Improve the low-level messaging cryptography and enable a transition to DIDComm 2.0 to improve the security of the communication paths between agents.
  - RFCs 0044, 0360, 0334, 0587

- Use protocols and standards that support multiple ledger types and verifiable credential formats.
  - RFCs 0434, 0023, 0453, 0454

- Where appropriate, enable standard mediator coordination capabilities for mobile agents and multi-tenant agencies.
  - RFC 0211

### AIP 2.0 Clarification Changelog

Since approval of the AIP 2.0 profile, the following RFCs have been clarified by updating the commit in the link to the RFC:

- 2022-03: RFC 0004 Agents, RFC 0005 DIDComm, RFC 0046 Mediators and Relays, RFC 0211 Route Coordination
  - Note: In this update, a number of RFCs were changed solely for the purpose
    of changing a link in the RFC to reference the "main" branch.
  - Pull request: [#724](https://github.com/hyperledger/aries-rfcs/pull/724)

- 2022-06: RFC 0023 DID Exchange, RFC 0025 DIDComm Transports, RFC 0434 Out of Band
  - Pull request: [#739](https://github.com/hyperledger/aries-rfcs/pull/739)

#### Base Requirements

 RFC Type | RFC/Link to RFC Version | Note
--- | --- | ---
Concept | [0003-protocols](https://github.com/hyperledger/aries-rfcs/tree/4e78319e5f79df2003ddf37f8f497d0fae20cc63/concepts/0003-protocols) | [AIP V1.0, Reformatted](https://gist.github.com/swcurran/6976dc1fd1b10c51343cf3812288b345/revisions?diff=unified)
Concept | [0004-agents](https://github.com/hyperledger/aries-rfcs/tree/4e78319e5f79df2003ddf37f8f497d0fae20cc63/concepts/0004-agents) | AIP V1.0, Unchanged
Concept | [0005-didcomm](https://github.com/hyperledger/aries-rfcs/tree/1b4b014246d19c865c9b5520b97fe0376a86d8c4/concepts/0005-didcomm) | [AIP V1.0, Minimally Updated](https://gist.github.com/swcurran/788195ea0bccec53e1f9fe3509034341/revisions?diff=unified)
Concept | [0008-message-id-and-threading](https://github.com/hyperledger/aries-rfcs/tree/b3a3942ef052039e73cd23d847f42947f8287da2/concepts/0008-message-id-and-threading) | [AIP V1.0, Updated](https://gist.github.com/swcurran/db72109ea4f2e336ac91f4fbab3f4048/revisions?diff=unified)
Concept | [0011-decorators](https://github.com/hyperledger/aries-rfcs/tree/b3a3942ef052039e73cd23d847f42947f8287da2/concepts/0011-decorators) | [AIP V1.0, Updated](https://gist.github.com/swcurran/04229583a509f12258352f9c85b9c9b6/revisions?diff=unified)
Concept | [0017-attachments](https://github.com/hyperledger/aries-rfcs/tree/7759addb1506d107fddec692403bbc9e55fe491f/concepts/0017-attachments) | [AIP V1.0, Updated](https://gist.github.com/swcurran/7d88f9866175af96a70e5c6c00fa0148/revisions?diff=unified)
Concept | [0020-message-types](https://github.com/hyperledger/aries-rfcs/tree/4e78319e5f79df2003ddf37f8f497d0fae20cc63/concepts/0020-message-types) | [AIP V1.0, Updated](https://gist.github.com/swcurran/8f95c25b5c778426d3a47fe6d7c46c70/revisions?diff=unified)<br>Mandates message prefix `https://didcomm.org` for Aries Protocol messages.
Concept | [0046-mediators-and-relays](https://github.com/hyperledger/aries-rfcs/tree/45b4233fcffda14f1339380ae2233289f21296b0/concepts/0046-mediators-and-relays) | [AIP V1.0, Minimally Updated](https://gist.github.com/swcurran/2486b63615f7a36c1e997b6c8b10c245/revisions?diff=unified)
Concept | [0047-json-LD-compatibility](https://github.com/hyperledger/aries-rfcs/tree/4e78319e5f79df2003ddf37f8f497d0fae20cc63/concepts/0047-json-ld-compatibility) | [AIP V1.0, Minimally Updated](https://gist.github.com/swcurran/8ef311d793fc6964328687af3c0efd34/revisions?diff=unified)
Concept | [0050-wallets](https://github.com/hyperledger/aries-rfcs/tree/4e78319e5f79df2003ddf37f8f497d0fae20cc63/concepts/0050-wallets) | AIP V1.0, Unchanged
Concept | [0094-cross-domain messaging](https://github.com/hyperledger/aries-rfcs/tree/b3a3942ef052039e73cd23d847f42947f8287da2/concepts/0094-cross-domain-messaging) | [AIP V1.0, Updated](https://gist.github.com/swcurran/e3f27e3ab85a260aaf279352ecc4e1fb/revisions?diff=unified)
Concept | [0519-goal-codes](https://github.com/hyperledger/aries-rfcs/tree/b3a3942ef052039e73cd23d847f42947f8287da2/concepts/0519-goal-codes) | :new:
Feature | [0015-acks](https://github.com/hyperledger/aries-rfcs/tree/b3a3942ef052039e73cd23d847f42947f8287da2/features/0015-acks) | [AIP V1.0, Updated](https://gist.github.com/swcurran/81af391bfd79539edec530150045fe51/revisions?diff=unified)
Feature | [0019-encryption-envelope](https://github.com/hyperledger/aries-rfcs/tree/4e78319e5f79df2003ddf37f8f497d0fae20cc63/features/0019-encryption-envelope) | [AIP V1.0, Updated](https://gist.github.com/swcurran/c652dfd39706e50be4145568797e667a/revisions?diff=unified)<br>See envelope note below
Feature | [0023-did-exchange](https://github.com/hyperledger/aries-rfcs/tree/bf3d796cc33ce78ed7cde7f5422b10719a68be21/features/0023-did-exchange) | :new:
Feature | [0025-didcomm-transports](https://github.com/hyperledger/aries-rfcs/tree/f39481e92ad1a10dbc499cd4931a08c3497cee3f/features/0025-didcomm-transports) | [AIP V1.0, Minimally Updated](https://gist.github.com/swcurran/1e64cba5f6c524d38ad596209df090df/revisions?diff=unified)
Feature | [0035-report-problem](https://github.com/hyperledger/aries-rfcs/tree/b3a3942ef052039e73cd23d847f42947f8287da2/features/0035-report-problem) | [AIP V1.0, Updated](https://gist.github.com/swcurran/d9432abc436e6a069d6ffcd41dc86060/revisions?diff=unified)
Feature | [0044-didcomm-file-and-mime-types](https://github.com/hyperledger/aries-rfcs/tree/b3a3942ef052039e73cd23d847f42947f8287da2/features/0044-didcomm-file-and-mime-types) | :new:
Feature | [0048-trust-ping](https://github.com/hyperledger/aries-rfcs/tree/4e78319e5f79df2003ddf37f8f497d0fae20cc63/features/0048-trust-ping) | :new:
Feature | [0183-revocation-notification](https://github.com/hyperledger/aries-rfcs/tree/4e78319e5f79df2003ddf37f8f497d0fae20cc63/features/0183-revocation-notification) | :new:
Feature | [0360-use-did-key](https://github.com/hyperledger/aries-rfcs/tree/4e78319e5f79df2003ddf37f8f497d0fae20cc63/features/0360-use-did-key) | :new:
Feature | [0434-outofband](https://github.com/hyperledger/aries-rfcs/tree/2bc7db66d15a55d70ce5bd16b2513a853c9d5749/features/0434-outofband) | :new:
Feature | [0453-issue-credential-v2](https://github.com/hyperledger/aries-rfcs/tree/b3a3942ef052039e73cd23d847f42947f8287da2/features/0453-issue-credential-v2) | Update to V2 Protocol
Feature | [0454-present-proof-v2](https://github.com/hyperledger/aries-rfcs/tree/b3a3942ef052039e73cd23d847f42947f8287da2/features/0454-present-proof-v2) | Update to V2 Protocol
Feature | [0557-discover-features-v2](https://github.com/hyperledger/aries-rfcs/tree/b3a3942ef052039e73cd23d847f42947f8287da2/features/0557-discover-features-v2) | :new:
Feature | [0627-static-peer-dids](https://github.com/hyperledger/aries-rfcs/tree/4739fbf6de07a54c3fee072bd85741422730b3cd/features/0627-static-peer-dids)  | :new:
Feature | [0317-please-ack](https://github.com/hyperledger/aries-rfcs/tree/9ff2cab45487a1f6f74254abc9134419f2ad5858/features/0317-please-ack)  | :new:

#### MEDIATE: Mediator Coordination

 RFC Type | RFC/Link to RFC Version | Note
--- | --- | ---
Feature | [0211-route-coordination](https://github.com/hyperledger/aries-rfcs/tree/55e1e1c6e339ef0843268b4f3349b95cb7bd49a5/features/0211-route-coordination) | :new:
Feature | [0092-transport-return-route](https://github.com/hyperledger/aries-rfcs/tree/b3a3942ef052039e73cd23d847f42947f8287da2/features/0092-transport-return-route) | :new:

#### INDYCRED: Indy Based Credentials

 RFC Type | RFC/Link to RFC Version | Note
--- | --- | ---
Feature | [0592-indy-attachments](https://github.com/hyperledger/aries-rfcs/tree/26344513082af4d76c77b8b4f5064e72d0a83b58/features/0592-indy-attachments) | :new: Evolved from AIP V1.0
Concept | [0441-present-proof-best-practices](https://github.com/hyperledger/aries-rfcs/tree/4e78319e5f79df2003ddf37f8f497d0fae20cc63/concepts/0441-present-proof-best-practices) | :new:

#### LDCRED: JSON-LD Based Credentials

 RFC Type | RFC/Link to RFC Version | Note
--- | --- | ---
Feature | [0593-json-ld-cred-attach](https://github.com/hyperledger/aries-rfcs/tree/b3a3942ef052039e73cd23d847f42947f8287da2/features/0593-json-ld-cred-attach) | :new:
Feature | [0510-dif-pres-exch-attach](https://github.com/hyperledger/aries-rfcs/tree/7a44f650d3cebf5b3047c1680618978393a497d5/features/0510-dif-pres-exch-attach) | :new:

#### BBSCRED: BBS+ Based Credentials

 RFC Type | RFC/Link to RFC Version | Note
--- | --- | ---
Feature | [0593-json-ld-cred-attach](https://github.com/hyperledger/aries-rfcs/tree/b3a3942ef052039e73cd23d847f42947f8287da2/features/0593-json-ld-cred-attach) | :new:
Feature | [0646-bbs-credentials](https://github.com/hyperledger/aries-rfcs/blob/7a44f650d3cebf5b3047c1680618978393a497d5/features/0646-bbs-credentials/README.md) | :new:
Feature | [0510-dif-pres-exch-attach](https://github.com/hyperledger/aries-rfcs/tree/7a44f650d3cebf5b3047c1680618978393a497d5/features/0510-dif-pres-exch-attach) | :new:

#### DIDCOMMV2PREP: DIDComm v2 Prep
 RFC Type | RFC/Link to RFC Version | Note
--- | --- | ---
Feature | [0587-encryption-envelope-v2](https://github.com/hyperledger/aries-rfcs/tree/b3a3942ef052039e73cd23d847f42947f8287da2/features/0587-encryption-envelope-v2) | :new:<br>See envelope note below

#### CHAT: Chat related features
 RFC Type | RFC/Link to RFC Version | Note
--- | --- | ---
Feature | [0095-basic-message](https://github.com/hyperledger/aries-rfcs/tree/b3a3942ef052039e73cd23d847f42947f8287da2/features/0095-basic-message) | :new:

#### AIP v2.0 Test Suite

The [Aries Agent Test Harness](https://github.com/hyperledger/aries-agent-test-harness) has a set of tests tagged to exercise AIP 1.0 and AIP 2.0, including the extended targets.

#### Implementers Note about DIDComm Envelopes and the `ACCEPT` element

AIP 2.0 contains two RFCs that reference envelopes 0019-encryption-envelope and 0587-encryption-envelope-v2 (links above).
The important feature that Aries implementers should understand to differentiate which envelope format can or is being used by an agent is the
`accept` element of the DIDComm service endpoint and the out-of-band `invitation` message. If the `accept` element is not present, the
agent can only use the RFC 0019-encryption-envelope present. If it is present, the values indicate the envelope format(s)
the agent does support. See the RFCs for additional details.

#### Changelog - AIP 2.0

The original commit used in the definition of AIP 2.0 was: b3a3942ef052039e73cd23d847f42947f8287da2

The following clarifications have been made to RFCs that make up AIP 2.0:

- RFC 0003 Protocols: A correction to the tic-tac-toe example protocol was made.
- RFC 0017 Attachments: A clarification was made around the use of base64url encoding/decoding.
- RFC 0434 Out of Band: The RFC status was changed to "Accepted."
- RFC 0627 Static Peer DIDs: The RFC status was changed to "Accepted."
- RFC 0441 Present Proof Best Practices: A convention for representing dates to enable simple "older than" predicates was added.
- RFC 0510 DIF Presentation Exchange Attachment: The RFC Status was changed to "Accepted."
- RFC 0646 BBS Credentials: The RFC Status was changed to "Accepted."
- RFC 0317 Please Ack: The RFC Status was changed to "Accepted" and added to the AIP 2.0 base requirements list. Original discussion included the please ack decorator, but it wasn't added to the AIP 2.0 list before releasing AIP 2.0.
- RFC 0592 Indy Attachment Format: The encoding algorithm used for credential attributes was added from RFC 0036.

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

_Implementation Notes_ [may need to include a link to test results](https://github.com/hyperledger/aries-rfcs/blob/main/README.md#accepted).


Name / Link | Implementation Notes
--- | ---
 |  | 
