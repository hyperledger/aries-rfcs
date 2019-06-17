"""
Implements design-by-contract utilities.
"""

class PreconditionViolation(Exception):
    def __init__(self, comment):
        super().__init__(f"Precondition violated -- {comment}")

class PostconditionViolation(Exception):
    def __init__(self, comment):
        super().__init__(f"Postcondition violated -- {comment}")

class InvariantViolation(Exception):
    def __init__(self, comment):
        super().__init__(f"Invariant violated -- {comment}")

def precondition(expr, comment):
    if not expr:
        raise PreconditionViolation(comment)

def postcondition(expr, comment):
    if not expr:
        raise PostconditionViolation(comment)

class Postcondition:
    def __init__(self, postchecker, comment):
        self.postchecker = postchecker
        self.comment = comment

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if not self.postchecker():
            raise PostconditionViolation(comment)
