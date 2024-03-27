# Define states and events, including symbolic (numeric) constants and their friendly names.
STATE_NAMES = ['my-move', 'their-move', 'wrap-up', 'done']
for i in range(len(STATE_NAMES)):
    globals()[STATE_NAMES[i].replace('-', '_').upper() + '_STATE'] = i

EVENT_NAMES = ['send move', 'receive move', 'send outcome', 'receive outcome']
for i in range(len(EVENT_NAMES)):
    globals()[EVENT_NAMES[i].upper().replace(' ', '_') + '_EVENT'] = i


class StateMachine:
    def __init__(self, logic, pre=None, post=None, on_error=None):
        self.state = None
        self.logic = logic
        self.pre = pre
        self.post = post
        self.on_error = on_error

    def handle(self, event):
        s = self.state
        if event == SEND_MOVE_EVENT:
            if s in [None, MY_MOVE_STATE]:
                self._transition_to(WRAP_UP_STATE if self.logic.is_done() else THEIR_MOVE_STATE, event)
            else:
                raise AssertionError(f"Programmer error; I can't move when state = {STATE_NAMES[s]}.")
        elif event == RECEIVE_MOVE_EVENT:
            if s in [None, THEIR_MOVE_STATE]:
                self._transition_to(WRAP_UP_STATE if self.logic.is_done() else MY_MOVE_STATE, event)
            else:
                self._on_error(f"Other party can't move when state = {STATE_NAMES[s]}")
        elif event in [SEND_OUTCOME_EVENT, RECEIVE_OUTCOME_EVENT]:
            if s != DONE_STATE:
                self._transition_to(DONE_STATE, event)
        else:
            raise AssertionError("Illegal event %d." % event)

    def _on_error(self, msg):
        if self.on_error:
            self.on_error(msg)

    def _transition_to(self, state, event):
        if self.pre:
            # Ask permission before transitioning
            if not self.pre(state, event):
                return
        self.state = state
        if self.post:
            self.post(state, event)