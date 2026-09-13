# PitSeeder 4.2.11 Release Notes

> **Superseded before publication.** This prepared package line was not released;
> its changes are carried into v4.3.0.

PitSeeder 4.2.11 implements the CLI portion of accepted
[CR024](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR024_AIA_to_RAIkeep_Ephemeral_Flag_Self_Cleanup.md).

- Every default finite `pits` call disposes its tracked pits and removes the
  exact PID-specific process flags it owns after the JsonPit durability boundary.
- Normal completion, exception unwind, Ctrl+C, and process-exit cleanup converge
  on the same ownership-safe release path.
- `--retain-window` remains an explicit v4.2.11 compatibility exception and is
  scheduled for removal in the next major release.
- `Master.flag` remains untouched; crashes and forced termination continue to
  rely on TTL detection and explicit maintenance pruning.

Command-level tests prove normal and exceptional cleanup, twenty sequential
finite invocations with zero residual flags, deliberate retention, and master
lease preservation.
