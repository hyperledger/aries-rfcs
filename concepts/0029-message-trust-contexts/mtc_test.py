from mtc import *

UNDEFINED = MessageTrustContext()
ZERO = MessageTrustContext(denied=-1)
PARTIAL = MessageTrustContext(INTEGRITY | CONFIDENTIALITY)


def test_undefined_trust():
    assert '?' == UNDEFINED.abbrevs
    assert '?' == str(UNDEFINED)
    assert '?' == UNDEFINED.labels

def test_zero_trust():
    x = ZERO.abbrevs
    assert '+' not in x
    assert len(x.split('-')) > 8

def test_partial_trust():
    assert '+c+i' == PARTIAL.abbrevs
    assert '+c+i' == str(PARTIAL)
    assert '+confidentiality +integrity' == PARTIAL.labels


def test_flag_changes():
    x = MessageTrustContext()
    assert x.trust_for(SIZE_OK) is None
    assert '?' == x.abbrevs
    x.affirm(SIZE_OK | VALUES_OK)
    assert x.trust_for(SIZE_OK | VALUES_OK) == True
    assert '+s+v' == x.abbrevs
    assert '+size +values' == x.labels
    x.deny(SIZE_OK)
    assert x.trust_for(SIZE_OK) == False
    assert x.trust_for(VALUES_OK) == True
    assert '+v-s' == x.abbrevs
    assert '+values -size' == x.labels

def test_from_text():
    x = MessageTrustContext.from_text("+s+A --n +x")
    assert x.affirmed == (SIZE_OK | AUTHENTICATED_ORIGIN)
    assert x.denied == NONREPUDIATION
    x = MessageTrustContext.from_text("+Integrity -Confidentiality")
    assert x.affirmed == INTEGRITY
    assert x.denied == CONFIDENTIALITY
