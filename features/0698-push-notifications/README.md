# Aries RFC 0698: Push Notifications Protocol 1.0

- Authors: [Timo Glastra](mailto:timo@animo.id) (Animo Solutions) & [Berend Sliedrecht](mailto:berend@animo.id) (Animo Solutions)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2021-10-07
- Status Note: Initial version
- Start Date: 2021-05-05
- Tags: [feature](/tags.md#feature), [protocol](/tags.md#protocol)

## Summary

A protocol to coordinate a push notification configuration between two agents.

## Motivation

This protocol would give an agent enough information to send push notifications about specific events to a mobile device. This would be of great benefit for mobile wallets, as a holder can be notified when new messages are pending at the mediator. Mobile applications, such as wallets, are often killed and can not receive messages from the mediator anymore. Push notifications would resolve this problem.

## Tutorial

### Name and Version

URI: `https://didcomm.org/push-notifications/1.0`

Protocol Identifier: `push-notifications`

Version: `1.0`

### Key Concepts

When an agent would like to receive push notifications at record event changes, e.g. incoming credential offer, incoming connection request, etc., the agent could initiate the protocol by sending a message to the other agent.

This protocol only defines how an agent would get the token, and possibly the vendor, which is necessary for push notifications.

### Roles

This protocol has two main roles, namely notification-sender and notification-receiver. To make it possible for notification-receivers to discover which notification services a notification-sender supports, each unique service has their own role within the protocol. It is possible to support all, one, or none of the sender roles.

**native-notification-sender**
**expo-notification-sender**
**fcm-notification-sender**

**notification-receiver**

### Services

Push notifications can be sent from many kinds of services, e.g. [Expo](https://docs.expo.dev/push-notifications/sending-notifications/), [Firebase Cloud Messaging](https://firebase.google.com/docs/cloud-messaging), [Apple Push Notifications](https://developer.apple.com/documentation/usernotifications/setting_up_a_remote_notification_server).

Since these services require slightly different data, we have to accommodate for this.

In order to implement this protocol, the [get-device-info](#get-device-info) and [device-info](#device-info) messages MUST be implemented. If the implementation also wants to act as a notification-sender, one or more of the set device info messages must also be supported.

Each service, that uses their own `device_token` instead of using the native `device_token`, has their own message defined.

#### Supported Services

The protocol currently supports the following push notification services

- Any push notification service that only requires the native `device_token` and `device_vendor` (e.g. Azure Notifications Hub)
- Expo
- Firebase Cloud Messaging (fcm) (Specifically for Android AND iOS)

### Messages

When a notification-receiver wants to receive push notifications from the notification-sender, the notification-receiver has to send one of the following messages:

#### Set Native Device Info

Message to set the device info using the native device token for push notifications. If this message is supported, this means the implementation supports the `native-notification-sender` role.

```jsonc
{
  "@type": "https://didcomm.org/push-notifications/1.0/set-native-device-info",
  "@id": "<UUID>",
  "device_token": "<DEVICE_TOKEN>",
  "device_vendor": "<DEVICE_VENDOR>"
}
```

#### Set Expo Device Info

Message to set the device info for using the [Expo Push Notification Service](https://docs.expo.dev/push-notifications/sending-notifications/) and SDKs. If this message is supported, this means the implementation supports the `expo-notification-sender` role.

```jsonc
{
  "@type": "https://didcomm.org/push-notifications/1.0/set-expo-device-info",
  "@id": "<UUID>",
  "device_token": "<EXPO_TOKEN>",
  "device_vendor": "<DEVICE_VENDOR>"
}
```

#### Set Firebase Cloud Messaging Device Info

Message to set the device info for using the [Firebase Cloud Messaging Service](https://firebase.google.com/docs/cloud-messaging) (FCM) and SDKs. Android uses FCM by default, so this service is specifically targeted at using FCM for all platforms. If this message is supported, this means the implementation supports the `fcm-notification-sender` role.

```jsonc
{
  "@type": "https://didcomm.org/push-notifications/1.0/set-fcm-device-info",
  "@id": "<UUID>",
  "device_token": "<FCM_TOKEN>",
  "device_vendor": "<DEVICE_VENDOR>"
}
```

Description of the fields:

- `device_token` -- The token that is required by the notification provider
- `device_vendor` -- The vendor for the device (string, 'android', 'ios')

It is important to note that the set device info message can be used to set, update and remove the device info. To set, and update, these values the normal messages as stated above can be used. To remove yourself from receiving push notifications, you can send the same message where all values MUST be `null`. If either value is `null` a `problem-report` can be sent back with `missing-value`.

#### Get Device Info

When a notification-receiver wants to get their push-notification configuration, they can send the following message:

```jsonc
{
  "@type": "https://didcomm.org/push-notifications/1.0/get-device-info",
  "@id": "<UUID>"
}
```

#### Device Info

Response to the get device info:

```jsonc
{
  "@type": "https://didcomm.org/push-notifications/1.0/device-info",
  "device_token": "<DEVICE_TOKEN>",
  "device_vendor": "<DEVICE_VENDOR>",
  "service": "<SERVICE>"
  "~thread": {
      "thid": "<GET_DEVICE_INFO_UUID>",
  }
}
```

- `service` -- The service used to send push notifications (string, 'native', 'expo', 'fcm')

This message can be used by the notification-receiver to receive their device info, e.g., `device_token` and `device_vendor`. If the notification-sender does not have these fields for that connection, a `problem-report` can be used as a response with `not-registered-for-push-notifications`.

#### Adopted messages

In addition, the [`ack`](https://github.com/hyperledger/aries-rfcs/blob/08653f21a489bf4717b54e4d7fd2d0bdfe6b4d1a/features/0015-acks/README.md) message is adopted into the protocol for confirmation by the notification-sender. The ack message SHOULD be sent in response to any of the set-device-info messages.

### Sending Push Notifications

When an agent wants to send a push notification to another agent, the payload of the push notifications MUST include the `@type` property to indicate the message is sent by the notification-sender. Guidelines on notification messages are not defined.

```jsonc
{
  "@type": "https://didcomm.org/push-notifications",
  ...
}
```

Description of the fields:

- `@type` -- Indicator of what kind of notification it is. (This could help the notification-receiver with parsing if a notification comes from a mediator, for example)

#### Discovery

To see which services are available for any notification-sender, the [Discover Features](https://github.com/hyperledger/aries-rfcs/blob/08653f21a489bf4717b54e4d7fd2d0bdfe6b4d1a/features/0031-discover-features/README.md) protocol can be used. An example of requesting the supported services might be as follows:

```jsonc
{
  "@type": "https://didcomm.org/discover-features/1.0/query",
  "@id": "<UUID>",
  "query": "https://didcomm.org/push-notifications/1.0",
  "comment": "I'm wondering what notification services you support"
}
```

Which could return the following response if all notification services are supported:

```jsonc
{
  "@type": "https://didcomm.org/discover-features/1.0/disclose",
  "protocols": [
    {
      "pid": "https://didcomm.org/push-notifications/1.0",
      "roles": ["fcm-notification-sender", "expo-notification-sender", "native-notification-sender"]
    }
  ]
}
```

The roles in this message specified which service can be used to receive notifications from.

## Drawbacks

The RFC currently doesn't account for browser push notifications using the [Push Manager API](https://developer.mozilla.org/en-US/docs/Web/API/PushManager), sending push notifications to desktop devices, or other push notification services. Each service, device or vendor requires a considerable amount of domain knowledge. The RFC can be extended with new services over time. The `device_vendor` and `service` deliberately also support a generic string parameter, so the protocol can be extended with new services without introducing a new major protocol version.

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
