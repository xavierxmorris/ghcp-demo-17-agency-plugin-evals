# Agent contract

This repository is a public, synthetic workshop for GitHub Copilot and Agency
plugin evaluations. It is not an incident-response or production-change system.

- Keep all services, incidents, runbooks, metrics, and change plans fictional.
- Never add credentials, private URLs, customer data, or proprietary runbooks.
- Keep the three projects independent: each must remain loadable as its own
  local Agency plugin.
- Do not place grading answers in `instruction.md`; prompts must sound like real
  user requests.
- Keep each eval task directory name identical to `metadata.instance_id`.
- Every project must retain at least one negative case with
  `expected_tool = "NONE"`.
- MCP lookup results are deterministic. Do not add network access or a fallback
  that invents a runbook.
- The change-risk agent writes advice only. It never deploys, approves, or
  modifies production systems.
- Preserve LF endings for custom-agent and skill Markdown files.

Validation:

```powershell
python -m unittest discover -s tests -v
python scripts\check_repo.py
.\go.ps1 -Check
```

When Agency is installed, `go.ps1 -Check` also validates each plugin and
materializes every authored eval without running a model.
