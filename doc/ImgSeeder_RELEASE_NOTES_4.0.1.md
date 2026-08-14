# Release Notes: ImgSeeder v4.0.1

**Date:** 2026-08-10
**Author / Delivering Agent:** RAIkeep Dev Agent
**Delivered Version:** v4.0.1
**Target Consumers:** AfricaStage, AIA
**Status:** Prepared — publication approval pending

## 1. Summary

ImgSeeder v4.0.1 adds command-first `organize` and `clean` interfaces to `iorg`
with operation-scoped options and contextual help. Established flat invocations
remain functional during the `4.x` transition.

## 2. Resolved Change Requests (CRs)

- [`CR006_AfricaStage_to_RAIkeep_CliSubcommands.md`](https://github.com/Burkhardt/AIA/blob/main/doc/CR006_AfricaStage_to_RAIkeep_CliSubcommands.md) — implements contextual subcommands and isolated operation options for `iorg`.

## 3. Root Cause Analysis & Technical Resolution

The flat parser exposed organization conventions and deletion switches in one
option set, then inferred delete versus organize behavior after parsing. The
v4.0.1 entry point selects the command parser only when the leading token is
`organize` or `clean`; all other input continues through the existing parser.

Both parsers normalize into the same organizer and short-name deletion handlers.
The command parser validates option scope before execution and maps human-facing
convention numbers `1`, `2`, and `3` to the three declared enum choices.

The CR's abbreviated clean example omitted the existing required deletion target.
RAIkeep retained `ShortName` as a required argument so `clean --force` can never
be interpreted as an unbounded delete. When `--subscriber` is omitted, the final
segment of the complete `--root` destination supplies the subscriber identity;
callers may instead provide an explicit parent root plus `--subscriber`.

## 4. Public Contract & API / Package Changes

Preferred syntax:

```text
iorg organize [<Subscriber> | --subscriber <name>] --source <dir> (-r|--root) <dir>
              (-p|--pathconv) <1|2|3> (-n|--nameconv) <1|2|3>
iorg clean <ShortName> [--subscriber <name>] (-r|--root) <dir> [--cache] [--force]
```

- `organize` owns source and convention options.
- `clean` owns `--cache` and `--force`; it is a dry run by default.
- `-r` remains a supported short alias for `--root` in both command parsers; it
  is a configuration option and is not deprecated by the subcommand transition.
- Help explicitly marks the `-p`/`--pathconv`, `-n`/`--nameconv`, and
  `-c`/`--cloud` defaults. Cloud choices preserve the configured
  `Os.Config.DefaultCloudOrder`, omit providers without configured paths, and
  reject providers outside that filtered list. When cloud is omitted, the first
  available configured default is selected; an explicit absolute root or `.`
  remains local unless the caller explicitly supplies a cloud option.
- Existing flat organization and short-name deletion syntax remains supported
  throughout `4.x`.
- The legacy parser is scheduled for removal in `5.x.x`; see
  [`CLI-PARSER-TRANSITION-4.x-TO-5.x.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CLI-PARSER-TRANSITION-4.x-TO-5.x.md).
- Startup banner rules no longer use repeated equals characters.

## 5. Validation & Acceptance Evidence

- `ImgSeeder.Tests`: **15 passed, 0 failed, 0 skipped**.
- Executable-process coverage proves command organization, inferred subscriber
  resolution, safe clean dry-run/force behavior, exact-target deletion, legacy
  organization compatibility, option isolation, contextual help, and banner
  formatting.
- Process-level version coverage proves `iorg --version` emits `iorg v4.0.1`.
- Debug builds complete with zero warnings and zero errors.

## 6. Upgrade & Consumption Instructions

1. Update the coordinated RAIkeep tool line to v4.0.1 after publication approval.
2. Prefer `iorg organize` and `iorg clean` for new scripts.
3. Existing flat scripts may migrate during `4.x`; they are scheduled to stop
   working in `5.x.x`.
4. Keep `ShortName` explicit for every clean operation and add `--force` only
   after reviewing the default dry-run output.
5. Independently validate AfricaStage image workflows and record the
   requester-led CR006 Accepted/Rejected evaluation.
