# 0270: Interop Test Suite
- Authors: [Daniel Hardman](daniel.hardman@gmail.com)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2019-10-25
- Status Note: Codifies some thinking about scope and mental model that are already socialized. Provides some new thinking as well.
- Supersedes: Partially, and in some ways, [Indy HIPE 0015](https://github.com/hyperledger/indy-hipe/blob/master/text/0015-agent-test-suite-interface/README.md) and [Indy HIPE 0016](https://github.com/hyperledger/indy-hipe/blob/master/text/0016-agent-test-suite-v1/README.md). Also, represents answers to questions that the community first posed in [this HackMD doc](https://hackmd.io/JW5b9xYCRGKqyqhVevTZ_g) and first attempted to answer in the [indy-agent repo](https://github.com/hyperledger/indy-agent).
- Start Date: 2018-10-25
- Tags: concept

## Summary

Describes the goals, scope, and interoperability contract of the Aries Interop Test Suite. Does NOT serve as a design doc for the test suite code, or as a developer guide explaining how the test suite can be run; see the [test suite codebase](https://github.com/hyperledger/aries-protocol-test-suite) for that.

## Motivation

The Aries Interop Test Suite makes SSI interoperability publicly and objectively measurable. It is a major deliverable of the Aries project as a whole--not a minor detail that only test zealots care about. It's important that the entire SSI community understand what it offers, how it works, what its results mean, and how it should be used.

## Tutorial

Interoperability is a buzzword in the SSI/decentralized identity space. We all want it.

Without careful effort, though, interoperability is subjective and slippery. If products A and B implement the same spec, or if they demo cooperation in a single workflow, does that mean they can be used together? How much? For how long? Across which release boundaries? With what feature caveats?

We need a methodology that gives crisp answers to questions like these--and it needs to be more efficient than continuously exercising every feature of every product against features of every other product.

However, it's important to temper our ambitions. Standards, community specs, and reference implementations exist, and many of them come with tests or test suites of their own. Products can test themselves with these tools, and with custom tests written by their dev staffs, and make rough guesses about interoperability. The insight we're after is a bit different.

### Goals

What we need is a tool that achieves these goals:

1. **Evaluate practical interoperability** of [agents](../../concepts/0004-agents/README.md).

    >[Other software that offers SSI features](../../concepts/0004-agents/README.md#the-agent-ness-continuum) should also be testable. Here, such components are conflated with agents for simplicity, but it's understood that the suite targets protocol participants no matter what their technical classification.
 
   Focus on remote interactions that deliver business value: [high-level protocols](../../concepts/0003-protocols/README.md) built atop [DIDComm](../../concepts/0005-didcomm/README.md), such as [credential issuance](../../features/0036-issue-credential/README.md), [proving](../../features/0037-present-proof/README.md), and [introducing](../../features/0028-introduce/README.md), where each [participant](../../concepts/0003-protocols/roles-participants-etc.md#participants) uses different software. DID methods, ledgers, crypto libraries, credential implementationss, and DIDComm infrastructure should have separate tests that are out of scope here. None of these generate deep insight into whether packaged software is interoperable enough to justify purchase decisions; that's the gap we need to plug.
   
2. **Describe results in a formal, granular, reproducible way** that supports comparison between agents A and B, and between A at two different points of time or in two different configurations.

    This implies a structured report, as well as support for versioning of the suite, the agents under test, and the results.

3. **Track the collective community state of the art**, so measurements are comprehensive and up-to-date, and so new ideas automatically encounter pressure to be vetted for interoperability.
 
    The test suite isn't a compliance tool, and it should be unopinionated about what's important and what's not. However, it should embody a broad list of testable features--[certainly, ones that are standard](/README.md#accepted), and often, [ones that are still maturing](/README.md#demonstrated).
    
### Dos and Don'ts

Based on the preceding context, the following rules guide our understanding of the test suite scope:

* **DO** organize testing around protocols, as this is the major way that interoperability questions manifest. "Can agent X issue credentials in a way that agent Y accepts?" is a question about whether X and Y support a common protocol.
* **DO** test many protocols.
* **DO** allow easy extension for new protocols, both as contributions inside the codebase and as external code added after the test suite is installed.
* **DO** evaluate unhappy paths (timeouts, brownouts, graceful handling of version incompatibilities, [reporting](../../features/0035-report-problem/README.md), [troubleshooting](../../features/0034-message-tracing/README.md)...), since practical interoperability is often a function of robustness in suboptimal circumstances. 
* **DO** test all relevant versions of each protocol. (The test suite does not need to maintain an unreasonably comprehensive inventory of all protocols; old protocols could be retired if they become difficult to support. An agent wishing to certify against an old protocol could download an old version of the test suite to certify. However, we generally want the test suite to support both breadth--many protocols--and depth--multiple protocol versions if they are all in active use.)
* **DO** test roles in a protocol separately, and DO test only one agent at a time. The question isn't *"Does agent X support the issuance protocol?"* but rather *"Does agent X support* role Y *in the issuance protocol?"* All roles in a protocol other than the one role for the one tested agent should be played by the test suite. 
* **DO** test required and optional [decorators](../../concepts/0011-decorators/README.md) to the extent that they are relevant to interoperability.
* **DO** distinguish between required and optional features of a protocol in results.
* **DO** provide value for agents that talk over transports besides HTTP: BlueTooth, SMTP, AMQP, and so forth -- but **DON'T** get bogged down in all the permutations of transport and routing.
* **DO** describe results in a formally defined data structure that can be prettified in various ways.
* **DO** allow the test suite to be an automated step in a CI/CD pipeline.
* **DO** evaluate *message* correctness, but touch more lightly on *data* correctness. See [this discussion about the distinction between messages and data](../../concepts/0017-attachments/README.md#messages-versus-data), and note how the [Issue Credential](../../features/0036-issue-credential/README.md) and [Present Proof](../../features/0037-present-proof/README.md) protocols push credential and presentation format to a concern about the format of attached data, so the data can evolve at a different rate from the protocol.

<hr> 
 
* **DON'T** attempt to replace proper unit, functional, or integration tests for agents.
* **DON'T** attempt to replace pen-testing or security analyses.
* **DON'T** attempt to replace formal methods (proofs of correctness/eventual consistency/security guarantees)
* **DON'T** test governance, policy, regulatory compliance, or similar high-level concerns outside fundamental interoperability. 
* **DON'T** require manual interaction.
* **DON'T** artificially link one protocol's results to another's.
* **DON'T** attempt to release the test suite in sync with other Aries artifacts. Rather, use an independent release cadence that many uncoordinated agent projects can leverage per their own convenience.
* **DON'T** impose unreasonable processes, tools, architecture constraints, or dependencies on builders of agents or test suite contributors. For example, if the test suite required the agent under test to be instrumented, and the instrumentation library weren't available on certain platforms, that would violate this rule. It should be possible for just about any agent to be put under test, long after its initial design, just by implementing the backchannel.
* **DON'T** require that the test suite be runnable by an independent third party; trust results as reported by an agent's own developers. The suite might be relevant in a certification process, but is not intended to embody a certification process in and of itself.
* **DON'T** worry about test suite performance much. We want tests to run in minutes, so we shouldn't do anything ridiculously time-consuming--but simplicity of the suite is more important than its efficiency.

### General Approach

We've chosen to pursue these goals by maintaining a modular interop test suite as a deliverable of the Aries project. The test suite is an agent in its own right, albeit an agent with deliberate misbehaviors, a security model unsuitable for production deployment, an independent release schedule, and a desire to use every possible version of every protocol.

Currently the suite lives in the `aries-protocol-test-suite` repo, but the location and codebase could change without invalidating this RFC; the location is an implementation detail.

### Contract Between Suite and Agent Under Test

The contract between the test suite and the agents it tests is:

#### Suite will...

1. Be packaged for local installation.

    Packaging could take various convenient forms. Those testing an agent install the suite in an environment that they control, where their agent is already running, and then configure the suite to talk to their agent.
    
2. *Evaluate* the **agent under test** by engaging in protocol interactions over a **frontchannel**, and *control* the interactions over a **backchannel**. Both channels use DIDComm over HTTP.

    Over the frontchannel, the test suite and the agent under test look like ordinary agents in the ecosystem; any messages sent over this channel could occur in the wild, with no clue that either party is in testing mode.
    
    The backchannel is the place where testing mode manifests. It lets the agent's initial state be set and reset with precision, guarantees its choices at forks in a workflow, eliminates any need for manual interaction, and captures notifications from the agent about errors. Depending on the agent under test, this backchannel may be very simple, or more complex. For more details, see [Backchannel](#backchannel) below.

    Agents that interact over other transports on either channel can use transport adapters provided by the test suite, or write their own. HTTP is the least common denominator transport into which any other transports are reinterpreted. Adapting is the job of the agent developer, not the test suite--but the suite will try to make this as easy as possible.
    
    <a href="https://docs.google.com/presentation/d/1Rn1gEnYXnIetC9IXrZynyh2FI6XHEE7n8wE6eIpvwZA/edit" target="imgsrc"><img src="channels.png" alt="channels"/></a>
    
3. Not probe for agent features. Instead, it will just run whatever subset of its test inventory is declared relevant by the agent under test.

    This lets simple agents do simple integrations with the test suite, and avoid lots of needless error handling on both sides.
    
4. Use a set of predefined identities and a set of starting conditions that all agents under test must be able to recognize on demand; these are referenced on the backchannel in control messages. See [Predefined Inventory](#predefined-inventory) below.

5. Run tests in arbitrary orders and combinations, but only run one test at a time.

    Some agents may support lots of concurrency, but the test suite should not assume that all agents do.

6. Produce an [__interop profile__](#interop-profile) for the agent under test, with respect to the tested features, for every successful run of the test suite.

    A "successful" run is one where the test suite runs to completion and believes it has valid data; it has nothing to do with how many tests are passed by the agent under test. The test suite will not emit profiles for unsuccessful runs.
     
     Interop profiles emitted by the test suite are the artifacts that should be [hyperlinked in the Implementation Notes section of protocol RFCs](../../README.md#accepted). They could also be published (possibly in a prettified form) in release notes, distributed as a product or documentation artifact, or returned as an attachment with the `disclose` message of the [Discover Features protocol](../../features/0031-discover-features/README.md).
     
7. Have a very modest footprint in RAM and on disk, so running it in Docker containers, VMs, and CI/CD pipelines is practical.
 
8. Run on modern desktop and server operating systems, but not necessarily on embedded or mobile platforms. However, since it interacts with the agent under test over a remote messaging technology, it should be able to test agents running on any platform that's capable of interacting over HTTP or over a transport that can be adapted to HTTP.

9. Enforce reasonable timeouts unless configured not to do so (see note about user interaction below).
 
#### Agent under test will...

1. Provide a consistent name for itself, and a semver-compatible version, so test results can be compared across test suite runs.

2. Use the test suite configuration mechanism to make a claim about the tests that it believes are relevant, based on the features and roles it implements.

2. Implement a distinction between test mode and non-test mode, such that:
 
    * Test mode causes the agent to expose and use a backchannel--but the backchannel does not introduce a risk of abuse in production mode.
    
    * Test mode either causes the agent to need no interaction with a user (preferred), or is combined with test suite config that turns off timeouts (not ideal but may be useful for debugging and mobile agents). This is necessary so the test suite can be automated, or so unpredictable timing on user interaction doesn't cause spurious results.
    
    The mechanism for implementing this mode distinction could be extremely primitive (conditional compilation, cmdline switches, config file, different binaries). It simply has to preserve ordinary control in the agent under test when it's in production, while ceding some control to the test suite as the suite runs.

3. Faithfully create the start conditions implied by named states from the [Predefined Inventory](#predefined-inventory), when requested on the backchannel.

4. Accurately report errors on the backchannel.

## Reference

### Releasing and Versioning

Defining a release and versioning scheme is important, because the test suite's version is embedded in every interop profile it generates, and people who read test suite output need to reason about whether the results from two different test suites are comparable. By picking the right conventions, we can also avoid a lot of complexity and maintenance overhead.

The test suite releases implicitly with every merged commit, and is versioned in a [semver-compatible](https://semver.org/) way as follows:

* The `major` version of the test suite version corresponds to the provisions of the contract defined in this RFC. Any breaking changes in this RFC will require an increment of the major number.

* The `minor` version of the test suite is a count of how many protocol+version combinations the community knows about. This number is derived from a list of known [PIURIs](../../concepts/0003-protocols/uris.md#piuri) that's autogenerated from metadata about protocols in the `aries-rfcs` repo. Publishing or versioning a protocol in the community thus automatically causes the test suite's minor version to increment.

* The `patch` version of the test suite is the 7-character short form of the git commit hash for the source code from which it is built.

The major version should change rarely, after significant community debate. The minor version should update on a weekly or monthly sort of timeframe as protocols accumulate and evolve in the community--without near-zero release effort by contributors to the test suite. The patch version is updated automatically with every commit. This is a very light process, but it still allows the test suite on Monday and the test suite on Friday to report versions like `1.39.5e22189` and `1.40.c5d8aaf`, to know which version of the test suite is later, to know that both versions implement the same contract, and to know that the later version is backwards-compatible with the earlier one.

### Test Naming and Grouping

Tests in the test suite are named in a comma-separated form that groups them by protocol, version, role, and behavior, in that order. For example, a test of the `holder` role in version `1.0` of the the `issue-credential` protocol, that checks to see if the holder sends a proper `ack` at the end, might be named:

    issue-credential,1.0,holder,sends-final-ack
    
Because of punctuation, this format cannot be reflected in function names in code, and it also will probably not be reflected in file names in the test suite codebase. However, it provides useful grouping behavior when sorted, and it is convenient for parsing. It lets agents under test declare patterns of relevant tests with wildcards. An agent that supports the credential issuance but not holding, and that only supports the 1.1 version of the `issue-credential` protocol, can tell the test suite what's relevant with:

    issue-credential,1.1,issuer,*
    
### Interop Profile

The results of a test suite run are represented in a JSON object that looks like this:

```jsonc
{
    "@type": "Aries Test Suite Interop Profile v1"
    "suite_version": "1.39.5e22189",
    "under_test_name": "Aries Static Agent Python",
    "under_test_version": "0.9.3",
    "test_time": "2019-11-23T18:59:06", // when test suite launched
    "results": [
        {"name": "issue-credential,1.0,holder,ignores-spurious-response", "pass": false },
        {"name": "issue-credential,1.0,holder,sends-final-ack", "pass": true },
    ]
}
```

### Backchannel

[TODO: reconcile this against what Daniel B and Sam already envisioned. I just made this up off the top of my head...]

The backchannel between test suite and agent under test is managed as a standard DIDComm protocol. The identifier for the message family is X. The messages include:

* `reset-state`: Sent from suite to agent. Throws away all current state and gives keys and relationships that must exist in the KMS, by referencing named items from the [Predefined Inventory](#predefined-inventory).
* `start`: Sent from suite to agent. Triggers the agent under test to make the first move in a protocol. Identifies the role the agent should take, and possibly the message type the agent should emit to start, if more than one start message is possible. Also identifies the roles and endpoints for any other participants.
* `control-next`: Sent from suite to agent. Tells the agent under test what to do the next time it is their turn to make a decision in the protocol. For example, if the protocol under test is tic-tac-toe, this might tell the agent under test what move to make. Does this in a generic way by attaching an approximation of the plaintext message the test suite wants the agent under test to emit. The agent can examine this JSON and act accordingly.
* `problem-report`: Sent from agent to suite to report errors in the testing procedure itself. Any such message invalidates and abandons the current test.
* `report-state-change`: Sent from agent to suite to report that it is now in a new state in the protocol.

### Predefined Inventory

TODO: link to the predefined identity for the test suite created by Daniel B, plus the RFC about other predefined DIDs. Any and all of these should be names as possible existing states in the KMS. Other initial states:

* totally empty KMS
* corrupt KMS
* 100 random DIDs from various DID methods, with ratios per method configurable

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

*Implementation Notes* [may need to include a link to test results](/README.md#accepted).

Name / Link | Implementation Notes
--- | ---
 | 

