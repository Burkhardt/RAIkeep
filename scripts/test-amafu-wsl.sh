#!/usr/bin/env bash
set -euo pipefail

# Builds the current checkout, leaving the observer's installed tools unchanged.
# The observer and its cloud paths are resolved through Os.Config and Amafu.
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
scratch="$(mktemp -d "${TMPDIR:-/tmp}/raikeep-amafu-wsl.XXXXXXXX")"
trap 'rm -rf -- "$scratch"' EXIT

dotnet publish "$root/Amafu/amafu/amafu.csproj" --configuration Release \
  --runtime linux-x64 --self-contained false -p:PublishAot=false -p:UseAppHost=false \
  --output "$scratch/publish"

RAIKEEP_AMAFU_WSL_PUBLISH="$scratch/publish" \
RAIKEEP_WSL_OBSERVER="${1:-Themba}" \
dotnet test "$root/tests/Amafu.Observer.Tests/Amafu.Observer.Tests.csproj" \
  --logger 'console;verbosity=detailed'
