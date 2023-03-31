# RFC 0780: Use Data URLs for Images and More in Credential Attributes

- Authors: [Stephen Curran](swcurran@cloudcompass.ca), [Clecio Varjao](clecio.varjao@gov.bc.ca)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2023-03-31
- Status Note: New RFC being proposed.
- Supersedes: None
- Start Date: 2023-03-31
- Tags: [feature](/tags.md#feature)

## Summary

Some credentials include attributes that are not simple strings or numbers, such
as images or JSON data structures. When complex data is put in an attribute
the issuer **SHOULD** issue the attribute as a Data URL, as defined in [IETF RFC 2397], and whose use
is described in this [Mozilla Developer Documentation] article.

[IETF RFC 2397]: https://datatracker.ietf.org/doc/rfc2397/
[Mozilla Developer Documentation]: https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URLs

On receipt of all credentials and presentations, holders and verifiers
**SHOULD** check all string attributes to determine if they are Data URLs. If
so, they **SHOULD** securely process the data according to the metadata
information in the Data URL, including:

- the [MIME type] of the data (such as `image/png` or `application/json`)
- whether the data is [base64 encoded].

[base64 encoded]: https://datatracker.ietf.org/doc/rfc4648/
[MIME type]: https://www.ucolick.org/~sla/fits/mime/inetstds.html

This allows, for example, an Aries Mobile Wallet to detect that a data element
is an image and how it is encoded, and display it for the user as an image,
not as a long (long) string of gibberish.

## Motivation

Holders and verifiers want to enable a delightful user experience when an issuer
issues attributes that contain other than strings or numbers, such as an
image or a JSON data structure. In such cases, the holder and
verifiers need a way to know the format of the data so it can be processed
appropriately and displayed usefully. While the Aries community encourages the
use of the [Overlays Capture Architecture specification] as outlined
in [RFC 0755 OCA for Aries] for such information, there will be times where an
OCA Bundle is not available for a given credential. In the absence of an OCA Bundle, the holders and verifiers of
such attributes need data type information for processing and displaying the attributes.

[Overlays Capture Architecture specification]: https://oca.colossi.network/specification/
[RFC 0755 OCA for Aries]: https://github.com/swcurran/aries-rfcs/blob/oca4aries/features/0755-oca-for-aries/README.md

## Tutorial

An issuer wants to issue a verifiable credential that contains an image, such as
a photo of the holder to which the credential is issued. Issuing such an
attribute is typically done by converting the image to a base64 string. This is
handled by the various verifiable credential formats supported by Aries issuers.
The challenge is to convey to the holder and verifiers that the attribute is not
"just another string" that can be displayed on screen to the user. By making the
attribute a Data URL, the holder and verifiers can detect the type and encoding
of the attribute, process it, and display it correctly.

For example, this image (from the IETF 2793 specification):

![](photo.png)

can be issued as the attribute `photo` in a verifiable credential with its value a Data URL as follows:

```json
{
"photo": "data:image/png;base64,R0lGODdhMAAwAPAAAAAAAP///ywAAAAAMAAwAAAC8IyPqcvt3wCcDkiLc7C0qwyGHhSWpjQu5yqmCYsapyuvUUlvONmOZtfzgFzByTB10QgxOR0TqBQejhRNzOfkVJ+5YiUqrXF5Y5lKh/DeuNcP5yLWGsEbtLiOSpa/TPg7JpJHxyendzWTBfX0cxOnKPjgBzi4diinWGdkF8kjdfnycQZXZeYGejmJlZeGl9i2icVqaNVailT6F5iJ90m6mvuTS4OK05M0vDk0Q4XUtwvKOzrcd3iq9uisF81M1OIcR7lEewwcLp7tuNNkM3uNna3F2JQFo97Vriy/Xl4/f1cf5VWzXyym7PHhhx4dbgYKAAA7"
}
```

The syntax of a Data URL is described in [IETF RFC 2397]. The \<tl;dr> version is:

- `data:` -- hardcoded.
- `<MIME type>` -- optional, the [MIME type] of the data.
- `;base64` -- optional, if present, the data is [base64 encoded].
- `,` -- hardcoded separator.
- `<data>` -- the attribute data in the specified encoding.

A holder or verifier receiving a credential or presentation **MUST** check
each attribute is a string, and if so, if it is a Data URL (likely by using a
regular expression). If it is a Data URL it should be securely processed
accordingly.

Aries Data URL verifiable credential attributes **MUST** include the `<MIME type>`.

### Image Size

A separate issue from the use of Data URLs is how large an image (or other data
type) can be put into an attribute and issued as a verifiable credential. That
is an issue that is dependent on the verifiable credential implementation and
other factors. For AnonCreds credentials, the attribute will be treated as a
string, a hash will be calculated over the string, and the resulting number will
be signed--just as for any string. The size of the image does not matter.
However, there may be other components in your deployment that might impact how
big an attribute in a credential can be. Many in the community have successfully
experimented with the use of images in credentials, so consulting others on the
question might be helpful.

For the purpose of this RFC, the amount of data in the attribute is not
relevant.

### Security

As noted in this [Mozilla Developer Documentation] and this [Mozilla Security
Blog Post about Data URLs], Data URLs are blocked from being used in the Address
Bar of all major browsers. That is because Data URLs may contain HTML that can
contain anything, including HTML forms that collect data from users. Since Aries
holder and verifier agents are not general purpose content presentation engines
(as are browsers) the use of Data URLs are less of a security risk. Regardless,
holders and verifiers **MUST** limit their processing of attributes containing
Data URLs to displaying the data, and not executing the data. Further, Aries
holders and verifiers **MUST** stay up on dependency vulnerabilities, such as
images constructed to exploit vulnerabilities in libraries that display images.

[Mozilla Security Blog Post about Data URLs]: https://blog.mozilla.org/security/2017/11/27/blocking-top-level-navigations-data-urls-firefox-59/

## Reference

References for implementing this RFC are:

- [IETF RFC 2397]
- [Mozilla Developer Documentation]
- [Stack Overflow Article on a Data URL Regex](https://stackoverflow.com/questions/5714281/regex-to-parse-image-data-uri)
- [A GitHub Gist of JavaScript to detect a data URL](https://gist.github.com/bgrins/6194623)

## Drawbacks

The Aries community is moving to the use of the [Overlay Capture Architecture
Specification] to provide a more generalized way to accomplish the same thing
(understanding the meaning, format and encoding of attributes), so this RFC is
duplicating a part of that capability. That said, it is easier and faster for
issuers to start using, and for holders and verifiers to detect and use.

Issuers may choose to issue Data URLs with MIME types not commonly known to
Aries holder and verifier components. In such cases, the holder or verifier
**MUST NOT** display the data.

Even if the MIME type of the data is known to the holders and verifiers, it may
not be obvious how to present the data on screen in a useful way. For example,
an attribute holding a JSON data structure with an array of values may not
easily be displayed.

## Rationale and alternatives

We considered using the same approach as is used in [RFC 0441 Present Proof Best
Practices](../../concepts/0441-present-proof-best-practices/README.md#dates-and-predicates)
of a special suffix (`_img`) for the attribute name in a credential to indicate that
the attribute held an image. However, that provides far less information than this
approach (e.g., what type of image?), and its use is limited to images. This RFC
defines a far more complete, standard, and useful approach.

As noted in the drawbacks section, this same functionality can (and should) be
achieved with the broad deployment of [Overlay Capture Architecture
Specification] and [RFC 0755 OCA for Aries]. However, the full deployment of
[RFC 0755 OCA for Aries] will take some time, and in the meantime, this is a
"quick and easy" alternate solution that is useful alongside OCA for Aries.

## Prior art

In the use cases of which we are aware of issuers putting images and JSON
structures into attributes, there was no indicator of the attribute content, and
the holders and verifiers were assumed to either "know" about the data content
based on the type of credential, or they just displayed the data as a string.

## Unresolved questions

Should this RFC define a list (or the location of a list) of MIME types that
Aries issuers can use in credential attributes?

For supported MIME types that do not have obvious display methods (such as
JSON), should there be a convention for how to display the data?

## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

*Implementation Notes* [may need to include a link to test results](/README.md#accepted).

Name / Link | Implementation Notes
--- | ---
 | 

