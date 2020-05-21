### Message Type and Protocol Identifier URIs

Message types and protocols are identified with URIs that match certain
conventions.

#### MTURI

A __message type URI__ (MTURI) identifies message types unambiguously.
Standardizing its format is important because it is parsed by agents that
will map messages to handlers--basically, code will look at this string and
say, "Do I have something that can handle this message type inside protocol
*X* version *Y*?" When that analysis happens, it must do more than compare
the string for exact equality; it may need to check for semver compatibility.

The URI MUST be composed as follows:

![MTURI structure](mturi-structure.png)

```ABNF
message-type-uri  = doc-uri delim protocol-name 
    "/" protocol-version "/" message-type-name
delim             = "?" / "/" / "&" / ":" / ";" / "="
protocol-name     = identifier
protocol-version  = semver
message-type-name = identifier
identifier        = alpha *(*(alphanum / "_" / "-" / ".") alphanum)
```

It can be loosely matched and parsed with the following regex:

```regex
    (.*?)([a-z0-9._-]+)/(\d[^/]*)/([a-z0-9._-]+)$
```

A match will have captures groups of (1) = `doc-uri`, (2) = `protocol-name`,
(3) = `protocol-version`, and (4) = `message-type-name`.

The goals of this URI are, in descending priority:

* Code can use the URI to route messages to protocol
handlers using [semver rules](#semver-rules-for-protocols).

* The definition of a protocol should be tied to the URI such
that it is semantically stable. This means that once version 1.0
of a protocol is defined, its definition [should not change in ways that would break implementations](#semver-rules-for-protocols).

* Developers can discover information about novel protocols, using
the URI to browse or search the web.

The `doc-uri` portion is any URI that exposes documentation about
protocols. A developer should be able to browse to that URI and use human intelligence
to look up the named and versioned protocol. Optionally and preferably, the
full URI may produce a page of documentation about the specific message type,
with no human mediation involved.

#### PIURI

A shorter URI that follows the same conventions but lacks the
`message-type-name` portion is called a __protocol identifier URI__
(PIURI).

![PIURI structure](piuri-structure.png)

```ABNF
protocol-identifier-uri  = doc-uri delim protocol-name
    "/" semver
```

Its loose matcher regex is:

```regex
    (.*?)([a-z0-9._-]+)/(\d[^/]*)/?$
```

The following are examples of valid MTURIs and PIURIs:

* MTURI `did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/issue-credential/1.1/credential-offer`
  * This is the soon-to-be-deprecated URI for an Aries core protocol message type
* MTURI: `http://didcomm/issue-credential/1.1/credential-offer`
  * This is a future URI for an Aries core protocol message type (following a [community transition](../../features/0348-transition-msg-type-to-https/README.md))
* PIURI `did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/issue-credential/1.1`
* PURI: `http://didcomm/issue-credential/1.1`

As can be seen from the examples above, the `doc-uri` portion of the URIs enable protocol namespacing,
allowing anyone to publish and use their own protocols. The ones above use the namespaces claimed for
core Aries protocols. More on namespacing and the use of these URIs to find protocols specifications
can be found in the [message types RFC](../0020-message-types/README.md).