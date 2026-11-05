# CR077 implementation and verification

Targets: RAIkeep **4.6.0**; optional Vikela **4.6.0**, synchronized under the
Twin-Shield Doctrine. This supersedes CR077's original independent launch target.

**Latest preflight: packaging verified; full release gate not green.** The fresh
solution run passed 1,191 tests and failed one OneDrive/Mzansi propagation test.
See the synchronized preflight below and the current evidence receipt. The
successful initial implementation run remains recorded as historical evidence.

Implementation is local. Publication and provisioning belong to Engenho; no
release chain, package publication, fleet installation, or release retag is part
of this implementation run. Vikela was already present as the `vikela/` submodule.

## Programmer-visible before/after

| Operation | Before | After |
|---|---|---|
| C# live indexing, SetProperty, Merge, ExtendWith, DeleteProperty | Supported object API | Preserved; no facade or payload generator required |
| Python live indexing, set_property, extend_with, delete_property | Supported object API | Preserved with matching Id assertions and atomic validation |
| Python live id/modified/deleted property setters | Could bypass immediate notification checks | Reject protected assignments immediately in both tracking modes |
| Python merge(patch) | No matching instance method | Natural instance method delegates to the existing validated patch machinery |
| Python add(same-owner live handle) | Could append its full projection again | Flush pending changes only; no redundant snapshot history |
| Python PitItem(existing_item) submitted to add | Copy could retain a cleared client-metadata marker | Detached copy retains lifecycle provenance and is rejected as a client snapshot write |
| Python extend(JSON array) | Rows applied sequentially, allowing a valid prefix before a later error | Validate all rows, combine explicitly supplied fields, append one sparse mutation |
| Cross-owner AddHistorical | C# could bypass the normal live-owner check | Both languages reject foreign live handles, including in historical replay |
| C# RAI011/RAI012 | Name-based guesses; unordered method-wide sets | Semantic types, chronological symbol states, aliases, collections and bounded source helpers |
| Python framework lint | Absent | Vikela CLI, Pylint checker, IPython cell magic and notebook scanning |

Assignment is acceptance into in-memory history, not immediate filesystem/cloud
persistence. Save/explicit disposal remain durability boundaries. Distinct
assignments remain distinct mutations. Neither a grouped patch nor the linter
creates a distributed transaction.

## Evidence and acceptance boundaries

- All 19 Sipho probes and seven boundary cases have C# semantic fixtures and Python
  counterparts. Supported same-owner live operations are classified according to
  the engine contract rather than the earlier snapshot assumption.
- Additional positive fixtures cover detached/cast/aliased writes, lifecycle
  mutation, statement order, helper-filled collections and lifetime retirement.
- Historical-source scans use git show for 1710524, 8ef1bb3, 2a66ee4 and fbf5d32.
  Each checks the actual collection/create sites and includes a deliberately unsafe
  semantic positive control. Unresolved application dependencies are retained as
  resolution notes: these scans are not full AfricaStage project compilations.
- The cross-language test uses two independent processes on a configured cloud
  root. One Python process renames/deletes while C# retains its stale view, then
  writes only Status. Both tracking modes preserve the rename and tombstone through
  reload and a second Python verification. This is distinct from cross-machine
  provider propagation, which the existing SSH/cloud suites verify.
- The package is tested as an installed wheel in a fresh environment, including
  standalone JSON, Pylint and IPython extension loading.

## Deliberate v4.6.0 limits

- No approved automatic rewrites. --fix and --qondisa are equivalent opt-in flags;
  findings remain suggestions and source stays unchanged. No fields are dropped
  to manufacture a sparse payload.
- Static analysis is bounded and conservative. Unknown types/flows, dynamic
  imports, reflection, arbitrary callbacks and unresolved helpers are not proof
  of a violation or proof of safety. Runtime checks remain authoritative.
- C# helpers are summarized within the inspected syntax tree, up to four calls.
  Python uses resolved imports/annotations and source-local summaries. These are
  not unrestricted interprocedural analyses of arbitrary dependencies.
- Notebook scanning uses document order; the cell magic checks without execution.
- Native PyCharm inspection support remains milestone 2. Milestone 1 provides an
  External Tool setup. Pylint/IPython integrations are exercised programmatically;
  VS Code/PyCharm graphical interaction has not been verified on this machine.
- The local interpreter test run uses Python 3.14. The GitHub CI workflow also
  defines 3.12/3.13 runs; those remote matrix jobs have not yet been executed.

## Release and provisioning handover

Use [Rita's CR077 handover](HANDOVER_TO_RITA_Engenho_CR077_Vikela.md). The new
publish-pypi.yaml workflow uses Trusted Publishing and requires a PyPI policy for
Burkhardt/vikela, workflow publish-pypi.yaml, environment pypi. The workflow has
not been remotely dispatched. PyPI returned 404 for vikela during preparation;
that observation does not reserve its name.

The existing metadata bumper aligned the established suite to 4.6.0 and regenerated
standalone jpit. Vikela now launches in lockstep at 4.6.0 under the Twin-Shield Doctrine.
No logic was added to
release-chain.sh and Vikela is not inserted into its package list. Engenho must
carry the complete coordinated release and keep the umbrella final.

Vikela is optional development tooling. Runtime and development provisioning are
independent selections, and production hosts receive no lint tooling by default.
A global CLI environment does not automatically expose a Pylint plugin in a
project interpreter or an IPython extension in a kernel.

## Initial implementation verification

Verified locally on 2026-11-04:

| Gate | Result |
|---|---|
| Full `dotnet test RAIkeep.slnx --no-restore --nologo` | **1,192 passed; zero failed or skipped** |
| Python jsonpit runtime suite | **131 passed** |
| Vikela suite, including the 26 translated probes | **70 passed** |
| Existing coordinated consistency validator | **141 checks passed** |
| Full solution pack | **11 NuGet packages**, all 4.6.0 |
| Original Python wheel/sdist builds and Twine metadata checks | jsonpit/jpit 4.6.0; initial Vikela candidate (superseded below) |
| Fresh installed wheel checks | Vikela JSON/Pylint/IPython; jpit/jsonpit version commands |
| CLI formatter source synchronization / git diff whitespace | Passed |

The final full solution run includes 234 JsonPit tests, both configured-cloud
cross-language tracking modes, `RemoteSync_MasterClient_FullScenario` (2m19s),
and the remote provider conflict-signal scenario (55s). An earlier full run failed
the remote-sync scenario after 12m38s. Its isolated rerun passed in 9m12s; the final
complete run then passed. Slow provider reads were observed, but the earlier
failure's root cause was not established. No cloud services, mounts, or test gates
were changed to obtain these results.

Historical scans of all four required AfricaStage commits produced no proven
RAI011 findings at the reported collection/create sites; each scan's deliberately
unsafe positive control produced one finding. Application-reference resolution
remained incomplete, so these results do not replace a full AfricaStage compiler
build against the new analyzer. The unresolved-reference notes accompany the
machine-readable evidence.

[Current release evidence and exact child source commits](verification/CR077_Release_Evidence.json)
records the latest 17 local artifacts, their SHA-256 digests, dependency metadata, source
SHAs, test counts, and historical-scan limitations. Initial implementation artifact directories were
`/private/tmp/cr077-nuget-dist`, `/private/tmp/cr077-python-dist`, and
`/private/tmp/cr077-vikela-dist`. Engenho must build and verify its own publication
artifacts from the recorded immutable sources; this receipt does not claim a
remote workflow or publication has run.

The final detailed .NET log is `/private/tmp/cr077-dotnet-complete.log`.
Python and Vikela logs are `/private/tmp/cr077-python-all.log` and
`/private/tmp/cr077-vikela-tests.log`. The release validator log is
`/private/tmp/cr077-release-validation.log`.

For a local help preview before publication:

```sh
/private/tmp/cr077-venv/bin/vikela -h
```

All implementation commits and the umbrella synchronization are local. No push,
tag, workflow dispatch, package publication, or fleet provisioning was performed.


## Twin-Shield synchronized packaging preflight

All 12 child repositories and all distribution identities now target **4.6.0**. The
10 .NET repositories produce **11 NuGet packages**, because RaiGuard CLI and
RaiGuard.Analyzer are separate packages. Python produces **three distributions**:
jsonpit, its existing jpit companion, and Vikela. The inventory therefore contains
**14 distributions / 17 artifact files**, rather than 12 distributions.

Vikela's runtime __version__, banner, README/install examples, editor guidance,
and workflow example now match its 4.6.0 pyproject metadata. A regression check
asserts agreement between package metadata and the runtime version.

The JsonPit sync constellation SVG and rendered 128/192/512 PNGs are preserved.
JsonPit's NuGet icon is the bundled assets/logo-128x128.png. JsonPit.Python and
Vikela sdists include assets; their wheels exclude artwork and remain code-only.
README hero marks use absolute repository URLs for PyPI rendering. Local asset
links in the supplied visual identity specifications were made portable.

Candidate artifacts are in /private/tmp/raikeep-4.6.0-candidates/nuget and
/private/tmp/raikeep-4.6.0-candidates/python. All metadata versions, dependency
versions, console entry points, runtime version constants, source-archive asset
bytes, PNG dimensions, wheel asset exclusion, and the NuGet icon were checked.
Twine accepted all six Python wheel/sdist files. Builds used committed child
sources; current source SHAs and artifact hashes are in the evidence receipt.

The fresh installed-wheel environment reports jpit v4.6.0, jsonpit v4.6.0, and
vikela v4.6.0. JSON diagnostics, Pylint loading, and the non-executing IPython
magic passed. Standalone jpit was regenerated and reports jpit v4.6.0.

Final full solution result: **1,191 passed, one failed, zero skipped**.
RemoteSync_MasterClient_FullScenario passed local pit creation, then timed out
waiting 600 seconds for SyncTest.pit to become visible on Mzansi. It did not reach
the remote mutation phase. Test ID: sync-20261105005621-54453. The separate remote
conflict scenario and both cross-language tracking-mode tests passed. The reason
for the missing OneDrive propagation has not been established; packaging results
must not be substituted for this failed integration gate. Read-only diagnostics confirmed that Mzansi SSH responds, its OneDrive path is
mounted as fuse.rclone, and rclone-odata.service is active/running. Those states
do not prove that new files are propagating. No service/mount changes or automatic
test retries were used to turn the gate green.
The Python runtime suite passed 131 tests; Vikela passed 71 tests. The coordinated
consistency validator passed 141 checks. Detailed logs use the prefix
/private/tmp/raikeep-460-preflight-; the full solution log is
/private/tmp/raikeep-460-preflight-dotnet.log and the installed-wheel log is
/private/tmp/raikeep-460-wheel-smoke.log. No publication or provisioning ran.
