# RAIkeep release preparation

## Preparing the next version

The RAIkeep custodian prepares the source and pushes the signed-off candidate. The release operator starts Engenho after reviewing the preflight result.

1. Check the proposed version against the component tags, registry entries and Engenho checkpoint. If publication is already underway, preserve the candidate commits and use the existing run's status for recovery.
2. Activate the release Python environment with pytest installed. From the umbrella checkout run `python3 scripts/bump-version.py 4.7.3`, substituting the agreed version for the next release. This assigns versions in the [release manifest](scripts/release-manifest.json), project files, Python metadata and coordinated dependency references. Keep bootstrap tooling pins and frozen distributions on their intended versions.
3. Review all current Markdown and PlantUML affected by the release. Update package install examples, API and CLI documentation, release notes, configuration examples and diagrams whose depicted behavior changed. Regenerate their tracked SVGs and check the rendered files and links. Preserve historical release records.
4. Run `python3 scripts/validate-release.py 4.7.3 4.7.2` with the candidate and previous versions. Inspect its exit status. Run applicable builds, tests and Rail/Vikela checks. Pack the candidate, check packaged documentation and perform isolated installation and CLI smoke tests. Record results, skips and failures in a versioned preflight record under `doc/`. The [4.6.7 record](doc/RELEASE_PREFLIGHT_4.6.7.md) shows the checks used for a previous release.
5. Commit and push each changed component to its repository. Then commit and push the exact submodule pointers, manifest, release notes and preflight documentation in the umbrella repository. Verify the remote project versions and pinned commits and check for clean worktrees.
6. Run `engenho release 4.7.3 --dry-run` from the prepared umbrella checkout. A successful simulation verifies the graph and preflight exercised by Engenho. Check the separate package-version and release-validator results before declaring the candidate ready.

## Publication and provisioning

The [4.7.3 preflight record](doc/RELEASE_PREFLIGHT_4.7.3.md) tracks candidate verification and outstanding checks.

The operator starts `engenho release 4.7.3` manually. Engenho coordinates version tags, publication workflows, registry indexing and the final umbrella release. After successful publication the operator can run `engenho provision all --release 4.7.3`. Engenho installs both `umgodi` and `jpit` from the `umgodi-json` distribution.
