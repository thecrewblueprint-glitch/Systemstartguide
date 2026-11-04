import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class AgentPatternContracts(unittest.TestCase):
    def test_role_contracts_avoid_external_authority(self):
        data = json.loads((ROOT / "agentpacks/role-contract-v1.json").read_text())
        self.assertEqual(data["runtime_status"], "DECLARATIVE_ONLY")
        roles = data["roles"]
        self.assertGreaterEqual(len(roles), 7)
        self.assertEqual(len(roles), len({r["id"] for r in roles}))
        for role in roles:
            for field in ("id","purpose","inputs","outputs","allowed_actions","prohibited_actions"):
                self.assertTrue(role.get(field), (role.get("id"), field))
            self.assertNotIn("external-write", role["allowed_actions"])
            self.assertIn("external-write", role["prohibited_actions"])

    def test_workflows_have_fallback_and_review(self):
        roles = json.loads((ROOT/"agentpacks/role-contract-v1.json").read_text())
        known = {r["id"] for r in roles["roles"]}
        data = json.loads((ROOT/"workflows/pattern-library-v1.json").read_text())
        patterns = data["patterns"]
        self.assertIn(data["default_pattern"], {p["id"] for p in patterns})
        self.assertEqual(len(patterns), len({p["id"] for p in patterns}))
        for p in patterns:
            for field in ("id","kind","when","roles","steps","fallback","human_gate","success_measure"):
                self.assertTrue(p.get(field), (p.get("id"), field))
            self.assertTrue(set(p["roles"]).issubset(known), p["id"])
            self.assertGreaterEqual(len(p["steps"]), 3)
        self.assertIn("event-driven-sync", {p["id"] for p in patterns})
        self.assertIn("human-gated-action", {p["id"] for p in patterns})

if __name__ == "__main__":
    unittest.main()
