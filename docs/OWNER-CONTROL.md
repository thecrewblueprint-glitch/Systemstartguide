# Owner Control and Governance

## Decision rights

| Class | Examples | Authority |
| --- | --- | --- |
| Read/plan | summarize requirements, run local tests, produce repo proposals | in-scope assistant may do |
| Internal low-risk editing | task drafts, docs changes in authorized branch | configured repository permissions |
| External change | repo creation, invites, publish, automation activation, messages, deployment | explicit owner authorization + scoped tool access |
| Sensitive/irreversible | delete, spend, security permission changes, legal commitments, bulk export | owner-led review, independent confirmation where available |

## Minimum repository controls

- Owner retains at least one independently secured administrator account, with MFA and recovery capability.
- Use per-repo collaborator permissions and least-privilege connectors. No shared account passwords.
- Protect the default branch: require pull requests / reviews / CI as appropriate and prevent uncontrolled force pushes. Some protections require GitHub plan or settings.
- Restrict Actions tokens to read by default. Never run untrusted PR code with secrets or elevated tokens.
- Store credentials in a dedicated secret manager or GitHub secrets, **not** committed code.
- Keep a decision log, audit trail, backup/export procedure, and incident stop/revoke playbook.
- Separate public templates from private client and business data.

## Approval record (documentation only)

An approval log is evidence, **not** a technical permission system.

```text
Decision ID:
Requested by:
Action and exact target:
Why:
Data sensitivity:
Estimated cost:
Approver and verified channel:
Decision (approved/declined):
Date:
Execution link:
Verification evidence:
Rollback/stop plan:
```

## Owner emergency stop

Disable affected third-party integrations/scheduled automation, revoke impacted tokens, pause deployment pipelines, restrict collaborators, and preserve non-sensitive audit evidence. Use GitHub and app administration controls directly. Agents cannot bypass these controls or restore their own access.
