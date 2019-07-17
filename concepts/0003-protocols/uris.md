# Message Type and Protocol Identifier URIs

Message types and protocols are identified with URIs that match certain
conventions.

### MTURI

A __message type URI__ (MTURI) identifies message types unambiguously.
Standardizing its format is important because it is parsed by agents that
will map messages to handlers--basically, code will look at this string and
say, "Do I have something that can handle this message type inside protocol
*X* version *Y*?" When that analysis happens, it must do more than compare
the string for exact equality; it may need to check for semver compatibility,
and it has to compare the protocol name and message type name ignoring case
and punctuation.

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

    (.*?)([a-z0-9._-]+)/(\d[^/]*)/([a-z0-9._-]+)$

A match will have captures groups of (1) = `doc-uri`, (2) = `protocol-name`,
(3) = `protocol-version`, and (4) = `message-type-name`.

The goals of this URI are, in descending priority:

* Code can use the URI to route messages to protocol
handlers using [semver rules](semver.md).

* The definition of a protocol should be tied to the URI such
that it is semantically stable. This means that once version 1.0
of a protocol is defined, its definition [should not change in
ways that would break implementations](semver.md).

* Developers can discover information about novel protocols, using
the URI to browse or search the web.

The `doc-uri` portion is any URI that exposes documentation about
protocols. A developer should be able to browse to that URI and use human intelligence
to look up the named and versioned protocol. Optionally and preferably, the
full URI may produce a page of documentation about the specific message type,
with no human mediation involved.

### PIURI

A shorter URI that follows the same conventions but lacks the
`message-type-name` portion is called a __protocol identifier URI__
(PIURI).
 
 
![PIURI structure](piuri-structure.png)
 
```ABNF
protocol-identifier-uri  = doc-uri delim protocol-name 
    "/" semver
```

Its loose matcher regex is:

    (.*?)([a-z0-9._-]+)/(\d[^/]*)/?$
    
Some examples of valid MTURIs and PIURIs include:

* `http://example.com/protocols?which=lets_do_lunch/1.0/` (PIURI with fully automated lookup of protocol docs)
* `http://example.com/message_types?which=lets_do_lunch/1.0/proposal` (MTURI)
* `https://github.com/hyperledger/indy-hipe/tree/d7879f5e/text:trust_ping/1.0/ping`
   (MTURI). Note that this URI returns a 404 error if followed directly--but
   per rules described above, the developer should browse to the doc root
   ([https://github.com/hyperledger/indy-hipe/tree/d7879f5e/text](
   https://github.com/hyperledger/indy-hipe/tree/d7879f5e/text
   )) and look for documentation on the `trust_ping/1.0` protocol.
* `did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/trust_ping/1.0/ping` (MTURI) This
   uses a DID reference to look up an endpoint named `spec` that serves
   information about protocols. (The exact syntax of DID references--URIs
   where the DID functions like a domain name, and additional info is
   fetched from a DID Doc in much the same way IP address and hostname
   definitions are fetched from a DNS record--is still being finalized.
   See the latest [DID Spec](https://w3c-ccg.github.io/did-spec/) for details.)

