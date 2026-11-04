import json
import tempfile
import unittest
from pathlib import Path
from architect.engine import ManifestError, check, design, generate, parse_manifest, slug


class ArchitectureTests(unittest.TestCase):
    def setUp(self):
        self.manifest = {
            "schema_version": 1,
            "business": {"name": "Cedarline Services", "owner_login": "example-owner"},
            "constraints": {"privacy": "private", "cost_ceiling": "free", "team_mode": "solo"},
            "capabilities": [],
            "workflows": [],
        }

    def test_minimal_footprint(self):
        plan = design(self.manifest)
        self.assertEqual([r["domain"] for r in plan["repositories"]], ["governance", "delivery"])
        self.assertFalse(plan["remote_changes_performed"])

    def test_graph_capabilities(self):
        self.manifest["capabilities"] = ["automation", "integrations", "knowledge-base"]
        repos = design(self.manifest)["repositories"]
        self.assertEqual(len(repos), 5)
        self.assertTrue(all(r["visibility"] == "private" for r in repos))
        self.assertTrue(any(r["risk"] == "elevated" for r in repos))
        self.assertTrue(any(r["depends_on"] for r in repos))

    def test_safe_slug(self):
        self.assertEqual(slug("Moss & Stone, LLC"), "moss-stone-llc")
        with self.assertRaises(ManifestError):
            slug("✨")

    def test_reject_public_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.manifest["constraints"]["privacy"] = "public"
            file = Path(tmp) / "manifest.json"
            file.write_text(json.dumps(self.manifest))
            with self.assertRaises(ManifestError):
                parse_manifest(file)

    def test_require_manual_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.manifest["workflows"] = [{"name":"intake","trigger":"request","input":"message","output":"task","manual_fallback":False}]
            file = Path(tmp) / "manifest.json"
            file.write_text(json.dumps(self.manifest))
            with self.assertRaises(ManifestError):
                parse_manifest(file)

    def test_generation_audit_and_tamper(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "workspace"
            generate(self.manifest, out)
            self.assertEqual(check(out), [])
            with self.assertRaises(ManifestError):
                generate(self.manifest, out)
            policy = out / "cedarline-services-governance" / "POLICY.json"
            value = json.loads(policy.read_text())
            value["automation_enabled"] = True
            policy.write_text(json.dumps(value))
            self.assertTrue(any("unsafe policy" in item for item in check(out)))

    def test_dependency_well_formed(self):
        self.manifest["capabilities"] = ["product-engineering", "analytics"]
        plan = design(self.manifest)
        names = {r["slug"] for r in plan["repositories"]}
        self.assertTrue(all(set(r["depends_on"]).issubset(names) for r in plan["repositories"]))


if __name__ == "__main__":
    unittest.main()
