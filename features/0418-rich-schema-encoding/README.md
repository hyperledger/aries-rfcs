# Aries RFC 0418: Aries Rich Schema Encoding Objects
- Author: [Ken Ebert](mailto:ken@sovrin.org), [Mike Lodder](mailto:mike@sovrin.org), [Brent Zundel](mailto:brent.zundel@evernym.com), [Alexander Shcherbakov](mailto:alexander.shcherbakov@evernym.com)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2020-02-10
- Status Note: Part of proposed Rich Schema capabilities for credentials 
- Supersedes:
- Start Date: 2019-03-19
- Tags: [feature](/tags.md#feature), [rich-schemas](/tags.md#rich-schemas)

## Summary

The introduction of rich schemas and their associated greater range of
possible attribute value data types require correspondingly rich
transformation algorithms. The purpose of the new encoding object is
to specify the algorithm used to perform transformations of each attribute
value data type into a canonical data encoding in a deterministic way. 

The initial use for these will be the transformation of attribute value
data into 256-bit integers so that they can be incorporated into the
anonymous credential signature schemes we use. The transformation
algorithms will also allow for extending the cryptographic schemes and
various sizes of canonical data encodings (256-bit, 384-bit, etc.). The
transformation algorithms will allow for broader use of predicate proofs,
and avoid hashed values as much as possible, as they do not support
predicate proofs.

Encoding objects are processed in a generic way defined in 
[Rich Schema Objects Common](https://github.com/hyperledger/aries-rfcs/tree/main/concepts/0420-rich-schemas-common).

## Motivation

All attribute values to be signed in anonymous credentials must be
transformed into 256-bit integers in order to support the 
[Camenisch-Lysyanskaya signature][CL-signatures] scheme.

The current methods for creating a credential only accept attributes which
are encoded as 256-bit integers. The current possible source attribute
types are integers and strings. No configuration method exists at this time
to specify which transformation method will be applied to a particular
attribute. All encoded attribute values rely on an implicit understanding
of how they were encoded.

The current set of canonical encodings consists of integers and hashed
strings. The introduction of encoding objects allows for a means of
extending the current set of canonical encodings to include integer
representations of dates, lengths, boolean values, and floating point
numbers. All encoding objects describe how an input is transformed
into an encoding of an attribute value according to the transformation
algorithm selected by the issuer.

## Tutorial


### Intro to Encoding Objects
Encoding objects are JSON objects that describe the input types,
transformation algorithms, and output encodings. The encoding object
is stored on the ledger.

### Properties
Encoding's properties follow the generic template defined in 
[Rich Schema Common](https://github.com/hyperledger/aries-rfcs/tree/main/concepts/0420-rich-schemas-common#how-rich-schema-objects-are-stored-in-the-data-registry).

Encoding's `content` field is a JSON-serialized string with the following fields:

- `input`: a description of the input value.
- `output`: a description of the output value.
- `algorithm`:
  - `documentation`: a URL which references a specific github commit of
  the documentation that fully describes the transformation algorithm.
  - `implementation`: a URL that links to a reference implementation of the
  transformation algorithm. It is not necessary to use the implementation
  linked to here, as long as the implementation used implements the same
  transformation algorithm.
  - `description`: a brief description of the transformation algorithm.
- `testVectors`: a URL which references a specific github commit of a
selection of test vectors that may be used to provide assurance that a
transformation algorithm implementation is correct. 


### Example Encoding
An example of the `content` field of an Encoding object:
```
{
    "input": {
        "id": "DateRFC3339",
        "type": "string"
    },
    "output": {
        "id": "UnixTime",
        "type": "256-bit integer"
    },
    "algorithm": {
        "description": "This encoding transforms an
            RFC3339-formatted datetime object into the number
            of seconds since January 1, 1970 (the Unix epoch).",
        "documentation": URL to specific github commit,
        "implementation": URL to implementation
    },
    "testVectors": URL to specific github commit
}
```

### Transformation Algorithms

The purpose of a transformation algorithm is to deterministically convert
a value into a different encoding. For example, an attribute value may be
a string representation of a date, but the CL-signature signing mechanism
requires all inputs to be 256-bit integers. The transformation algorithm
takes this string value as input, parses it, and encodes it as a 256-bit
integer.  

It is anticipated that the encodings used for CL signatures and their
associated transformation algorithms will be used primarily by two
entities. First, the issuer will use the transformation algorithm to
prepare credential values for signing. Second, the verifier will use the
transformation algorithm to verify that revealed values were correctly
encoded and signed, and to properly transform values against which
predicates may be evaluated.

#### Integer Representation

In order to properly encode values as integers for use in predicate proofs,
a common 256-bit integer representation is needed. Predicate proofs are
kept simple by requiring all inputs to be represented as positive integers.
To accomplish this, we introduce a zero-offset and map all integer results
onto a range from 9 to 2<sup>256</sup> - 10. The zero point in this range
is 2<sup>255</sup>. 

Any transformation algorithm which outputs an integer value should use this
representation.

#### Floating Point Representation
In order to retain the provided precision of floating point values, we use
[Q number format](https://en.wikipedia.org/wiki/Q_(number_format)), a
binary, fixed-point number format. We use 64 fractional bits.


#### Reserved Values

For integer and floating point representations, there are some reserved
numeric strings which have a special meaning.

| Special Value | Representation         | Description |
| ------------- | ---------------------- | ----------- |
| -∞            | 8                      | The largest negative number.<br>Always less than any other valid integer. |
| ∞             | 2<sup>256</sup> - 9    | The largest positive number.<br>Always greater than any other valid integer. |
| NULL          | 7                      | Indicates that the value of a field is not supplied.<br>Not a valid value for comparisons. |
| NaN           | 2<sup>256</sup> - 8    | Floating point NaN.<br>Not a valid value for comparisons. |
| reserved      | 1 to 6                 | Reserved for future use. |
| reserved      | 2<sup>256</sup> - 7 to 2<sup>256</sup> - 1 | Reserved for future use. |


#### Documentation
The value of the documentation field is intended to be a URL which, when
dereferenced, will provide specific information about the transformation
algorithm such that it may be implemented. We recommend that the URL
reference some immutable content, such as a specific github commit, an IPFS
file, etc.


#### Implementation
The value of the implementation field is intended to be a URL which, when
dereferenced, will provide a reference implementation of the transformation
algorithm.

#### Test Vectors
Test vectors are very important. Although not comprehensive, a set of
public test vectors allows for multiple implementations to verify adherence
to the transformation algorithm for the set. Test vectors should consist of
a set of comma-separated input/output pairs. The input values should be
read from the file as strings. The output values should be byte strings
encoded as hex values.

The value of the test_vectors field is intended to be a URL which, when
dereferenced, will provide the file of test vectors. We recommend that the
URL reference some immutable content, such as a specific github commit, an
IPFS file, etc.

### Data Registry Storage
Aries will provide a means for writing contexts to and reading contexts
from a verifiable data registry (such as a distributed ledger).

An Encoding object will be written to the ledger in a generic way defined in 
[Rich Schema Objects Common](https://github.com/hyperledger/aries-rfcs/tree/main/concepts/0420-rich-schemas-common#how-rich-schema-objects-are-stored-in-the-data-registry).


### Aries Data Registry Interface
Aries Data Registry Interface methods for adding and retrieving an Encoding object from the
ledger comply with the generic approach described in [Rich Schema Objects Common](https://github.com/hyperledger/aries-rfcs/tree/main/concepts/0420-rich-schemas-common#aries-data-registry-interface).

This means the following methods can be used:
- `write_rich_schema_object`
- `read_rich_schema_object_by_id`
- `read_rich_schema_object_by_metadata`

## Reference
[reference]: #reference

The following is a 
[reference implementation of various transformation algorithms](https://github.com/sovrin-foundation/aries-credx-framework-rs/blob/master/src/encoding/mod.rs).

[Here](https://www.researchgate.net/publication/220922101_A_Signature_Scheme_with_Efficient_Protocols) is the paper that defines Camenisch-Lysyanskaya signatures.

- [0250: Rich Schema Objects](https://github.com/hyperledger/aries-rfcs/tree/main/concepts/0250-rich-schemas)
- [0420: Rich Schema Objects Common](https://github.com/hyperledger/aries-rfcs/tree/main/concepts/0420-rich-schemas-common) 


## Drawbacks
[drawbacks]: #drawbacks

This increases the complexity of issuing verifiable credentials and
verifiying the accompanying verifiable presentations. 

## Rationale and alternatives

Encoding attribute values as integers is already part of using anonymous
credentials, however the current method is implicit, and relies on use of a
common implementation library for uniformity. If we do not include
encodings as part of the Rich Schema effort, we will be left with an
incomplete set of possible predicates, a lack of explicit mechanisms for
issuers to specify which encoding methods they used, and a corresponding
lack of verifiablity of signed attribute values.

In another design that was considered, the encoding on the ledger was
actually a function an end user could call, with the ledger nodes
performing the transformation algorithm and returning the encoded value.
The benefit of such a design would have been the guarantee of uniformity
across encoded values. This design was rejected because of the
unfeasibility of using the ledger nodes for such calculations and the
privacy implications of submitting attribute values to a public ledger.

## Prior art

A description of a prior effort to add encodings to Indy may be found in
this [jira ticket](https://jira.hyperledger.org/browse/IS-786) and 
[pull request](https://github.com/hyperledger/indy-sdk/pull/1048).

What the prior effort lacked was a corresponding enhancement of schema
infrastructure which would have provided the necessary typing of attribute
values.

## Unresolved questions
- Is the proposed interface generic enough to support other data
registries?
- We are not defining Rich Schema objects as DID DOCs for now. We may re-consider this in future once DID DOC format
is finalized.
- It may make sense to extend DID specification to include using DID for referencing Rich Schema objects.
- The proposed canonicalization form of a content to be used for DID's id-string generation is in a Draft version, so we 
may find a better way to do it.
  
## Implementations

The following lists the implementations (if any) of this RFC. Please do a
pull request to add your implementation. If the implementation is open
source, include a link to the repo or to the implementation within the
repo. Please be consistent in the "Name" field so that a mechanical
processing of the RFCs can generate a list of all RFCs supported by an
Aries implementation.

Name / Link | Implementation Notes
--- | ---
 |  | 

