# 0566: Issuer-Hosted Custodial Agents
- Authors: [Sam Curren](mailto:telegramsam@gmail.com)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2020-11-16
- Status Note: Draft
- Start Date: 2020-10-27
- Tags: concept

In the fully realized world of Self Soverign Identity, credential holders are equipped with capable agents to help them manage credentials and other SSI interactions. Before we arrive in that world, systems that facilitate the transition from the old model of centralized systems to the new decentralized models will be necessary and useful.

One of the common points for a transition system is the issuance of credentials. Today's centralized systems contain information within an information silo. Issuing credentials requires the recipient to have an agent capable of receiving and managing the credential. Until the SSI transition is complete, some users will not have an agent of their own.

Some users don't have the technology or the skills to use an agent, and there may be users who don't want to participate.

In spite of the difficulties, there are huge advantages to transition to a decentralized system. Even when users don't understand the technology, they do care about the benefits it provides.

This situation leaves the issuer with a choice: Maintain both a centralized system AND a decentralized SSI one, or enable their users to participate in the decentralized world.

This paper addresses the second option: How to facilitate a transition to a decentralized world by providing issuer-hosted custodial agents.

## Issuer-Hosted Custodial Agents

A custodial agent is an agent hosted on behalf of someone else. This model is common in the cryptocurrency space. An Issuer-Hosted Custodial Agent is exactly what it sounds like: an agent hosted for the holder of a credential by the issuer of the credential.

This custodial arrangement involves managing the credentials for the user, but also managing the keys for the user. Key management on behalf of another is often called guardianship.

An alternative to hosting the agent directly is to pay for the hosting by a third party provider. This arrangement addresses some, but not all, of the issues in this paper.

This custodial arrangement is only necessary for the users without their own agents. Users running their own agents (often a mobile app), will manage their own keys and their own credentials.

For the users with their own agents, the decentralized world has taken full effect: they have their own data, and can participate fully in the SSI ecosystem.

For the users with hosted custodial agents, they have only made a partial transition. The data is still hosted by the issuer. With appropriate limits, this storage model is no worse than a centralized system. Despite the data storage being the same, a hosted agent provides the ability to migrate to another agent if the user desires.

Hosting agents for users might sound like a costly endeavor, but hosted agents contain an advantage. Most hosted agents will only be used by their owners for a small amount of time, most likely similar to their interaction with the centralized system it replaces. This means that the costs are substantially lower than hosting a full agent.

## Hosted Agent Interaction

Hosted agents have some particular challenges in providing effective user interaction. Detailed below are several options that can be used alone or in combination.

### Browser Based
Providing a browser based user interface for a user is a common solution when the user will have access to a computer. Authentication will likely use something familiar like a username and password.

### Authorizing Actions
The user will often need a way to authorize actions that their agent will perform.
A good option for this is via the use of a basic cell phone through SMS text messages or voice prompts.
Less urgent actions can use an email sent to the user, prompting the user to login and authorize the actions.

### Offline / Paper based
At times the user will have no available technology for their use. In this case, providing QR codes printed on paper with accompanying instructions will allow the user to facilitate verifier (and perhaps another issuer) access to their cloud agent.
QR Codes, such as those detailed in the Out Of Band Protocol, can contain both information for connecting to agent AND an interaction to perform.
Presenting the QR code for scanning can serve as a form of consent for the prescribed action within the QR code.
Printed QR codes can be provided by the issuer at the time of custodial agent creation, or from within a web interface available to the user.

### Kiosk based
Kiosks can be useful to provide onsite interaction with a hosted agent. Kiosk authentication might take place via username and password, smartcard, or USB crypto key, with the possible inclusion of a biometric.
Kiosks must be careful to fully remove any cached data when a session closes.
Any biometric data used must be carefully managed between the kiosk and the hosted agent.

### Smartphone App
While it is common for a smartphone app to be an agent by itself, there are cases where a smartphone app can act as a remote for the hosted agent. In this iteraction, keys, credentials, and other wallet related data is held in the custodial agent. The mobile app acts as a remote viewer and a way for the user to authorize actions taken by the custodial agent.

## Best Practices

The following best practices should be followed to ensure proper operation and continued transition to a fully realized SSI architecture.
Most of these practices depend upon and support one another.

### Defend the SSI architecture
When issuers host custodial agents, care must be taken to avoid shortcuts that would violate SSI architecture. Deviations will frequently lead to incompatibilities.

### DIDComm Protocol based Integration
Communication between hosted agents and credential issuing agent must be based on published DIDComm protocols. Any communication which eliminates the use of a DID must be avoided. Whenever possible, these should be well adopted community protocols. If the case a new protocol is needed for a particular interaction, this must be fully documented and published, to allow other agents to become compatible by adopting the new protocol.

### Allow bring-your-own agents
The onboarding process must allow users to bring their own compatible agents. This will be possible as long as any communication is protocol based. No features available to hosted agents should be blocked from user provided agents.

### Limit wallet scope to data originating from the issuer
Issuer hosted agents should have limits placed on them to prevent general use. This will prevent the agent from accepting additional credentials and data outside the scope of the issuer, therefore introducing responsibility for data that was never intended. This limtation must not limit the user in how they use the credentials issued, only in the acceptance of credentials and data from other issuers or parties.
The use of policy and filters should be used to limit the types of credentials that can be held, which issuers should be allowed, and which protocols are enabled.
None of these restrictions are necessary for bring-your-own agents provided by users.

### Allow migrate from hosted to bring-your-own
Users must be allowed to transition from an issuer-hosted agent to an agent of their choosing. This can happen either via a backup in a standard format, or via re-issuing relevant credentials.

### Transparent to the verifier
A verifier should not be able to tell the difference between a custodial hosted agent vs a bring-your-own agent.

### Action Log
All actions taken by the wallet should be preserved in a log viewable to the user. This includes how actions were authorized, such as a named policy or confirmation via text message.

### Encrypted Wallets
Hosted wallet data should be encrypted at rest.

### Independant key management
Keys used for hosted agents should have key mangement isolated from the issuer keys. Access to the keys for hosted agents should be carefully limited to the minimum required personnel. All key access should be logged.

### Hosted Agent Isolation
Agents must be sufficiently isolated from each other to prevent a malicious user from accessing another user's agent or data or causing interruptions to the operation of another agent.

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

*Implementation Notes* [may need to include a link to test results](/README.md#accepted).

Name / Link | Implementation Notes
--- | ---
 |
