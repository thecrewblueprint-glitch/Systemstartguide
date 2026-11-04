# Workflows from day zero

## 0. Map the real process

For every real business workflow, record **trigger → input → owner → steps → output → verification → recovery**. Mark the current manual method before proposing automation.

## 1. Useful first workflows

- **Request intake:** capture request, deadline, evidence/source, and assigned reviewer.
- **Weekly priorities:** inspect commitments, choose one high-impact task, and record what "done" means.
- **Decision log:** capture approvals, rejected options, costs, and next review date.
- **Research:** preserve source URLs, retrieved dates, confidence, and unanswered questions.
- **Quality gate:** run validation once per meaningful batch; repair failures, rerun, then request human review.

## 2. Promote carefully

Manual checklist → assistant drafts → test on synthetic inputs → owner review → bounded execution with rollback → observed automation. Scheduled or external actions remain disabled until authorized.

## 3. Collaboration contract

Every handoff includes: `task_id`, `role`, `scope`, `inputs`, `allowed_tools`, `proposal`, `evidence`, `owner_decision`, `status`, `next_step`. Roles do not own accounts or set policy.

## 4. Audit and maintenance

Maintain a readable audit log with timestamps, actor, target, decision, evidence, outcome, and unresolved questions. Do not record raw credentials, customer data, or unnecessary personal information. Review tool permission drift and dormant workflows monthly.
