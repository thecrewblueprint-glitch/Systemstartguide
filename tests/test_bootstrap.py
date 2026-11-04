import json
import tempfile
import unittest
from pathlib import Path
from scripts.bootstrap import ConfigurationError, config_from_file, make_plan, scaffold, slug


class BootstrapTests(unittest.TestCase):
    def setUp(self):
        self.data = {
            "business_name": "Northstar Studio",
            "owner_login": "sample-owner",
            "workflows": ["request-intake"],
            "optional_domains": [],
            "visibility": "private",
        }

    def test_slug_safe(self):
        self.assertEqual(slug("  Hello & World  "), "hello-world")
        with self.assertRaises(ConfigurationError):
            slug("🔥")

    def test_minimum_three_repos_private(self):
        plan = make_plan(self.data)
        self.assertEqual(len(plan["repositories"]), 3)
        self.assertTrue(all(r["visibility"] == "private" for r in plan["repositories"]))
        self.assertFalse(plan["remote_changes_performed"])

    def test_optional_repo(self):
        self.data["optional_domains"] = ["automation", "products", "automation"]
        self.assertEqual(len(make_plan(self.data)["repositories"]), 5)

    def test_reject_nonprivate_config(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "config.json"
            path.write_text(json.dumps({**self.data, "visibility": "public"}))
            with self.assertRaises(ConfigurationError):
                config_from_file(path)

    def test_scaffold_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            dest = Path(temp) / "out"
            plan = scaffold(self.data, dest)
            self.assertTrue((dest / plan["repositories"][0]["name"] / "GOVERNANCE.md").exists())
            self.assertTrue((dest / "setup-checklist.md").exists())
            with self.assertRaises(ConfigurationError):
                scaffold(self.data, dest)

    def test_reject_unrecognized_workflow(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "config.json"
            path.write_text(json.dumps({**self.data, "workflows": ["execute-anything"]}))
            with self.assertRaises(ConfigurationError):
                config_from_file(path)


if __name__ == "__main__":
    unittest.main()
