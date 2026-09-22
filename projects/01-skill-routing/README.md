# Project 01 — Skill routing

The `incident-brief` skill turns repository evidence into a concise on-call
handoff. Its evals measure:

- activation for incident-summary requests;
- separation of observation from inference;
- explicit missing-data reporting; and
- non-activation for unrelated creative work.

Load it locally:

```powershell
agency copilot --plugin local:.\projects\01-skill-routing
```

Validate and generate:

```powershell
agency eval-new doctor --plugin .\projects\01-skill-routing --no-tokens
agency eval-new generate --plugin .\projects\01-skill-routing --out .\generated-evals\01-skill-routing
```
