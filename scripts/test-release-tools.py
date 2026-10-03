#!/usr/bin/env python3
"""Exercise release preparation against isolated copies, without publishing."""

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location(
	"release_tools", ROOT / "scripts/validate-release.py"
)
tools = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tools)


class ReleaseToolsTests(unittest.TestCase):
	def setUp(self):
		self.temp = tempfile.TemporaryDirectory(prefix="raikeep-release-tests-")
		self.addCleanup(self.temp.cleanup)
		self.root = Path(self.temp.name)
		manifest_path = ROOT / "scripts/release-manifest.json"
		self.manifest = json.loads(manifest_path.read_text())
		self.version = self.manifest["current_version"]
		paths = {target["path"] for target in self.manifest["targets"]}
		paths.update(
			note.format(version=self.version) for note in self.manifest["release_notes"]
		)
		paths.update(f"{repo}/README.md" for _, repo, _ in tools.PACKAGE_REPOS)
		paths.update(
			[
				"README.md",
				"doc/README.md",
				"scripts/release-manifest.json",
				"Amafu/amafu/AmafuApplication.cs",
			]
		)
		for relative in paths:
			destination = self.root / relative
			destination.parent.mkdir(parents=True, exist_ok=True)
			shutil.copyfile(ROOT / relative, destination)

	def validate(self):
		validator = tools.ReleaseValidator(self.root, self.version)
		with contextlib.redirect_stdout(io.StringIO()):
			success = validator.run_all_validations([])
		return success, validator.errors

	def test_current_release_and_repeated_bump_preserve_literal_expressions(self):
		self.assertEqual((True, []), self.validate())
		before = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
		bumper = tools.ReleaseBumper(
			self.root, self.root / "scripts/release-manifest.json", self.version
		)
		with contextlib.redirect_stdout(io.StringIO()):
			self.assertTrue(bumper.bump())
		for path, contents in before.items():
			self.assertEqual(
				contents, path.read_bytes(), str(path.relative_to(self.root))
			)
		source = (self.root / "Amafu/amafu/AmafuApplication.cs").read_text()
		self.assertIn('WriteLine($"amafu v{Version()}");', source)
		installer = (self.root / "scripts/install-clis.sh").read_text()
		self.assertIn(
			'DEFAULT_VERSION="${DEFAULT_VERSION:-' + self.version + '}"', installer
		)

	def test_stale_conditional_fallback_is_rejected(self):
		project = self.root / "JsonPit/JsonPit.csproj"
		text = project.read_text()
		text = text.replace(
			f">{self.version}</OsLibPackageVersion>", ">0.0.1</OsLibPackageVersion>"
		)
		project.write_text(text)
		success, errors = self.validate()
		self.assertFalse(success)
		self.assertEqual(1, len(errors))
		self.assertIn("fallback property <OsLibPackageVersion> is 0.0.1", errors[0])


if __name__ == "__main__":
	unittest.main()
