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
assert_published_submodule_tag() { prerequisite_tags+=("$1"); }
require_package_published() { prerequisite_packages+=("$1"); }
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
	prerequisite_tags=()
	prerequisite_packages=()
	VER=4.5.13
	MODE="$mode"
	PYPI_TOKEN=test main "$VER" "$MODE"
	actual="${events[*]}"
	if [[ "$actual" != "$expected" ]]; then
		printf 'Unexpected order for %s:\n  expected: %s\n  actual:   %s\n' "${mode:-normal}" "$expected" "$actual" >&2
		exit 1
	fi
	if [[ "$mode" == "--resume-after-raiutils" ]]; then
		[[ "${prerequisite_tags[*]}" == 'Amafu OsLib RaiUtils' ]]
		[[ "${prerequisite_packages[*]}" == 'amafu oslibcore raiutils' ]]
	fi
}

check_order '' 'preflight Amafu OsLib RaiUtils RaiImage RaiDiagram RaidSeeder JsonPit JsonPit.Python ImgSeeder PitSeeder RaiGuard pointers visibility umbrella'
check_order '--resume-after-amafu' 'preflight OsLib RaiUtils RaiImage RaiDiagram RaidSeeder JsonPit JsonPit.Python ImgSeeder PitSeeder RaiGuard pointers visibility umbrella'
check_order '--resume-after-oslib' 'preflight RaiUtils RaiImage RaiDiagram RaidSeeder JsonPit JsonPit.Python ImgSeeder PitSeeder RaiGuard pointers visibility umbrella'
check_order '--resume-after-raiutils' 'preflight RaiImage RaiDiagram RaidSeeder JsonPit JsonPit.Python ImgSeeder PitSeeder RaiGuard pointers visibility umbrella'
check_order '--resume-after-raiimage' 'preflight RaiDiagram RaidSeeder JsonPit JsonPit.Python ImgSeeder PitSeeder RaiGuard pointers visibility umbrella'
check_order '--resume-after-raidiagram' 'preflight RaidSeeder JsonPit JsonPit.Python ImgSeeder PitSeeder RaiGuard pointers visibility umbrella'
check_order '--resume-after-raiguard' 'preflight pointers visibility umbrella'

# PyPI visibility must include the companion package, not only the core wheel.
probe_log="$(mktemp)"
trap 'rm -f "$probe_log"' EXIT

# Recovery must not publish anything when RaiUtils is unavailable or its tag mismatches.
for failed_prerequisite in package tag; do
	: > "$probe_log"
	if (
		require_package_published() {
			if [[ "$failed_prerequisite" == package && "$1" == raiutils ]]; then die 'Simulated unavailable RaiUtils'; fi
		}
		assert_published_submodule_tag() {
			if [[ "$failed_prerequisite" == tag && "$1" == RaiUtils ]]; then die 'Simulated mismatched RaiUtils tag'; fi
		}
		release_submodule() { printf '%s\n' "$1" >> "$probe_log"; }
		VER=4.5.17
		MODE=--resume-after-raiutils
		PYPI_TOKEN=test main "$VER" "$MODE"
	) >/dev/null 2>&1; then
		echo "Recovery accepted a failed $failed_prerequisite prerequisite." >&2
		exit 1
	fi
	[[ ! -s "$probe_log" ]]
done

release_http_code() { printf '%s\n' "$1" >> "$probe_log"; printf '200\n'; }
hold_and_check_pypi >/dev/null
grep -Fq '/pypi/jsonpit/4.5.13/json' "$probe_log"
grep -Fq '/pypi/jpit/4.5.13/json' "$probe_log"

printf 'Release order checks passed.\n'
