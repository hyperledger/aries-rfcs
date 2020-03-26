# Aries RFC 0348: Transition Message Type to HTTPs

- Authors: [Stephen Curran](mailto:swcurran@cloudcompass.ca)
- Status: [ACCEPTED](/README.md#accepted)
- Since: 2020-01-30
- Status Note: In step 1 - community is updating implementations to accept old and new formats. **Target Completion Date: 2020.02.29** 
- Supersedes:
- Start Date: 2019-12-13
- Tags: feature, community-update

## Summary

Per issue [#225](https://github.com/hyperledger/aries-rfcs/issues/225), the
Aries community has agreed to change the prefix for protocol message types that currently use the
`did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/` to use `https://didcomm.org/`. Examples of the two message types forms are:

- Before: `did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/notification/1.0/ack`
- After: `https://didcomm.org/notification/1.0/ack`

This RFC follows the guidance in [RFC
0345](../../concepts/0345-community-coordinated-update/README.md) about
community-coordinated updates to (try to) ensure that independently deployed,
interoperable agents remain interoperable throughout this transition.

The transition from the old to new formats will occur in four steps:

- **DONE Pre-work**: where we agree on the transition plan outlined in this RFC.
  - Any RFC updates related to this transition needed before starting the transition are completed.
  - > To Do: Identify if there any prerequisite RFC changes to be made.
- **IN PROGRESS Step 1: Agent builders MUST update all agent code bases and deployments to accept incoming message types in the old (did) and new (https) formats. During this step, agents MUST default to sending out messages in the old format.**
  - Each agent builder SHOULD notify the community they have completed Step 1 by submitting a PR to update their entry in the [implementations](#implementations) accordingly.
- **Step 2**: Agent builders MUST update all agent code bases and deployments to send out all messages using the new (https) format. The old (did) format is deprecated but will still be accepted. An agent deployment MAY send out an old format message type upon receipt of a message containing an old format message type.
  - Each agent builder SHOULD notify the community they have completed Step 2 by submitting a PR to update their entry in the [implementations](#implementations) accordingly.
- **Step 3**: Agent builders SHOULD update their deployments to remove all support for receiving the old format and MUST NOT send out messages using the old message type format.

> **Note**: Any RFCs that already use the new "https" message type should continue to use the use new format in all cases&mdash;accepting and sending. New protocols defined in new and updated RFCs should use the new "https" format.

The community coordination triggers between the steps above will be as follows:

- **Pre-work to Step 1** - a PR to this RFC is merged that sets the RFC status to [ACCEPTED](/README.md#accepted).
  - The [ACCEPTED](/README.md#accepted) version of this RFC is included in the current [Aries Interop Profile](/concepts/0302-aries-interop-profile/README.md) version.
- **Step 1 to Step 2** - the community agrees that the majority of the deployed agents have completed Step 1. A PR to this RFC is merged that sets the RFC status to [ADOPTED](/README.md#adopted).
  - Agent builders indicate completion of Step 1 by updating the [Implementations](#implementations) section of this RFC.
  - All other RFCs in this repo are updated to use the new message type format.
  - The [ADOPTED](/README.md#adopted) version of this RFC is included in the current [Aries Interop Profile](/concepts/0302-aries-interop-profile/README.md) version.
- **Step 2 to Step 3** - the community agrees that the majority of the deployed agents have completed Step 2. A PR to this RFC is merged that sets the RFC status to [RETIRED](/README.md#retired).
  - Agent builders indicate completion of Step 2 by updating the [Implementations](#implementations) section of this RFC.

## Motivation

To enable agent builders to independently update their code bases and deployed agents while maintaining interoperability.

## Tutorial

The general mechanism for this type of transition is documented in [RFC 0345](../../concepts/0345-community-coordinated-update/README.md) about
community-coordinated updates.

The specific sequence of events to make this particular transition is outlined in the [summary](#summary) section of this RFC.

## Reference

See the [summary](#summary) section of this RFC for the details of this transition.

## Drawbacks

None identified.

## Rationale and alternatives

This approach balances the speed of adoption with the need for independent deployment and interoperability.

## Prior art

The approach outlined in [RFC
0345](../../concepts/0345-community-coordinated-update/README.md) about
community-coordinated updates is a well-known pattern for using deprecation to
make breaking changes in an ecosystem. That said, this is the first attempt to
use this approach in Aries. Adjustments to the transition plan will be made as needed, and RFC 0345 will be updated based on lessons learned in executing this plan.

## Unresolved questions

- Are any changes to existing RFCs needed before starting Step 1?

## Implementations

The following table lists the status of various agent code bases and deployments with respect to the steps of this transition. Agent builders MUST update this table as they complete steps of the transition.

Name / Link | Implementation Notes
--- | ---
[Aries Protocol Test Suite](https://github.com/hyperledger/aries-protocol-test-suite) | No steps completed
[Aries Toolbox](https://github.com/hyperledger/aries-toolbox) | Completed Step 1 [code change](https://github.com/hyperledger/aries-toolbox/pull/155). 
[Aries Framework - .NET](https://github.com/hyperledger/aries-framework-dotnet) | No steps completed
[Streetcred.id](https://streetcred.id/) | No steps completed
[Aries Cloud Agent - Python](https://github.com/hyperledger/aries-cloudagent-python) | Completed Step 1 [code change](https://github.com/hyperledger/aries-cloudagent-python/pull/379)
[Aries Static Agent - Python](https://github.com/hyperledger/aries-staticagent-python) | No steps completed
[Aries Framework - Go](https://github.com/hyperledger/aries-framework-go) | No steps completed
[Connect.Me](https://www.evernym.com/blog/connect-me-sovrin-digital-wallet/) | No steps completed
[Verity](https://www.evernym.com/products/) | No steps completed
[Pico Labs](http://picolabs.io/) | Completed Step 1 [code change](https://github.com/picolab/G2S) and notifying known owner/operators of Pico Agents
[Libvcx](https://github.com/hyperledger/indy-sdk) | Completed Step 1 [code change](https://github.com/hyperledger/indy-sdk/pull/2136)