from dbc import *

# Declare flags so our IDE will recognize them. We'll set numeric values for them just below.
SIZE_OK = DESERIALIZE_OK = KEYS_OK = VALUES_OK = CONFIDENTIALITY = INTEGRITY = \
    AUTHENTICATED_ORIGIN = NONREPUDIATION = PFS = UNIQUENESS = LIMITED_SCOPE = 1

# Now set numeric values and derive other constants from these.
def _derive_constants(g):
    n = 1
    labels = []
    for key in g:
        if not key.startswith('_'):
            i = g[key]
            if isinstance(i, int):
                g[key] = n
                n *= 2
                label = key.replace('_OK', '').lower()
                labels.append(label)
    postcondition(n > 256, "should have defined a bunch of constants")
    # Figure out the shortest abbrev for each label.
    abbrevs = []
    for i in range(len(labels)):
        label = labels[i]
        for j in range(1, len(label)):
            prefix = label[:j]
            collides = False
            for k in range(len(labels)):
                if k != i:
                    other = labels[k]
                    if other.startswith(prefix):
                        collides = True
                        break
            if not collides:
                abbrevs.append(prefix)
                break
    postcondition(len(abbrevs) == len(labels), "should have found a unique abbrev for every label")
    return labels, abbrevs, n / 2

LABELS, ABBREVS, _MAX_FLAG = _derive_constants(globals())
del _derive_constants


class MessageTrustContext:
    """
    Describe the trust guarantees associated with a given message.
    See http://bit.ly/2UutabT for more information.
    """
    def __init__(self, affirmed: int = 0, denied: int = 0):
        precondition(affirmed & denied == 0, "what's affirmed and denied can't overlap")
        self._affirmed = affirmed
        self._denied = denied

    def affirm(self, flags):
        self._affirmed |= flags
        self._denied &= ~flags

    def deny(self, flags):
        self._denied |= flags
        self._affirmed &= ~flags

    def undefine(self, flags):
        self._affirmed &= ~flags
        self._denied &= ~flags

    def trust_for(self, flag):
        """
        Tells what trust applies for the given flag -- True if trusted, False if explicitly
        not trusted, or None if trust for that flag has not been evaluated.
        """
        if (self._affirmed & flag) == flag: return True
        if (self._denied & flag) == flag: return False
        return None

    @property
    def affirmed(self):
        return self._affirmed

    @property
    def denied(self):
        return self._denied

    @classmethod
    def get_flag_for_label(cls, label):
        n = 1
        for ab in ABBREVS:
            if label.startswith(ab):
                return n
            n *= 2
        return 0

    @classmethod
    def from_text(cls, txt):
        mtc = MessageTrustContext()
        if txt:
            if txt != '?':
                # Scenarios: A) start with something like +a+i-n-p; B) start with -n-p+a+i
                pluses = txt.replace(' ', '').lower().split('+')
                # Now we'll have: A) ['','a','i-n-p']; B) ['-n-p','a','i']
                for plus in pluses:
                    if not plus: continue
                    minuses = plus.split('-')
                    if minuses[0]:
                        # This is really a plus followed by minuses
                        mtc.affirm(MessageTrustContext.get_flag_for_label(minuses[0]))
                    for minus in minuses[1:]:
                        if minus:
                            mtc.deny(MessageTrustContext.get_flag_for_label(minus))
        return mtc

    @classmethod
    def _get_text(cls, flags, labels, mark, spacer):
        x = ''
        i = 0
        n = 1
        while n < _MAX_FLAG:
            if (flags & n) == n:
                x = x + spacer + mark + labels[i]
            n *= 2
            i += 1
        return x.lstrip()

    @property
    def abbrevs(self):
        """
        Return an abbreviated string that summarizes which flags are set and explicitly unset.
        """
        pluses = MessageTrustContext._get_text(self._affirmed, ABBREVS, '+', '')
        minuses = MessageTrustContext._get_text(self._denied, ABBREVS, '-', '')
        return '?' if (not pluses and not minuses) else pluses + minuses

    @property
    def labels(self):
        """
        Return a long-form string that describes which flags are set and explicitly unset.
        """
        pluses = MessageTrustContext._get_text(self._affirmed, LABELS, '+', ' ')
        minuses = MessageTrustContext._get_text(self._denied, LABELS, '-', ' ')
        if pluses and minuses: return pluses + ' ' + minuses
        if pluses: return pluses
        if minuses: return minuses
        return '?'

    def __str__(self):
        return self.abbrevs