"""Resolve the real Dropbox test drive without replacing configuration."""
import os
from pathlib import Path
import runpy
import subprocess


class CloudUnavailable(Exception):
	pass


def dropbox_test_root(project_root: Path) -> tuple[Path, dict]:
	config = Path.home() / ".config" / "RAIkeep.json5"
	overrides = (os.environ.get(name) for name in ("JSONPIT_CONFIG", "RAIKEEP_CONFIG"))
	if not config.is_file() or any(value and Path(value).expanduser().resolve() != config.resolve() for value in overrides):
		raise CloudUnavailable("the real RAIkeep configuration is unavailable or overridden")
	loads = runpy.run_path(str(project_root / "inqaba/inqaba/json5.py"))["loads_json5"]
	settings = loads(config.read_text(encoding="utf-8"))
	if settings.get("TestCloud") != "Dropbox":
		raise CloudUnavailable("TestCloud is not Dropbox")
	try:
		result = subprocess.run(["amafu", "list", "cloud", "Dropbox"], capture_output=True, text=True, check=True)
	except (OSError, subprocess.CalledProcessError) as error:
		raise CloudUnavailable(f"cannot resolve Dropbox through amafu: {error}") from error
	lines = result.stdout.splitlines()
	if len(lines) != 1 or not Path(lines[0]).is_absolute():
		raise ValueError("amafu did not return one absolute Dropbox root")
	root = Path(lines[0]).resolve()
	configured = settings.get("Cloud", {}).get("Dropbox")
	if not isinstance(configured, str) or not configured:
		raise CloudUnavailable("Cloud.Dropbox is not configured")
	if Path(configured).expanduser().resolve() != root:
		raise ValueError("amafu Dropbox root differs from Cloud.Dropbox in the real configuration")
	if not root.is_dir():
		raise CloudUnavailable("the configured Dropbox root is unavailable")
	return root, settings
