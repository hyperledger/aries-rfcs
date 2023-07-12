# Aries RFC 0793: Unqualified DID Transition

- Authors: [Sam Curren](mailto:swcurran@cloudcompass.ca)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2023-07-11
- Status Note: In Pre-work **Target Completion Date: 2023.10.15** 
- Supersedes:
- Start Date: 2023-07-11
- Tags: [feature](/tags.md#feature), [community-update](/tags.md#community-update)

## Summary

Historically, Aries use of the Indy SDK's wallet included the use of 'unqualified DIDs' or DIDs without a did: prefix and method. 
This transition documents the process of migrating any such DIDs still in use to fully qualified DIDs.

The transition from unqualified DIDs to peer:did:2 is described here: https://github.com/TimoGlastra/legacy-did-transformation

The use and support for did:peer:3 is also included in this transition.

This process ONLY applies to agent codebases using unqualified DIDs. Any codebases not using unqualified DIDs may ignore this process.

This RFC follows the guidance in [RFC
0345](../../concepts/0345-community-coordinated-update/README.md) about
community-coordinated updates to (try to) ensure that independently deployed,
interoperable agents remain interoperable throughout this transition.

The transition from the unqualified to qualified DIDs will occur in four steps:

- **Pre-work**: where we agree on the transition plan outlined in this RFC.
  - Finalize did:peer:3 details, including feature discovery support of did:peer:3.
  - Verify transisiton plan and code.
- **Step 1**: Agent builders MUST update all agent code bases and deployments to accept DIDs in the old (unqualified) and new (transitioned) forms. During this step, agents MUST continue the use of unqualified DIDs in all cases where they are currently being used.
  - Each agent builder SHOULD notify the community they have completed Step 1 by submitting a PR to update their entry in the [implementations](#implementations) accordingly.
- **Step 2**: Agent builders MUST update all agent code bases and deployments to use only fully qualified DIDs in all communication. Unqualified DIDs received are matched by the receiving agent to the associated fully qualified DID.
  - Each agent builder SHOULD notify the community they have completed Step 2 by submitting a PR to update their entry in the [implementations](#implementations) accordingly.
- **Step 3**: Agent builders SHOULD update their deployments to remove all support for receiving unqualified DIDs and MUST NOT use unqualified DIDs.

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
[Aries Framework - .NET](https://github.com/hyperledger/aries-framework-dotnet) | No steps completed
[Trinsic.id](https://trinsic.id/) | No steps completed
[Aries Cloud Agent - Python](https://github.com/hyperledger/aries-cloudagent-python) | No steps completed
[Aries Static Agent - Python](https://github.com/hyperledger/aries-staticagent-python) | No steps completed
[Aries Framework - Go](https://github.com/hyperledger/aries-framework-go) | No steps completed
[Connect.Me](https://www.evernym.com/blog/connect-me-sovrin-digital-wallet/) | No steps completed
[Verity](https://www.evernym.com/products/) | No steps completed
[Pico Labs](http://picolabs.io/) | No steps completed
[IBM](https://github.com/IBM-Blockchain-Identity/unknown) | No steps completed
IBM Agent | No steps completed
[Aries Cloud Agent - Pico](https://github.com/Picolab/aries-cloudagent-pico) | No steps completed
[Aries Framework JavaScript](https://github.com/hyperledger/aries-framework-javascript) | No steps completed