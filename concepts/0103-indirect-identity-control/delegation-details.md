# Delegation Details

Three basic approaches to delegation are possible:

1. Delegate by expressing intent in a DID Doc.
2. Delegate with verifiable credentials.
3. Delegate by sharing a wallet.

The alternative of delegating via the `authorization` section of a DID Doc
(option #1) is [unnecessarily fragile, cumbersome, redundant, and expensive to implement](
https://docs.google.com/presentation/d/1-nEPpomAhhm6HPZf9C1o-rEljSNNKj-i4NuXjIW8BLI/edit#slide=id.g572b6fbf26_0_69).
The theory of delegation with DIDs and credentials has been explored thoughtfully
in many places (see [Prior Art and References](#prior-art-and-references)). The emergent consensus is:

* __Formal delegation is best accomplished with a credential__ (option 2). This creates an audit
trail, makes it possible to declare and enforce limits on what the delegate can do,
takes advantage of standard verification and revocation features, and makes recursive
delegation possible but not automatic.

* __Informal__ (undeclared, invisible) __delegation could be accomplished
by granting access to a shared wallet__ (option 3). However, this [introduces risks of
abuse](https://docs.google.com/presentation/d/1-nEPpomAhhm6HPZf9C1o-rEljSNNKj-i4NuXjIW8BLI/edit#slide=id.g572b6fbf26_0_63)
that make it unsuitable for use cases requiring high standards of
security, accountability, and privacy.

## Use Cases

The following use cases are good tests of whether we're implementing delegation
properly.

### 1. Thrift Bank Employees

Thrift Bank wishes to issue employee credentials to its employees, giving them delegated
authority to perform certain actions on behalf of the bank (e.g., open their till, unlock
the front door, etc). Thrist has a DID, but wishes to grant credential-issuing authority
to its Human Resources Department (which has a separate DID). In turn, the HR department
wishes to further delegate this authority to the Personnel Division. Inside of the Personnel
division, three employees, Cathy, Stan, and Janet will ultimately be responsible for issuing
the employee credentials.

* Cathy, Stan, and Janet should not have the ability to further delegate the authority.
* The employee credentials should include the proof of delegated authority.
* Revocation of the authority to issue the employee credential should be possible at any point along the chain of delegation
* Proving non-revocation of delegated authority should be possible by Cathy, Stan, and Janet without the need for the Bank, HR, or Personnel to be involved.
* Revoking the authority to issue the credential should not invalidate the issued employee credentials.

### 2. U-Rent-a-Car

U-Rent-a-Car is a multinational company that owns a large fleet of vehicles.
Its national headquarters issues a credential, C1, to its regional office in Quebec, authorizing
U-Rent-a-Car Quebec to delegate driving privileges to customers, for cars owned by the parent
company. Alice rents a car from U-Rent-a-Car Quebec. U-Rent-a-Car Quebec issues a driving privileges
credential, C2, to Alice. C2 gives Alice the privilege to drive the car from Monday through Friday
of a particular week. Alice climbs in the car and uses her C2 credential to prove to the car (which
acts as verifier) that she is an authorized driver. She gets pulled over for speeding on Wednesday
and uses C2 to prove to the police that she is the authorized driver of the car. On Thursday night
Alice goes to a fancy restaurant. She uses valet parking. She issues credential C3 to the valet,
allowing him to drive the car within 100 meters of the restaurant, for the next 2 hours while she
is at the restaurant. The valet uses this credential to drive the car to the parking garage. While
Alice eats, law enforcement goes to U-Rent-a-Car Quebec with a search warrant for the car. The law
enforcement agency has discovered that the previous driver of the car was a criminal. It asks
U-Rent-a-Car Quebec to revoke C2, because they don’t want the car to be driven any more, in case
evidence is accidentally destroyed. At the end of dinner, Alice goes to the valet and asks for her
car to be returned. The valet goes to the car and attempts to open the door using C3. The car tests
the validity of the delegation chain of C3, and discovers that C2 has been revoked, making C3 invalid.
The car refuses to open the door. Alice has to take Uber to get home. Law enforcement officials take
possession of the car.

### 3. Acme Departments

Acme wants its HR department to issue Acme Employment Credentials, its Accounting department to issue
Purchase Orders and Letters of Credit, its Marketing department to officially sign press releases,
and so forth. All of these departments should be provably associated with Acme and acting under Acme’s
name in an official capacity.

### 4. Members of an LLC

Like [#3](#3-acme-departments), but simpler. 3 or 4 people each need signing authority for the LLC,
so LLC delegates that authority.

### Approaches to recursive delegation
TODO
1. Root authority delegates directly at every level.
2. Follow the chain
3. Embed the chain

### Revocation
[TODO]

### Infra-identity Delegation
TODO

## Prior Art and References

All of the following sources have contributed valuable thinking about delegation:

* "[Traversing the Web of Trust: A Protocol for Trusting the Issuer of a Verifiable Credential](
https://docs.google.com/document/d/1nYq0iakgtyC21oUGWa5hLuJUoKeJFpURtGz6HcLIltY/edit)", by Stephen Curran, Feb 2018.
* "[Delegation of Authority for Organizations + Services w/DID’s + VerfCreds](https://iiw.idcommons.net/Delegation_of_Authority_for_Organizations_%2B_Services_w/DID%E2%80%99s_%2B_VerfCreds) (IIW session, April 2018)
* "[Digital Identity: A Chain of Claims](https://medium.com/@trbouma/digital-identity-a-chain-of-claims-70fee8519d3d)",
by Tim Bouma, May 2018. (See also several other posts by Tim about his work on the Pan-Canadian Trust
Framework.)
* [Appendix C of the W3C Verifiable Credentials Spec](https://w3c.github.io/vc-data-model/#subject-holder-relationships)
* [Object Capabilities for Linked Data](https://w3c-ccg.github.io/ocap-ld/)
* [Section 5.3 of the DID Spec](https://w3c-ccg.github.io/did-spec/#authorization-and-delegation)
* "[Delegation Concepts in Sovrin](https://docs.google.com/presentation/d/1-nEPpomAhhm6HPZf9C1o-rEljSNNKj-i4NuXjIW8BLI/edit)"
* "[Human Agency Has a Standard](https://docs.google.com/document/d/112GrR_i7HgstckRSiamlpu6scLV4dqroImFAjwDmFUI/edit)", by Adrian Gropper