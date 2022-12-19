# 0755: Overlays Capture Architecture (OCA) For Aries

- Authors: [Stephen Curran](swcurran@gmail.com)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2022-09-27
- Status Note: In the process of being implemented in several Aries Frameworks (ACA-Py, AFJ)
- Supersedes: Supersedes [0013-Overlays](/concepts/0013-overlays/README.md) as
  that RFC is/was about the OCA specification, while this covers the application of the OCA
  Specification for Aries agents.
- Start Date: 2022-09-25
- Tags: [concept](/tags.md#concept)

## Summary

[Overlays Capture Architecture](https://oca.colossi.network/) (OCA) is, per the
[OCA specification], a "standardized global solution for data capture and
exchange." Given a data structure (such as a verifiable credential), OCA allows
for the creation of purpose-specific overlays of information about that data
structure. Each overlay provides some knowledge about the overall data structure
or the individual attributes within it. The information in the overlays makes it
possible to create useful software for capturing data, displaying it and
exchanging it. While the OCA [site](https://oca.colossi.network/) and
[OCA specification] can be reviewed for
a detailed background of OCA and its various purposes, in this RFC we'll focus
on its purpose in Aries, which is quite constrained and pragmatic--a mechanism
for an issuer to provide information about a verifiable credential to allow
holder and verifier software to display the credential in a human-friendly way,
including the issuer's preferred branding. The image below shows an Aries mobile
Wallet displaying the same credential without and with OCA overlays applied in
two languages. All of the differences in the latter two screenshots from the
first come from issuer-supplied OCA data.

[OCA Specification]: https://oca.colossi.network/specification/

![Example: Using OCA in Aries Bifold](assets/bifold-oca-example.jpg)

This RFC formalizes how Aries verifiable credential issuers can make a JSON [OCA
Bundle] (a set of related OCA overlays about a base data structure) available to
holders and verifiers that includes the following information for each type of
credential they issue.

- Metadata about the credential, such as the Classification system upon which
  the credential is based.
- Metadata about the credential in multiple languages, such as its name,
  description, the name and description of the issuer and so on.
- Type, format, encoding, standard and units information about the credential's raw
  attribute data.
- Metadata about the attributes within the credential in multiple languages,
  such as a label and help text.
- A set of branding elements (logo, background image, color and so on) that
  holder and verifier software can use in displaying the credential.

The standard flow of data between participants is as follows:

- An issuer creates an OCA Bundle for each type of verifiable credential it
issues.
- During credential issuance using [RFC 0453 Issue Credential V2 v2.2 (or later)
protocol] the issuer MAY include in the protocol's `credential-offer` or
`credential` messages the OCA Bundle for the credential type as an `oca-bundle`
[issue credential supplement].
- On receipt, the holder software has full access to the OCA information
published by that issuer and can use the OCA data to display the credential for
its user(s) in the language of their choice and with credential branding from
the issuer.
- The holder MAY share the OCA Bundle with a verifier by using [RFC 0453 Issue
Credential V2 v2.2 (or later) protocol] to add the `oca-bundle` credential
supplement received from the issuer.
- On receipt, the verifier software has full access to the OCA information
published by that issuer and can use the OCA data to display the credential for
its user(s) in the language of their choice and with credential branding from
the issuer.

[RFC 0453 Issue Credential V2 v2.2 (or later)
protocol]: https://github.com/hyperledger/aries-rfcs/tree/main/features/0453-issue-credential-v2#22---addition-of-supplements
[issue credential supplement]: https://github.com/hyperledger/aries-rfcs/tree/main/features/0453-issue-credential-v2#supplements
[OCA Bundle]: https://oca.colossi.network/specification/#bundle

While the issuer providing the OCA Bundle for a credential type using the
credential supplement mechanism is the typical flow (as detailed in this RFC),
other flows, outside of the scope of this RFC are possible. See the [rationale
and alternatives section of this RFC for some
examples](#rationale-and-alternatives).

## Motivation

The core data models for verifiable credentials are more concerned about the
correct cryptographic processing of the credentials than about general
processing of the attribute data, and the user experience of those using
credentials. An AnonCreds verifiable credential contains the bare minimum of
metadata about a credential--basically, just the developer-style names for the
type of credential and the attributes within it. JSON-LD-based verifiable
credentials has the capacity to add more information about the attributes in a
credential, but the data is not easily accessed and is provided to enable
machine processing rather than improving user experience.

OCA allows credential issuers to declare information about the verifiable
credential types it issues to improve the handling of those credentials by
holder and verifier Aries agents, and to improve the on-screen display of the
credentials, through the application of issuer-specified branding elements.

## Tutorial

The tutorial section of this RFC defines the coordination necessary for an
the creation, publishing, retrieval and use of an OCA Bundle for a given
type of verifiable credential.

``` Note

In this overview, we assume the the use of OCA specifically for verifiable
credentials, and further, specifically for AnonCreds verifiable credentials. OCA
can also be used be applied to any data structure, not just verifiable
credentials, and for other verifiable credential models, such as those based on
the JSON-LD- or JWT-style verifiable credentials. As the Aries
community applies OCA to other styles of verifiable credential, we
will extend this RFC.

```

### Issuer Activities

The use of OCA as defined in this RFC begins with an issuer preparing an [OCA
Bundle] for each type of credential they issue. An OCA Bundle is a JSON data
structure consisting of the [Capture Base], and some additional overlays of
different types (listed in the [next section](#oca-specification-overlays)).

While an OCA Bundle can be manually maintained in an OCA Bundle JSON file, a
common method of maintaining OCA source data is to use a spreadsheet, and
generating the OCA Bundle from source. See the section of this RFC called [OCA
Tooling](#oca-issuer-tools) for a link to an OCA Source spreadsheet, and
information on tools available for managing OCA Source data.

The creation of the OCA Bundle and the configuration of the issuer's Aries
Framework to deliver the OCA Bundle during credential issuance should be all
that a specific issuer needs to do in using OCA for Aries. An Aries Framework
that supports OCA for Aries should handle the rest of the technical
requirements.

#### OCA Specification Overlays

All OCA data is based on a [Capture Base], which defines the data structure
described in the overlays. For AnonCreds, the Capture Base attributes MUST be
the list of attributes in the AnonCreds schema for the given credential type.
The Capture Base also MUST contain:

- the type of each attribute, based on an enumerated list of [types defined in
  the OCA
  specification](https://oca.colossi.network/v1.1.0-rc.html#attribute-type)
- a list of the base attributes that will hold Personally Identifiable
Information (PII) in an issued credential. An issuer SHOULD use the [Kantara
Initiative's Blinding Identity
Taxonomy](https://docs.kantarainitiative.org/Blinding-Identity-Taxonomy-Report-Version-1.0.html)
to identify the attributes to flag as being PII.

With the Capture Base defined, the following additional overlay types MAY be
created by the Issuer and SHOULD be expected by holders and verifiers.
Overlay types flagged "multilingual" may have multiple instances of the overlay,
one for each issuer-supported language (e.g en for English, fr French, SP
Spanish, etc.) or country-language (e.g., en-CA for Canadian English, fr-CA for
Canadian French), as defined in the [OCA Specification about
languages](https://oca.colossi.network/specification/#language).

Any overlay types that a holder or verifier does not expect MUST be ignored.

- The **[Character Encoding
overlay](https://oca.colossi.network/v1.1.0-rc.html#character-encoding-overlay)**
contains the encoding for each attribute in the capture base.
- The **[Format
overlay](https://oca.colossi.network/v1.1.0-rc.html#format-overlay)** provides
the input structure for each data attribute. The format may be useful in
displaying the data in a style expected by the user, based on the content of the
data and their language preferences. For example, displaying the elements of a
date in the user's preferred format.
- The multilingual **[Label
overlay](https://oca.colossi.network/v1.1.0-rc.html#label-overlay)** provides a
label to be used for each attribute for a given language. The label overlay also
includes labels for attributes with enumerated values (called categories in the
OCA specification). For example, a data attribute containing the codes "EN",
"FR", "SP" could have a category entries that indicate the codes correspond to
"English", "French" and "Spanish", respectively.
- The multilingual **[Information
overlay](https://oca.colossi.network/v1.1.0-rc.html#information-overlay)** provides
a description or help text about each attribute for a given language. There will
be one overlay per issuer-supported language.
- The multilingual **[Meta overlay](https://oca.colossi.network/v1.1.0-rc.html#meta-overlay)** contains
information about the credential itself, such as "name" and "description." For Aries, the meta overlay
SHOULD include the following additional name/value pairs, specific to the OCA for Aries use case:
  - `issuer` - the name of the issuer of the credential.
  - `issuer_description` - a description for the issuer of the credential.
  - `issuer_url` - a URL for the issuer of the credential.
- The **[Unit overlay](https://oca.colossi.network/specification/#unit-overlay)**
  allows the issuer to declare the units of measurement for the attributes in
  the overlay.
- The **[Standard
  Overlay](https://oca.colossi.network/specification/#standard-overlay)** indicates
  that some or all of the attributes use specific data standards populating the
  attribute in a credential. This might be used, for example, for defining
  the standard applied in populating a data attribute with a date or date/time.
  - See the [section](#aries-specific-standards-in-the-oca-standard-overlay)
    about the Aries specific date/time related standards that Aries agents
    SHOULD recognize: "dateint" and "Unix Time".

[Capture Base]: https://oca.colossi.network/v1.1.0-rc.html#capture-base

#### Aries-Specific Standards in the OCA Standard Overlay

Aries agents SHOULD recognize the attribute standards `dateint` and `Unix Time`
in the [Standard
  Overlay](https://oca.colossi.network/specification/#standard-overlay) and
apply those standards to the corresponding attributes data according to how they
are used in Aries, as outlined below.

In AnonCreds, zero-knowledge proof (ZKP) predicates (used, for example, to prove
older than a given age based on date of birth without sharing the actual date of
birth) must be based on **integers**. The Aries-specific entries used in the
Standard overlay `dateint` and `Unix Time` facilitate the use of AnonCreds
predicates for date and date/time attributes, respectively.

- "`dateint`" in the Standard overlay indicates that the specified attribute's
data is a date constructed according to the Aries `dateint` specification as
described in [Aries RFC 0592](../0592-indy-attachments/README.md). Briefly,
`dateint` is a date (YYYYMMDD) provided in a credential attribute as an integer
(for example `September 29, 2022` is the integer `20,220,929`).

- "`Unix Time`" in the Standard overlay indicates that the specified attribute's
data is a date/time timestamp constructed according to the `Unix
Time`[Unix/POSIX data standard](https://en.wikipedia.org/wiki/Unix_time) for
date/time timestamps. Briefly, `Unix Time` is a date/time represented as the
number of seconds since January 1, 1970 UTC.

A recipient of an OCA Bundle with attributes referenced in the Standard overlay
as using `dateint` or `Unix Time`Standards SHOULD convert the integer attribute
data into a date or date/time (respectively) and display the information as
appropriate for the user. For example, a mobile app should display the data as a
date or date/time based on the user's language/country setting, possibly
combined with an app setting for showing the data in [short, medium, long or
full
form](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat/DateTimeFormat).

#### Aries Specific "Branding" Overlay

In addition to the core OCA Overlays listed earlier, Aries issuers MAY include
an additional Aries-specific "extension" overlay, the **branding overlay**, that
gives the issuer a way to provide a set of data elements about the branding that
they would like to see applied to a given type of credential. The `branding
overlay` is a defined list of name/value pairs. Holders (and verifiers) can use
the values when displaying the credential in a "Card" format of that type from
that issuer.

An example branding overlay is as follows, along with a brief definition of the
items, and a sample image of how the data elements are to be used. The sample is
provide only to convey the concept of the branding overlay and how it is to be
used. Issuers, holders and verifiers should use [Aries RFC 0756: The Aries
Credential Branding Style Guide] for details on how the elements are to be
provided and used in displaying credentials.

[Aries RFC 0756: The Aries Credential Branding Style Guide]: https://docs.google.com/document/d/1WPpwzV3uH7KIPAATHGactconcn1J_IQ9/edit?usp=sharing&ouid=110035014596191352733&rtpof=true&sd=true

``` todo

To Do: Convert the Style Guide to a markdown file create as a new RFC (per guidance from the Aries Working Group).

```

``` json
{
  "capture_base": "EPMaG1h2hVxKCZ5_3KoNNwgAyd4Eq8zrxK3xgaaRsz2M",
  "type": "aries/overlays/branding/1.0",
  "logo": "data:image/png;base64,iVBORw...",
  "background_image": "data:image/png;base64,iVBORw0K...",
  "background_image_slice": "data:image/png;base64,iVBORw0K...",
  "primary_background_color": "#2E86C1",
  "secondary_background_color": "#2E86C1",
  "primary_attribute": "family_name",
  "secondary_attribute": "given_names",
  "issued_date_attribute": "",
  "expiry_date_attribute": "",
}
```

![Sample: Using the Branding Overlay, from the Aries Credential Branding Style
Guide](assets/Sample-use-of-Branding-Overlay.jpg)

[hashlink]: https://datatracker.ietf.org/doc/html/draft-sporny-hashlink
[Data URL Scheme]: https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URLs

- logo - a URI for a logo to display on the credential in some contexts.
The URI can be an HTTP URL, a [hashlink] or, to support inline images, a data
URL (e.g.: data:image/png;base64,...) as defined by the [Data URL Scheme]. The
logo MUST adhere to the logo properties defined in [Aries RFC 0756: The Aries
Credential Branding Style Guide].
- background_image - a URI for a background image to display with the
credential in some contexts. The URI could be an HTTP URL, a [hashlink] or, to
support inline images, a data URL (e.g.: data:image/png;base64,...) as defined
by the [Data URL Scheme]. The image MUST adhere to the background image
properties defined in [Aries RFC 0756: The Aries Credential Branding Style
Guide].
- background_image_slice - a URI for a background image slice to display
with the credential in some contexts. The URI could be a HTTP URL, a [hashlink]
or, to support inline images, a data URL (e.g.: data:image/png;base64,...) as
defined by the [Data URL Scheme]. The image MUST adhere to the background image slice
properties defined in [Aries RFC 0756: The Aries Credential Branding Style
Guide].
- primary_background_color - hex color code for the primary background color of the
  credential to be used in some contexts.
- secondary_background_color - hex color code for the secondary background color of the
  credential to be used in some contexts.
- primary_attribute - the name of a capture base attribute to be displayed on
  the credential in some contexts.
- secondary_attribute - the name of a capture base attribute to be displayed on
  the credential in some contexts.
- issued_date_attribute - the name of a capture base attribute that is the date
  of issuance of the credential. If there is no such attribute, leave blank.
- expiry_date_attribute - the name of a capture base attribute that is the
  expiry date of the credential. If there is no such attribute, leave blank.

It is deliberate that the credential branding defined in this RFC does **not**
attempt to achieve pixel-perfect on screen rendering of the equivalent paper
credential. There are two reasons for this.

First, studies have shown that issuers do not want people to think that the
digital credentials they have in their mobile wallet can be used as literal
replacements for paper during person-to-person (non-digital) verifications by
the holder showing their mobile device screen to the verifier. By showing
verifiers their screen, the holder may be oversharing their personal data. As
well, digital credentials are even easier to forge than paper credentials when
they are to be verified by a human, and we want to discourage using digital
credentials in that way.

Second, having each issuer provide pixel-perfect layout guidance to Aries agents
that supports a responsive user interface on a wide range of devices (laptops,
tablets and thousands of mobile phones) is extraordinarily complex. Further, a
wallet wanting to provide a consistent, helpful user experience will be severely
hampered by displaying credentials with many (perhaps hundreds) of completely
different credential layouts and styles.

Instead, the guidance in this RFC and the [Aries RFC 0756: The Aries Credential
Branding Style Guide] gives the issuer a few ways to brand their credentials,
and holder/verifier apps the latitude to use those issuer-provided elements in a
consistent for all issuers and credentials.

#### OCA Issuer Tools

An Aries OCA Bundle can be managed as pure JSON as found in this [sample OCA for
Aries OCA Bundle]. However, managing such multilingual content in JSON is not
easy, particularly if the language translations come from team members not
comfortable with working in JSON. An easier way to manage the data is to use an
[OCA For Aries OCA Source spreadsheet] and a converter to create the OCA Bundle
JSON from the spreadsheet. We recommend that an issuer maintain the spreadsheet
file in version control and use a pipeline action to generate the OCA Bundle
when the source file is updated.

The OCA Source Spreadsheet contains the following:

- An introductory tab with guidance on how to use the spreadsheet.
- A Capture Base tab with information about the attributes in the credential.
- A Branding tab with information about the issuer and the branding of the
  credential.
- A language or country-language code tab per country-language to be supported
  containing the source data for all all multilingual overlays.

As of the writing of this RFC, a single tool for generating a full OCA for Aries
OCA Bundle is not available. Over time, we expect that this part of the RFC will
be clarified as tooling improvements become available. The current recommended
approach to generating an OCA Bundle from OCA source is as follows:

- Maintain the OCA for Aries OCA Source spreadsheet, evolved from the sample
  [OCA for Aries OCA Source].
- Maintain the Branding overlay and the per language Meta overlays as a JSON
  file, evolved from this sample [Branding and Meta Overlays JSON file].
- Use the open source [Parser from the Human Colossus Foundation] to convert the
  spreadsheet to JSON.
- Remove from the generated JSON the two "layout" overlays. See this [GitHub
  issue](https://github.com/THCLab/oca-rust/issues/2) requesting that an option
  be added to the OCA Parser to not generate those overlays.
- Add in the manually maintained Branding and Meta Overlays file, updating the
  references to the capture bases as required.

Scripting the process should be relatively simple, and our expectation is that
the community will evolve the [Parser from the Human Colossus Foundation] to
make the process even easier.

[sample OCA for Aries OCA Bundle]: ./sample_oca_for_aries_oca_bundle.json
[OCA for Aries OCA Source spreadsheet]: ./OCA4Aries.xlsx
[Branding and Meta Overlays JSON file]: ./sample_branding_meta_overlays.json
[Parser from the Human Colossus Foundation]: https://github.com/THCLab/oca-rust

Over time, we expect to see other tooling become available--notably, an
interactive tool for issuers to use in populating their Branding overlay.

#### Issuing A Credential

The currently preferred mechanism for an issuer to provide an OCA Bundle to a
holder is when issuing a credential using
[RFC0453 Issue Credential](../0453-issue-credential-v2/README.md), version 2.2 or later, the issuer
provides, in the [credential offer
message](https://github.com/hyperledger/aries-rfcs/tree/main/features/0453-issue-credential-v2/README.md#offer-credential),
an OCA Bundle as a [credential
supplement](https://github.com/hyperledger/aries-rfcs/tree/main/features/0453-issue-credential-v2/README.md#supplements).

- The supplement type MUST be `oca-bundle`.
- The OCA Bundle MUST be in the JSON form of an OCA Bundle, not the ZIP format.
- The attachment MUST be
[signed](../../concepts/0017-attachments/README.md#signing-attachments) by the
issuer, and may be of [type
`base64url`](../../concepts/0017-attachments/README.md#base64url), meaning the
OCA Bundle is embedded in the message, or of [type
`link`](../../concepts/0017-attachments/README.md#links).

The reason OCA Bundle attachment must be signed by the issuer so that if the holder
passes the OCA Bundle on to the verifier, the verifier can be certain that the
issuer provided the OCA Bundle, and that it was not created by a malicious holder.

Issuers should be aware that to ensure that the signature on a linked OCA Bundle
(using the attachment [type `link`](../../concepts/0017-attachments/README.md#links))
remains verifiable, the content resolved by the link must not change over time.
For example, an Issuer might publish their OCA Bundles in a public GitHub
repository, and send a link to the OCA Bundle during issuance. In that case the
Issuer is advised to send a commit-based GitHub URL, rather than a branch-based
reference. The Issuer may update the OCA Bundle sent to different holders over
time, but once issued, each OCA Bundle MUST remain accessible.

#### Warning: External Attachments

The use of an attachment of type `link` for the OCA Bundle itself, or the use of
external references to the images in the [branding
overlay](#aries-specific-branding-overlay) could provide malicious issuers with
a mechanism for tracking the use of a holder's verifiable credential.
Specifically, the issuer could:

- Make any or all of the OCA bundle external references a unique identifier for
  the holder.
- When the holder retrieves the OCA bundle, the issuer does not learn anything
  useful as they already know they have issued a credential to that holder.
- If the holder passes the OCA bundle to verifiers and the verifiers resolve the
  external references, the malicious issuer would learn that the holder has used
  their verifiable credential in a presentation, and perhaps, with what verifier.

A holder MAY choose not to attach an OCA Bundle to a verifier if it contains any
external references. Non-malicious issuers are encouraged to **not** use
external references in their OCA Bundles and as such, to minimize the inlined
images in the branding overlay.

### Holder Activities

Before processing a credential and an associated OCA Bundle, the holder SHOULD
determine if the issuer is known in an ecosystem and has a sufficiently positive
reputation. For example, the holder might determine if the issuer is in a suitable [Trust Registry]
or request a presentation from the issuer about their identity.

[Trust Registry]: https://wiki.trustoverip.org/display/HOME/ToIP+Trust+Registry+Protocol+Specification

On receipt of a credential with an OCA Bundle supplement, the holder SHOULD
retrieve the OCA Bundle attachment, verify the signature is from the issuer's
public DID, verify the signature, and verify that the [OCA Capture Base] is for
the credential being offered or issued to the holder. If verified, the holder
should associate the OCA Bundle with the credential, including the signature.

The holder SHOULD take appropriate security precautions in handling the
remainder of the OCA data, especially the images as they could contain a
malicious payload. The security risk is comparable to a browser receiving a web
page containing images.

Holder software should be implemented to use the OCA Bundle when processing
and displaying the credential as noted in the list below. Developers of holder
software should be familiar with the overlays the issuer is likely to provide
(see list [here](#oca-specification-overlays)) and how to use them according to
[Aries RFC 0756: The Aries Credential Branding Style Guide].

- Check the country and language settings of the current user and use the
appropriate multilingual overlays to respect those settings in displaying
credential metadata and attributes (labels, etc.).
- Consider adding multilingual informational popups in your app using the per
  attribute data in the "information" overlay.
- Consider using the PII flag in the Capture Base to provide guidance to the
  user about the sharing of PII.
- Use the credential branding overlay and [Aries RFC 0756: The Aries Credential
  Branding Style Guide] in displaying the credential in various contexts (e.g.,
  in a credential offer prompt, in a list, selected from a list, alone on a
  page, etc.).
- Process the attribute data using the `type`, `encoding`, `format`, `unit` and
  `standard` overlays and display tha attributes appropriately for a given user.
  For example, display dates in a form suitable for the language and country
  settings of the user.
- Use the OCA-provide metadata about the credential, such as the
  name/description of the issuer, name/description of the credential type.

A recommended tactic when adding OCA support to a holder is when a credential is
issued without an associated OCA Bundle, generate one using the information
available about the type of the credential, default images, and randomly
generated colors. That allows for the creation of screens that assume an OCA
Bundle is available.

#### Adding OCA Bundles to Present Proof Messages

Once a holder has an OCA Bundle that was issued with the credential, it MAY pass
the OCA Bundle to a verifier when a presenting a proof that includes claims from
that credential. This can be done via the [present proof credential supplements]
approach, similar to what used when the credential was issued to the holder.
When constructing the `present_proof` message to hold a proof, the holder would
iterate through the credentials in the proof, and if there is an issuer-supplied
OCA Bundle for the credentials, add the OCA Bundle as a supplement to the
message. The signature from the Issuer MUST be included with the supplement.

A holder SHOULD NOT send an OCA Bundle to a verifier if the OCA Bundle is a
link, or if any of the data items in the OCA Bundle are links, as noted in the
in the [warning about external attachments in OCA
Bundles](#warning-external-attachments).

[present proof credential supplements]: https://github.com/hyperledger/aries-rfcs/tree/main/features/0454-present-proof-v2#22---addition-of-supplements

### Verifier Activities

On receipt of a presentation with OCA Bundle supplements, the verifier SHOULD
retrieve the OCA Bundle attachments, verify the signatures are from the
credential issuers' public DIDs, verify the signatures, and verify that the [OCA
Capture Base] is for the credentials being presented to the verifier. If
verified, the verifier should associate the OCA Bundle with the source
credential from the presentation.

On receipt of a presentation with OCA Bundle supplements, the verifier MAY
process the OCA Bundle attachment and verify the issuer's signature. If it
verifies, the verifier should associate the OCA Bundle with the source
credential from the presentation. The verifier SHOULD take appropriate security
precautions in handling the data, especially the images. The holder software
should be implemented to use the OCA Bundle when processing and displaying the
credential as noted in the list below.

Developers of verifier software should be familiar with the overlays the issuer
is likely to provide (see list [here](#oca-specification-overlays)) and how to
use them according to [Aries RFC 0756: The Aries Credential Branding Style
Guide]. The list of [how to use the OCA Bundle as a holder](#holder-activities)
applies equally to verifiers.

## Reference

- The [OCA Specification]
- [Aries RFC 0756: The Aries Credential Branding Style Guide]

## Drawbacks

- As noted in this [warning](#warning-external-attachments), the use of links
  either for OCA Bundles or for the images that are embedded in OCA Bundles are
  both extremely useful and problematic. It would be nice to be able to allow
  links for/in the OCA Bundles without the potential of being used to track the
  holder.
- If the OCA Bundle is passed to the holder as a link, the issuer must continue
  to make that content available for as long as the holder might retain the
  credential. Putting the OCA Bundle on a verifiable data registry (such as a
  ledger/blockchain) might be a good way to publish such data.
- The processing of an OCA Bundle, and particularly the processing of images in
  the branding overlay, provide an attack vector for malicious issuers.
  Developers of holder software SHOULD take precautions in handling and
  displaying the data.

## Rationale and alternatives

- The OCA architecture seems well suited to the Aries verifiable credential
use case, supporting the important capabilities of data formats, accessibility
support, multilingual support and the desire for issuers to brand their
credentials.
- The use of JSON-LD could provide some of the required capabilities covered by
OCA (such as multilingual labels), but that solution requires adding
considerable overhead and far more complicated processing to achieve a minimum
of the capabilities available through OCA.
- The current situation of having almost no metadata about credentials is
extremely limiting.
  - Extracting best available metadata from the Schema and Credential Definition
    objects, converting developer attribute/credential names of human friendly
    (e.g. "given_name" to Given Name, or "ssn" to "Ssn") and using that for the
    display of a credential.
  - The random generation of a background color for a given credential for use
  when displaying a credential.
- There are other flows that could be used to get an OCA Bundle to holders and
verifiers.
  - A publisher of a schema might also publish an OCA Bundle based on the
schema, for anyone to use.
  - An Aries agent vendor (such as the creator of an Aries mobile wallet) might
create a repository of OCA Bundles of common credential types for deployments of
their agent.
  - When using such alternatives, agents retrieving an OCA Bundle should have a
way to verify the source of the OCA Bundle, such as having a cryptographic
signature over the OCA Bundle from the designated publisher.

## Prior art

None, as far as we are aware.

## Unresolved questions

- Are there better ways for issuers to publish OCA Bundles for consumption by
  holders/verifiers?
- How do we balance the prevention of possible tracking by issuers, and the use
  of links to OCA Bundles or assets within OCA Bundles.

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull
request to add your implementation. If the implementation is open source,
include a link to the repo or to the implementation within the repo. Please be
consistent in the "Name" field so that a mechanical processing of the RFCs can
generate a list of all RFCs supported by an Aries implementation.

*Implementation Notes* [may need to include a link to test results](/README.md#accepted).

Name / Link | Implementation Notes
--- | ---
 |
