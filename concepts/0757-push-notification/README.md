# 0757: Push Notification
- Authors: [Sam Curren](telegramsam@gmail.com)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2022-11-02 
- Status Note:  
- Start Date: 2022-11-02 
- Tags: [concept](/tags.md#concept)

## Summary

This RFC Describes the general concept of push notification as it applies to Aries Agents. There are a variety of push notification systems and methods, each of which is described in it's own feature RFC.

> Note: These protocols operate only between a mobile app and it's mediator(s). There is no requirement to use these protocols when mobile apps and mediator services are provided as a bundle. These protocols exist to facilitate cooperation between open source mediators and mobile apps not necessarily developed between the same parties.

## Motivation

Mobile agents typically require the use of Mediators to receive DIDComm Messages. When messages arrive at a mediator, it is optimal to send a push notification to the mobile device to signal that a message is waiting. This provides a good user experience and allows mobile agents to be responsive without sacrificing battery life by routinly checking for new messages.

## Tutorial

Though push notification is common mobile platforms, there are a variety of different systems with various requirements and mecanisms. Most of them follow a familiar pattern:

#### Setup Phase
1. Notification Sender (mediator) registers with a push notification service. This typically involves some signup procedure.
2. Notification Recipient (mobile app) registers with the push notification service. This typically involves some signup procedure. For some platforms, or for a mediator and mobile app by the same vendor, this will be accomplished in step 1.
3. Notification Recipient (mobile app) adds code (with config values obtained in step 2) to connect to the push notification service.
4. Notification Recipient (mobile app) communicates necessary information to the Notification Sender (mediator) for use in sending notifications.

#### Notification Phase
5. A message arrives at the Notification Sender (mediator) destined for the Notification Recipient (mobile app).
6. Notification Sender (mediator) calls an API associated with the push notification service with notification details, typically using the information obtained in step 4.
7. Notification Recipient (mobile app) is notified (typically via a callback function) of the notification details.
8. Notification Recipient (mobile app) then connects to the Notification Sender (mediator) and receives waiting messages.

In spite of the flow similarities between the push notification platforms, the implementations, libraries used, and general code paths vary substantially. 
Each push notification method is described in it's own protocol. This allows the protocol to fit the specific needs and terminology of the notification method it enables. Feature Discovery can be used between the Notification Sender and the Notification Recipient to discover push notification compatibility.

### Public Mediators

Some push notification methods require matching keys or secrets to be used in both sending and receiving notifications. This requirement makes these push notification methods unusable by public mediators.

Public mediators SHOULD only implement push notification methods that do not require sharing secrets or keys with application implementations.

## Push Notification Protcols

0699 - [Push Notification APNS 1.0](../../features/0699-push-notifications-apns/README.md) (Apple Push Notification Service)
   
## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

*Implementation Notes* [may need to include a link to test results](/README.md#accepted).

Name / Link | Implementation Notes
--- | ---
 | 

