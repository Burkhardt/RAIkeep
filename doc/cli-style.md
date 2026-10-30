# RAIkeep CLI style

This is the help-screen contract for `pits`, `iorg`, `raid`, `rail`, `amafu`,
and the Python `jpit` / `jsonpit` entry points. The approved pits preview is
the reference. Help formatting must not change command behavior or machine output.

## Layout

- Use a monospaced terminal font with Nerd Font glyphs. Italic and bold faces
  improve the presentation; terminals without these faces still receive the text.
- Output spaces for alignment, never tab characters. Source-code indentation may
  use tabs; whitespace inside output strings is part of the program's behavior.
- Use three columns: option label, glyph, description. Right-pad labels to the
  longest label in the table, leave two spaces, reserve two cells for the glyph,
  then leave two spaces before the description. Continuation rows use the same columns.
- Measure plain text before inserting ANSI sequences. Count Unicode scalars for
  the single-cell ASCII and Nerd Font glyphs used in these columns, not UTF-16 units.
- A narrow terminal may put the description on an indented following line.
- `rail --groups` wraps descriptions and rule entries at 90 visible columns,
  at word boundaries. Continuations align after the description label or
  `RAIxxx ` prefix. Rule entries use the same two-space indentation as
  `Description:` and have no leading bullet or brackets: IDs are
  bold blue everywhere, including group lists and prose; titles are cyan.
  The `Description:` label is italic magenta and
  description text yellow. Keep an indivisible word intact even if that word
  alone exceeds the available width.
- The entire banner heading, including its information glyph and version, is bold
  cyan. Decorative rules are regular cyan, at least 40 characters long, and
  extend to the visible heading width for longer titles. Use the actual executable version.
- Do not advertise legacy syntax or add a Legacy row. Examples use canonical commands.
- Remove spaces around choice separators: `(<PitName>|--wwwa)` and
  `(--out-dir <dir>|--json)`.

## Glyph groups

The glyph in the second column supplies the base color for the row's ordinary
label and description. Use the same mapping across tools. Syntax highlighting
takes precedence over this base color.

| Glyph meaning | ANSI foreground |
| --- | --- |
| Folder | Yellow (`33`) |
| Help / question mark | Green (`32`) |
| Banner toggle | Bright magenta (`95`) |
| Information | Cyan (`36`) |
| File | Magenta (`35`) |
| Download / upload | Blue (`34`) |
| Success / check | Bright green (`92`) |
| Unavailable | Bright red (`91`) |
| Warning / force | Bright yellow (`93`) |
| Error / bug | Red (`31`) |
| Execution | Indexed color `114` |
| Rule / shield | Indexed color `75` |
| Repair / wrench | Indexed color `208` |
| Output | Indexed color `117` |
| Numeric convention selector | Indexed color `180` |

Related variants, such as banner on/off or success/check, belong to one group.
New glyph groups need an explicit palette choice in the common formatter.

## Syntax colors and emphasis

| Construct | Rendering |
| --- | --- |
| Option names, such as `-b`, `--patch`, `--source` | Green (`32`) everywhere |
| Content of `<tenant\|path>` | Bright cyan (`96`) and italic |
| Round one-of group, such as `(<PitName>\|--wwwa)` | Magenta (`35`); angle contents remain italic |
| Optional square group, such as `[-a\|--all]` | Bright blue (`94`) |
| Code inside single quotes | Yellow (`33`) |

Option names retain their green color inside groups and quoted code. Nested angle
values retain their bright cyan color inside optional groups or quoted code;
inside round one-of groups they use that group's magenta. This keeps required
values, choices, and optional notation distinguishable without changing a switch's color.

The characters `<`, `>`, and `|` keep the surrounding base color and remain upright.
Only the value text inside angle brackets is italic. Ordinary explanatory
parentheses, such as `(for piping to jq)`, are not one-of groups. Quoted code
returns to the surrounding style at its closing quote. Reset ANSI style at span
boundaries so colors, bold, and italics cannot leak into following text or the prompt.

## Cloud provider choices

Use a yellow folder glyph in the second column and the folder group's yellow
base text. Color each provider badge separately, in configured display order:

1. Bright cyan (`96`).
2. Bright green (`92`).
3. Bright blue (`94`).
4. Bright red (`91`).
5. Magenta (`35`).
6. Bright magenta (`95`).
7. Cyan (`36`).
8. Blue (`34`), then repeat the palette.

Retain the named provider badges and numbered badges for account-qualified names.
Use configuration for available choices; styling must not invent a default cloud
or change how a command resolves its destination.

## Plain and machine output

Respect a nonempty `NO_COLOR` and `TERM=dumb`. Redirected help is plain text:
the same words and spacing, with no ANSI escapes. JSON receipts, listings, audit
data, and diagnostics are outside this help-only formatter and retain their existing contracts.

## pits and jpit option parity

`jsonpit` and `jpit` are entry points to the same Python CLI. Shared operations
must use the same public option names, glyphs, descriptions, and syntax styling
as `pits`; Python-only commands may retain their own options.

| Public spelling | Meaning | Unadvertised compatibility spellings |
| --- | --- | --- |
| `-r, --pitroot` | Pit root or tenant | Python also accepts `--root` |
| `-c, --cloud` | Explicit configured cloud | Existing library wrapper aliases remain accepted |
| `-b, --debug` | Diagnostic context | — |
| `-n, --nologo` | Suppress the banner | — |
| `-w, --window` | Keep the activity window until timeout | `--retain-window` |
| `-x, --id-exists` | Require every incoming ID to exist before seeding | `--require-exist`, `--require-existing` |
| `--patch` | Alias for `--id-exists` | — |

Hide old spellings in general and command help. Keep accepting them in the
parser and typed wrappers. General help omits positional-argument explanation
rows; a named-pit help request, such as `pits Activity -h`, may show them.
General command summaries show `list` without advertising `ls`; command-specific
`list -h` and `ls -h` show both listing usage forms. Keep these rules and their
regression checks aligned across the C# and Python implementations.

Directory export uses `export <PitName> --out-dir <dir>` and writes
`<PitName>.json`; `export --wwwa --out-dir <dir>` writes `wwwa.json` with the
same resolved-reference projection. Use `--json` for stdout. Select exactly one
output mode. An offset-explicit `--at` produces the shared `_export` / `data`
envelope. Python's former `--out <file>` remains accepted but unadvertised.

## Implementation and verification

The C# implementation is `OsLib/CliHelpStyle.cs`. Standalone Amafu compiles an
identical dependency-free source copy under `amafu/Shared/`; it does not acquire
an OsLib package dependency. Run `python3 scripts/sync-cli-style.py` after changing
the canonical source, and `python3 scripts/sync-cli-style.py --check` to detect drift.
Python implements the same contract in `jsonpit/cli_style.py`.

Tests must verify printed columns after stripping ANSI sequences, glyph group
colors, provider badges, uniform switch colors in examples, nested notation,
bold/italic boundaries, and plain redirected output. Test help and subcommand
help without installing tools or writing cloud data. Keep previews local until
the user has approved their appearance; do not publish or run the release chain
as part of a style change.

After a local `dotnet build RAIkeep.slnx`, preview one tool with
`env -u NO_COLOR bash scripts/preview-cli-help.sh pits` (substitute `iorg`,
`raid`, `rail`, `amafu`, or `jpit`). Pass `all` to display each tool in turn.
The preview runs local binaries and the Python checkout; it does not install
tools or run the release chain.

Run `python3 scripts/test-cli-style.py` to compare C# and Python ANSI output
byte-for-byte for common syntax, banners, cloud badges, and aligned rows, and to
compare their shared option rows in actual redirected help. The release validator
also checks that the two C# formatter source copies remain identical.
