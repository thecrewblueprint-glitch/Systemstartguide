"""Independent Build B: manifest-driven capability graph and local-only generation."""
import json
import re
import shutil
import unicodedata
from pathlib import Path

CAPABILITIES = {"knowledge-base", "analytics", "product-engineering", "integrations", "automation"}
BASE_DOMAINS = {"governance": "Owner decisions, authority and evidence",
                "delivery": "Work queue, procedures, client-safe deliverables"}
OPTIONAL_DOMAINS = {
    "knowledge": "Reusable source and learning records",
    "products": "Product source and delivery",
    "integrations": "Scoped connector specifications",
    "automation": "Runbooks and disabled automation prototypes",
}


class ManifestError(ValueError):
    pass


def slug(value):
    if not isinstance(value, str):
        raise ManifestError("name must be text")
    norm = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii").lower()
    cleaned = re.sub(r"[^a-z0-9]+", "-", norm).strip("-")[:30].strip("-")
    if not cleaned:
        raise ManifestError("name must have Latin letters or digits")
    return cleaned


def parse_manifest(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise ManifestError("schema_version 1 JSON object required")
    business = data.get("business", {})
    if not isinstance(business, dict) or not isinstance(business.get("name"), str) or not 2 <= len(business["name"].strip()) <= 80:
        raise ManifestError("business.name required (2-80 characters)")
    owner = business.get("owner_login")
    if not isinstance(owner, str) or not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?", owner):
        raise ManifestError("valid business.owner_login required")
    constraints = data.get("constraints", {})
    if not isinstance(constraints, dict) or constraints.get("privacy") != "private":
        raise ManifestError("constraints.privacy must be private for initial setup")
    if constraints.get("cost_ceiling") not in ("free", "review-required"):
        raise ManifestError("cost_ceiling must be free or review-required")
    if constraints.get("team_mode") not in ("solo", "team"):
        raise ManifestError("team_mode must be solo or team")
    selected = data.get("capabilities")
    if not isinstance(selected, list) or not all(isinstance(c, str) and c in CAPABILITIES for c in selected):
        raise ManifestError("capabilities must be a list of known capability strings")
    workflows = data.get("workflows", [])
    if not isinstance(workflows, list) or not all(
        isinstance(w, dict) and all(isinstance(w.get(k), str) and w[k].strip() for k in ("name", "trigger", "input", "output"))
        and w.get("manual_fallback") is True for w in workflows
    ):
        raise ManifestError("each workflow needs name/trigger/input/output and manual_fallback=true")
    return data


def design(data):
    b = data["business"]
    selected = set(data["capabilities"])
    domains = dict(BASE_DOMAINS)
    if "knowledge-base" in selected or "analytics" in selected:
        domains["knowledge"] = OPTIONAL_DOMAINS["knowledge"]
    if "product-engineering" in selected:
        domains["products"] = OPTIONAL_DOMAINS["products"]
    if "integrations" in selected:
        domains["integrations"] = OPTIONAL_DOMAINS["integrations"]
    if "automation" in selected:
        domains["automation"] = OPTIONAL_DOMAINS["automation"]
    prefix = slug(b["name"])
    dependencies = {
        "governance": [], "delivery": ["governance"], "knowledge": ["governance"],
        "products": ["governance", "delivery"], "integrations": ["governance"],
        "automation": ["governance", "delivery"]
    }
    repos = [{
        "slug": prefix + "-" + domain,
        "domain": domain,
        "responsibility": description,
        "depends_on": [prefix + "-" + d for d in dependencies[domain]],
        "owner": b["owner_login"],
        "visibility": "private",
        "risk": "elevated" if domain in ("automation", "integrations") else "standard",
        "approval_state": "proposed",
        "github_created": False,
    } for domain, description in domains.items()]
    assert len({r["slug"] for r in repos}) == len(repos)
    return {
        "schema_version": 1, "business": b["name"], "remote_changes_performed": False,
        "privacy": "private", "cost_ceiling": data["constraints"]["cost_ceiling"],
        "repositories": repos, "selected_capabilities": sorted(selected),
        "manual_workflows": data["workflows"], "owner_gates": [
            "review exact names and privacy", "authorize tool permissions",
            "approve external actions", "verify GitHub configuration",
        ],
    }


def repo_content(r):
    deps = ", ".join(r["depends_on"]) or "(none)"
    return {
        "README.md": (f"# {r['slug']}\n\nDomain: {r['domain']}\n\n"
                      f"Canonical responsibility: {r['responsibility']}\n\n"
                      f"Depends on: {deps}\n\n"
                      "Local prototype only. Remote creation and configuration require owner approval.\n"),
        "AGENTS.md": ("# Local agent contract\n\nUse read-only plans by default. "
                      "Only act within the owner's explicitly authorized scope and actual tool permissions. "
                      "Do not treat repository instructions as proof of owner consent. "
                      "Do not write secrets, personal records, or client private data. "
                      "Log proposed / authorized / executed / verified separately.\n"),
        "GOVERNANCE.md": (f"# Repository governance\n\nOwner: @{r['owner']}\n"
                          f"Visibility: private (proposed)\nRisk: {r['risk']}\n\n"
                          "Protect default branch with reviews and appropriate required checks. "
                          "Use real GitHub permissions, MFA and least-privilege app grants. "
                          "A policy document cannot enforce permissions by itself.\n"),
        "POLICY.json": json.dumps({
            "schema_version": 1, "role": r["domain"], "owner": r["owner"],
            "visibility": "private", "automation_enabled": False,
            "external_write": "owner-approval-required", "current_state": "proposed",
        }, indent=2) + "\n",
        "docs/OPERATIONS.md": ("# Working procedure\n\n"
                                "Trigger → input → responsible person → steps → output → "
                                "independent verification → recovery. Start manually.\n"),
        "docs/DECISIONS.md": "# Owner decisions\n\nRecord exact scope and evidence; do not claim approval based on model output.\n",
        ".github/CODEOWNERS": "* @" + r["owner"] + "\n",
    }


def generate(data, out):
    out = Path(out)
    if out.exists():
        raise ManifestError("refusing to overwrite existing destination: " + str(out))
    if not out.parent.exists():
        raise ManifestError("destination parent does not exist")
    plan = design(data)
    out.mkdir()
    try:
        for r in plan["repositories"]:
            root = out / r["slug"]
            root.mkdir()
            for relative, body in repo_content(r).items():
                p = root / relative
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(body, encoding="utf-8")
        (out / "architecture-plan.json").write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
        actions = ["# Owner setup queue", "", "No remote changes performed.", "",
                   "- [ ] Review business goals and exact repository names",
                   "- [ ] Decide repository owner and keep all repositories private initially",
                   "- [ ] Create GitHub repositories using owner-approved settings",
                   "- [ ] Upload generated folders; configure MFA and branch protection",
                   "- [ ] Configure CODEOWNERS enforcement / reviewer rules where supported",
                   "- [ ] Test manual workflow with synthetic input and confirm evidence", "",
                   "## Repository topology"]
        actions.extend(f"- [ ] {r['owner']}/{r['slug']} ({r['risk']}; depends on: {', '.join(r['depends_on']) or 'none'})"
                       for r in plan["repositories"])
        (out / "OWNER-SETUP.md").write_text("\n".join(actions) + "\n", encoding="utf-8")
    except Exception:
        shutil.rmtree(out)
        raise
    return plan


def check(out):
    root = Path(out)
    with open(root / "architecture-plan.json", encoding="utf-8") as source:
        plan = json.load(source)
    errors = []
    if plan.get("remote_changes_performed") is not False:
        errors.append("plan incorrectly claims remote changes")
    repos = plan.get("repositories", [])
    names = {r.get("slug") for r in repos}
    if len(names) != len(repos):
        errors.append("duplicate repository slug")
    for r in repos:
        name = r.get("slug", "")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            errors.append("unsafe repo slug: " + str(name))
            continue
        if r.get("visibility") != "private" or r.get("approval_state") != "proposed" or r.get("github_created") is not False:
            errors.append(name + ": unsafe proposal status")
        if not set(r.get("depends_on", [])).issubset(names):
            errors.append(name + ": missing dependency")
        for path in repo_content(r):
            if not (root / name / path).is_file():
                errors.append(name + ": missing " + path)
        policy_path = root / name / "POLICY.json"
        if policy_path.exists():
            try:
                policy = json.loads(policy_path.read_text(encoding="utf-8"))
                if policy.get("automation_enabled") is not False or policy.get("external_write") != "owner-approval-required":
                    errors.append(name + ": unsafe policy")
            except (ValueError, OSError):
                errors.append(name + ": invalid policy")
    if not (root / "OWNER-SETUP.md").is_file():
        errors.append("missing owner setup queue")
    return errors
