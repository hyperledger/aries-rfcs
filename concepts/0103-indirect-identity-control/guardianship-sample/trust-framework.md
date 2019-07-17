# Sample Trust Framework

[![mya](mya.jpg)](https://docs.google.com/presentation/d/1qUYQa7U1jczEFun3a7sB3lKHIprlwd7brfOU9hEJ34U/edit#slide=id.p7)

This document describes a sample trust framework for guardianship appropriate
to the [IRC-as-guardian-of-Mya-in-a-refugee-camp use case](
https://docs.google.com/presentation/d/1qUYQa7U1jczEFun3a7sB3lKHIprlwd7brfOU9hEJ34U/edit#slide=id.p7).
It is accompanied by a [sample schema for a guardianship credential](schema.md).

For general background on guardianship and their credentials, see [this slide presentation](
http://bit.ly/2vZGJoK).

The trust framework shown here is a reasonable starting point, and it demonstrates the breadth
of issues well. However, it probably would need significantly more depth to provide enough
guidance for developers writing production software, and to be legally robust in many different
jurisdictions.

### Name, Version, Author

This is the "Sovrin ID4All Vulnerable Populations Guardianship Trust Framework", version "1.0".
The trust framework is abbreviated in credential names and elsewhere as "SIVPGTF". It is
maintained by the Sovrin ID4All Working Group. The guardianship credential schema described here
is known as a "gcred".

### Scope

The trust framework applies to situations where NGOs like the International Red Cross/Red Crescent,
UNICEF, or Doctors Without Borders are servicing large populations of vulnerable refugees, both children
and adults, in formal camps. It assumes that the camps have at least modest, intermittent access to
telecommunications, and that that they operate with at least tacit approval from relevant legal
authorities. It may not provide enough guidance or protections in situations involving active combat,
or in legal jurisdictions where rule of law is very tenuous.

### Bases for Guardianship

In this framework, guardianship is based on one or more of the following formally defined rationales:

* `dependent-appointment`: The dependent was capable of appointing a guardian, and chose to appoint
  the named guardian(s) to that role. This is considered the strongest basis for guardianship.
* `kinship`: The dependent is known to be vulnerable because of age or disability. The guardian is
  related to the dependent and thus has a natural claim to guardianship status. This trust framework
  formally recognizes the following kinship relationships, in order from strongest to weakest:
  `biological-parent`, `step-parent`, `sibling`, `grandparent`, `aunt-or-uncle`, `first-cousin`,
  `indirect-relative`, `tribe-adult`. Kinships weaker than `first-cousin` are considered invalid
  as the basis for guardianship by themselves.
* `adjudicated`: A legal authority, or a council consisting of 5 grandmothers, chose the guardian.
* `self`: No suitable guardian could be found on another basis, but the dependent needed a guardian,
  so the guardian assumed the status until a better alternative could be found.

### Identifying a guardian

This framework assumes that credentials will use ZKP technology. Thus, no holder attributes are
embedded in a gcred except for the holder's blinded link secret. During a guardianship challenge,
the holder should include appropriate identifying evidence based on ZKP credential linking.

### Identifying a dependent

This framework defines the following formal ways to identify a dependent in a gcred:

* `credentialSubject.first_name`
* `credentialSubject.last_name`
* `credentialSubject.birth_date`
* `credentialSubject.gender`
* `credentialSubject.native_language`
* `credentialSubject.identifying_marks`
* `credentialSubject.photo`
* `credentialSubject.iris`
* `credentialSubject.fingerprint`

These fields should appear in all gcreds. First name should
be the name that the dependent acknowledges and answers to, not necessarily the legal first name.
Last name may be empty if it is unknown. Birth date may be approximate. Photo is required and must
be a color photo of at least 800x800 pixel resolution, taken at the time the guardianship credential
is issued, showing the dependent only, in good light. At least one of iris and fingerprint are strongly
recommended, but neither is required.

### Permissions

Guardians may be assigned some or all of the following formally defined permissions in this trust framework:

* `routine-medical-care`: Consent to normal medical treatment, including vaccinations, HIV tests, prescriptions,
  hospitalization, dental procedures, surgeries, and so forth.
* `do-not-resuscitate`: Consent to discontinue life support.
* `school`: Enroll or unenroll dependent in school programs. Customize courses of instruction.
* `necessaries`: Receive food, hygiene items, clothing, and other materials allocated to the dependent.
* `gender-identity`: Specify the gender by which the dependent shall be known.
* `religious-observance`: Require the dependent to observe religious practices, or consent for the dependent not to do so.
* `light-travel`: Take the dependent outside the camp, returning before dark.
* `extended-travel`: Take the dependent outside the camp for extended periods.
* `unenroll`: Permanently remove the dependent from the camp's care.
* `contracts`: Enter into financial or other legally binding arrangements on behalf of the dependent.
* `marriage-family-planning`: Give consent for the dependent to marry, or require them to do so. Direct the use
  contraceptives.
* `delegate`: Give permission to a non-guardian to exercise some of the guardian's privileges, possibly
  with restrictions.
* `successor`: Designate a replacement to assume guardian duties.
* `authorize`: Configure the permissions of self or other guardians.

### Constraints

A guardian's ability to control the dependent may be constrained in the following formal
ways by guardianship credentials that use this trust framework:

#### Boundary

Guardian can only operate within named boundaries, such as the boundaries of a country, province, city,
military command, river, etc. Boundaries are specified as a localized, comma-separated list of strings, where
each locale section begins with a `|` (pipe) character followed by an ISO639 language code followed by
a `:` (colon) character, followed by data. All localized values must describe the same
constraints; if one locale's description is more permissive than another's, the most restrictive
interpretation must be used. An example might be:

    "constraints.boundaries": "|en: West side of Euphrates river, within Baghdad city limits
        |es: lado oeste del río Eufrates, dentro del centro de Bagdad
        |fr: côté ouest de l'Euphrate, dans les limites de la ville de Bagdad
        |ar: الجانب الغربي من نهر الفرات ، داخل حدود مدينة بغداد"

#### Point of Origin and Radius

The `constraints.point_of_origin` and `radius` fields are an additional or alternative way to specify
a geographical constraint. They must be used together. Point of origin is a string that may use
latitude/longitude notation (e.g., "@40.4043328,-111.7761829,15z"), or a landmark. Landmarks
must be localized as described previously. Radius is an integer measured in kilometers.

    "constraints.point_of_origin": "|en: Red Crescent Sunrise Camp"
    "constraints.radius_km": 10

#### Jurisdictions

This is a comma-separated list of legal jurisdictions where the guardianship applies.
It is also localized:

    "constraints.jurisdictions": "|en: EU, India, Bangladesh"

#### Trigger and Circumstances

These are human-friendly description of circumstances that must apply in order to make
the guardian's status active. It may be used in conjunction with a trigger (see next).
It is vital that the wording of these fields be carefully chosen to minimize ambiguity;
carelessness could invite abuse. Note that each of these fields could be used separately.
A trigger by itself would unconditionally confer guardianship status; circumstances
without a trigger would require re-evaluation with every guardianship challenge and might
be used as long as an adult is unconscious or diagnosed with dementia, or while
traveling with a child, for example.

    "constraints.trigger": "|en: Death of parent"
    "constraints.circumstances": "|en: While a parent or adult sibling is unavailable, and no
        new guardian has been adjudicated.
        |ar: في حين أن أحد الوالدين أو الأشقاء البالغين غير متوفر ، وليس
                      الوصي الجديد تم الفصل فيه."

#### Timing

These allow calendar restrictions. Both start time and end time are expressed as ISO8601
timestamps in UTC timezone, but can be limited to day- instead of hour-and-minute-precision
(in which case timezone is irrelevant). Start time is inclusive, whereas end time is
exclusive (as soon as the date and time equals or exceeds end time, the guardianship
becomes invalid). Either value can be used by itself, in addition
to being used in combination.

    "constraints.startTime": "2019-07-01T18:00"
    "constraints.endTime": "2019-08-01"

### Auditing

It is strongly recommended that an audit trail be produced any time a guardian performs any
action on behalf of the dependent, except for `school` and `necessaries`. Reports of auditable
events are accomplished by generating a JSON document in the following format:

```JSON
{
    "@type": "SIVPGTF audit/1.0",
    "event_time": "2019-07-25T18:03:26",
    "event_place": "@40.4043328,-111.7761829,15z",
    "challenger": "amy.smith@redcross.org",
    "witness": "fred.jones@redcross.org",
    "guardian": "Farooq Abdul Sami",
    "basis": "natural parent",
    "dependent": "Isabel Sami, DOB 2009-05-21",
    "event": "enroll in class, receive books",
    "justifying_permissions": "school, necessaries"
    "evidence": ...photo of Farooq and Isabel
}
```

### Appeal

NGO staff (who receive delegated authority from the NGO that acts as guardian), and a council of 5 grandmothers
maintain a balance of powers. Decisions of either group may be appealed to the other. Conformant NGOs
must identify a resource that can adjudicate an escalated appeal, and this resource must be independent
in all respects--legal, financial, human, and otherwise--from the NGO. This resource must
have contact information in the form of a phone number, web site, or email address, and the contact
info must be provided in the guardianship credential in the `appeal_uri` field.

### Freshness and Offline Operation
[TODO]

### Revocation
[TODO]

### Best Practices

* Perform a guardianship challenge whenever a guardian performs an action requiring permissions other
than `school` and `necessaries`.
* Require the disclosure of dependent photo and the comparison of the photo to the dependent,
who must be physically present, for all operations using the `routine-medical-care`, `do-not-resuscitate`,
`gender-identity`, and `light-travel` permissions.
* Require a biometric match (fingerprint or iris strongly preferred, or else photo plus two related adult
witnesses) for the `extended travel`, `unenroll`, `contracts`, and `marriage-family-planning` permissions
to be exercised.
* Where possible.
