# CR077 implementation and verification

Targets: RAIkeep **4.6.0**; optional Vikela **0.1.0**.

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

## Deliberate v0.1.0 limits

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
standalone jpit. Vikela retains its separate 0.1.0 version. No logic was added to
release-chain.sh and Vikela is not inserted into its package list. Engenho must
carry the complete coordinated release and keep the umbrella final.

Vikela is optional development tooling. Runtime and development provisioning are
independent selections, and production hosts receive no lint tooling by default.
A global CLI environment does not automatically expose a Pylint plugin in a
project interpreter or an IPython extension in a kernel.

## Verification results

Verified locally on 2026-11-04:

| Gate | Result |
|---|---|
| Full `dotnet test RAIkeep.slnx --no-restore --nologo` | **1,192 passed; zero failed or skipped** |
| Python jsonpit runtime suite | **131 passed** |
| Vikela suite, including the 26 translated probes | **70 passed** |
| Existing coordinated consistency validator | **141 checks passed** |
| Full solution pack | **11 NuGet packages**, all 4.6.0 |
| Python wheel/sdist builds and Twine metadata checks | jsonpit/jpit 4.6.0; Vikela 0.1.0 |
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

[Release evidence and exact child source commits](verification/CR077_Release_Evidence.json)
records the 17 local artifacts, their SHA-256 digests, dependency metadata, source
SHAs, test counts, and historical-scan limitations. Local artifact directories are
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
