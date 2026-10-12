#!/usr/bin/env python3
"""Exercise release preparation against isolated copies, without publishing."""

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import re
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
extract_spec = importlib.util.spec_from_file_location(
	"release_note_extractor", ROOT / "scripts/extract-release-notes.py"
)
extractor = importlib.util.module_from_spec(extract_spec)
extract_spec.loader.exec_module(extractor)


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
			note.format(version=self.version, major=self.version.split(".", 1)[0])
			for note in self.manifest["release_notes"]
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
		validator = tools.ReleaseValidator(self.root, self.version, run_external_checks=False)
		with contextlib.redirect_stdout(io.StringIO()):
			success = validator.run_all_validations([])
		return success, validator.errors

	def test_current_release_and_repeated_bump_preserve_literal_expressions(self):
		self.assertEqual((True, []), self.validate())
		before = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
		bumper = tools.ReleaseBumper(
			self.root,
			self.root / "scripts/release-manifest.json",
			self.version,
			run_external_checks=False,
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

	def test_amafu_package_readme_rejects_html_folding(self):
		readme = self.root / "Amafu/README.md"
		readme.write_text(readme.read_text().replace("## Previous Versions", "<details>\n## Previous Versions"))
		success, errors = self.validate()
		self.assertFalse(success)
		self.assertEqual(1, len(errors))
		self.assertIn("Amafu README contains collapsible HTML tags not supported by NuGet", errors[0])

	def test_new_release_is_prepended_once(self):
		note = self.root / "doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md"
		self.assertTrue(tools.ReleaseBumper.prepend_release_section(note, "4.5.9"))
		text = note.read_text()
		self.assertLess(text.index("## 4.5.9"), text.index("## 4.5.8"))
		self.assertFalse(tools.ReleaseBumper.prepend_release_section(note, "4.5.9"))
		self.assertEqual(1, len(re.findall(r"^## 4\.5\.9$", note.read_text(), re.MULTILINE)))

	def test_release_body_contains_only_requested_version(self):
		note = self.root / "doc/releases/v4.x/RAIkeep_RELEASE_NOTES_4.x.md"
		body = extractor.extract(note, "4.5.8")
		self.assertTrue(body.startswith("## 4.5.8\n"))
		self.assertNotIn("## 4.5.7", body)
		with self.assertRaisesRegex(ValueError, "Expected exactly one"):
			extractor.extract(note, "4.9.9")


if __name__ == "__main__":
	unittest.main()
