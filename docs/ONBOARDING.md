# Guided onboarding (one question per turn)

## Stage 1 — Understand outcomes

Determine what the business does; what recurring result the owner wants; the current bottleneck; current software/services; and which process is most worthwhile to improve. Explain with examples, not programming jargon.

## Stage 2 — Classify capabilities

Each feature needs a human-verified use case. Supported starter categories:
- `knowledge-base`: reusable knowledge, SOPs and source evidence
- `analytics`: read-only metrics and review
- `product-engineering`: software/product delivery
- `integrations`: connectors to existing systems and scoped synchronization
- `automation`: scheduled/event-triggered actions, only after safe dry runs

The baseline `governance` and `delivery` repositories are always present. A simple solo operation may need nothing else.

## Stage 3 — Design access

Ask which users are owners, collaborators, contractors, customers and observers; which data is sensitive; and whether tooling must be free. Default everyone except the owner to no access. Repository reads, writes, approvals, releases, external APIs and financial actions are separate rights.

## Stage 4 — Generate and review

Create `workspace.json`. Run the planner in read-only mode, review graph, cost, tradeoffs and exact repository names. Human owner authorizes remote creation one batch at a time; never make a blanket permission request. Generate local structure, then direct the owner through repo creation in GitHub if a connected tool cannot create repositories.

## Stage 5 — Evidence and adaptation

After each setup change capture URL, timestamp, actor, permission evidence and test status. A missing confirmation is `unverified`. Replace incorrect assumptions rather than entrenching them. Review automation safety and recurring costs before activation.

## New user example

Owner: "I run a cleaning business and keep forgetting client requests."

Agent: "Where do new client requests arrive today?"

Owner: "Mostly email and text."

Agent: "First we'll define a manual intake workflow and a task queue. I won't request mailbox access yet; would you prefer to start by tracking requests manually, or compare tools that can connect later?"

Only after agreement should the agent propose a concrete repository and connector plan.
