# CR014 — Typed CLI Command Wrappers

**Requesting product:** RAIkeep
**Requester and acceptance owner:** RAI
**Receiving product:** RAIkeep
**Target release:** RAIkeep v4.2.2
**Date:** 2026-08-20
**Status:** Accepted by RAI — implementation underway

## 1. Scope clarification

The submitted CR014 testing-infrastructure draft is replaced by this accepted
scope after review with RAI.

RAIkeep package projects remain responsible for testing their own behavior.
AIA and other consumers remain responsible for their integration tests. CR014
does not introduce an eighth `RAIkeep.Testing` package, an umbrella CDAT
harness, or duplicate tests for PitSeeder and ImgSeeder behavior.

CR014 instead closes the typed external-command boundary needed by servers,
agents, and other long-running consumers that invoke the installed RAIkeep CLI
tools.

## 1.1 Principal determination: submitted instructions overruled

In the capacity of senior Codex Agent and Principal of RAIkeep, I explicitly
overrule the following instructions from the submitted
`CR014_AIA_to_RAIkeep_Testing_Infrastructure.md` draft:

1. **A new public `Raikeep.Testing` package.** This would silently create an
   eighth published package and alter the coordinated seven-package release
   chain. No eighth package is introduced by CR014.
2. **A shared umbrella CDAT harness that determines `ACCEPTED` or `REJECTED`.**
   Consumer acceptance belongs to AIA or the consuming product. RAIkeep must
   provide verifiable public behavior, but must not make the provider's harness
   the consumer's independent acceptance authority.
3. **New package-level test projects for all seven packages.** The seven
   package-owned test projects already exist and are exercised by their owning
   repositories. CR014 does not duplicate or replace them.
4. **Tests that re-exercise PitSeeder or ImgSeeder product behavior from
   OsLib or the umbrella.** Pit persistence remains PitSeeder/JsonPit test
   responsibility; image organization remains ImgSeeder/RaiImage test
   responsibility. OsLib tests only its wrapper contract.
5. **A public fake/sample `IDiagramModelProvider` as CR014 testing
   infrastructure.** This is unrelated to the typed `pits` and `iorg` process
   boundary and is not introduced under CR014.
6. **Generic public verification APIs added solely for the proposed CDAT
   harness.** CR014 adds only the public APIs required to construct, validate,
   and execute typed CLI calls.
7. **An automated CR → Release Notes → Evaluation workflow.** Governance
   evaluation remains a human/agent responsibility and is not converted into a
   library runtime result by CR014.
8. **The draft's obsolete per-package and aggregate test-count acceptance
   criteria.** Verification uses the actual current package suites and reports
   their observed counts; it does not preserve the internally inconsistent
   `214 tests` claim.
9. **Default asset seeding requirements and the testing-infrastructure ADR.**
   These are unrelated to command wrapping and are not prerequisites for the
   typed CLI boundary.

This determination does **not** reduce existing package-owned test coverage,
CR008/CR009/CR010 acceptance coverage, package-only restore validation, or the
manual release gate held by RAI. It narrows CR014 to the concrete missing
capability approved by RAI: safe, typed invocation of installed RAIkeep CLI
tools from servers, agents, and other consumers.

## 1.2 Determination on the CR014.1 test concept

RAI subsequently adopted `CR014.1_test-concept.md` as the required wrapper-test
guidance. Its six layers and acceptance criteria are therefore part of CR014:

- exact token, ordering, quoting, special-character, empty, and repeated-value
  preservation through capture executables;
- output, error, Unicode, long-output, no-output, exit-code, timeout, and
  cancellation coverage;
- representative mandatory/optional parameter combinations rather than an
  exhaustive Cartesian product;
- wrapper-start failures distinguished from completed CLI results;
- original argument-vector metadata on completed results; and
- minimal real-CLI smoke checks that prove `pits` and `iorg` can be invoked
  through their wrappers without duplicating either product's domain tests.

The existing `RaiSystemResult` remains the result type and is extended where
needed to satisfy the concept; a parallel result model is unnecessary. Tests
remain in the existing package-owned test projects rather than creating the
eighth package rejected in section 1.1. These placement decisions reconcile
CR014.1 with RAIkeep's established package boundary without reducing any of
its behavioral requirements.

## 2. Request

1. Add public `PitsCommand` and `IorgCommand` wrappers to OsLibCore.
2. Model the preferred 4.x subcommand syntax for `pits` and `iorg`.
3. Validate mandatory parameters and mutually exclusive modes before starting
   a process.
4. Pass optional parameters only when explicitly supplied.
5. Execute arguments as discrete process tokens so paths and values behave as
   they do when correctly quoted in a shell command.
6. Support synchronous and asynchronous execution, output/error capture, exit
   codes, and cancellation through the existing
   `CliCommand -> RaiSystem` boundary.
7. Audit RAIkeep calls to `pits`, `iorg`, ImageMagick, PlantUML, and the image
   optimizers. Calls to a wrapped tool must use its wrapper rather than an
   individually constructed process invocation.

## 3. Package boundary

### 3.1 OsLibCore

OsLibCore owns tool-neutral process execution and installed-tool discovery.
It therefore owns:

- `CliCommand` tokenized execution overloads;
- `PitsCommand`;
- `IorgCommand`; and
- the argument contract types used by those wrappers.

These types must not depend on JsonPit, RaiImage, PitSeeder, or ImgSeeder. They
model only the public CLI grammar and installed executable.

### 3.2 RaiImage

RaiImage retains wrappers whose commands are specific to image and diagram
rendering:

- `ImageMagickCommand`;
- `PlantUmlCommand`;
- `OptiPngCommand`; and
- `JpegTranCommand`.

Image operations must delegate to these wrappers. A wrapper may create
`RaiSystem` internally as the single process boundary when special launch
behavior is required, such as `java -jar` for PlantUML.

### 3.3 PitSeeder and ImgSeeder

PitSeeder continues to own the `pits` executable and its behavior. ImgSeeder
continues to own the `iorg` executable and its behavior. Neither project gains
a dependency on its OsLib wrapper.

## 4. Required `pits` grammar

`PitsCommand` shall support the preferred command forms:

```text
pits seed <PitName> --source <file> [global options]
pits seed --wwwa --source <directory> [global options]
pits export (<PitName> | --wwwa) --out-dir <directory> [global options]
pits export (<PitName> | --wwwa) --json [global options]
pits audit (<PitName> | --wwwa) [--machine <filter>] [--level <severity>] [--json] [global options]
```

Supported global options are `--pitroot`, `--cloud`, `--debug`, `--nologo`, and
`--retain-window`.

The wrapper shall reject a missing pit target, a simultaneous pit and WWWA
target, a missing source, a missing export destination, or simultaneous JSON
and directory export modes before executing the binary.

## 5. Required `iorg` grammar

`IorgCommand` shall support the preferred command forms:

```text
iorg organize --source <directory> --root <directory>
  --pathconv <1|2|3> --nameconv <1|2|3>
  [--subscriber <name>] [global options]

iorg clean <ShortName> --root <directory>
  [--subscriber <name>] [--cache] [--force] [global options]
```

Supported global options are `--cloud`, `--debug`, and `--nologo`.

The wrapper shall reject missing source/root/short-name parameters, invalid
path or naming convention numbers, path-like short names, and blank explicitly
supplied subscriber or cloud values before executing the binary.

## 6. Verification boundary

Wrapper tests shall use executable capture doubles created through OsLib test
utilities. They shall prove:

- executable discovery and invocation;
- exact argument count, order, and value preservation;
- paths and values containing spaces remain one argument;
- mandatory and mutually exclusive parameter validation occurs before launch;
- optional arguments appear only when requested;
- exit code, standard output, and standard error are returned; and
- asynchronous execution and cancellation use the established OsLib contract.

The tests shall not exercise Pit persistence, image organization, or other
internal behavior owned by PitSeeder and ImgSeeder.

## 7. Documentation and release

- Keep every package version at `4.2.2`.
- Document the public wrappers in the API and README of each package that owns
  one.
- Cite CR014 in the affected package and umbrella 4.2.2 release notes.
- Update CLI hierarchy documentation to show wrapper ownership.
- Run focused wrapper tests, affected package Release suites, all relevant
  downstream Release suites, and package-only dependency validation.
- Do not tag or publish. RAI manually starts `scripts/release-chain.sh 4.2.2`
  after preparation is complete.

## 8. Acceptance criteria

CR014 is complete when:

- `PitsCommand` and `IorgCommand` are public OsLibCore APIs;
- their preferred 4.x command forms and parameters are typed and validated;
- wrapped processes receive exact tokenized arguments;
- image and diagram tool calls use their RaiImage wrappers;
- no individually baked `pits` or `iorg` execution remains in production code;
- focused wrapper tests pass without testing PitSeeder or ImgSeeder internals;
- affected API, README, hierarchy, and 4.2.2 release documents are current;
- the coordinated 4.2.2 release preflight is green; and
- RAI retains the release-chain execution gate.

---

*Accepted and scope-corrected by RAI after review of the submitted testing-
infrastructure draft and the package-owned testing boundary.*
