# Pitlint and JsonPit mutation guardrails

Date: 2026-11-04

Status: Pitlint name and overall direction agreed with Rainer. This is an
implementation plan, not a publication record or a replacement for a ratified CR.

## Selected identity

| Surface | Name |
|---|---|
| Project | Pitlint |
| Intended GitHub repository | Burkhardt/pitlint |
| Intended PyPI distribution | pitlint |
| Python import module | pitlint |
| Standalone CLI | pitlint |

Pitlint provides Python guardrails for JsonPit and its surrounding framework.
It is optional development tooling, separate from the jsonpit runtime and jpit
CLI. The name was selected after checking PyPI and GitHub; that check does not
reserve the name. No repository or PyPI project is created by this document.

## Preserve the object model

The existing object-oriented APIs remain primary. Applications do not need
static payload generators, application-specific write wrappers, or a new facade.

- C#: preserve live indexing, SetProperty, Merge, ExtendWith, DeleteProperty,
  DeletePropertyPath, fresh PitItem construction, and Add.
- Python: preserve the corresponding live item indexing and mutation/deletion
  methods, with tests establishing the same observable mutation contract.
- Same-owner live handles, detached snapshots, and new items are distinct states.
  Preserve live object and nested object identities and sparse history.
- Validate whole patch payloads before acceptance, including lifecycle protection.
  A patch is not a distributed transaction; ordinary successive assignments do
  not become one grouped operation.
- Reject cross-owner live writes and unsafe client lifecycle payloads. Keep
  historical replay explicit; do not suggest it as a way around client guards.
- An additional Pit.Patch convenience method is deferred unless a concrete caller
  need justifies it. Existing item methods already perform patch operations.

Read JsonPit/AGENTS.md, MUTATION_TRACKING.md, and GettingStarted.md before changing
the C# mutation implementation or writing its examples. Read the Python mutation
implementation too; do not assume parity from matching method names.

## Analyzer work

Sharpen C# RAI011 and relevant RAI012 coverage against the engine contract.
Introduce Python counterparts through Pitlint, initially focused on these rules.

- Resolve actual receiver types and methods rather than identifiers ending in Pit.
- Track fresh items, same-owner live handles, detached projections, and unknown
  values through aliases, casts, reassignment, scopes, helpers, and collections.
- Respect execution order. A later assignment cannot change the classification
  of an earlier write.
- Distinguish proven violations from unresolved analysis. Do not make unsupported
  runtime claims merely because a value originated at an indexer or Get call.
- Preserve collection operations and supported tracked mutations. Do not introduce
  a blanket prohibition on Remove: a tracked live removal can emit a tombstone.
- Reconcile diagnostics and CR040 guidance with the live-reference contract.
- Share analysis between the C# compiler analyzer and rail. State the limits of
  standalone analysis when a project's references cannot be resolved.

The proposed Python implementation is a Pylint checker with a standalone Pitlint
CLI adapter. Keep framework rule meanings aligned with RAI011/RAI012 while mapping
them to valid Pylint-native diagnostic identifiers and descriptive symbols.
Keep Ruff/mypy configuration; do not duplicate unrelated lint rules.

## Programmer-facing diagnostics

Every finding should carry the rule, severity, file, line/column, a reason,
actionable object-oriented guidance, and a documentation link.

The CLI must support readable terminal output, pure machine-readable JSON, and
documented exit codes distinguishing findings from execution/configuration errors.
The same rule configuration applies in editors and CI. Default checks do not edit
source files. Automatic fixes are a later, explicit opt-in capability restricted
to transformations proven safe; never infer an intended patch by dropping fields.

Follow doc/cli-style.md for terminal help and themed output. Machine output and
redirected plain output retain their established contracts.

## Editor support

- VS Code: use Microsoft's Pylint extension with the checker installed in the
  selected development environment. Verify inline and Problems diagnostics.
- PyCharm: first provide an External Tool setup with navigable file/line findings.
  Native inline diagnostics and quick fixes are a separate tested integration
  milestone, not an assumed property of the external command.
- CLI and CI support are part of the first Pitlint delivery.

Do not add Pylint or editor integration packages as jsonpit runtime dependencies.

## Acceptance evidence

Use AfricaStage's actual before/after methods as fixtures, supplemented by the
19 Sipho probes and the seven additional analysis boundary cases. Source refs:

- 1710524: original before-state with 36 RAI011 findings under analyzer 4.5.13.
- 8ef1bb3: RAI011 conformance changes; do not use the orphaned 889f70f ref.
- 2a66ee4: subsequent RAI002/RAI003 changes.
- fbf5d32: corrected report, including three false positives rather than four.

Keep derived fixtures small and preserve their real control/data flow. Respect
source licensing when copying application code into a public test repository.
Assert diagnostic locations and semantic outcomes, not only warning totals.

Runtime acceptance must cover live identity, sparse fragments, protected fields,
tombstones, detached snapshots, both tracking modes, save/reload, independent
process replication, and C#/Python parity. A passing same-process test does not
establish multi-replica behavior. Run the full solution checks before release.

## Engenho handover

Rita's Engenho runner will own release orchestration and provisioning. Do not
invest in improvements to release-chain.sh for this work.

Once implementation and packaging contracts are concrete, provide Rita a prompt
covering package identities, dependencies, validation commands, publication and
visibility checks, immutable source references, retry/recovery behavior, and the
umbrella's final release step. Record actual verified contracts, not guessed
Engenho endpoints or invented request properties.

Provisioning must keep Python runtime tools and optional Pitlint development
tooling independently selectable. It must respect an explicit Python skip,
environment ownership, supported OS/WSL targets, and exact requested versions.
An isolated global CLI installation does not automatically make the Pylint
checker importable in a project's selected interpreter; document and verify both
installation modes. Do not install development lint tooling on every production
server by default.

The next release number and Pitlint versioning policy will be confirmed during
release preparation. Do not move existing release tags or add Pitlint to the old
shell chain as part of naming or planning.
