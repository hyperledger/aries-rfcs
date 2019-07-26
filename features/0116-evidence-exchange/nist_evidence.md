# ToDo

## Objectives
The goal of this protocol is to allow Holders to provider inquiring Verifiers with a secure and trusted mechanism for obtaining access to the foundational evidence that gave the Issuer the assurance to create the verifiable credential(s) that the Holder has presented to the Verifier. Evidence can be physical or digital information or documentation.

Identity proofing’s sole objective is to ensure the applicant is who they claim to be to a stated level of certitude.

## questions
1. What evidence (information or documentation) was used to establish the level of certitude necessary to allow for the issuance of verifiable credential?

2. For each identity proofing objective such as Address, Identity, Photo and Achievement, which forms of evidence were used?  

## Relevance Statement

## Vernacular

Building on [Decentralized Digital Notary (DDN) terms](./digital_notary_usecase.md#vernacular) we introduce a mapping to [NIST 800-63A Digital Identity Guidelines Terminology](https://pages.nist.gov/800-63-3/sp800-63-3.html#def-and-acr):

| Term | Definition |
| --- | --- |
| Verifiable Credential | A digital credential that is compliant with the [W3C Verifiable Credential Specification](https://w3c.github.io/vc-data-model/).
| [Derived Credentials](https://pages.nist.gov/800-63-3/sp800-63a.html#sec6) |An issued verifiable credential based on an identity proofing process over *Original Documents* or other *Derived Credentials*. |
| Credential Service Provider (CSP) |
A trusted entity that issues verifiable credentials credentials.
Either an *Issuer of Origination* for an *Original Document* or an Issuer of a *Derived Credential*. A DDN is an example of a CSP that issues *Derived Credential*. |
| Identity Evidence |
Information or documentation provided by the Holder to support the issuance of an *Original Document*. Identity evidence may be physical (e.g. a driver license) or *Digital Assertion*  |
| Identity Proofing | The process by which a CSP collects, validates, and verifies *Identity Evidence*. This process yields the attestations (claims of confidence) by which a CSP is then able to use to issue a verifiable credential. |
| Digital Assertion | A non-physical (digital) form of evidence.
Often in the form of a Digital Signature. A CSP may rely on remote service to carry out an identity proofing process and may then require the identity proofing service provider to digitally sign the content that is the subject of the assertion. |

## Assurance Levels
The NIST 800-63A Digital Identity Guidelines outline three (3) levels of identity proofing assurance. These level describe the degree of due-diligence performed during an identity proofing process. [Table 5-1 in Section 5.2 Identity Assurance Levels](https://pages.nist.gov/800-63-3/sp800-63-3.html#sec5).

|Identity Assurance Level | Applicability |
| **IAL1** | Not Applicable |
| **IAL2** | Either remote or in-person identity proofing was performed. |
| **IAL3** | In-person identity proofing was mandatory and was performed. Evidence was verified by a trained and authorized representative through examination of physical documentation.|



What type evidence was collected and how was it confirmed?


### Remote proofing
Accoring to NIST Information Technology Laboratory Workshop Report from December 2015,
[NIST Working Group Report Measuring Strength of Identity Proofing (December 2105)](https://www.nist.gov/sites/default/files/nstic-strength-identity-proofing-discussion-draft.pdf)
* corroborating authoritative sources of data
* Some instantiations of remote proofing
also include a virtual session where a user may digitally present documents for verification.

organizations that implement identity proofing generally seek to balance cost, convenience, and security for both the provider and the individual.
Examples of these tradeoffs include:
* Reducing the complexity of a remote proofing experience to improve the online experience
can result in an increased risk of false acceptance,
* Increased complexity to reduce false acceptance can result in increased abandonment and
false rejections rates that are unacceptable to some service providers, and
* Users that do not share characteristics with the expected user population (e.g., national
origin, country of residency) can lead to persons that are unable to complete proofing

### Premise
While technology advancements around identity verification are improving, business policies (most often grounded in risk mitigation) will not change at the same rate of speed. For example, just because a financial institution in Singapore is willing to rely on the KYC due-diligence processing of another institution, we should not assume that the banks in another geolocation (i.e: Hong Kong) can embrace the same level of trust. For this reason, we must enable Verifiers with the option to obtain evidence that backs any assertions made by digital credential issuers.  

Based on a *web-of-trust* and cryptographic processing techniques,   Verifiers of digital credentials can fulfill their identity proofing workflow requirements. However, business policies and regulatory compliance may require them to have evidence for inquires such as government mandated Anti Money Laundering (AML) Compliance audits.

According to a NIST Information Technology Laboratory workshop report, [Measuring Strength of Identity Proofing](https://www.nist.gov/sites/default/files/nstic-strength-identity-proofing-discussion-draft.pdf) from December 2015, there are two (2) identity proofing methods that can be leveraged by a CSP:

| Method | Description |
| --- | --- |
| In-Person Identity Proofing | Holder is required to present  themselves and their documentation directly to a trained  representative of an identity proofing agency. |
| Remote Identity Proofing  | Holder is not expected to present themselves or their documents at a physical location. Validation and verification of presented data is performed programmatically against one or more corroborating authoritative sources of data.|

### goal

Verifiers or relying parties (RPs) of digital credentials need to make informed decisions about the risk of accepting a digital identity before trusting the digital credential and granting associated privileges. To mitigate such risk, the Verifier may need to understand the strength of the identity proofing process.

If the In-Person Identity Proofing method was used, the strength can easily be determined by allowing the Verifier to gain access to the any *Original Document* used by the Issuer of a *Derived Credential*. In the situation where a Remote Identity Proofing method was used, what type of evidence can the Holder supply to the Verifier?

## concepts
