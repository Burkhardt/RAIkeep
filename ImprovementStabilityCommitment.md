# Improvement Stability Commitment

Date: 2026-03-13

## Purpose

This document states a practical engineering commitment for RAIkeep:

- improve the libraries by using them
- stabilize the libraries by consolidating duplicated behavior into them
- avoid building one-off tooling in tests when the same capability belongs in the product libraries

This is meant to be publishable and actionable. It is not a slogan document. It is a working constraint on how new capabilities should be added.

## Core Position

RAIkeep should increasingly build, test, and validate itself with its own abstractions.

If a new capability is needed for testing, automation, or integration work, the default question should be:

"Should this become a reusable capability of OsLib, JsonPit, RaiUtils, or another RAIkeep library?"

The default answer should be yes unless there is a strong reason not to do so.

## Commitments

### 1. Reusable capabilities belong in the library, not only in the test

If we need to:

- execute scripts
- execute commands and capture stdout and stderr
- run remote shell commands over ssh
- wait for files to appear or vanish
- inspect synchronized cloud-backed files
- persist diagnostic traces

then those capabilities should exist as reusable library features when they are generally useful beyond one single test method.

Test code may compose these capabilities, but should not be their only home.

### 2. We will prefer self-hosting over ad hoc externalism

If RAIkeep already has a way to do something, we should use it.

Examples:

- if we already have `TextFile`, we should use `TextFile` for file creation and mutation
- if we already have `RaiFile`, we should use it for cloud-aware file behavior
- if we already have `RaiSystem`, we should use it for process execution instead of creating fresh process wrappers in tests
- if we already have `Script`, we should use or extend it instead of bypassing it with raw command strings where a reusable script abstraction is more appropriate

This is partly about consistency and partly about pressure-testing our own abstractions.

### 3. If our abstraction is not good enough, we improve it

The correct response to a missing feature is usually not:

- write a parallel helper in one test class

The correct response is usually:

- extend the existing abstraction so that the test and the product can both use it

Examples:

- if `RaiSystem` does not expose enough structured process results, improve `RaiSystem`
- if we need ssh-based command execution and it is generally useful, add a reusable ssh-oriented abstraction to OsLib
- if cloud synchronization waiting needs better diagnostics or timeout handling, add those capabilities where they belong in OsLib

### 4. Symmetry matters

The things we build should be used.

The things we use repeatedly should be built properly.

This symmetry is a stability strategy:

- repeated use reveals defects
- shared implementation reduces drift
- improvements in one place benefit both product code and tests

### 5. Tests should exercise the same important paths that production relies on

Where practical, tests should avoid bypassing core RAIkeep abstractions in favor of raw framework or operating system calls.

That does not mean raw platform calls are forbidden. It means they must have a clear reason.

Acceptable reasons include:

- bootstrapping the very first layer below our abstractions
- inspecting system state that our library intentionally does not model yet
- validating behavior against an independent external signal

But these should be deliberate exceptions, not the default approach.

### 6. New integration infrastructure should be designed for reuse from the start

When we add infrastructure for real cloud tests, remote observation, or distributed diagnostics, we should assume that:

- OsLib tests may use it
- JsonPit tests may use it
- later production or support tooling may also use it

That means naming, location, API shape, diagnostics, and configuration should be chosen accordingly.

## Architectural Consequences

This commitment implies the following direction for future work.

### Process execution

`RaiSystem` should remain the primary process execution abstraction.

If the current API is too weak for modern integration work, we should strengthen it rather than route around it.

Possible improvements:

- stronger structured results
- easier timeout control
- clearer stderr and stdout capture
- better async support
- explicit exit validation helpers

### Script execution

`Script` should be the preferred abstraction when a command sequence is substantial enough to deserve a named executable artifact.

If we need reusable remote command scripts, the answer should likely be a first-class abstraction, not repeated hand-built command strings.

### Remote execution

If ssh-based observation becomes part of the RAIkeep testing and diagnostic workflow, then OsLib should likely grow a reusable remote execution abstraction.

Candidate directions:

- `SshSystem`
- `RemoteSystem`
- `SshScript`

The exact name matters less than the principle: remote execution should not live only in one integration test helper if it is part of the testing strategy going forward.

### Cloud synchronization diagnostics

If we need to measure propagation timing, appearance, vanishing, content visibility, or remote file state, then these should be modeled as reusable diagnostic capabilities rather than embedded in one-off polling code scattered across tests.

## Decision Rule

Before adding a new helper, ask these questions:

1. Is this capability specific to one single test body only?
2. Would this be useful in another test, another project, or a support tool?
3. Does an existing RAIkeep abstraction already cover most of it?
4. If not, should the abstraction be improved so it does?

If the answers point to reuse, the implementation should move into the library layer.

## Immediate Implication For Current Work

This commitment applies directly to the new remote Google Drive test work.

The recently added `GoogleDriveRemoteProbe` in the OsLib tests is acceptable as a temporary spike, but it should not be treated as the final design.

Under this commitment, the next step should be to refactor the useful parts into reusable OsLib capabilities, especially where they currently duplicate or bypass existing concepts such as:

- process execution
- script execution
- remote command execution
- file visibility polling
- diagnostic reporting

## What This Commitment Is Not

This commitment does not mean:

- every tiny helper must move into the product library immediately
- tests can never use platform APIs directly
- abstraction growth should be uncontrolled

It means we should be deliberate, reuse-oriented, and consistent.

We should avoid solving the same problem twice in two different layers when one shared solution would make the system better.

## Review Standard

New test infrastructure should increasingly be reviewed against these questions:

- Does this duplicate an existing RAIkeep abstraction?
- If yes, why was the existing abstraction not used?
- If the abstraction was insufficient, should it be improved now?
- Will this helper likely be needed again?
- If yes, why is it not part of the reusable library surface?

## Working Agreement

Going forward, we will prefer:

- strengthening RAIkeep abstractions over bypassing them
- reusing RAIkeep abstractions over raw one-off code
- moving durable capabilities into libraries over leaving them trapped in tests
- letting tests dogfood the product libraries wherever practical

That is the commitment.