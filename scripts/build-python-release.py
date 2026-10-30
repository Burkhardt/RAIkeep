#!/usr/bin/env python3
"""Build and smoke-test both Python distributions without publishing."""

import argparse
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import tomllib


def run(*args: str) -> None:
	subprocess.run(args, check=True)


def verify_help(command: list[str]) -> None:
	"""Reject stale help in the actual installed wheel or standalone artifact."""
	environment = os.environ.copy()
	environment["NO_COLOR"] = "1"
	result = subprocess.run([*command, "-h", "-n"], env=environment, check=True, capture_output=True, text=True)
	output = result.stdout
	if "\t" in output or "\033" in output:
		raise ValueError(f"Packaged help must be space-aligned plain text when redirected: {command}")
	for label in ["-w, --window", "-x, --id-exists", "-r, --pitroot"]:
		if not any(line.startswith(label) for line in output.splitlines()):
			raise ValueError(f"Packaged help is missing the current option {label}: {command}")
	if any(alias in output for alias in ["--retain-window", "--require-existing", "--require-exist"]):
		raise ValueError(f"Packaged help advertises a hidden compatibility alias: {command}")


def build(repo: Path, version: str, output: Path) -> None:
	for directory, name in [(repo, "jsonpit"), (repo / "packages/jpit", "jpit")]:
		metadata = tomllib.loads((directory / "pyproject.toml").read_text())["project"]
		if metadata["name"] != name or metadata["version"] != version:
			raise ValueError(f"{name} metadata must match {version} before publication.")
		if name == "jpit" and metadata["dependencies"] != [f"jsonpit=={version}"]:
			raise ValueError("jpit must depend on the exact coordinated jsonpit version.")
		if metadata["scripts"] != {"jpit": "jsonpit.cli:main", "jsonpit": "jsonpit.cli:main"}:
			raise ValueError(f"{name} must expose both CLI names.")
		output.mkdir(parents=True, exist_ok=True)
		run(sys.executable, "-m", "build", "--outdir", str(output), str(directory))
	artifacts = sorted([*output.glob(f"*-{version}-*.whl"), *output.glob(f"*-{version}.tar.gz")])
	if len(artifacts) != 4:
		raise ValueError("Expected a wheel and source archive for each Python distribution.")
	run(sys.executable, "-m", "twine", "check", *(str(path) for path in artifacts))
	run(sys.executable, str(repo / "scripts/build_standalone.py"), "--output", str(output / "jpit"))
	with tempfile.TemporaryDirectory(prefix="raikeep-python-install-") as temporary:
		venv = Path(temporary)
		run(sys.executable, "-m", "venv", str(venv))
		bin_dir = venv / ("Scripts" if sys.platform == "win32" else "bin")
		python = bin_dir / ("python.exe" if sys.platform == "win32" else "python")
		run(str(python), "-m", "pip", "install", "--no-index", "--no-deps", *(str(p) for p in artifacts if p.suffix == ".whl"))
		for name in ("jpit", "jsonpit"):
			command = bin_dir / (name + (".exe" if sys.platform == "win32" else ""))
			for flag in ("-v", "--version"):
				result = subprocess.run([str(command), flag], check=True, capture_output=True, text=True)
				if result.stdout.strip() != f"{name} v{version}":
					raise ValueError(f"Unexpected installed CLI output: {result.stdout!r}")
			verify_help([str(command)])
		result = subprocess.run([str(python), str(output / "jpit"), "--version"], check=True, capture_output=True, text=True)
		if result.stdout.strip() != f"jpit v{version}":
			raise ValueError(f"Unexpected standalone version: {result.stdout!r}")
		verify_help([str(python), str(output / "jpit")])
	print(f"Verified both Python packages and standalone jpit v{version}.")


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("repo", type=Path)
	parser.add_argument("version")
	parser.add_argument("output", type=Path)
	args = parser.parse_args()
	build(args.repo.resolve(), args.version, args.output.resolve())
