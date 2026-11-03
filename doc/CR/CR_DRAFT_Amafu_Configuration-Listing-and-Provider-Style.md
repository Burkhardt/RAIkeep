# Proposed CR — Amafu configuration listing and provider presentation

Status: **Superseded by ratified CR076 and RAI's subsequent two-line cloud-layout amendment.**

Authoritative specification: [CR076](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR076_AIA_to_RAIkeep_Amafu_Configuration_Listing_and_Provider_Style.md).
The original proposal below is retained as a historical record, not the final output contract.
Date: 2026-11-02.
CR number and target release: unassigned.
Owner: RAIkeep / Amafu. Requested by Dr. Rainer Burkhardt.

This proposal supersedes the initial local `amafu list all` preview on branch
`codex/amafu-list-config`. It does not change the interrupted v4.5.16 release,
its tags, package versions, or umbrella pointers. The release chain remains
manually operated by RAI; provisioning remains with Engenho.

## 1. Purpose

Let users inspect selected RAIkeep settings without reading the JSON5 source.
Use aligned, styled human-readable listings consistent with the CLI help screen,
and clean scalar output when requesting one value. Do not dump the configuration
file verbatim.

Read the current user's `~/.config/RAIkeep.json5`. The operation is read-only:
no provider discovery, directory creation, configuration repair, write probes,
SSH connections, cloud application launches, or remote configuration reads.
Keep Amafu standalone without introducing an OsLib runtime dependency.

## 2. Public command contract

```text
amafu list temp
amafu list backup
amafu list order <provider|all>
amafu list cloud <provider|all>
amafu list observer <name|all>
```

| Selector | Configuration entry | Output |
| --- | --- | --- |
| `temp` | `TempDir` | Expanded absolute directory path |
| `backup` | `LocalBackupDir` | Expanded absolute directory path |
| `order <provider>` | `DefaultCloudOrder` | One-based position, or `0` when absent |
| `order all` | `DefaultCloudOrder` | All names, in configured order, on one line |
| `cloud <provider>` | `Cloud[provider]` | Expanded absolute configured directory path |
| `cloud all` | `Cloud` | Aligned provider names and configured directory paths |
| `observer <name>` | Named entry in `Observers` | Configured SSH target, such as `rsb@Mzansi` |
| `observer all` | `Observers` | Aligned observer names and configured SSH targets |

Remove the top-level `all` selector: `amafu list all` is not a supported way to
print the file or a complete configuration dump. `all` is supported only as the
second selector for `order`, `cloud`, and `observer`.

Proposed default for ratification: `amafu list` without a selector displays its
usage and available selectors. It does not print configuration contents.
Selectors without required arguments likewise report the required syntax.

## 3. Scalar lookups

Command arguments use literal configured names without decorative glyphs.
Provider badges belong to human-readable output, not to argument values.

For a configuration whose first ordered provider is 󰰕 OneDrive:

```zsh
amafu list cloud OneDrive
```

```text
/Users/RSB/Library/CloudStorage/OneDrive/OneDriveData/
```

```zsh
amafu list order OneDrive
```

```text
1
```

```zsh
amafu list order SomeOtherDrive
```

```text
0
```

`0` means the name is absent from `DefaultCloudOrder`. It also applies when a
provider has a `Cloud` entry but is not included in that ordered array. It does
not conceal a missing, unreadable, or malformed configuration file.

```zsh
amafu list observer Mzansi
```

```text
rsb@Mzansi
```

Each successful scalar lookup prints exactly its value and one terminating
newline. No banner, label, quotes, glyphs, ANSI escapes, or summary appears on
stdout. The absent order value `0` is a successful lookup with exit code 0.
Do not invent an SSH target by combining a local username with an observer name.

Expand `~` against the execution user's home directory. Normalize configured
directory paths to absolute paths with a trailing directory separator, using
the execution platform's conventions. Do not require the directory to exist,
resolve symlinks into vendor paths, or guess a path from a provider name.
Read observer entries using the configuration shapes already supported by
RAIkeep; preserve the configured SSH target spelling.

## 4. Human-readable collection output

These examples are illustrative configuration values, not hardwired defaults.

### `amafu list order all`

Preserve `DefaultCloudOrder` exactly; the first displayed entry has position 1.
Use a single space between badged provider names and two leading spaces:

```text
  󰰕 OneDrive 󰯴 Dropbox 󰯽 GoogleDrive 󰰃 ICloudDrive
```

### `amafu list cloud all`

List every configured `Cloud` entry, including providers not present in
`DefaultCloudOrder`. Use matching pairs from the configuration; do not assign
another provider's path to a name. Each row starts with one literal tab before
the provider badge. Put one space between the badge and provider name, omit the
colon after the name, and put exactly two literal tabs before the opening path
quote. Quote each path with balanced double quotes because paths can contain
spaces. Do not substitute space padding for these tabs.

The row contract, shown with escaped control characters, is
`\t{badge} {provider}\t\t"{path}"\n`. The following preview contains actual tabs:

```text
	󰰕 OneDrive		"/Users/RSB/Library/CloudStorage/OneDrive/OneDriveData/"
	󰯴 Dropbox		"/Users/RSB/Library/CloudStorage/Dropbox/DropboxData/"
	󰯽 GoogleDrive		"/Users/Shared/ServerData/GDriveData/"
	󰰃 ICloudDrive		"/Users/RSB/Library/Mobile Documents/com~apple~CloudDocs/ICloudDriveData/"
```

### `amafu list observer all`

List configured observer names and targets using space-padded columns:

```text
  Mzansi:  rsb@Mzansi
  Ingwe:   rsb@ingwe
  Mdlaka:  umshadisi@Mdlaka
```

Proposed deterministic ordering: cloud entries follow `DefaultCloudOrder` where
present, followed by remaining entries in configuration order. Observer entries
retain configuration order. Empty collections print a short plain-language
message rather than generating defaults. These ordering and empty-state choices
are proposals for ratification.

## 5. Shared styling and provider glyphs

Follow the existing [CLI style guide](https://github.com/Burkhardt/RAIkeep/blob/main/doc/cli-style.md).
Keep space-padded help and observer columns; measure visible columns before
adding ANSI styling. The cloud collection rows in section 4 are an explicit
RAI-requested exception to the guide's space-only layout: preserve their one
leading tab and two separator tabs, including in redirected output. Respect
`NO_COLOR`, `TERM=dumb`, and redirected output. Collection output retains its
layout and provider glyphs when colors are disabled.

Every provider-name appearance in human-readable collection output and rendered
help prose must carry the same badge as jpit. This requirement excludes literal
command arguments and the intentionally undecorated scalar output contract.
Use the existing `CliHelpStyle.CloudGlyph` / jpit provider-icon algorithm:

| Provider display name | Glyph code point | Badge initial |
| --- | --- | --- |
| 󰰕 OneDrive | `U+F0C15` | O |
| 󰯴 Dropbox | `U+F0BF4` | D |
| 󰯽 GoogleDrive | `U+F0BFD` | G |
| 󰰃 ICloudDrive | `U+F0C03` | I |

Reuse numbered badges for account-qualified or other configured names, including
the existing `(number)` fallback after nine entries. Do not invent a separate
first-letter or fixed provider-color mapping.

Badge colors follow display position, using the existing repeating ANSI palette:
`96`, `92`, `94`, `91`, `35`, `95`, `36`, `34`. Provider text uses the folder
group's yellow (`33`). Compute one provider display sequence per invocation and
reuse its badge indices and colors wherever the same provider is displayed.
For a help-style collection, use the shared folder group for path labels and
values; use the information group's cyan (`36`) for observer labels and targets.
Keep syntax highlighting and bold/italic help rules consistent with the guide.

Standalone Amafu must continue compiling the synchronized dependency-free
formatter copy. Verify with `python3 scripts/sync-cli-style.py --check`.

## 6. General and selector-specific help

Remove the `Configuration` row from the standard `amafu -h` screen. Add `list`
to the command summary and advertise the canonical selector forms.

Support help before accessing configuration, including when the file is absent:

```zsh
amafu list -h
amafu list temp -h
amafu list backup -h
amafu list order -h
amafu list cloud -h
amafu list observer -h
```

`--help` is equivalent to `-h`; `-n` / `--nologo` suppresses only the help banner.
Help must select the most specific recognized selector, regardless of where a
global help flag appears. Do not answer `amafu list order -h` with only generic
list help.

The order help must explain these points explicitly:

```text
amafu list order <provider|all>
  <provider>  Prints its one-based position in DefaultCloudOrder.
              Prints 0 when the name is not in DefaultCloudOrder.
  all         Lists configured provider names in their configured order.
```

Cloud help explains expanded configured paths and the `all` table. Observer
help explains exact configured SSH targets and the `all` table. Temp and backup
help identify their configuration keys and path expansion behavior. Each selector
help includes a valid command example and describes its output shape. Provider
names in explanatory output use the shared provider badges and colors; example
commands remain executable without glyphs in their arguments.

## 7. Diagnostics and read-only behavior

Proposed exit codes, for ratification:

- `0`: successful listing or help; includes an absent order lookup returning `0`.
- `2`: invalid selector, missing argument, surplus argument, or unsupported option.
- `4`: missing/unreadable/malformed configuration, invalid selected value type,
  or missing named cloud/observer/temp/backup value.

Errors go to stderr with empty stdout. Do not silently turn missing cloud or
observer names into empty successful values. A valid absent ordered name is the
explicit exception described above.

Use the configured key spelling in output. Proposed lookup policy: selectors
and named lookups are case-insensitive when unambiguous; case-colliding configured
names produce a diagnostic rather than choosing one silently. Confirm this
policy during ratification.

No command changes configuration, checks provider connectivity, logs into a cloud
account, or prints unrelated configuration entries. A structured observer entry
must expose only its supported SSH target, not unrelated credential fields.
Strict JSON output, arbitrary setting queries, raw-file dumps, and remote
execution flags are outside this proposal.

## 8. Acceptance criteria

1. All command forms in section 2 work; the superseded top-level `list all`
   is rejected with useful usage guidance.
2. Temp, backup, and cloud scalar paths expand correctly on macOS, Linux/WSL,
   and Windows without creating directories or resolving symlinks.
3. Named order lookups return exact one-based positions; absent names return
   only `0\n` with exit code 0, including a name configured outside the order.
4. A named observer lookup returns exactly the configured SSH target plus a
   newline. Collection mode preserves each name/target association.
5. `order all` preserves configured order, and `cloud all` includes every cloud
   entry with the correct path. Each cloud row has exactly one leading tab,
   one space between badge and name, no colon after the name, and exactly two
   tabs before the double-quoted path. Observer columns and help use spaces.
6. Provider glyphs, numbered fallbacks, initials, and badge-color sequences match
   jpit and the shared formatter, including reordered and account-qualified names.
7. Scalar output has no decoration even in an interactive terminal. Redirected
   collection/help output contains no ANSI escapes; `NO_COLOR` and `TERM=dumb`
   are honored. ANSI resets prevent style leakage.
8. Every selector's `-h` / `--help` displays detailed selector-specific usage,
   examples, and semantics without reading configuration. In particular,
   `amafu list order -h` documents both one-based positions and absent-name `0`.
   The standard help no longer has a Configuration row.
9. Missing configuration, invalid types, unsupported arguments, ambiguous names,
   and unknown named values follow the ratified diagnostics contract with no
   partial successful output.
10. Configuration bytes and modification time remain unchanged. No shortcuts,
    temporary files, directories, cloud data, or network connections are created.
11. Existing `detect`, `init`, `init-config`, and `reconcile` behavior remains
    unchanged; Amafu's targeted tests and shared-style synchronization pass.

## 9. Ratification and delivery

Adele assigns the final CR number and target release and confirms the proposed
default usage, deterministic collection ordering, empty-state presentation,
case-matching policy, and error codes. The requested selector syntax, order
sentinel `0`, detailed selector help, and provider-style parity above record RAI's
explicit requirements.

After ratification, replace the initial local preview implementation, update
Amafu's README/API documentation and selector help, run the targeted acceptance
tests, and provide a local terminal preview for RAI's visual review before any
push or publication. Preserve existing release tags and never modify a published
package in place. RAI starts the release chain manually; Engenho provisions.
