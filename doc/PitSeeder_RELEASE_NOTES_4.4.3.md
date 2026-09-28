# PitSeeder 4.4.3 Release Notes

PitSeeder and `pits` 4.4.3 implement accepted
[`CR043_AfricaStage_to_RAIkeep_Improve-pits-seed-array-error-message.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR043_AfricaStage_to_RAIkeep_Improve-pits-seed-array-error-message.md).

- `pits seed` accepts a single root JSON/JSON5 entity when it contains an exact,
  non-empty string `Id`; `Kind` alone and differently cased `id` fields do not
  satisfy the entity identity contract.
- Existing entity arrays and keyed entity maps remain supported.
- Invalid roots explain all three accepted forms. Non-object array/map entries
  and entities without valid identifiers receive specific diagnostics.
- Parsing, shape checks, entity-identity validation, and protected-attribute
  validation all finish before the destination `Pit` is opened, so rejected
  payloads create no pit directory, process flag, or partial state.

Seed comments, export, audit, deletion, maintenance, event archiving, and clean
process-flag release remain intact. Dependencies align to JsonPit and OsLibCore
4.4.3.
