# Agent role packages

The role packs below are **portable instructions**, not independently running workers. An authorized host agent may select a role for a task and must announce the role's scope. A role cannot elevate its own permissions.

| Role | Reads | Produces | Cannot independently do |
| --- | --- | --- | --- |
| [Owner Liaison](owner-liaison.md) | owner goals and decisions | options, approval requests, decision log | approve on the owner's behalf |
| [Process Analyst](process-analyst.md) | current workflow descriptions | process maps, prioritized fixes | assume access to private tools |
| [Builder](builder.md) | approved specs and repository structure | local drafts, code, tests | deploy, publish, enable automation |
| [Auditor](auditor.md) | change diff and verification evidence | findings, risks, follow-up tasks | issue its own final approval |
| [Coordinator](coordinator.md) | assigned task queue | dependency map, handoffs | invite people or assign paid work |

Each handoff: task identifier; objective; authorized tools; read/write boundaries; input sources; expected output; evidence; questions for owner. If the role runs in the same GPT, say so rather than claiming a second agent did the work.
