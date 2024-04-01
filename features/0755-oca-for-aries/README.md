# 0755: Overlays Capture Architecture (OCA) For Aries

- Authors: [Stephen Curran](swcurran@gmail.com)
- Status: [DEMONSTRATED](/README.md#demonstrated)
- Since: 2024-03-02
- Status Note: Implemented in the [Bifold Wallet](https://github.com/openwallet-foundation/bifold-wallet)
- Start Date: 2022-09-25
- Version: 1.0
- Tags: [feature](/tags.md#feature)

## Summary

[Overlays Capture Architecture](https://oca.colossi.network/) (OCA) is, per the
[OCA specification], a "standardized global solution for data capture and
exchange." Given a data structure (such as a verifiable credential), OCA allows
for the creation of purpose-specific overlays of information about that data
structure. Each overlay provides some knowledge (human and machine-readable)
about the overall data structure or the individual attributes within it. The
information in the overlays makes it possible to create useful software for
capturing data, displaying it and exchanging it. While the [OCA
website](https://oca.colossi.network/) and [OCA specification] can be reviewed
for a detailed background of OCA and its various purposes, in this RFC we'll
focus on its purpose in Aries, which is quite constrained and pragmatic--a
mechanism for an issuer to provide information about a verifiable credential to
allow holder and verifier software to display the credential in a human-friendly
way, including using the viewers preferred language, and the issuer's preferred
branding. The image below shows an Aries mobile Wallet displaying the same
credential without and with OCA overlays applied in two languages. All of the
differences in the latter two screenshots from the first come from
issuer-supplied OCA data.

[OCA Specification]: https://oca.colossi.network/specification/
[RFC0756 OCA for Aries Style Guide]: ../0756-oca-for-aries-style-guide/README.md

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
  holder and verifier software are expected to use in displaying the credential.

The standard flow of data between participants is as follows:

- An issuer creates an OCA Bundle for each type of verifiable credential it
issues.
- During credential issuance using [RFC 0453 Issue Credential V2 v2.2 (or later)
protocol] the issuer MAY include in the protocol's `credential-offer` or
`credential` messages the OCA Bundle for the credential type as an `oca-bundle`
[issue credential supplement].
- When provided, the holder software has full access to the OCA information
published by that issuer and can use the OCA data to render the credential for
its user(s) in the language of their choice, with credential branding from
the issuer, based on the [RFC0756 OCA for Aries Style Guide].
- The holder MAY share the OCA Bundle with a verifier by using [RFC 0453 Issue
Credential V2 v2.2 (or later) protocol] to add the `oca-bundle` credential
supplement received from the issuer.
- On receipt, the verifier software has full access to the OCA information
published by that issuer and can use the OCA data to render the credential for
its user(s) in the language of their choice, with credential branding from
the issuer, based on the [RFC0756 OCA for Aries Style Guide].

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
generating the OCA Bundle from the Excel source. See the section of this RFC
called [OCA Tooling](#oca-issuer-tools) for a link to an OCA Source spreadsheet,
and information on tools available for managing the OCA Source data and
generating a corresponding OCA Bundle.

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

An OCA Bundle that contains overlay types that a holder or verifier does not
expect MUST be processed, with the unexpected overlays ignored.

- The **[Character Encoding Overlay]** contains the encoding for each attribute
in the capture base.
- The **[Format Overlay]** provides
the input structure for each data attribute. The format may be useful to the
holder (or verifier) in displaying the data in a style expected by the user,
such as knowing that a given field of `type` binary is an image in `image/jpeg`
format.
- The multilingual **[Label Overlay]** provides a label to be used for each
attribute for a given language. The label overlay also includes labels for
attributes with enumerated values (called categories in the OCA specification).
For example, a data attribute containing the codes "EN", "FR", "SP" could have a
category entries that indicate the codes correspond to "English", "French" and
"Spanish", respectively.
- The multilingual **[Information Overlay]** provides a description or help text
about each attribute for a given language. There will be one overlay per
issuer-supported language.
- The multilingual **[Meta Overlay]** contains information about the credential
itself. For Aries, the meta overlay SHOULD include the following additional
name/value pairs, specific to the OCA for Aries use case:
  - `name` - the name of the credential.
  - `description` - a description of the credential.
  - `issuer` - the name of the issuer of the credential.
  - `issuer_description` - a description for the issuer of the credential.
  - `issuer_url` - a URL for the issuer of the credential.
  - `credential_help_text` - help text about the credential
  - `credential_support_url` - a URL for a service providing support in the use of the credential.
- The **[Unit Overlay]**
  allows the issuer to declare the units of measurement for the attributes in
  the overlay.
- The **[Standard Overlay]** indicates that some or all of the attributes use
  specific data standards populating the attribute in a credential. This might
  be used, for example, for defining the standard applied in populating a data
  attribute with a date or date/time.
- The **[Entry Code Overlay]** contains a list of enumerated values for each
  data attribute that uses enumerated values. An example might be a list of
  regional jurisdiction (such as provinces or states) short forms that will be
  placed in an attribute (e.g., NY, ND, AL, CA, etc.). The attributes in the
  credential are expected to be populated with one of the enumerated values.
- The **[Entry Overlay]** contains a language-specific list of the meanings for
  each enumerated value for each data attribute that uses enumerated values. For
  our example of short forms of jurisdictions, the "meanings" would be the
  expanded list per language supported (English, French, Spanish, etc.) of
  jurisdictions (e.g., New York, North Dakota, Alabama, California, etc.).

[Capture Base]: https://oca.colossi.network/v1.1.0-rc.html#capture-base
[Character Encoding Overlay]: https://oca.colossi.network/v1.1.0-rc.html#character-encoding-overlay
[Format Overlay]: https://oca.colossi.network/v1.1.0-rc.html#format-overlay
[Label Overlay]: https://oca.colossi.network/v1.1.0-rc.html#label-overlay
[Information Overlay]: https://oca.colossi.network/v1.1.0-rc.html#information-overlay
[Meta Overlay]: https://oca.colossi.network/v1.1.0-rc.html#meta-overlay
[Unit Overlay]: https://oca.colossi.network/specification/#unit-overlay
[Standard Overlay]: https://oca.colossi.network/specification/#standard-overlay
[Entry Code Overlay]: https://oca.colossi.network/specification/#entry-code-overlay
[Entry Overlay]: https://oca.colossi.network/specification/#entry-overlay

#### Aries-Specific Dates in the OCA Format Overlay

In AnonCreds, zero-knowledge proof (ZKP) predicates (used, for example, to prove
older than a given age based on date of birth without sharing the actual date of
birth) must be based on **integers**. In the AnonCreds/Aries community, common
ways for representing dates and date/times as integers so that they can be used
in ZKP predicates are the `dateint` and `Unix Time` formats, respectively.

- "`dateint`" is a credential attribute that uses the Aries `dateint`
specification as described in [Aries RFC
0592](../0592-indy-attachments/README.md). Briefly, `dateint` is a date
(YYYYMMDD) provided in a credential attribute as an integer (for example
`September 29, 2022` is the integer `20220929` or `20,220,929`). `dateint` is
also part of [ISO standard 1989 for COBOL Programming
Interfaces](https://www.iso.org/standard/74527.html), described [here in an IBM
document](https://www.ibm.com/docs/en/cobol-zos/6.3?topic=sf-format-arguments-return-values-date-time-intrinsic-functions#INFFORM__stand_date).

- "`Unix Time`" is a credential attribute that is a date/time timestamp
constructed according to the `Unix Time` [Unix/POSIX data
standard](https://en.wikipedia.org/wiki/Unix_time). Briefly, `Unix Time` is a
date/time represented as the number of seconds since January 1, 1970 UTC.

In an OCA for Aries OCA Bundle, a `dateint` and `Unix Time` attributes MUST
have the following values in the indicated overlays:

- `dateint`
  - datatype `DateTime` in the [Capture Base]
  - standard `urn:iso:std:iso:1989` in the [Standard Overlay]
  - character encoding `utf-8` in the [Character Encoding Overlay]
  - format `YYYYMMDD` in the [Format Overlay]
  - Example: `20230114` for "January 14, 2023"
- `Unix Time`
  - datatype `DateTime` in the [Capture Base]
  - standard `urn:unix:unix-time` in the [Standard Overlay]
  - character encoding `utf-8` in the [Character Encoding Overlay]
  - format `epoch` in the [Format Overlay]
  - Example: `1673715495` for "Sat Jan 14 2023 16:58:15 GMT+0000"

A recipient of an OCA Bundle with the combination of overlay values referenced
above for `dateint` and `Unix Time` SHOULD convert the integer attribute data
into a date or date/time (respectively) and display the information as
appropriate for the user. For example, a mobile app should display the data as a
date or date/time based on the user's language/country setting and timezone,
possibly combined with an app setting for showing the data in [short, medium,
long or full
form](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat/DateTimeFormat).

#### Aries Specific "branding" Overlay

In addition to the core OCA Overlays listed earlier, Aries issuers MAY include
an additional Aries-specific extension overlay, the **"branding" overlay**, that
gives the issuer a way to provide a set of data elements about the branding that
they would like to see applied to a given type of credential. The `branding
overlay` is similar to the multilanguage Meta overlay (e.g. ones for English,
French and Spanish), with a specified set of name/value pairs. Holders (and
verifiers) use the branding values from the issuer when rendering a credential
of that type according the [RFC0756 OCA for Aries Style Guide].

An example of the use of the branding overlay is as follows, along with a
definition of the name/value pair elements, and a sample image of how the
elements are to be used. The sample is provide only to convey the concept of the
branding overlay and how it is to be used. Issuers, holders and verifiers should
refer to [RFC0756 OCA for Aries Style Guide] for details on how the elements are to
be provided and used in displaying credentials.

```
{
    "type": "aries/overlays/branding/1.0"
    "digest": "EBQbQEV6qSEGDzGLj1CqT4e6yzESjPimF-Swmyltw5jU",
    "capture_base": "EKpcSmz06sJs0b4g24e0Jc7OerbJrGN2iMVEnwLYKBS8",
    "logo": "https://raw.githubusercontent.com/hyperledger/aries-rfcs/oca4aries/features/0755-oca-for-aries/best-bc-logo.png",
    "background_image": "https://raw.githubusercontent.com/hyperledger/aries-rfcs/oca4aries/features/best-bc-background-image.png",
    "background_image_slice": "https://raw.githubusercontent.com/hyperledger/aries-rfcs/oca4aries/features/best-bc-background-image-slice.png",
    "primary_background_color": "#003366",
    "secondary_background_color": "#003366",
    "secondary_attribute": "given_names",
    "primary_attribute": "family_name",
    "secondary_attribute": "given_names",
    "issued_date_attribute": "",
    "expiry_date_attribute": "expiry_date_dateint",
}
```

![Sample: Using the Branding Overlay, from the Aries Credential Branding Style
Guide](assets/Sample-use-of-Branding-Overlay.png)

[hashlink]: https://datatracker.ietf.org/doc/html/draft-sporny-hashlink
[Data URL Scheme]: https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URLs

- OCA Overlay-related items:
  - `type` - a the type of the overlay, using the `aries` namespace.
  - `digest` - the self-addressing identifier (SAID) for the overlay. Note that in this example, the SAID is not accurate for the data in the example.
  - `capture_base` - the self-addressing identifier (SAID) for the capture base to which this overlay applies.
- `logo` - a URI for a logo to display on the credential in some contexts.
The URI can be an HTTP URL, a [hashlink] or, to support inline images, a data
URL (e.g.: `data:image/png;base64,...`) as defined by the [Data URL Scheme]. The
logo MUST adhere to the logo properties defined in [RFC0756 OCA for Aries Style Guide].
- `background_image` - a URI for a background image to display with the
credential in some contexts. The URI could be an HTTP URL, a [hashlink] or, to
support inline images, a data URL (e.g.: `data:image/png;base64,...`) as defined
by the [Data URL Scheme]. The image MUST adhere to the background image
properties defined in [RFC0756 OCA for Aries Style Guide].
- `background_image_slice` - a URI for a background image slice to display
with the credential in some contexts. The URI could be a HTTP URL, a [hashlink]
or, to support inline images, a data URL (e.g.: `data:image/png;base64,...`) as
defined by the [Data URL Scheme]. The image MUST adhere to the background image slice
properties defined in [RFC0756 OCA for Aries Style Guide].
- `primary_background_color` - hex color code for the primary background color of the
  credential to be used in some contexts.
- `secondary_background_color` - hex color code for the secondary background color of the
  credential to be used in some contexts.
- `primary_attribute` - the name of a capture base attribute to be displayed on
  the credential in some contexts.
- `secondary_attribute` - the name of a capture base attribute to be displayed on
  the credential in some contexts.
- `issued_date_attribute` - the name of a capture base attribute that is the date
  of issuance of the credential. If there is no such attribute, leave blank.
- `expiry_date_attribute` - the name of a capture base attribute that is the
  expiry date of the credential. If there is no such attribute, leave blank.

It is deliberate that the credential branding defined in this RFC does **not**
attempt to achieve pixel-perfect on screen rendering of the equivalent paper
credential. There are two reasons for this:

- First, studies have shown that issuers do not want people to think that the
digital credentials they have in their mobile wallet can be used as literal
replacements for paper during person-to-person (non-digital) verifications by
the holder showing their mobile device screen to the verifier. By showing
verifiers their screen, the holder may be oversharing their personal data. As
well, digital credentials are even easier to forge than paper credentials when
they are to be verified by a human, and we want to discourage using digital
credentials in that way.
- Second, having each issuer provide pixel-perfect layout guidance to Aries agents
that supports a responsive user interface on a wide range of devices (laptops,
tablets and thousands of mobile phones) is extraordinarily complex. Further, a
wallet wanting to provide a consistent, helpful user experience will be severely
hampered by displaying credentials with many (perhaps hundreds) of completely
different credential layouts and styles.

Instead, the guidance in this RFC and the [RFC0756 OCA for Aries Style Guide]
gives the issuer a few ways to brand their credentials, and holder/verifier apps
information on how to use those issuer-provided elements in a manner consistent
for all issuers and all credentials.

#### OCA Issuer Tools

An Aries OCA Bundle can be managed as pure JSON as found in this [sample OCA for
Aries OCA Bundle]. However, managing such multilingual content in JSON is not
easy, particularly if the language translations come from team members not
comfortable with working in JSON. An easier way to manage the data is to use an
OCA source spreadsheet for most of the data, some in a source JSON file, and to
use a converter to create the OCA Bundle JSON from the two sources. We recommend
that an issuer maintain the spreadsheet file and source JSON in version control
and use a pipeline action to generate the OCA Bundle when the source files are
updated.

The OCA Source Spreadsheet, an [example of which is attached to this
RFC](OCA4Aries.xlsx), contains the following:

- An introductory tab about the OCA content in the spreadsheet.
- A tab with instructions on using the spreadsheet.
- A "Main" tab with the "Capture Base" data, along with data for other, non-multilingual overlays.
- A language or country-language code tab per country-language to be supported by the issuer
  containing the source data for all multilingual overlays.

The JSON Source file contains the [Aries-specific Branding
Overlay](#aries-specific-branding-overlay). Attached to this RFC is an [example
Branding Overlay JSON file](branding.json) that issuers can use to start.

The following is how to create an OCA Source spreadsheet and from that, generate
an OCA Bundle. Over time, we expect that this part of the RFC will be clarified
as the tooling evolves.

- Creating/Maintaining the Excel File
  - Make a copy of the latest [OCA Template] from the [Human Colossus Foundation].
  - Fill in the "Main" tab with the attributes from the schema, completing the
    relevant columns for each attribute. Current columns to complete:
    - CB-CL: Classification
    - CB-AN: Attribute Name
    - CB-AT: Attribute Type
    - CB-FA: Flagged Attribute
    - OL-CH: Character Encoding
    - OL-FT: Format
    - OL-ST: Standard
    - OL-EC: Entry Codes
    - OL-UT: Unit
  - As needed, populate the columns for "dateint" and "Unix Time" attributes as indicated in the [Aries Specific Dates in the OCA Formats Overlay](#aries-specific-dates-in-the-oca-format-overlay) section of this document.
  - Rename the sample language tab (`en`) to one of the language or language-country that as an issuer, you want to support.
  - Fill in the data in columns other than C (which is automatically populated from the `Main` tab) for the first language as appropriate.
  - Populate column A and B as follows:
    - In column A (`OL-MN: Meta [Attribute Name]`), add the values:
      - "name"
      - "description"
      - "issuer"
      - "issuer_description"
      - "issuer_url"
      - "credential_help_text"
      - "credential_support_url"
      - "watermark"
        - The "watermark" is used to mark non-production credentials, as described in the ["non-production watermark" section of RFC0756 OCA for Aries Style Guide](../0756-oca-for-aries-style-guide#non-production-watermark)
    - Complete column B (`OL-MV: Meta [Attribute Value]`) as appropriate for each column A name (listed above).
  - Duplicate and rename the initial language tab for each language or language-country that as an issuer, you want to support.
  - Update each additional language tab.
- Creating/Maintaining the Branding JSON file
  - Make a copy of the attached example [branding JSON file](branding.json), and update the values for the credential you are issuing.
- Generating the OCA Bundle from the OCA for Aries Source files:
  - Use the open source [OCA Parser from the Human Colossus Foundation] to convert the
    spreadsheet to JSON. The current command to use is `parser parse oca --path <OCA Excel File> > <output Excel JSON OCA Bundle>`
  - Use the open source [jq utility](https://stedolan.github.io/jq/) to add the `branding.json` file to the JSON Excel output to produce the OCA Bundle with the following command, replacing the file names in the command with the ones for your use:
    - `jq ".[].overlays += $(cat BRANDING-JSON-FILE)" OCA-EXCEL-FILE > OCA-BUNDLE-JSON-FILE`
    - From a command line in this folder, the following command can be run to generate the OCA Bundle JSON to standard output:
      - `jq ".[].overlays += $(cat branding.json)" OCA4AriesExcel.json`

> NOTE: The `capture_base` and `digest` fields in the branding overlay of the resulting OCA Bundle JSON file will **not** be updated to be proper self-addressing identifiers (SAIDs) as required by the [OCA Specification]. We are looking into how to automate the updating of those data elements.

[OCA Template]: https://github.com/THCLab/oca-ecosystem/raw/main/examples/template.xlsx

Scripting the generation process should be relatively simple, and our expectation is that
the community will evolve the [Parser from the Human Colossus Foundation] to
simplify the process further.

[sample OCA for Aries OCA Bundle]: ./sample_oca_for_aries_oca_bundle.json
[OCA Parser from the Human Colossus Foundation]: https://github.com/THCLab/oca-rust

Over time, we expect to see other tooling become available--notably, a tool for
issuers to see what credentials will look like when their OCA Bundle is applied.

#### Issuing A Credential

> This section of the specification remains under consideration. The use of the
> `credential supplement` as currently described here is somewhat problematic
> for a number of reasons.
> 
> - The issuer has no way to update the OCA Bundle for a given holder after
>   issueance. We see this as a likely use case to enable, for example, an
>   issuer supporting additional languages over time.
> - The "External Attachments" risk, as described in [this section of this
>   RFC](#warning-external-attachments).
> - The complicated way for a verifier to get an OCA Bundle when needed after a
>   presentation.
>
> We are currently investigating if an OCA Bundle can be published to the same
> VDR as holds an AnonCreds Schema or Credential Definition. We think that would
> overcome each of those concerns and make it easier to both publish and
> retrieve OCA Bundles.

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
external references to the images in the
[branding Overlay](#aries-specific-branding-overlay) could provide malicious issuers with
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
[RFC0756 OCA for Aries Style Guide].

- Check the country and language settings of the current user and use the
appropriate multilingual overlays to respect those settings in displaying
credential metadata and attributes (labels, etc.).
- Consider adding multilingual informational popups in your app using the per
  attribute data in the "information" overlay.
- Consider using the PII flag in the Capture Base to provide guidance to the
  user about the sharing of PII.
- Use the branding overlay and [RFC0756 OCA for Aries Style Guide] in
  displaying the credential in various contexts (e.g., in a credential offer
  prompt, in a list, selected from a list, alone on a page, etc.).
- Process the attribute data using the `type`, `character encoding`, `format`,
  `unit` and `standard` overlays and display tha attributes appropriately for a
  given user. For example, display dates in a form suitable for the language and
  country settings of the user.
- Where enumerated names are used for credential attributes, retrieve and use
  the name-value pairs in the [Entry Code Overlay] and [Entry Overlay] to display the data.
- Use the OCA-provide metadata about the credential, such as the
  name/description of the issuer, name/description of the credential type.

A recommended tactic when adding OCA support to a holder is when a credential is
issued without an associated OCA Bundle, generate an OCA Bundle for the
credential using the information available about the type of the credential,
default images, and randomly generated colors. That allows for the creation of
screens that assume an OCA Bundle is available. The [RFC0756 OCA for Aries Style
Guide] contains guidelines for doing that.

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
use them according to [RFC0756 OCA for Aries Style Guide]. The list of [how to
use the OCA Bundle as a holder](#holder-activities) applies equally to
verifiers.

## Reference

- The [OCA Specification]
- [RFC0756 OCA for Aries Style Guide]

## Drawbacks

- The use of credential supplements might not be the best way to publish OCA
  Bundles. The Aries community is currently investigating if OCA Bundles can be
  published to the Verifiable Data Registry upon which the schema and credential
  definition are published.
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
