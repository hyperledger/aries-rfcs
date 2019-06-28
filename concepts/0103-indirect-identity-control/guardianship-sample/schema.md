# Sample Guardianship Schema

[![mya](mya.jpg)](https://docs.google.com/presentation/d/1qUYQa7U1jczEFun3a7sB3lKHIprlwd7brfOU9hEJ34U/edit#slide=id.p7)

This document presents a sample schema for a guardianship credential appropriate
to the [IRC-as-guardian-of-Mya-in-a-refugee-camp use case](
https://docs.google.com/presentation/d/1qUYQa7U1jczEFun3a7sB3lKHIprlwd7brfOU9hEJ34U/edit#slide=id.p7).
It is accompanied by a [sample trust framework](trust-framework.md).

The raw schema is here: [schema.json](schema.json)

For general background on guardianship and their credentials, see [this slide presentation](
http://bit.ly/2vZGJoK).

### How to Use

The schema documented here could be passed as the `attrs` arg to the [`indy_issuer_create_schema()`
method in libindy](https://github.com/hyperledger/indy-sdk/blob/af6ebf4d9c7b4b04ac0bf313c3a9805965e50e92/libindy/src/api/anoncreds.rs#L55).
The "1.0" in this document's name refers to the fact that we are using Indy 1.0-style schemas; we aren't trying to
use the rich schema constructs that will be available to us when the ["schema 2.0" effort](
https://github.com/hyperledger/indy-hipe/pull/119) is mature.

The actual JSON you would need to pass to the `indy_issuer_create_schema()` method is given in
the attached [schema.json](schema.json) file. In
code, if you place that file's content in a string variable and pass the variable as the `attrs`
arg, the schema will be registered on the ledger. You might use values like "Red Cross Vulnerable
Populations Guardianship Cred" and "1.0" as the `name` and `version` args to that same function.
You can see an example of how to make the call by looking at the ["Save Schema and Credential
Definition" How-To in Indy SDK](
https://github.com/hyperledger/indy-sdk/blob/master/docs/how-tos/save-schema-and-cred-def/README.md).

See the [accompanying trust framework](trust-framework.md) for an explanation of individual
fields.