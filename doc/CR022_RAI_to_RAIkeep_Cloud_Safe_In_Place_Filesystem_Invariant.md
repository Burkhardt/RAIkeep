# CR022 — Incident Corrective Action: Cloud-Safe In-Place Filesystem Invariant

**Record type:** Incident corrective-action and regression-prevention record

**Requesting product:** RAIkeep

**Requester and acceptance owner:** RAI

**Receiving product:** RAIkeep

**Provider / implementation lead:** Codex (Owner and Lead Custodian, RAIkeep)

**Affected packages:** `OsLibCore`, `RaiImage`, `JsonPit`, `ImgSeeder`,
`PitSeeder` (`pits`), with a repository-wide audit of all seven RAIkeep packages

**Target release:** Coordinated RAIkeep v4.2.9

**Incident date:** 2026-09-09

**Date proposed:** 2026-09-09

**Status:** Accepted, implemented, and verified for v4.2.9; awaiting RAI's
manual release-chain gate

---

## 1. Classification and purpose

CR022 is numbered in the RAIkeep change sequence for traceability, but it is not
a discretionary product enhancement. It records an incident investigation,
corrects defects found by that investigation, and establishes a universal
cloud-storage safety invariant across RAIkeep.

The incident followed this explicitly applied maintenance command against the
live AIA subscriber tree:

```text
pits maintain -c OneDrive -r AIA --wwwa --apply \
  --prune-process-flags --older-than 01:00:00 \
  --repair-legacy-extensions
```

During and after the operation, OneDrive presented directory activity that made
the `Activity`, `Person`, `Object`, and `Place` pit directories appear to vanish
and reappear. OneDrive subsequently raised its mass-deletion protection prompt,
reporting that 1,514 files had recently been deleted or moved out of OneDrive.

RAIkeep has previously suffered defects in which a file or directory was staged
outside a CloudDrive and then moved or swapped into the cloud-backed tree. Such
operations can make an established cloud pathname disappear, replace its sync
identity, or cause the provider to observe delete/recreate transitions. This can
produce remote conflicts, ghost duplicates, mass-deletion alarms, and data loss.

CR022 makes prevention of that pattern an explicit, testable, package-wide
contract rather than a convention limited to JsonPit canonical files.

## 2. Established forensic findings

### 2.1 The four live pit directories were not replaced

The actual live directories retained their original filesystem identities and
July 2026 creation dates:

```text
AIA/Activity
AIA/Person
AIA/Object
AIA/Place
```

Their modification timestamps changed because child artifacts were created and
removed. OneDrive's FileProvider reconciliation records showed the directories
as downloaded, uploaded, not trashed, and without unresolved conflicts.

The investigation therefore found no evidence that CR021 maintenance moved,
deleted, or replaced those four live directory objects.

### 2.2 The applied cleanup produced deliberate file deletions

OneDrive's local safe-deletion ledger identified these pending deletions under
the live `AIA` tree:

- 687 expired `.flag` process artifacts removed by the explicitly authorized
  `--prune-process-flags` operation; and
- 436 extensionless legacy artifacts removed only after their corrected
  `.flag` or `.event` siblings had materialized and validated.

No live `.pit`, `.json`, or `.receipt` file was listed for deletion under the
live `AIA` tree. Additional safe-deletion entries belonged to configured-cloud
test trees such as `AIA.Test` and were not canonical AIA production pits.

The mass-deletion prompt was consequently real and must not be dismissed, but
the large file component was consistent with the explicitly requested cleanup.

### 2.3 An erroneous empty nested WWWA tree was created and removed

The same OneDrive ledger recorded deletion of exactly these five directories:

```text
AIA/Activity/AIA
AIA/Activity/AIA/Activity
AIA/Activity/AIA/Object
AIA/Activity/AIA/Person
AIA/Activity/AIA/Place
```

No deleted child files were recorded beneath that nested tree. It was an empty,
erroneously created WWWA structure, not the live top-level WWWA tree.

The most probable presentation explanation is that OneDrive surfaced the leaf
directory names without their complete paths. This made removal of the nested
empty `Activity`, `Person`, `Object`, and `Place` directories appear to be
removal of the live top-level pits.

### 2.4 The report-only maintenance defect is proven

`Pit.Maintain` attempts to return when its pit directory is absent, but it checks
the lazy `PitDir` property. Accessing that property first calls `mkdir()`:

```csharp
public RaiPath PitDir
{
    get
    {
        pitDir ??= JsonFile.Path.mkdir();
        return pitDir;
    }
}
```

The resulting guard is ineffective:

```csharp
if (!PitDir.Exists()) return result;
```

When report-only `pits maintain --wwwa` is given a wrongly resolved root, its
four-pit loop can therefore create the missing tree even though the command is
described as non-mutating. A root resolved as `AIA/Activity/AIA` produces the
exact empty nested structure recorded by OneDrive.

The exact earlier command line or caller that supplied this wrong root was not
recoverable from available shell history. The command shown in section 1, with
both `-c OneDrive` and `-r AIA`, resolves to the correct configured AIA root and
does not explain the nested path. The defective creation mechanism and its exact
filesystem result are nevertheless established independently of that missing
caller history.

### 2.5 CR021 maintenance did not stage through `Os.TempDir`

The CR021 maintenance implementation performs receipt creation, flag pruning,
and legacy-extension repair beside the affected pit artifacts. It does not use
`Os.TempDir`, `TmpFile`, a staging directory, or a whole-directory move.

Legacy-extension repair creates and validates the corrected sibling before
removing the obsolete extensionless source. This is an intentional same-parent
name repair, not replacement of an established destination pathname.

## 3. Additional violations discovered by the incident audit

Although they did not cause the nested CR021 tree, the package-wide audit found
two production paths that violate the governing invariant and must be corrected
in the same incident release.

### 3.1 ImgSeeder temporary staging

`ImgSeeder.OrganizeWithReport` currently:

1. creates a subscriber staging tree beneath an optional temporary root or
   `Os.TempDir`;
2. copies each source image into that staging tree; and
3. moves the staged file into its final subscriber/ImageTree destination.

When the destination is cloud-backed, this is the expressly prohibited
temporary-to-cloud move pattern.

### 3.2 RaiImage `JpegTran` original-file displacement

`ImageMagick.JpegTran` currently moves the original image into `Os.TempDir`,
runs the transformation into the original pathname, and may delete and move the
temporary original back during rollback.

For a cloud-backed original, its established pathname disappears during normal
execution and may disappear again during rollback. This is prohibited even when
the source and restored content are byte-identical.

### 3.3 Unsafe general replacement primitives in OsLibCore

The audit also found general primitives capable of reproducing the same class of
incident:

- `RaiFile.mv(..., replace: true)` may replace an existing destination object or
  delete the destination before moving the source;
- `RaiFile.cp` removes an existing destination before copying;
- `RaiPath.mv(..., replace: true)` recursively removes an existing destination
  directory before moving another directory into its pathname; and
- `RaiPath.cp(..., replace: true)` recursively removes and recreates an existing
  destination tree.

These operations may retain their established behavior for non-cloud paths where
documented compatibility requires it. They must not remove or replace an
existing cloud-backed destination as an implementation technique.

## 4. Universal RAIkeep cloud-storage invariant

The following rules govern every RAIkeep library, CLI, test utility, and future
package.

### 4.1 Prohibited operations

1. A file or directory created beneath `Os.TempDir`, another temporary root, or
   an external staging tree must never be moved, renamed, or identity-replaced
   into a CloudDrive destination.
2. An existing cloud-backed file must never be deleted, moved away, or replaced
   as an implementation technique for updating its content.
3. An existing cloud-backed directory must never be recursively removed and
   recreated, swapped, or replaced as an implementation technique.
4. A temporary sibling must not replace an existing cloud-backed pathname by
   rename, even when the underlying local filesystem describes that operation as
   atomic. Cloud providers are not required to preserve that local atomicity or
   remote identity.
5. Backups and rollback must not move the established cloud pathname away, even
   briefly.
6. Report-only, inspect, list, audit, validation, and dry-run operations must
   perform zero filesystem mutation. Object construction and lazy property
   access must not weaken this rule.

### 4.2 Required operations

1. A genuinely new cloud file is created at its final cloud pathname through the
   RaiFile boundary.
2. Content updates to an existing cloud file open and write that same pathname
   in place. The pathname remains present for the entire update.
3. If an external tool requires a local working file, it may produce an isolated
   temporary result. After successful validation, only the result's bytes may be
   written through an in-place RaiFile operation to the continuously existing
   cloud destination. The temporary file object itself is never moved or renamed
   into the CloudDrive.
4. A backup of an existing cloud file, when requested, is made by copying bytes;
   the live pathname is not relocated.
5. New parent directories are created individually at their final locations only
   when the mutating operation explicitly requires them.
6. All production filesystem work remains behind `RaiPath`, `RaiFile`, and their
   typed subclasses. CR022 authorizes no new direct `System.IO` usage outside the
   OsLibCore boundary.
7. `Os.Config` is read-only configuration authority for these decisions. CR022
   does not rewrite, replace, extend, or use it as mutable state.

### 4.3 Intentional semantic rename or move

The invariant does not prohibit an explicitly requested user-domain relocation,
such as changing an ItemId and moving its artifacts to their newly derived tree
location, or repairing an extensionless artifact to its correct same-parent
name. In such cases the disappearance of the old pathname and creation of the
new pathname are the requested semantic result.

Such a move must still:

- use the RaiFile/RaiPath boundary;
- never stage through `Os.TempDir`;
- never replace an already existing cloud destination by delete/swap;
- materialize and validate the new destination before removing the old source
  whenever the operation is implemented as copy-then-remove; and
- leave the source intact if destination creation or validation fails.

Whole cloud-directory replacement is not authorized as a semantic move under
CR022.

## 5. Required corrections

### 5.1 JsonPit maintenance purity

`Pit.Maintain` shall inspect the non-creating `JsonFile.Path` before accessing
any lazy path that can call `mkdir()`.

- Report-only maintenance against a missing pit returns a missing/deferred result
  or typed error without creating a directory, flag, receipt, event, or file.
- Applied maintenance also validates its target before creating or opening a
  writable `Pit`.
- Maintenance remains explicit-operation I/O; finalizers remain strictly free of
  recovery publication and filesystem I/O.

If preserving a creating `PitDir` property remains necessary for mutating APIs,
JsonPit shall expose or use a separate non-creating path for inspection. A
read-only caller must not accidentally invoke creation through the writable
property.

### 5.2 `pits maintain` root validation

PitSeeder shall validate the resolved target before constructing any writable or
filesystem-creating `Pit`:

- the resolved root directory must already exist;
- a single-pit target must already contain its expected pit location;
- a WWWA target with none of the four expected pit locations is rejected as a
  wrong root;
- when only some WWWA pits exist, missing pits are reported and skipped without
  creating them; and
- validation failure leaves a before/after filesystem inventory unchanged.

Relative `-r` behavior may remain supported, but a relative path is resolved and
reported completely before validation. No implicit fallback to the current
directory, configured cloud root, or another guessed location is introduced.

### 5.3 OsLibCore fail-fast enforcement

OsLibCore shall enforce the invariant at the lowest reusable boundary:

- `RaiFile.mv` and `RaiPath.mv` fail before mutation when a source beneath
  `Os.TempDir` would be moved into a cloud-backed destination;
- cloud destination replacement never uses delete-then-move, rename replacement,
  directory removal, or whole-tree recreation;
- `RaiFile.cp` overwrites an existing cloud file in place rather than calling
  `rm()` first;
- replacement of an existing cloud directory through `RaiPath.mv` or
  `RaiPath.cp` fails fast;
- cloud backup behavior copies rather than relocates the live pathname; and
- prohibited operations throw a typed OsLibCore domain exception containing the
  attempted operation and relevant source/destination paths, rather than leaking
  a raw `System.IO` exception.

The implementation shall preserve normal intentional deletion through explicit
`rm()`/`rmdir()` calls. CR022 prevents deletion as a hidden implementation detail
of copy, move, save, conversion, backup, rollback, inspection, or replacement;
it does not remove explicit deletion capabilities.

### 5.4 ImgSeeder direct destination write

ImgSeeder shall remove the subscriber staging tree beneath `Os.TempDir`.

Each organized artifact shall be written directly to its final derived
ImageTree/ItemTree pathname through OsLibCore. An existing cloud destination is
updated in place if the operation explicitly permits overwrite; otherwise the
operation fails without modifying either path.

The optional `tempRoot` surface shall be removed if it is not public API, or
deprecated and made behaviorally inert if compatibility requires retaining its
signature. It must not provide an escape hatch around the invariant.

### 5.5 RaiImage transformation and rollback

`ImageMagick.JpegTran` shall leave the original cloud pathname continuously
present.

A compliant flow may:

1. read/copy the source into an isolated working input when required by the
   external tool;
2. render a separate temporary output;
3. validate successful command completion and the output artifact;
4. write the validated output bytes into the existing destination pathname
   through an in-place RaiFile operation; and
5. remove only the isolated temporary artifacts.

Failure before the in-place write leaves the original untouched. Failure during
an in-place write is surfaced as a typed domain I/O failure and must never invoke
a delete-and-move rollback.

ImageMagick, PlantUML, `pits`, `iorg`, and every other wrapped CLI path shall be
screened for independently implemented temporary-to-cloud moves, delete/replace
updates, and directory swaps. Tool execution remains routed through the approved
typed wrapper chain; CR022 does not add direct process execution.

## 6. Required regression coverage

### 6.1 OsLibCore

- Moving a file from `Os.TempDir` to a cloud destination fails before either
  path changes.
- Moving a directory from `Os.TempDir` to a cloud destination fails before
  either tree changes.
- Copying over an existing cloud file never observes the destination pathname as
  absent.
- Replacing an existing cloud directory by move or copy fails without deleting
  any child.
- A requested backup copies bytes and leaves the live cloud pathname present.
- A permitted same-tree semantic rename to a nonexisting destination still works.
- Prohibited operations produce the typed OsLibCore exception with source,
  destination, and operation context.

Tests shall exercise the public RaiPath/RaiFile APIs, not merely inspect source
text or mock the method that owns the invariant.

### 6.2 JsonPit

- `Pit.Maintain` in report-only mode against a nonexistent path leaves the entire
  parent tree byte-for-byte and entry-for-entry unchanged.
- The test observes directory creation as well as file creation, deletion,
  rename, and timestamp changes.
- Applied maintenance against an invalid target fails without creating the pit
  directory.
- Existing CR021 receipt, grace, repair, pruning, finalizer-no-I/O, and
  path-reopenability tests remain green.
- Canonical persistence keeps an existing cloud-backed pit pathname continuously
  present.

### 6.3 PitSeeder

- `pits maintain --wwwa` against the reconstructed wrong root
  `AIA/Activity/AIA` creates none of `Activity`, `Person`, `Object`, or `Place`.
- A WWWA root containing none of the expected pits fails clearly and performs no
  filesystem mutation.
- A partially populated WWWA root reports missing pits without creating them.
- The exact CR021 apply command resolves the configured subscriber root before
  opening any pit.
- Report-only human and JSON modes have identical zero-mutation behavior.

### 6.4 RaiImage and ImgSeeder

- `JpegTran` never moves the original into `Os.TempDir` and keeps an existing
  destination pathname present throughout success and injected failure paths.
- Failed conversion leaves the original content unchanged when failure occurs
  before commit.
- ImgSeeder creates no subscriber staging directory beneath `Os.TempDir`.
- ImgSeeder writes new output at its final derived destination and performs no
  temporary-to-cloud move.
- Overwrite tests prove that an existing cloud destination is not first removed.

### 6.5 Repository-wide and configured-cloud verification

- Audit production sources in all seven packages for `Os.TempDir`, `TmpFile`,
  `RaiFile.mv`, `RaiPath.mv`, delete-before-copy, and delete-before-recreate
  flows whose destination may be cloud-backed.
- Every remaining temporary-file use must document why it cannot be moved or
  identity-replaced into a CloudDrive.
- Run focused local tests and complete Release suites for OsLibCore, RaiImage,
  JsonPit, ImgSeeder, and PitSeeder, followed by all seven package release suites
  and umbrella preflight.
- Exercise the path-presence and report-only guarantees against at least one
  configured real CloudDrive root using isolated test names.
- Configured-cloud cleanup must be bounded and reported so a test cannot silently
  generate a mass-deletion event. A skipped configured-cloud test does not count
  as final acceptance of the cloud contract.

## 7. Documentation and release record

The v4.2.9 preparation shall:

- add the universal cloud-storage invariant to the umbrella and affected package
  contributor/development documentation;
- update affected README and foldable `API.md` files for changed public behavior
  and any new typed exception;
- publish coordinated v4.2.9 release notes for all seven packages and the
  umbrella, explicitly citing CR021 and CR022;
- state that CR022 is an incident corrective release, not a new identity,
  storage, or background-service architecture;
- record the report-only directory-creation defect, the absence of canonical pit
  deletion in the investigated incident, and the additional ImgSeeder/RaiImage
  violations found by audit; and
- provide operators a concise explanation of expected OneDrive mass-deletion
  prompts when an explicitly applied maintenance run retires large numbers of
  obsolete artifacts.

Package versions shall be prepared as coordinated v4.2.9. Tagging, GitHub
release creation, NuGet publication, umbrella labeling, and execution of
`release-chain.sh 4.2.9` remain behind RAI's separate manual release gate.

## 8. Non-goals

CR022 does not:

- weaken CR003/CR021 canonical-save-before-cleanup or receipt-grace rules;
- restore obsolete flags, extensionless artifacts, or test data already selected
  for intentional cleanup;
- add background timers, cron jobs, finalizer I/O, or hidden maintenance;
- change JsonPit process/master identity;
- add CloudDrive identity management;
- modify `Os.Config` or make it mutable;
- prohibit explicit user-authorized deletion;
- prohibit legitimate temporary working output that remains local and is removed
  locally; or
- claim that cloud providers implement local rename/replace atomicity.

## 9. Acceptance criteria

CR022 is complete when:

- report-only `pits maintain`, including `--wwwa`, cannot create any directory or
  file under any target resolution;
- wrong and partially populated maintenance roots are handled without implicit
  directory creation;
- no production RAIkeep path moves a file or directory from `Os.TempDir` into a
  CloudDrive;
- no content update temporarily removes or identity-replaces an existing
  cloud-backed pathname;
- no general RaiPath/RaiFile replacement primitive can recursively replace an
  existing cloud-backed directory;
- ImgSeeder and `JpegTran` comply with the invariant on success, failure, and
  rollback paths;
- intentional same-tree semantic rename and explicit deletion remain available
  under their documented contracts;
- all focused, package Release, configured-cloud, and umbrella preflight tests
  pass;
- documentation and v4.2.9 release records describe the incident and corrected
  contract accurately; and
- no tag, package publication, umbrella label, or release-chain execution occurs
  until RAI grants the separate manual release authorization.

---

*Prepared by the RAIkeep provider from RAI's incident report, OneDrive deletion
ledger evidence, FileProvider metadata, and a repository-wide production source
audit. The governing rule is intentionally stronger than ordinary local
filesystem practice: an established cloud pathname must remain continuously
present, and no temporary or replacement file identity may be moved into it.*
