#!/usr/bin/env python3
"""Exercise the tracked-package guard in an isolated Git repository."""
from pathlib import Path
import subprocess
import tempfile


chain = Path(__file__).resolve().with_name("release-chain.sh")


def git(root: Path, *args: str) -> None:
	subprocess.run(["git", "-C", str(root), *args], check=True)


def guard(root: Path, expected_success: bool) -> None:
	result = subprocess.run(
		["bash", "-c", 'source "$1"; assert_no_tracked_packages "$2" fixture',
		 "tracked-package-test", str(chain), str(root)],
		capture_output=True, text=True,
	)
	if (result.returncode == 0) != expected_success:
		raise RuntimeError(f"Unexpected tracked-package guard result:\n{result.stdout}{result.stderr}")


with tempfile.TemporaryDirectory(prefix="tracked-package-preflight-") as directory:
	root = Path(directory)
	git(root, "init", "-q")
	(root / ".gitignore").write_text("*.nupkg\n*.snupkg\n")
	(root / "artifacts").mkdir()
	(root / "artifacts/RaiUtilsCore.2.3.1.nupkg").write_text("legacy")
	guard(root, True)
	git(root, "add", "-f", "artifacts/RaiUtilsCore.2.3.1.nupkg")
	guard(root, False)
	git(root, "rm", "--cached", "-q", "artifacts/RaiUtilsCore.2.3.1.nupkg")
	(root / "artifacts/RaiUtilsCore.2.3.1.snupkg").write_text("symbols")
	git(root, "add", "-f", "artifacts/RaiUtilsCore.2.3.1.snupkg")
	guard(root, False)
	git(root, "rm", "--cached", "-q", "artifacts/RaiUtilsCore.2.3.1.snupkg")
	guard(root, True)
print("Tracked-package preflight checks passed.")
