> Superseded by [ratified CR049](CR049_AIA_and_jsonpit_to_RAIkeep_Live-ID-Validation_and_Zip-Image-Import.md), including Rainer's subsequent implementation clarifications. Retained as proposal history; not the active specification.

# Draft CR — Live ID Validation and ZIP Image Import Receipts

| Metadata | Proposal |
| :--- | :--- |
| Document ID | Unassigned; draft for review |
| Date | 2026-10-01 |
| Status | Proposed; not ratified or implemented |
| Providers | RAIkeep and jsonpit-python |
| RAIkeep components | JsonPit, PitSeeder (`pits`), ImgSeeder (`iorg`), supporting RaiImage/OsLib APIs and typed command wrappers as needed |
| Python components | jsonpit library and `jpit` CLI in jsonpit-python |
| Target release | To be assigned after ratification |

## 1. Problem and intended outcome

Two operator observations motivate this combined request:

1. Live Pit data contains unresolved identifiers such as `{AdminPersonId}`. An unresolved template is a valid non-empty string under current PitSeeder checks and can become an unintended entity.
2. An ImportPhotos activity needs to receive a ZIP archive, copy its images into the configured image tree, record the actual import results, and hand successful imports to a later selection activity. The source link may arrive through a chat with Cize or WhatsApp with Umshadisi.

The combined outcome is an import workflow with concrete identities and a machine-readable result suitable for persistence through either `pits` or `jpit`. These are two deliverables under one CR, with independent acceptance tests.

The screenshots are problem evidence. They do not establish who wrote existing data, authorize cleanup, or define an already-approved CLI or application schema.

## 2. Ownership and architecture

| Component | Responsibility |
| :--- | :--- |
| C# JsonPit | Enforce the live entity ID rule at public ingestion/mutation boundaries; validate batches before changing in-memory state. |
| PitSeeder / `pits` | Preflight the whole input before opening a writable Pit; present actionable diagnostics; accept explicit standard input. |
| Python jsonpit | Enforce the equivalent live ID and batch validation contract. |
| `jpit` in jsonpit-python | Apply the same preflight and diagnostics to `put` and its `seed` alias; support the documented standard-input contract. |
| ImgSeeder / `iorg` | Read ZIP images, resolve destinations using existing naming rules, copy them, and emit an import receipt. |
| RaiImage / OsLib | Retain existing naming and cloud-safe storage boundaries; expose necessary typed operations and wrapper options. |
| ImportPhotos activity / application | Resolve incoming messages and provider-specific links, supply import/activity IDs and destinations, persist receipts, and start the selection activity. |

The ID rule belongs in JsonPit as well as PitSeeder: a CLI-only check would leave direct library callers able to introduce the same records. Validation belongs at live write boundaries, not general deserialization or the `PitItem.Id` setter, so existing history remains accessible.

`iorg` returns data and does not invoke a Pit writer or start business activities itself. The caller chooses the destination Pit and which engine writes the receipt.

## 3. Deliverable A — prohibit template markers in live entity IDs

### 3.1 Exact rule

A live incoming entity ID must satisfy existing non-empty string requirements and must not contain either literal character `{` or `<` anywhere in the decoded string.

- Reject `{AdminPersonId}`, `<AdminPersonId>`, `Person{Suffix}`, and `Person<Pending`.
- Apply the rule after JSON/JSON5 decoding, including escaped forms of those characters.
- Do not silently substitute, strip, trim into a different identity, or generate a replacement ID.
- Do not add a general ASCII-only or alphanumeric-only restriction.
- Continue accepting these characters in ordinary fields such as `Name`, `EMail`, and `Note`. The rule concerns the entity's own `Id`, not every nested property named `Id`.
- This CR does not add a separate restriction on `}` or `>` alone.

The rule applies to new entities and live content updates, with or without `--require-existing` / `--patch`. Existence checking is an additional condition, not an alternative to ID validation.

### 3.2 Preflight and diagnostics

Both engines must validate all entities in a submitted batch before applying any of them. A bad entity after a valid entity must leave the complete batch unapplied. CLI rejection must occur before opening the destination for write, creating target directories/process flags, or acquiring a master lease.

This is an input-validation guarantee, not a new distributed transaction or rollback guarantee for subsequent storage failures. For multi-Pit bulk commands, the guarantee is per input batch/destination; this CR does not introduce cross-Pit transactions.

Proposed common diagnostic, written to stderr with exit code `1`:

```text
error: Entity Id '{AdminPersonId}' contains a prohibited template marker ('{' or '<'). Resolve template placeholders before writing to a Pit.
```

Source name and one-based entity position may be appended. Library callers receive an argument/validation exception before mutation. Existing validation of reserved lifecycle fields remains in force.

### 3.3 Existing data and recovery

Loading, listing, exporting, canonical persistence of existing state, change-file replay, and explicit historical replay continue to preserve existing records and identifiers verbatim. They must not make an otherwise readable Pit fail merely because it contains a legacy placeholder ID.

Explicit deletion/tombstoning of an existing malformed ID remains possible through a bounded engine-owned cleanup path. It must not become a general bypass for live creation or updates. Reintroducing such a record as a new live entity remains prohibited. No automatic deletion, rename, or migration is included.

## 4. Deliverable B — ZIP image imports and JSON receipts

### 4.1 Proposed CLI surface

Extend the existing `organize` verb:

```text
iorg organize --source <directory-or-local.zip> [existing destination/naming options]
iorg organize --source <directory-or-local.zip> --import-id <Id> [--activity-id <Id>] --json [existing options]
iorg organize --source-url <direct-https-zip-url> --import-id <Id> [--activity-id <Id>] --json [existing options]
```

`--source` and `--source-url` are mutually exclusive. JSON receipt mode requires an explicit concrete import ID; no example template ID is inserted automatically. Activity ID is an optional correlation value. Validate both supplied identities before importing.

The proposal includes direct HTTPS ZIP downloads. Provider share pages, interactive login, chat/WhatsApp access, and credential acquisition remain responsibilities of the calling activity, which can download a local ZIP instead. Receipts and diagnostics must not expose credentials or signed URL query strings.

Retain existing `--root` / `--app`, tenant, naming, and path conventions. ZIP mode enumerates supported images in nested archive folders; directory mode retains its existing enumeration behavior. Existing filename-to-ItemId/image-number rules remain authoritative. Preserve each archive entry's original relative name in the report.

### 4.2 Planning, copies, and failures

Before destination mutation, enumerate candidates, validate IDs and archive structure, and calculate all final destinations. Check the candidate identity before any filename normalization could erase a prohibited marker, and check the final derived ItemId as well.

For ZIP input:

- Reject traversal, absolute paths, and link entries that could escape the bounded input workspace or destination tree.
- Set finite, documented limits on download bytes/time, entry count, and expanded bytes; enforce them while reading. Exact defaults are to be settled in implementation review.
- Record unsupported files, directories, and ZIP metadata as skipped entries; do not recursively unpack nested archives.
- Reject conflicting entries that normalize to the same destination before copying.
- Preserve existing destination files: identical content may be reported as `Unchanged`; different content is a collision error. No implicit overwrite is added by this CR.
- Use existing RaiImage naming and RaiFile storage boundaries. Any temporary download/extraction workspace remains outside the cloud tree; copy bytes to final paths and never move temporary filesystem objects into a CloudDrive.

Preflight errors produce no destination image writes. A runtime I/O failure can leave already copied images: report them truthfully and return failure. Do not claim batch atomicity for image copies or delete successful copies as an implicit rollback. A retry of an identical archive must reuse identical destinations and report them as `Unchanged`, avoiding duplicate images.

Successful local writes do not certify remote synchronization or HTTP availability on an image server.

### 4.3 Receipt contract

With `--json`, stdout contains exactly one JSON entity object and no banner, progress text, ANSI sequences, or prose. Human diagnostics go to stderr. Use the same receipt format for directory and ZIP imports.

Proposed successful receipt:

```json
{
  "Id": "ImportPhotos-20261001-001",
  "Class": "ImageImport",
  "ReceiptVersion": 1,
  "ActivityId": "ImportPhotos-7017-001",
  "Status": "Completed",
  "Tenant": "Nomsa",
  "Source": { "Kind": "Zip", "Name": "concert-photos.zip" },
  "Summary": { "Copied": 1, "Unchanged": 0, "Skipped": 0, "Failed": 0 },
  "Files": [
    {
      "SourceEntry": "concert/nomsa-concert-11.jpg",
      "ItemId": "NomsaConcert",
      "ImageNumber": 11,
      "RelativePath": "NomsaCon/NomsaConce/NomsaConcert_11.jpg",
      "Status": "Copied"
    }
  ]
}
```

`Class: ImageImport` and these field names are proposed application contract values, not a new enforced Pit schema. Omit optional values when absent. Relative paths are relative to the resolved tenant image root; no server URL is fabricated from a local path. Do not emit top-level `Modified` or `Deleted`, which remain engine-owned lifecycle fields.

Emit per-file error codes/messages for failures and reasons for skips. Summary counts must agree with the file entries. Once copying begins, include unattempted candidates with an explicit status if processing stops early.

- `Completed`, exit `0`: at least one eligible image is copied or verified unchanged, with no import errors. Explicitly skipped non-images do not make the import fail.
- `Partial`, exit `1`: some images are available but one or more eligible images failed or were left unattempted.
- `Failed`, exit `1`: validation/download failure, no eligible images, or no eligible image successfully available.

When enough invocation context exists, failed operations also emit a receipt. Unparseable arguments or an invalid receipt ID may fail with stderr only. The activity persists partial/failed receipts deliberately and never treats them as a successful import.

## 5. Receipt ingestion through pits and jpit

Add explicit standard-input support:

```text
pits seed <PitName> --source - [existing options]
jpit put <PitName> - [existing options]
jpit seed <PitName> - [existing options]
```

`-` means read stdin to completion before validating or writing. Preserve single-entity, array, and keyed-map support where already contracted; the single receipt object must work in both engines. Empty/malformed stdin fails without writing. For `pits`, stdin is a single-Pit input, not a `--wwwa` directory substitute.

The `jpit` spellings above are proposed parity requirements for jsonpit-python; its source has not been inspected for this draft. Its provider must confirm existing behavior and implement any missing portions.

A direct shell pipe cannot prevent a downstream writer from consuming a partial-result receipt before the producer exits. `pipefail` alone does not make that safe. The activity must buffer the result, inspect the importer exit code and receipt status, then decide what to persist and whether to start selection.

Illustrative success-only shell workflow using proposed options:

```sh
iorg organize --source ./photos.zip \
  --root /srv/images --tenant Nomsa --pathconv 3 --nameconv 3 \
  --import-id ImportPhotos-20261001-001 --json > ./import-result.json &&
  pits seed ImageImports --source - -r /srv/pits < ./import-result.json
```

The equivalent Python consumer is `jpit put ImageImports -` (or `jpit seed ImageImports -`) with its configured root options and the same buffered JSON. Neither engine must implement ZIP extraction to satisfy its part of this CR.

Only after both a completed image import and successful receipt persistence may the application initiate the selection activity. Receipt persistence failure must retain the result for retry rather than repeat the import blindly. There is no distributed transaction across the image tree, the Pit, and the activity engine.

## 6. Acceptance criteria

| ID | Scenario | Required evidence |
| :--- | :--- | :--- |
| A01 | `{Id}`, `<Id>`, embedded markers, and JSON-escaped markers | C# and Python library/CLI rejection before live mutation. |
| A02 | Valid first entity followed by invalid ID | No batch entity applied; CLI creates no writable Pit artifacts. |
| A03 | Valid ID with `{TenantName}` / `<value>` in ordinary fields | Accepted and preserved. |
| A04 | Default upsert and strict patch | Same marker rejection; existing CR047 checks retained. |
| A05 | Existing malformed historical record | Read/list/export/replay/save remain usable; explicit tombstone works; live re-creation fails. |
| B01 | ZIP with nested images and non-image metadata | Correct RaiImage destinations; exact receipt counts and skip reasons. |
| B02 | Traversal, link entry, normalized collision, invalid derived ID, exceeded archive limit | Error before destination mutation; no out-of-bound extraction. |
| B03 | Existing identical/different destination | Identical is unchanged; different content is rejected without overwrite. |
| B04 | Injected copy failure after one success | Nonzero exit, accurate partial receipt, no automatic selection. |
| B05 | Direct HTTPS ZIP succeeds/fails; authenticated share page supplied | Bounded download and actionable failure; no credential leakage or false success. |
| B06 | `--json` including debug settings | Exactly one parseable receipt on stdout; diagnostics on stderr. |
| C01 | Successful receipt fed to `pits` and `jpit` stdin | Same entity data committed; lifecycle metadata supplied by each engine. |
| C02 | Empty/malformed stdin or invalid receipt ID | Nonzero exit and no Pit mutation. |
| C03 | Failed import or failed receipt persistence | Activity does not begin selection; result retained for explicit recovery. |
| C04 | Repeated identical import and cloud-root destination | No duplicate images; CR022 storage invariants retained. |

## 7. Compatibility, exclusions, and delivery

This intentionally tightens live ID acceptance. Document that IDs containing `{` or `<` can no longer be created or updated through ordinary live writes. Other fields and valid IDs retain their semantics.

No entity-type restriction based on the Pit name is introduced: rejecting a person in `Locations` would require a separate schema/application rule. No existing live data is cleaned as part of implementation. Chat integrations, selection logic, and provider-specific share-link authentication are application work; this CR defines their handoff contract.

Delivery order: ratify the contract and assign its CR number; implement shared C# validation and PitSeeder preflight/stdin; implement ImgSeeder ZIP/receipt support and necessary typed wrappers; implement/certify Python jsonpit and jpit parity; run the acceptance matrix; document and release through each project's established process. RAIkeep completion alone is not evidence of Python completion.

Related contracts:

- [CR043 — seed payload shapes and preflight](../CR043_AfricaStage_to_RAIkeep_Improve-pits-seed-array-error-message.md)
- [CR047 — existing-entity patch mode](CR047_jsonpit_and_pits_Require-Existing-Patch-Flag-and-Seed-Commit-Count.md)
- [CR040 — lifecycle fields and live mutation](../CR040_AIA_to_RAIkeep_and_jsonpit_Prohibit-Read-Modify-Write.md)
- [CR022 — cloud-safe storage](../CR022_RAI_to_RAIkeep_Cloud_Safe_In_Place_Filesystem_Invariant.md)
- [Current iorg operation contract](../IORG-OPERATIONS.md)

Draft design choices for ratification: direct HTTPS ZIP input in the first release; explicit import IDs and receipt field names; preserving conflicting existing images; archive resource-limit defaults. No CR number or release version is reserved by this draft.
