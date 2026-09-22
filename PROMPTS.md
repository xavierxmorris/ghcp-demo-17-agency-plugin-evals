# Prompts

## Start the Eval Guide

```powershell
agency copilot --plugin mp:plugin-eval@curated
```

Inside the session:

```text
/agency-eval-guide
```

## Project 1 — skill routing

```text
Inspect projects/01-skill-routing. Review its authored evals for realistic user
language, answer leakage, happy-path coverage, incomplete evidence, and
over-trigger prevention. Preserve the synthetic incident domain.
```

Useful follow-up:

```text
Propose one additional edge case that tests whether the skill distinguishes
observed evidence from an inference. Do not put the expected answer in the user
prompt.
```

## Project 2 — MCP tool selection

```text
Inspect projects/02-mcp-tool-selection. Check whether the evals prove that the
agent calls lookup_runbook when grounded data is required, handles no-match
results honestly, and avoids the MCP for unrelated requests.
```

Useful follow-up:

```text
Add a scenario where two runbooks share a symptom but only one matches the
service. Grade tool choice and returned runbook identity separately.
```

## Project 3 — custom-agent behavior

```text
Inspect projects/03-custom-agent-regression. Check whether the evals measure
policy use, explicit missing evidence, bounded behavior, and creation of the
change-risk-review.md artifact.
```

Useful follow-up:

```text
Add a boundary case where the change is low impact but has no rollback test.
The prompt must sound like a change owner asking for review, not a test author
describing the desired verdict.
```

## Run one scenario while iterating

```powershell
agency eval-new run `
  --plugin .\projects\03-custom-agent-regression `
  --task change-risk-reviewer--missing-rollback-evidence `
  --keep-tempdir
```

## Ask Copilot to diagnose a red result

```text
Read the selected eval result, its task.toml, instruction.md, and fixtures.
Classify the failure as routing, tool selection, evidence use, rubric mismatch,
or nondeterminism. Do not weaken the rubric until you show why the expected
behavior is wrong.
```
