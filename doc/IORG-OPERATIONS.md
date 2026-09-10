# `iorg` operations manual

## Purpose

`iorg` organizes and maintains subscriber-scoped image and diagram artifacts in
the RAIkeep ItemTree. It can copy normalized source images into their convention
paths, discover managed artifacts, relocate or rename a complete ItemId family,
and remove exact families or rendered derivatives.

Iorg does **not** have a JsonPit-style audit/event-log feature. It does not create
an `Events` directory or durable operation log. Its current inspection tools are:

- `iorg list`, which is strictly read-only; and
- `iorg clean <ItemId>` without `--force`, which previews an exact-family
  deletion without deleting anything.

## ItemTree model

Files sharing one exact ItemId belong to one logical family even when their
extensions and suffixes differ. For example:

```text
AfricanB/AfricanBri/
  AfricanBrisket_01.png
  AfricanBrisket_02.webp
  AfricanBrisket.svg
  AfricanBrisket.puml
  AfricanBrisket_config.puml
  AfricanBrisket.raid
  AfricanBrigadine.png
```

`AfricanBrisket` operations include its images and diagram artifacts, but do not
include the bucket-sharing `AfricanBrigadine.png` sibling.

## Command overview

| Command | Purpose | Filesystem effect |
|---|---|---|
| `iorg organize` | Normalize and copy source images into an ItemTree | Writes new destination files; source remains |
| `iorg list` | Discover managed images and diagram artifacts | Strictly read-only |
| `iorg move` | Relocate and optionally rename one exact ItemId family | Moves files; no dry run |
| `iorg clean <ItemId>` | Preview or delete one exact ItemId family | Dry run unless `--force` |
| `iorg clean --cache` | Remove rendered derivatives across one subscriber tree | Deletes immediately; `--force` is neither needed nor accepted |

Use contextual help for the installed version:

```bash
iorg --help
iorg organize --help
iorg list --help
iorg move --help
iorg clean --help
```

There is no `iorg maintain` command. In the 4.x compatibility parser, an
unrecognized bare first token can still be interpreted as the legacy positional
subscriber. Consequently, `iorg maintain -h` displays `Subscriber: maintain`
and resolves a corresponding destination; it does not select a maintenance
operation. Use `iorg --help` for root help and one of the four command names
shown above for contextual help. This positional ambiguity disappears when the
legacy parser is removed in `5.x.x`.

## Root and subscriber resolution

There are two supported ways to identify a subscriber tree.

### Parent root plus explicit subscriber

```bash
iorg list '*' \
  -c OneDrive \
  --root LiveAfricaStageImage \
  --subscriber Nomsa
```

This resolves to:

```text
<configured OneDrive>/LiveAfricaStageImage/Nomsa
```

### Complete subscriber root

```bash
iorg list '*' --root /srv/images/LiveAfricaStageImage/Nomsa
```

When `--subscriber` is omitted, the final `--root` segment is treated as the
subscriber and the supplied path is the complete subscriber destination.

For predictable scripts, specify `-c` explicitly for configured CloudDrive
roots or use an explicit absolute local path. If `-c` is omitted for a relative
root, iorg may select the first configured provider in
`Os.Config.DefaultCloudOrder`.

`-r` and `--root` are equivalent supported spellings. `-r` is not legacy.

## Path conventions

| Number | Name | `AfricanBrisket` example below subscriber root |
|---:|---|---|
| `1` | `CanonicalByName` | `AfricanBrisket/` |
| `2` | `ItemIdTree3x3` | `Afr/Africa/` |
| `3` | `ItemIdTree8x2` | `AfricanB/AfricanBri/` |
| `4` | `Flat` | directly in the subscriber root |

`ItemIdTree8x2` is the default for commands where the path convention is
optional. Unicode ItemIds are NFC-normalized and bucketed by Unicode text
elements rather than raw UTF-16 code units.

## Naming conventions

`iorg organize` requires a naming convention:

| Number | Name | Purpose |
|---:|---|---|
| `1` | `Legacy` | Established full legacy component naming |
| `2` | `ItemTemplate` | Simplified `ItemId_TemplateName.ext` rendering names |
| `3` | `Structured` | Glob-searchable structured ItemId, image number, suffix, and metadata naming |

`Structured` is the current default convention elsewhere in the tool.

## Organize source images

```bash
iorg organize \
  --source /srv/incoming/Nomsa \
  -c OneDrive \
  --root LiveAfricaStageImage \
  --subscriber Nomsa \
  --pathconv 3 \
  --nameconv 3
```

The subscriber may instead be supplied positionally, but not both ways:

```bash
iorg organize Nomsa --source /srv/incoming/Nomsa \
  -c OneDrive --root LiveAfricaStageImage --pathconv 3 --nameconv 3
```

Organize behavior:

- enumerates supported image files directly in the source directory;
- normalizes each filename through RaiImage naming rules;
- calculates its ItemId and image number;
- copies it directly to its final ItemTree pathname;
- leaves the source file untouched;
- reports each success and per-file failure; and
- never stages output in `Os.TempDir` before moving it into a CloudDrive.

Use `--debug` for full source/destination paths and resolution diagnostics.

## Discover files with `list`

`list` recursively searches one resolved subscriber tree and is strictly
read-only.

```bash
iorg list 'WorkInPro*' \
  -c OneDrive --root LiveAfricaStageImage --subscriber Nomsa

iorg list '*.puml' \
  -c OneDrive --root LiveAfricaStageImage --subscriber Nomsa

iorg list '*.raid' \
  -c OneDrive --root LiveAfricaStageImage --subscriber Nomsa

iorg list '*' \
  -c OneDrive --root LiveAfricaStageImage --subscriber Nomsa
```

Quote wildcard patterns so the invoking shell does not expand them before iorg
receives the pattern.

List returns managed image and diagram artifacts, including `.puml`, `.raid`,
and supported image types. Unknown files such as `.tmp` are excluded. Zero
matches are successful and report `0 matching file(s)`.

Output modes:

- default: one filename per match plus a count;
- `--quiet`: one full pathname per match, no summary; and
- `--json`: a JSON array of filenames, no banner or prose.

Do not combine `--quiet` and `--json`.

## Inspect an exact ItemId family before changing it

For discovery by prefix or extension, use `list`. Before deleting an exact
family, use `clean` without `--force`:

```bash
iorg clean AfricanBrisket \
  -c OneDrive --root LiveAfricaStageImage --subscriber Nomsa
```

This searches every supported path convention for files belonging to the exact
ItemId and prints what would be deleted. It does not select similar ItemIds that
merely share the same bucket or prefix.

This dry run is the best current preflight before `move`, because `iorg move`
does not itself have a dry-run option.

## Move, rename, or migrate a family

### Move to a selected path convention

```bash
iorg move AfricanBrisket \
  -c OneDrive --root LiveAfricaStageImage --subscriber Nomsa \
  --pathconv 3
```

The ItemId stays `AfricanBrisket`; all matching family files move to its 8x2
home.

### Rename the whole family

```bash
iorg move AfricanBrisket AfricanDinner \
  -c OneDrive --root LiveAfricaStageImage --subscriber Nomsa \
  --pathconv 3
```

Every selected filename keeps its suffix and extension while its ItemId stem
changes, for example:

```text
AfricanBrisket_01.png       -> AfricanDinner_01.png
AfricanBrisket_config.puml  -> AfricanDinner_config.puml
AfricanBrisket.raid         -> AfricanDinner.raid
```

Move behavior:

- searches all supported source path conventions;
- fails if the same ItemId exists in more than one distinct convention home;
- selects the exact ItemId family rather than a shell-style prefix family;
- moves image and diagram artifacts together;
- can combine rename and path-convention migration; and
- prunes vacated empty bucket directories after a successful family move.

Output modes:

- default: `source -> destination` plus a count;
- `--quiet`: destination full pathnames only; and
- `--json`: structured source/destination records.

`move` mutates the filesystem immediately. Inspect the family first.

## Clean one exact ItemId family

Dry-run preview:

```bash
iorg clean AfricanBrisket \
  -c OneDrive --root LiveAfricaStageImage --subscriber Nomsa
```

Apply the exact-family deletion:

```bash
iorg clean AfricanBrisket \
  -c OneDrive --root LiveAfricaStageImage --subscriber Nomsa \
  --force
```

The applied command removes supported source images, rendered derivatives,
`.svg`, `.puml`, `_config.puml`, and `.raid` members of the exact family while
preserving a bucket-sharing sibling such as `AfricanBrigadine.png`. Empty bucket
directories are pruned afterward.

Always review the dry-run output before adding `--force`, especially on a
CloudDrive.

## Clean rendered derivatives

```bash
iorg clean --cache \
  -c OneDrive --root LiveAfricaStageImage --subscriber Nomsa
```

This recursively deletes recognized rendered derivatives, including WebP/AVIF
and structured cache/template/tile variants, while preserving source images and
diagram source artifacts.

`clean --cache` is already an explicit destructive operation. It does not offer
a dry run and rejects `--force`. Use `iorg list` to inspect relevant extension or
suffix patterns before invoking it.

## Machine-readable workflows

Find all PlantUML sources:

```bash
iorg list '*.puml' -c OneDrive --root LiveAfricaStageImage \
  --subscriber Nomsa --json
```

Count a discovered family:

```bash
iorg list 'AfricanBrisket*' -c OneDrive --root LiveAfricaStageImage \
  --subscriber Nomsa --json | jq 'length'
```

Record a move result:

```bash
iorg move AfricanBrisket AfricanDinner \
  -c OneDrive --root LiveAfricaStageImage --subscriber Nomsa \
  --pathconv 3 --json
```

Iorg has no historical audit log for these actions. Capture JSON output in the
calling deployment or agent workflow when a durable external operation record
is required.

## Cloud-storage safety

RAIkeep's mandatory invariant applies to every mutating iorg operation:

- output is written or moved through RaiFile directly at the CloudDrive target;
- no TempDir-created file or directory is moved into a configured cloud tree;
- a file is not deliberately deleted and recreated as an update mechanism; and
- broad directory replacement is forbidden.

Explicit clean operations still produce intentional CloudDrive deletions. Review
their scope and provider confirmation carefully.

## Exit behavior and troubleshooting

- Successful commands return exit code `0`; `list` also succeeds with zero
  matches.
- Invalid options, unresolved roots, ambiguous ItemId placement, missing move
  sources, or per-file failures return a nonzero result.
- Add `--debug` to show resolution and exception details.
- Use command-specific help rather than relying on older flat `4.x` syntax.
- The old flat syntax remains compatible through `4.x`; command-first syntax is
  preferred and will be required in `5.x.x`.

## Terminal font

The help screen uses Nerd Font glyphs. Blink on iPadOS has been verified with
[Jet Brains Mono Nerd Font](https://github.com/blinksh/patched-fonts/blob/main/Jet%20Brains%20Mono%20Nerd%20Font.css).
See [TERMINAL_FONTS.md](https://github.com/Burkhardt/RAIkeep/blob/main/doc/TERMINAL_FONTS.md)
for setup guidance.
