---
name: incident-brief
description: Create an evidence-grounded incident handoff from notes, metrics, and repository context. Use when asked for an incident summary, on-call handoff, status snapshot, or known-unknowns list. Do not use for launch announcements, general creative writing, or unrelated documentation.
---

Create a concise incident handoff from the evidence available in the workspace.

1. Read the incident notes and any metrics or service context.
2. Separate observed facts from hypotheses. Never promote an inference to fact.
3. If severity is not explicitly stated, write `Severity: unconfirmed`.
4. Write `incident-brief.md` with these headings:
   - `Severity`
   - `Customer impact`
   - `Observed evidence`
   - `Known unknowns`
   - `Next actions`
5. Preserve identifiers and timestamps exactly as supplied.
6. Do not invent owners, root causes, mitigations, or recovery times.

Keep the handoff useful to the next on-call engineer: brief, explicit, and
honest about missing information.
