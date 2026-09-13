# RAIkeep 4.2.11 Release Notes

> **Superseded before publication.** RAI intentionally skipped v4.2.11. These
> prepared changes are delivered in the coordinated v4.3.0 release.

RAIkeep 4.2.11 is the coordinated seven-package delivery of accepted
[CR023 PlantUML relationship rendering](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR023_AIA_to_RAIkeep_PlantUml_Relationship_Rendering.md)
and
[CR024 process-flag self-cleanup](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR024_AIA_to_RAIkeep_Ephemeral_Flag_Self_Cleanup.md).

## RaiDiagram relationship rendering

- Activity Interaction manifests now render their relationships, including
  direction, role labels, and cardinality, rather than requiring an edgeless
  fallback.
- The compiler publishes its accepted element and relationship vocabularies.
- PlantUML `allowmixing` preserves truthful mixed element declarations while
  permitting their relationships to render.
- Unknown constructs remain explicit failures instead of being silently omitted.

## JsonPit and `pits` clean exit

- Graceful `Pit.Dispose()` removes the exact owned PID-specific process flag
  through OsLib's cloud-aware `RaiFile.rm()` boundary.
- Default finite CLI calls leave zero owned process flags after normal or
  exceptional completion; Ctrl+C and process-exit cleanup use the same path.
- `Master.flag`, lease TTL, crash recovery, and explicit maintenance pruning are
  unchanged.
- `--retain-window` remains only as a documented 4.2.11 compatibility exception
  and is scheduled for removal in the next major release.
- Finalizers remain strictly free of filesystem and recovery-publication I/O.

All seven versions and fallback dependency properties align on 4.2.11. Tagging,
GitHub labeling, workflow dispatch, and NuGet publication remain behind RAI's
manual `scripts/release-chain.sh 4.2.11` gate.
