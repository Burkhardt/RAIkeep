# CR051 — Multiple Cloud Accounts and Named Shortcuts

| Field | Ratified Specification |
| --- | --- |
| Requestor | Dr. Rainer Burkhardt (`RAI`, Chief Product & Technology Officer) |
| Drafting agent | RAIkeep Codex Agent |
| Reviewing / submitting agent | Adele (`7010`, Product Manager, AIA Platform) |
| Date | 2026-10-03 |
| Status | **Ratified Platform Mandate** |
| Number | **CR051** (Re-numbered from draft CR050; CR050 assigned in central register) |
| Target release | `Amafu v4.5.3` / `RAIkeep v4.5.3` |
| Components | Amafu; OsLib and PitSeeder compatibility; jsonpit-python / jpit parity verification |

## 1. Observed problem

A macOS user has two provider-managed Google Drive roots:

```text
~/Library/CloudStorage/GoogleDrive-rainer.burkhardt@gmail.com/My Drive/
~/Library/CloudStorage/GoogleDrive-yebo@umshadisi.com/My Drive/
```

Amafu enumerates the candidates but `CloudStorageDetector.AddFirstExisting`
returns immediately after the first existing candidate. Consequently, `detect`,
generated configuration, and `--create-links` expose only one `GoogleDrive`.
The same helper limits OneDrive and Dropbox discovery to one selected root.
`Checked` also stops recording candidates after the first match for a provider.

## 2. Requested outcome

Discover every distinct supported account root and give each a readable,
selectable name. For the reported Google accounts:

```text
GoogleDriveRainer -> ~/Library/CloudStorage/GoogleDrive-rainer.burkhardt@gmail.com/My Drive/GDriveData/
GoogleDriveYebo   -> ~/Library/CloudStorage/GoogleDrive-yebo@umshadisi.com/My Drive/
```

Each account independently prefers its existing `GDriveData` subfolder. The
example assumes Rainer has that subfolder and Yebo does not; discovery must
inspect both and must not create either provider root or data subfolder.

With `--create-links`, create:

```text
~/.CloudStorage/GoogleDriveRainer
~/.CloudStorage/GoogleDriveYebo
```

A link targets the selected root for that account. It never moves cloud data.

## 3. Proposed naming and discovery contract

These policies are proposals for Adele and Rainer to ratify, not final mandates.

1. Distinguish provider family (`GoogleDrive`) from the account's configuration
   key / shortcut name (`GoogleDriveRainer`) and its real root. Use an internal
   account model rather than treating every name as a new provider family.
2. For `GoogleDrive-<email>`, take the nonempty leading segment before the first
   `.` or `@`, and capitalize its initial letter invariantly: `rainer.burkhardt@gmail.com`
   becomes `Rainer`; `yebo@umshadisi.com` becomes `Yebo`. The rest of the account
   identity remains available for diagnostics; the short name is not identity.
3. Use qualified names whenever Google account identity is available, including
   when only one account is mounted. Adding or removing another account must
   not rename an existing account.
4. Check name uniqueness without case sensitivity to accommodate ordinary
   macOS filesystems. If two accounts produce `GoogleDriveRainer`, show both
   identities and require explicit distinct name mappings before writing
   configuration or shortcuts. Do not silently discard one, repoint a link,
   append enumeration-dependent numbers, or choose an account arbitrarily.
5. A mapping must be a single safe path component. Reject separators, traversal
   components, empty names, and names that collide with another account or an
   existing unrelated destination. Final normalization and mapping syntax are
   review decisions listed below.
6. Enumerate and report all candidates in deterministic order. Deduplicate exact
   and wildcard paths that identify the same account root, including supported
   symlink aliases. Report inaccessible candidates as diagnostics rather than
   treating a partial scan as proof that there are no additional accounts.
7. Generic or shared fallback roots with no account identity must not hide
   identified accounts. Retain legacy single-root support; ambiguous additional
   roots require a distinct explicit name unless they resolve to an already
   discovered account.

## 4. Configuration, CLI, and compatibility

Proposed generated configuration uses named account keys and real root paths:

```json5
Cloud: {
  GoogleDriveRainer: "~/Library/CloudStorage/GoogleDrive-rainer.burkhardt@gmail.com/My Drive/GDriveData/",
  GoogleDriveYebo: "~/Library/CloudStorage/GoogleDrive-yebo@umshadisi.com/My Drive/"
}
```

- `DefaultCloudOrder` must contain valid generated keys. Preserve an existing
  user's explicit preference during any approved migration. Deterministic
  discovery order must not be mistaken for the user's preferred account.
- `pits -c GoogleDriveRainer` and `jpit -c GoogleDriveRainer` must select the same
  configured root. Check OsLib/PitSeeder and Python key validation, path
  expansion, cloud classification, scans, and diagnostics for assumptions that
  keys belong to a fixed provider-name enum.
- `detect --json` must expose every account. Preserve the existing `name` and
  `path` meanings; propose additive `provider` and `account` fields for explicit
  family and account identity. Confirm schema compatibility with consumers.
- Plain detection and every dry run remain read-only. `--create-links` remains
  opt-in. Configuration generation keeps real roots, not shortcut paths.
- Existing `Cloud.GoogleDrive` values, existing `DefaultCloudOrder`, and existing
  `~/.CloudStorage/GoogleDrive` links must continue working without automatic
  rewriting. Never repoint the generic link when account enumeration changes.
- For new multi-account configurations, recommend qualified keys only. A legacy
  generic alias may be retained explicitly for its previously selected account;
  it must not cause scans or operations to process one physical pit twice.
- `init` retains its existing refusal to overwrite configuration without
  `--force`; shortcut conflicts are not overridden by that flag. Document a
  reviewable migration procedure for existing configurations.

## 5. OneDrive and other providers

OneDrive is not limited to a single account overall: Microsoft documents one
personal account plus multiple work or school accounts. Its macOS sync client
has an additional restriction for business accounts with the same display name
across organizations. Discovery must reflect actual distinct local roots rather
than assuming one root per provider.

Sources: [Microsoft account guidance](https://support.microsoft.com/en-us/onedrive/how-to-add-an-account-in-microsoft-onedrive),
[Microsoft sync guidance](https://support.microsoft.com/en-us/onedrive/sync-your-computer-s-files-and-folders-with-onedrive).

Propose `OneDrivePersonal` and organization-qualified names such as
`OneDriveContoso` where folder metadata supports them. Do not apply Google's
email splitting rule to an organization label. Ambiguous identities and names
use the same explicit mapping policy. Review supported Dropbox account naming
as part of the same discovery model; retain `ICloudDrive` for its single detected
user root. This CR does not configure or sign into any provider client.

## 6. Acceptance criteria

| ID | Verification |
| --- | --- |
| A01 | Two Google roots are both listed in text and JSON, and both appear in checked-path diagnostics. |
| A02 | The reported emails produce `GoogleDriveRainer` and `GoogleDriveYebo`; each independently chooses its existing data subfolder. |
| A03 | Adding/removing accounts or changing enumeration order leaves established account names and targets stable. |
| A04 | Same-prefix, case-only, and invalid-name collisions are explicit; no ambiguous configuration or link writes occur. |
| A05 | Duplicate candidate paths and supported symlink aliases do not produce duplicate accounts. |
| A06 | Two distinct OneDrive roots are represented independently, with tested personal/organization naming. |
| B01 | `--create-links` creates both named links; repeat invocation preserves matching links and original data. |
| B02 | Existing generic links and configuration remain unchanged; conflicts preserve all existing paths, including under `--force`. |
| B03 | Plain detection and dry runs create no directories, configuration, or links. |
| B04 | Generated configuration and `DefaultCloudOrder` refer to valid account keys; explicit user defaults are preserved in migration. |
| C01 | Both `pits` and `jpit` select each named root independently using the same configuration. |
| C02 | Provider classification still recognizes Google/OneDrive semantics with qualified keys, and duplicate aliases do not duplicate pit operations. |
| C03 | Existing single-account configuration, fallback roots, and JSON consumers retain documented compatibility. |
| C04 | Fixture-home tests cover missing/inaccessible roots and never touch the operator's actual configuration or cloud data. |

## 7. Review decisions before implementation

Adele should ratify or revise:

- Account-qualified names even with one known Google account, while preserving
  legacy generic keys and links without implicit reassignment.
- Collision handling by explicit mapping, the exact mapping input syntax, and
  where stable mappings live without mutable OsLib global configuration.
- Name normalization for punctuation, Unicode, and organization names.
- Default-account selection for a newly generated multi-account configuration.
- Additive JSON account metadata and its compatibility requirements.
- Final scope for OneDrive and Dropbox in the first implementation.

After formal submission, implement and verify in Amafu first, coordinate Python
consumer parity with Adele, and choose the next shared release version. This
file is a draft only and does not expand the 4.5.2 feature set.

## 8. Rainer's implementation clarifications (2026-10-03)

These subsequent instructions supersede conflicting draft language above:

- Amafu takes the lead: generated `RAIkeep.json5` must be consumable by Os.Config.
  OsLib reads all configured string roots, independent of provider-label names,
  and recognizes shortcut paths as cloud-backed storage.
- Dropbox and iCloud discovery retain their existing logic in this delivery.
- One personal OneDrive root is selected under the compatible `OneDrive` key;
  all discovered corporate accounts retain their own qualified keys.
- Commands must work without interactive prompts. Explicit personal selection
  from the command line takes precedence; an existing valid configured choice
  is otherwise retained. With no valid prior choice, the longest personal
  folder name wins, then the highest numeric suffix; ordinal path order breaks
  any remaining tie. This is a name-based heuristic, not an age measurement.
- A reconciliation mode previews newly discovered drives and migration to
  `~/.CloudStorage` paths. An explicit apply option creates a backup and updates
  configuration while preserving unrelated settings and existing default order.
- Case-insensitive account-name collisions fail with both roots identified.
  No interactive mapping prompt or automatic numeric account renaming is added.

Implemented command spelling: `amafu reconcile [--apply|--dry-run]` and
`--onedrive-personal <folder-name-or-path>` on detect, init, and reconcile.
Explicit personal selection plus apply may repoint only the OneDrive shortcut
that matches the previously configured root. Other conflicts are preserved.
