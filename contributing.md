# ![Aries RFCs](collateral/aries-rfcs-logo.png)

## Contributing

### Do you need an RFC?

Use an RFC to advocate substantial changes to the Aries ecosystem, where
those changes need to be understood by developers who *use* Aries. Minor
changes are not RFC-worthy, and changes that are internal in nature,
invisible to those consuming Aries, should be documented elsewhere.

### Preparation

Before writing an RFC, consider exploring the idea on
[chat](https://chat.hyperledger.org/channel/aries), on community calls
(see the [Hyperledger Community Calendar](
https://wiki.hyperledger.org/community/calendar-public-meetings)),
or on [aries@lists.hyperledger.org](
mailto:aries@lists.hyperledger.org). Encouraging feedback from maintainers
is a good sign that you're on the right track.

### How to propose an RFC

  - Fork [the RFC repo](https://github.com/hyperledger/aries-RFC).
  - Pick a descriptive folder name for your RFC. Don't pick a number yet.
    See [Best Practices: RFC Naming](concepts/0074-didcomm-best-practices/README.md#rfc-naming)
    for guidance.
  - Decide which parent folder is appropriate for your RFC.
    If it is about a specific protocol or decorator or feature, its parent
    should be /features; if it is about a concept that will be used in many
    different features, its parent should be /concepts.
  - Create the folder and copy `0000-template.md` to `<parent>/<your folder name>/README.md`.
  - Fill in the RFC. Put care into the details: RFCs that do not present
    convincing motivation, demonstrate an understanding of the impact of the
    design, or are disingenuous about the drawbacks or alternatives tend to be
    poorly received. You can add supporting artifacts, such as diagrams and sample
    data, in the RFC's folder. Make sure you follow [community-endorsed best
    practices](concepts/0074-didcomm-best-practices/README.md).
  - Consider how the RFC should be [tagged](/tags.md).
  - Assign a number to your RFC. Get the number by loading <a target="rfcnum"
    href="https://dhh1128.github.io/next-aries-rfc-num/">this web page</a> (or,
    if you want to do it the hard way, by inspecting open and closed PRs against
    this repo to figure out what the next PR number will be). Rename your folder from
    `<your folder name>` to `<your 4-digit number>-<your folder name>`. At the
    top of your README.md, modify the title so it is in the form: `<your 4-digit
    number>: Friendly Version of Your Title`. Commit your changes.
  - In the root of the repo, run `python code/generate_index.py` to update the index
    with your new RFC.
  - In the root of your repo, run `pytest code` to see whether your RFC passes all
    automated tests. The RFC tests are simple. They just check for things like
    naming conventions and hyperlink correctness.
  - Commit the updated version of /index.md and push your changes.
  - Submit a pull request.

Make sure that all of your commits satisfy the [DCO requirements](
https://github.com/probot/dco#how-it-works) of the repo and conform
to the license restrictions noted [below](#intellectual-property).

The RFC Maintainers will check to see if the process has been followed, and request
any process changes before merging the PR.

When the PR is merged, your RFC is now formally in the PROPOSED state.

### Changing an RFC Status

The lifecycle of an RFC is driven by the author or current champion of the RFC. To move an RFC along
in the lifecycle, submit a PR with the following characteristics:

- The PR should __ONLY__ change the RFC status. Note that this requires refreshing the index (`python code/generate_index.py && pytest code`).
- The title of the PR should include a deadline date for merging the PR and the referenced RFC.
  - Example: `Status to Accepted, deadline 2019.08.15, RFC 0095-basic-message`
- The PR comment should document why the status is being changed.
- The deadline date should be 2 weeks after announcing the proposed status change on an Aries WG call. The PR should also be announced on the [#aries rocketchat channel](https://chat.hyperledger.org/channel/aries).
- Barring negative feedback from the community, the repo's maintainers should merge the PR after the deadline.
- The deadline should be moved by two weeks after addressing each substantive change to the RFC made during the status change review period.


### How to get an RFC demonstrated

If your RFC is a feature, it's common (though not strictly required) for
it to go to a DEMONSTRATED state next. Write some code that embodies the
concepts in the RFC. Publish the code. Then [submit a PR](#changing-an-rfc-status) that adds your
early implementation to the [Implementations section](/0000-template.md#implementations),
and that changes the status to DEMONSTRATED. These PRs should be accepted
immediately, as long as all unit tests pass.

### How to get an RFC accepted

After your RFC is merged and officially acquires the [PROPOSED status](
README.md#status--proposed), the RFC will receive feedback from the larger community,
and the author should be prepared to revise it. Updates may be made via pull request,
and those changes will be merged as long as the process is followed.

When you believe that the RFC is mature enough (feedback is somewhat resolved,
consensus is emerging, and implementation against it makes sense), [submit a PR](#changing-an-rfc-status) that
changes the status to [ACCEPTED](README.md#status--accepted). The status change PR
will remain open until the maintainers agree on the status change.

>NOTE: contributors who used the Indy HIPE process prior to May 2019 should
see the acceptance process substantially simplified under this approach.
The bar for acceptance is not perfect consensus and all issues resolved;
it's just general agreement that a doc is "close enough" that it makes
sense to put it on a standards track where it can be improved as
implementation teaches us what to tweak.

### How to get an RFC adopted

An accepted RFC is a standards-track document. It becomes an acknowledged
standard when there is evidence that the community is deriving meaningful
value from it. So:

- Implement the ideas, and find out who else is implementing.
- Socialize the ideas. Use them in other RFCs and documentation.
- Update the agent test suite to reflect the ideas.

When you believe an RFC is a _de facto_ standard, [raise a PR](#changing-an-rfc-status) that changes the
status to [ADOPTED](README.md#status--adopted).  If the community is friendly
to the idea, the doc will enter a two-week "Final Comment Period" (FCP), after
which there will be a vote on disposition.

### Intellectual Property

This repository is licensed under an [Apache 2 License](LICENSE). It is protected
by a [Developer Certificate of Origin](https://developercertificate.org/) on every commit.
This means that any contributions you make must be licensed in an Apache-2-compatible
way, and must be free from patent encumbrances or additional terms and conditions. By
raising a PR, you certify that this is the case for your contribution.

### Signing commits (DCO)

If you are here because you forgot to sign your commits, fear not. Check out [how to sign previous commits](#how-to-sign-previous-commits)

We use developer certificate of origin (DCO) in all hyperledger repositories, so to get your pull requests accepted, you must certify your commits by signing off on each commit.

#### Signing your current commit
  - `$ git commit -s -m "your commit message"`
  - To see if your commits have been signed off, run `$ git log --show-signature`
  - If you need to re-sign the most current commit, use `$ git commit --amend --no-edit -s`.

The `-s` flag signs the commit message with your name and email.

#### How to Sign Previous Commits
   1. Use `git log --show-signature` to see which commits need to be signed.
   1. Go into interactive rebase mode using `$ git rebase -i HEAD~X` where X is the number of commits up to the most current commit you would like to see.
   1. You will see a list of the commits in a text file. **On the line after each commit you need to sign**, add `exec git commit --amend --no-edit -s` with the lowercase `-s` adding a text signature in the commit body. Example that signs both commits:
      ```
      pick 12345 commit message
      exec git commit --amend --no-edit -s
      pick 67890 commit message
      exec git commit --amend --no-edit -s
      ```
    1. If you need to re-sign a bunch of previous commits at once, find the earliest unsigned commit using `git log --show-signature` and use that the HASH of the commit before it in this command: `git rebase --exec 'git commit --amend --no-edit -n -s' -i HASH`. This will sign every commit from most recent to right before the HASH.
    1. You will probably need to do a force push `git push -f` if you had previously pushed unsigned commits to remote.

