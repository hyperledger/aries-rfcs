# 0693: Cross-Platform Credential Representation

- Authors: [Horacio Nunez](mailto:mailto:horacio.nunez@kiva.org) (Kiva Protocol)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2021-07-06
- Status Note:
- Supersedes:
- Start Date: 2021-02-10
- Tags: [feature](/tags.md#feature)

## Summary
Aries Agent developers currently build end user products without a standard method of rendering credentials.
This RFC proposes how the Aries community can reuse available open technologies to build such a rendering method.

Key results include:
- Feasibility of cross platform rendering.
- Enable branding of credentials.

This RFC also enumerate the specific challenges that by using this method could be tackled next.

## Motivation
The human computer interaction between agents and their users will always gravitate around credentials.
This interaction is more useful for users when their representation resembles that of their conventional 
(physical) counterparts.

Achieving effortless semiotic parity with analog credentials doesn't come easy or cheap. 
In fact, when reviewing new Aries-base projects, is always the case that the rendering of 
credentials with any form of branding is a demanding portion of the roadmap.

Since the work required here is never declarative the work never stops feeling sysyphean.
Indeed, the cost of writing code of representing a credential remains constant over time, no
matter how many times we do it.

Imagine if we achieve declarative while empowering branding.

### Entering SVG

The solution we propose is to adopt SVG as the default format to describe how to represent SSI credentials, and to 
introduce a convention to ensure that credentials values could be embedded in the final user interface. 
The following images illustrates how this can work:

![SVG + Credential Values](https://i.imgur.com/3ssaQUB.png "SVG + Credential Values")

### SVG + Credential Values

We propose a notation of the form `{{credential.values.[AttributeName]}}` and `{{credential.names.[AttributeName]}}`.
This way both values and attributes names can be used in branding activities.

#### Cross Platform

Since SVG is a web standard based on XML there isn't a shortage of existing tools to power brand and engineering needs 
right away. Indeed, any implementation will be powered by native SVG renderer and XML parser.

## Future work

* (RFC) A default credential representation to serves as community baseline
* (RFC) How to communicate the designated credential representation among agents.
* (RFC) Expand metadata available to include Revocation status.
* (Dev Tool) Standalone desktop tool to help design/brand a credential stored in an agent.
