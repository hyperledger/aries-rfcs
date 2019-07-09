# Roles, Participants, Parties, and Controllers

## Roles

The __roles__ in a protocol are the perspectives (responsibilities, privileges) that parties take on an
interaction. 

This perspective is manifested in three general ways:

 * by the expectations that a party takes on in a protocol (ex. a role may be expected to do something to start a protocol).
 * by the messages that a party can and does use in the course of the protocol (some messages may be reserved for a single role, while other may used by some if not all roles).
 * by the state and the transition rules
 
Like parties, roles are normally known at the start of the protocol but this is not a requirement.

In an auction protocol, there are only two roles--*auctioneer*
and *bidder*--even though there may be many parties involved.

## Participants

The __participants__ in a protocol are the agents that consume and/or emit
[plaintext application-level messages](
https://github.com/hyperledger/indy-hipe/tree/master/text/0026-agent-file-format#agent-plaintext-messages-ap)
that embody the protocol's interaction. Alice, Bob, and
Carol may each have a cloud agent, a laptop, and a phone; if they engage in an
introduction protocol using phones, then the agents on their phones are the participants.
If the phones talk directly over Bluetooth, this is particularly clear--but even if the
phones leverage push notifications and HTTP such that cloud agents help with routing,
only the phone agents are participants, because only they maintain state for the
interaction underway. (The cloud agents would be __facilitators__, and the laptops would
be __bystanders__). When a protocol is complete, the participant agents know about the
outcome; they may need to synchronize or replicate their state before other agents of the
parties are aware.

## Parties

The __parties__ to a protocol are the entities directly responsible for achieving the protocol's goals.
When a protocol is high-level, parties are typically people or organizations; as protocols become lower-level,
parties may be specific agents tasked with detail work through delegation.

Imagine a situation where Alice wants a vacation. She engages with a travel agent named Bob. Together, they
begin an "arrange a vacation" protocol. Alice is responsible for expressing her parameters and proving her willingness to
pay; Bob is responsible for running a bunch of subprotocols to work out the details. Alice and Bob--not software
agents they use--are parties to this high-level protocol, since they share responsibility for its goals.

As soon as Alice has provided enough direction and hangs up the phone, Bob begins a sub-protocol with a hotel to book
a room for Alice. This sub-protocol has related but different goals--it is about booking a particular hotel room, not
about the vacation as a whole. We can see the difference when we consider that Bob could abandon the booking and choose
a different hotel entirely, without affecting the overarching "arrange a vacation" protocol.

With the change in goal, the parties have now changed, too. Bob and a hotel concierge are the ones responsible
for making the "book a hotel room" protocol progress. Alice is an approver and indirect stakeholder, but she is
not doing the work. (In [RACI terms](https://en.wikipedia.org/wiki/Responsibility_assignment_matrix),
Alice is an "accountable" or "approving" entity, but only Bob and the concierge are "responsible" parties.)

Now, as part of the hotel reservation, Bob tells the concierge that the guest would like access to a waverunner
to play in the ocean on day 2. The concierge engages in a sub-sub-protocol to reserve the waverunner. The
goal of this sub-sub-protocol is to reserve the equipment, not to book a hotel or arrange a vacation. The parties to this
sub-sub-protocol are the concierge and the person or automated system that manages waverunners.

Often, parties are known at the start of a protocol; however, that is not a requirement. Some protocols might commence
with some parties not yet known or assigned.

For many protocols, there are only two parties, and they are in a pairwise relationship. Other protocols
are more complex. Introductions involves three; an auction may involve many.

Normally, the parties that are involved in a protocol also participate in the interaction but this is not always the
case. Consider a gossip protocol, two parties may be talking about a third party. In this case, the third party would
not even know that the protocol was happening and would definitely not participate.

## Controllers

The __controllers__ in a protocol are entities that make decisions. They may or may not be direct parties.

Imagine a remote chess game between Bob and Carol, conducted with software agents. The chess protocol isn't
technically about _how to select a wise chess move_; it's about _communicating the moves_ so parties achieve
the shared goal of running a game to completion. Yet choices about moves are clearly made as the protocol
unfolds. These choices are made by controllers--Bob and Carol--while the agents responsible for the work of
moving the game forward wait with the protocol suspended.

In this case, Bob and Carol could be analyzed as parties to the protocol, as well as controllers. But in other
cases, the concepts are distinct. For example, in a protocol to issue credentials, the issuing institution
might use an AI and/or business automation as a controller.