"""Offline behavior tests; no CAD or external service is required."""

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "audit_release.py"
spec = importlib.util.spec_from_file_location("audit_release", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ReleaseAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.file = self.root / "board.kicad_pcb"
        self.file.write_bytes(b"sample design content\n")
        self.manifest = self.root / "release-manifest.json"
        self.data = {
            "schema_version": 1,
            "release_id": "fixture-r1",
            "source_revision": "a" * 40,
            "required_roles": ["native-electrical"],
            "artifacts": [{"path": self.file.name, "role": "native-electrical", "sha256": hashlib.sha256(self.file.read_bytes()).hexdigest()}],
            "omissions": {},
        }

    def run_audit(self, **kwargs):
        self.manifest.write_text(json.dumps(self.data), encoding="utf-8")
        return module.audit(self.manifest, **kwargs)

    def test_valid_inventory(self):
        result = self.run_audit()
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["inventory_scope"], "complete")

    def test_changed_content_rejected(self):
        self.file.write_bytes(b"different content")
        self.assertTrue(any("mismatch" in e for e in self.run_audit()["errors"]))

    def test_missing_file_rejected(self):
        self.file.unlink()
        self.assertTrue(any("missing" in e for e in self.run_audit()["errors"]))

    def test_missing_role_rejected(self):
        self.data["required_roles"].append("mechanical-drawings")
        self.assertTrue(any("Required role" in e for e in self.run_audit()["errors"]))

    def test_declared_omission_reported(self):
        self.data["required_roles"].append("placement")
        self.data["omissions"]["placement"] = "Hand-assembled prototype; automatic placement unqualified."
        result = self.run_audit()
        self.assertEqual(result["errors"], [])
        self.assertIn("placement", result["declared_omissions"])

    def test_unlisted_file_rejected_or_marked_partial(self):
        (self.root / "forgotten.pdf").write_bytes(b"document")
        self.assertTrue(self.run_audit()["errors"])
        result = self.run_audit(allow_unlisted=True)
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["inventory_scope"], "partial")
        self.assertEqual(result["unlisted_files"], ["forgotten.pdf"])

    def test_duplicate_artifact_rejected(self):
        self.data["artifacts"].append(dict(self.data["artifacts"][0]))
        with self.assertRaises(module.InvalidManifest):
            self.run_audit()

    def test_path_escape_rejected(self):
        for path in ["../elsewhere", "/tmp/elsewhere", "a/../elsewhere", "a//b", "./board.kicad_pcb", "a\\b"]:
            with self.subTest(path=path):
                self.data["artifacts"][0]["path"] = path
                with self.assertRaises(module.InvalidManifest):
                    self.run_audit()

    def test_symlink_rejected(self):
        link = self.root / "alias.kicad_pcb"
        link.symlink_to(self.file)
        self.data["artifacts"][0]["path"] = link.name
        self.assertTrue(any("Symlink" in e for e in self.run_audit()["errors"]))

    def test_symlink_parent_rejected(self):
        actual = self.root / "real"
        actual.mkdir()
        (actual / "board").write_bytes(self.file.read_bytes())
        (self.root / "alias").symlink_to(actual, target_is_directory=True)
        self.data["artifacts"][0]["path"] = "alias/board"
        self.assertTrue(any("Symlink" in e for e in self.run_audit()["errors"]))

    def test_empty_artifact_rejected_even_with_correct_hash(self):
        self.file.write_bytes(b"")
        self.data["artifacts"][0]["sha256"] = hashlib.sha256(b"").hexdigest()
        self.assertTrue(any("Empty" in e for e in self.run_audit()["errors"]))

    def test_invalid_schema_and_identifiers_rejected(self):
        cases = [("source_revision", "d496dda"), ("schema_version", True), ("required_roles", []), ("release_id", " ")]
        for key, value in cases:
            with self.subTest(key=key):
                original = self.data[key]
                self.data[key] = value
                with self.assertRaises(module.InvalidManifest):
                    self.run_audit()
                self.data[key] = original

    def test_provided_and_omitted_conflict_rejected(self):
        self.data["omissions"]["native-electrical"] = "Incorrect omission"
        with self.assertRaises(module.InvalidManifest):
            self.run_audit()

    def test_cli_exit_statuses(self):
        self.run_audit()
        def run():
            return subprocess.run([sys.executable, str(SCRIPT), str(self.manifest)], capture_output=True, text=True)
        self.assertEqual(run().returncode, 0)
        self.file.write_bytes(b"modified")
        self.assertEqual(run().returncode, 1)
        self.manifest.write_text("not json", encoding="utf-8")
        self.assertEqual(run().returncode, 2)


if __name__ == "__main__":
    unittest.main()
