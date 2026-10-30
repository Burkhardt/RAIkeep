#!/usr/bin/env bash
# Preview local builds only. Never installs tools or invokes a mutating verb.
set -euo pipefail
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
selected="${1:-all}"
case "$selected" in
  all) tools=(pits jpit iorg raid rail amafu) ;;
  pits|jpit|jsonpit|iorg|raid|rail|amafu) tools=("$selected") ;;
  *) printf 'Usage: %s [all|pits|jpit|jsonpit|iorg|raid|rail|amafu]\n' "$0" >&2; exit 2 ;;
esac
for tool in "${tools[@]}"; do
  printf '\n%s local help preview\n\n' "$tool"
  if [[ "$tool" == jpit || "$tool" == jsonpit ]]; then
    PYTHONPATH="$repo_root/JsonPit.Python${PYTHONPATH:+:$PYTHONPATH}" \
      "${PYTHON:-python3}" -m jsonpit.cli --help
    continue
  fi
  case "$tool" in
    pits) assembly=PitSeeder/pits/bin/Debug/net10.0/pits.dll ;;
    iorg) assembly=ImgSeeder/bin/Debug/net10.0/ImgSeeder.dll ;;
    raid) assembly=RaidSeeder/raid/bin/Debug/net10.0/raid.dll ;;
    rail) assembly=RaiGuard/rail/bin/Debug/net10.0/rail.dll ;;
    amafu) assembly=Amafu/amafu/bin/Debug/net10.0/amafu.dll ;;
  esac
  if [[ ! -f "$repo_root/$assembly" ]]; then
    printf 'Missing local build. Run dotnet build RAIkeep.slnx first.\n' >&2
    exit 1
  fi
  dotnet "$repo_root/$assembly" --help
done
