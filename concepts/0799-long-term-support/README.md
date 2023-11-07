# 0799 Aries Long Term Support Releases
- Authors: [Sam Curren](telegramsam@gmail.com)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2023-11-07 
- Start Date: 2023-11-07 
- Tags: [concept](/tags.md#concept)

Long Term Support Releases of Aries projects will assist those using the software to integrate within their development processes.

These LTS details are guides for Aries code projects. Details specific to each project will be found within the relevant repositories.

## Motivation

Long Term Support releases allow stable use of projects without frequent code updates. Designating LTS releases frees projects to develop features without worry of disrupting those seeking feature stable deployments. 

It is recommended, when possible, to designate an LTS release when a project reaches compliance with an Interop Profile, AIP or other.

## LTS Release Tagging

- No Specific version number scheme for LTS releases are set Aries-wide. Each project can use any version numbering they desire.
- An LTS Release is specified by including the letters LTS after the version number.
- The README.md file within each repository must indicate which version is an LTS release, with a link to the release or branch of the LTS

## LTS Support Timeline

- Each LTS release MUST be supported for at least 9 months AFTER the next LTS release is designated.
- When the next LTS release is designated, the prior LTS release must clearly indicate the End of Support Date at least 9 months in future.
- If a support term in excess of the minimum 9 months is chosen and and End of Support Date published, that period MUST be honored for that release.
- Projects may may designate an LTS release with any candance desired by the project.
- Frequent LTS relases may result in multiple LTS releases receiving support. Seeking community input for LTS release timing may decrease support efforts.

## LTS Release Updates

- Each LTS release MUST be updated for security updates for the duration of its support lifetime.
- Each LTS release MAY include bugfixes that impact usability of the release.
- Updates MUST NOT include API updates, programatic interface changes, or major logic changes.

## References
This policy is inspired by the Fabric LTS Policy https://hyperledger.github.io/fabric-rfcs/text/0005-lts-release-strategy.html

