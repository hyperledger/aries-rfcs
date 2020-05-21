### State Details and State Machines

While some protocols have only one sequence of states to manage, in most
different roles perceive the interaction differently. The sequence of states
for each role needs to be described with care in the RFC.

#### State machines

By convention, protocol state and sequence rules are described using the
concept of state machines, and we encourage developers who implement
protocols to build them that way.

Among other benefits, this helps with error handling: when one agent
sends a [`report-problem`](../../features/0035-report-problem/README.md)
message to another, the message can make it crystal clear which state it
has fallen back to as a result of the error.

Many developers will have encountered a formal of definition of state machines as
they wrote parsers or worked on other highly demanding tasks, and may worry
that state machines are heavy and intimidating. But as they are used in
Aries protocols, state machines are straightforward and elegant. They
cleanly encapsulate logic that would otherwise be a bunch of conditionals
scattered throughout agent code. The [tictactoe example protocol](tictactoe/README.md)
example includes a complete state machine in less than 50
lines of [python code](tictactoe/state_machine.py), with [tests](tictactoe/test_state_machine.py).

For an extended discussion of how state machines can be used, including in nested
protocols, and with hooks that let custom processing happen at each point in
a flow, see [https://github.com/dhh1128/distributed-state-machine](
https://github.com/dhh1128/distributed-state-machine/blob/master/README.md).

#### Processing Points

A protocol definition describes key points in the flow where business logic
can attach. Some of these __processing points__ are obvious, because the
protocol makes calls for decisions to be made. Others are implicit. Some examples
include:

* The _beginning_ and _end_.
* The _launch of a subprotocol_.
* The _completion of a subprotocol_, or the _subprotocol changing state_.
* _Sending a message_. (For each send, the sender could choose to go silent
and abandon the interaction instead, though many
protocols would ask for notification to be emitted as best practice.)
* (Receiving a message_. (Requires validation, then integration
with policy and processes internal to the agent and its sovereign domain,
to move the interaction forward.)