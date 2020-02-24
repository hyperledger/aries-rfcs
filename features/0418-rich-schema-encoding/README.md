# Aries RFC 0418: Aries Rich Schema Encoding Objects
- Author: [Ken Ebert](ken@sovrin.org), [Mike Lodder](mike@sovrin.org), [Brent Zundel](brent.zundel@evernym.com)
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


### Intro to encoding objects
Encoding objects are JSON objects that describe the input types,
transformation algorithms, and output encodings. The encoding object
is stored on the ledger.

### Properties
An encoding object is identified by a DID, and is formatted as a DID
Document. It contains the following properties:

#### id
The DID which identifies the encoding object. The id-string of the
DID is the base58 representation of the SHA2-256 hash of the canonical form
of the value of the data object of the content property. The
canonicalization scheme we recommend is the IETF draft
[JSON Canonicalization Scheme (JCS).](https://tools.ietf.org/id/draft-rundgren-json-canonicalization-scheme-16.html)

#### name
The name of the encoding object as a utf-8 string value. By convention,
the name should be taken from the input and output encodings:
<input>_<output>

#### version
The version of this named encoding object.

#### hash_value
The hash of the encoding object contained in the content block data 
property.

#### encoding
The encoding object consists of:
- `input`: a description of the input value.
- `output`: a description of the output value
- `algorithm`:
  - `documentation`: a URL which references a specific github commit of
  the documentation that fully describes the transformation algorithm.
  - `implementation`: a URL that links to a reference implementation of the
  transformation algorithm. It is not necessary to use the implementation
  linked to here, as long as the implementation used implements the same
  transformation algorithm.
  - `description`: a brief description of the transformation algorithm.
- `test_vectors`: a URL which references a specific github commit of a
selection of test vectors that may be used to provide assurance that a
transformation algorithm implementation is correct. 


### Example Encoding
- data (object)
    The object with the encoding data
  - `id`: The encoding's DID; the id-string of its DID is the base58
  representation of the SHA2-256 hash of the canonical form of the value of
  the encoding object,
  - `content`: This property is used to hold immutable content:
    - `type`: "enc",
    - `name`: encoding's name string,
    - `version`: schema's version string,
    - `hash`:
      - `type`: the type of hash,
      - `value`: the hexadecimal value of the hash of the canonical form of
      the data object,
    - `data`: the encoding object

```
{
    "encoding": {
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
        "test_vectors": URL to specific github commit
    }
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


### Aries Data Registry Interface
We propose adding two Aries-Data-Registry-Interface methods for writing and
reading context objects:
- `write_encoding`: a method to write an encoding object to a data
registry. 
- `read_encoding`: a method to read an encoding object from a data
registry.

#### write_encoding
```
Writes an encoding object to the ledger.

#Params
submitter: {
    key: public key of the submitter,
    keystore: key manager where private key is stored
}, 
data: {
    id: identifier for the encoding object,
    encoding: encoding object,
    name: encoding name string,
    version: encoding version string,
    ver: version of the encoding object JSON format
},
registry: identifier for the registry

#Returns
registry_response: result as json,
error: {
    code: aries common error code,
    description:  aries common error description
}
```
#### read_encoding
```
Reads an encoding object from the ledger.

#Params
submitter (optional): {
    key: public key of the submitter,
    keystore: key manager where private key is stored
}, 
id: identifier for the encoding object,
registry: identifier for the registry

#Returns
registry_response: encoding object,
error: {
    code: aries common error code,
    description:  aries common error description
}
```

## Reference
[reference]: #reference

The following is a 
[reference implementation of various transformation algorithms](https://github.com/sovrin-foundation/aries-credx-framework-rs/blob/master/src/encoding/mod.rs)
Here is the paper that defines
[Camenisch-Lysyanskaya signatures.][CL-signatures] 
[CL-signatures]: (https://groups.csail.mit.edu/cis/pubs/lysyanskaya/cl02b.pdf)

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

