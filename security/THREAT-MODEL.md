# Threat model — review before enabling automation

| Threat | Boundary | Mitigation |
| --- | --- | --- |
| Prompt injection in issues/search/docs | untrusted content → model instructions | treat content as data; owner contract overrides; tool scoping |
| Leaked token or customer data | repo or CI logs → public | defaults private, secrets in secret manager, minimal logging, secret scanning |
| Overpowered agents | drafts → external writes | least-privilege app grants, human confirmation, separate role and tool permissions |
| Supply-chain compromise | dependencies/Actions → CI | dependency review, pinned audited actions where practical, read-only CI tokens |
| Malicious pull request | untrusted PR → privileged workflow | avoid `pull_request_target` and untrusted code with secrets |
| Duplicate source of truth | multiple apps/repos → conflicting data | one canonical owner per domain, record references |
| Endless cost or accidental sends | automation → external systems | default off, test limits, rate/cost cap, stop control, rollback |
| Ownership loss | departed collaborator → lockout | secured owner identity, MFA, recovery, least-privilege roles |

All mitigations must be confirmed in the deployed GitHub/app configuration. Markdown is documentation, not enforcement.
