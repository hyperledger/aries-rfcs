# Aries RFC 0257: Private Credential Issuance
- Authors: Daniel Hardman and Lovesh Harchandani
- Status: [PROPOSED](/README.md#proposed)
- Since: 2019-10-16
- Status Note: under study  
- Start Date: 2019-08-26
- Tags: [concept](/tags.md#concept), [protocol](/tags.md#protocol)

## Summary

This document describes an approach to let private individuals issue credentials without needing to have a public DID or credential definition on the ledger but more importantly without disclosing their identity to the credential receiver or the verifier. The idea is for the private individual to anchor its identity in a public entity (DID) like an organization. The public entity issues a credential to the private individual which acts as a permission for the private individual to issue credentials on behalf of the public entity. To say it another way, the public entity is delegating the issuance capability to the private individual. The receiver of the delegated credential (from the private individual) does not learn the identity of the private individual but only learn that the public entity has allowed this private individual to issue credentials on its behalf. When such a credential is used for a proof, the verifier's knowledge of the issuer is same as the credential receiver, it only knows identity of the public entity. The contrasts the current anonymous credential scheme used by Aries where the credential receiver and proof verifier know the identity of the credential issuer. Additionally, using the same cryptographic techniques, the private individual can delegate issuance rights further, if allowed by the public entity. 

## Motivation

As they’ve been implemented so far, verifiable credentials in general, and Indy-style credentials in particular, are not well suited to helping private individuals issue. Here are some use cases we don’t address:

#### Recommendations
Alice wants to give Bob a credential saying that he did good work for her as a plumber.

#### Testimony
Alice isn’t necessarily recommending Bob, but she’s willing to say that he was physically present at her house at 9 am on July 31.

#### Payment receipts
Bob, a private person selling a car, wants to issue a receipt to Alice, confirming that she paid him the price he was asking.

#### Agreements
Alice wants to issue a receipt to Carol, acknowledging that she is taking custody of a valuable painting and accepting responsibility for its safety. Essentially, this is Alice formalizing her half of a contract between peers. Carol wants to issue a receipt to Alice, formalizing her agreement to the contract as well. Note that consent receipts, whether they be for data sharing or medical procedures, fall into this category, but the category is broader than consent.

#### Delegation
Alice wants to let Darla, a babysitter, have the right to seek medical care for her children in Alice’s absence.

The reasons why these use cases aren’t well handled are:

#### Issuers are publicly disclosed. 
Alice would have to create a wholly public persona and DID for her issuer role--and all issuance she did with that DID would be correlatable. This endangers privacy. (Non-Indy credentials have exactly this same problem; there is nothing about ZKPs that makes this problem arise. But proponents of other credential ecosystems don't consider this risk a concern, so they may not think their credentialing solution has a problem.)

#### Issuance requires tooling, setup, and ongoing maintenance.
An issuer needs to register a credential definition and a revocation registry on the ledger, and needs to maintain revocation status. This is an expensive hassle for private individuals. (Setup for credential issuance in non-ZKP ecosystems is also a problem, particularly for revocation. However, it may be more demanding for Indy due to the need for a credential definition and due to the more sophisticated revocation model.)

## Tutorial

### Delegatable credentials as a tool

[Delegatable Credentials](https://github.com/hyperledger/aries-rfcs/tree/main/concepts/0104-delegatable-credentials) are a useful tool that we can use to solve this problem. They function like special Object Capabilities (OCAP) tokens, and may offer the beginnings of a solution. They definitely address the delegation use cases, at least. Their properties include:

* A root issuer that is willing to go through setup and maintenance hassle creates a normal Indy credential and issues it to a normal Indy holder.

* This root holder can generate a new credential, based on the first one, that extends all or part of the trust from the root credential into a new delegate credential held by a delegate holder. The process of delegating subsets of trust through new delegate credentials can be repeated as often as needed.

* Each delegate credential embeds a pre-generated proof that the delegate holder derives their authority from the root holder through an unbroken chain of delegation. This proof can use ZKP techniques that are non-correlating and non-identifying of everyone in the chain other than the root issuer. For example, it might prove that the proximate holder was an over-21 resident of a particular city, as supported by evidence from their driver’s license--and that the proximate holder received delegated authority from a root holder that was was the proximate holder’s employer. Embedding proofs of delegation in this way eliminates the need to interact with anyone in the delegation chain. The only thing that these embedded, pre-generated proofs cannot contain is proof of non-revocation. That must be tested by interacting with the blockchain.

* Only the root issuer has to go through a setup process.

* Only the root issuer, not any holders in a delegation chain, must be publicly disclosed.

* All holders can revoke anything that they delegated, by using a revocation mechanism (possibly but not necessarily on a ledger) provided by the root issuer. This registry is unusual compared to that of ordinary credentials, in that others besides the creator of the registry (delegate holders) can write to it directly.

### Applying Delegatable Credentials to Other Use Cases

Here is how we might apply delegatable credentials to the private-individuals-can-issue problem.

A new kind of issuer is needed, called a __private credential facilitator__ (__PCF__). The job of a PCF is to eliminate some of the setup and maintenance hassle for private individual issuers by acting as a root issuer in a delegatable credential chain.

On demand, a PCF is willing to issue a personal trust root (PTR) credential to any individual who asks. A PTR is a delegatable credential that points to a __delegation trust framework__ where particular delegation patterns and credential schemas are defined. The PTR grants all privileges in that trust framework to its holder. It may also contain fields that describe the holder in certain ways (e.g., the holder is named Alice, the holder has a particular birth date or passport number or credit card number, the holder has a blinded link secret with a certain value, etc), based on things that the individual holder has proved to the PCF. The PCF is not making any strong claim about holder attributes when it issues these PTR credentials; it's just adding a few attributes that can be easily re-proved by Alice in the future, and that can be used to reliably link the holder to more traditional credentials with higher bars for trust. In some ways the PCF acts like a notary by endorsing or passing along credential attributes that originated elsewhere.

For example, Alice might approach a PCF and ask for a PTR that she can use as a homeowner who wishes to delegate certain privileges in her smart home to AirBnB guests. The PCF would (probably for a fee) ask Alice to prove her name, address, and home ownership with either verifiable or non-digital credentials, agree with Alice on a trust framework that's useful for AirBnB scenarios, and create a PTR for Alice that gives Alice all privileges for her home under that trust framework.

With this PTR in hand, Alice can now begin to delegate or subdivide permissions in whatever way she chooses, without a public DID and without going through any issuer setup herself. She issues (delegates) credentials to each guest, allowing them to adjust the thermostat and unlock the front doors, but not to schedule maintenance on the furnace. Each delegated credential she issues traces its trust back to the PTR and from there, to the PCF.

Alice can revoke any credential she has delegated in this way, without coordinating either upstream or downstream. The PCF she contracted with gave her access to do this by either configuring their own revocation registry on the ledger so it was writable by Alice's DID as well as their own, or by providing a database or other source of truth where revocation info could be stored and edited by any of its customers.

This use of delegatable credentials is obvious, and helpful. But what's cooler and less obvious is that Alice can also use the PTR and delegatable credential mechanism to address non-delegation use cases. For example, she can issue a degenerate delegated credential to Bob the plumber, granting him zero privileges but attesting to Alice's 5-star rating for the job he did. Bob can use this credential to build his reputation, and can prove that each recommendation is unique because each such __recommendation credential__ is bound to a different link secret, which in turn traces back to a unique human due to the PCF's vetting of Alice when Alice enrolled in the service. If Alice agrees to include information about herself in the recommendation credential, Bob can even display credential-based recommendations (and proofs derived therefrom) on his website, showing that recommendation A came from a woman named Alice who lived in postal code X, whereas recommendation B came from a man named Bob who lived in postal code Y.

Lets consider another case where an employee issues a delegated credential on the basis of a credential issued to by the employer. Lets say the PCF is an employer. The PCF issues a PTR credential to each of its employee using which the employee can issue recommendation credentials to different 3rd party service providers associated with the employer. The recommender (employee) while issuing a recommendation credential proves that he has a valid non-revoked PTR credential from the PCF. The credential contains the id of the employee, the rating, other data and is signed by the employee's private key. The 3rd party service provider can discover the employee's public key from the employer's hosted database. Now the service provider can use this credential to create proofs which do not reveal the identity of the employee but only the employer. If the verifier wanted more protection, he could demand that the service provider verifiably encrypt the employee ID from the PTR credential for the employer such that if the employer wishes (in case of any dispute), deanonymize the employee by decrypting the encrypted employee ID.

Alice can issue __testimony credentials__ in the same way she issues __recommendation credentials__. And she can issue __payment receipts__ the same way.

### More about Reputation Management

Reputation requires a tradeoff with privacy; we haven't figured out anonymous reputation yet. If Alice's recommendation of Bob as a plumber (or her testimony that Bob was at her house yesterday) is going to carry any weight, people who see it need to know that the credential used as evidence truly came from a woman named Alice--not from Bob himself. And they need to know that Alice couldn't distort reputation by submitting dozens of recommendations or eyewitness accounts herself.

Therefore, issuance of by private individuals should start by carefully answering this question:

>What characteristic(s) of the issuer will make this credential useful?

The characteristics might include:

* A combination of the issuer’s attributes that allows verifiers to tell two different issuers apart. Let’s call these data items __distinguishing factors__.
* Any attributes of the issuer that may give her credential gravitas / relevance to future verifiers: location, proof of issuer reputation, possibly demographics. Let’s call these data items __weighting factors__.

Weighting factors are probably irrelevant to payment receipts and agreements; proofs in these use cases are about binary matching, not degree.

All of our use cases for individual issuance care about distinguishing factors. Sometimes the distinguishing factors might be fuzzy (enough to tell that Alice-1 recommending Bob as a plumber is different from Alice-2, but not enough to strongly identify); other times they have to be exact. They do need distinguishing factors, though. Where these factors could maybe be fuzzy in recommendations or  do matter, though. In many cases, the distinguishing factors need to be strongly identifying, whereas for recommendations or testimony, fuzzier distinguishing factors might  probably don’t care about weighting factors.

Distinguishing factors and weighting factors should be embedded in each delegated credential, to the degree that they will be needed in downstream use to facilitate reputation. In some cases, we may want to use verifiable encryption to embed some of them. This would allow Alice to give an eyewitness testimony credential to Bob, to still remain anonymous from Bob, but to prove to Bob at the time of private issuance that Alice's strong personal identifiers are present, and could be revealed by Alice's PCF (or a designated 3rd party) if Bob comes up with a compelling reason.


## Reference

#TODO

## Drawbacks

#TODO

## Rationale and alternatives

#TODO

## Prior art

#TODO

## Unresolved questions

#TODO
   
## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

Name / Link | Implementation Notes
--- | ---
 |  | 

