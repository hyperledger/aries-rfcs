# Aries RFC 0746: Shorten URL Protocol 1.0

- Authors: [Timo Glastra](mailto:timo@animo.id) (Animo Solutions)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2022-07-26
- Status Note: Initial version
- Start Date: 2022-07-20
- Tags: [feature](/tags.md#feature), [protocol](/tags.md#protocol)

## Summary

A protocol to request a shortened URL for a given URL.

## Motivation

URL shorteners are common technology used by a variety of services. There's a lot of free to use url shorteners available, but those bring in privacy concerns and don't always support invalidating the URL. When an agent can't host shortened url themselves (e.g. in the case of a mobile edge agent), having another agent host the shortened url provides a good solution to dynamically shorten the url. This would allow agents to create QR codes of invitations that are easy to scan in size, and also allows to share the shortened with other agents out of band

> Note: Some platforms such as iOS remove the query from an url when you click on it if the query is too long. This is problematic for out of band invitations that rely on the `oob` property to be present
> in the invitation url.
> E.g. in the case of the following url: `https://my-url.com?oob=1234`, the url when clicked on will be interpreted as `https://my-url.com`.

## Tutorial

### Name and Version

URI: `https://didcomm.org/shorten-url/1.0`

Protocol Identifier: `shorten-url`

Version: `1.0`

### Roles

**url-shortener**

**long-url-provider**

The **url-shortener** is an agent who will provide the **long-url-provider** with a shortened url. The **long-url-provider** can then share this shortened link. The **url-shortener** will return the long url when the short url is fetched.

### Messages

#### Request Shortened URL

Message sent by the **long-url-provider** to the **url-shortener** to request a shortened version of an url.

```json
{
  "@type": "https://didcomm.org/shorten-url/1.0/request-shortened-url",
  "@id": "<UUID>",
  "url": "<URL>",
  "requested_validity_seconds": <INTEGER>,
  "goal_code": "<GOAL_CODE>"
}
```

Description of the fields:

- `url` -- (required) The url that should be shortened
- `requested_validity_seconds` -- (required) The time in seconds that the shortened url should be valid. If not provided, the **url-shortener** determines the validity time. The value can be set to `0` to request the shortened url to be valid indefinitely (or until the url is invalidated using the `invalidate-shortened-url` message).
- `goal_code` -- (required) A goal code that can be used to identify the purpose of the shortened url. See [Goal Codes](#goal-codes) below for supported goal codes.

When a problem occurs during the request, the **url-shortener** can send a problem report message. This RFC defines a set of problem codes that can be used to identify the problem, see [Problem Reports](#problem-codes) below.

##### Problem Codes

The `request-shortened-url` messages has a set of problem report codes speicifc to this message. It follows the semantics of [RFC 0035: Report Problem Protocol 1.x](../0035-report-problem/README.md).

| Problem Report Code       | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `validity_too_long`       | The `requested_validity_seconds` is too long for the **url-shortener**. Try again with a lower `requested_validity_seconds` value. If the `requested_validity_seconds` in the `shorten-url-request` message was `0`, it means the **url-shortener** does not allow urls to be valid indefinitely. The **url** SHOULD add a `problem_items` entry to the problem report indicating the maximum validity a **long-url-provider** can request for a shortened url: `[{ "max_validity_seconds": <INTEGER> }]` |
| `invalid_url`             | The provided url is not a valid url. The **long-url-provider** should retry with a valid url.                                                                                                                                                                                                                                                                                                                                                                                                             |
| `invalid_protocol_scheme` | The provided url uses an invalid protocol scheme (e.g. `wss`). This can either mean the **url-shortener** does not support shortening this specific scheme, or that the scheme does not support url shortening.                                                                                                                                                                                                                                                                                           |

| `invalid_goal_code` | The goal code is not a valid goal code as defined by this RFC, or the goal code is not supported by the **url-shortener**. Either way, the **long-url-provider** should use another goal code, or abort the request for a shortened url. |

##### Goal Codes

The `request-shortened-url` messages has a set of goal codes specific to this message. It follows the semantics of [RFC 0519: Goal Codes](../../concepts/0519-goal-codes/README.md).

| Goal Code       | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | Reference                                                                                                  |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------- |
| `shorten`       | Shorten an URL according to the [Standard URL Shortening](#standard-url-shortening) as described in this RFC. This is meant to be used as a generic url shortener. If you want to shorten out of band invitations, the `shortend.oobv1` and `shorten.oobv2` goal codes should be used.                                                                                                                                                                                                                                                                                                                                                                                                                                         | [Standard URL Shortening](#standard-url-shortening)                                                        |
| `shorten.oobv1` | Shorten an URL according to the URL shortening rules as defined in the [Out of Band V1 Protocol](../0434-outofband/README.md#url-shortening). This means the URL shortener MUST adhere to the url shortener rules as defined in this protocol. When this goal code is used, the `url` property in the message **MUST** include the `oob` property. If shortening an out of band invitation is desired, but doesn't need to follow the shortening rules as defined in the out of band v1 protocol the more generic `shorten` goal code can be used.                                                                                                                                                                             | [RFC 0434: Out-of-Band Protocol 1.x](../0434-outofband/README.md#url-shortening)                           |
| `shorten.oobv2` | Shorten an URL according to the URL shortening rules as defined in the [Out of Band V2 Protocol](https://identity.foundation/didcomm-messaging/spec/#short-url-message-retrieval) from the DIDComm V2 specification. This means the URL shortener MUST adhere to the url shortener rules as defined in this protocol. When this goal code is used, the `url` property in the request message **MUST** include the `_oob` property and the `shortened_url` property in the response message MUST include the `_oobid` property. If shortening an out of band invitation is desired, but doesn't need to follow the shortening rules as defined in the out of band v2 protocol the more generic `shorten` goal code can be used. | [Out of Band V2 Protocol](https://identity.foundation/didcomm-messaging/spec/#short-url-message-retrieval) |

#### Shortened URL

Message sent by the **url-shortener** to the **long-url-provider** to share the shortened url.

```json
{
  "@type": "https://didcomm.org/shorten-url/1.0/shortened-url",
  "@id": "<UUID>",
  "shortened_url": "<SHORTENED-URL>",
  "expires_time": <INTEGER>,
  "~thread": {
    "thid": "<@id of request-shortened-url>"
  }
}
```

Description of the fields:

- `shortened_url` -- (required) The shortend version of the url
- `expires_time` -- (optional) Timestamp after which the shortened url is no longer valid. For privacy reasons, the **url-shortener** MUST invalidate the shortend url after the specified timestamp. Follows the semantics of the `_time` property as defined in [RFC 0074: DIDComm Best Practices](../../concepts/0074-didcomm-best-practices/README.md#time). If not defined it means the shortened url will be valid indefinitely (or until the url is invalidated using the `invalidate-shortened-url` message).

The message MUST inclue the `~thread.thid` property with the `@id` value of the [Request Shortened URL](#request-shortened-url) message.

#### Invalidate Shortened URL

Message sent by the **long-url-provider** to the **url-shortener** to invalidate a shortened url. This is useful if the short url is no longer needed and reduces the chance of unwanted exposure. If the **long-url-provider** is authorized to invalidate the shortened url, the **url-shortener** SHOULD invalidate the url due to privacy concerns.

```json
{
  "@type": "https://didcomm.org/shorten-url/1.0/invalidate-shortened-url",
  "@id": "<UUID>",
  "shortened_url": "<SHORTENED-URL>"
}
```

Description of the fields:

- `shortened_url` -- (required) The shortened url that should be invalidated.

It is important to note the **url-shortener** MUST only invalidate the short url if the request was made by a connection authorized to do so. This doesn't necesarily have to be the same connection as the one that requested the short url, but there should be caution in who can invalidate which short url.

If the **url-shortener** has invalidated the short url, it MUST send an [Ack message](../0015-acks/README.md#ack-message) with `status` value of `OK`.

##### Problem Codes

The `invalidate-shortened-url` messages has a set of problem report codes speicifc to this message. It follows the semantics of [RFC 0035: Report Problem Protocol 1.x](../0035-report-problem/README.md).

| Problem Report Code     | Description                                                                                                                                                                                                                                                                                                                                                                                 |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `short_url_invalid`     | The `shortened_url` is invalid. This could be for a number of reasons, but most probably (a) the url is already expired, (b) the url is already invalidated, or (c) the url does not exist. The exact reason doesn't matter, as the end result is the same.                                                                                                                                 |
| `rejected_invalidation` | The **url-shortener** refuses to invalidate the shortened url. A reason for this could be that the **long-url-provider** is not authorized to invalidate the shortened url. The associated description should be very clear and hint towards what the **long-url-provider** can do to resolve the issue. This prlblem report should not be used if `short_url_invalid` can be used instead. |

#### Adopted messages

This protocol doesn't adopt any messages, but relies on the generic [RFC 0015: Ack Message](../0015-acks/README.md#ack-message) and the [RFC 0035: Report Problem Protocol 1.x](../0035-report-problem/README.md#the-problem-report-message-type). Specifc messages describe when and with what values the specific messages should be used.

#### Standard URL Shortening

The standards process for shortening an URL follows the process as used by most commercial URL shorteners.

When the shortened URL is requested, the **url-shortener** MUST respond with a status code of `301` or `302` and include a `Location` header specifcing header specifying the long url.

## Drawbacks

- Using another agent as url shortener leaks some information about the connections an agent makes to the other agent. However in the case of a mediator, where this protocol will probably be most often used, as mobile edge agents can't create shortened urls themeslves, and the mediator already keeps a list of all the registered keys from RFC 0211, this doesn't leak a lot of extra information.
- Using the mediator as a url shortener adds extra dependency on the mediator to be avaiable and act in your favor. However, as the mediator already plays a crucial role in routing messages, it doesn't add a lot of extra trust in the mediator.

## Prior art

-

## Unresolved questions

None

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

| Name / Link | Implementation Notes |
| ----------- | -------------------- |
|             |                      |
