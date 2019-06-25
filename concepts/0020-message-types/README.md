# 0020: Message Types
- Name: message-types
- Authors: Daniel Bluhm <daniel.bluhm@sovrin.org>, Sam Curren <sam@sovrin.org>
- Start Date: 2018-07-06

## Status

- Status: [ACCEPTED](/README.md#rfc-lifecycle)
- Status Date: 2019-05-24
- Status Note: Supersedes [HIPE 0021 Message Types](https://github.com/hyperledger/indy-hipe/tree/master/text/0021-message-types)

## Summary

Define structure of message type strings used in agent to agent communication, describe their resolution to documentation URIs, and offer guidelines for protocol specifications.

## Motivation

A clear convention to follow for agent developers is necessary for interoperability and continued progress as a community.

## Tutorial

A "Message Type" is a required attribute of all communications sent between parties. The message type instructs the receiving agent how to interpret the content and what content to expect as part of a given message.

Types are specified within a message using the `@type` attribute:

```json
{
    `@type`:<message type string>,
    // other attributes
}
```

Message types are URIs that resolve to developer documentation for the message type, as described in [Protocol URIs](../0003-protocols/uris.md). 

We recommend that message types are ledger resolvable DIDs with an endpoint specifier and path. This allows for the document locations to be updated to a new location for a stable definition.

### Example DID and DID Document for Message Type Specification

The following was taken from a presentation by Drummond Reed during the Agent Summit. A link to this presentation can be found below in the [Reference](#reference) section.

#### Problem
How to use a DID to identify a digital object that:

1. Can be widely referenced.
2. Is cryptographically verifiable.
3. Is human readable *enough* for developers.

#### Solution
Use a full DID reference that contains a service name and path.

##### Example DID Reference
This DID reference contains a service name (`;spec`) followed by a path that expresses the semantics of an example protocol.

```
did:sov:123456789abcdefghi1234;spec/exampleprotocol/1.0/exampletype
```

#### Example DID Document
This example DID document shows a service endpoint that includes a name property (emphasized) whose purpose is to enable creation of DID references that can deterministically select that service in order to have an algorithmic transformation into a concrete URI.

```json
{
  "@context": "https://w3id.org/did/v1",
  "id": "did:example:123456789abcdefghi",
  "publicKey": [{
    "id": "did:example:123456789abcdefghi#keys-1",
    "type": "RsaSigningKey2018",
    "owner": "did:example:123456789abcdefghi",
    "publicKeyPem": "-----BEGIN PUBLIC KEY...END PUBLIC KEY-----\r\n"
  }],
  "authentication": [{
    "type": "RsaSignatureAuthentication2018",
    "publicKey": "did:example:123456789abcdefghi#keys-1"
  }],
  "service": [{
    "type": "Document",
    "name": "spec", // <--- Name property
    "serviceEndpoint": "https://sovrin.org/specs/"
  }]
}
```

#### Resolution Process
This is the full ABNF for a DID:

```ABNF
  did-reference      = did [ ";" did-service ] [ "/" did-path ] [ "?" did-query ]
                     [ "#" did-frag ]
  did                = "did:" method ":" specific-idstring
  method             = 1*namechar
  namechar           = %x61-7A / DIGIT
  specific-idstring  = idstring *( ":" idstring )
  idstring           = 1*idchar
  idchar             = ALPHA / DIGIT / "." / "-"
  did-service        = 1*servchar *( ";" 1*servchar )
  servchar           = idchar / "=" / "&"
```

The purpose of the `did-service` component that may optionally follow a DID is to enable construction of a DID reference that may be algorithmically transformed into a concrete URL to access the target resource. There are two algorithms for this transformation. Both begin with the same first step:

1. Extract the DID plus the `did-service` component from the DID reference. Call this the *DID service locator*. Call the rest of the DID reference the `service-specific` string.

#### Service Selection by ID
This algorithm MUST be used if the `did-service` component does NOT begin with the string `type=`.

2. Select the first `service` object whose id property contains an exact match to the DID service locator.
3. Select the `serviceEndpoint` property of the selected `service` object.
4. Extract the value of the `serviceEndpoint` property. Call this the *endpoint URL*.
5. Append the service-specific string to the endpoint URL.
6. The final result is the concrete URL.

##### Example
The following agent message is received with a type not known to the developer:

```json
{
    '@type': 'did:sov:123456789abcdefghi1234;spec/exampleprotocol/1.0/exampletype',
    'attr_a': 5,
    'attr_b': 'Gouda'
}
```

The `@type` is extracted, with a DID reference that resolves to the example `service` block above:

``` json
did:sov:123456789abcdefghi1234;spec/exampleprotocol/1.0/exampletype
```

A DID resolver would algorithmically transform that DID reference to the following concrete URL:

```
https://sovrin.org/specs/exampleprotocol/1.0/exampletype
```

The developer would then be able to load this URL in a browser to discover the meaning of `attr_a` and `attr_b`.

### Aries Core Message Namespace

`did:sov:BzCbsNYhMrjHiqZDTUASHg` will be used to namespace protocols defined by the community as "core protocols" or protocols that agents should minimally support.

This DID is currently held by Daniel Hardman. Ownership will be transferred to the correct entity as soon as possible.

### Protocols
Protocols provide a logical grouping for message types. These protocols, along with each type belonging to that protocol, are to be defined in future HIPEs or through means appropriate to subprojects.

#### Protocol Versioning
Version numbering should essentially follow [Semantic Versioning 2.0.0](https://semver.org/), excluding patch version
number. To summarize, a change in the major protocol version number indicates a breaking change while the minor protocol version number indicates non-breaking additions.

## Message Type Design Guidelines

These guidelines are guidelines on purpose. There will be situations where a good design will have to choose between conflicting points, or ignore all of them. The goal should always be clear and good design.

#### Respect Reserved Attribute Names

Reserved attributes are prefixed with an `@` sign, such as `@type`. Don't use this prefix for an attribute, even if use of that specific attribute is undefined.

#### Avoid ambiguous attribute names

Data, id, and package, are often terrible names. Adjust the name to enhance meaning. For example, use  `message_id` instead of `id`.

#### Avoid names with special characters

Technically, attribute names can be any valid json key (except prefixed with @, as mentioned above). Practically, you should avoid using special characters, including those that need to be escaped. Underscores and dashes [_,-] are totally acceptable, but you should avoid quotation marks, punctuation, and other symbols.

#### Use attributes consistently within a protocol

Be consistent with attribute names between the different types within a protocol. Only use the same attribute name for the same data. If the attribute values are similar, but not exactly the same, adjust the name to indicate the difference.

#### Nest Attributes only when useful

Attributes do not need to be nested under a top level attribute, but can be to organize related attributes. Nesting all message attributes under one top level attribute is not usually a good idea.

### Design Examples

**Example 1**

```json
{
    "@type": "did:example:00000;spec/pizzaplace/1.0/pizzaorder",
    "content": {
        "id": 15,
        "name": "combo",
        "prepaid?": true,
        "ingredients": ["pepperoni", "bell peppers", "anchovies"]
    }
}
```

Suggestions: Ambiguous names, unnecessary nesting, symbols in names.

**Example 1 Fixed**

```json
{
    "@type": "did:example:00000;spec/pizzaplace/1.0/pizzaorder",
    "table_id": 15,
    "pizza_name": "combo",
    "prepaid": true,
    "ingredients": ["pepperoni", "bell peppers", "anchovies"]
}
```



## Reference

- [Drummond Reed's presentation on using DIDs as message type specifiers](https://docs.google.com/document/d/1t-AsCPjvERBZq9l-iXn2xffJwlNfFoQhktfIaMFjN-c/edit#heading=h.x1wbqftasrx2)
- [Daniel Hardman's Agent Summit Notes](https://docs.google.com/document/d/1TP_7MKfuIrlY3rz4cz_tuuCFi7hdUWifeKwr5h-QTYM/edit)
- [Stephen Curran's presentation summarizing the Agent Summit](https://docs.google.com/presentation/d/1l-po2IKVhXZHKlgpLba2RGq0Md9Rf19lDLEXMKwLdco/edit)
- [DID Spec](https://w3c-ccg.github.io/did-spec/)
- [Semantic Versioning](../0003-protocols/semver.md)
- [Core Message Structure](https://github.com/hyperledger/indy-hipe/pull/17)
