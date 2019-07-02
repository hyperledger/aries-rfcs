# 0074: DIDComm Best Practices
- Authors: Devin Fisher, Daniel Hardman
- Start Date: 2019-01-15

## Status
- Status: [PROPOSED](/README.md#rfc-lifecycle)
- Status Date: 2019-06-10
- Status Note: This captures some tribal knowledge from the Indy
community. However, it is by no means uniformly accepted inside
that group, and it has never been shared in a larger context. Therefore,
the RFC is currently fodder for discussion.

## Summary

Identifies some conventions that are generally accepted
as best practice by developers of DIDComm software. Explains
their rationale. This document is a recommendation, not normative.

## Motivation

By design, DIDComm architecture is extremely flexible. Besides adapting
well to many platforms, programming languages, and idioms, this let us
leave matters of implementation style in the hands of developers. We
don't want framework police trying to enforce rigid paradigms.

However, some best practices are worth documenting. There is tribal
knowledge in the community that represents battle scars. Collaboration
is fostered if learning curves don't have to proliferate. Therefore,
we offer the following guidelines.

## Tutorial

### Names

Names show up in lots of places in our work. We name RFCs, concepts
defined in those RFCs, [protocols](../0003-protocols/README.md),
[message types](../0003-protocols/uris.md#mturi), keys in JSON, and
much more.

The two most important best practices with names are:

* Pick descriptive and accurate names. [Thoughtfully chosen names can
save enormous amounts of commenting and documentation](
https://codecraft.co/2012/08/28/good-code-is-named-right/).
* Be consistent.

These are so common-sense that we won't argue them. But a few other
points are worthy of comment.

#### snake_case and variants

Nearly all code uses multi-word tokens as names. Different
programming ecosystems have different conventions for managing them:
`camelCase`, `TitleCase`, `snake_case`, `kabob-case`, `SHOUT_CASE`, etc. We want
to avoid a religious debate about these conventions, and we want to leave
developers the freedom to choose their own styles. However, we also want
to avoid random variation that makes it hard to predict the correct form.
Therefore, we try to stay idiomatic in the language we're using, and many of our
tokens are defined to compare case-insensitive with punctuation omitted, so
the differences melt away. This is the case with protocol names and message type names,
for example; it means that you should interpret "TicTacToe" and "tic-tac-toe" and
"ticTacToe" as being the same protocol. If you are writing a java function for it,
by all means use "ticTacToe"; if you are writing CSS, by all means use "tic-tac-toe".

The community tries to use `snake_case` in JSON key names, even though camelCase is
slightly more common. This is not a hard-and-fast
rule; in particular, a few constructs from DID Docs leak into DIDComm, and these
use the camelCase style that those specs expect. However, it was felt that snake_case
was mildly preferable because it didn't raise the questions about acronyms that
camelCase does (is it "zeroOutRAMAlgorithm", "zeroOutRamAlgorithm", or "zeroOutRAMalgorithm"?).

The main rule to follow with respect to case is: Use the same convention as the rest
of the code around you, and in JSON that's intended to be interoperable,
use snake_case unless you have a good reason not to. Definitely use the same case conventions
as the other keys in the same JSON schema.

#### Terminology and Notation

Use terms correctly and consistently.

The [Sovrin Glossary V2](https://docs.google.com/document/d/1gfIz5TT0cNp2kxGMLFXr19x1uoZsruUe_0glHst2fZ8/edit)
is considered a definitive source of terms. We will probably move it over to Aries at some point as
an officially sponsored artifact of this group. [RFC 0006: SSI Notation](../0006-ssi-notation/README.md) is also
a definitive reference.

RFCs in general should make every effort to define new terms only when needed, to
be clear about the concepts they are labeling, and use prior work
consistently. If you find a misalignment in the terminology or notation used by RFCs,
please [open a github issue](../../github-issues.md).

#### Terseness and abbreviations

We like obvious abbreviations like "ipaddr" and "inet" and "doc" and "conn". We also
formally define abbreviations or acronyms for terms and then use the short forms as appropriate.

However, we don't value terseness so much that we are willing to give up clarity. Abbreviating
"wallet" as "wal" or "agent" as "ag" is quirky and discouraged.

#### RFC naming

RFCs that define a protocol should be named in the form `<do something>-protocol`, where
`<do-something>` is a verb phrase like `issue-credential`, or possibly a noun phrase like
`did-exchange`--something that makes the theme of the protocol obvious. The intent is to
be clear; a protocol name like "connection" is [too vague because you can do lots of things
with connections](https://docs.google.com/presentation/d/11UVwJ2xqMmXyXr2BVsjz53S-tbMUhD1tmkhzfN7KMRw/edit#slide=id.g5b1be5d0c1_0_66).

Protocol RFCs need to be [versioned thoughtfully](../../concepts/0003-protocols/semver.md).
However, we do not put version numbers in a protocl RFC's folder name. Rather, the RFC
folder contains all versions of the protocol, with the latest version documented in
README.md, and earlier versions documented in subdocs named according to version, as
in `version-0.9.md` or similar. The main README.md should contain a section of links
to previous versions. This allows the most natural permalink for a protocol to be a link
to the current version, but it also allows us to link to previous versions explicitly
if we need to.

RFCs that define a decorator should be named in the form `<decorator name>-decorator`, as
in `timing-decorator` or `trace-decorator`.

### JSON

Json is a very flexible data format. This can be nice, but it can also lead to data
modeled in ways that cause a lot of bother for some programming languages.
Therefore, we recommend the following choices.

#### No Variable Type Arrays

Every element in an array should be the same data type. This is helpful for statically and
strongly typed programming languages that want arrays of something more specific than
a base Object class. A violating example:

```JSON
[
   {
  	"id":"324234",
  	"data":"1/3/2232"
   },
   {
  	"x_pos":3251,
  	"y_pos":11,
  	"z_pos":55
   }
]
```
Notice that the first object and the second object in the array have no structure in common.

Although the benefit of this convention is especially obvious for some programming languages,
 it is helpful in all languages to keep parsing logic predictable and reducing branching
 cod epaths.

#### Don't Treat Objects as Associative Arrays

Many loosely typed programming languages conflate the concept of an associative array (dict, map)
with the concept of object. In python, for example, an object is just a `dict` with some syntactic
sugar, and python's JSON serialization handles the two interchangeably when serializing.

This makes it tempting to do the same thing in JSON. An unhappy example:

```JSON
{
    "usage": {
        "194.52.101.254": 34,
        "73.183.146.222": 55,
        "149.233.52.170": 349
    }
}
```

Notice that the keys of the `usage` object are unbounded; as the set of IP addresses grows, the set of keys
in `usage` grows as well. JSON is an "object notation", and `{...}` is a JSON _object_ -- NOT a JSON
associative array--but this type of modeling ignores that. If we model data this way, we'll end up with
an "object" that could have dozens, hundreds, thousands, or millions of keys with identical semantics
but different names. That's not how objects are supposed to work.

Note as well that the keys here, such as "192.52.101.254", are not appropriate identifiers in most programming
languages. This means that unless deserialization code maps the keys to keys in an associative array (dict, map),
it will not be able to handle the data at all. Also, this way to model the data assumes that we know how
lookups will be done (in this case, ipaddr-->number); it doesn't leave any flexibility for other access
patterns.

A better way to model this type of data is as a JSON array, where each item in the array is a tuple
of known field types with known field names. This is only slightly more verbose. It allows deserialization
to map to one or more lookup data structures per preference, and is handled equally well in strongly,
statically typed programming languages and in loosely typed languages:

```JSON
{
    "usage": [
        { "ip": "194.52.101.254", "num": 34 },
        { "ip": "73.183.146.222", "num": 55 },
        { "ip": "149.233.52.170", "num": 349 }
    ]
}
```

#### Numeric Field Properties

Json numeric fields are very flexible. As wikipedia notes in its discussion about JSON numeric primitives:

    Number: a signed decimal number that may contain a fractional part and may use exponential
    E notation, but cannot include non-numbers such as NaN. The format makes no distinction
    between integer and floating-point. JavaScript uses a double-precision floating-point format
    for all its numeric values, but other languages implementing JSON may encode numbers
    differently.

Knowing that something is a number may be enough in javascript, but in many other programming
languages, more clarity is helpful or even required. If the intent is for the number to be
a non-negative or positive-only integer, say so when your field is [defined in a protocol](
../0003-protocols/tictactoe/README.md#reference). If you know the
valid range, give it. Specify whether the field is nullable.

Per the [first guideline above about names](#names), name your numeric fields in a way that
makes it clear they are numbers: "references" is a bad name in this respect (could be a
hyperlink, an array, a string, etc), whereas "reference_count" or "num_of_refs" is much better.

#### Date Time Conventions

Representing date- and time-related data in JSON is a source of huge variation,
since the datatype for the data isn't obvious even before it's serialized.
A quick [survey of source code across industries and geos](
 https://en.wikipedia.org/wiki/System_time) shows that
dates, times, and timestamps are handled with great inconsistency outside JSON as well.
Some common storage types include:

* 32-bit (signed or unsigned) seconds since epoch (Jan 1, 1970 and Jan 1, 1980 are both used)
* 64-bit 100-nanosecond intervals since Jan 1, 1601
* Floating-point days and fractions of days since Dec 30, 1899
* Whole integer days since Jan 1, 1900
* Floating point scientific time (billions of years since big bang)
* clock ticks since OS booted
* milliseconds since OS booted

Of course, many of these datatypes have special rules about their
relationship to timezones, which further complicates matters. And timezone
handling is notoriously inconsistent, all on its own.

Some common names for the fields that store these times include:

* &lt;something&gt;Time
* &lt;something&gt;Date
* &lt;something&gt;Timestamp
* &lt;something&gt;Millis or * &lt;something&gt;Ms or &lt;something&gt;Secs

The intent of this RFC is NOT to eliminate all diversity. There are
good reasons why these different datatypes exist. However, we would like
DIDComm messages to use broadly understood naming conventions that clearly
communicate date- and time-related semantics, so that where there is
diversity, it's because of different use cases, not just chaos.

By convention, DIDComm field suffixes communicate datatype and semantics for date-
and time-related ideas, as described below. As we've stressed before,
conventions are recommendations only. However:

1. It is strongly preferred that developers not ignore these perfectly usable
conventions unless they have a good reason (e.g., a need to
measure the age of the universe in seconds in scientific notation, or a need
for ancient dates in a genealogy or archeology use case).

2. Developers should never *contradict* the conventions. That is, if a developer
sees a date- or time-related field that appears to match what's documented here,
the assumption of alignment ought to be safe. Divergence should use new
conventions, not redefine these.

Field names like "expires" or "lastmod" are
deprecated, because they don't say enough about what to expect from the values.
(Is "expires" a boolean? Or is it a date/time? If the latter, what is its
granularity and format?)

##### `_date`
Used for fields that have only date precision,
no time component. For example, `birth_date` or `expiration_date`.
Such fields should be represented as strings in ISO 8601 format
(_yyyy-mm-dd_). They should contain a timezone indicator if and only
if it's meaningful (see [Timezone Offset Notation](#timezone-offset-notation)).

##### `_time`
Used for fields that identify a moment with both date and
time precision. For example, `arrival_time` might communicate when a
train reaches the station. The datatype of such fields is a string
in ISO 8601 format (_yyyy-mm-ddTHH:MM:SS.xxx..._) using the Gregorian
calendar, and the timezone defaults to UTC. However:
* Precision can vary from minute to microsecond or greater.
* It is _strongly_ recommended to use the "Z" suffix to make UTC
  explicit: "2018-05-27 18:22Z"
* The capital 'T' that separates date from time in ISO 8601 can
freely vary with a space. (Many datetime formatters support this
variation, for greater readability.) 
* If local time is needed, [Timezone Offset Notation](#timezone-offset-notation) is used.

##### `_sched`
Holds a string that expresses appointment-style schedules
such as "the first Thursday of each month, at 7 pm". The format of
these strings is recommended to follow [ISO 8601's Repeating Intervals
notation](https://en.wikipedia.org/wiki/ISO_8601#Repeating_intervals) where possible. Otherwise, the
format of such strings may vary; the suffix doesn't stipulate a
single format, but just the semantic commonality of scheduling.


##### `_clock`
Describes wall time without reference to a date, as in `13:57`.
Uses ISO 8601 formatted strings and a 24-hour cycle, not AM/PM.

##### `_t`
Used just like `_time`, but for unsigned integer seconds since
Jan 1, 1970 (with no opinion about whether it's a 32-bit or 64-bit value).
Thus, a field that captures a last modified timestamp for a file, as
number of seconds since Jan 1, 1970 would be `lastmod_t`. This suffix
was chosen for resonance with Posix's `time_t` datatype, which has
similar semantics.

##### `_tt`
Used just like `_time` and `_t`, but for 100-nanosecond
intervals since Jan 1, 1601. This matches the semantics of the Windows
FILETIME datatype.

##### `_sec` or subunits of seconds (`_milli`, `_micro`, `_nano`)
Used for fields that tell how long something took. For example, a field
describing how long a system waited before retry might be named
`retry_milli`. Normally, this field would be represented as an unsigned
positive integer.

##### `_dur`
Tells duration (elapsed time) in friendly, calendar based
units as a string, using the conventions of [ISO 8601's Duration
concept](https://en.wikipedia.org/wiki/ISO_8601#Durations). `Y` = year,
`M` = month, `W` = week, `D` = day, `H` = hour, `M` = minute, `S` = second:
"P3Y2M5D11H" = 3 years, 2 months, 5 days, 11 hours. 'M' can be preceded
by 'T' to resolve ambiguity between months and minutes: "PT1M3S" = 1 minute,
3 seconds, whereas "P1M3S" = 1 month, 3 seconds.

##### `_when`
For vague or imprecise dates and date ranges. Fragments of
ISO 8601 are preferred, as in "1939-12" for "December 1939". The token
"to" is reserved for inclusive ranges, and the token "circa" is reserved
to make fuzziness explicit, with "CE" and "BCE" also reserved. Thus,
Cleopatra's `birth_when` might be "circa 30 BCE", and the timing of
the Industrial Revolution might have a `happened_when` of "circa 1760
to 1840".

##### Timezone Offset Notation

Most timestamping can and should be done in UTC, and should use the "Z" suffix
to make the Zero/Zulu/UTC timezone explicit.

However, sometimes the local time and the UTC time for an event are both of
interest. This is common with news events that are tied to a geo, as with the
time that an earthquake is felt at its epicenter. When this is the case,
rather than use two fields, it is recommended to use timezone
offset notation (the "+0800" in "2018-05-27T18:22+08:00"). Except for the "Z"
suffix of UTC, timezone *name* notation is deprecated, because timezones can
change their definitions according to the whim of local lawmakers, and because
resolving the names requires expensive dictionary lookup. Note that this
convention is exactly [how ISO 8601 handles the timezone issue](
https://en.wikipedia.org/wiki/ISO_8601#Time_offsets_from_UTC).

### Blobs

In general, blobs are encoded as base64 strings in DIDComm.

### Unicode

UTF-8 is our standard way to represent unicode strings in JSON and all other contexts. For casual
definition, this is sufficient detail.

For advanced use cases, it may be necessary to understand subtleties like [Unicode
normalization forms and canonical equivalence](https://unicode.org/reports/tr15/).
We generally assume that we can compare strings for equality and sort order using a
simple binary algorithm. This is approximately but (in some corner cases) not exactly
the same as assuming that text is in NFC normalization form with no case
folding expectations and no extraneous surrogate pairs. Where more precision is
required, the definition of DIDComm message fields should provide it.

### Hyperlinks

This repo is designed to be browsed as HTML. Browsing can be done directly through
github, but we may publish the content using Github Pages and/or ReadTheDocs. As
a result, some [hyperlink hygiene is observed](https://github.com/hyperledger/aries-rfcs/issues/92)
to make the content as useful as possible:

* Hyperlinks (both internal to the repo and external to it) must not be broken.
* Fragments like `#heading-title` must correctly reference a real markdown heading.
* Hyperlinks to an RFC should point to the RFC's README.md rather than to a folder
with (possibly) many documents.
* Hyperlinks from one RFC to another should be in relative form (`../features/my-rfc/README.md`),
not in absolute form (`/features/my-rfc/README.md`) or external form
(`https://github.com/hyperledger/aries-rfcs/blob/master/features/my-rfc/README.md`).
This lets us move or embed the content, and it prevents branch names from
cluttering the hyperlink.

These rules are enforced by a unit test that runs `code/check_links.py`. To run
it, go to the root of the repo and run `pytest code` -- or simply invoke the
`check_links` script directly. Normally, `check_links` does not test external
hyperlinks on the web, because it is too time-consuming; if you want that check,
add `--full` as a command-line argument. 

## Reference

- [Discussion of date and time datatypes on Wikipedia](https://en.wikipedia.org/wiki/System_time)
- [ISO 8601](https://de.wikipedia.org/wiki/ISO_8601)
- [Unicode TR 15 on Normalization Forms](https://unicode.org/reports/tr15/)
- [DIDComm's stance on JSON-LD Compatibility](../0047-json-ld-compatibility/README.md)
- [DIDComm localization](../../features/0043-l10n/README.md)

## Drawbacks

The main concern with this type of RFC is that it will produce more heat than
light -- that is, that developers will debate minutiae instead of getting stuff
done. We hope that the conventions here feel reasonable and lightweight enough
to avoid that.

## Rationale and alternatives

- If we weren't using JSON, but rather something like ProtoBuf or MsgPack, datatype handling would probably
  require less conventions, but we would still have a similar need.
- [JSON-LD allows some forms of datatype coercion](https://w3c.github.io/json-ld-syntax/#type-coercion),
  but not enough to satisfy all our requirements. It is also considered overly heavy in terms of
  parsing and validation dependencies. See [DIDComm's stance on JSON-LD Compatibility](
  ../0047-json-ld-compatibility/README.md)

## Unresolved questions

- What other conventions do we need?