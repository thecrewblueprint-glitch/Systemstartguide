# Connect a brand-new GPT

A repository is **not automatically visible** to every GPT. Use one of the following supported patterns:

1. **Connected GitHub tool:** connect GitHub in the ChatGPT environment and grant explicit, least-privilege access. Ask the agent to read `README.md`, `AGENTS.md`, `docs/OWNER-CONTROL.md`, and `agentpacks/README.md` from this repo.
2. **No connected GitHub tool:** copy `AGENTS.md` into the new GPT's instructions, and provide the relevant documentation / archive as reference material. Instructions-only access does not make GitHub writes possible.
3. **Custom GPT builder:** place the essential operating contract in its instructions; attach non-secret reference material if available; use optional authorized Actions/connectors only if configured. Features vary by plan/client and should be checked in the current UI.

## First message to a new GPT

> Read the Business System Starter operating contract. Guide me through Stage 0, one question at a time. Assume I am a beginner. Build a system only for workflows I actually need. Default to private, propose before changing external systems, and keep me as owner/admin.

## Practical rule

Never paste API keys, passwords, bank details, client personal data, or tax identifiers into GPT instructions or repository files. Business-specific details belong in the owner's authorized private systems. A successful conversation is not proof that remote repositories were created.
