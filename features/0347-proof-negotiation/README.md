# Aries RFC 0347: Proof Negotiation

- Authors: [Philipp Rieblinger](p.rieblinger@esatus.com), [Sebastian Weidenbach](s.weidenbach@esatus.com)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2019-12-13
- Status Note: Initial proposal after discussion on rocketchat
- Supersedes: 
- Start Date: 2019-09-09
- Tags: [feature](/tags.md#feature), [protocol](/tags.md#protocol)

## Summary

This RFC proposes an extension to [Aries RFC 0037: Present Proof Protocol 1.0](https://github.com/hyperledger/aries-rfcs/tree/master/features/0037-present-proof#aries-rfc-0037-present-proof-protocol-10) by taking the concept of groups out of the [DID credential manifest](https://github.com/decentralized-identity/credential-manifest/blob/master/explainer.md) and including them in the present proof protocol. Additionally to the rules described in the credential manifest, an option to provide alternative attributes with a weight is being introduced here. Also, the possibility to include not only attributes, but also credentials and openids in a proof by using a "type" was taken from the DID credential manifest. 
The goal of this is an approach to make proof presentation more flexible, allowing attributes to be required or optional as well as allowing a choose-from-a-list scenario. 
So far, proof requests were to be replied to with a proof response that contained all attributes listed in the proof request. To this, this RFC adds a way to mark attributes as optional, so that they are communicated as nice-to-have to the user of a wallet.
 
## Motivation

We see a need in corporate identity and access management for a login process handling not only user authentication against an application, but also determining which privileges the user is being granted inside the application and which data the user must or may provide. Aries can provide this by combining a proof request with proof negotiation.

## Use Case Example

A bank needs a customer to prove they are credit-worthy using Aries-based Self-Sovereign Identity. For this, the bank wants to make the proof of credit-worthyness flexible, in that an identity owner can offer different sets and combinations of credentials. For instance, this can be a choice between a certificate of credit-worthiness from another trusted bank or alternatively a set of credentials proving ownership over real estate and a large fortune in a bank account, for example. Optionally, an Identity Owner can add certain credentials to the proof to further prove worthiness in order to be able to obtain larger loans.

## Tutorial

A proof request sent to an identity owner defines the attributes to be included in the proof response, i.e. the ones to prove. To add a degree of flexibility to the process, it is possible to request attributes as necessary (meaning they have to be included in the response for it to be valid) or to allow the identity owner to pick one of or several of multiple attributes from a list. Furthermore, attributes can be marked as optional. For users, this procedure may look like the example of a privacy-friendly access permission process shown in the manifesto of [Okuna](https://www.okuna.io/de/manifesto#privacyfriendly), an open-source social network that is still in development at the time of this writing (click on "continue with Okuna" to see said example). Backend-wise, this may be implemented as follows:

### Proof Request with attribute negotiation

This feature can be implemented building on top of the [credential manifest](https://github.com/decentralized-identity/credential-manifest) developed by the Decentralized Identity Foundation.
One feature the above concept by the Decentralized Identity Foundation lacks is a way of assigning a weight to attributes within the category "one of". It is possible that future implementations using this concept will want to prefer certain attributes over others in the same group if both are given, so a way of assigning these different priorities to attributes should be possible. Below is an the above example of a proof request to which a rule "pick_weighted" and a group D were added. Furthermore, the categories "groups_required" and "groups_optional" were added to be able to differentiate between required and optional attributes which the credential manifest did not.

Example of a proof presentation request (from verifier):

```
{
    "@type": "https://didcomm.org/present-proof/1.0/request-presentation",
    "@id": "98fd8d82-81a6-4409-acc2-c35ea39d0f28",
    "comment": "some comment",
    "request_presentations~attach": [
        {
            "@id": "libindy-request-presentation-0",
            "mime-type": "application/json",
            "data":  {
                "base64": "<yaml-formatted string describing attachments, base64url-encoded because of libindy>"
            }
        }
    ]
}
```
The base64url-encoded content above decodes to the following data structure, a presentation preview:
```
{
    "@type": "https://didcomm.org/present-proof/1.0/presentation-preview",
	"@context": "https://path.to/schemas/credentials",
	"comment":"some comment",
	"~thread": {
		"thid": "98fd8d82-81a6-4409-acc2-c35ea39d0f28",
		"sender_order": 0
	}
	"credential":"proof_request", // verifiable claims elements
	"groups_required": [ // these groups are the key feature to this RFC
			{
				"rule":"all",
				"from": ["A", "B"]
			},
			{
				"rule": "pick",
				"count": 1,
				"from": ["C"]
			},
			{
				"rule": "pick_weighted",
				"count": 1,
				"from": ["D"]
			}
		],
		"groups_optional": [
			{
				"rule": "all",
				"from": ["D"]
			}
		],
    "inputs": [
        {
			"type": "data",
			"name": "routing_number",
			"group": ["A"],
			"cred_def_id": "<cred_def_id>",
			// "mime-type": "<mime-type>" is missing, so this defaults to a json-formatted string; if it was non-null, 'value' would be interpreted as a base64url-encoded string representing a binary BLOB with mime-type telling how to interpret it after base64url-decoding
			"value": {
				"type": "string",
				"maxLength": 9
			},
		},
		{
            "type": "data",
			"name": "account_number",
			"group": ["A"], 
            "cred_def_id": "<cred_def_id>",
            "value": {
				"type": "string",
				"value": "12345678"
        },
		{
			"type": "data",
			"name": "current_residence_duration",
			"group": ["A"],
            "cred_def_id": "<cred_def_id>",
			"value": {
				"type": "number",
				"maximum": 150
			}
		},
		{
			"type": "credential",
			"group": ["C"],
			"schema": "https://eu.com/claims/IDCard",
			"constraints": {
				"subset": ["prop1", "prop2.foo.bar"],
				"issuers": ["did:foo:gov1", "did:bar:gov2"]
			}
		},
		{
			"type": "credential",
			"group": ["C"],
			"schema": "hub://did:foo:123/Collections/schema.us.gov/Passport",
			"constraints": {
				"issuers": ["did:foo:gov1", "did:bar:gov2"]
			}
			
		},
		{
			"type": "credential",
			"group": ["B"],
			"schema": ["https://claims.linkedin.com/WorkHistory", "https://about.me/WorkHistory"],
			"constraints": {
				"issuers": ["did:foo:auditor1", "did:bar:auditor2"]
			}
		},
		{
			"type": "credential",
			"group": ["B"],
			"schema": "https://claims.fico.org/CreditHistory",
			"constraints": {
				"issuers": ["did:foo:bank1", "did:bar:bank2"]
			}
		},
		{
			"type": "openid",
			"group": ["A"],
			"redirect": "https://login.microsoftonline.com/oauth/"
			"parameters": {
				"client_id": "dhfiuhsdre",
				"scope": "openid+profile"                    
			}
		},
		{
			"type": "credential",
			"group": ["D"],
			"schema": "https://some.login.com/someattribute",
			"constraints": {
				"issuers": ["did:foo:iss1", "did:foo:iss2"]
			},
			"weight": 0.8
		},
		{
			"type": "credential",
			"group": ["D"],
			"schema": "https://some.otherlogin.com/someotherattribute",
			"constraints": {
				"issuers": ["did:foox:iss1", "did:foox:iss2"]
			},
			"weight": 0.2
		}
    ],
    "predicates": [
        {
            "name": "<attribute_name>",
            "cred_def_id": "<cred_def_id>",
            "predicate": "<predicate>",
            "threshold": <threshold>
        }
    ]
}
```

### Valid Proof Response with attribute negotiation

The following data structure is an example for a valid answer to the above credential request. It contains all attributes from groups A and B as well as one credential from each C and D. Note that the provided credential from Group D is the one weighted 0.2 as the owner did not have or was not willing to provide the one weighted 0.8.

Valid proof presentation:
```
{
    "@type": "https://didcomm.org/present-proof/1.0/proof-presentation",
    "@id": "98fd8d82-81a6-4409-acc2-c35ea39d0f28",
    "comment": "some comment",
    "presentations~attach": [
        {
            "@id": "libindy-presentation-0",
            "mime-type": "application/json",
            "data": {
                "base64": "<yaml-formatted string describing attachments, base64url-encoded because of libindy>"
            }
        }
    ]
}
```
The base64url-encoded content above would decode to this data:
```
{
    "@type": "https://didcomm.org/present-proof/1.0/presentation-preview",
	"@context": "https://path.to/schemas/credentials"
	"comment":"some comment",
	"~thread": {
		"thid": "98f38d22-71b6-4449-adc2-c33ea39d1f29",
		"sender_order": 1,
		"received_orders": {did:sov:abcxyz":1}
	}
	"credential":"proof_response", // verifiable claims elements
	"inputs_provided": [
		{
			"type": "data",
			"field": "routing_number",
			"value": "123456"
		},
		{
			"type": "data",
			"field": "account_number",
			"value": "12345678"
		},
		{
			"type": "data",
			"field": "current_residence_duration",
			"value": 8
		},		
		{
			"type": "credential",
			"schema": ["https://claims.linkedin.com/WorkHistory", "https://about.me/WorkHistory"],
			"issuer": "did:foo:auditor1"
		},
		{
			"type": "credential",
			"schema": "https://claims.fico.org/CreditHistory",
			"issuer": "did:foo:bank1"
		},
		{
			"type": "openid",
			"redirect": "https://login.microsoftonline.com/oauth/"
			"client_id": "dhfiuhsdre",
			"profile": "..."
		},
		{
			"type": "credential",
			"schema": "https://eu.com/claims/IDCard"
			"issuer": "did:foo:gov1"
		},
		{
		"type": "credential",
			"group": ["D"],
			"schema": "https://some.otherlogin.com/someotherattribute",
			"issuer": "did:foox:iss1"
		}
    ],
    "predicates": [ // empty in this case
    ]
}
```
## Reference

The "@id"-Tag and thread decorator in the above JSON-messages is taken from [RFC 0008](https://github.com/hyperledger/aries-rfcs/tree/master/concepts/0008-message-id-and-threading).

## Drawbacks

If a user needs to choose from a list of credentials each time a proof request with a "pick_one"-rule is being requested, some users may dislike this, as this process requires a significant amount of user interaction and, thereby, time. This could be mitigated by an 'optional'-rule which requests all of the options the 'pick one'-rule offers. Wallets can then offer two pre-settings: "privacy first", which offers as little data and as many interactions with the user as possible, while "usability first" automatically selects the 'optional'-rule and sends more data, not asking the user before everytime. The example dialog from the Okuna manifesto referred to before shows a great way to implement this. It offers the user the most privacy-friendly option by default (which is what the GDPR requires) or the prividing of optional data. Futhermore, the optional data can be customized to include or exclude specific data.

## Rationale and alternatives

Not implementing proof negotiation would mean that Aries-based Distributed Ledgers would be limited to a binary yes-or-no approach to authentication and authorization of a user, while this proof negotiation would add flexibility.
An alternative way of implementing the proof negotiation is performing it ahead of the proof request in a seperate request and response.
The problem with not implementing this feature would be that a proof request may need to be repeated over and over again with a different list of requested attributes each time, until a list is transferred which the specific user can reply to. This process would be unnecessarily complicated and can be facilitated by implementing this here concept.

## Prior art
[RFC0037-present-proof](https://github.com/hyperledger/aries-rfcs/tree/master/features/0037-present-proof) is the foundation which this RFC builds on using groups from the [credential manifest](https://github.com/decentralized-identity/credential-manifest) by 
the decentralized identity foundation, a "format that normalizes the definition of requirements for the issuance of a credential".

## Unresolved questions

- The above proof request includes a schema ID for every credential requests. This was taken from the DID credential manifest. It may make more sense to include a credential definition ID there, as a credential could potentially be built from one credential definition but this credential definition from several schemas.
- The exact layout and syntax of the proof request above is open to debate, it was designed to stick as close as possible to existing RFCs and concepts.
- Can this feature be implemented in a way that does not break proof requests from anoncreds version 1.x?
- Writing this RFC rose the question if the length of a proof request is limited in any way. A JSON-message containing the attributes in the proof can theoretically be infinitely long. Is this being handled in any way? It may lead to overflows at some point.
- This RFC describes the negotiation of a proof inside the proof request itself. Depending on the functionality around proofs it may be more desirable to implement the proof negotiation as a seperate protocol which is used before the actual proof request.
- It might be possible to accomplish the goal of this RFC by extending the present-preview message and adding prover functionality that allows the prover to select credentials they have to satisfy the request, just as is done in the proof request/proof process, but with the specific goal of only sending back a proposal, not a proof 


## Implementations

Name / Link | Implementation Notes
--- | ---
