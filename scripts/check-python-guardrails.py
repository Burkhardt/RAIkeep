"""Run Vikela across tracked umbrella and submodule Python sources."""
import json
from pathlib import Path
import subprocess
import sys

from guardrail_sources import sources


def main():
    root = Path(__file__).resolve().parents[1]
    files = sources(root, "*.py", "*.ipynb")
    if not files:
        raise RuntimeError("No Python sources found")

    # Both implementations test that these operations raise ProtectedAttributeError.
    # Match the operation, so another violation in the same test still fails.
    operations = {
        'item["Id"] = "Other"',
        'del item["Id"]',
        'item.set_property({"Status": "Bad", "Modified": "invalid"})',
    }
    expected = {(f"{project}/tests/test_live_references.py", operation)
                for project in ("JsonPit.Python", "umgodi-json") for operation in operations}
    expected_count = len(expected)
    run = subprocess.run([sys.executable, "-m", "vikela", "--json", *files],
                         cwd=root / "vikela", stdout=subprocess.PIPE)
    if run.returncode not in (0, 1):
        return run.returncode
    failures = 0
    for finding in json.loads(run.stdout):
        path = Path(finding["path"])
        relative = path.relative_to(root)
        line = finding["line"]
        if finding["rule"] == "RAI012":
            operation = path.read_text(encoding="utf-8").splitlines()[line - 1].strip()
            key = (relative.as_posix(), operation)
            if key in expected:
                expected.remove(key)
                continue
        print(f"{relative}:{line}: {finding['rule']} {finding['reason']}")
        failures += 1
    print(f"Vikela checked {len(files)} files: {failures} unexpected findings, "
          f"{expected_count - len(expected)} expected negative-test findings.")
    for path, operation in sorted(expected):
        print(f"Expected RAI012 diagnostic missing in {path}: {operation}")
    return int(bool(failures or expected))


if __name__ == "__main__":
    sys.exit(main())
