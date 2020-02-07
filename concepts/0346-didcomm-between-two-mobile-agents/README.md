# 0346: DIDCOMM BETWEEN TWO MOBILE AGENTS USING CLOUD AGENT MEDIATOR
- Author: [Sukalpo Mitra](sukalpomitra@gmail.com)
- Start Date: 2019-06-23

## Status
- Status: [PROPOSED](/README.md#proposed)
- Status Date: 2019-06-23
- Status Note: ???

## Summary

Explains how one mobile edge agent can send messages to another mobile edge agent through cloud agents. The sender edge agent also determines the route of the message. The recipient, on the other hand, can consume messages at its own pace and time.

## Motivation
[motivation]: #motivation

The DIDCOMM between two mobile edge agents should be easy and intuitive for a beginner to visualize and to implement.

## Scenario

Alice sends a connection request message to Bob and Bob sends back an acceptance response. For simplicity's sake, we will only consider the cloud agents in play while sending and receiving a message for Alice.

## Cloud Agent Registration Process

A registration process is necessary for an edge agent to discover cloud agents that it can use to send a message through them. Cloud agents in the simplest form are routers hosted as a web application that solves the problem of availability by providing a persistent IP address. The Web server has a wallet of it's own storing its private key as a provisioning record, along with any information needed to forward messages to other agents. Alice wants to accept a connection invitation from Bob. But before doing so Alice needs to register herself with one or more cloud agents. The more cloud agents she registers with the more cloud agents she can use in transporting her message to Bob. To register herself with a cloud agent she visits the website of a cloud agent and simply scans a QR code.

The cloud agent registration invite looks like below

```JSON
{​
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/didexchange/1.0/cloudagentregistrationinvitation",​
    "@id": "12345678900987654321",​
    "label": "CloudAgentA",​
    "recipientKeys": ["8HH5gYEeNc3z7PYXmd54d4x6qAfCNrqQqEB3nS7Zfu7K"],​
    "serviceEndpoint": "https://cloudagenta.com/endpoint",
    "responseEndpoint": "https://cloudagenta.com/response", 
    "consumer": "b1004443feff4f3cba25c45ef35b492c",
    "consumerEndpoint" : "https://cloudagenta.com/consume"​
}​
```

The registration data is base64 encrypted and is added to alink as part of the c_a_r query param. The recipient key is the public key of "Cloud Agent A". The service endpoint is where the edge agent should send the message to. Response endpoint is where a response that is being sent to Alice should be sent to. For example, if Bob wants to send a message to Alice, then Bob should send the message to the response endpoint. Consumer endpoint is where Alice's edge agent should consume the messages that are sent to her. The "Consumer" is an identifier to identify Alice's edge agent by the cloud agent "A". This identifier is different with each cloud agent and hence provides low correlation risk. Each time an invitation QR code is generated, a new consumer id is generated. No acknowledgment is required to be sent to the cloud agent or vice versa as the consumer-generated is never repeated.

All the endpoint data and the public key of the cloud agents are then stored as non secret records in Alice's wallet with a tag "cloud-agent"

## How connection request from Alice flows to Bob

When Alice scans Bob's QR code invitation. It starts preparing the connection request message. It first queries the wallet record service for records tagged with "cloud-agent" and puts them in a list. The edge agent now randomly chooses one from the list (say Cloud Agent "A") and creates a new list without the cloud agent that is already chosen. Alice's edge agent creates the connection request message json and adds the service endpoint as the chosen cloud agent's response endpoint together with its consumer id. 

```JSON
"serviceEndpoint": "https://cloudagenta.com/response/b1004443feff4f3cba25c45ef35b492c"
```

It then packs this message by Bob's recipient key and then creates another json message structure like the below by ising the forward message type

```JSON
{​
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/routing/1.0/forward",​
    "@id": "12345678900987654321",​
    "msg": "<Encrypted message for Bob here>",
    "to": "<Service endpoint of Bob>"​
}​
```

It then packs it with the public key of cloud agent "A".

Now it randomly chooses cloud agent from the new list and keeps on repeating the process of writing the message forwarding request.

For example, say the next random cloud agent that it chooses is Cloud Agent "C". So now it creates another message forward json structure as below

```JSON
{​
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/routing/1.0/forward",​
    "@id": "12345678900987654321",​
    "msg": "<Encrypted message for Cloud Agent A>",
    "to": "<Service endpoint of Cloud Agent A>"​
}​
```
And then packs with Cloud Agent "C"'s public key.

This process happens till it has exhausted all the list of the cloud agent in the list and then sends the message to the service endpoint of the last cloud agent (say Cloud Agent "B") chosen. 
For example, the message could have randomly been packed for this path,
B->C->A where A is one of Bob's cloud agents that stores the message on the distributed log.

## Message Forwarding process by cloud agents

When the message is reached to cloud agent "B", the message is first unpacked by cliud agent "B"'s private key. It then finds out the message type is of "forward". It then processes the message by taking the value of the "message" attribute in the decrypted json and sending it to the forwardTo URI.

Thus Cloud Agent "B" unpacks the message and forward the message to Cloud Agent "C" who then again unpacks and forwards it to Cloud Agent "A". Cloud Agent "A" ultimately unpacks and forwards it to Bob's edge agent (For simplicity sake we are not describing how the message reaches Bob through Bob's registered cloud agents)

## Bob returns a response back

Bob when recives the connection request message from Alice. It then creates a connection accept response and sends the response back to Alice at the service endpoint of Alice which is 

```JSON
"serviceEndpoint": "https://cloudagenta.com/response/b1004443feff4f3cba25c45ef35b492c"
```

For simplicity sake, we are not describing how the message ends up at the above endpoint from Bob after multiple routing through Bob's cloud agents. When the message actually ends up at the service endpoint mentioned by Alice, which is the response endpoint of cloud agent "A", the cloud agent simply stores it in a [distributed log](https://)(NEEDS A LINK TO KAFKA INBOX RFC) using the consumer id as a key

## Alice consumes connection accepted response from Bob

Alice's edge agent periodically checks the consumer endpoint of all the cloud agents it has registered with. For each cloud agent, Alice passes the unique consumer id that was used in registration so that cloud agent can return the correct messages. When it does the same for cloud agent "A", it simply consumes the message from the distributed log.

# Drawbacks and Alternatives
[drawbacks]: #drawbacks
In other suggested message formatting protocol Alice would provide a list of routing keys and the endpoint of the first hop in the chain of cloud agents. That gives allice confidence that bob is forced to use the path she has provided. The proposed routing in this RFC lacks that confidence. In contrast, routing with a list of routing keys requires a lot of overhead set up before establishing a connection. This proposed routing simplifies that overhead and provides more flexibility.

# Related art
[related-art] #prior-art
Aries-rfc [Aries RFC 0046: Mediators and Relays](Aries RFC 0046: Mediators and Relays)

# Prior art
[prior-art]: #prior-art
???

# Unresolved questions
[unresolved]: #unresolved-questions
Does separation of a "service endpoint" and "Consumer endpoint" provide a point of correlation that can be avoided by handling all messages through a single service endpoint?

Can a cloud agent have their own army of servers that just basically looks into a registry of servers and randomly chooses an entry and exit node and a bunch of hops and just passes the message along. The exit node will then pass the message to the next cloud agent?  