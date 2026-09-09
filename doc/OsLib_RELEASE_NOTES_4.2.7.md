# OsLibCore 4.2.7 Release Notes

Implements the OsLibCore portion of accepted
[CR020](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR020_RAI_to_RAIkeep_Iorg_Read_Only_Wildcard_Listing.md).

- Adds typed `IorgListRequest` and `IorgMoveRequest` forms, deterministic argument builders, and sync/async `IorgCommand` execution.
- Aligns `IorgCleanRequest` with exact-ItemId cleanup and explicit subscriber-wide cache cleanup.
- Adds `PathConventionType.Flat` after all existing values, preserving numeric compatibility.
- Adds `RaiPath.EnumerateFiles(searchPattern, recursive)` so consumers can request recursive traversal without referencing the underlying platform traversal enum.
- Verifies argument-token fidelity, option forwarding, validation, and async process execution.

Tagging and NuGet publication remain behind RAI's manual release gate.
