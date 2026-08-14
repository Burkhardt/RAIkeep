#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPOSITORIES=(. OsLib RaiUtils RaiImage RaiDiagram JsonPit ImgSeeder PitSeeder)
PATTERN='\[[^]\n]+\]\((?!<?(?:https?://|mailto:|#|/))<?[^)\n>]+\.md(?:#[^)\n>]*)?>?\)'
failed=0

for repository in "${REPOSITORIES[@]}"; do
  repository_dir="$ROOT_DIR/$repository"
  [[ -d "$repository_dir" ]] || {
    echo "Missing repository: $repository_dir" >&2
    failed=1
    continue
  }

  matches="$({
    git -C "$repository_dir" ls-files -z '*.md' \
      | xargs -0 rg -n --pcre2 "$PATTERN" -- 2>/dev/null
  } || true)"

  if [[ -n "$matches" ]]; then
    echo "Relative Markdown document links in $repository:" >&2
    echo "$matches" >&2
    failed=1
  fi
done

if [[ "$failed" != "0" ]]; then
  exit 1
fi

echo "All tracked Markdown document links use absolute destinations."
