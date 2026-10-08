#!/usr/bin/env bash
set -euo pipefail

# Sequential release orchestrator for the RAIkeep umbrella and submodules.
# This script assumes each repo's release changes are already prepared locally.
# It enforces strict dependency order and waits until NuGet exposes both the
# exact package and registration document before the next package begins.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VER="${1:-}"
MODE="${2:-}"
# NuGet package repositories, in dependency order. JsonPit.Python joins the
# coordinated release separately because it builds and publishes a PyPI wheel.
PACKAGE_REPOS=(Amafu OsLib RaiUtils RaiImage RaiDiagram RaidSeeder JsonPit ImgSeeder PitSeeder)
PYTHON_REPO="JsonPit.Python"
PYTHON_PACKAGE="jsonpit"

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

setup_release_python() {
	local venv_dir="$HOME/.venvs/raikeep-release"
	local module
	[[ -f "$venv_dir/pyvenv.cfg" ]] || die "Release virtual environment is missing or invalid: $venv_dir. Create it with Python 3.12 or newer: python3 -m venv \"$venv_dir\""
	RELEASE_PYTHON="$venv_dir/bin/python3"
	[[ -x "$RELEASE_PYTHON" ]] || die "Release Python is missing or not executable: $RELEASE_PYTHON. Recreate $venv_dir on this machine."

	# Child Python commands in validate-release.py must use this environment too.
	# These changes apply only to this script and its children, not the caller.
	export VIRTUAL_ENV="$venv_dir"
	export PATH="$venv_dir/bin:$PATH"
	unset PYTHONHOME
	"$RELEASE_PYTHON" -c 'import sys; sys.exit(0 if sys.prefix != sys.base_prefix and sys.version_info >= (3, 12) else 1)' >/dev/null 2>&1 \
		|| die "Release Python cannot run as a Python 3.12+ virtual environment: $RELEASE_PYTHON. Recreate $venv_dir on this machine."
	for module in pytest build twine; do
		"$RELEASE_PYTHON" -c "import $module" >/dev/null 2>&1 \
			|| die "Python module '$module' is missing or cannot be imported in $venv_dir. Install release tools with: \"$RELEASE_PYTHON\" -m pip install --upgrade pip pytest build twine"
	done
	log "Using release Python: $RELEASE_PYTHON"
}

csproj_version() {
	local repo_dir="$1"
	local csproj_rel="$2"
	sed -n 's:.*<Version>\([^<]*\)</Version>.*:\1:p' "$repo_dir/$csproj_rel" | head -n 1
}

python_project_version() {
	local repo_dir="$1"
	sed -n 's/^version[[:space:]]*=[[:space:]]*"\([^"]*\)"/\1/p' "$repo_dir/pyproject.toml" | head -n 1
}

latest_remote_tag() {
	local repo_dir="$1"
	git -C "$repo_dir" ls-remote --tags origin 'v[0-9]*.[0-9]*.[0-9]*' \
		| awk -F'/' '{print $NF}' \
		| sed 's/\^{}//' \
		| sort -Vu \
		| tail -1
}

derive_next_patch_version() {
	local common latest version major minor patch
	for repo in "${PACKAGE_REPOS[@]}"; do
		latest="$(latest_remote_tag "$ROOT_DIR/$repo")"
		[[ -n "$latest" ]] || die "$repo has no remote vX.Y.Z tag"
		if [[ -z "${common:-}" ]]; then
			common="$latest"
		elif [[ "$latest" != "$common" ]]; then
			die "Remote tag mismatch: $repo latest is $latest, expected $common"
		fi
	done
	latest="$(latest_remote_tag "$ROOT_DIR/$PYTHON_REPO")"
	[[ -n "$latest" ]] || die "$PYTHON_REPO has no remote vX.Y.Z tag"
	[[ "$latest" == "$common" ]] || die "Remote tag mismatch: $PYTHON_REPO latest is $latest, expected $common"

	version="${common#v}"
	IFS=. read -r major minor patch <<<"$version"
	[[ "$major" =~ ^[0-9]+$ && "$minor" =~ ^[0-9]+$ && "$patch" =~ ^[0-9]+$ ]] \
		|| die "Cannot parse latest remote tag: $common"
	echo "$major.$minor.$((patch + 1))"
}

assert_clean() {
	local repo_dir="$1"
	local name="$2"
	if [[ -n "$(git -C "$repo_dir" status --porcelain)" ]]; then
		die "$name has uncommitted changes. Commit/stash first: $repo_dir"
	fi
}

assert_tracked_clean() {
	local repo_dir="$1"
	local name="$2"
	if [[ -n "$(git -C "$repo_dir" status --porcelain --untracked-files=no)" ]]; then
		die "$name has uncommitted tracked changes. Commit them before starting the release chain."
	fi
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

	local head_sha remote_tag_sha local_tag_sha
	head_sha="$(git -C "$repo_dir" rev-parse HEAD)"
	remote_tag_sha="$(git -C "$repo_dir" ls-remote --tags origin "refs/tags/$tag" | awk '{print $1}')"
	local_tag_sha="$(git -C "$repo_dir" rev-parse -q --verify "refs/tags/$tag" 2>/dev/null || true)"

	if [[ -z "$remote_tag_sha" ]]; then
		if [[ -n "$local_tag_sha" && "$local_tag_sha" != "$head_sha" ]]; then
			die "$name: local tag $tag exists at $local_tag_sha, but HEAD is $head_sha. Refusing to retag."
		fi
		log "$name: creating and pushing tag $tag"
		if [[ -z "$local_tag_sha" ]]; then
			git -C "$repo_dir" tag -a "$tag" -m "$name $tag"
		fi
		git -C "$repo_dir" push origin "refs/tags/$tag"
		return
	fi

	if [[ "$remote_tag_sha" == "$head_sha" ]]; then
		log "$name: remote tag $tag already points to HEAD"
		return
	fi

	die "$name: remote tag $tag exists at $remote_tag_sha, but HEAD is $head_sha. Refusing to retag."
}

preflight_submodule() {
	local name="$1"
	local repo_rel="$2"
	local csproj_rel="$3"
	local repo_dir="$ROOT_DIR/$repo_rel"
	local branch current_ver recorded_sha head_sha behind ahead

	assert_clean "$repo_dir" "$name"
	branch="$(git -C "$repo_dir" branch --show-current)"
	[[ "$branch" == "main" ]] || die "$name must be on main, but is on '$branch'."

	git -C "$repo_dir" fetch origin --prune
	read -r behind ahead <<<"$(git -C "$repo_dir" rev-list --left-right --count origin/main...HEAD)"
	[[ "$behind" == "0" ]] || die "$name main is behind or diverged from origin/main. Synchronize it before release."

	current_ver="$(csproj_version "$repo_dir" "$csproj_rel")"
	[[ "$current_ver" == "$VER" ]] || die "$name version mismatch in $csproj_rel (found $current_ver, expected $VER)"

	recorded_sha="$(git -C "$ROOT_DIR" rev-parse "HEAD:$repo_rel")"
	head_sha="$(git -C "$repo_dir" rev-parse HEAD)"
	[[ "$recorded_sha" == "$head_sha" ]] || die "RAIkeep HEAD records $name at $recorded_sha, but its prepared HEAD is $head_sha. Commit the updated submodule pointer in RAIkeep first."

	log "$name: preflight passed at $head_sha ($ahead commit(s) ahead of origin/main)"
}

preflight_python_submodule() {
	local repo_dir="$ROOT_DIR/$PYTHON_REPO"
	local branch current_ver recorded_sha head_sha behind ahead

	assert_clean "$repo_dir" "$PYTHON_REPO"
	branch="$(git -C "$repo_dir" branch --show-current)"
	[[ "$branch" == "main" ]] || die "$PYTHON_REPO must be on main, but is on '$branch'."

	git -C "$repo_dir" fetch origin --prune
	read -r behind ahead <<<"$(git -C "$repo_dir" rev-list --left-right --count origin/main...HEAD)"
	[[ "$behind" == "0" ]] || die "$PYTHON_REPO main is behind or diverged from origin/main. Synchronize it before release."

	current_ver="$(python_project_version "$repo_dir")"
	[[ "$current_ver" == "$VER" ]] || die "$PYTHON_REPO version mismatch in pyproject.toml (found $current_ver, expected $VER)"

	recorded_sha="$(git -C "$ROOT_DIR" rev-parse "HEAD:$PYTHON_REPO")"
	head_sha="$(git -C "$repo_dir" rev-parse HEAD)"
	[[ "$recorded_sha" == "$head_sha" ]] || die "RAIkeep HEAD records $PYTHON_REPO at $recorded_sha, but its prepared HEAD is $head_sha. Commit the updated submodule pointer in RAIkeep first."

	log "$PYTHON_REPO: preflight passed at $head_sha ($ahead commit(s) ahead of origin/main)"
}

release_umbrella() {
	local branch behind ahead

	log "===== RAIkeep umbrella ($TAG) ====="
	assert_tracked_clean "$ROOT_DIR" "RAIkeep"
	branch="$(git -C "$ROOT_DIR" branch --show-current)"
	[[ "$branch" == "main" ]] || die "RAIkeep must be on main, but is on '$branch'."

	git -C "$ROOT_DIR" fetch origin --prune
	read -r behind ahead <<<"$(git -C "$ROOT_DIR" rev-list --left-right --count origin/main...HEAD)"
	[[ "$behind" == "0" ]] || die "RAIkeep main is behind or diverged from origin/main. Synchronize it before release."

	push_main_if_needed "$ROOT_DIR" "RAIkeep"
	ensure_tag_on_head "$ROOT_DIR" "RAIkeep" "$TAG"
	wait_workflow_success "$ROOT_DIR" "publish-release.yml" "$TAG"
	local release_title
	release_title="$(gh -R "$(git -C "$ROOT_DIR" remote get-url origin)" release view "$TAG" --json name --jq '.name')"
	[[ "$release_title" == "RAIkeep $TAG" ]] \
		|| die "RAIkeep GitHub Release title '$release_title' does not match 'RAIkeep $TAG'."
	log "RAIkeep: umbrella tag and GitHub Release $TAG are synchronized"
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
		sleep 5
	done

	[[ -n "$run_id" && "$run_id" != "null" ]] || die "No workflow run found for $workflow_file @ $tag"

	log "Waiting for $workflow_file run $run_id"

	for _ in $(seq 1 360); do
		status="$(gh -R "$(git -C "$repo_dir" remote get-url origin)" run view "$run_id" --json status --jq '.status')"
		conclusion="$(gh -R "$(git -C "$repo_dir" remote get-url origin)" run view "$run_id" --json conclusion --jq '.conclusion')"

		log "$workflow_file run $run_id status=${status:-unknown} conclusion=${conclusion:-unknown}"

		if [[ "$status" == "completed" ]]; then
			if [[ "$conclusion" == "success" ]]; then
				gh -R "$(git -C "$repo_dir" remote get-url origin)" run view "$run_id" \
					--json databaseId,url,updatedAt,status,conclusion,displayTitle
				return
			fi
			gh -R "$(git -C "$repo_dir" remote get-url origin)" run view "$run_id" --log-failed | tail -n 200 || true
			die "Workflow failed: $workflow_file run $run_id"
		fi

		sleep 5
	done

	die "Timed out waiting for workflow: $workflow_file @ $tag"
}

hold_and_check_flatcontainer() {
	local package_id="$1"
	local version="$2"

	local start_e now_e elapsed package_code registration_code ts
	local package_url registration_url
	package_url="https://api.nuget.org/v3-flatcontainer/${package_id}/${version}/${package_id}.${version}.nupkg"
	registration_url="https://api.nuget.org/v3/registration5-gz-semver2/${package_id}/${version}.json"
	start_e="$(date -u +%s)"

	while true; do
		now_e="$(date -u +%s)"
		elapsed=$((now_e - start_e))
		ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
		package_code="$(curl -sS -o /dev/null -w "%{http_code}\n" "$package_url")"
		registration_code="$(curl -sS -o /dev/null -w "%{http_code}\n" "$registration_url")"

		echo "$ts package=${package_id} elapsed=${elapsed}s nupkg=${package_code} registration=${registration_code}"

		if [[ "$package_code" == "200" && "$registration_code" == "200" ]]; then
			log "$package_id $version is available through NuGet package and registration endpoints"
			return
		fi

		sleep 10
	done
}

require_package_published() {
	local package_id="$1"
	local version="$2"
	local package_code registration_code

	package_code="$(curl -sS -o /dev/null -w "%{http_code}\n" \
		"https://api.nuget.org/v3-flatcontainer/${package_id}/${version}/${package_id}.${version}.nupkg")"
	registration_code="$(curl -sS -o /dev/null -w "%{http_code}\n" \
		"https://api.nuget.org/v3/registration5-gz-semver2/${package_id}/${version}.json")"
	log "Resume prerequisite: $package_id $version nupkg=$package_code registration=$registration_code"
	[[ "$package_code" == "200" && "$registration_code" == "200" ]] \
		|| die "Cannot resume: $package_id $version is not fully published."
}

assert_tagged_submodule_pointer() {
	local name="$1"
	local repo_rel="$2"
	local tagged_sha current_sha head_sha

	tagged_sha="$(git -C "$ROOT_DIR" rev-parse "$TAG:$repo_rel")"
	current_sha="$(git -C "$ROOT_DIR" rev-parse "HEAD:$repo_rel")"
	head_sha="$(git -C "$ROOT_DIR/$repo_rel" rev-parse HEAD)"
	[[ "$tagged_sha" == "$current_sha" && "$current_sha" == "$head_sha" ]] \
		|| die "$name does not match the immutable RAIkeep $TAG pointer (tag=$tagged_sha, main=$current_sha, checkout=$head_sha)."
	log "$name: checkout and current umbrella pointer match immutable $TAG at $head_sha"
}

release_submodule() {
	local name="$1"
	local repo_rel="$2"
	local csproj_rel="$3"
	local solution_rel="$4"
	local package_id="$5"
	local workflow_file="$6"

	local repo_dir="$ROOT_DIR/$repo_rel"
	local branch recorded_sha head_sha behind ahead
	log "===== $name ($TAG) ====="

	assert_clean "$repo_dir" "$name"
	branch="$(git -C "$repo_dir" branch --show-current)"
	[[ "$branch" == "main" ]] || die "$name moved off main after preflight."
	git -C "$repo_dir" fetch origin --prune
	read -r behind ahead <<<"$(git -C "$repo_dir" rev-list --left-right --count origin/main...HEAD)"
	[[ "$behind" == "0" ]] || die "$name origin/main advanced after preflight. Stop before tagging an unexpected state."
	recorded_sha="$(git -C "$ROOT_DIR" rev-parse "HEAD:$repo_rel")"
	head_sha="$(git -C "$repo_dir" rev-parse HEAD)"
	[[ "$recorded_sha" == "$head_sha" ]] || die "$name HEAD changed after the umbrella label was created."

	local current_ver
	current_ver="$(csproj_version "$repo_dir" "$csproj_rel")"
	[[ "$current_ver" == "$VER" ]] || die "$name version mismatch in $csproj_rel (found $current_ver, expected $VER)"

	# Validate the same package-only dependency graph used by the publish
	# workflow before creating the release tag. Local umbrella checkouts can
	# otherwise substitute project references and conceal stale package pins.
	log "$name: validating package-only restore"
	dotnet restore "$repo_dir/$solution_rel" /p:UseLocalRAIkeepSources=false

	push_main_if_needed "$repo_dir" "$name"
	ensure_tag_on_head "$repo_dir" "$name" "$TAG"
	wait_workflow_success "$repo_dir" "$workflow_file" "$TAG"
	hold_and_check_flatcontainer "$package_id" "$VER"
}

hold_and_check_pypi() {
	local start_e now_e elapsed code ts
	start_e="$(date -u +%s)"
	while true; do
		now_e="$(date -u +%s)"
		elapsed=$((now_e - start_e))
		ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
		code="$(curl -sS -o /dev/null -w "%{http_code}\n" "https://pypi.org/pypi/${PYTHON_PACKAGE}/${VER}/json")"
		echo "$ts package=${PYTHON_PACKAGE} elapsed=${elapsed}s pypi=${code}"
		if [[ "$code" == "200" ]]; then
			log "$PYTHON_PACKAGE $VER is available from PyPI"
			return
		fi
		sleep 10
	done
}

release_python_package() {
	local repo_dir="$ROOT_DIR/$PYTHON_REPO"
	local branch recorded_sha head_sha behind ahead current_ver dist_dir
	local -a artifacts

	log "===== $PYTHON_REPO ($TAG) ====="
	assert_clean "$repo_dir" "$PYTHON_REPO"
	branch="$(git -C "$repo_dir" branch --show-current)"
	[[ "$branch" == "main" ]] || die "$PYTHON_REPO moved off main after preflight."
	git -C "$repo_dir" fetch origin --prune
	read -r behind ahead <<<"$(git -C "$repo_dir" rev-list --left-right --count origin/main...HEAD)"
	[[ "$behind" == "0" ]] || die "$PYTHON_REPO origin/main advanced after preflight. Stop before tagging an unexpected state."
	recorded_sha="$(git -C "$ROOT_DIR" rev-parse "HEAD:$PYTHON_REPO")"
	head_sha="$(git -C "$repo_dir" rev-parse HEAD)"
	[[ "$recorded_sha" == "$head_sha" ]] || die "$PYTHON_REPO HEAD changed after the umbrella label was created."
	current_ver="$(python_project_version "$repo_dir")"
	[[ "$current_ver" == "$VER" ]] || die "$PYTHON_REPO version mismatch in pyproject.toml (found $current_ver, expected $VER)"

	dist_dir="$(mktemp -d "${TMPDIR:-/tmp}/raikeep-${PYTHON_PACKAGE}-${VER}.XXXXXX")"
	log "$PYTHON_REPO: building source and wheel distributions"
	"$RELEASE_PYTHON" -m build --outdir "$dist_dir" "$repo_dir"
	artifacts=("$dist_dir/${PYTHON_PACKAGE}-${VER}"*)
	[[ -e "${artifacts[0]}" ]] || die "$PYTHON_REPO build did not produce ${PYTHON_PACKAGE}-${VER} artifacts."

	push_main_if_needed "$repo_dir" "$PYTHON_REPO"
	ensure_tag_on_head "$repo_dir" "$PYTHON_REPO" "$TAG"
	[[ -n "${PYPI_TOKEN:-}" ]] || die "PYPI_TOKEN is required to publish $PYTHON_PACKAGE $VER to PyPI."
	TWINE_USERNAME=__token__ TWINE_PASSWORD="$PYPI_TOKEN" \
		"$RELEASE_PYTHON" -m twine upload --non-interactive "${artifacts[@]}"
	hold_and_check_pypi
	rm -rf "$dist_dir"
}

verify_parent_pointers_unchanged() {
	local parent_dir="$ROOT_DIR"
	local changed

	changed="$(git -C "$parent_dir" status --porcelain --untracked-files=no -- Amafu OsLib RaiUtils RaiImage RaiDiagram RaidSeeder JsonPit JsonPit.Python ImgSeeder PitSeeder || true)"
	[[ -z "$changed" ]] || die "RAIkeep submodule pointers changed after umbrella label $TAG was created. Stop and investigate; the label must describe the exact released commits."
	log "RAIkeep: submodule pointers still match umbrella label $TAG"
}

final_visibility_summary() {
	log "===== Final package visibility checks ====="

	local check_url package_code registration_code
	check_url() {
		local pkg="$1"
		package_code="$(curl -sS -o /dev/null -w "%{http_code}\n" "https://api.nuget.org/v3-flatcontainer/${pkg}/${VER}/${pkg}.${VER}.nupkg")"
		registration_code="$(curl -sS -o /dev/null -w "%{http_code}\n" "https://api.nuget.org/v3/registration5-gz-semver2/${pkg}/${VER}.json")"
		echo "$pkg nupkg=$package_code registration=$registration_code"
		[[ "$package_code" == "200" && "$registration_code" == "200" ]] \
			|| die "$pkg $VER is not fully visible at the final release gate."
	}

	check_url amafu
	check_url oslibcore
	check_url raiutils
	check_url raiimage
	check_url raidiagram
	check_url raidseeder
	check_url jsonpit
	check_url imgseeder
	check_url pitseeder
	local pypi_code
	pypi_code="$(curl -sS -o /dev/null -w "%{http_code}\n" "https://pypi.org/pypi/${PYTHON_PACKAGE}/${VER}/json")"
	echo "$PYTHON_PACKAGE pypi=$pypi_code"
	[[ "$pypi_code" == "200" ]] || die "$PYTHON_PACKAGE $VER is not fully visible at the final release gate."
}

prepare_recovery() {
	local umbrella_behind

	assert_tracked_clean "$ROOT_DIR" "RAIkeep"
	[[ "$(git -C "$ROOT_DIR" branch --show-current)" == "main" ]] \
		|| die "RAIkeep must be on main for recovery."
	git -C "$ROOT_DIR" fetch origin --prune
	read -r umbrella_behind _ \
		<<<"$(git -C "$ROOT_DIR" rev-list --left-right --count origin/main...HEAD)"
	[[ "$umbrella_behind" == "0" ]] \
		|| die "RAIkeep main is behind or diverged from origin/main."
	git -C "$ROOT_DIR" rev-parse --verify "refs/tags/$TAG" >/dev/null \
		|| die "RAIkeep does not have the required immutable $TAG label."
	push_main_if_needed "$ROOT_DIR" "RAIkeep recovery"
}

resume_after_amafu() {
	log "Recovery mode: preserve existing $TAG labels and resume after Amafu"
	prepare_recovery

	log "Waiting for the recovered Amafu publication to become fully visible"
	hold_and_check_flatcontainer "amafu" "$VER"

	assert_tagged_submodule_pointer "OsLib" "OsLib"
	assert_tagged_submodule_pointer "RaiUtils" "RaiUtils"
	assert_tagged_submodule_pointer "RaiImage" "RaiImage"
	assert_tagged_submodule_pointer "RaiDiagram" "RaiDiagram"
	assert_tagged_submodule_pointer "RaidSeeder" "RaidSeeder"
	assert_tagged_submodule_pointer "JsonPit" "JsonPit"
	assert_tagged_submodule_pointer "$PYTHON_REPO" "$PYTHON_REPO"
	assert_tagged_submodule_pointer "ImgSeeder" "ImgSeeder"
	assert_tagged_submodule_pointer "PitSeeder" "PitSeeder"

	log "Preflighting the nine unpublished packages"
	preflight_submodule "OsLib" "OsLib" "OsLib.csproj"
	preflight_submodule "RaiUtils" "RaiUtils" "RaiUtils.csproj"
	preflight_submodule "RaiImage" "RaiImage" "RaiImage.csproj"
	preflight_submodule "RaiDiagram" "RaiDiagram" "RaiDiagram.csproj"
	preflight_submodule "RaidSeeder" "RaidSeeder" "raid/raid.csproj"
	preflight_submodule "JsonPit" "JsonPit" "JsonPit.csproj"
	preflight_python_submodule
	preflight_submodule "ImgSeeder" "ImgSeeder" "ImgSeeder.csproj"
	preflight_submodule "PitSeeder" "PitSeeder" "pits/pits.csproj"

	release_submodule "OsLib" "OsLib" "OsLib.csproj" "OsLib.slnx" "oslibcore" "publish-nuget.yml"
	release_submodule "RaiUtils" "RaiUtils" "RaiUtils.csproj" "RaiUtils.slnx" "raiutils" "publish-nuget.yml"
	release_submodule "RaiImage" "RaiImage" "RaiImage.csproj" "RaiImage.slnx" "raiimage" "publish-nuget.yml"
	release_submodule "RaiDiagram" "RaiDiagram" "RaiDiagram.csproj" "RaiDiagram.slnx" "raidiagram" "publish-nuget.yaml"
	release_submodule "RaidSeeder" "RaidSeeder" "raid/raid.csproj" "RaidSeeder.slnx" "raidseeder" "publish-nuget.yaml"
	release_submodule "JsonPit" "JsonPit" "JsonPit.csproj" "JsonPit.slnx" "jsonpit" "publish-nuget.yml"
	release_python_package
	release_submodule "ImgSeeder" "ImgSeeder" "ImgSeeder.csproj" "ImgSeeder.slnx" "imgseeder" "publish-nuget.yaml"
	release_submodule "PitSeeder" "PitSeeder" "pits/pits.csproj" "PitSeeder.slnx" "pitseeder" "publish-nuget.yaml"

	verify_parent_pointers_unchanged
	final_visibility_summary
	log "Release chain recovery completed for $VER"
}

resume_after_oslib() {
	log "Recovery mode: preserve existing $TAG labels and resume after OsLib"
	prepare_recovery

	require_package_published "amafu" "$VER"
	require_package_published "oslibcore" "$VER"

	assert_tagged_submodule_pointer "RaiUtils" "RaiUtils"
	assert_tagged_submodule_pointer "RaiImage" "RaiImage"
	assert_tagged_submodule_pointer "RaiDiagram" "RaiDiagram"
	assert_tagged_submodule_pointer "RaidSeeder" "RaidSeeder"
	assert_tagged_submodule_pointer "JsonPit" "JsonPit"
	assert_tagged_submodule_pointer "$PYTHON_REPO" "$PYTHON_REPO"
	assert_tagged_submodule_pointer "ImgSeeder" "ImgSeeder"
	assert_tagged_submodule_pointer "PitSeeder" "PitSeeder"

	log "Preflighting the eight unpublished packages"
	preflight_submodule "RaiUtils" "RaiUtils" "RaiUtils.csproj"
	preflight_submodule "RaiImage" "RaiImage" "RaiImage.csproj"
	preflight_submodule "RaiDiagram" "RaiDiagram" "RaiDiagram.csproj"
	preflight_submodule "RaidSeeder" "RaidSeeder" "raid/raid.csproj"
	preflight_submodule "JsonPit" "JsonPit" "JsonPit.csproj"
	preflight_python_submodule
	preflight_submodule "ImgSeeder" "ImgSeeder" "ImgSeeder.csproj"
	preflight_submodule "PitSeeder" "PitSeeder" "pits/pits.csproj"

	release_submodule "RaiUtils" "RaiUtils" "RaiUtils.csproj" "RaiUtils.slnx" "raiutils" "publish-nuget.yml"
	release_submodule "RaiImage" "RaiImage" "RaiImage.csproj" "RaiImage.slnx" "raiimage" "publish-nuget.yml"
	release_submodule "RaiDiagram" "RaiDiagram" "RaiDiagram.csproj" "RaiDiagram.slnx" "raidiagram" "publish-nuget.yaml"
	release_submodule "RaidSeeder" "RaidSeeder" "raid/raid.csproj" "RaidSeeder.slnx" "raidseeder" "publish-nuget.yaml"
	release_submodule "JsonPit" "JsonPit" "JsonPit.csproj" "JsonPit.slnx" "jsonpit" "publish-nuget.yml"
	release_python_package
	release_submodule "ImgSeeder" "ImgSeeder" "ImgSeeder.csproj" "ImgSeeder.slnx" "imgseeder" "publish-nuget.yaml"
	release_submodule "PitSeeder" "PitSeeder" "pits/pits.csproj" "PitSeeder.slnx" "pitseeder" "publish-nuget.yaml"

	verify_parent_pointers_unchanged
	final_visibility_summary
	log "Release chain recovery completed for $VER"
}

resume_after_raidiagram() {
	log "Recovery mode: preserve existing $TAG labels and resume after RaiDiagram"
	prepare_recovery

	require_package_published "amafu" "$VER"
	require_package_published "oslibcore" "$VER"
	require_package_published "raiutils" "$VER"
	require_package_published "raiimage" "$VER"
	log "Waiting for the recovered RaiDiagram publication to become fully visible"
	hold_and_check_flatcontainer "raidiagram" "$VER"

	assert_tagged_submodule_pointer "RaidSeeder" "RaidSeeder"
	assert_tagged_submodule_pointer "JsonPit" "JsonPit"
	assert_tagged_submodule_pointer "$PYTHON_REPO" "$PYTHON_REPO"
	assert_tagged_submodule_pointer "ImgSeeder" "ImgSeeder"
	assert_tagged_submodule_pointer "PitSeeder" "PitSeeder"

	log "Preflighting the five unpublished packages"
	preflight_submodule "RaidSeeder" "RaidSeeder" "raid/raid.csproj"
	preflight_submodule "JsonPit" "JsonPit" "JsonPit.csproj"
	preflight_python_submodule
	preflight_submodule "ImgSeeder" "ImgSeeder" "ImgSeeder.csproj"
	preflight_submodule "PitSeeder" "PitSeeder" "pits/pits.csproj"

	release_submodule "RaidSeeder" "RaidSeeder" "raid/raid.csproj" "RaidSeeder.slnx" "raidseeder" "publish-nuget.yaml"
	release_submodule "JsonPit" "JsonPit" "JsonPit.csproj" "JsonPit.slnx" "jsonpit" "publish-nuget.yml"
	release_python_package
	release_submodule "ImgSeeder" "ImgSeeder" "ImgSeeder.csproj" "ImgSeeder.slnx" "imgseeder" "publish-nuget.yaml"
	release_submodule "PitSeeder" "PitSeeder" "pits/pits.csproj" "PitSeeder.slnx" "pitseeder" "publish-nuget.yaml"

	assert_tagged_submodule_pointer "RaidSeeder" "RaidSeeder"
	assert_tagged_submodule_pointer "JsonPit" "JsonPit"
	assert_tagged_submodule_pointer "$PYTHON_REPO" "$PYTHON_REPO"
	assert_tagged_submodule_pointer "ImgSeeder" "ImgSeeder"
	assert_tagged_submodule_pointer "PitSeeder" "PitSeeder"
	final_visibility_summary
	log "Release chain recovery completed for $VER"
}

main() {
	setup_release_python
	require_cmd git
	require_cmd gh
	require_cmd curl
	require_cmd dotnet
	require_cmd sed
	require_cmd sleep
	require_cmd mktemp
	[[ -n "${PYPI_TOKEN:-}" ]] || die "PYPI_TOKEN is required for coordinated PyPI publication."

	[[ $# -le 2 ]] || die "Usage: scripts/release-chain.sh [version] [--resume-after-amafu|--resume-after-oslib|--resume-after-raidiagram]"
	if [[ -n "$MODE" && "$MODE" != "--resume-after-amafu" && "$MODE" != "--resume-after-oslib" && "$MODE" != "--resume-after-raidiagram" ]]; then
		die "Unknown release mode '$MODE'. Expected --resume-after-amafu, --resume-after-oslib, or --resume-after-raidiagram."
	fi
	if [[ -n "$MODE" && -z "$VER" ]]; then
		die "Recovery mode requires the interrupted release version."
	fi
	if [[ -z "$VER" ]]; then
		VER="$(derive_next_patch_version)"
	fi
	TAG="v${VER}"
	log "Executing automated release consistency validation for $VER..."
	"$RELEASE_PYTHON" "$ROOT_DIR/scripts/validate-release.py" "$VER" || die "Release validation failed. Correct errors before running release chain."
	if [[ "$MODE" == "--resume-after-amafu" ]]; then
		resume_after_amafu
		return
	elif [[ "$MODE" == "--resume-after-oslib" ]]; then
		resume_after_oslib
		return
	elif [[ "$MODE" == "--resume-after-raidiagram" ]]; then
		resume_after_raidiagram
		return
	fi

	log "Release chain start for $VER"
	log "Order: RAIkeep umbrella release -> Amafu -> OsLib -> RaiUtils -> RaiImage -> RaiDiagram -> RaidSeeder -> JsonPit -> JsonPit.Python -> ImgSeeder -> PitSeeder"

	log "Preflighting all ten packages before labeling RAIkeep"
	preflight_submodule "Amafu" "Amafu" "amafu/amafu.csproj"
	preflight_submodule "OsLib" "OsLib" "OsLib.csproj"
	preflight_submodule "RaiUtils" "RaiUtils" "RaiUtils.csproj"
	preflight_submodule "RaiImage" "RaiImage" "RaiImage.csproj"
	preflight_submodule "RaiDiagram" "RaiDiagram" "RaiDiagram.csproj"
	preflight_submodule "RaidSeeder" "RaidSeeder" "raid/raid.csproj"
	preflight_submodule "JsonPit" "JsonPit" "JsonPit.csproj"
	preflight_python_submodule
	preflight_submodule "ImgSeeder" "ImgSeeder" "ImgSeeder.csproj"
	preflight_submodule "PitSeeder" "PitSeeder" "pits/pits.csproj"

	release_umbrella

	release_submodule "Amafu" "Amafu" "amafu/amafu.csproj" "Amafu.slnx" "amafu" "publish-nuget.yaml"
	release_submodule "OsLib" "OsLib" "OsLib.csproj" "OsLib.slnx" "oslibcore" "publish-nuget.yml"
	release_submodule "RaiUtils" "RaiUtils" "RaiUtils.csproj" "RaiUtils.slnx" "raiutils" "publish-nuget.yml"
	release_submodule "RaiImage" "RaiImage" "RaiImage.csproj" "RaiImage.slnx" "raiimage" "publish-nuget.yml"
	release_submodule "RaiDiagram" "RaiDiagram" "RaiDiagram.csproj" "RaiDiagram.slnx" "raidiagram" "publish-nuget.yaml"
	release_submodule "RaidSeeder" "RaidSeeder" "raid/raid.csproj" "RaidSeeder.slnx" "raidseeder" "publish-nuget.yaml"
	release_submodule "JsonPit" "JsonPit" "JsonPit.csproj" "JsonPit.slnx" "jsonpit" "publish-nuget.yml"
	release_python_package
	release_submodule "ImgSeeder" "ImgSeeder" "ImgSeeder.csproj" "ImgSeeder.slnx" "imgseeder" "publish-nuget.yaml"
	release_submodule "PitSeeder" "PitSeeder" "pits/pits.csproj" "PitSeeder.slnx" "pitseeder" "publish-nuget.yaml"

	verify_parent_pointers_unchanged
	final_visibility_summary

	log "Release chain completed for $VER"
}

main "$@"
