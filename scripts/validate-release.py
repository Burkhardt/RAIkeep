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
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List, Tuple

# All 10 coordinated .NET child repositories in dependency order
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
	("RaiGuard", "RaiGuard", "rail/rail.csproj"),
]

PYTHON_REPO = ("JsonPit.Python", "pyproject.toml")
CENTRAL_RELEASE_NOTES_ONLY = {"RaiGuard"}


def release_note_path(name: str, version: str) -> str:
	major = version.split(".", 1)[0]
	return f"doc/releases/v{major}.x/{name}_RELEASE_NOTES_{major}.x.md"


def release_note_anchor(version: str) -> str:
	return version.replace(".", "")


class ReleaseValidator:
	def __init__(
		self, root_dir: Path, target_version: str, *, run_external_checks: bool = True
	):
		self.root_dir = root_dir.resolve()
		self.version = target_version
		self.run_external_checks = run_external_checks
		self.tag = f"v{target_version}"
		self.errors: List[str] = []
		self.checks_passed = 0

	def error(self, rel_path: str, line_no: int | None, message: str) -> None:
		loc = f"{rel_path}:{line_no}" if line_no is not None else rel_path
		self.errors.append(f"  ❌ {loc} -> {message}")

	def pass_check(self) -> None:
		self.checks_passed += 1

	def validate_command(
		self,
		description: str,
		command: List[str],
		*,
		env: dict[str, str] | None = None,
	) -> bool:
		"""Runs a release gate command and reports its concise diagnostics."""
		try:
			result = subprocess.run(
				command,
				cwd=self.root_dir,
				env=env,
				text=True,
				capture_output=True,
				check=False,
			)
		except OSError as ex:
			self.error(description, None, f"Could not execute {' '.join(command)}: {ex}")
			return False
		if result.returncode == 0:
			self.pass_check()
			return True
		output = (result.stdout + result.stderr).strip().replace("\n", " ")
		self.error(description, None, f"Command failed ({result.returncode}): {output[-1000:]}")
		return False

	@staticmethod
	def normalize_parity_output(output: str) -> str:
		"""Normalizes only line endings for cross-runtime CLI parity."""
		return output.replace("\r\n", "\n").strip()

	@staticmethod
	def pits_parity_command() -> list[str]:
		"""Run the built CLI without rebuilding inside a temporary HOME."""
		return ["dotnet", "PitSeeder/pits/bin/Debug/net10.0/pits.dll"]

	def validate_cli_list_parity(self) -> None:
		"""Exercises the public local-root list --all contract of both CLIs."""
		with tempfile.TemporaryDirectory(prefix="raikeep-cli-parity-") as temporary:
			fixture = Path(temporary)
			home = fixture / "home"
			cloud_root = fixture / "cloud-root"
			temp_root = fixture / "temp"
			tenant = cloud_root / "Tenant"
			tenant.mkdir(parents=True)
			temp_root.mkdir()
			configuration = home / ".config" / "RAIkeep.json5"
			configuration.parent.mkdir(parents=True)
			configuration.write_text(
				"{\n"
				f'  TempDir: "{temp_root}",\n'
				'  DefaultCloudOrder: ["ParityCloud"],\n'
				f'  Cloud: {{ "ParityCloud": "{cloud_root}" }}\n'
				"}\n",
				encoding="utf-8",
			)
			source = Path(temporary) / "seed.json"
			source.write_text('[{"Id":"ParitySample"}]', encoding="utf-8")
			shared_env = os.environ.copy()
			shared_env["HOME"] = str(home)

			seed = self.validate_command(
				"pits local parity fixture seed",
				[*self.pits_parity_command(), "seed", "Activity", "--source", str(source), "-r", str(tenant), "-n"],
				env=shared_env,
			)
			if not seed:
				return

			csharp = subprocess.run(
				[*self.pits_parity_command(), "list", "-r", "Tenant", "--all", "-n"],
				cwd=self.root_dir,
				env=shared_env,
				text=True,
				capture_output=True,
				check=False,
			)
			python_env = shared_env.copy()
			python_env["PYTHONPATH"] = str(self.root_dir / "JsonPit.Python")
			python = subprocess.run(
				["python3", "-m", "jsonpit.cli", "list", "-r", "Tenant", "--all", "-n"],
				cwd=self.root_dir,
				env=python_env,
				text=True,
				capture_output=True,
				check=False,
			)
			if csharp.returncode != python.returncode:
				self.error(
					"pits/jpit list --all parity",
					None,
					f"exit codes differ: pits={csharp.returncode}, jpit={python.returncode}; "
					f"jpit: {(python.stdout + python.stderr).strip()[-500:]}",
				)
				return
			csharp_output = self.normalize_parity_output(csharp.stdout)
			python_output = self.normalize_parity_output(python.stdout)
			if csharp_output != python_output:
				self.error(
					"pits/jpit list --all parity",
					None,
					"formatted output differs: "
					f"pits={csharp_output!r}; jpit={python_output!r}",
				)
				return
			self.pass_check()

	def validate_cli_help_parity(self) -> None:
		"""Exercises the conditional WWWA help block of both public CLIs."""
		with tempfile.TemporaryDirectory(prefix="raikeep-help-parity-") as temporary:
			fixture = Path(temporary)
			home = fixture / "home"
			temp_root = fixture / "temp"
			tenant = fixture / "Tenant"
			tenant.mkdir()
			temp_root.mkdir()
			configuration = home / ".config" / "RAIkeep.json5"
			configuration.parent.mkdir(parents=True)
			configuration.write_text(
				"{\n"
				f'  TempDir: "{temp_root}",\n'
				"  Cloud: {}\n"
				"}\n",
				encoding="utf-8",
			)
			source = fixture / "seed.json"
			source.write_text('[{"Id":"ParitySample"}]', encoding="utf-8")
			shared_env = os.environ.copy()
			shared_env["HOME"] = str(home)
			shared_env["NO_COLOR"] = "1"
			python_env = shared_env.copy()
			python_env["PYTHONPATH"] = str(self.root_dir / "JsonPit.Python")

			seed = self.validate_command(
				"pits WWWA help parity fixture seed",
				[*self.pits_parity_command(), "seed", "Person", "--source", str(source), "-r", str(tenant), "-n"],
				env=shared_env,
			)
			if not seed:
				return

			def run_help(command: list[str], env: dict[str, str], description: str) -> str | None:
				try:
					result = subprocess.run(
						command,
						cwd=self.root_dir,
						env=env,
						text=True,
						capture_output=True,
						check=False,
					)
				except OSError as ex:
					self.error(description, None, f"Could not execute {' '.join(command)}: {ex}")
					return None
				if result.returncode != 0:
					self.error(description, None, f"Command failed ({result.returncode}): {(result.stdout + result.stderr).strip()[-1000:]}")
					return None
				return self.normalize_parity_output(result.stdout)

			pits = self.pits_parity_command()
			jpit = ["python3", "-m", "jsonpit.cli"]
			bare_csharp = run_help([*pits, "--help", "-n"], shared_env, "pits default help")
			bare_python = run_help([*jpit, "--help", "-n"], python_env, "jpit default help")
			contextual_csharp = run_help([*pits, "--help", "-r", str(tenant), "-n"], shared_env, "pits contextual WWWA help")
			contextual_python = run_help([*jpit, "--help", "-r", str(tenant), "-n"], python_env, "jpit contextual WWWA help")
			explicit_csharp = run_help([*pits, "--help", "--wwwa", "-n"], shared_env, "pits explicit WWWA help")
			explicit_python = run_help([*jpit, "--help", "--wwwa", "-n"], python_env, "jpit explicit WWWA help")
			if any(output is None for output in [bare_csharp, bare_python, contextual_csharp, contextual_python, explicit_csharp, explicit_python]):
				return

			quartet_files = [f"{name}.pit" for name in ("Person", "Object", "Place", "Activity")]
			if any(name in bare_csharp or name in bare_python for name in quartet_files):
				self.error("pits/jpit default help parity", None, "Default help must omit the WWWA status block.")
				return

			def status_lines(output: str) -> list[str]:
				return [line for line in output.split("\n") if line.startswith("\uea74 ") and ".pit" in line]

			contextual_csharp_lines = status_lines(contextual_csharp)
			contextual_python_lines = status_lines(contextual_python)
			explicit_csharp_lines = status_lines(explicit_csharp)
			explicit_python_lines = status_lines(explicit_python)
			if contextual_csharp_lines != contextual_python_lines:
				self.error("pits/jpit contextual WWWA help parity", None, f"status lines differ: pits={contextual_csharp_lines!r}; jpit={contextual_python_lines!r}")
				return
			if explicit_csharp_lines != explicit_python_lines:
				self.error("pits/jpit explicit WWWA help parity", None, f"status lines differ: pits={explicit_csharp_lines!r}; jpit={explicit_python_lines!r}")
				return
			if len(contextual_csharp_lines) != 4 or len(explicit_csharp_lines) != 4:
				self.error("pits/jpit WWWA help parity", None, "Expected exactly four WWWA status lines for contextual and explicit help.")
				return
			self.pass_check()

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
			self.error(
				rel_path, None, f"File does not exist (cannot check: {description})"
			)
			return False
		content = p.read_text(encoding="utf-8")
		if not re.search(pattern, content, flags):
			self.error(
				rel_path,
				None,
				f"Missing pattern for {description}: expected regex '{pattern}'",
			)
			return False
		self.pass_check()
		return True

	def validate_no_stale_versions(
		self,
		rel_path: str,
		stale_versions: List[str],
		line_filter_pattern: str | None = None,
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
					self.error(
						rel_path,
						idx,
						f"Found stale version '{stale}' in line: {line.strip()}",
					)

	def run_all_validations(self, prior_versions: List[str]) -> bool:
		v = self.version
		major = v.split(".", 1)[0]
		anchor = release_note_anchor(v)
		print(f"============================================================")
		print(f"🔍 Validating RAIkeep Toolchain for Release {v}")
		print(f"============================================================")

		# 1. Project file versions (.csproj and Python package metadata)
		print("\n[1/7] Checking package versions & dependencies...")
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
					for match in re.finditer(
						rf"<{dep}\b[^>]*>([^<]+)</{dep}>", content
					):
						actual = match.group(1).strip()
						if actual != v:
							self.error(
								rel,
								None,
								f"{name} fallback property <{dep}> is {actual}, expected {v}",
							)
						else:
							self.pass_check()
		self.validate_file_contains(
			f"{PYTHON_REPO[0]}/{PYTHON_REPO[1]}",
			rf'^version\s*=\s*"{re.escape(v)}"\s*$',
			"jsonpit Python project version",
			flags=re.MULTILINE,
		)
		self.validate_file_contains(
			f"{PYTHON_REPO[0]}/jsonpit/__init__.py",
			rf'^__version__\s*=\s*"{re.escape(v)}"\s*$',
			"jsonpit Python package __version__",
			flags=re.MULTILINE,
		)
		self.validate_file_contains(
			"RaiGuard/rail/rail.csproj",
			rf"<PackageReleaseNotes>Coordinated {re.escape(v)} release;",
			"RaiGuard CLI package release notes",
		)

		# 2. CLI version tests
		print("\n[2/7] Checking CLI unit tests...")
		self.validate_file_contains(
			"Amafu/amafu.Tests/AmafuApplicationTests.cs",
			rf'Assert\.Equal\("amafu v{re.escape(v)}",',
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

		# 3. Python tests and cross-runtime CLI discovery/help parity
		if self.run_external_checks:
			print("\n[3/7] Running Python tests and pits/jpit list/help parity...")
			pits_built = self.validate_command(
				"pits parity build",
				["dotnet", "build", "PitSeeder/pits/pits.csproj", "--no-restore", "--nologo", "-v", "minimal", "-m:1", "-nodeReuse:false"],
			)
			python_cmd = (
				["python3", "-m", "pytest", "JsonPit.Python/tests"]
				if subprocess.run(["python3", "-m", "pytest", "--version"], capture_output=True).returncode == 0
				else ["python3", "JsonPit.Python/tests/run_all.py"]
			)
			with tempfile.TemporaryDirectory(prefix="raikeep-python-tests-") as temporary:
				# Cross-engine tests invoke the installed pits CLI. Give it an isolated
				# valid configuration rather than depending on the user's HOME.
				home = Path(temporary) / "home"
				config = home / ".config" / "RAIkeep.json5"
				config.parent.mkdir(parents=True)
				cloud_root = Path(temporary) / "cloud"
				cloud_root.mkdir()
				config.write_text(
					json.dumps({"TempDir": str(Path(temporary) / "temp"),
						"DefaultCloudOrder": ["OneDrive"], "Cloud": {"OneDrive": str(cloud_root)}}),
					encoding="utf-8",
				)
				python_env = os.environ.copy()
				python_env["HOME"] = str(home)
				python_env["PYTHONPATH"] = str(self.root_dir / PYTHON_REPO[0])
				self.validate_command(
					"JsonPit.Python tests",
					python_cmd,
					env=python_env,
				)
			if pits_built:
				self.validate_cli_list_parity()
				self.validate_cli_help_parity()
		else:
			print("\n[3/7] Skipping external checks for isolated release-tool test.")

		# 4. Release Notes Existence
		print("\n[4/7] Checking Release Notes files...")
		for name in ["RAIkeep", *(package for package, _, _ in PACKAGE_REPOS)]:
			rel_path = release_note_path(name, v)
			if not self.validate_file_exists(rel_path):
				continue
			headings = re.findall(
				r"^## (\d+(?:\.\d+)+)$",
				(self.root_dir / rel_path).read_text(encoding="utf-8"),
				re.MULTILINE,
			)
			if headings and headings[0] == v and headings.count(v) == 1:
				self.pass_check()
			else:
				self.error(rel_path, None, f"Expected exactly one leading '## {v}' section; found {headings[:3]}.")
		legacy_notes = list((self.root_dir / "doc").glob("*_RELEASE_NOTES_[34].*.md"))
		if legacy_notes:
			self.error("doc", None, f"Flat 3.x/4.x release notes remain: {len(legacy_notes)} file(s).")
		else:
			self.pass_check()

		# 5. Documentation Headers, Overviews & Scope Notes
		print("\n[5/7] Checking documentation headers & scope notes...")
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

		# 6. README Files, Install Snippets, and Links
		print("\n[6/7] Checking README headings, install commands & release links...")
		# Amafu uses an explicit, product-named current-version heading and three
		# installer entry points. The script is the single executable install contract.
		self.validate_file_contains(
			"Amafu/README.md",
			rf"^## Amafu v{re.escape(v)}$",
			"Amafu README current-version heading",
			flags=re.MULTILINE,
		)
		for mode, privilege in (("native", "sudo "), ("global", ""), ("system", "sudo ")):
			self.validate_file_contains(
				"Amafu/README.md",
				rf"InstallAmafu\.sh \| {privilege}bash -s -- {mode} {re.escape(v)}",
				f"Amafu README {mode} installer command",
			)
		self.validate_file_contains(
			"Amafu/README.md",
			rf"Latest release notes:.*releases/v{major}\.x/Amafu_RELEASE_NOTES_{major}\.x\.md#{anchor}",
			"Amafu README Latest release notes link",
		)
		self.validate_file_contains(
			"Amafu/amafu/amafu.csproj",
			r'<None Include="\.\./README\.md" Pack="true"',
			"Amafu package uses the repository README",
		)
		amafu_readme = self.root_dir / "Amafu/README.md"
		if amafu_readme.is_file():
			if re.search(r"</?(?:details|summary)\b", amafu_readme.read_text(encoding="utf-8"), re.IGNORECASE):
				self.error("Amafu/README.md", None, "Amafu README contains collapsible HTML tags not supported by NuGet.")
			else:
				self.pass_check()
		self.validate_file_contains(
			"scripts/InstallAmafu.sh",
			rf'^DEFAULT_VERSION="{re.escape(v)}"$',
			"Amafu-only installer default version",
			flags=re.MULTILINE,
		)

		# Each package README identifies the current release once. Both the newer
		# "Latest Version" layout and legacy numeric headings remain valid while
		# READMEs are migrated.
		for name, repo_rel, _ in PACKAGE_REPOS:
			readme_rel = f"{repo_rel}/README.md"
			if name not in CENTRAL_RELEASE_NOTES_ONLY:
				heading_pattern = (
					rf"^## Amafu v{re.escape(v)}$"
					if name == "Amafu"
					else rf"^## (?:Latest Version )?{re.escape(v)}$"
				)
				self.validate_file_contains(
					readme_rel,
					heading_pattern,
					f"{name} README current-version heading",
					flags=re.MULTILINE,
				)
				self.validate_file_contains(
					readme_rel,
					rf"releases/v{major}\.x/{name}_RELEASE_NOTES_{major}\.x\.md#{anchor}",
					f"{name} README release notes link",
				)
				self.validate_file_contains(
					readme_rel,
					rf"Latest release notes:.*releases/v{major}\.x/{name}_RELEASE_NOTES_{major}\.x\.md#{anchor}",
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
		for name in ["RAIkeep", *(package for package, _, _ in PACKAGE_REPOS)]:
			label = "OsLibCore" if name == "OsLib" else name
			self.validate_file_contains(
				"doc/README.md",
				rf"(?m)^- \[{label} {re.escape(v)}\]\(https://github\.com/Burkhardt/RAIkeep/blob/main/{re.escape(release_note_path(name, v))}#{anchor}\)$",
				f"doc/README.md {name} release link",
			)
		self.validate_file_contains(
			"RunReleaseChain.md",
			rf"scripts/release-chain\.sh {re.escape(v)}",
			"RunReleaseChain.md recommended invocation",
		)

		# 7. Scan for Stale Version Leaks in Active Install / Current Lines
		print("\n[7/7] Scanning for stale version leaks...")
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

	def __init__(
		self,
		root_dir: Path,
		manifest_path: Path,
		target_version: str,
		*,
		run_external_checks: bool = True,
	):
		self.root_dir = root_dir.resolve()
		self.manifest_path = manifest_path.resolve()
		self.target_version = target_version
		self.run_external_checks = run_external_checks
		self.manifest = self._load_manifest()

	def _load_manifest(self) -> dict:
		import json

		if not self.manifest_path.is_file():
			raise FileNotFoundError(f"Manifest not found: {self.manifest_path}")
		return json.loads(self.manifest_path.read_text(encoding="utf-8"))

	@staticmethod
	def prepend_release_section(path: Path, version: str) -> bool:
		"""Add one new version at the top of a package's major-version history."""
		major = version.split(".", 1)[0]
		name = path.name.split("_RELEASE_NOTES_", 1)[0]
		section = (
			f"## {version}\n\n"
			f"- Release version: `{version}`\n"
			f"- Coordination tag: `v{version}`\n\n"
			"### Highlights\n"
			"<!-- LLM / Author: summarize key architectural highlights and changes here -->\n\n"
			"### Coordinated Dependencies\n"
			f"- Aligned with RAIkeep synchronized `{version}` line."
		)
		if not path.is_file():
			path.parent.mkdir(parents=True, exist_ok=True)
			path.write_text(f"# {name} Release Notes {major}.x\n\n{section}\n", encoding="utf-8")
			return True
		content = path.read_text(encoding="utf-8")
		if re.search(rf"^## {re.escape(version)}$", content, re.MULTILINE):
			return False
		header = re.match(r"(#[^\n]+\n)\n*", content)
		if not header:
			raise ValueError(f"Release history has no top-level heading: {path}")
		updated = content[:header.end()].rstrip() + "\n\n" + section + "\n\n---\n\n" + content[header.end():].lstrip()
		path.write_text(updated, encoding="utf-8")
		return True

	def bump(self) -> bool:
		v = self.target_version
		major = v.split(".", 1)[0]
		anchor = release_note_anchor(v)
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
				replacement = rule["replacement"].format(version=v, major=major, anchor=anchor)
				updated = re.sub(pattern, replacement, updated)

			# Also apply @latestVersion line markers if present
			if "@latestVersion" in updated:

				def replace_marker(match):
					line = match.group(0)
					prefix, sep, marker = line.partition("@latestVersion")
					updated_prefix = re.sub(r"(?<!\d)\d+\.\d+\.\d+(?!\d)", v, prefix)
					return updated_prefix + sep + marker

				updated = re.sub(
					r"^.*@latestVersion.*$", replace_marker, updated, flags=re.MULTILINE
				)

			if updated != content:
				file_path.write_text(updated, encoding="utf-8")
				print(f"  ✏️ Updated: {rel_path}")
				changed_count += 1
			else:
				print(f"  ✔️ Up to date: {rel_path}")

		# 2. Ensure each submodule README identifies the current release. Preserve a
		# concise Latest Version heading when a README has adopted that layout.
		print("\n[2/4] Ensuring current-version headers in submodule READMEs...")
		for name, repo_rel, _ in PACKAGE_REPOS:
			if name in CENTRAL_RELEASE_NOTES_ONLY:
				continue
			readme_rel = f"{repo_rel}/README.md"
			readme_path = self.root_dir / readme_rel
			if not readme_path.is_file():
				continue
			text = readme_path.read_text(encoding="utf-8")
			if name in {"OsLib", "RaiUtils", "RaiImage", "RaiDiagram", "JsonPit"}:
				# Option B keeps one current section. Keep its install snippets in
				# step with the coordinated package version.
				updated = re.sub(
					r"(dotnet add package \S+ --version )\d+\.\d+\.\d+",
					lambda match: match.group(1) + v,
					text,
				)
				updated = re.sub(
					r'(<PackageReference Include="[^"]+" Version=")\d+\.\d+\.\d+("\s*/>)',
					lambda match: match.group(1) + v + match.group(2),
					updated,
				)
				if updated != text:
					readme_path.write_text(updated, encoding="utf-8")
					print(f"  📝 Updated install version in {readme_rel}")
					changed_count += 1
					text = updated
			current_heading = (
				rf"^## Amafu v{re.escape(v)}$"
				if name == "Amafu"
				else rf"^## (?:Latest Version )?{re.escape(v)}$"
			)
			if re.search(current_heading, text, re.MULTILINE):
				continue

			if name == "Amafu":
				amafu_match = re.search(r"^## Amafu v\d+\.\d+\.\d+$", text, re.MULTILINE)
				if amafu_match:
					updated = text[:amafu_match.start()] + f"## Amafu v{v}" + text[amafu_match.end():]
					readme_path.write_text(updated, encoding="utf-8")
					print(f"  📝 Updated Amafu current-version header in {readme_rel}")
					changed_count += 1
					continue

			latest_match = re.search(r"^## Latest Version \d+\.\d+\.\d+$", text, re.MULTILINE)
			if latest_match:
				updated = text[:latest_match.start()] + f"## Latest Version {v}" + text[latest_match.end():]
				readme_path.write_text(updated, encoding="utf-8")
				print(f"  📝 Updated Latest Version header in {readme_rel}")
				changed_count += 1
				continue

			if name in {"OsLib", "RaiUtils", "RaiImage", "RaiDiagram", "JsonPit"} and "## Previous Versions" in text:
				match = re.search(r"^## \d+\.\d+\.\d+$", text, re.MULTILINE)
				if match and match.start() < text.index("## Previous Versions"):
					updated = text[:match.start()] + f"## {v}" + text[match.end():]
					updated = re.sub(
						r"Coordinated \d+\.\d+\.\d+ release; public behavior is aligned with the synchronized platform\.",
						f"Coordinated {v} release; public behavior is aligned with the synchronized platform.",
						updated,
						count=1,
					)
					readme_path.write_text(updated, encoding="utf-8")
					print(f"  📝 Updated current release section in {readme_rel}")
					changed_count += 1
					continue

			# Legacy READMEs retain their historical numeric heading layout.
			match = re.search(r"^## \d+\.\d+\.\d+", text, re.MULTILINE)
			if match:
				header = (
					f"## {v}\n\n"
					f"Coordinated {v} release; public behavior is aligned with the synchronized platform.\n\n"
					f"Latest release notes: [{name} {v} release notes](https://github.com/Burkhardt/RAIkeep/blob/main/{release_note_path(name, v)}#{anchor}).\n\n"
				)
				idx = match.start()
				readme_path.write_text(text[:idx] + header + text[idx:], encoding="utf-8")
				print(f"  📝 Prepended ## {v} section to {readme_rel}")
				changed_count += 1

		# RaiGuard keeps its release notes only in the umbrella, but its own
		# README still describes the current tool and analyzer packages.
		raiguard_readme = self.root_dir / "RaiGuard/README.md"
		if raiguard_readme.is_file():
			readme = raiguard_readme.read_text(encoding="utf-8")
			updated = re.sub(r"(?m)^## Latest Version \d+\.\d+\.\d+$", f"## Latest Version {v}", readme, count=1)
			updated = re.sub(
				r"Latest release notes: \[[^\]\n]+\]\([^)]+\)",
				f"Latest release notes: [RaiGuard {v} release notes](https://github.com/Burkhardt/RAIkeep/blob/main/{release_note_path('RaiGuard', v)}#{anchor})",
				updated,
				count=1,
			)
			updated = re.sub(
				r'(<PackageReference Include="RaiGuard\.Analyzer" Version=")\d+\.\d+\.\d+("\s*>)',
				lambda match: match.group(1) + v + match.group(2),
				updated,
			)
			if updated != readme:
				raiguard_readme.write_text(updated, encoding="utf-8")
				print("  📝 Updated RaiGuard/README.md current release")
				changed_count += 1

		# 3. Prepend one section to each major-version release history.
		print("\n[3/4] Updating consolidated release histories...")
		for note_pattern in self.manifest.get("release_notes", []):
			rel_note = note_pattern.format(version=v, major=major, anchor=anchor)
			note_path = self.root_dir / rel_note
			if self.prepend_release_section(note_path, v):
				print(f"  📝 Prepended {v}: {rel_note}")
				changed_count += 1
			else:
				print(f"  ✔️ Contains {v}: {rel_note}")

		index_path = self.root_dir / "doc/README.md"
		index = index_path.read_text(encoding="utf-8")
		updated_index = index
		for name in ["RAIkeep", *(package for package, _, _ in PACKAGE_REPOS)]:
			label = "OsLibCore" if name == "OsLib" else name
			link = (
				f"- [{label} {v}](https://github.com/Burkhardt/RAIkeep/blob/main/"
				f"{release_note_path(name, v)}#{anchor})"
			)
			updated_index = re.sub(
				rf"(?m)^- \[{label} \d+\.\d+\.\d+\]\([^)]+\)$",
				link,
				updated_index,
				count=1,
			)
		if updated_index != index:
			index_path.write_text(updated_index, encoding="utf-8")
		umbrella_readme_path = self.root_dir / "README.md"
		if umbrella_readme_path.is_file():
			u_readme = umbrella_readme_path.read_text(encoding="utf-8")
			updated_u = re.sub(
				r"(?m)^The prepared coordinated release is `\d+\.\d+\.\d+`\.",
				f"The prepared coordinated release is `{v}`.",
				u_readme,
				count=1,
			)
			for name in ["RAIkeep", *(package for package, _, _ in PACKAGE_REPOS)]:
				label = "OsLibCore" if name == "OsLib" else name
				link = (
					f"- [{label} {v}](https://github.com/Burkhardt/RAIkeep/blob/main/"
					f"{release_note_path(name, v)}#{anchor})"
				)
				updated_u = re.sub(
					rf"(?m)^- \[{label} \d+\.\d+\.\d+\]\([^)]+\)$",
					link,
					updated_u,
					count=1,
				)
			if updated_u != u_readme:
				umbrella_readme_path.write_text(updated_u, encoding="utf-8")
				print("  📝 Updated README.md current release links")
				changed_count += 1

		# 4. Update current_version in manifest itself
		print("\n[4/4] Updating release manifest version...")
		self.manifest["current_version"] = v
		manifest_content = self.manifest_path.read_text(encoding="utf-8")
		updated_manifest = re.sub(
			r'("current_version"\s*:\s*")[^"]+("\s*,)',
			rf"\g<1>{v}\g<2>",
			manifest_content,
			count=1,
		)
		if updated_manifest != manifest_content:
			self.manifest_path.write_text(updated_manifest, encoding="utf-8")
			print(f"  💾 Updated {self.manifest_path.name} current_version to {v}")
		else:
			print(f"  ✔️ {self.manifest_path.name} current_version is already {v}")

		print(f"\n✨ Bump complete! ({changed_count} files touched/scaffolded)")
		print("Now running release validation suite...\n")

		validator = ReleaseValidator(self.root_dir, v, run_external_checks=self.run_external_checks)
		stale = [old_v] if old_v and old_v != v else ["4.4.5", "4.4.6", "4.4.8"]
		return validator.run_all_validations(stale)


def main():
	if len(sys.argv) == 2 and sys.argv[1] in {"-h", "--help"}:
		print("Usage: python3 scripts/validate-release.py <version> [stale_version_1 stale_version_2 ...]")
		print("   or: python3 scripts/validate-release.py --bump <new_version>")
		return
	if len(sys.argv) < 2:
		print(
			"Usage: python3 scripts/validate-release.py <version> [stale_version_1 stale_version_2 ...]"
		)
		print("   or: python3 scripts/validate-release.py --bump <new_version>")
		sys.exit(1)

	root_dir = Path(__file__).resolve().parent.parent
	manifest_path = root_dir / "scripts" / "release-manifest.json"

	if sys.argv[1] == "--bump":
		if len(sys.argv) < 3:
			print(
				"Error: --bump requires a target version (e.g. python3 scripts/validate-release.py --bump 4.5.1)"
			)
			sys.exit(1)
		new_version = sys.argv[2].lstrip("v")
		if not re.match(r"^\d+\.\d+\.\d+", new_version):
			print(f"Error: Invalid version format '{new_version}'. Expected semantic version like '4.5.10'")
			sys.exit(1)
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
