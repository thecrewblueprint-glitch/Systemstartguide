# Governance and owner-admin control

## Authority matrix

| Action | Analyst | Builder | Auditor | Coordinator | Human owner |
| --- | --- | --- | --- | --- | --- |
| Read authorized workspace docs | yes | yes | yes | yes | yes |
| Draft plans and tasks | yes | yes | yes | yes | yes |
| Change local mock files | no | in-scope | in-scope tests | no | yes |
| Merge/alter GitHub settings | no | only via explicitly scoped approval + permission | no | no | decides |
| Activate integration / publish / contact external parties / spend | no | no by default | no | no | decides and authorizes |

## Real control points

**Authentication:** personal GitHub accounts with MFA and recovery access; do not make the GPT a shared admin identity.

**Authorization:** enforce repo branch protections/rulesets, role permissions, required reviewer rules and restricted GitHub App OAuth scopes. A generated `POLICY.json` is an advisory declaration until implemented in platform controls.

**Records:** capture decisions with exact targets, rationale, cost, reversibility, owner-verified channel and execution evidence. Avoid personal and sensitive identifiers.

**Data minimization:** store sensitive live customer/staff/financial data in fit-for-purpose restricted systems; GitHub holds only code, public-safe templates, redacted metadata, and links.

**Audit:** proposed → owner-reviewed → authorized → executed → verified (or rejected/failed). Preserve failures and uncertainty. Keep rollback paths.

**Emergency stop:** revoke app access, disable schedules, pause deployment, remove compromised collaborators, inspect recent changes and preserve incident evidence. A prompt cannot override actual GitHub/app administrative controls.

**No fake controls:** templates do not replace a secure identity provider, secret manager, legal agreement, tax professional, or incident process.
