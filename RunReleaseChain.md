# Prep work

As preprocessing, 
first commit all changes in all subprojects with meaningful messages.
Then, find the next release number available across all 6 projects and change the csproj file's version number accordingly - all with one number (i.e. v3.11.1).
Then check all md files that need update and also all puml files that need updates so that both forms of documentation reflect the current code.

# How to run next time:

<code>cd /Users/rsb/Project2026/GitHub/RAIkeep
scripts/release-chain.sh 3.11.1</code>

The enforced package order is:

- `OsLibCore`
- `RaiUtils`
- `RaiImage`
- `JsonPit`
- `ImgSeeder`
- `PitSeeder`

The chain keeps the 300-second wait between published packages and verifies package visibility through the NuGet flat-container `.nupkg` URL.

Do not run this as part of version-prep work unless publication is explicitly requested.

## About running inside the LLM:

```
Yes, this can be run within this chat workflow by asking me to execute it.
I am using GPT-5.3-Codex.
The exact model tier selection such as Medium is controlled by your Copilot/session configuration, not by the shell script itself.
```
