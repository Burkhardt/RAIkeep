#!/usr/bin/env bash
set -euo pipefail

# Exercise release sequencing without Git, package builds, or publication.
source "$(dirname "${BASH_SOURCE[0]}")/release-chain.sh"

events=()
record() { events+=("$1"); }
setup_release_python() { RELEASE_PYTHON="$(command -v true)"; }
require_cmd() { :; }
log() { :; }
preflight_umbrella() { record preflight; }
preflight_submodule() { :; }
preflight_python_submodule() { :; }
assert_prepared_submodule_pointer() { :; }
assert_published_submodule_tag() { :; }
require_package_published() { :; }
hold_and_check_flatcontainer() { :; }
release_submodule() { record "$1"; }
release_python_package() { record JsonPit.Python; }
release_raiguard() { record RaiGuard; }
verify_parent_pointers_unchanged() { record pointers; }
final_visibility_summary() { record visibility; }
release_umbrella() { record umbrella; }

check_order() {
	local mode="$1" expected="$2" actual
	events=()
	VER=4.5.13
	MODE="$mode"
	PYPI_TOKEN=test main "$VER" "$MODE"
	actual="${events[*]}"
	if [[ "$actual" != "$expected" ]]; then
		printf 'Unexpected order for %s:\n  expected: %s\n  actual:   %s\n' "${mode:-normal}" "$expected" "$actual" >&2
		exit 1
	fi
}

check_order '' 'preflight Amafu OsLib RaiUtils RaiImage RaiDiagram RaidSeeder JsonPit JsonPit.Python ImgSeeder PitSeeder RaiGuard pointers visibility umbrella'
check_order '--resume-after-amafu' 'preflight OsLib RaiUtils RaiImage RaiDiagram RaidSeeder JsonPit JsonPit.Python ImgSeeder PitSeeder RaiGuard pointers visibility umbrella'
check_order '--resume-after-oslib' 'preflight RaiUtils RaiImage RaiDiagram RaidSeeder JsonPit JsonPit.Python ImgSeeder PitSeeder RaiGuard pointers visibility umbrella'
check_order '--resume-after-raiimage' 'preflight RaiDiagram RaidSeeder JsonPit JsonPit.Python ImgSeeder PitSeeder RaiGuard pointers visibility umbrella'
check_order '--resume-after-raidiagram' 'preflight RaidSeeder JsonPit JsonPit.Python ImgSeeder PitSeeder RaiGuard pointers visibility umbrella'
check_order '--resume-after-raiguard' 'preflight pointers visibility umbrella'

printf 'Release order checks passed.\n'
