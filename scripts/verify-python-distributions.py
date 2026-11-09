#!/usr/bin/env python3
"""
verify-python-distributions.py — Coordinated isolated release verification for inqaba and umgodi-json.

Performs:
1. Runtime dependency policy audit (minimal production dependencies, test tools isolated in dev).
2. Wheel and sdist building for inqaba and umgodi-json.
3. Twine check on all distribution artifacts.
4. Clean installation into a fresh, isolated virtual environment.
5. Import verification:
   - inqaba: InqPath, InqRelPath, InqFile, InqTextFile, InqJsonFile, InqConfig
   - umgodi: import umgodi
6. CLI entry point verification:
   - jpit --version
   - umgodi --version
7. Artwork and README verification.
8. Full 198-test pytest suite execution in isolated release environment.
"""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import tomllib
import zipfile
import tarfile

ROOT = Path(__file__).resolve().parent.parent


def run(*args: str, cwd: Path = ROOT, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
	res = subprocess.run(
		args,
		cwd=cwd,
		env=env or os.environ.copy(),
		capture_output=True,
		text=True,
	)
	if res.returncode != 0:
		print(f"Command failed ({res.returncode}): {' '.join(args)}", file=sys.stderr)
		if res.stdout:
			print(res.stdout, file=sys.stderr)
		if res.stderr:
			print(res.stderr, file=sys.stderr)
		sys.exit(res.returncode)
	return res


def check_runtime_dependency_policy() -> None:
	print("==> Checking runtime dependency policies...")
	# 1. inqaba: zero runtime dependencies
	inqaba_toml = tomllib.loads((ROOT / "inqaba/pyproject.toml").read_text(encoding="utf-8"))
	inqaba_deps = inqaba_toml.get("project", {}).get("dependencies", [])
	if inqaba_deps:
		raise ValueError(f"inqaba must have empty runtime dependencies, found: {inqaba_deps}")
	print("  [OK] inqaba: empty runtime dependencies []")

	# 2. umgodi-json: inqaba only, no test tooling
	umgodi_toml = tomllib.loads((ROOT / "umgodi-json/pyproject.toml").read_text(encoding="utf-8"))
	umgodi_deps = umgodi_toml.get("project", {}).get("dependencies", [])
	for dep in umgodi_deps:
		if not dep.startswith("inqaba"):
			raise ValueError(f"umgodi-json runtime dependency '{dep}' is not permitted; inqaba only.")
	forbidden = {"pytest", "pytest-cov", "mypy", "ruff", "build", "twine"}
	for dep in umgodi_deps:
		for tool in forbidden:
			if tool in dep.lower():
				raise ValueError(f"Forbidden test tool '{tool}' found in umgodi-json runtime dependencies!")
	print("  [OK] umgodi-json: inqaba only (test tooling isolated in [project.optional-dependencies].dev)")


def verify_artwork_and_readme() -> None:
	print("==> Verifying README and artwork inclusion...")
	# inqaba
	inqaba_art = ROOT / "inqaba/assets/inqaba-soweto-twins.svg"
	if not inqaba_art.exists():
		raise FileNotFoundError(f"Missing required artwork: {inqaba_art}")
	inqaba_readme = (ROOT / "inqaba/README.md").read_text(encoding="utf-8")
	if "inqaba-soweto-twins.svg" not in inqaba_readme:
		raise ValueError("inqaba/README.md must reference inqaba-soweto-twins.svg")
	print("  [OK] inqaba artwork and README verified")

	# umgodi-json
	for art in [
		"umgodi-json-sync.svg",
		"umgodi-json-sync-banner.svg",
		"umgodi-json-sync-compact.svg",
	]:
		p = ROOT / "umgodi-json/assets" / art
		if not p.exists():
			raise FileNotFoundError(f"Missing required artwork: {p}")
	umgodi_readme = (ROOT / "umgodi-json/README.md").read_text(encoding="utf-8")
	if "umgodi-json-sync.svg" not in umgodi_readme:
		raise ValueError("umgodi-json/README.md must reference umgodi-json-sync.svg")
	print("  [OK] umgodi-json artwork and README verified")


def build_and_verify_packages(python_bin: str) -> None:
	print("==> Building distributions in isolated environment...")
	with tempfile.TemporaryDirectory(prefix="raikeep-build-") as dist_dir:
		dist = Path(dist_dir)

		# Build inqaba
		run(python_bin, "-m", "build", "--outdir", str(dist), str(ROOT / "inqaba"))
		# Build umgodi-json
		run(python_bin, "-m", "build", "--outdir", str(dist), str(ROOT / "umgodi-json"))

		artifacts = sorted(dist.glob("*"))
		print(f"  Built {len(artifacts)} distribution artifact(s):")
		for a in artifacts:
			print(f"    - {a.name} ({a.stat().st_size:,} bytes)")

		# Twine check
		print("==> Running twine check...")
		twine_res = run(python_bin, "-m", "twine", "check", *(str(a) for a in artifacts))
		print("  [OK] Twine check passed")

		# Verify sdist archives include required artwork
		for a in artifacts:
			if a.name.endswith(".tar.gz"):
				with tarfile.open(a, "r:gz") as tar:
					names = tar.getnames()
					if "inqaba" in a.name:
						assert any("inqaba-soweto-twins.svg" in n for n in names), "sdist missing inqaba artwork"
					elif "umgodi" in a.name:
						assert any("umgodi-json-sync.svg" in n for n in names), "sdist missing umgodi artwork"

		# Install into a fresh virtual environment
		print("==> Verifying install in fresh virtualenv...")
		with tempfile.TemporaryDirectory(prefix="raikeep-fresh-venv-") as venv_dir:
			fresh_venv = Path(venv_dir)
			run(python_bin, "-m", "venv", str(fresh_venv))
			fresh_bin = fresh_venv / ("Scripts" if sys.platform == "win32" else "bin")
			fresh_python = fresh_bin / ("python.exe" if sys.platform == "win32" else "python")
			fresh_pip = fresh_bin / ("pip.exe" if sys.platform == "win32" else "pip")

			# Install inqaba wheel first
			inqaba_whl = next(dist.glob("inqaba-*.whl"))
			run(str(fresh_pip), "install", str(inqaba_whl))

			# Verify inqaba imports
			print("  Verifying inqaba imports...")
			inq_verify_script = (
				"from inqaba import InqPath, InqRelPath, InqFile, InqTextFile, InqJsonFile, InqConfig\n"
				"print('INQABA_OK')\n"
			)
			res_inq = run(str(fresh_python), "-c", inq_verify_script)
			assert "INQABA_OK" in res_inq.stdout
			print("  [OK] from inqaba import InqPath, InqRelPath, InqFile, InqTextFile, InqJsonFile, InqConfig")

			# Install umgodi-json wheel
			umgodi_whl = next(dist.glob("umgodi_json-*.whl"))
			run(str(fresh_pip), "install", str(umgodi_whl))

			# Verify umgodi imports
			print("  Verifying umgodi imports...")
			res_umg = run(str(fresh_python), "-c", "import umgodi; print('UMGODI_OK')")
			assert "UMGODI_OK" in res_umg.stdout
			print("  [OK] import umgodi")

			# Verify CLI commands
			jpit_bin = fresh_bin / ("jpit.exe" if sys.platform == "win32" else "jpit")
			umgodi_bin = fresh_bin / ("umgodi.exe" if sys.platform == "win32" else "umgodi")

			res_jpit = run(str(jpit_bin), "--version")
			assert "jpit v" in res_jpit.stdout
			print(f"  [OK] jpit CLI: {res_jpit.stdout.strip()}")

			res_umg_cli = run(str(umgodi_bin), "--version")
			assert "umgodi v" in res_umg_cli.stdout
			print(f"  [OK] umgodi CLI: {res_umg_cli.stdout.strip()}")


def run_pytest_suite(python_bin: str) -> None:
	print("==> Running complete test suite in isolated environment...")
	res = run(python_bin, "-m", "pytest", "umgodi-json/tests", "-q")
	print(f"  [OK] Test suite passed: {res.stdout.splitlines()[-1]}")


def main() -> None:
	print("======================================================================")
	print("RAIkeep Coordinated Python Distribution Verification")
	print("Target packages: Burkhardt/inqaba · Burkhardt/umgodi-json")
	print("======================================================================")

	check_runtime_dependency_policy()
	verify_artwork_and_readme()

	# Prepare or use .release-venv
	venv_path = ROOT / ".release-venv"
	venv_bin = venv_path / ("Scripts" if sys.platform == "win32" else "bin")
	venv_python = str(venv_bin / ("python.exe" if sys.platform == "win32" else "python"))
	venv_pip = str(venv_bin / ("pip.exe" if sys.platform == "win32" else "pip"))

	if not (venv_path / "bin" / "python").exists():
		print(f"==> Initializing isolated environment at {venv_path}...")
		run(sys.executable, "-m", "venv", str(venv_path))
		run(venv_pip, "install", "--upgrade", "pip")

	# Ensure dev tools are installed in isolated venv only
	run(venv_pip, "install", "build", "twine", "pytest")
	run(venv_pip, "install", "-e", "./inqaba")
	run(venv_pip, "install", "-e", "./umgodi-json[dev]")

	build_and_verify_packages(venv_python)
	run_pytest_suite(venv_python)

	print("======================================================================")
	print("All Python distribution verifications PASSED successfully.")
	print("======================================================================")


if __name__ == "__main__":
	main()
