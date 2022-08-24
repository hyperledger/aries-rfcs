```jsonc
{
    "@context": [
        "https://github.com/hyperledger/aries-rfcs/blob/main/concepts/0430-machine-readable-governance-frameworks", 
        "https://fightthevirus.org/covid19-fw"
    ],
    "name": "COVID-19 Creds"
    "1.0",
    "description": "Which health-related credentials can be trusted for which levels of assurance, given which assumptions.",
    "docs_uri": "http://fightthevirus.org/covid19-fw/v1",
    "data_uri": "http://fightthevirus.org/covid19-fw/v1/tf.json",
    "topics": ["health", "public safety"],
    "jurisdictions": ["us", "uk", "eu"],
    "roles": ["healthcare-provider", "healthcare-worker", "patient"],
    "privileges": [
        {"name": "travel", "uri": "http://ftv.org/tf/travel"},
        {"name": "receive-healthcare", "uri": "http://ftv.org/tf/be-patient"},
        {"name": "tlc-fragile", "uri": "http://ftv.org/tf/tlc"},
        {"name": "visit-hot-zone", "uri": "http://ftv.org/tf/visit"}
    ],
    // Name all the duties that are significant to understanding
    // interactions in this governance framework. Each duty is defined for humans
    // at the specified URI, so a person can understand what it
    // entails.
    "duties": [
        {"name": "safe-accredit", "uri": "http://kmk.org/tf/responsible-accredit"},
        {"name": "GDPR-dat-control", "uri": "http://europa.eu/gdpr/trust-fw/gdpr-data-controller"}
        {"name": "GDPR-edu-verif", "uri": "http://kmk.org/tf/gdpr-verif"}
        {"name": "accept-kmk-tos", "uri": "http://kmk.org/tf/tos"}
    ],
    // Use DIDs to define key participants in the ecosystem. KMK is
    // the accreditation authority for higher education in Germany.
    // Here we show it using two different DIDs.
    "define": [
        {"name": "KMK": "id": "did:example:abc123"},
        {"name": "KMK": "id": "did:anotherexample:def456"},
    ], 
    // Describe role-based rules of behavior like "X can do Y if Z,"
    // where Z is a criterion following "when".
    "rules": [
        {"grant": ["accredit"], "when": {"name": "KMK"},
            "duties": ["safe-accredit"]},
        {"grant": ["issue-edu"], "when": {
                // Proof request (see RFC 0037) specifying that
                // institution is accredited by KMK.
            },
            // Any party who fulfills these criteria is considered
            // to have the "school" role.
            "thus": ["school"],
            // And is considered to have the "GDPR-dat-control" duty.
            "duties": ["GDPR-dat-control", "accept-kmk-tos"]
        },
        {"grant": "hold-edu", "when": {
                // Proof request specifying that holder is a human.
                // The presence of this item in the TF means that
                // conforming issuers are supposed to verify
                // humanness before issuing. Issuers can impose
                // additional criteria; this is just the base
                // requirement.
            },
            // Any party who fulfills these criteria is considered
            // to qualify for the "graduate" role.
            "thus": "graduate",
            "duties": ["accept-kmk-tos"]
        },
        // In this governance framework, anyone can request proof based
        // on credentials. No criteria are tested to map an entity
        // to the "anyone" role.
        {
            "grant": "request-proof", "thus": "anyone",
            "duties": ["GDPR-edu-verif", "accept-kmk-tos"]
        },
    ],
    // Is there an authority that audits interactions?
    "audit": {
        // Where should reports be submitted via http POST?
        "uri": "http://kmk.org/audit",
        // How likely is it that a given interaction needs to
        // be audited? Each party in the interaction picks a
        // random number between 0 and 1, inclusive; if the number
        // is <= this number, then that party submits a report about it.
        "probability": "0.01"
    },
    // Is there an authority to whom requests for redress can
    // be made, if one party feels like another violates
    // the governance framework? 
    "redress": {
        "uri": "http://kmk.org/redress"
    }
}   
```