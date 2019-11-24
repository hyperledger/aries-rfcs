# Aries RFC 0303: V0.1 Credential Exchange (Deprecated)

- Authors: [Tomislav Markovski](mailto:tomislav@streetcred.id), [Andrew Whitehead](mailto:andrew@1crm.com), [Stephen Curran](mailto:swcurran@cloudcompass.ca)
- Status: [RETIRED](../../README.md#retired)
- Since: 2019-11-12
- Status Note: Deprecated, but in common use in existing deployments of Aries agents. See [Implementations](#implementations) 
- Supersedes: [HackMD Document](https://hackmd.io/oWSw18DLTYCmHi_ty_gYvg?view)
- Start Date: 2019-03-13
- Tags: feature, protocol

## Summary

The 0.1 version of the ZKP Credential Exchange protocol (based on Hyperledger Indy) covering both issuing credentials and presenting proof. These messages were implemented to enable demonstrating credential exchange amongst interoperating agents for IIW 28 in Mountain View, CA. The use of these message types continues to today (November 2019) and so they are being added as an RFC for historical completeness and to enable reference in [Aries Interop Profile](../../concepts/0302-aries-interop-profile/README.md).

## Motivation

Enables the exchange of Indy ZKP-based verifiable credentials - issuing verifiable credentials and proving claims from issued verifiable credentials.

## Tutorial

This RFC defines a minimal credential exchange protocols. For more details of a complete credential exchange protocol, see the [Issue Credentials](../0036-issue-credential/README.md) and [Present Proof](../0037-present-proof/README.md) RFCs.

### Issuing a credential:

1. The issuer sends the holder a Credential Offer
2. The holder responds with a Credential Request to the issuer
3. The issuer sends a Credential Issue to the holder, issuing the credential

### Presenting a proof:

1. The verifier sends the holder/prover a Proof Request
2. The holder/prover constructs a proof to satisfy the proof requests and sends the proof to the verifier

## Reference

The following messages are supported in this credential exchange protocol.

### Issue Credential Protocol

The process begins with a `credential-offer`. The thread decorator is implied for all messages except the first.

The <libindy json string> element is used in most messages and is the string returned from libindy for the given purpose - an escaped JSON string. The agent must process the string if there is a need to extract a data element from the JSON - for example to get the `cred-def-id` from the `credential-offer`.

Acknowledgments and Errors should be signalled via adopting the standard `ack` and `problem-report` message types, respectively.

#### Credential Offer

```jsonld
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/credential-issuance/0.1/credential-offer",
    "@id": "<uuid-offer>",
    "comment": "some comment",
    "credential_preview": <json-ld object>,
    "offer_json": <libindy json string>
}
```

#### Credential Request

```jsonld
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/credential-issuance/0.1/credential-request",
    "@id": "<uuid-request>",
    "comment": "some comment",
    "request": <libindy json string>
}
```

#### Credential Issue

``` jsonld
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/credential-issuance/0.1/credential-issue",
    "@id": "<uuid-credential>",
    "issue": <libindy json string>
}
```

### Presentation Protocol

The message family to initiate a presentation. The verifier initiates the process. The thread decorator is implied on every message other than the first message. The `ack` and `problem-report` messages are to be adopted by this message family.

#### Presentation Request

```jsonld
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/credential-presentation/0.1/presentation-request",
    "@id": "<uuid-request>",
    "comment": "some comment",
    "request": <libindy json string>
}
```

#### Credential Presentation

```jsonld
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/credential-presentation/0.1/credential-presentation",
    "@id": "<uuid-presentation>",
    "comment": "some comment",
    "presentation": <libindy json string>
}
```


## Drawbacks

The RFC is not technically needed, but is useful to have as an Archived RFC of a feature in common usage.

## Rationale and alternatives

N/A

## Prior art

N/A

## Unresolved questions

N/A

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

Name / Link | Implementation Notes
--- | ---
[Aries Framework - .NET](https://github.com/hyperledger/aries-framework-dotnet) | .NET framework for building agents of all types; [MISSING test results](/tags.md#test-anomaly)
[Streetcred.id](https://streetcred.id/) | Commercial mobile and web app built using Aries Framework - .NET; [MISSING test results](/tags.md#test-anomaly)
[Aries Cloud Agent - Python](https://github.com/hyperledger/aries-cloudagent-python) | Contributed by the government of British Columbia.; [MISSING test results](/tags.md#test-anomaly)
[OSMA - Open Source Mobile Agent](https://github.com/mattrglobal/osma) | Open SOurce mobile app built on Aries Framework - .NET; [MISSING test results](/tags.md#test-anomaly)
