# Aries RFC 0745: Push Notifications Expo Protocol 1.0

- Authors: [Timo Glastra](mailto:timo@animo.id) (Animo Solutions) & [Berend Sliedrecht](mailto:berend@animo.id) (Animo Solutions)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2022-07-26
- Status Note: Initial version
- Start Date: 2022-07-15
- Tags: [feature](/tags.md#feature), [protocol](/tags.md#protocol)

> Note: This protocol is currently written to support sending push notifications through [Expo's push notification service](https://docs.expo.dev/push-notifications/overview/). For sending push notification directly using APNS or FCM see the respective RFCs; [0734: Push Notifications fcm](../0734-push-notifications-fcm/README.md) and [0699: Push Notifications apns](../0699-push-notifications-apns/README.md).

## Summary

[Expo](https://expo.dev) provides tools and services on top of [React Native](https://reactnative.dev/). This RFC defines a protocol to coordinate expo push notification configuration between two agents, allowing the **notification-sender** to send push notifications through Expo's push notification service to the **notification-receiver**.

## Motivation

When mobile edge agents are offline and messages are received at the mediator, it is desired that the mediator can inform the mobile agent of pending messages. A protocol to set the push notification device info at another agent allows the mediator to send updates to the mobile agent.

## Tutorial

### Name and Version

URI: `https://didcomm.org/push-notifications-expo/1.0`

Protocol Identifier: `push-notifications-expo`

Version: `1.0`

### Key Concepts

When an agent would like to receive push notifications of pending messages, e.g. when a forward message is received at the mediator, the **notification-receiver** can register for push notifications at the **notification-sender** using the `set-device-info` message.

This protocol only defines how an agent would get the token which is necessary for push notifications.

Each platform is has its own protocol so that we can easily use [0031: Discover Features 1.0](https://github.com/hyperledger/aries-rfcs/blob/main/features/0031-discover-features/README.md) and [0557: Discover Features 2.X](https://github.com/hyperledger/aries-rfcs/blob/main/features/0557-discover-features-v2/README.md) to see which specific services are supported by the other agent.

### Roles

**notification-sender**

**notification-receiver**

The **notification-sender** is an agent who will send the **notification-receiver** notifications. The **notification-receiver** can get and set their push notification configuration at the **notification-sender**.

### Services

This RFC focusses on configuring the data necessary for pushing notifications to iOS and Android, via [Expo's Push API](https://docs.expo.dev/push-notifications/sending-notifications/)

### Messages

When a notification-receiver wants to receive push notifications from the notification-sender, the notification-receiver has to send the following message:

#### Set Device Info

Message to set the device info using the [Expo Push Token](https://docs.expo.dev/versions/latest/sdk/notifications/#getexpopushtokenasyncoptions-expotokenoptions-expopushtoken) for push notifications.

```json
{
  "@type": "https://didcomm.org/push-notifications-expo/1.0/set-device-info",
  "@id": "<UUID>",
  "device_token": "<DEVICE_TOKEN>"
}
```

Description of the fields:

- `device_token` -- The token that is required by the notification provider. Usually has the format of `ExponentPushToken[xxxxxxxxxxxxxxxxxxxxxx]` (string, null)

It is important to note that the set device info message can be used to set, update and remove the device info. To set, and update, these values the normal messages as stated above can be used. To remove yourself from receiving push notifications, you can send the same message where the `device_token` value is `null`.

#### Get Device Info

When a notification-receiver wants to get their push-notification configuration, they can send the following message:

```json
{
  "@type": "https://didcomm.org/push-notifications-expo/1.0/get-device-info",
  "@id": "<UUID>"
}
```

#### Device Info

Response to the get device info:

```json
{
  "@type": "https://didcomm.org/push-notifications-expo/1.0/device-info",
  "device_token": "<DEVICE_TOKEN>",
  "~thread": {
    "thid": "<GET_DEVICE_INFO_UUID>"
  }
}
```

This message can be used by the notification-receiver to receive their device info, e.g. `device_token`. If the notification-sender does not have this field for that connection, a `problem-report` MAY be used as a response with `not-registered-for-push-notifications`.

#### Adopted messages

In addition, the [`ack`](https://github.com/hyperledger/aries-rfcs/blob/08653f21a489bf4717b54e4d7fd2d0bdfe6b4d1a/features/0015-acks/README.md) message is adopted into the protocol for confirmation by the notification-sender. The ack message MUST be sent in response to any of the set-device-info messages.

### Sending Push Notifications

When an agent wants to send a push notification to another agent, the payload of the push notifications MUST include the `@type` property, and COULD include the `message_tag` property, to indicate the message is sent by the notification-sender. Guidelines on notification messages are not defined.

```json
{
  "@type": "https://didcomm.org/push-notifications-expo",
  "message_tag": "<MESSAGE_TAG>",
  ...
}
```

Description of the fields:

- `@type` -- Indicator of what kind of notification it is. (This could help the notification-receiver with parsing if a notification comes from another agent, for example)
- `message_tag` -- Optional field to connect the push notification to a DIDcomm message. As defined in [0334: jwe-envelope](https://github.com/hyperledger/aries-rfcs/tree/main/features/0334-jwe-envelope) or [0019: encryption-envelope](https://github.com/hyperledger/aries-rfcs/tree/main/features/0019-encryption-envelope).

## Drawbacks

Each service requires a considerable amount of domain knowledge. The RFC can be extended with new services over time.

The `@type` property in the push notification payload currently doesn't indicate which agent the push notification came from. In e.g. the instance of using multiple mediators, this means the notification-receiver does not know which mediator to retrieve the message from.

## Prior art

- This RFC is based on the implementation of the [`AddDeviceInfoMessage`](https://github.com/hyperledger/aries-framework-dotnet/blob/9bc6346a21da263083bbac8dd8227cc941c95ea9/src/Hyperledger.Aries.Routing/AddDeviceInfoMessage.cs) in Aries Framework .NET

## Unresolved questions

None

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

| Name / Link | Implementation Notes |
| ----------- | -------------------- |
|             |                      |
