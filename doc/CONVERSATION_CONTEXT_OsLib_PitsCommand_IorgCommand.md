# Conversation Context: OsLib `PitsCommand` and `IorgCommand`

## Provenance

This note exports the relevant context available in the current Codex task
history. It was not recovered from a repository document or a persistent Codex
memory file. No corresponding memory file is known to exist.

The excerpts below are preserved to explain the statement that RAI and Codex
had **discussed** possible `PitsCommand` and `IorgCommand` wrappers without
turning that discussion into an approved CR or an implementation commitment.

## Relevant conversation excerpts

### 1. RAI raised the common system-command abstraction

RAI wrote:

> Yes. Let's do this. And also: let's test with the real plantuml cli, not with
> a pruned one, ok?
> RaiUtils should have all we need to wrap a system call to plantuml ... or
> where do we have it? All the tools we use, magick being one, pits, iorg
> potentially, certainly plantuml for generating svg from puml ... all those
> should have a system call kind of class. What do you suggest where we put
> those ... or do we have them already?
> If we have please tell me where they are. If not, tell me where you would put
> them. If we are putting them in RaiUtils, I would be willing to make RaiUtils
> depending on OsLib, RaiImage and RaiDiagram ... hoping that neither RaiImage
> nor RaiDiagram are currently depending on RaiUtils.

This asked for architectural analysis and explicitly mentioned `pits` and
`iorg` as potential members of a shared command abstraction.

### 2. The earlier Codex response proposed a later discussion

The next RAI message quoted the relevant Codex response as follows:

> For 4.2.2 we can discuss moving the two tool-neutral command adapters from
> RaiImage down to OsLib and adding PitsCommand/IorgCommand there. For this task
> I’ll use the existing real production chain: PlantUmlDiagramRenderer →
> RaiImage.PlantUmlCommand → OsLib.CliCommand → RaiSystem

This was a proposal to **discuss** adding the wrappers. It did not say that they
had been implemented or approved for CR010.

### 3. RAI followed up on whether OsLib was the appropriate package

RAI then wrote:

> Are you saying the pits and iorg cli calls could be placed inside OsLib?
> Because they do not depend on any other library ... only on being installed
> on that system as a tool... which is always necessary for any tool anyways?
> Are we using the term tool or CliTool anywhere in OsLib?

This continued the architectural discussion but did not contain a direction to
implement the wrappers, acceptance criteria, or release authorization.

## What the available context establishes

- A common CLI-tool abstraction for `magick`, PlantUML, `pits`, and `iorg` was
  discussed.
- OsLib was identified as a possible home because it already owns
  `CliCommand` and `RaiSystem`.
- `PitsCommand` and `IorgCommand` were proposed names.
- The proposal was deferred to a later discussion while CR010 continued using
  the existing PlantUML production chain.

## What the available context does not establish

- No CR in the repository requests `PitsCommand` or `IorgCommand`.
- No acceptance of a specific public API or package placement is recorded.
- No instruction to implement these wrappers for 4.2.2 is recorded.
- No 4.2.2 release note claims that the wrappers exist.

At the time this conversation-context export was requested, the accurate status
was therefore: **discussed and still undecided, not approved or implemented**.

## Subsequent resolution

RAI subsequently approved the capability for RAIkeep 4.2.2 and clarified that
the required verification boundary is the wrapper contract—not duplicated
PitSeeder or ImgSeeder product testing. The accepted scope is recorded in
[`CR014_RAI_to_RAIkeep_Typed_CLI_Command_Wrappers.md`](https://github.com/Burkhardt/RAIkeep/blob/main/doc/CR014_RAI_to_RAIkeep_Typed_CLI_Command_Wrappers.md).

That later decision supersedes the historical status above without changing
the provenance of the earlier conversation excerpts.
