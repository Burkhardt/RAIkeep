#!/usr/bin/env python3
"""Build and smoke-test both Python distributions without publishing."""

import argparse
from pathlib import Path
import subprocess
import sys
import tempfile
import tomllib


def run(*args: str) -> None:
	subprocess.run(args, check=True)


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
			for flag in ("-v", "--version"):
				command = bin_dir / (name + (".exe" if sys.platform == "win32" else ""))
				result = subprocess.run([str(command), flag], check=True, capture_output=True, text=True)
				if result.stdout.strip() != f"{name} v{version}":
					raise ValueError(f"Unexpected installed CLI output: {result.stdout!r}")
		result = subprocess.run([str(python), str(output / "jpit"), "--version"], check=True, capture_output=True, text=True)
		if result.stdout.strip() != f"jpit v{version}":
			raise ValueError(f"Unexpected standalone version: {result.stdout!r}")
	print(f"Verified both Python packages and standalone jpit v{version}.")


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument("repo", type=Path)
	parser.add_argument("version")
	parser.add_argument("output", type=Path)
	args = parser.parse_args()
	build(args.repo.resolve(), args.version, args.output.resolve())
