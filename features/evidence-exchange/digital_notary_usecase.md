# Decentralized Digital Notary

## Preface
The intent of this document is to describe the concepts of a *Digital Notary* with respect to the bootstrapping of the decentralized identity ecosystem and to demonstrate using example user stories the applicability of the [Evidence Exchange Protocol](./README.md).  

## Overview

### Problem Statement
How do we bootstrap the digital credential ecosystem when many of the issuing institutions responsible for foundational credentials (i.e.: brith certificate, drivers license, etc) [tend to be laggards](#commentary) when it comes to the adoption of emerging technology? What if we did not need to rely on these issuing institutions and instead leveraged the attestations of [trusted third parties](https://en.m.wikipedia.org/wiki/Trusted_third_party)?

### Vernacular

| Term | Definition |
| --- | --- |
| Original Document | Any issued artifact that satisfies the [Original-Document Rule](https://definitions.uslegal.com/o/original-document-rule/) in accordance with [principle of evidence law](https://en.wikipedia.org/wiki/Evidence_(law)). The original artifact may be in writing or a mechanical, electronic form of publication. |
| Issuer of Origination | The entity (business, organization, individual or government) that is the original publisher of an *Original Document*. |
| Tier 1 Proofs | A category of [foundational credentials](./README.md#kyc-document-types) (*Original Documents*) that are often required to prove identity and address during KYC or onboarding processes. |
| Decentralized Digital Notary (DDN) | A trusted third party that enables digital interactions between Holders and Verifiers. As an issuer of digitally verifiable credentials, it creates permanent evidence that an *Original Document* existed in a certain form at a particular point in time. This role will be especially important to address scalability and the bootstrapping of the decentralized identity ecosystem since many *Issuers of Origination* may be laggards. |
| DDN Insurer | An entity (party) in an insurance contract that underwrites insurance risks associated with the activities of a DDN. This includes a willingness to pay compensation for any negligence on the part of the DDN for failure to perform the necessary due-diligence associated with the examination and vetting of *Original Documents*. |
| Trust Framework Certification Authority | An entity that adheres to a governance framework for a specific ecosystem and is responsible for overseeing and auditing the Level of Assurance a DDN (Relying Party) has within the ecosystem. |
| Mobile Field Agents | Location-based service providers that allow agencies to bring their services to remote (rural) customers. |

### Concept
During the identity verification process, an entity may require access to the genesis documents from the Issuers of Origination before issuing credentials. We see such requirements in some of the routine identity instrument interactions of our daily lives such as obtaining a Driver's License or opening a Bank Account.

![clm-examiner](./img/clm_examiner.png)

We assume that government agencies such and the [DMV](https://en.wikipedia.org/wiki/Department_of_Motor_Vehicles) (*drivers license*) and Vital Records (brith certificate) will not be early adopters of digital credentials yet their associated [Tier 1 Proofs](#vernacular) are critical to the the creation of a network effect for the digital credential ecosystem.

We therefore need a forcing function that will disrupt behavior. Image a trusted business entity, a Decentralized Digital Notary (DDN), that would take the responsibility of vouching for the existence of *Original Documents* and have the certitude to issue verifiable credentials attesting to personal data claims made by the *Issuer of Origination*.

![ddn_concept](./img/ddn_concept.png)

Today (*blue shaded activity*), an individual receives *Original Documents* from issuing institutions and presents these as evidence to each Verifier. Moving forward (*beige shaded activity*), a [wide range of businesses](#applicable-businesses) consider acting as DDNs, our reliance on *Issuers of Origination* to be the on-ramps for an individuals digital identity experience diminishes. Overtime, our dependency on the proactive nature of such institutions becomes mute and the more successful DDNs become the more reactionary these institutions will need to be to protect their value in the ecosystem.

### Applicable Businesses

Any entity that has the breath and reach to connect with consumers at scale would be an ideal candidate for the role of a DDN. Some examples include:

* Retail Banks
* Credit Unions
* Regional Rural Banks (India)
* Mobile Field Agents
* Background Screening Service Providers

The monetization opportunities for such businesses also vary. The linkages between proof-of-identity and proof-of-value can be achieved in several manners:

1. Individual pays for issuance of certificates
1. Verifier pays the underwriter with a payment instrument (i.e.: fiat or cryptocurrency). The payment is for the service of underwriting the screening of an individual so that the Verifier does not have to do it. 

## Stories
Presented herein are a series of user stories that incorporate the concepts of a DDN and the ability of a verifier to gain access to Issuer vetted KYC documents using the [Evidence Exchange Protocol](./README.md).

The stories focus on the daily lifecycle activities of a single individual who needs to open a brokerage account and also apply a Life Insurance Policy.

### Persona
| Name | Role |
| --- | --- |
| Stacy | An individual that desire to open a brokerage account and also apply a Life Insurance Policy. |
| Retail Bank | DDN (Issuer) |
| Thomas | Notary at the Retail Bank famialir with the DDN Process. |
| Brokerage Firm | Verifier |
| Dropbox | Document Management Service |

### Document Examination Process

#### Retail Bank (DDN Awareness)
Stacy is a member of her neighborhood Retail Bank. She received an email notification that as a new member benefit, the bank is now offering members with the ability to begin their digital identity journey. Stacey is given access to literature describing the extend to the bank's offering and a video of the process for how to get started. Stacey watches the video, reads the online material and decides to make an appointment with her local bank notary and fill out the preliminary online forms.

#### Retail Bank (Paper Vetting Process)
Stacey attends her appointment with Thomas. She came prepared to request two digital credentials for the following *Official Documents*: SSN, Birth Certificate, proof of employment (paystub) and proof of address (utility bill). Thomas explains to Stacey that given the types of KYC Documents she desires to be digitally notarized, bank policy is to issue a single digital credential that attests to all the personal data she is prepared to present. The bank refers to this verifiable credential as the *Basic KYC Credential* and they use a common schema that is used by many DDNs in teh Sovrin ecosystem.

>Note: This story depicts one approach. Clearly, the bank's policy could be to have a schema and credential for each *Original Document*.  

Stacy supplied Thomas with the paper based credentials for each of the aforementioned documents. Thomas scans each document and performs the necessary vetting process according to business policies. Thomas explains that while the bank is can issuer Stacey her new digital credential for a fee of $10 USD renewable annually, access to her scanned documents would only be possible if she opt-in to the digital document management service on her online banking account. Through this support she is able to provide digital access to the scanned copies of her paper credentials that were vetted by the bank. Stacey agrees to opt-in.

While Stacey is waiting for her documents to be digitally notarized, she downloads, installs and configures a Wallet App on her smartphone from the list of apps recommended by the bank. Upon completion of the vetting process, Thomas returns all *Original Document* back t Stacey and explains to her where she can now request the delivery of her new digital credential in her online account. Stacey leave the bank with her first digital credential on her device.

#### Retail Bank (Hybrid Vetting Process)
During Stacey's preparation activity when she was filling out the  preliminary online forms before her appointment with Thomas, she remembered that she had scanned her recent proof of employment (paystub) and proof of address (utility bill) at home and stored them on her Dropbox account. She decides to use the section of the form to grant the bank access (url and password) to these files. When she attends her appointment with Thomas, the meeting is altered only by the fact that she has limited her requirement of physical document presentment. However, Thomas does explain to her that bank policy is that the bank does not use remote links in their digital document management service. Instead, the bank uses the Dropbox link to obtain a copy, perform the vetting process and then store the copy in-house and allow Stacey to gain access to a link for the document stored at the bank.  

#### Credential Management
Later that evening, Stacey decides to explore her new Digital Credential features within her online bank account. She sees that she has the ability to request access to the vetted resources the bank has used to vouch for her digital identity. She opens her Wallet App and sends a `evidence_request` message to the bank. Within a few seconds she receives and processes the bank's `evidence_response` message. Her Wallet App allows her to view the evidence available to her:

| Issuer | Credential | Evidence Type | Original Document |
| --- | --- | --- | --- |
| Retail Bank | Basic KYC Credential | Address | Utility Bill |
| Retail Bank | Basic KYC Credential | Address | Employment PayStub |
| Retail Bank | Basic KYC Credential | Identity | SSN |
| Retail Bank | Basic KYC Credential | Identity | Birth Certificate |
| Retail Bank | Basic KYC Credential | Photo | Bank Member Photo |

### Verification Process

#### Brokerage Account (*Credential Exchange Evidence*)
Stacey decides she will open a new brokerage account with a local Brokerage Firm. She opens the firms account registration page using her laptop web browser. The firm allows her to establish a new account and obtain a brokerage member credential if she can provide digitally verifiable proof of identity, address and employment. Stacey clicks to begin the onboarding process. She scans a QRCode using her Wallet App and accepts a connection request from the firm. She then responds to a proof request using the Wallet and her Retail Bank credential. Upon verification of her proof response, the firm
sends Stacey an offer for a *Brokerage Membership Credential* which she accepts. The firm also sends her `evidence_access_request` and an explanation that the firm's policy for regulatory reasons is to obtain access to the proof that KYC due-diligence was performed for Address, Identity and Photo. Stacey uses her Wallet App to instruct her Cloud Agent to send an `evidence_access_response`.

#### Life Insurance Policy (*DIDComm Doc Sharing*)
Stacey receives notification from her Insurance Company that they require an update to her life insurance policy account. The firm has undertaken a digital transformation strategy that impacts her 15yr old account. She has been given access to a new online portal and the choices on how to supply digital copies of her SSN and Birth Certificate. Stacey is too busy to take time to visit the Insurance Company to provide *Original Documents* for their vetting and digitization. She decides to submit her notarized digital copies.  She opens the companies account portal page using her laptop web browser. Stacey registers, signs in and scans a QRCode using her Wallet App. She accepts a connection request from the firm. She then responds to `evidence_access_request` for proof of that KYC due-diligence was performed for Identity and Photo. Stacey uses her Wallet App to instruct her Cloud Agent to send an `evidence_access_response`.

## Commentary

1. This concepts of a digital notary can be applied today in application domains such as indirect auto lending, title management (auto, recreational vehicle, etc).
2. Since 2015, [AAMVA](https://www.aamva.org/mDL-Resources/) in conjunction with [ISO JTC1/SC27/WG10 18013-5 mDL Team](https://www.iso.org/standard/69084.html) has been working on a single credential solution for cross jurisdictional use amongst DMVs. This public sector activity is a key source of IAM industry motivation for alternative solutions to Credential Lifecycle Management. Government agencies will eventually need to address discussions around technical debit investments and defacto open source standards.
