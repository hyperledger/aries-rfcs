
# RFC 0781 Trust Input Protocol
- Authors: Mathieu Glaude, Subhasis Ojha
- Status: PROPOSED
- Since: 2023-11-23
- Status Note: New RFC being proposed
- Supersedes: None
- Start Date: 2023-11-23

 ## Summary

 The Trust Input Protocol is a conceptual framework designed to assist with the making of trust decisions within digital interactions. It emphasizes the importance of both technical (cryptographic) trust and human trust. The protocol introduces the concept of "Trust Inputs," which are sources of information that assist entities in making trust decisions. For the purpose of this RFC, trust inputs may only come from Trust Registries that support DIDComm-based messaging, based on [RFC 0160: Connection Protocol](https://github.com/hyperledger/aries-rfcs/blob/main/features/0160-connection-protocol/README.md). The first use case that this framework looks to support is allowing verifiers of a digital credential proof presentation to query the authoritativeness of digital credential issuers against trust registries.

 ## Motivation
 
The primary motivation for creating a Trust Input Protocol is to address the challenges of establishing trust in digital interactions. As digital transactions become more prevalent, there's a growing need to ensure that parties can trust each other, especially in contexts where real or perceived risks are involved. Traditional cryptographic methods provide technical trust, ensuring that data hasn't been altered or falsified. However, they don't address the human aspect of trust, such as verifying the authenticity of a claim or ensuring that a claim has been issued by a recognized authority. The Trust Input Protocol aims to bridge this gap by providing a framework where parties can seek trust inputs from various sources to make informed trust decisions. Although we focus on trust registries in the short-term, we imagine this protocol being capable of allowing trust decision making entities to seek inputs from sources outside of trust registries. For this reason, we will use the broader term `trust-input`.

![Making a trust decision](https://github.com/Northern-Block/trustinputprotocol/blob/main/trust-inputs-flow.png)

This above diagram was taken from a June 29, 2023 presentation given to the Trust over IP Foundation ([Slides](https://docs.google.com/presentation/d/1UMacqKZOEXiisNMz38_47FmJBUj69XePcTg9WbUCJtw/edit?usp=sharing), [Recording](https://zoom.us/rec/share/Hx-3oOZBL_vIPgf-2I6zP7QuBdQNKki4yULa2U71-VMvIrXUrS21HBAobYKBoUV5.gDEK5BKn5yJUq7nN)).

Trust registries are authoritative sources of information that we can use as inputs to make trust decisions. In the digital credentialing world, we can imagine sometimes needing to check an authoritative source to know if a credential was issued by an authority. And the reason for a protocol? We want to make sure we avoid building proprietary solutions and rather work with the community to develop standards and protocols that can be used by any implementer.

Inspiration for this protocol was taken from [RFC 0113: Question Answer Protocol](https://github.com/hyperledger/aries-rfcs/blob/main/features/0113-question-answer/README.md). We have gone beyond this protocol by adding structure to it, since we need a standard method for requesting for authorization related to credential issuance contexts.

 ## Tutorial

 This RFC introduces a protocol for interacting with trust registries. The identifier for the message family used by this protocol is `trust-input`, and the fully qualified URI for its definition is: 
 
 *https://didcomm.org/trust-input/1.0*

  ## Roles

  There are two roles in the `trust-input` protocol: `requestor` and `trust-registry`. The `requestor` asks the `trust-registry` if credential metadata of a verifiable credential shared by a holder was issued by an authorized issuer, and the `trust-registry` responds with an answer. Any type of entity can be a requestor and inquire about the authority of an issuing entity. All the requests sent by the requestor are sent in a single message type, and the same is true for the response from the `trust-registry`.

  ## States

  This is a classic two-step request~response interaction, so it uses the predefined state machines for any `requestor` and `trust-registry`:

<img src= "https://github.com/Northern-Block/trustinputprotocol/blob/main/trust-input-states.png" width="408.16" height="300">

  ## Messages

 ### query Message Type

A trust-input-protocol/query message looks like this:

    {
    "@type": "https://didcomm.org/trust-input/1.0/query",
      	"@id": "yWd8wfYzhmuXX3hmLNaV5bVbAjbWaU",
      	"query": {
        		"trust-task":"issuance",
        		"include-governance":"yes",
        		"credentialmetadata":[
          			{
            		"credential-id": "http://university.example/credentials/1872",
    			"credential-format": "1",
            		"issuer-did": "did:example:123456abcdef"
          			}
        		]
        	},
      	"comment": "Please tell me if this issuer is authoritative to issue this credential type..."
    }

The query message says, “ Please tell me if the issuer: ‘did:example:123456abcdef’ is authorized to issue the credential: ‘http://university.example/credentials/1872’. And please give me information about the governance framework that governs the trust registry operation.” Please refer to the Localisation section below for further details.

The `requestor` can send an array of issuers and credentials in their request to the trust registry. If they’re seeking multiple trust inputs from a single trust registry, they can get them in a single request.

The values for `credential-format` are:

    1 = AnonCreds
    2 = JSON-LD
    3 = JWT

Additional formats can be supported and added to this above list.

The credential field within the requestor’s `query` may include a * wildcard. An example use of this could be “I’m interested in knowing all the credentials that this specific issuer is authorized to offer”. This may be useful for discovery purposes.

### response Message Type

A trust-input/response message looks like this:

    { 
    "@type": "https://didcomm.org/trust-input/1.0/response",
    "~thread": {
          	"thid": "yWd8wfYzhmuXX3hmLNaV5bVbAjbWaU" 
      	},
      	"governance":"http://university.example/governanceframework",
      	"response":[	
    {
          		"credential-id": "http://university.example/credentials/1872",
          		"status": "2",
            	"status_date":"yyyy'-'MM'-'dd'T'HH':'mm':'ss'.'fff'Z'"
        		}
    	]
    }

The `response` field is a JSON array of response support descriptor objects that matches the query. Each descriptor has a `credential-id` that contains a credential (fully qualified verifiable credential id), plus the current authoritative `status` of the credential issuer to issue said credential.

The response returns the current status of the credential issuer(s) against their authority to issue credentials at the time of `query`.

The values for `status` are:

    1 = Not found
    2 = Valid
    3 = Expired (not renewed after the previous valid registration period) [when was it expired]
    4 = Terminated (voluntary termination by the registered party) [when was it terminated]
    5 = Revoked [when was it revoked]

For status values 3, 4, 5; the trust registry will return a date value of when that status became that value.

A `query` which contains a *wildcard would return all the credentials offered by the issuer’s DID.
The date format returned in the response is a web UTC format. The date represents  the status changes of status values and the `requestor` can use that info to make their trust decision.

## Trust Registry Considerations

### Connection Establishment

The connection between the `requestor` and the `trust-registry` is established via an out-of-band message sent to the `requestor`. Other connection methods such as [RFC 0160](https://github.com/hyperledger/aries-rfcs/blob/main/features/0160-connection-protocol/README.md) can also be used.

### Identifier

`trust-registry` must have a resolvable Verifiable Identifier (VID).

### Governance

The trust registries that an entity using this protocol will interact with should ensure their trust registries are aligned with the [Trust over IP’s Trust Registry Governance Framework](https://github.com/trustoverip/tswg-trust-registry-tf/blob/main/v2/requirements.md#governing-authorities).

A governance document must be published to be able to respond to a request that asks for governance.

## Localization

Because the `requestor` is being returned a status number to represent the status, the implementers can use this to localise it in the language of their choice and make it friendly to their application or user experience.

The `query` message contains a `comment` field that is localizable. This field is optional and may not be often used, but when it is, it is to provide a human-friendly justification for the query. An agent that consults its master before answering a query could present the content of this field as an explanation of the request.

All message types in this family thus have the following implicit decorator:

    {
    
    "~l10n": {
	    "locales": { "en": ["comment"] },
	    "catalogs": ["https://github.com/hyperledger/aries-rfcs/features/trust-input/requestor/catalog.json"]
    
		    }
    }
 

For more information, see the [localization RFC](https://github.com/hyperledger/aries-rfcs/blob/main/features/0043-l10n/README.md).


## Open Topics

-   How to implement using [RFC 0434: Out-of-Band Protocol 1.1](https://github.com/hyperledger/aries-rfcs/blob/main/features/0434-outofband/README.md)? We plan to leave this out of scope until a further version.
- Governance on how the credential id is entered into a trust registry will be required. And this is dependent on the credential format. So there will likely be a required field in the trust registry for credential format, which would then dictate how the credential id is entered. The format for the credential metadata in the trust registry must align with the format received by the `requestor`.


## Acknowledgements

Although many people helped with the thinking behind this protocol, the authors would like to specifically thank these following people for their support and contributions:

-   British Columbia Government - Kyle Robinson and Nancy Norris
    
-   CIRA - Jacques Latour and Jesse Carter
    
-   Continuum Loop - Darrell O’Donnell
    
-   IDLab - Cosanna Preston-Idedia and Hadrien Seymour-Provencher
    
-   Trust over IP’s Trust Registry Task Force
    

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

  
| Name/Link | Implementation Notes |
|--|--|
| [nborbit.io](http://nborbit.io) | Commercial trust task orchestration application built by [Northern Block](https://northernblock.io/) using Aries Cloud Agent Python (ACA-Py). |





