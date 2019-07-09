# Decentralized Digital Notary

## Preface
The intent of this document is to describe the concepts of a *Digital Notary* with respect to the bootstrapping of the decentralized identity ecosystem and to demonstrate by example the applicability of the [Evidence Exchange Protocol](./README.md).  

## Problem Statement
How do we bootstrap the digital credential ecosystem when many of the issuing institutions responsible for foundational credentials (i.e.: brith certificate, drivers license, etc) tend to be laggards when it comes to the adoption of emerging technology? What if we did not need to rely on these issuing institutions and instead leveraged the attestations of [trusted third parties](https://en.m.wikipedia.org/wiki/Trusted_third_party)?

## Vernacular

| Term | Definition |
| --- | --- |
| Original Document | Any issued artifact that satisfies the [Original-Document Rule](https://definitions.uslegal.com/o/original-document-rule/) in accordance with [principle of evidence law](https://en.wikipedia.org/wiki/Evidence_(law)). The original artifact may be in writing or a mechanical, electronic form of publication. |
| Issuer of Origination | The entity (business, organization, individual or government) that is the original publisher of an *Original Document*. |
| Tier 1 Proofs | A category of [foundational credentials](./README.md#kyc-document-types) (*Original Documents*) that are often required to prove identity and address during KYC or onboarding processes. |
| Decentralized Digital Notary (DDN) | A trusted third party that enables digital interactions between Holders and Verifiers. As an issuer of digitally verifiable credentials, it creates permanent evidence that an *Original Document* existed in a certain form at a particular point in time. This role will be especially important to address scalability and the bootstrapping of the decentralized identity ecosystem since many *Issuers of Origination* may be laggards. |
| DDN Insurer | An entity (party) in an insurance contract that underwrites insurance risks associated with the activities of a DDN. This includes a willingness to pay compensation for any negligence on the part of the DDN for failure to perform the necessary due-diligence associated with the examination and vetting of *Original Documents*. |
| Trust Framework Certification Authority | An entity that adheres to a governance framework for a specific ecosystem and is responsible for overseeing and auditing the Level of Assurance a DDN (Relying Party) has within the ecosystem. |
| Mobile Field Agents | Location-based service providers that allow agencies to bring their services to remote (rural) customers. |

## Concept
During the identity verification process, an entity may require access to the genesis documents from the Issuers of Origination before issuing credentials. We see such requirements in some of the routine identity instrument interactions of our daily lives such as obtaining a Driver's License or opening a Bank Account.

![clm-examiner](./img/clm_examiner.png)

We assume that government agencies such and the [DMV](https://en.wikipedia.org/wiki/Department_of_Motor_Vehicles) (*drivers license*) and Vital Records (brith certificate) will not be early adopters of digital credentials yet their associated [Tier 1 Proofs](#Vernacular) are critical to the the creation of a network effect for the digital credential ecosystem.

We therefore need a forcing function that will disrupt behavior. Image a trusted business entity, a Decentralized Digital Notary (DDN), that would take the responsibility of vouching for the existence of *Original Documents* and have the certitude to issue verifiable credentials attesting to personal data claims made by the *Issuer of Origination*.

![ddn_concept](./img/ddn_concept.png)

Today (*blue shaded activity*), an individual receives *Original Documents* from issuing institutions and presents these as evidence to each Verifier. Moving forward (*beige shaded activity*), a [wide range of businesses](#applicable-businesses) consider acting as DDNs, our reliance on *Issuers of Origination* to be the on-ramps for an individuals digital identity experience diminishes. Overtime, our dependency on the proactive nature of such institutions becomes mute and the more successful DDNs become the more reactionary these institutions will need to be to protect their value in the ecosystem.






## Applicable businesses

Any entity that has the breath and reach to connect with consumers at scale would be an ideal candidate for the role of a DDN. Some examples include:

* Retail Banks
* Credit Unions
* Regional Rural Banks (India)
* Mobile Field Agents
* Background Screening Service Providers



##Persona
* Stacy: Citizen
* Issuer: Retail Bank
* Verifier A: Brokerage
* Verifier B: Insurance Exchange
* DocMgr: Dropbox

##Stories

### Document Storage

#### Retail Bank
Stacy has supplied her local Retail Bank with paper based credentials during her vetting process for creating a new account. This vetting process included SSN, Birth Certificate, proof of employment (paystub) and proof of address (utility bill). The Retail Bank offered her a new perk for her account, document management as part of her online banking features. through this support she is able to provide digital access to the scanned copies of her paper credentials that were vetted by the bank.

#### Dropbox or other file management provider
Stacy has supplied her local Retail Bank with paper based credentials during her vetting process for creating a new account. This vetting process included SSN, Birth Certificate, proof of employment (paystub) and proof of address (utility bill). The Retail Bank offered her a new perk for her account, document management as part of her online banking features. She now has the ability to provide digital access to the scanned copies of her paper credentials that were vetted by the bank via 3rd party providers like Dropbox.

### Issuance w/Consent
During the issuance for her Bank Credential, Stacy opts-in to allow her Agency URL to be included in the credential.  

### Verification

#### Voluntary Direct
During her verification process with her new stock broker, she grants her broker access to her digital documents by providing them with her Agency URL.

#### Voluntary Indirect
During her verification process with her new stock broker, she grants her broker access to her digital documents via the Agency URL in her Bank Credential.

#### Unsolicited
Stacey has decided to join an Insurance Exchange where she can benefit from Insurance Agencies fighting for her business. These agencies need access to certain data (that is not correlated) that will allow the insurance companies to compute offers without having a relationship with Stacey. Upon determination that Stacey is a candidate for an offer, the Insurance Exchange can contact Stacy's Agent and send a proof request for access to documents that will support the justification of the offer.

##Assumptions

1. Holder *must* present doc access to Verifier such that Verifier can be assured that the Issuer vetted the document.
2. Some business processes and/or regulatory compliance requirements *may* demand that a Verifier gains access to the original vetted documents of an Issuer.
3. Some Issuers *may* accept digital access links to documents as input into vetting process. This is often associated with Issuers who will accept copies of the original documents.


## Workflow

### Examination

1. Stacy hands docs to be vetted to the Retail Bank.
	1. Paper Docs
	2. Links to Digital Docs
2. Bank vets the docs and determines they are valid/authentic/compliant.
3. Bank updates Stacy's account with links to the archived docs.
4. Bank issues Stacy a Membership Credential that contains her DocMgmtServiceURL.

### Direct Voluntary Verification

1. Stacy opens an online Stock Broker Account using a webform.
2. Stacy provides DocMgmtServiceURL as part of webform
3. Broker verifier App contacts (connects) with Stacy's DocMgmtService
3. Broker receives url access to required docs.

### Indirect Voluntary Verification

1. Stacy opens an online Stock Broker Account using a webform.
2. Stacy provides Agency URL as part of webform
3. Broker sends a proof request to Stacey's Agent requesting for proof of an Examiner vouching for vetted docs.
4. Stacey responds with her Bank Membership that contains the URL of her DocMgmtServiceURL.  
5. Broker verifier App contacts (connects) with Stacy's DocMgmtService
6. Broker receives url access to required docs.

### Unsolicited Verification

1. Stacy joins the Insurance Exchange. In doing so she exchanges pairwise DIDs.
	1. She stores the DID of trusted entity connection.
	2. She provides in her DID doc, her Agent URL.
	3. She provides the exchange with meta data about herself (range of salary, geolocation, sex, etc) that can be used for determining insurance rates.
2. Insurance company determines that Stacey's DID is associated with data that is consistent with an offer they would like to make.
3. Insurance company connects with Stacy's Agent and sends a proof request for proof of an Examiner that  is willing to vouch for vetted docs.
4. Stacey responds with her Bank Membership that contains the URL of her DocMgmtServiceURL.
5. Insurance company validates docs and sends Stacey and offer.

>Notes
>
>1. These are high level flows. ZKP processing for certain vetted data will most likely be more appropriate.
>2. The pointer herein is that an Agent can provide additional Services (DID Doc ServiceURL) that can be used to redirect and handle certain consent based processing.
