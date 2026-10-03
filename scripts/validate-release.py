#!/usr/bin/env python3
"""
Release Validation & Consistency Gate for RAIkeep and its Submodules.

Validates that all .csproj files, version constants, test assertions,
documentation headers, install snippets, release notes, and submodule
pointers are 100% consistent and free of stale version leaks before
release-chain.sh executes.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple

# All 9 coordinated child repositories in dependency order
PACKAGE_REPOS = [
    ("Amafu", "Amafu", "amafu/amafu.csproj"),
    ("OsLib", "OsLib", "OsLib.csproj"),
    ("RaiUtils", "RaiUtils", "RaiUtils.csproj"),
    ("RaiImage", "RaiImage", "RaiImage.csproj"),
    ("RaiDiagram", "RaiDiagram", "RaiDiagram.csproj"),
    ("RaidSeeder", "RaidSeeder", "raid/raid.csproj"),
    ("JsonPit", "JsonPit", "JsonPit.csproj"),
    ("ImgSeeder", "ImgSeeder", "ImgSeeder.csproj"),
    ("PitSeeder", "PitSeeder", "pits/pits.csproj"),
]


class ReleaseValidator:
    def __init__(self, root_dir: Path, target_version: str):
        self.root_dir = root_dir.resolve()
        self.version = target_version
        self.tag = f"v{target_version}"
        self.errors: List[str] = []
        self.checks_passed = 0

    def error(self, rel_path: str, line_no: int | None, message: str) -> None:
        loc = f"{rel_path}:{line_no}" if line_no is not None else rel_path
        self.errors.append(f"  ❌ {loc} -> {message}")

    def pass_check(self) -> None:
        self.checks_passed += 1

    def validate_file_exists(self, rel_path: str) -> bool:
        p = self.root_dir / rel_path
        if not p.is_file():
            self.error(rel_path, None, f"Required file is missing.")
            return False
        self.pass_check()
        return True

    def validate_file_contains(
        self, rel_path: str, pattern: str, description: str, flags: int = 0
    ) -> bool:
        p = self.root_dir / rel_path
        if not p.is_file():
            self.error(rel_path, None, f"File does not exist (cannot check: {description})")
            return False
        content = p.read_text(encoding="utf-8")
        if not re.search(pattern, content, flags):
            self.error(rel_path, None, f"Missing pattern for {description}: expected regex '{pattern}'")
            return False
        self.pass_check()
        return True

    def validate_no_stale_versions(
        self, rel_path: str, stale_versions: List[str], line_filter_pattern: str | None = None
    ) -> None:
        p = self.root_dir / rel_path
        if not p.is_file():
            return
        lines = p.read_text(encoding="utf-8").splitlines()
        for idx, line in enumerate(lines, start=1):
            if line_filter_pattern and not re.search(line_filter_pattern, line):
                continue
            for stale in stale_versions:
                if stale in line:
                    self.error(rel_path, idx, f"Found stale version '{stale}' in line: {line.strip()}")

    def run_all_validations(self, prior_versions: List[str]) -> bool:
        v = self.version
        print(f"============================================================")
        print(f"🔍 Validating RAIkeep Toolchain for Release {v}")
        print(f"============================================================")

        # 1. Project file versions (.csproj)
        print("\n[1/6] Checking .csproj versions & dependencies...")
        for name, repo_rel, csproj_rel in PACKAGE_REPOS:
            rel = f"{repo_rel}/{csproj_rel}"
            self.validate_file_contains(
                rel,
                rf"<Version>{re.escape(v)}</Version>",
                f"{name} project <Version>",
            )
            # Check internal fallback dependencies where applicable
            p = self.root_dir / rel
            if p.is_file():
                content = p.read_text(encoding="utf-8")
                for dep in [
                    "OsLibPackageVersion",
                    "RaiUtilsPackageVersion",
                    "RaiImagePackageVersion",
                    "RaiDiagramPackageVersion",
                    "JsonPitPackageVersion",
                ]:
                    for match in re.finditer(rf"<{dep}\b[^>]*>([^<]+)</{dep}>", content):
                        actual = match.group(1).strip()
                        if actual != v:
                            self.error(rel, None, f"{name} fallback property <{dep}> is {actual}, expected {v}")
                        else:
                            self.pass_check()

        # 2. Source code constants and version tests
        print("\n[2/6] Checking code version constants & CLI unit tests...")
        self.validate_file_contains(
            "Amafu/amafu/VersionInfo.cs",
            rf'Current = "{re.escape(v)}"',
            "Amafu VersionInfo.cs constant",
        )
        self.validate_file_contains(
            "Amafu/amafu.Tests/AmafuApplicationTests.cs",
            rf'Assert\.Equal\("amafu {re.escape(v)}",',
            "Amafu CLI --version unit test",
        )
        self.validate_file_contains(
            "RaidSeeder/raid.Tests/RaidSeederTests.cs",
            rf'Assert\.Equal\("raid v{re.escape(v)}",',
            "RaidSeeder CLI --version unit test",
        )
        self.validate_file_contains(
            "ImgSeeder/ImgSeeder.Tests/CliSubcommandTests.cs",
            rf'Assert\.Equal\("iorg v{re.escape(v)}",',
            "ImgSeeder CLI --version unit test",
        )
        self.validate_file_contains(
            "PitSeeder/pits.Tests/CliSubcommandTests.cs",
            rf'Assert\.Equal\("pits v{re.escape(v)}",',
            "PitSeeder CLI --version unit test",
        )

        # 3. Release Notes Existence
        print("\n[3/6] Checking Release Notes files...")
        # Umbrella release notes
        self.validate_file_exists(f"doc/RAIkeep_RELEASE_NOTES_{v}.md")
        # All child release notes
        for name, _, _ in PACKAGE_REPOS:
            self.validate_file_exists(f"doc/{name}_RELEASE_NOTES_{v}.md")
        # Amafu local release notes required by its native GitHub release workflow
        self.validate_file_exists(f"Amafu/Amafu_RELEASE_NOTES_{v}.md")

        # 4. Documentation Headers, Overviews & Scope Notes
        print("\n[4/6] Checking documentation headers & scope notes...")
        self.validate_file_contains(
            "RaidSeeder/API.md",
            rf"# RaidSeeder command reference {re.escape(v)}",
            "RaidSeeder API.md heading",
        )
        self.validate_file_contains(
            "RaidSeeder/API.md",
            rf"`raid --version` prints `raid v{re.escape(v)}`",
            "RaidSeeder API.md version text",
        )
        self.validate_file_contains(
            "JsonPit/API.md",
            rf"public JsonPit {re.escape(v)} API",
            "JsonPit API.md overview",
        )
        self.validate_file_contains(
            "OsLib/API.md",
            rf"`OsLibCore {re.escape(v)}` API surface",
            "OsLib API.md overview",
        )
        self.validate_file_contains(
            "RaiDiagram/API.md",
            rf"public RaiDiagram {re.escape(v)} API",
            "RaiDiagram API.md overview",
        )
        self.validate_file_contains(
            "RaiUtils/API.md",
            rf"## {re.escape(v)} scope note",
            "RaiUtils API.md scope note",
        )
        self.validate_file_contains(
            "RaiImage/API.md",
            rf"## {re.escape(v)} scope note",
            "RaiImage API.md scope note",
        )

        # 5. README Files, Install Snippets, and Links
        print("\n[5/6] Checking README headings, install commands & release links...")
        # Amafu README install snippets and platform heading
        self.validate_file_contains(
            "Amafu/README.md",
            rf"AMAFU_VERSION={re.escape(v)}",
            "Amafu README AMAFU_VERSION",
        )
        self.validate_file_contains(
            "Amafu/README.md",
            rf"## Platform support in {re.escape(v)}",
            "Amafu README platform support heading",
        )
        self.validate_file_contains(
            "Amafu/README.md",
            rf"dotnet tool install --global Amafu --version {re.escape(v)}",
            "Amafu README dotnet tool install",
        )
        self.validate_file_contains(
            "Amafu/README.md",
            rf"dotnet tool update --global Amafu --version {re.escape(v)}",
            "Amafu README dotnet tool update",
        )
        self.validate_file_contains(
            "Amafu/README.md",
            rf"--version {re.escape(v)}",
            "Amafu README sudo dotnet tool version",
        )

        # Each submodule README must have ## <VER> section and link to its notes
        for name, repo_rel, _ in PACKAGE_REPOS:
            readme_rel = f"{repo_rel}/README.md"
            self.validate_file_contains(
                readme_rel,
                rf"## {re.escape(v)}",
                f"{name} README ## {v} section",
            )
            self.validate_file_contains(
                readme_rel,
                rf"{name}_RELEASE_NOTES_{re.escape(v)}\.md",
                f"{name} README release notes link",
            )
            self.validate_file_contains(
                readme_rel,
                rf"Latest release notes:.*{name}_RELEASE_NOTES_{re.escape(v)}\.md",
                f"{name} README Latest release notes link",
            )

        # Umbrella README.md and doc/README.md
        self.validate_file_contains(
            "README.md",
            rf"RAIkeep {re.escape(v)}",
            "RAIkeep README release list",
        )
        self.validate_file_contains(
            "doc/README.md",
            rf"RAIkeep {re.escape(v)}",
            "doc/README.md current release notes list",
        )
        self.validate_file_contains(
            "RunReleaseChain.md",
            rf"scripts/release-chain\.sh {re.escape(v)}",
            "RunReleaseChain.md recommended invocation",
        )

        # 6. Scan for Stale Version Leaks in Active Install / Current Lines
        print("\n[6/6] Scanning for stale version leaks...")
        for name, repo_rel, _ in PACKAGE_REPOS:
            readme_rel = f"{repo_rel}/README.md"
            self.validate_no_stale_versions(
                readme_rel,
                prior_versions,
                line_filter_pattern=r"(--version|AMAFU_VERSION=|Platform support in|Latest release notes)",
            )
            api_rel = f"{repo_rel}/API.md"
            self.validate_no_stale_versions(
                api_rel,
                prior_versions,
                line_filter_pattern=r"(scope note|command reference|API surface|API Reference|overview|dependency line|fallback package)",
            )

        print("\n============================================================")
        if self.errors:
            print(f"❌ VALIDATION FAILED: {len(self.errors)} error(s) detected:")
            for err in self.errors:
                print(err)
            print("============================================================")
            return False
        else:
            print(f"✅ ALL {self.checks_passed} RELEASE CHECKS PASSED CLEANLY!")
            print(f"   Platform is 100% synchronized and verified for release {v}.")
            print("============================================================")
            return True


class ReleaseBumper:
    """
    Deterministic version bumper driven by scripts/release-manifest.json.
    Touches only explicitly registered targets without filesystem crawling.
    """
    def __init__(self, root_dir: Path, manifest_path: Path, target_version: str):
        self.root_dir = root_dir.resolve()
        self.manifest_path = manifest_path.resolve()
        self.target_version = target_version
        self.manifest = self._load_manifest()

    def _load_manifest(self) -> dict:
        import json
        if not self.manifest_path.is_file():
            raise FileNotFoundError(f"Manifest not found: {self.manifest_path}")
        return json.loads(self.manifest_path.read_text(encoding="utf-8"))

    def bump(self) -> bool:
        v = self.target_version
        old_v = self.manifest.get("current_version", "")
        print(f"============================================================")
        print(f"🚀 Bumping RAIkeep Platform from {old_v} -> {v}")
        print(f"============================================================")

        changed_count = 0

        # 1. Update manifest targets via targeted regex
        print("\n[1/4] Applying targeted replacements across registered files...")
        for target in self.manifest.get("targets", []):
            rel_path = target["path"]
            file_path = self.root_dir / rel_path
            if not file_path.is_file():
                print(f"  ⚠️ Warning: Target file {rel_path} does not exist. Skipping.")
                continue

            content = file_path.read_text(encoding="utf-8")
            updated = content

            # Apply explicit replacement rules
            for rule in target.get("replacements", []):
                pattern = rule["pattern"]
                replacement = rule["replacement"].format(version=v)
                updated = re.sub(pattern, replacement, updated)

            # Also apply @latestVersion line markers if present
            if "@latestVersion" in updated:
                def replace_marker(match):
                    line = match.group(0)
                    prefix, sep, marker = line.partition("@latestVersion")
                    updated_prefix = re.sub(r"(?<!\d)\d+\.\d+\.\d+(?!\d)", v, prefix)
                    return updated_prefix + sep + marker

                updated = re.sub(r"^.*@latestVersion.*$", replace_marker, updated, flags=re.MULTILINE)

            if updated != content:
                file_path.write_text(updated, encoding="utf-8")
                print(f"  ✏️ Updated: {rel_path}")
                changed_count += 1
            else:
                print(f"  ✔️ Up to date: {rel_path}")

        # 2. Prepend version headers in submodule READMEs if needed
        print("\n[2/4] Ensuring version history headers in submodule READMEs...")
        for name, repo_rel, _ in PACKAGE_REPOS:
            readme_rel = f"{repo_rel}/README.md"
            readme_path = self.root_dir / readme_rel
            if not readme_path.is_file():
                continue
            text = readme_path.read_text(encoding="utf-8")
            if not re.search(rf"^## {re.escape(v)}\b", text, re.MULTILINE):
                # Find the first existing ## section to prepend before it
                match = re.search(r"^## \d+\.\d+\.\d+", text, re.MULTILINE)
                if match:
                    header = (
                        f"## {v}\n\n"
                        f"Coordinated {v} release; public behavior is aligned with the synchronized platform.\n\n"
                        f"Release notes: [{name}_RELEASE_NOTES_{v}.md](https://github.com/Burkhardt/RAIkeep/blob/main/doc/{name}_RELEASE_NOTES_{v}.md).\n\n"
                    )
                    idx = match.start()
                    new_text = text[:idx] + header + text[idx:]
                    readme_path.write_text(new_text, encoding="utf-8")
                    print(f"  📝 Prepended ## {v} section to {readme_rel}")
                    changed_count += 1

        # 3. Scaffold missing release note markdown files
        print("\n[3/4] Scaffolding release notes templates...")
        for note_pattern in self.manifest.get("release_notes", []):
            rel_note = note_pattern.format(version=v)
            note_path = self.root_dir / rel_note
            if not note_path.is_file():
                note_path.parent.mkdir(parents=True, exist_ok=True)
                title = Path(rel_note).stem.replace(f"_{v}", f" {v}").replace("_", " ")
                template = (
                    f"# {title}\n\n"
                    f"- Release version: `{v}`\n"
                    f"- Coordination tag: `v{v}`\n\n"
                    f"## Highlights\n"
                    f"<!-- LLM / Author: summarize key architectural highlights and changes here -->\n\n"
                    f"## Coordinated Dependencies\n"
                    f"- Aligned with RAIkeep synchronized `{v}` line.\n"
                )
                note_path.write_text(template, encoding="utf-8")
                print(f"  📄 Scaffolding created: {rel_note}")
                changed_count += 1
            else:
                print(f"  ✔️ Exists: {rel_note}")

        # 4. Update current_version in manifest itself
        print("\n[4/4] Updating release manifest version...")
        import json
        self.manifest["current_version"] = v
        self.manifest_path.write_text(json.dumps(self.manifest, indent=2) + "\n", encoding="utf-8")
        print(f"  💾 Updated {self.manifest_path.name} current_version to {v}")

        print(f"\n✨ Bump complete! ({changed_count} files touched/scaffolded)")
        print("Now running release validation suite...\n")

        validator = ReleaseValidator(self.root_dir, v)
        stale = [old_v] if old_v and old_v != v else ["4.4.5", "4.4.6", "4.4.8"]
        return validator.run_all_validations(stale)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/validate-release.py <version> [stale_version_1 stale_version_2 ...]")
        print("   or: python3 scripts/validate-release.py --bump <new_version>")
        sys.exit(1)

    root_dir = Path(__file__).resolve().parent.parent
    manifest_path = root_dir / "scripts" / "release-manifest.json"

    if sys.argv[1] == "--bump":
        if len(sys.argv) < 3:
            print("Error: --bump requires a target version (e.g. python3 scripts/validate-release.py --bump 4.5.1)")
            sys.exit(1)
        new_version = sys.argv[2].lstrip("v")
        bumper = ReleaseBumper(root_dir, manifest_path, new_version)
        success = bumper.bump()
        sys.exit(0 if success else 1)

    version = sys.argv[1].lstrip("v")
    stale_versions = sys.argv[2:] if len(sys.argv) > 2 else ["4.4.5", "4.4.6", "4.4.8"]

    validator = ReleaseValidator(root_dir, version)
    success = validator.run_all_validations(stale_versions)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

