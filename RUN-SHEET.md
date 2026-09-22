# Run sheet

Ten minutes, four beats.

## Setup

```powershell
cd ghcp-demo-17-agency-plugin-evals
python -m pip install -r projects\02-mcp-tool-selection\requirements.txt
.\go.ps1 -Check
.\go.ps1
```

Keep the generated report open.

## Beat 1 — One extension type is not enough (2 minutes)

Show the three project rows in the report.

**Say:** “A skill, a tool, and a specialist agent fail differently. A single
‘did the answer look okay?’ test cannot diagnose routing, grounding, and policy
behavior.”

## Beat 2 — The prompt is not the answer key (2 minutes)

Open:

- `projects/01-skill-routing/evals/tasks/incident-brief--checkout-handoff/instruction.md`
- the sibling `task.toml`

**Say:** “The agent receives the user request and fixture. The expected tool,
keywords, and rubric remain in the grading definition. If the prompt names the
answer or tool, the eval measures obedience rather than capability.”

## Beat 3 — Negative cases catch over-triggering (3 minutes)

Search for:

```text
expected_tool = "NONE"
```

**Say:** “A plugin that activates on every request can look perfect if the suite
contains only happy paths. Every project has an unrelated request that should
not trigger its component.”

Then run:

```powershell
agency eval-new generate `
  --plugin .\projects\02-mcp-tool-selection `
  --out .\generated-evals\02-mcp-tool-selection
```

Point out that generation validates the suite without spending a model run.

## Beat 4 — CI has two evidence levels (3 minutes)

Open `.github/workflows/ci.yml` and `.github/workflows/agency-evals.yml`.

**Say:** “Hosted CI checks deterministic contracts and the real MCP protocol.
The manual self-hosted workflow runs the model-scored evals. A missing Agency
harness is not painted green.”

Close with:

```powershell
agency copilot --plugin mp:plugin-eval@curated
```

Then:

```text
/agency-eval-guide
```

## Recovery

| Problem | Response |
| --- | --- |
| `agency` is not found | Run the deterministic workshop first; install Agency before `eval-new` steps |
| `msbench-cli` is missing | Use `generate`, install the supported harness, or use Vally only for trusted local content |
| MCP import fails | `python -m pip install -r projects\02-mcp-tool-selection\requirements.txt` |
| Docker is unavailable | Materialize tasks with `generate`; do not claim a model-scored result |
| A task fails | Read its result and rubric; do not weaken the criterion just to turn it green |
