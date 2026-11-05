# Prompt for Rita: CR077 release and selective Vikela provisioning

Rita, implement the CR077 publication/provisioning changes in Engenho using its
existing typed runner and result contracts. Do not extend release-chain.sh or
invoke it for Vikela. RAIkeep and **vikela** target **4.6.0** together under the
Twin-Shield Doctrine. This supersedes the original CR077 0.1.0 launch target;
optional installation remains independent of the runtime packages. Confirm the
final local commit IDs with the operator
before dispatching publication; working-tree paths are not immutable references.

## Concrete changes and package identities

- RAIkeep includes the existing `vikela/` git submodule, remote
  `https://github.com/Burkhardt/vikela.git`.
- PyPI distribution/import/CLI are all `vikela`; there is no pitlint package.
- `vikela==4.6.0` is the independent CLI with no third-party runtime dependencies.
- `vikela[pylint]==4.6.0` adds the Pylint checker. Invocation:
  `python -m pylint --load-plugins=vikela ...`.
- `vikela[notebook]==4.6.0` adds IPython for `%load_ext vikela` / `%%vikela`.
- `jsonpit` and `jpit` launch in lockstep with Vikela at 4.6.0; neither runtime
  distribution depends on Vikela. Provisioning them must not silently install
  development tooling.
- RaiGuard.Analyzer/RaiGuard 4.6.0 use semantic receiver/provenance checks. CLI
  `rail check` performs non-executing source compilation with restored references;
  missing references are reported as incomplete resolution, not manufactured
  mutation warnings.

## Validation gates

Run in a complete synchronized umbrella checkout, with its intended Python test
interpreter and the normal configured-cloud/SSH prerequisites:

```sh
dotnet test RAIkeep.slnx
python -m pytest JsonPit.Python/tests
python -m pytest vikela/tests
python scripts/check-cr077-africastage.py --source <AfricaStage-checkout> --output <report.json>
```

For the Python tests, install their dev requirements in the validation environment
and point PYTHONPATH at JsonPit.Python when running from the umbrella. Install
Vikela with its dev extra in that environment. A missing interpreter, configured
cloud, SSH access, skipped cloud test, or incomplete source reference context is
not successful acceptance evidence. Preserve stdout/stderr and test result files.
The historical-source checker uses git show/read-only snapshots and a semantic
positive control; its unresolved dependency notes must accompany the results.

Build Vikela from its own repository with `python -m build --outdir <empty-dir>`
and `python -m twine check <empty-dir>/*`. Confirm wheel/sdist metadata Name=vikela
and Version=4.6.0; hash the actual artifacts. Smoke-test the wheel in a fresh venv:
version, help, JSON, findings/clean exit codes, Pylint load, and IPython extension.
Use the built package, not only an editable checkout.

## Candidate inventory and artwork policy

The 10 .NET child repositories produce **11 NuGet packages**: Amafu, OsLibCore,
RaiUtils, RaiImage, RaiDiagram, RaidSeeder, JsonPit, ImgSeeder, PitSeeder,
RaiGuard, and RaiGuard.Analyzer. Do not omit either RaiGuard distribution.
Python produces **three distributions**: jsonpit, its existing jpit companion,
and Vikela. All 14 distributions are version 4.6.0. Wheels plus sdists yield
17 candidate artifact files when combined with the 11 nupkg files.

JsonPit and Vikela source archives contain their assets directories, including
canonical SVGs and the 128/192/512 PNGs. Python wheels deliberately contain code
and package metadata without the artwork. Their README hero marks use absolute
repository asset URLs so PyPI does not depend on local files. JsonPit's NuGet
PackageIcon is assets/logo-128x128.png, included inside the nupkg.

Reproduce this selection when rebuilding from the recorded child commits. Do not
upload all files found in an old artifact directory. Check exact package IDs,
versions, metadata, dependencies, CLI runtime versions, asset inclusion/exclusion,
and SHA-256 digests before the runner advances to publication.

## Current gate status

Candidate packaging verification passed for every 4.6.0 distribution, but the
latest full solution run is **not green**: 1,191 passed and one failed.
RemoteSync_MasterClient_FullScenario created its local pit successfully, then
waited 600 seconds without seeing that file on Mzansi through OneDrive. It did
not reach the remote mutation phase. Python runtime (131), Vikela (71), and
consistency checks (141) passed. The remote conflict and cross-language tests
also passed. Preserve this failure as a blocking acceptance result; do not
silently exclude the test or infer provider health from successful packaging.
The initial implementation's successful full run is historical evidence, not a
replacement for this preflight result. See the current evidence receipt and
implementation report for exact sources, artifacts, and logs.

## Publication and recovery

Vikela has `.github/workflows/publish-pypi.yaml`, manually dispatched with
`release_ref: v4.6.0`. It checks the version/tag, runs tests, builds once, and
publishes those artifacts through PyPI Trusted Publishing. Required policy:
GitHub owner Burkhardt, repository vikela, workflow publish-pypi.yaml,
environment pypi. The owner must establish that policy before the publish step;
there are no long-lived PyPI API keys in this implementation. This workflow has
not been remotely exercised merely because its local tests pass.

Keep NuGet/JsonPit dependency order and existing verified publication contracts.
Vikela is independent of the runtime NuGet dependency chain; keep its version aligned with the
4.6.0 umbrella while preserving its optional development-tool packaging. Do not publish dependent
packages until their exact dependencies are installable. The umbrella tag/release
is the final coordinated step after successful package publication and visibility.

Record repository, immutable source SHA, tag, package/version, artifact hashes,
workflow/run ID, and visibility result per publication. Recover using the same
source/tag and verified package state. Do not move a tag to satisfy a changed HEAD.
Distinguish upload acceptance, package validation/indexing, actual installability,
workflow failure, and a transient GitHub API polling failure. Retry a read-only
poll with bounded backoff; a polling timeout must not cause an upload or retag.
If a package already exists, verify its expected provenance before skipping it.
Retain the operator's existing control over release execution and provisioning.

## Fleet selection and environment ownership

Read destinations from the executing host's RAIkeep.json5 Observers using the
existing Engenho resolver. Keep Windows and WSL installations separate. Preserve
host-key verification, account selection, and the selected project/kernel Python.

Provide independent typed choices for runtime tools and development lint tooling
using Engenho's established naming conventions; this handover does not invent new
HTTP endpoints or prescribe unimplemented request field names.

- Production runtime targets: jsonpit/jpit as requested; **no Vikela by default**.
- Developer/CI targets: explicitly requested Vikela CLI and/or checker extras.
- An explicit Python skip means no Python prerequisite probing, installation,
  upgrade, or removal and no Vikela provisioning on that target.
- CLI-only installs may use an isolated tool environment. Editor checks require
  Vikela plus Pylint inside the **project interpreter**. A pipx-installed command
  alone is not proof that VS Code/PyCharm can import the plugin.
- Notebook support requires the extra in the selected kernel interpreter.
- Do not write editor configuration into arbitrary projects without selecting the
  project. Provide reviewed templates from vikela/docs/editors.md.
- Respect externally managed Python environments; do not use
  --break-system-packages. Do not modify cloud daemons or mount points.

## Operator experience

Standalone Vikela exit codes: 0 clean, 1 findings, 2 syntax/configuration,
4 internal/environment failure. Pylint mode retains Pylint's native exit codes.
JSON stdout is a pure array; operational diagnostics go to stderr. Findings include
rule, location, reason, object-oriented suggestion, and documentation URL.

`--fix` and `--qondisa` are equal first-class spellings. Version 4.6.0 has no
approved automatic rewrites: it reports suggestions and leaves files unchanged.
Do not provision or advertise speculative repair behavior. Cell magic never
executes its inspected cell; notebook scanning follows document order, not kernel
execution history. Native PyCharm inspections remain milestone 2; milestone 1 is
an External Tool with file/line navigation.
