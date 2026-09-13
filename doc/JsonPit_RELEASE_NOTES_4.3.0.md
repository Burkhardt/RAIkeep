# JsonPit 4.3.0 Release Notes

JsonPit 4.3.0 carries the accepted
[CR024 process-flag self-cleanup](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR024_AIA_to_RAIkeep_Ephemeral_Flag_Self_Cleanup.md)
implementation from the intentionally unpublished 4.2.11 preparation.

- Explicit `Pit.Dispose()` removes only its exact owned PID-specific flag after
  the established durability work through `RaiFile.rm()`.
- Read-only and writable pits share the same cleanup path.
- `Master.flag`, lease TTL, crash recovery, and maintenance pruning are unchanged.
- Finalizers remain strictly free of filesystem and recovery-publication I/O.

The package participates in the coordinated 4.3.0 dependency line. Publication
remains behind RAI's manual release gate.
