#!/usr/bin/env bash
set -euo pipefail

# Sequential release orchestrator for RAIkeep submodules and PitSeeder publish.
# This script assumes each repo's release changes are already prepared locally.
# It enforces order, workflow success waits, 5-minute hold windows, and NuGet
# flat-container visibility checks.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VER="${1:-}"

if [[ -z "$VER" ]]; then
  echo "Usage: $(basename "$0") <version>"
  echo "Example: $(basename "$0") 3.8.15"
  exit 1
fi

TAG="v${VER}"
MIN_HOLD_SECONDS=300

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Missing required command: $1" >&2
    exit 1
  }
}

log() {
  printf '[%s] %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*"
}

die() {
  echo "ERROR: $*" >&2
  exit 1
}

confirm() {
  local prompt="$1"
  read -r -p "$prompt [y/N]: " ans
  [[ "$ans" == "y" || "$ans" == "Y" ]]
}

csproj_version() {
  local repo_dir="$1"
  local csproj_rel="$2"
  perl -ne 'if (/<Version>([^<]+)<\/Version>/) { print "$1\n"; exit }' "$repo_dir/$csproj_rel"
}

assert_clean() {
  local repo_dir="$1"
  local name="$2"
  if [[ -n "$(git -C "$repo_dir" status --porcelain)" ]]; then
    die "$name has uncommitted changes. Commit/stash first: $repo_dir"
  fi
}

checkout_sync_main() {
  local repo_dir="$1"
  local name="$2"

  git -C "$repo_dir" fetch origin --prune

  if [[ "$(git -C "$repo_dir" branch --show-current)" != "main" ]]; then
    git -C "$repo_dir" checkout main
  fi

  git -C "$repo_dir" pull --ff-only origin main
}

push_main_if_needed() {
  local repo_dir="$1"
  local name="$2"
  local ahead
  ahead="$(git -C "$repo_dir" rev-list --left-right --count origin/main...HEAD | awk '{print $2}')"
  if [[ "$ahead" != "0" ]]; then
    log "$name: pushing main ($ahead commit(s) ahead)"
    git -C "$repo_dir" push origin main
  fi
}

ensure_tag_on_head() {
  local repo_dir="$1"
  local name="$2"
  local tag="$3"

  local head_sha remote_tag_sha
  head_sha="$(git -C "$repo_dir" rev-parse HEAD)"
  remote_tag_sha="$(git -C "$repo_dir" ls-remote --tags origin "refs/tags/$tag" | awk '{print $1}')"

  if [[ -z "$remote_tag_sha" ]]; then
    log "$name: creating and pushing tag $tag"
    git -C "$repo_dir" tag "$tag"
    git -C "$repo_dir" push origin "refs/tags/$tag"
    return
  fi

  if [[ "$remote_tag_sha" == "$head_sha" ]]; then
    log "$name: remote tag $tag already points to HEAD"
    return
  fi

  die "$name: remote tag $tag exists at $remote_tag_sha, but HEAD is $head_sha. Refusing to retag."
}

wait_workflow_success() {
  local repo_dir="$1"
  local workflow_file="$2"
  local tag="$3"

  local run_id status conclusion
  run_id=""

  for _ in $(seq 1 180); do
    run_id="$(gh -R "$(git -C "$repo_dir" remote get-url origin)" run list --workflow "$workflow_file" --limit 100 \
      --json databaseId,headBranch,createdAt \
      --jq "map(select(.headBranch==\"$tag\")) | sort_by(.createdAt) | reverse | .[0].databaseId")"
    if [[ -n "$run_id" && "$run_id" != "null" ]]; then
      break
    fi
    perl -e 'select undef,undef,undef,5;'
  done

  [[ -n "$run_id" && "$run_id" != "null" ]] || die "No workflow run found for $workflow_file @ $tag"

  log "Waiting for $workflow_file run $run_id"

  for _ in $(seq 1 360); do
    status="$(gh -R "$(git -C "$repo_dir" remote get-url origin)" run view "$run_id" --json status --jq '.status')"
    conclusion="$(gh -R "$(git -C "$repo_dir" remote get-url origin)" run view "$run_id" --json conclusion --jq '.conclusion')"

    if [[ "$status" == "completed" ]]; then
      if [[ "$conclusion" == "success" ]]; then
        gh -R "$(git -C "$repo_dir" remote get-url origin)" run view "$run_id" \
          --json databaseId,url,updatedAt,status,conclusion,displayTitle
        return
      fi
      gh -R "$(git -C "$repo_dir" remote get-url origin)" run view "$run_id" --log-failed | tail -n 200 || true
      die "Workflow failed: $workflow_file run $run_id"
    fi

    perl -e 'select undef,undef,undef,5;'
  done

  die "Timed out waiting for workflow: $workflow_file @ $tag"
}

hold_and_check_flatcontainer() {
  local package_id="$1"
  local version="$2"

  local start_e now_e elapsed code ts
  start_e="$(date -u +%s)"

  while true; do
    now_e="$(date -u +%s)"
    elapsed=$((now_e - start_e))
    ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    code="$(curl -s -o /dev/null -w "%{http_code}\n" "https://api.nuget.org/v3-flatcontainer/${package_id}/${version}/${package_id}.${version}.nupkg")"

    echo "$ts package=${package_id} elapsed=${elapsed}s code=${code}"

    if [[ $elapsed -ge $MIN_HOLD_SECONDS && "$code" == "200" ]]; then
      return
    fi

    perl -e 'select undef,undef,undef,10;'
  done
}

release_submodule() {
  local name="$1"
  local repo_rel="$2"
  local csproj_rel="$3"
  local package_id="$4"
  local workflow_file="$5"

  local repo_dir="$ROOT_DIR/$repo_rel"
  log "===== $name ($TAG) ====="

  assert_clean "$repo_dir" "$name"
  checkout_sync_main "$repo_dir" "$name"

  local current_ver
  current_ver="$(csproj_version "$repo_dir" "$csproj_rel")"
  [[ "$current_ver" == "$VER" ]] || die "$name version mismatch in $csproj_rel (found $current_ver, expected $VER)"

  push_main_if_needed "$repo_dir" "$name"
  ensure_tag_on_head "$repo_dir" "$name" "$TAG"
  wait_workflow_success "$repo_dir" "$workflow_file" "$TAG"
  hold_and_check_flatcontainer "$package_id" "$VER"
}

release_pitseeder_via_parent_tag() {
  local pit_dir="$ROOT_DIR/PitSeeder"
  local parent_dir="$ROOT_DIR"

  log "===== PitSeeder ($TAG) ====="

  assert_clean "$pit_dir" "PitSeeder"
  checkout_sync_main "$pit_dir" "PitSeeder"

  local current_ver
  current_ver="$(csproj_version "$pit_dir" "pits/pits.csproj")"
  [[ "$current_ver" == "$VER" ]] || die "PitSeeder version mismatch in pits/pits.csproj (found $current_ver, expected $VER)"

  push_main_if_needed "$pit_dir" "PitSeeder"

  checkout_sync_main "$parent_dir" "RAIkeep"

  # Stage and commit only PitSeeder pointer if changed.
  if [[ -n "$(git -C "$parent_dir" status --porcelain -- PitSeeder)" ]]; then
    log "RAIkeep: committing PitSeeder pointer update"
    git -C "$parent_dir" add PitSeeder
    git -C "$parent_dir" commit -m "release: PitSeeder $VER"
  else
    log "RAIkeep: PitSeeder pointer already up to date"
  fi

  push_main_if_needed "$parent_dir" "RAIkeep"

  ensure_tag_on_head "$parent_dir" "RAIkeep" "$TAG"
  wait_workflow_success "$parent_dir" "publish-pitseeder-nuget.yml" "$TAG"
  hold_and_check_flatcontainer "pitseeder" "$VER"
}

finalize_parent_pointers() {
  local parent_dir="$ROOT_DIR"
  local changed

  changed="$(git -C "$parent_dir" status --porcelain -- OsLib RaiUtils RaiImage JsonPit || true)"

  if [[ -z "$changed" ]]; then
    log "RAIkeep: no OsLib/RaiUtils/RaiImage/JsonPit pointer changes to commit"
    return
  fi

  log "RAIkeep: committing final released submodule pointers"
  git -C "$parent_dir" add OsLib RaiUtils RaiImage JsonPit
  git -C "$parent_dir" commit -m "chore: sync released submodule pointers to $VER"
  git -C "$parent_dir" push origin main
}

final_visibility_summary() {
  log "===== Final flat-container checks ====="

  local check_url code
  check_url() {
    local pkg="$1"
    code="$(curl -s -o /dev/null -w "%{http_code}\n" "https://api.nuget.org/v3-flatcontainer/${pkg}/${VER}/${pkg}.${VER}.nupkg")"
    echo "$pkg $code"
  }

  check_url oslibcore
  check_url raiutils
  check_url raiimage
  check_url jsonpit
  check_url pitseeder
}

main() {
  require_cmd git
  require_cmd gh
  require_cmd curl
  require_cmd perl

  log "Release chain start for $VER"
  log "Order: OsLib -> RaiUtils -> RaiImage -> JsonPit -> PitSeeder"

  if ! confirm "Proceed with release chain for $VER?"; then
    echo "Aborted."
    exit 0
  fi

  release_submodule "OsLib" "OsLib" "OsLib.csproj" "oslibcore" "publish-nuget.yml"
  release_submodule "RaiUtils" "RaiUtils" "RaiUtils.csproj" "raiutils" "publish-nuget.yml"
  release_submodule "RaiImage" "RaiImage" "RaiImage.csproj" "raiimage" "publish-nuget.yml"
  release_submodule "JsonPit" "JsonPit" "JsonPit.csproj" "jsonpit" "publish-nuget.yml"

  release_pitseeder_via_parent_tag

  finalize_parent_pointers
  final_visibility_summary

  log "Release chain completed for $VER"
}

main "$@"
