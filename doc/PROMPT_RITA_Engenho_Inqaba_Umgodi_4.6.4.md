# Draft prompt for Rita: Inqaba and Umgodi publishing through Engenho

Historical draft. RAI assigned initial publishing and workflow setup to the RAIkeep custodian. See the [current handover](https://github.com/Burkhardt/RAIkeep/blob/main/doc/HANDOVER_RELEASE_PREP_v4.6.4.md).

Rita, please prepare Engenho and the new Python package repositories for the
RAIkeep 4.6.4 release. This is implementation and verification work; leave the
actual release invocation to RAI. Zébio's downstream work and TestCloud adoption
are not prerequisites for this task or for running RAIkeep's release chain.

## Repositories and package identities

| GitHub repository | PyPI distribution | Python import | Console commands |
| --- | --- | --- | --- |
| Burkhardt/inqaba | `inqaba` | `inqaba` | None currently |
| Burkhardt/umgodi-json | `umgodi-json` | `umgodi` | `jpit`, `umgodi` |

Local checkouts are under `/Users/RSB/Projects/GitHub/RAIkeep/`; Engenho is at
`/Users/RSB/Projects/GitHub/Engenho/`.

Current package versions are 0.1.0 and the umbrella manifest still says 4.6.3.
Target the upcoming coordinated 4.6.4 preparation, but derive and validate exact
versions from the finalized release metadata; do not publish the current draft.

## Implement the publishing integration

1. Add `.github/workflows/publish-pypi.yaml` to both new package repositories.
   The manifest already requests this filename with `dispatch: true`, and
   Engenho's ReleaseChain supplies a `release_ref` input. Verify that the requested
   immutable tag exists, the checkout matches it, and the tag version matches
   package metadata. Build and test before publication. Existing Vikela workflow
   conventions are a useful local starting point.
2. Use PyPI Trusted Publishing for the intended projects under Burkhardt's
   account. Match the repository owner/name, workflow filename and GitHub
   environment exactly. Scope OIDC permissions to publishing. Report any missing
   PyPI/GitHub account-side setup with the exact required fields; do not assume
   a committed workflow means the publisher registration exists.
3. Ensure Engenho's isolated verification environment installs pytest and each
   package's development dependencies, plus build/twine tooling. Do not require
   RAI to install pytest globally. Keep these tools out of runtime dependencies.
   Install the candidate Inqaba alongside Umgodi before running Umgodi tests;
   an unreleased dependency must not accidentally resolve from PyPI.
4. Build wheels and sdists, run `twine check`, and test a fresh installation from
   those artifacts. Verify imports, distribution/module version agreement,
   `pip check`, persistence smoke behavior and both CLI version commands.
   Retain READMEs, supplied SVG artwork and PlantUML/SVG class diagrams in the
   documented artifacts; preserve the assigned artwork.
5. Wire the existing paired preflight into the verification
   flow with a prepared environment. It runs both test suites, builds both
   distributions, checks sdist assets and installs wheels without an index.
   From the Umgodi repository, run
   `python scripts/preflight.py --inqaba ../inqaba`.
   Adapt integration
   as needed rather than duplicating divergent checks. Keep destructive cloud
   sequence tests opt-in and report that they were not run; hosted jobs must
   not pretend to exercise real Dropbox or Nkosikazi/Mzansi replication.
6. Enforce Inqaba publication and exact-version registry visibility before Umgodi
   publication. Keep the umbrella release last. Preserve immutable tags and
   checkpoint/resume behavior; never mark a package complete after only workflow
   dispatch or after finding an older version on PyPI.
7. Reconcile the manifest's `extraPackages` for Umgodi. Its `jpit` and `umgodi`
   names are console entry points, not additional distributions produced by the
   current wheel build. Do not wait for or publish phantom distributions. Keep
   compatibility-distribution decisions explicit and preserve existing users.
8. Preserve frozen `JsonPit.Python`/`jsonpit-python`. The current manifest still
   contains a legacy publish command referencing temporary 4.6.3 jsonpit/jpit
   artifacts. Prevent those stale artifacts from being used for this release;
   coordinate manifest ownership with the RAIkeep agent. Do not republish the
   frozen implementation or change its code as part of adding the new packages.

## Ownership and acceptance

Rita owns the Engenho integration and the two package publishing workflows for
this task. RAIkeep owns coordinated version/release-note changes, frozen-package
handling in the version bumper, document-link repairs and final library checks.
Coordinate edits to the shared release manifest so parallel work does not
overwrite changes. The proposed TestCloud key remains a separate RAIkeep
configuration item, not a downstream prerequisite.

Add focused runner/workflow validation for version/tag mismatch, failed tests,
missing prerequisites, dependency ordering, exact-version registry checks and
resume behavior. Include non-publishing verification of workflow inputs and
package identities. No live upload is needed to prove preparation correctness.

Return changed repositories/files and commits, commands/results, artifact hashes,
any remaining publisher-registration work, and whether Engenho's new-package
integration is ready. Distinguish that result from overall RAIkeep release
readiness. Do not run the production release chain, create release tags, upload
packages or provision machines as part of this preparation prompt.
