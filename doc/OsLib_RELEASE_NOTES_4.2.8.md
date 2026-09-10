# OsLibCore 4.2.8 Release Notes

OsLibCore 4.2.8 implements its share of accepted
[CR021](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR021_RAI_to_RAIkeep_JsonPit_Durable_Cleanup_Receipts_and_Pits_Coordination.md).

- Explicit non-default `TextFile` extensions now preserve dotted logical stems such as `Nkosikazi-AIA.Api-93455.flag`; implicit complete-filename parsing remains compatible.
- Adds the unambiguous `(Name, Ext)` `TextFile` constructor.
- Adds `PitsMaintainRequest`, deterministic argument construction, and sync/async `Maintain` execution.
- Typed `PitsCommand` calls now share a process-local provider/root/pit gate. Same-target calls queue, unrelated targets may overlap, WWWA takes `Person`, `Object`, `Place`, `Activity` in fixed order, and queued cancellation launches no child.
- No `Os.Config` mutation or new direct consumer filesystem dependency was introduced.

Verified by the full OsLibCore Release suite and focused CR021 argument, transport,
dotted-name, concurrency, and cancellation tests.
