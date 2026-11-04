# Business System Architect — Build B (Capability-Graph)

**Independent candidate implementation.** A portable starting point for a fresh GPT to design a business super-system from a **capability manifest** rather than from a fixed repository checklist.

The owner describes actual capabilities, constraints, stakeholders and risks. A small deterministic planner returns a **repository graph**, roles, approval gates, and local scaffold. Nothing contacts GitHub or changes remote systems.

## Run locally

Requires Python 3.10+ only; no dependencies, subscriptions, API keys or external credentials.

```bash
python3 -m architect.cli plan examples/workspace.json
python3 -m architect.cli generate examples/workspace.json --out ./my-business-workspace
python3 -m architect.cli check ./my-business-workspace
python3 -m unittest discover -s tests -v
```

## Connect a new GPT

Provide [AGENTS.md](AGENTS.md), [docs/ONBOARDING.md](docs/ONBOARDING.md), [docs/GOVERNANCE.md](docs/GOVERNANCE.md), and [agentpacks/registry.json](agentpacks/registry.json) to a new GPT. It needs an authorized GitHub connector to **read** the repository directly; without that, give it these non-sensitive files as references. It needs separate permissions and owner approval to create or modify remote repositories.

Suggested first message: **"Use the Business System Architect onboarding. Interview me about my actual business processes and constraints one question at a time. Generate a repo topology and risk gates. Do not create remote resources until I review exact names and permissions."**

## Principle

The system must be useful **before automation**. A two-repo baseline holds governance and delivery work; optional, justified capabilities add knowledge, products, integrations, or automation. Each has its own canonical owner and dependencies. This discourages sprawling systems that become expensive to operate.

## Deliverables

- [docs/ONBOARDING.md](docs/ONBOARDING.md): conversation and handoff
- [docs/GOVERNANCE.md](docs/GOVERNANCE.md): owner authority, collaborator rules
- [docs/STATE-MACHINE.md](docs/STATE-MACHINE.md): decision and evidence lifecycle
- [security/THREAT-MODEL.md](security/THREAT-MODEL.md): threat register
- [agentpacks/registry.json](agentpacks/registry.json): agent package interface
- [tools/catalog.json](tools/catalog.json): possible tools, **not** enabled integrations
- [examples/workspace.json](examples/workspace.json): synthetic business specification
- [architect/engine.py](architect/engine.py): graph planner and local generator

This project is not an authentication service, agent orchestration platform, or substitute for GitHub's actual access controls. The role names here do not assert that other model instances are running. No business-specific records are bundled.
