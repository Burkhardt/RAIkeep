#!/usr/bin/env bash
set -euo pipefail

# Read-only guard tests; no package builds, network calls, or publication.
source "$(dirname "${BASH_SOURCE[0]}")/release-chain.sh"
fixture_dir="$(mktemp -d "${TMPDIR:-/tmp}/tracked-package-preflight.XXXXXX")"
trap 'rm -rf "$fixture_dir"' EXIT
git -C "$fixture_dir" init -q
printf '*.nupkg\n*.snupkg\n' > "$fixture_dir/.gitignore"
mkdir "$fixture_dir/artifacts"
printf legacy > "$fixture_dir/artifacts/RaiUtilsCore.2.3.1.nupkg"

# Ignored local build outputs are not part of an Actions checkout.
assert_no_tracked_packages "$fixture_dir" fixture
git -C "$fixture_dir" add -f artifacts/RaiUtilsCore.2.3.1.nupkg
if (assert_no_tracked_packages "$fixture_dir" fixture) >/dev/null 2>&1; then
	echo 'Preflight accepted a tracked legacy NuGet package.' >&2
	exit 1
fi
git -C "$fixture_dir" rm --cached -q artifacts/RaiUtilsCore.2.3.1.nupkg
printf symbols > "$fixture_dir/artifacts/RaiUtilsCore.2.3.1.snupkg"
git -C "$fixture_dir" add -f artifacts/RaiUtilsCore.2.3.1.snupkg
if (assert_no_tracked_packages "$fixture_dir" fixture) >/dev/null 2>&1; then
	echo 'Preflight accepted a tracked symbol package.' >&2
	exit 1
fi
git -C "$fixture_dir" rm --cached -q artifacts/RaiUtilsCore.2.3.1.snupkg
assert_no_tracked_packages "$fixture_dir" fixture
printf 'Tracked-package preflight checks passed.\n'
