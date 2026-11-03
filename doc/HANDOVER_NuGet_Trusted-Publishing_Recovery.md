# NuGet Trusted Publishing migration and v4.5.16 recovery

Date: 2026-11-02.
Status: workflow changes prepared locally; NuGet policy configuration and rollout
remain pending. No workflow dispatch, package upload, tag change, or remote push
is authorized by this document itself.

## Required NuGet policies

Open the NuGet account's Trusted Publishing page, not API Keys. Each policy uses:

- Package Owner: `Burkhardt`.
- CI/CD Provider: `GitHub Actions`.
- Repository Owner: `Burkhardt`.
- Workflow File: `publish-nuget.yml` (filename only).
- Environment: empty; these jobs do not declare an environment.
- Scope: push new versions of existing packages.

Create or verify these four policies. Restrict each package pattern to its exact
package ID; do not use a wildcard for the entire account.

| Suggested policy name | GitHub Repository | NuGet package pattern |
| --- | --- | --- |
| OsLib GitHub publishing | `OsLib` | `OsLibCore` |
| RaiUtils GitHub publishing | `RaiUtils` | `RaiUtils` |
| RaiImage GitHub publishing | `RaiImage` | `RaiImage` |
| JsonPit GitHub publishing | `JsonPit` | `JsonPit` |

The repository and package names are distinct for OsLib: GitHub uses `OsLib`;
NuGet uses `OsLibCore`. Policy names are descriptive labels, not package IDs.
No replacement long-lived API key or GitHub secret is required.

Reference: [NuGet Trusted Publishing setup](https://learn.microsoft.com/en-us/nuget/nuget-org/trusted-publishing).

## Prepared workflow behavior

Each of the four repositories has a local `codex/nuget-trusted-publishing` branch
in `/private/tmp/raikeep-trusted-publishing/<Repository>`.

- The publish job grants `contents: read` and `id-token: write`.
- `NuGet/login@v1` authenticates as NuGet user `Burkhardt` immediately before
  publication, producing a short-lived publishing key.
- The push step uses that step's output instead of `secrets.NUGET_API_KEY`.
- Tag-triggered publication retains the `v*` trigger.
- Manual dispatch requires an explicit `release_ref`, such as `v4.5.16`.
- Input validation permits only `vX.Y.Z` before checkout.
- Checkout explicitly selects `refs/tags/<release_ref>`, never the workflow
  branch or a similarly named branch.
- The checked-out project's version must match the selected tag. The workflow
  logs the actual source commit before building and packing.

These are workflow-only changes. They do not change package versions or product
source. Original release checkouts, umbrella gitlinks, and tags remain intact.

## Recovery boundary

The failed OsLib tag run uses the old static-key workflow. Rerunning that same
run will still use the old workflow; creating a NuGet policy alone cannot fix it.
Do not move or delete `v4.5.16` to get a different workflow.

For the current release, publish the migration **branch** separately after review,
leaving each repository's prepared release `main` and its immutable tag intact.
Its existing default-branch workflow already has `workflow_dispatch`, so the
corrected branch workflow can be selected explicitly for recovery.

Once the OsLib branch is available remotely and its NuGet policy exists, this
command is the intended manual recovery trigger; it publishes a package and must
only be run when RAI explicitly authorizes that release step:

```zsh
gh workflow run publish-nuget.yml \
  --repo Burkhardt/OsLib \
  --ref codex/nuget-trusted-publishing \
  -f release_ref=v4.5.16
```

That selects the corrected workflow from the branch and builds the existing
`v4.5.16` tag. It does not publish the migration branch's source as v4.5.16.

The other three repositories require the same corrected workflow when their
original v4.5.16 source is tagged. Preserve dependency order and wait for each
package to become installable before proceeding. Their automatic original-tag
runs still use the static-key workflow; do not mistake those runs for the
corrected manual dispatch or blindly restart the ordinary chain.

Do not merge these workflow commits into release `main` in the middle of the
chain: changing prepared child HEADs can break umbrella pointer and tag checks.
Likewise, the ordinary chain currently selects workflow runs by tag branch and
does not automatically recognize a successful dispatch from a migration branch.
Coordinate remaining recovery steps explicitly with RAI. Finalize the umbrella
only after every child package and immutable tag has been verified. The existing
`--resume-after-raiguard` mode is the final verification/umbrella path once all
children have actually completed.

After the interrupted release is complete, integrate the workflow-only commits
into each repository's main branch and synchronize umbrella pointers as part of
the next preparation. Normal future tag releases then use Trusted Publishing
without the recovery branch. Remove unused expired static secrets after migration
is verified; do not delete credentials that other workflows may still need.

## Verification completed locally

- Actionlint 1.7.7 validates all four workflow files.
- The focused Python suite checks authentication wiring, rejects malformed and
  shell-like tag values, executes the actual Bash version guards, and verifies
  original-tag checkout against a newer branch with a colliding branch name.
- All tests use temporary local Git fixtures; no login, upload, workflow dispatch,
  or remote writes occur.

Run the focused tests against these sibling worktrees:

```zsh
python3 /private/tmp/raikeep-trusted-publishing/RAIkeep/scripts/test-trusted-publishing.py \
  /private/tmp/raikeep-trusted-publishing
```

No product code changed, so full solution compilation/tests were not repeated.
NuGet's actual token exchange remains unverified until the matching policies are
created and the first explicitly authorized publication runs.
