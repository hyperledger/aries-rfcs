import pytest

from state_machine import *

class NeverDone:
    def is_done(self):
        return False

class BeDone:
    def is_done(self):
        return True

@pytest.fixture
def sm():
    return StateMachine(NeverDone())

def test_no_state_on_start(sm):
    assert sm.state is None

def test_my_move_first(sm):
    sm.handle(SEND_MOVE_EVENT)
    assert sm.state == THEIR_MOVE_STATE

def test_their_move_first(sm):
    sm.handle(RECEIVE_MOVE_EVENT)
    assert sm.state == MY_MOVE_STATE

def test_illegal_move_by_me(sm):
    sm.handle(SEND_MOVE_EVENT)
    # Sending a move when it's the other person's turn
    # is our programmer error, so it should assert.
    with pytest.raises(AssertionError):
        sm.handle(SEND_MOVE_EVENT)

def test_wrapup_from_them(sm):
    sm.state = THEIR_MOVE_STATE
    sm.logic = BeDone()
    sm.handle(RECEIVE_MOVE_EVENT)
    assert sm.state == WRAP_UP_STATE
    sm.handle(SEND_OUTCOME_EVENT)
    assert sm.state == DONE_STATE

def test_wrapup_from_me(sm):
    sm.state = MY_MOVE_STATE
    sm.logic = BeDone()
    sm.handle(SEND_MOVE_EVENT)
    assert sm.state == WRAP_UP_STATE
    sm.handle(SEND_OUTCOME_EVENT)
    assert sm.state == DONE_STATE

def test_send_move_in_wrapup(sm):
    sm.state = WRAP_UP_STATE
    # Sending a move when it's time to send an outcome
    # is our programmer error, so this should assert.
    with pytest.raises(AssertionError):
        sm.handle(SEND_MOVE_EVENT)

def test_receive_move_in_wrapup(sm):
    sm.state = WRAP_UP_STATE
    # Receiving a move when it's time to send an outcome
    # is a programmer error on the other side. It shouldn't
    # assert in our code, but should generate an error.
    # This is an error by the other party, so it should
    # trigger on_error.
    sm.on_error = ErrorHandler()
    sm.handle(RECEIVE_MOVE_EVENT)
    assert bool(sm.on_error.msg)
    assert sm.state == WRAP_UP_STATE

class ErrorHandler:
    def __init__(self):
        self.msg = None

    def __call__(self, msg):
        self.msg = msg

def test_illegal_move_by_them(sm):
    # This is an error by the other party, so it should
    # trigger on_error.
    sm.on_error = ErrorHandler()
    sm.handle(RECEIVE_MOVE_EVENT)
    assert sm.on_error.msg is None
    assert sm.state == MY_MOVE_STATE
    sm.handle(RECEIVE_MOVE_EVENT)
    assert bool(sm.on_error.msg)
    assert sm.state == MY_MOVE_STATE

def test_early_exit_by_me(sm):
    sm.handle(RECEIVE_MOVE_EVENT)
    sm.handle(SEND_OUTCOME_EVENT)
    assert sm.state == DONE_STATE

def test_early_exit_by_them(sm):
    sm.handle(SEND_MOVE_EVENT)
    sm.handle(SEND_OUTCOME_EVENT)
    assert sm.state == DONE_STATE

def test_unrecognized_event(sm):
    with pytest.raises(AssertionError):
        sm.handle(25)

def test_event_while_done(sm):
    for i in range(len(EVENT_NAMES)):
        sm.state = DONE_STATE
        sm.on_error = ErrorHandler()
        if i == SEND_MOVE_EVENT:
            with pytest.raises(AssertionError):
                sm.handle(i)
            assert sm.on_error.msg is None
        elif i in [SEND_OUTCOME_EVENT, RECEIVE_OUTCOME_EVENT]:
            # should be ignored
            sm.handle(i)
            assert sm.on_error.msg is None
        else: #i == RECEIVE_MOVE_EVENT:
            sm.handle(i)
            assert bool(sm.on_error.msg)

class HookHandler:
    def __init__(self, response):
        self.event = None
        self.response = response
        self.state = None

    def __call__(self, state, event):
        self.state = state
        self.event = event
        return self.response

def test_pre_hooks_allow(sm):
    for i in range(DONE_STATE):
        sm.state = i
        sm.pre = HookHandler(True)
        sm.handle(SEND_OUTCOME_EVENT)
        # Because we're allowing a transition, the pre hook should
        # be called with old state, but now we should have new state.
        assert sm.pre.state != i
        assert sm.state == sm.pre.state
        assert sm.pre.event == SEND_OUTCOME_EVENT

def test_pre_hooks_deny(sm):
    for i in range(DONE_STATE):
        sm.state = i
        # This hook handler should refuse to allow us to transition.
        sm.pre = HookHandler(False)
        sm.post = HookHandler(None)
        sm.handle(SEND_OUTCOME_EVENT)
        # Because we're denying a transition, the pre hook should
        # be called with new state, and we should still have old state.
        assert sm.state == i
        assert sm.pre.state != i
        assert sm.pre.event == SEND_OUTCOME_EVENT
        # We should never have called the post event.
        assert sm.post.event == None

def test_post_hooks(sm):
    for i in range(DONE_STATE):
        sm.state = i
        sm.post = HookHandler(None)
        sm.handle(SEND_OUTCOME_EVENT)
        # Because we're allowing a transition, the post hook should
        # be called with new state.
        assert sm.state != i
        assert sm.post.state == sm.state
        assert sm.post.event == SEND_OUTCOME_EVENT
