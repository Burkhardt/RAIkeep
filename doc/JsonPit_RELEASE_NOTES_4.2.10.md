# JsonPit 4.2.10 Release Notes

JsonPit 4.2.10 implements the RAI-authorized recovery-event archive backlog while
preserving CR021 durable cleanup and CR022 cloud-storage invariants.

- `PitMaintenanceOptions.ArchiveEvents` previews or applies compaction of a
  stable snapshot of valid loose recovery events.
- Archive names use the oldest and newest validated event-content timestamps in
  UTC: `Events_yyyyMMdd-HHmm_to_yyyyMMdd-HHmm.zip`.
- Apply creates one immutable archive directly in the existing `Events`
  directory, validates every selected filename and byte payload, and only then
  retires the matching loose files individually.
- Interrupted/partial retirement is restart-safe: identical loose/archive copies
  are recognized on retry. Changed sources, corrupt evidence, and pathname
  collisions are retained and reported.
- `PitAudit.Read(...)` transparently combines loose and archived events and
  deduplicates them by `EventId`; `PitAudit.Inspect(...)` additionally returns
  physical integrity/conflict diagnostics.

Tests cover preview, apply, exact UTC range naming, retry, collisions, corrupt
sources and archives, logical audit continuity, and event-identity conflicts.
