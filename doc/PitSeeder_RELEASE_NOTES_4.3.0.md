# PitSeeder 4.3.0 Release Notes

PitSeeder and `pits` 4.3.0 deliver accepted
[CR024 process-flag self-cleanup](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR024_AIA_to_RAIkeep_Ephemeral_Flag_Self_Cleanup.md).

- Finite normal, exceptional, Ctrl+C, and process-exit paths converge on
  deterministic disposal of the exact owned PID-specific flag.
- `--retain-window` remains a documented 4.x compatibility exception and is
  scheduled for removal in the next major release.
- Master leases and crash/TTL maintenance behavior are unchanged.

The unpublished 4.2.11 preparation is superseded. Package and CLI versions align
on 4.3.0. Publication remains behind RAI's manual release gate.
