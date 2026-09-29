# RAIkeep Manifesto

## Purpose

`RAIkeep` is the coordinated home of small libraries and command-line tools for
durable structured data, filesystem boundaries, images, and diagrams.

Its role is not to erase package boundaries. Its role is to make integration work, architectural alignment, and real-world validation possible while each library remains independently owned and independently releasable.

## Why JSON matters for agentic engineering

Modern software is increasingly authored and operated by mixed teams of people,
services, and agents. Those participants need a representation that can cross
language, process, machine, and model boundaries without hiding its meaning
inside one runtime or one vendor's database.

JSON and JSON5 are valuable in that environment because they are:

- readable by people and language models;
- directly consumable by tools in many programming languages;
- inspectable with ordinary editors, version-control tools, and shell commands;
- structurally expressive without requiring a generated client before the data
  can be understood;
- portable between local development, servers, cloud-synchronized storage, and
  archival media; and
- suitable for sparse change fragments, explicit tombstones, history, and
  point-in-time projection.

This does not mean that arbitrary JSON is automatically a sound data model.
RAIkeep adds conventions and APIs so identifiers, history, protected lifecycle
attributes, deletion, and persistence remain explicit. The document remains
inspectable, but callers should mutate it through the domain boundary rather
than through destructive read-modify-write replacement.

For agentic engineering this transparency is particularly important. An agent
can examine the same durable facts that an operator can inspect, propose a
sparse change instead of rewriting an entire record, and leave evidence that a
later person or agent can audit. Human readability is not decoration; it is a
control surface for accountability.

## Daemon-free, not coordination-free

JsonPit does not require a JsonPit-owned centralized database daemon. A
developer, application, or autonomous agent does not need to provision a
database server, distribute database credentials, maintain a connection pool,
or open a database service through a firewall. A configured directory on a
synchronized cloud drive is the shared persistence fabric.

This is a deliberately narrow meaning of **daemon-free**. OneDrive, Dropbox,
Google Drive, or iCloud still needs its own synchronization machinery when that
provider supplies the shared transport. JsonPit does not replace or secretly
embed that machinery. It coordinates above it through ordinary, inspectable
files and cloud-safe filesystem operations.

Daemon-free also does not mean coordination-free. Each participating process
joins the protocol through:

- a canonical `.pit` snapshot;
- append-only change fragments and cleanup receipts;
- an opportunistic `Master.flag` writer lease;
- PID-specific process activity windows; and
- immutable operational events.

The master is a temporary responsibility held by one participating process,
not a separately deployed leader service. Other processes can continue to
publish durable change fragments, and delayed fragments remain eligible for
deterministic merge after synchronization resumes.

Process lifecycle therefore matters. A long-running application or agent
should normally keep one shared `Pit` open for its lifetime and dispose it
cleanly at shutdown. A finite CLI invocation should publish its durability
boundary and release its own PID-specific activity flag when it exits normally.
A crashed process may leave evidence behind for timeout-based recovery and
explicit maintenance; a finalizer must not attempt filesystem recovery work.

This architecture removes a central database daemon, not operational
responsibility. Storage health, provider synchronization, graceful shutdown,
audit, and maintenance remain visible parts of the system contract.

## Asynchronous persistence with eventual durability

JsonPit's persistence model is **asynchronous persistence with eventual
durability**. The phrase describes a precise contract:

1. A process accepts and represents a change in its live in-memory `Pit`.
2. A persistence boundary publishes a coherent snapshot or durable change
   fragment without requiring every remote observer to be current first.
3. Cloud or shared-storage propagation may deliver that durable evidence to
   other machines later and out of order.
4. Readers merge validated history deterministically. Repeated observation of
   the same fragment is idempotent; delayed valid history is not discarded
   merely because it arrived late.
5. Given functioning storage, propagation, and subsequent maintenance/save
   opportunities, the participating copies converge on durable history.

The word **asynchronous** means that a successful local operation does not
promise immediate visibility on every machine. The word **durability** means
more than eventual observation: accepted changes are carried across explicit
durability boundaries and are not intentionally forgotten while convergence is
still pending.

This model intentionally does not promise:

- a distributed transaction spanning every machine;
- a global lock or an instantaneous cross-process snapshot;
- read-after-write visibility from an arbitrary remote observer;
- that a point-in-time export made today includes a fragment that has not yet
  propagated to the machine performing the export; or
- automatic repair of unavailable storage or unsupported external interference.

A point-in-time result therefore means: evaluate all history visible to this
process now at the requested historical cutoff. If a valid older fragment
arrives later, a later evaluation may know more about that historical moment.
That is honest temporal projection under asynchronously delivered evidence, not
a claim of globally complete historical knowledge.

The practical application pattern is:

- open one shared `Pit` for the application's lifetime;
- serve ordinary reads and writes from that in-memory model;
- submit sparse changes and tombstones instead of replacing projected items;
- call `Save()` or dispose cleanly at meaningful durability boundaries;
- allow change fragments, receipts, and the canonical file to perform their
  documented recovery and convergence roles; and
- use the .NET [`pits`](https://github.com/Burkhardt/PitSeeder) toolchain for
  audit and maintenance when operational evidence must be inspected or retained
  artifacts reconciled; Python developers and agents can use
  [`jpit`](https://pypi.org/project/jsonpit/) as the alternative JsonPit
  toolchain.

This is not the correct model for every workload. Choose a transactional
database when the domain requires synchronous distributed constraints or
immediate global consistency. Choose JsonPit where transparent history, modest
data volume, local responsiveness, portability, and convergent durability are
the more valuable properties.

The detailed engineering contracts live in:

- [Python `jsonpit` on PyPI](https://pypi.org/project/jsonpit/)
- [JsonPit Getting Started](https://github.com/Burkhardt/JsonPit/blob/main/GettingStarted.md#persistence-model-asynchronous-persistence-with-eventual-durability)
- [CR003 — concurrency contract and persistence races](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR003_RAI_to_RAIkeep_JsonPit-concurrency-contract-and-persistence-races.md)
- [Live split-master recovery](https://github.com/Burkhardt/RAIkeep/blob/main/doc/JsonPit-CONCEPT-Live-Split-Master-Recovery.md)
- [`.NET pits audit` operational manual](https://github.com/Burkhardt/RAIkeep/blob/main/doc/PITS-AUDIT.md),
  with [`jpit`](https://pypi.org/project/jsonpit/) as the Python avenue for
  developers and agents
- [Cloud-storage in-place invariant](https://github.com/Burkhardt/RAIkeep/blob/main/doc/Cloud-Storage-In-Place-Invariant.md)

## Agreements

### Package independence

Each package keeps its own identity, release flow, and internal responsibility.

The umbrella workspace is for coordinated work, not for collapsing the libraries into a single indistinguishable codebase.

### Real tests must be real

If a test claims to validate cloud behavior, it must run against an actual cloud-backed location on the machine that executes the test.

Sandboxed, redirected, or synthetic setups are valid for mechanics tests, but they must be named honestly and kept separate from real-environment cloud tests.

### Deterministic test behavior

Unit-style tests should leave the file system as they found it.

Randomized file and directory names are not the default testing strategy. Deterministic reusable paths with explicit cleanup are preferred.

### Configuration over environment

Library setup should be driven by `OsConfigFile`-based configuration.

Environment variables are not the configuration model. They may exist as legacy compatibility inputs or for narrowly defined system-resolution fallbacks, but they are not the desired source of truth.

For real cloud tests in particular, explicit configuration must win and environment-variable-based discovery must be ignored.

### Stable config location

The shared configuration location is:

`~/.config/RAIkeep.json5`

[`amafu init`](https://github.com/Burkhardt/Amafu) detects supported cloud-drive
mounts and creates this shared configuration for RAIkeep tools and libraries.
Amafu owns bootstrap discovery; consumers read the generated configuration but
do not silently invoke Amafu, rediscover providers, or rewrite the file.

Resolution of `~` is accepted. The use of environment variables to choose different config locations is not the intended direction.

### Save, not Persist

Configuration writes should use `Save()`.

Legacy `Persist()` APIs are considered obsolete compatibility wrappers and should be retired from active use.

### Honest naming

Names must describe reality.

If a test exercises configuration mechanics, probing rules, path normalization, or fallback logic, it should be named as such.

If a test is named for cloud behavior, it should validate cloud behavior on a real provider-backed path.

## Engineering direction

The direction of the codebase is toward:

- explicit configuration instead of implicit machine-state discovery
- deterministic tests instead of randomized temp layouts
- real integration tests instead of simulated claims
- small reusable libraries with clear boundaries
- documentation that reflects actual behavior rather than aspiration

## Working rule

When there is tension between convenience and truth, choose truth.

When there is tension between legacy behavior and architectural clarity, move toward clarity in small safe steps.
