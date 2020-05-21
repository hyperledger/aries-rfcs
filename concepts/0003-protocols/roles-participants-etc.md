### Roles, Participants, Parties, and Controllers

#### Roles

The __roles__ in a protocol are the perspectives (responsibilities, privileges) that parties take i an
interaction.

This perspective is manifested in three general ways:

 * by the expectations that a party takes on in a protocol (ex. a role may be expected to do something to start a protocol).
 * by the messages that a party can and does use in the course of the protocol (some messages may be reserved for a single role, while other may used by some if not all roles).
 * by the state and the transition rules

Like parties, roles are normally known at the start of the protocol but this is not a requirement.

#### Participants

The __participants__ in a protocol are the agents that send and/or receive
[plaintext application-level messages](../../concepts/../features/0044-didcomm-file-and-mime-types/README.md)
that embody the protocol's interaction.

#### Parties

The __parties__ to a protocol are the entities directly responsible for achieving the protocol's goals.
When a protocol is high-level, parties are typically people or organizations; as protocols become lower-level,
parties may be specific agents delegated with the detail work.

Often, parties are known at the start of a protocol; however, that is not a requirement. Some protocols might commence
with some parties not yet known or assigned.

For many protocols, there are only two parties, and they are in a pairwise relationship. Other protocols
are more complex. Introductions involves three; an auction protocol may involve many.

#### Controllers

The __controllers__ in a protocol are entities that make decisions. They may or may not be direct parties. Controller supplies the business logic or rules that drive each specific instance of a protocol. They provide the personality of the agent suitable for the use case it implements.

With protocols, that means the controller decides when to initiate a protocol (often
based on some external event), and how to respond to an
event that occurred related to the instance of a protocol&mdash;the receipt of a message
or perhaps a timeout waiting on a reply to a sent message.