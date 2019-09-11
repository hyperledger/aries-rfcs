### Why not ZCAP-LD?

The object capability model is great, and ZCAP-LD is an interesting solution that exposes that goodness to the VC ecosystem. However, we had the following concerns when we first encountered its spec (originally entitled "OCAP-LD"):

* It invents a new document format type, with associated new parsing and validation logic. We wondered whether a VC itself, instead of a new type of doc, could convey an object capability. Using a VC to convey delegation, instead of a new doc type, would minimize new code and possibly give a natural adaptation path for all VC ecosystems. (In fairness to ZCAP-LD, the reuse is fairly substantial with ZCAP-LD if your VC impl is JSON-LD centric. So this concern mainly resonates for people coming from a JWT- or ZKP-centric world.)

* ZCAP-LD's mechanism for validating the non-revocation status of each credential in the delegation chain seemed to follow the same revocation checking pattern as traditional non-ZKP credentials. This results in a workflow where everyone upstream in a delegated credential chain finds out each time a credential is used, which is a privacy concern.

* We had concerns about fragility. When issuers are massive institutions that are online 24x7x365, this may not be deeply problematic, but we wanted a solution that could be used by issuers that are regularly offline.

* It wasn't obvious to us how to use ZCAP-LD when ZKPs are a desirable feature.

* We needed to integrate delegation with the concepts of guardianship and controllership (e.g., so a guardian could delegate and a delegate could be a guardian). This required some commonality among the 3 modes of proxy identity control that was not modeled in ZCAP-LD.

* We wanted to use delegation features to faciliate issuance by private individuals, while short-circuiting the relatively demanding setup that normal VC issuance requires.  

For these reasons, we spent some time working out a somewhat similar mechanism. We hope we can reconcile the two at some point. For now, though, this doc just describes our alternative path.

