# 0345: Community Coordinated Update
- Authors: [Sam Curren](telegramsam@gmail.com)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2019-12-26 (date you submit your PR)
- Status Note: Initial Draft
- Start Date: 2019-12-06
- Tags: concept

## Summary

This RFC describes the recommended process for coordinating a community update. This is not a mandate; this process should be adapted as useful to the circumstances of the update being performed.

## Motivation

Occasionally, an update will be needed that requires a coordinated change to be made across the community. These should be rare, but are inevitable. The steps in this process help avoid a coordinated software deployment, where multiple teams must fit a tight timeline of software deployment to avoid compatibility problems. Tightly coordinated software deployments are difficult and problematic, and should be avoided whenever possible.

## Tutorial

This process descries how to move from OLD to NEW. OLD and NEW represent the required change, where OLD represents the item being replaced, and NEW represents the item OLD will be replaced with. Often, these will be strings. 

In brief, we first accept OLD _and_ NEW while still defaulting to OLD, Then we default to NEW (while still accepting OLD), and then we remove support for OLD. These steps are coordinated with the community with a gracious timeline to allow for development cycles and deployment ease.

### Prerequisite: Community agreement on change.

Before these steps are taken, the community MUST agree on the change to be made. 

### Step 1: Accept OLD and NEW 

The first step of the process is to accept both OLD and NEW from other agents. Typically, this is done by detecting and converting one string to the other in as few places in the software as possible. This allows the software to use a common value internally, and constrains the change logic to where the values are received.

OLD should still be sent on outbound communication to other agents.

During step 1, it is acceptable (but optional) to begin sending NEW when receiving NEW from the other agent. OLD should still be sent by default when the other Agent's support is unknown.

This step is formalized by writing and RFC detailing which changes are expected in this update. This step is scheduled in the community by including the update RFC in a new version of the Interop Profile and setting a community target. The schedule should allow a generous time for development, generally between 1 and 3 months.

**Step 1 Coordination**: This is the most critical coordination step. The community should have completed step 1 _before_ moving to step 2.

### Step 2: Default to NEW

The second step changes the outbound value in use from OLD to NEW. Communication will not break with agents who have completed Step 1. 

OLD must still be accepted during step 2. OLD becomes deprecated.

During step 2, it is acceptable (but optional) to keep sending OLD when receiving OLD from the other agent. NEW should still be sent by default when the other Agent's support is unknown.

This step is formalized by writing an RFC detailing which changes are expected in this update. This step is scheduled by including the update RFC in a new version of the Interop Profile and setting a community target date. The schedule should allow a generous time for development, generally between 1 and 3 months.

**Step 2 Coordination**: The community should complete step 2 _before_ moving to step 3 to assure that OLD is no longer being sent prior to removing support.

### Step 3: Remove support for OLD.

Software will be updated to remove support for OLD. Continued use is expected to result in a failure or error as appropriate

This step is formalized by writing an RFC detailing which changes are expected in this update. Upon acceptance of the RFC, OLD is considered invalid. At this point, nobody should be sending the OLD.

**Step 3 Coordination**: The deadline for step 3 is less important than the previous steps, and may be scheduled at the convenience of each development team.

## Reference

This process should only be used for changes that are not detectable via the [Discover Features protocol](https://github.com/hyperledger/aries-rfcs/blob/master/features/0031-discover-features/README.md), either because the Discover Features Protocol cannot yet be run or the Discover Features Protocol does not reveal the change.

#### Changes NOT applicable to this process

Any changes that can be handled by increasing the version of a protocol should do so. The new version can be scheduled via Interop Profile directly without this process.

Example proper applications of this process include switching the base common Message Type URI, and DID Doc Service Types.

#### Pace

The pace for Steps 1 and 2 should be appropriate for the change in question, but should allow generous time to allow for developer scheduling, testing, and production deployment schedules. App store approval process sometimes take a bit of time. A generous time allowance eases the burden of implementing the change.

## Drawbacks

This approach invites the drawbacks of sanity, unpanicked deployments, and steady forward community progress.

## Rationale and alternatives

- The only other general approach is a tightly coordinated rollout, which should be avoided.

## Prior art

This process was discussed in [Issue 318](https://github.com/hyperledger/aries-rfcs/issues/318) and in person at the 2019 December Aries Connectathon.

## Unresolved questions

- Should template RFCs be included for the steps outlined?
## Implementations

The following lists the implementations (if any) of this RFC. Please do a pull request to add your implementation. If the implementation is open source, include a link to the repo or to the implementation within the repo. Please be consistent in the "Name" field so that a mechanical processing of the RFCs can generate a list of all RFCs supported by an Aries implementation.

*Implementation Notes* [may need to include a link to test results](https://github.com/hyperledger/aries-rfcs/blob/master/README.md#accepted).

Name / Link | Implementation Notes
--- | ---
 | 
