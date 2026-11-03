#!/usr/bin/env python3
"""Check immutable-tag recovery without credentials, network, or publication."""

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(sys.argv.pop(1)).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
REPOS = ("OsLib", "RaiUtils", "RaiImage", "JsonPit")


def script(source, name):
	step = source.split(f"      - name: {name}\n", 1)[1].split("      - name:", 1)[0]
	block = step.split("        run: |\n", 1)[1]
	return "\n".join(line[10:] for line in block.splitlines() if line.startswith("          "))


class TrustedPublishingTests(unittest.TestCase):
	def test_release_chain_uses_the_standardized_workflow_filename(self):
		chain = (Path(__file__).resolve().parent / "release-chain.sh").read_text()
		for name in REPOS:
			calls = [line for line in chain.splitlines() if line.lstrip().startswith(f'release_submodule "{name}" ')]
			self.assertTrue(calls, name)
			for line in calls:
				self.assertTrue(line.endswith('"publish-nuget.yaml"'), line)

	def test_authentication_and_tag_checkout_contract(self):
		for name in REPOS:
			with self.subTest(repo=name):
				source = (ROOT / name / ".github/workflows/publish-nuget.yaml").read_text()
				self.assertNotIn("secrets.NUGET_API_KEY", source)
				self.assertIn("      id-token: write", source)
				self.assertIn("uses: NuGet/login@v1", source)
				self.assertIn("user: Burkhardt", source)
				self.assertIn("${{ steps.nuget_login.outputs.NUGET_API_KEY }}", source)
				self.assertIn("ref: refs/tags/${{ env.RELEASE_REF }}", source)
				self.assertLess(source.index("name: Validate release tag input"), source.index("name: Checkout"))
				self.assertLess(source.index("uses: NuGet/login@v1"), source.index("name: Publish to NuGet"))
				self.assertNotIn("GITHUB_REF_NAME#v", source)
				self.assertNotIn("${{ inputs.release_ref }}", script(source, "Validate release tag input"))

	def test_invalid_refs_cannot_pass_validation_or_execute_shell(self):
		invalid = ("", "main", "refs/heads/main", "refs/tags/v4.5.16", "4.5.16", "v4.5", "v4.5.16-rc1", "v4.5.16\nmain", "v4.5.16; touch injected", "$(touch injected)")
		with tempfile.TemporaryDirectory() as directory:
			for name in REPOS:
				source = (ROOT / name / ".github/workflows/publish-nuget.yaml").read_text()
				for ref in invalid:
					with self.subTest(repo=name, ref=ref):
						result = subprocess.run(["bash", "-eu", "-o", "pipefail", "-c", script(source, "Validate release tag input")],
							cwd=directory, env={**os.environ, "RELEASE_REF": ref}, capture_output=True, text=True)
						self.assertNotEqual(0, result.returncode)
			self.assertFalse((Path(directory) / "injected").exists())

	def test_recovery_builds_the_tag_even_when_workflow_branch_has_advanced(self):
		for name in REPOS:
			with self.subTest(repo=name), tempfile.TemporaryDirectory() as directory:
				root = Path(directory)
				def git(*args):
					return subprocess.check_output(["git", "-C", directory, *args], text=True).strip()
				git("init", "-q")
				git("config", "user.name", "Release test")
				git("config", "user.email", "release-test@example.invalid")
				project = root / f"{name}.csproj"
				project.write_text("<Project>\n  <Version>4.5.16</Version>\n</Project>\n")
				git("add", ".")
				git("commit", "-qm", "Tagged source")
				git("tag", "v4.5.16")
				expected = git("rev-parse", "HEAD")
				project.write_text("<Project>\n  <Version>4.5.17</Version>\n</Project>\n")
				git("commit", "-am", "Later source", "-q")
				git("branch", "v4.5.16")  # A colliding branch must never select later source.
				source = (ROOT / name / ".github/workflows/publish-nuget.yaml").read_text()
				env = {**os.environ, "RELEASE_REF": "v4.5.16", "GITHUB_REF_NAME": "main"}
				for step in ("Validate release tag input", "Validate tag matches csproj version"):
					if step == "Validate tag matches csproj version":
						git("checkout", "--quiet", "--detach", "refs/tags/v4.5.16")
					result = subprocess.run(["bash", "-eu", "-o", "pipefail", "-c", script(source, step)],
						cwd=directory, env=env, capture_output=True, text=True)
					self.assertEqual(0, result.returncode, result.stderr + result.stdout)
				self.assertEqual(expected, git("rev-parse", "HEAD"))
				self.assertIn(expected, result.stdout)
				mismatch = subprocess.run(["bash", "-eu", "-o", "pipefail", "-c", script(source, "Validate tag matches csproj version")],
					cwd=directory, env={**env, "RELEASE_REF": "v4.5.17"}, capture_output=True, text=True)
				self.assertNotEqual(0, mismatch.returncode)


if __name__ == "__main__":
	unittest.main()
