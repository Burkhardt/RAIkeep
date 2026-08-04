# Handover outgoing — RAIkeep to AIA — Package line and provider release attestation (v3.13.1)

**Date:** 2026-08-03  
**Provider owner:** RAIkeep (Sol, implementation agent)  
**Recipient:** AIA (Bob/Adele)  
**RAIkeep version:** 3.13.1  
**Status:** Delivered — packages tagged and provider acceptance evidence recorded  
**Responds to:** AIA's `HANDOVER-INCOMING-AIA-TO-RAIKEEP-v3.13.1-PACKAGE-BUMP.md`

---

## 1. Provider release attestation

RAIkeep confirms the official AIA-facing package line:

| Package | Version | Release classification | Provider tag commit |
|---|---:|---|---|
| `OsLibCore` | `3.13.1` | Additive API and implementation changes | `9be7c92` |
| `RaiUtils` | `3.13.1` | Dependency-line alignment; no production API change | `86faaa2` |
| `RaiImage` | `3.13.1` | Dependency-line alignment; no production API change | `12079cd` |
| `JsonPit` | `3.13.1` | Additive API plus process-activity lifecycle refinement | `e59f4a8` |

The coordinated release also includes the `ImgSeeder` and `PitSeeder` tools at `3.13.1`. The RAIkeep umbrella and all six child repositories have matching remote `v3.13.1` tags at their prepared release commits.

## 2. Delivered changes relevant to AIA

### OsLibCore

- Added `TextFile.SaveInPlace()` for small cloud-backed coordination files that must be updated without a preceding delete or rename.
- Added read-only `RaiFile.LastWriteTimeUtc`, allowing consumers such as JsonPit to read physical UTC modification time through the OsLib abstraction.
- Kept existing `TextFile.Save(...)`, backup, path, configuration-loading, and cloud-path behavior intact.
- No physical last-write-time setter was added. Logical timestamps remain the responsibility of the persisted data model.

### RaiUtils

- Aligned the package line with the coordinated `3.13.1` release.
- No production API or runtime behavior changed from `3.13.0`.

### RaiImage

- Aligned fallback dependencies to `OsLibCore 3.13.1` and `RaiUtils 3.13.1`.
- No production API or runtime behavior changed from `3.13.0`.
- Existing image-tree naming, `WordCase`, and PlantUML behavior remains compatible.

### JsonPit

- Process activity files now use `{Machine}-{Subscriber}-{PID}.flag`, so separate operating-system processes no longer share one process-activity filename.
- Added ownership-aware process activity operations, including `ProcessFlagFile.IsOwnedByCurrentProcess`, `ProcessFlagFile.TryReleaseCurrentProcess()`, and `Pit.TryReleaseProcessWindow()`.
- Explicit process-window release expires the owning flag in place and leaves an epoch tombstone. It does not delete/recreate the cloud-backed file.
- `Master.flag` remains a separate stable-participant writer lease. Releasing a process activity window never releases or rewrites the master lease.
- Master and process flag writes now use the OsLib in-place save path; canonical pit modification time is read through `RaiFile.LastWriteTimeUtc`.
- Corrected the historical-replay XML reference to `AddHistorical(PitItem)`.

The per-process activity lifecycle was delivered for finite clients, principally PitSeeder. AIA's long-running host should retain its process window naturally for the lifetime of its shared pit instances rather than call finite-command cleanup after each request.

## 3. CR summary included in v3.13.1

The resolved CLI request changed finite `pits` operations so they:

1. Track every pit opened by the command.
2. Perform the requested seed, export, or query.
3. Verify that each process activity flag still belongs to the current PID.
4. Expire the owning activity flag in place on normal completion and through best-effort exception, Ctrl+C, and process-exit cleanup.
5. Leave `Master.flag` untouched.
6. Retain the earlier timeout-based process window only when `--retain-window` is supplied.

Per-PID flag tombstones can accumulate. This was explicitly accepted as the safer trade-off for cloud synchronization and process-specific diagnostics.

The separate JsonPit persistence-snapshot concurrency CR was not implemented in `3.13.1`. This handover does not claim that overlapping in-process `Add`/`Save` snapshot materialization has been resolved.

## 4. AIA memory-first lifecycle compatibility

RAIkeep confirms that AIA's memory-first pit lifecycle remains the recommended integration pattern:

1. Resolve each configured pit path during application startup.
2. Construct and load one `Pit` instance for each distinct pit path.
3. Register and reuse that instance through the application container/singleton mechanism.
4. Apply accepted mutations to the shared in-memory instance.
5. Invoke the established save/flush operation at the application-defined persistence boundary.
6. On application shutdown, perform any application-required final flush before disposing the host.

Important invariants:

- Do not construct a new `Pit` for every HTTP request or operation.
- Do not use `ProcessFlagFile` as an application-level mutex.
- Do not clear `Master.flag` after a flush. Its timed lease protects propagation of the canonical write.
- A participant without the active master lease follows JsonPit's existing change-file path instead of directly replacing the canonical pit.
- Reopening a pit after persistence remains the appropriate integration check that the saved state can be loaded.

No AIA startup-load, in-memory mutation, or explicit flush contract was removed or renamed by this release.

## 5. Breaking-change and migration assessment

### Source and binary compatibility

For normal AIA package consumption, `3.13.1` is classified as non-breaking:

- OsLibCore additions are additive.
- RaiUtils and RaiImage contain no production API changes in this release.
- JsonPit adds process-window APIs and refines flag lifecycle behavior without removing the existing pit load/save surface.
- No configuration-loading or environment-variable contract changed.

### Operational compatibility note

The process activity filename is intentionally different: it now includes the PID. Any operational script that enumerates or deletes exact legacy `{Machine}-{Subscriber}.flag` process filenames must be updated to recognize `{Machine}-{Subscriber}-{PID}.flag` and expired epoch tombstones.

This does not change the name or stable-participant semantics of `Master.flag`.

### Migration required by AIA

No source migration is required for AIA's existing memory-first startup/load/flush code. AIA should regenerate or change no public client contract solely because of this RAIkeep package bump.

If AIA has diagnostics that assume one process activity filename per subscriber, update those diagnostics as described above. AIA should not adopt PitSeeder's `--retain-window`; that switch belongs to the finite CLI surface, not the long-running API host.

No new deprecations were introduced in the four AIA-facing packages by `3.13.1`.

## 6. Provider verification evidence

RAIkeep's coordinated release validation recorded:

- Umbrella `RAIkeep.slnx` build: succeeded with `0` warnings and `0` errors.
- OsLib tests: `66` passed, `0` failed.
- RaiUtils tests: `21` passed, `0` failed.
- RaiImage tests: `94` passed, `0` failed.
- JsonPit release scope: `103` passed, `0` failed, excluding the test owned by the separate open concurrency CR and the external remote-sync scenario.
- The external OneDrive remote-sync scenario passed on its immediate isolated rerun.
- PitSeeder tests: `7` passed, `0` failed.
- Two immediate consecutive read-only WWWA exports against the configured OneDrive `AIA` pit succeeded and left distinct expired PID-specific process tombstones.

AIA supplied additional consumer evidence after adopting `3.13.1`:

- `dotnet test AIA.slnx --configuration Release`: `176/176` passed.
- `pnpm --dir aia-workbench build`: passed.
- Live `/health`, `/openapi/v1.json`, and `/scalar/v1` checks returned HTTP `200`.
- Unauthenticated `POST /api/v1/Maintenance/flush` returned the expected HTTP `401`.

Together, the provider and consumer evidence is sufficient for the `3.13.1` package-bump acceptance baseline.

## 7. Response to AIA open decisions

### Additional AIA-side checks

No additional check blocks acceptance of `3.13.1`. For durable regression coverage, RAIkeep recommends that AIA retain or add one focused lifecycle integration test that:

1. Starts with the same singleton pit registration used by production.
2. Loads persisted state at startup.
3. Applies an in-memory mutation.
4. Invokes the authorized flush boundary.
5. Reopens the pit from disk and verifies the accepted mutation.

This should test AIA's real container and persistence boundary without creating one pit per request or substituting temporary configuration for the machine configuration contract.

### Deprecations and migration notes

There are no new `3.13.1` deprecations for AIA to propagate. The only operational migration note is the per-PID process activity filename described in §5.

### Canonical provider handover

The canonical RAIkeep response is:

`doc/HANDOVER-OUTGOING-RAIKEEP-TO-AIA-v3.13.1-PACKAGE-BUMP.md`

AIA may link directly to this file from its incoming handover and subsequent consumer handovers.

## 8. Authoritative supporting documents

- [`OsLib_RELEASE_NOTES_3.13.1.md`](OsLib_RELEASE_NOTES_3.13.1.md)
- [`RaiUtils_RELEASE_NOTES_3.13.1.md`](RaiUtils_RELEASE_NOTES_3.13.1.md)
- [`RaiImage_RELEASE_NOTES_3.13.1.md`](RaiImage_RELEASE_NOTES_3.13.1.md)
- [`JsonPit_RELEASE_NOTES_3.13.1.md`](JsonPit_RELEASE_NOTES_3.13.1.md)
- [`PitSeeder_RELEASE_NOTES_3.13.1.md`](PitSeeder_RELEASE_NOTES_3.13.1.md)
- [`PitSeeder_CR_release_for_cli-resolved-in-v3.13.1.md`](PitSeeder_CR_release_for_cli-resolved-in-v3.13.1.md)
- [`JsonPit-FlagFiles-And-Concurrency.md`](JsonPit-FlagFiles-And-Concurrency.md)

## 9. Remaining boundary

The annotated JsonPit concurrency CR remains open and separately governed. AIA should not infer from this package attestation that all overlapping in-process persistence scenarios are resolved. Any expansion of that scope requires its own testing and implementation agreement.
