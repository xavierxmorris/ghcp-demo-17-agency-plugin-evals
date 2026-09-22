# Demo 17 — Evaluate skills, MCP tools, and custom agents with Agency

**GitHub Copilot workshop | three plugin types | authored scenarios | negative cases | regression CI**

This repository turns “the plugin looked good in chat” into repeatable evidence.
It contains three small, independent Agency plugins that teach the strongest
evaluation use cases:

| Project | Best use case | What the eval proves |
| --- | --- | --- |
| [01 — Skill routing](projects/01-skill-routing) | Instructions should activate only for the right request and produce a stable response shape | Correct routing, evidence use, missing-data honesty, and non-activation for unrelated work |
| [02 — MCP tool selection](projects/02-mcp-tool-selection) | A model must call a deterministic system rather than invent an answer | Correct tool choice, correct runbook result, unknown-input handling, and no tool call for unrelated work |
| [03 — Custom-agent behavior](projects/03-custom-agent-regression) | A multi-step specialist must apply policy and create a reviewable artifact | Policy-grounded classification, explicit missing evidence, bounded behavior, and artifact creation |

All incidents, services, runbooks, and change plans are fictional.

## Quick start

Prerequisites:

- PowerShell 7+
- Python 3.11+
- Agency CLI `2026.9.16.4` or newer for Agency-specific checks
- Docker plus MSBench, or Vally, only when running model-scored evals

Run the deterministic gate:

```powershell
.\go.ps1 -Check
```

Generate the presenter report:

```powershell
.\go.ps1
```

The report lists every scenario and keeps the grading definition separate from
the prompt the evaluated agent receives.

## Use the Agency Eval Guide

Open a Copilot session with the curated eval plugin:

```powershell
agency copilot --plugin mp:plugin-eval@curated
```

Then invoke:

```text
/agency-eval-guide
```

Ask it to inspect one project at a time. Suggested prompts are in
[PROMPTS.md](PROMPTS.md).

The guide is a scaffolder, not an oracle. Review generated prompts for answer
leakage, add realistic fixtures, and keep at least one negative case.

## Validate and materialize authored evals

Use the same loop for each project:

```powershell
$plugin = ".\projects\01-skill-routing"
agency plugin check $plugin
agency eval-new doctor --plugin $plugin --no-tokens
agency eval-new generate --plugin $plugin --out .\generated-evals\01-skill-routing
```

`doctor` reports missing local harnesses as warnings unless `--strict` is
supplied. `generate` does not run a model; it proves Agency can convert the
authored task definitions into runnable evaluation tasks.

## Run model-scored evals

Run one changed scenario first:

```powershell
agency eval-new run `
  --plugin .\projects\01-skill-routing `
  --task incident-brief--checkout-handoff `
  --keep-tempdir
```

Then run the complete plugin suite:

```powershell
agency eval-new run --plugin .\projects\01-skill-routing --workers 2
agency eval-new run --plugin .\projects\02-mcp-tool-selection --workers 2
agency eval-new run --plugin .\projects\03-custom-agent-regression --workers 2
```

Use MSBench for isolated or publishable results. Vally is faster for trusted
local content but runs as the invoking user and is not an isolation boundary:

```powershell
agency eval-new run --plugin .\projects\01-skill-routing --harness vally
```

Each run produces per-task results and a `summary.json`.

## Regression CI

Two workflows deliberately separate deterministic evidence from model-scored
evidence:

- [`ci.yml`](.github/workflows/ci.yml) runs on GitHub-hosted Windows and Linux
  runners. It validates all manifests and task contracts, runs unit tests, and
  launches the local MCP server through the official Python SDK.
- [`agency-evals.yml`](.github/workflows/agency-evals.yml) is manual and targets
  a self-hosted runner labelled `agency`. It validates, materializes, and can
  optionally execute the full model-scored suites.

This separation prevents a missing private harness or Agency login from being
reported as a successful evaluation.

## Workshop materials

- [RUN-SHEET.md](RUN-SHEET.md) — 10-minute presenter flow
- [WORKSHOP.md](WORKSHOP.md) — 60-minute participant lab
- [PROMPTS.md](PROMPTS.md) — Eval Guide and Copilot prompts

## Honesty notes

- The committed scores are not pre-baked claims; run the suites in your own
  configured environment and inspect `summary.json`.
- Public CI proves repository shape and MCP protocol behavior. It does not
  substitute for a model-scored run.
- The local MCP uses a synthetic in-memory catalog and performs no network
  access.
- The custom agent produces a recommendation artifact only. It never approves
  or executes a change.
- Agency `eval-new` is experimental and hidden from `agency --help`; flags and
  output may change.

## Sources

The demo targets Agency CLI `2026.9.16.4` and the authored-eval layout
documented by Agency’s Evals guides. The MCP protocol adapter pins the official
Model Context Protocol Python SDK to `1.30.0`; SDK 2.x renamed `FastMCP` and
requires a separate migration.
