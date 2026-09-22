# Workshop — Build evidence for an Agency plugin

**Duration:** 60 minutes
**Outcome:** participants can choose an eval shape, author realistic scenarios,
materialize them, and distinguish deterministic CI from model-scored evidence.

## 1. Baseline the repository (5 minutes)

```powershell
python -m pip install -r projects\02-mcp-tool-selection\requirements.txt
.\go.ps1 -Check
```

Keep the output. It is the baseline for your changes.

## 2. Compare the three component types (10 minutes)

Read each plugin manifest and component:

```text
projects/01-skill-routing/skills/incident-brief/SKILL.md
projects/02-mcp-tool-selection/.mcp.json
projects/03-custom-agent-regression/agents/change-risk-reviewer.md
```

Record which failure each project is designed to detect:

- skill: routing and response-shape failure;
- MCP: tool-choice or grounded-data failure;
- agent: multi-step policy and artifact failure.

## 3. Inspect prompt/grader separation (10 minutes)

For one task, compare `instruction.md` with `task.toml`.

The instruction should contain only a plausible user request. The task
metadata holds:

- component identity;
- expected tool or `NONE`;
- expected outcome and keywords;
- rubric criteria;
- allowed skills, agents, or MCP tools;
- expected workspace artifacts.

If a prompt says “call lookup_runbook and return RB-CHK-017,” rewrite it. That
prompt already performed the routing and lookup.

## 4. Add an edge case with the Eval Guide (15 minutes)

Start:

```powershell
agency copilot --plugin mp:plugin-eval@curated
```

Invoke `/agency-eval-guide`, select one project, and use a prompt from
[PROMPTS.md](PROMPTS.md).

Review every generated file. Ensure:

1. the task directory equals `metadata.instance_id`;
2. the prompt sounds like a user;
3. fixtures contain enough context to act;
4. the expected answer is absent from the prompt;
5. the rubric distinguishes a real regression from stylistic variation.

## 5. Validate without spending a model run (10 minutes)

```powershell
python scripts\check_repo.py

agency eval-new doctor `
  --plugin .\projects\01-skill-routing `
  --no-tokens

agency eval-new generate `
  --plugin .\projects\01-skill-routing `
  --out .\generated-evals\01-skill-routing
```

Repeat for the project you changed.

## 6. Run and diagnose one task (10 minutes)

With a configured harness:

```powershell
agency eval-new run `
  --plugin .\projects\01-skill-routing `
  --task incident-brief--checkout-handoff `
  --keep-tempdir
```

If it fails, classify the failure before editing:

| Class | Typical evidence |
| --- | --- |
| Routing | Correct component never activated |
| Tool selection | Wrong tool or no tool call |
| Grounding | Tool ran, but response ignored or contradicted it |
| Fixture | Required evidence was absent or ambiguous |
| Rubric | Correct behavior failed because the criterion was overly specific |
| Nondeterminism | Repeated runs differ without a product change |

Do not lower a criterion solely because a run is red.

## Evidence to keep

- deterministic check output;
- generated task directory;
- `summary.json` from model-scored runs;
- changed task definitions and fixtures;
- a short failure classification for any red scenario.

## Limits

This workshop does not prove production readiness, security compliance, or
universal model behavior. It proves that the selected scenarios were executed
under the recorded harness, model, plugin, fixtures, and rubric.
