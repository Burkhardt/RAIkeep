# Proposed CR — Structured iorg inventory and content matching

Status: **Superseded by ratified CR075.**

Authoritative specification: [CR075](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR075_AIA_to_RAIkeep_Iorg_Structured_Inventory_and_Content_Matching.md).
The remaining draft text records the original proposal; delivery follows CR075.
Date: 2026-11-02.
CR number and target release: unassigned. This draft does not authorize release
publication or changes in AIA or Engenho.
Owners proposed: RAIkeep (`OsLib`, `RaiImage`, `ImgSeeder`); consumer adoption by
the AIA and Engenho teams.

## 1. Problem and intended behavior

`iorg list` already discovers recognized media and diagram files recursively.
Its ordinary JSON output is a filename array, and `--quiet` returns full paths.
Neither supplies file size, modification time or a content fingerprint.
Engenho's `ListVideos` consequently performs another metadata pass using
`Deno.stat`. AIA's `VideoBakeController.Bake` separately compares an existing
master's size with a remotely listed source's size. Equal lengths do not establish
equal file contents, and filesystem paths cannot be compared across machines as
if they named the same local file.

Provide two read-only capabilities:

1. **Inventory:** structured metadata for matching files in a configured
   CloudDrive, an ImageTree, or a subtree, directly usable with `jq`.
2. **Content discovery:** find other copies independently of filename using an
   explicit `--match bytes|visual` option. Return an array for one literal source
   file and a dictionary for a wildcard selector, including a wildcard that
   happens to match only one file.

The public vocabulary must distinguish **byte-identical** from **visually
equivalent under a specified comparison profile**. A visual match is not proof
of file identity and must never silently authorize replacing a canonical master.

## 2. Scope resolution and compatibility

Reuse the existing explicit root forms:

- `--cloud <configured-name> --root <cloud-relative-directory>` selects a
  directory under the cloud root from `Os.Config` on the execution machine.
  An explicit `--cloud ... --root .` selects that configured cloud root.
- `--cloud <configured-name> --app <app> --tenant <subscriber>` selects the
  existing `{cloudRoot}/{app}/Image/{subscriber}` hierarchy.
- `--root <absolute-directory>` selects a local filesystem root, without a
  cloud provider. This remains useful for offline callers and ordinary unit tests.
- A narrower `--root` selects a subtree. Inventory and duplicate search recurse
  within the selected root and never scan other configured drives implicitly.

Use `RaiPath` and `RaiFile` for path resolution, metadata and reads. Preserve
root provenance, use real configured cloud roots for live cloud integration
tests, and do not replace `Os.Config` for test isolation. Remote requests must
resolve paths on their execution host, through the typed `IorgCommand` SSH path.

Preserve current `list --json`, plain listing and `--quiet` contracts. Add
`--long` for structured metadata with `--json`; long human output follows the
shared CLI style. Do not repurpose the existing `-l` alias for `--nologo`.
Add `--ignore-case` for filename-pattern matching without changing today's
default case behavior. Extension classification is case-insensitive, including
`.MOV`; examples explicitly opt into case-insensitive pattern matching.

Keep the existing recognized-artifact filter by default. An explicit
`list --all-files --long --json` inventories every regular file, including
unrecognized extensions, using metadata only. Duplicate discovery initially
operates on supported image/video containers; it does not hash pits, event logs
or arbitrary application data. Additional artifact matching is a separate scope
decision.

## 3. A — Structured inventory

### Proposed commands

```zsh
iorg list '*.mov' --cloud ICloudDrive --root . --ignore-case --long --json \
  | jq '.[] | {RelativePath, SizeBytes, LastModifiedUtc}'

iorg list '*' --cloud OneDrive --app AfricaStage --tenant Nomsa --long --json \
  | jq 'sort_by(.SizeBytes) | reverse'

iorg list '*' --cloud OneDrive --app AfricaStage --tenant Nomsa \
  --all-files --long --json | jq '.[] | select(.MediaKind == null)'
```

Each array entry has the proposed schema below. Values are illustrative.

```json
[
  {
    "Name": "IMG_5443.MOV",
    "FullPath": "/home/rsb/ServerData/ICloudDriveData/PLVanguard/IMG_5443.MOV",
    "RelativePath": "PLVanguard/IMG_5443.MOV",
    "CloudRelativePath": "PLVanguard/IMG_5443.MOV",
    "ItemTreePath": null,
    "Extension": ".mov",
    "MediaKind": "Video",
    "SizeBytes": 47241468,
    "LastModifiedUtc": "2026-10-31T03:12:41.0000000Z",
    "Cloud": "ICloudDrive",
    "ResolvedRoot": "/home/rsb/ServerData/ICloudDriveData/",
    "ExecutionHost": "ingwe",
    "Sha256": null
  }
]
```

- `RelativePath` is relative to the selected search root. `CloudRelativePath`
  is relative to the configured cloud root, or null for an explicit local root.
- Emit `ItemTreePath` only when a managed ImageTree context establishes it;
  do not invent tenant/tree identities for loose media files.
- Preserve actual filename spelling and Unicode; normalize JSON relative path
  separators to `/`. `SizeBytes` is an integer byte count; timestamps are UTC.
  A missing timestamp is null, never the current time invented as a substitute.
- Default inventory reads metadata only. An optional `--checksum sha256` reads
  each selected file and populates `Sha256`; this requires `--long --json` and
  uses the same streaming primitive as byte matching. Without it, `Sha256` is null.
  Inventory fingerprints do not by themselves declare two files byte-identical.
  Reject `--checksum` combined with `--all-files` in this delivery: that mode is
  a metadata-only census of otherwise unrecognized application files.
- No banner, progress, ANSI escapes or human summary on JSON stdout. Diagnostics
  and summaries go to stderr. Document deterministic sorting by relative path.

## 4. B — Duplicate discovery and identity comparison

### Proposed command

```text
iorg duplicates <FileOrPattern> <existing root options>
  [--match bytes|visual] [--ignore-case] [--json]
  [--visual-profile strict-v1] [--jobs <positive-integer>]
```

`--match bytes` is the default. `--visual-profile` applies only to visual mode.
No automatic move, delete, deduplicate, hard-link or replacement operation is
part of this command.

### One source file: return an array

```zsh
iorg duplicates 'PLVanguard/IMG_5443.MOV' --cloud ICloudDrive --root . \
  --match bytes --json | jq '.[].File.FullPath'
```

A literal selector resolves exactly one source file within the search root.
A bare filename is allowed only when discovery resolves it uniquely; if the
same name occurs in several directories, require a root-relative path rather
than silently choosing one. Absolute sources must also be inside the selected
root in this first delivery. Reject traversal and out-of-root targets.

Search the whole selected root for matching content, irrespective of other
files' names or extensions. Exclude the source itself. Return `[]` when there
are no matches. Each match records the other file and comparison evidence:

```json
[
  {
    "File": {
      "Name": "RenamedClip.mp4",
      "RelativePath": "Archive/RenamedClip.mp4",
      "FullPath": "/resolved/root/Archive/RenamedClip.mp4",
      "SizeBytes": 47241468
    },
    "MatchMode": "Bytes",
    "Evidence": {
      "Algorithm": "SHA-256",
      "Digest": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "ByteComparisonVerified": true
    }
  }
]
```

`File` uses the inventory record schema from section 3; the shortened example
shows only a subset. The digest is an illustrative placeholder, not a real hash.

### Wildcard source selection: return a dictionary

```zsh
iorg duplicates '*' --cloud OneDrive --app AfricaStage --tenant Nomsa \
  --match bytes --json | jq 'with_entries(select(.value | length > 0))'

iorg duplicates '*.mov' --cloud ICloudDrive --root . --ignore-case \
  --match visual --visual-profile strict-v1 --json \
  | jq 'to_entries[] | {Source: .key, Matches: .value}'
```

The wildcard selects **source files**, not the eligible comparison targets.
Thus `*.mov` can find copies named `.mp4`, and `*` examines the whole eligible
ImageTree/subtree. Keys are root-relative paths, never basenames; values are the
same arrays of match records used by the literal-file form:

```json
{
  "Originals/clip.mov": [],
  "Archive/renamed.mp4": [],
  "Photos/unique.jpg": []
}
```

This example shows the schema for three unmatched sources. Include empty arrays
so a successfully examined unique file is distinguishable from an omitted file.
No selected sources returns `{}`. A wildcard never changes to an array merely
because it selected one source. Sort keys and match arrays deterministically.

Matches are evaluated against each source independently. Visual similarity need
not be transitive: A matching B and B matching C must not imply A matches C.
Reuse pair results and content fingerprints internally rather than reading and
comparing every pair repeatedly. Do not merge distinct same-named files or paths
which differ by spaces, case or Unicode on a filesystem that distinguishes them.

## 5. Byte comparison pipeline

1. Enumerate eligible files and collect typed metadata once; reject different
   byte lengths before reading file contents.
2. Stream eligible size groups through SHA-256 in bounded buffers. Cache only
   metadata and digests in process memory, not entire videos. Hash a requested
   literal source once. A uniquely sized file needs no content read for duplicate
   discovery, although explicit inventory `--checksum` still hashes it.
3. Equal size plus equal SHA-256 identifies a candidate pair. Confirm candidate
   equality by streaming byte comparison before reporting `MatchMode: Bytes`
   with `ByteComparisonVerified: true`. This avoids claiming mathematical proof
   from a digest alone. Different filenames and extensions have no bearing on it.
4. Reuse fingerprints within the operation. Do not write sidecar checksums,
   caches, extracted media or reports into cloud folders. JSON goes to stdout.

The implementation can use `RaiFile.OpenRead()` and .NET streaming hashing;
FFmpeg is not required for byte mode. The current import code already streams
SHA-256, so share an appropriate primitive rather than loading whole files into
byte arrays or introducing raw `System.IO` operations in consumers.

## 6. Visual comparison pipeline — explicit alternative

Visual mode is requested explicitly with `--match visual`. It detects equivalent
rendered images or video sequences even where container metadata or encoding
changes make the source bytes different. It reports a visual match, never a
byte-identity assertion.

Propose a versioned `strict-v1` profile with these reviewable boundaries:

- Images: apply authored orientation, preserve alpha, normalize color under a
  declared color-management policy, then compare complete decoded pixels.
- Video: apply display orientation and pixel aspect ratio, check dimensions,
  presentation timing, duration and frame coverage, and compare the complete
  corresponding visual sequences. Never conclude equivalence from a poster or
  a handful of sampled frames. Do not silently trim, crop, time-stretch or discard
  frames to obtain a match. Multiple visual streams must be handled explicitly;
  unsupported arrangements produce a diagnostic rather than an invented match.
- First check equality of normalized decoded fingerprints; this covers differing
  containers/metadata with equivalent decoded visuals. FFmpeg's hash/streamhash
  capabilities can support this stage after a defined normalization policy.
- To cover lossy re-encodes, use perceptual fingerprints only to shortlist
  candidates, then a complete visual comparison with a documented metric such
  as SSIM. A fingerprint match or an averaged score alone is not sufficient.
  Record both aggregate and worst-frame results where applicable. The profile's
  numeric thresholds and candidate filters require calibration and ratification
  on the acceptance corpus before implementation is declared complete. No
  universal claim of human-perceived equality follows from a threshold.
- Different resolutions, crops, HDR-to-SDR tone maps and edited clips are outside
  the proposed strict profile. Broader similarity can be a later named profile.
  Retain HDR/color metadata needed to refuse an unsupported normalization.
- **Audio is ignored by visual mode**, and every result states
  `AudioCompared: false`. Two videos may look alike and have different sound.
  Audio/whole-program equivalence would require a separately specified option.
- SVGs must not be rendered with unrestricted external resource access. Unsupported
  or unsafe media is reported as unexamined, not treated as unique.

Use existing typed ImageMagick support for still images and a typed FFmpeg/
FFprobe wrapper where required; do not add ad-hoc shell strings. Missing tools
are explicit failures for the affected visual capability. Byte mode continues
to work without media decoders.

Visual evidence extends each match record with `Profile`, `Method`
(`DecodedExact` or `Perceptual`), metric-specific scores and thresholds,
normalization settings, decoder versions, frames compared and `AudioCompared`.
Scores are metric results, not probabilities or a claim of 100% confidence.
Record `ByteComparisonVerified: false` unless a separate byte check succeeded.

All decoding and comparison uses bounded memory and pipes; media content is not
persisted to scratch or to the cloud. Memory still grows with the in-memory file
index and, potentially, the result size. Expose bounded worker concurrency
(`--jobs`, default 1), cancellation and execution limits. A resource limit must
report an incomplete operation rather than silently accepting a sampled match.

## 7. Read-only guarantees, errors and execution provenance

- Metadata inspection does not open media contents. Hashing/visual decoding does
  read contents and can trigger provider downloads, network I/O and cache use;
  do not describe it as metadata-only or promise zero physical disk activity.
- Revalidate size and modification metadata before/after content reads. A changed,
  disappearing or unreadable file is reported as unexamined and excluded from
  affirmative match results. These checks are not an atomic distributed snapshot.
- Never traverse directory links out of the selected root. Resolve aliases through
  OsLib; exclude the source's own canonical file and avoid reporting a symlink
  alias as a separate copy. Define physical hard-link handling during implementation.
- Ordinary success, including no matches, returns exit 0. Invalid selection,
  missing source, ambiguous basename, read/decoder failures or incomplete scans
  return nonzero. Do not silently turn an incomplete search into `[]`/`{}` success.
- After scanning has started, partial JSON must remain syntactically valid with
  stderr diagnostics and nonzero exit. Consumers must check exit status and must
  not infer completeness from a valid JSON document alone. Failures before a
  result can be formed may leave stdout empty. Never append human error text to JSON.
- Keep this boundary read-only. No upload, import, renaming or cleanup is implied.
  Revalidate at the consumer's point of action; a completed search is not a lock
  on the filesystem or the cloud replication fabric.

## 8. Ownership and proposed implementation sequence

1. Ratify addressing, option names, schemas, audio semantics and the visual
   acceptance profile. Assign a CR number and release only after this review.
2. Add shared typed inventory models and `IorgListRequest` metadata/checksum
   options in OsLib; add a typed duplicate request with explicit match mode.
   Use filesystem primitives behind OsLib boundaries and media operations in
   RaiImage. Document streaming, errors and cancellation on the public contracts.
3. Implement metadata JSON in ImgSeeder with backwards-compatible output tests.
4. Implement byte matching, grouping, stream verification and deterministic
   single-source/dictionary output. Keep file-name selection separate from identity.
5. Implement and calibrate visual mode, tool availability checks and decoder/profile
   provenance. Validate images, camera MOVs, MP4s and full video sequences.
6. Hand over consumer contracts: Rita can have `ListVideos` consume the new
   structured listing instead of performing `Deno.stat`; AIA can use byte-mode
   evidence for file identity. Local and remote paths must retain host/cloud
   provenance; the API must not assume its local cloud mirror is already current.
7. Update help under `cli-style.md`, API docs, operations examples and release
   validation. Obtain approval before coordinated version preparation. The user
   runs the release chain manually; Engenho handles subsequent provisioning.

The existing RAI002 file-size guidance/code fix remains useful for ordinary local
`RaiFile.Length` access. This CR addresses a different boundary: a structured CLI
inventory and explicit content comparisons, including remote execution.

## 9. Acceptance plan

| Area | Required evidence |
| --- | --- |
| Compatibility | Existing filename-array, plain and quiet listing tests remain unchanged and pass. |
| Metadata | Correct integer bytes, UTC timestamps, host/cloud/root provenance, tree and flat paths; unknown extension appears only with explicit all-files inventory. |
| jq | Direct pipes select sizes, paths and match groups; no banners, ANSI sequences or summaries enter JSON stdout. |
| Selection | Whole tree and subtree; literal source, ambiguous basename, wildcard selecting zero/one/many; quoted patterns, spaces and mixed-case extensions. |
| Byte positives | Renamed images/videos and copies with different recognized extensions match; no dependency on FFmpeg. |
| Byte negatives | Same size/different bytes do not match; different sizes are rejected without content reads; a test-injected digest collision fails final byte comparison. |
| Result shape | Literal returns an array; wildcard always a dictionary keyed by relative path; source excluded, unique sources retained with empty arrays, deterministic order. |
| Visual positives | Same decoded visuals with changed metadata/container; accepted lossy re-encodes meet a ratified profile and report their evidence. |
| Visual negatives | Similar scenes, a changed middle frame, different edits/timing, crop, tone mapping and unsupported color handling cannot pass merely through matching thumbnails or an average score. |
| Audio | Same visuals/different audio can match visually, with AudioCompared false; they do not pass byte identity. |
| Resources | Large synthetic media is processed with bounded buffers/workers; cancellation and limits report incomplete scans honestly. |
| Filesystem | Files changing/disappearing, permission failures, path escape, symlink aliases and same-basename files; no cloud files, sidecars or scratch media are written. |
| Remote | Same contract via IorgCommand over SSH on an authorized Observer; source paths and metadata belong to the execution host. |
| Consumers | Suggested AIA/Engenho adoption tests go to their owning teams; RAIkeep does not edit those implementations as part of this proposal. |

No live corpus scan, package publication or performance claim is authorized by
this draft. Use controlled fixtures for unit tests and separately authorized,
configured CloudDrive subtrees for live integration verification.

## 10. Primary references

- [.NET SHA256.HashDataAsync](https://learn.microsoft.com/en-us/dotnet/api/system.security.cryptography.sha256.hashdataasync?view=net-10.0)
  documents stream-based hashing.
- [FFmpeg hash muxer](https://ffmpeg.org/ffmpeg-formats.html#hash) hashes media
  frames; its default decoded-media behavior is distinct from hashing every
  byte in the original container. This distinction governs the two modes.
- [FFmpeg SSIM implementation](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_ssim.c)
  and [ImageMagick comparison options](https://imagemagick.org/command-line-options/)
  provide technical foundations for evaluating a visual profile, not a universal
  identity guarantee.
- [Current iorg operations](https://github.com/Burkhardt/RAIkeep/blob/main/doc/IORG-OPERATIONS.md)
  define the compatibility baseline.
- [CR020 read-only listing](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR020_RAI_to_RAIkeep_Iorg_Read_Only_Wildcard_Listing.md)
  defines existing filename output and typed CLI boundaries.
