# 0799: Aries Long Term Support Releases
- Authors: [Sam Curren](mailto:telegramsam@gmail.com)
- Status: [PROPOSED](/README.md#proposed)
- Since: 2023-11-07 
- Start Date: 2023-11-07 
- Tags: [concept](/tags.md#concept)

Long Term Support Releases of Aries projects will assist those using the software to integrate within their development processes.

## Motivation

Long Term Support releases allow stable use of projects without frequent code updates. Designating LTS releases frees projects to develop features without worry of disrupting those seeking feature stable deployments. 

## Project LTS Releases
- Details specific to each project will be found within the relevant repositories. 
- Projects SHOULD create an LTS policy within the code repository for the project. 
- Projects MAY alter any of these suggestions to match the needs of the project.

## LTS Release Tagging

- No Specific version number scheme for LTS releases are set Aries-wide. Each project can use any version numbering they desire. Projects must have a way to indicate patch releases.
- The README.md file within each repository must indicate which version is an LTS release, with a link to the release or branch of the LTS
- Each LTS release MUST include detailed release notes detailing the changes from the last LTS release, including complex details or gotchas.
- It is recommended, when possible, to designate an LTS release when a project reaches compliance with an Interop Profile, including an AIP.

## LTS Support Timeline

- Each LTS release MUST be supported for at least 9 months AFTER the next LTS release is designated.
- When the next LTS release is designated, the prior LTS release must clearly indicate the End of Support Date at least 9 months in future.
- A branch SHOULD be created to ease bugfixes and the maintenance of LTS patch releases.
- If a support term in excess of the minimum 9 months is chosen and and End of Support Date published, that period MUST be honored for that release.
- Projects may may designate an LTS release with any candance desired by the project.
- Frequent LTS relases may result in multiple LTS releases receiving support. Seeking community input for LTS release timing may decrease support efforts.

## LTS Release Updates

- Each LTS release MUST be updated for security updates via patch releases for the duration of its support lifetime.
- Each LTS release MAY include bugfixes that impact usability of the release.
- LTS patch releases MUST include detailed release notes.
- Updates MUST NOT include API updates, programatic interface changes, or major logic changes.

## References
This policy is inspired by the Fabric LTS Policy https://hyperledger.github.io/fabric-rfcs/text/0005-lts-release-strategy.html

