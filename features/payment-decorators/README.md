# 00xx: Payment Decorators
- Author: Sam Curren (sam@sovrin.org), Daniel Hardman (daniel.hardman@gmail.com), Tomislav Markovski
- Start Date: 2019-04-22

## Status
- Status: [PROPOSED](/README.md#rfc-lifecycle)
- Status Date: 2019-06-11
- Status Note: Still being studied. This supersedes [Indy HIPE PR #129](
https://github.com/hyperledger/indy-hipe/pull/129).

## Summary
[summary]: #summary

Defines the `~payment_request` and `~payment_receipt` decorators, which offer standard
payment features in all DIDComm interactions. The `~payment_request` decorator lets
DIDComm take advantage of the [W3C's Payment Request API]( https://www.w3.org/TR/payment-request)
in an interoperable way.

## Motivation
[motivation]: #motivation

Instead of inventing custom messages for payments in each protocol, arbitrary messages
can express payment semantics with `~payment_request` and `~payment_receipt`
decorators. Individual protocol specs should clarify on which messages and under which
conditions the decorators are used.

## Tutorial

The [W3C's Payment Request API](https://www.w3.org/TR/payment-request) governs interactions
between three parties:

1. payer
2. payee
3. payment method

The payer is usually imagined to be a person operating a web browser,
the payee is imagined to be an online store, and the payment method might be something like
a credit card processing service. The payee emits a [PaymentRequest](
 https://www.w3.org/TR/payment-request/#paymentrequest-interface) JSON structure; this
causes the payee to be prompted. The payer decides whether to pay, and if so, which payment
method and options she prefers. The payer's choices are embodied in a [PaymentResponse](
https://www.w3.org/TR/payment-request/#paymentresponse-interface)
JSON structure. This is then used to select the appropriate codepath and inputs to
invoke the desired payment method.

[![API flow](payment-request-api-flow.png)](payment-request-api-flow.puml)

Notice that this flow does not include anything coming back to the payer. The PaymentResponse
is a response from the payer to the payer's own agent, embodying choices about which credit
card to use and which shipping options are desired; it's not a response that crosses identity
boundaries. That's reasonable because this is the Payment __Request__ API, not a Payment
Roundtrip API. It's only about requesting payments, not completing payments or reporting
results. Also, each payment method will have unique APIs for fulfillment and receipts; the
W3C spec does not attempt to harmonize them.

In DIDComm, the major emphasis is on interactions between parties with different identities.
Thus the PaymentRequest going from payer to payee overlaps with DIDComm's focus, but
the PaymentResponse moving
payee and the payer both hold DIDs to interact over a secure channel,
and are both using [agents](../../concepts/0004-agents/README.md) to do the low-level
interacting.

The _payer_:_payment method_ interaction that actually transfers funds _might_ be DIDComm
as well, but since there are many existing payment methods that don't use DIDComm, we will
not assume that in this version of the spec. In the interaction between payer and payee,
how the payment is actually consummated is not nearly as interesting as knowing with
confidence that the payment has been made. Thus, we will leave the _payer_:_payment method_
interaction out of scope, and allow payment consummation to be solved in whatever way
suits the circumstances.

This leaves us with the need to represent the W3C's PaymentRequest data structure

### `~payment_request`

A sample `~payment_request decorator might look like this:

```json=
{
  "~payment_request": {
    "methodData": [ ... ],
    "details": {
      id: "super-store-order-123-12312",
      displayItems: [
        {
          label: "Sub-total",
          amount: { currency: "USD", value: "55.00" },
        },
        {
          label: "Sales Tax",
          amount: { currency: "USD", value: "5.00" },
          type: "tax"
        },
      ],
      total: {
        label: "Total due",
        // The total is USD$65.00 here because we need to
        // add shipping (below). The selected shipping
        // costs USD$5.00.
         amount: { currency: "USD", value: "65.00" },
      },
    }
      "@id": "xyz", //functions like a purchase order number
      "method": "sovrin",
      "unit": "tokens",
      "amount": "0.2", //or int? look at token work
      "recipient": "<address>"
  }
}
```
The `~payment_request` decorator is a list of payment structures. When multiple options are
present, they represent multiple payment options for the same thing.

The decorator can be applied at any level of a message, allowing a single message to indicate
payment methods for different things.

**method**:  which payment method is requested.

**unit**: Unit applied to the `amount` attribute. Unit will relate to the payment method.

**amount**: amount being requested.

**recipient**: payment address when payment is made.

#### Potential future attributes

- non-required payments (required =  false)
- multiple payments at once options (_and_ instead of _or_)
- expiration (date in request, date in receipt somehow, maybe use the timing decorator)

### `~payment_receipt`

This decorator on a message indicates that a payment has been made.

```json=
{
  "~payment_receipt": [{
      "related_requests": ["xyz"],
      "method": "sovrin",
      "amount": 0.2,
      "receipt": "",
      "recipient": "<address>",
      "extra": "?"
  }]
}
```

**related_requests**: This contains the `@id`s of `~payment_requests` that this payment receipt satisfies.

**receipt**: String which identifies payment for verification.

**extra**: Contains extra information about the payment made.

#### Notes

- Proof of payment could be a stronger form of receipt.

## Tutorial

[tutorial]: #tutorial

These decorators can be incorporated into messages as appropriate. Each protocol that uses
these decorators must designate which messages they may be used in and where in the state/sequence
they appear. If these decorators appear in a message where they are not expected, they should be
ignored.

Here are some examples from Credential Exchange HIPE. Note that unrelated attributes have been
removed from the examples. There are two messages within the Credential Exchange message family where
payment decorators are appropriate: `credential-offer` and `credential-request`.

#### Example Credential Offer

This message is sent by the issuer. The payment request indicates that payment requested for this offered credential.

```json
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/credential-issuance/1.0/credential-offer",
    "@id": "<uuid-offer>",
    "cred_def_id": "KTwaKJkvyjKKf55uc6U8ZB:3:CL:59:tag1",
    "~payment_request": [{
      "@id": "offer-34567654324565454",
      "method": "sovrin",
      "unit": "tokens",
      "amount": "0.2",
      "recipient": "pay:sov:45678987654345678987"
  	}],
    "credential_preview": <json-ld object>,
    ///...
}
```

#### Example Credential Request

This Credential Request is sent to the issuer, indicating that they have paid the requested amount.

```json
{
    "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/credential-issuance/1.0/credential-request",
    "@id": "<uuid-request>",
    "cred_def_id": "KTwaKJkvyjKKf55uc6U8ZB:3:CL:59:tag1",
    "~payment_receipt": [{
        "related_requests": ["offer-34567654324565454"],
        "method": "sovrin",
        "amount": "0.2",
        "receipt": "",
        "recipient": "pay:sov:45678987654345678987",
        "extra": "something"
    }]
	///...
}
```

## Drawbacks

[drawbacks]: #drawbacks

A difficult aspect of this is managing all the way that different payments apply to this decorator.

## Rationale and alternatives
[alternatives]: #alternatives

- We could allow each message family to indicate payment information independently. This would be very flexible, but tedious and very messy.
- We could not include payment information in messages, but that would limit useful applications.

## Prior art
[prior-art]: #prior-art

What applies here?

## Unresolved questions
[unresolved]: #unresolved-questions

- Should `method` be a json-ld `@type` to allow for different payment attributes? Example:

```json
{
    "@id": "xyz", //functions like a purchase order number
    "@type": "http://example.com/paymentmethods/sovrin",
    "unit": "tokens",
    "amount": "0.2", //or int? look at token work
    "recipient": "<address>"
}
```

This could allow the customization of the fields required for that payment. For example, if a payment method only had one unit, or perhaps required two attributes for the recipient address.
