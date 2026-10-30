# Handover to Rita: apply the RAIkeep CLI style to Engenho

Rita,

Rainer has reviewed and approved the local RAIkeep help-screen formatting.
Please apply the same visual language to the Engenho CLI in TypeScript/Deno:
aligned columns, colors grouped by glyph meaning, consistent syntax colors,
and readable wrapped descriptions. Keep Engenho's own commands and terminology.

This is a presentation change. Preserve command behavior, option parsing,
defaults, exit codes, and machine-output contracts. Please show Rainer a local
preview before pushing, publishing, or changing installed tools.

## Reference material

- [RAIkeep CLI style guide](https://github.com/Burkhardt/RAIkeep/blob/main/doc/cli-style.md)
- [C# formatter](https://github.com/Burkhardt/OsLib/blob/main/CliHelpStyle.cs)
- [Python formatter](https://github.com/Burkhardt/jsonpit-python/blob/main/jsonpit/cli_style.py)
- [rail group formatting](https://github.com/Burkhardt/RaiGuard/blob/main/rail/Program.cs)
- [Cross-language style checks](https://github.com/Burkhardt/RAIkeep/blob/main/scripts/test-cli-style.py)

These changes are currently being reviewed locally. If the linked revision does
not yet contain them, use the matching files in the RAIkeep working checkout
under `/Users/RSB/Projects/GitHub/RAIkeep`; older published formatting is not the
reference for this handover.

Please inspect Engenho's current CLI first, then implement one reusable help
renderer rather than styling each command separately. Port the formatting
contract, not the C# or Python dependencies. The pits/jpit parser and export
changes described in the guide are specific to those tools and are outside
this Engenho task.

## Columns and banner

Use spaces inside terminal output strings, never tabs. Source indentation is
a separate matter.

Each option table has three columns: option label, glyph, description. Pad labels
on the right to the longest visible label in that table, append two spaces,
reserve two cells for the glyph, then append two spaces before the description.
Measure plain text before adding ANSI sequences. Do not count escape bytes or
UTF-16 surrogate pairs as visible columns. For the reference's single-cell
ASCII/Nerd Font glyphs, TypeScript's `Array.from(text).length` corresponds to
the scalar count used by the C# formatter; it is not a universal width function
for arbitrary emoji, combining marks, or wide characters.

The complete banner heading, including its information glyph and actual CLI
version, is bold cyan (`1;36`). Decorative rules are regular cyan (`36`), at
least 40 horizontal characters long, and extend to the heading's visible width.
Use Engenho's actual executable name and version, not a copied RAIkeep version.

## Glyph colors

The second-column glyph determines the base color of both the option label and
its ordinary description text. The same glyph group always has the same base
color. File, folder, and transfer glyphs are separate groups.

| Meaning | ANSI SGR foreground |
| --- | --- |
| Folder | `33` yellow |
| Help / question mark | `32` green |
| Banner toggle | `95` bright magenta |
| Information | `36` cyan |
| File | `35` magenta |
| Download / upload | `34` blue |
| Success / check | `92` bright green |
| Unavailable | `91` bright red |
| Warning / force | `93` bright yellow |
| Error / bug | `31` red |
| Execution | `38;5;114` |
| Rule / shield | `38;5;75` |
| Repair / wrench | `38;5;208` |
| Output | `38;5;117` |
| Numeric convention selector | `38;5;180` |

Use the reference glyphs where Engenho has the corresponding concept. In
particular: folder `U+EA83`, help `U+F059`, information `U+EA74`, file `U+EA7B`,
banner `U+EB1E`, and shield `U+F3ED`. Do not add unused CLI options just to
demonstrate a glyph.

## Syntax colors take precedence

Apply syntax styles inside both labels and descriptions, including examples:

| Construct | Style |
| --- | --- |
| Every switch name, such as `-h` or `--json` | Green `32`, wherever it appears |
| Text inside `<tenant\|path>` | Bright cyan `96`, italic `3` |
| Round one-of group, such as `(<target>\|--all)` | Magenta `35` |
| Optional group, such as `[-a\|--all]` | Bright blue `94` |
| Code inside single quotes | Yellow `33` |

Keep switches green even inside optional groups, choices, and quoted code.
Angle-bracket contents retain their value style inside optional groups or
quoted code; inside a round choice they use that choice's magenta, still
italic. Only angle-bracket contents are italic, not `<`, `>`, or `|`; those
delimiters retain the surrounding base color. Ordinary prose parentheses are
not choice groups. Remove spaces around choice separators.

Quoted code ends at the closing quote, with the surrounding style restored.
Reset ANSI attributes at span boundaries to prevent bold, italic, or color
leaking into subsequent text or the shell prompt. Use the reference parser's
precedence rather than a series of overlapping regex replacements.

For a cloud-choice row, use the yellow folder group for ordinary text and
provider names. Give each provider badge its own color, in configured order:
`96`, `92`, `94`, `91`, `35`, `95`, `36`, `34`, then repeat. Preserve configured
provider names and named/numbered badges. Do not invent a default provider.

## Long descriptions and grouped entries

The approved `rail --groups` presentation is:

```text
 Group 'Formatting' ({ RAI010 })
  Description: Tab indentation ('\t') and single-space token separation invariants
  RAI010 Enforce tab indentation and prohibit consecutive spaces
```

- The group name inside single quotes uses the quoted-code style.
- Every diagnostic ID is bold blue (`1;94`), including membership lists,
  entry labels, and mentions within descriptions. Use Engenho's existing IDs;
  the `RAI010` example is a RAIkeep reference, not a new Engenho identifier.
- Entry titles are cyan (`36`). IDs have no square brackets or leading bullets.
- `Description:` is italic magenta (`3;35`); its text is yellow (`33`).
- Description labels and entry IDs both start with two spaces of indentation.
- Wrap descriptive blocks at 90 visible columns, at word boundaries. Never
  split a word. An indivisible word may exceed the limit.
- Align continuation lines after the label or ID and its following space:
  after `  Description: ` for descriptions, after `  RAI010 ` for that entry.
  Include indentation in the 90-column budget. Wrap group membership headers
  too when necessary.

Do wrapping before ANSI insertion. Retain the appropriate syntax and identifier
styles on continuation lines. Adapt this grouped presentation where Engenho
already has comparable human-readable listings; do not add commands for it.

## Plain output and verification

Respect a nonempty `NO_COLOR` and `TERM=dumb`. Redirected help must be plain
text, with the same words, alignment, and wrapping but no ANSI escapes. Reuse
Engenho's terminal/environment handling and permissions. JSON and other machine
output must remain clean and unchanged; banners must not contaminate them.

Add focused tests for:

1. Column alignment after stripping ANSI; no tabs in rendered output.
2. Glyph-group consistency and independently colored provider badges.
3. Switch colors in labels, examples, nested choices, and quoted code.
4. Italic angle contents, upright delimiters, bold headings, and style resets.
5. Word wrapping, hanging indentation, intact long words, and consistent ID
   styling throughout grouped output.
6. Plain redirected output, `NO_COLOR`, `TERM=dumb`, and unchanged JSON output.

Please return the changed files, focused test results, and exact local commands
Rainer can run to review general help, command help, and any grouped listing.
Keep the preview local until he approves its appearance.
