# Repository guidance

This workshop demonstrates when to evaluate a skill, MCP server, or custom
agent instead of treating all extensions as one undifferentiated prompt.

Use Python 3.11+, the standard library for repository tooling, and
`unittest`. The MCP adapter is the only external runtime dependency and is
pinned in `projects/02-mcp-tool-selection/requirements.txt`.

Authored eval prompts are user-facing inputs. Keep expected tools, outcomes,
keywords, and rubric criteria only in `task.toml`; never leak them into
`instruction.md`.

The deterministic validation layer and the model-scored eval layer are
different:

- `python scripts/check_repo.py` validates manifests, task shape, negative
  coverage, fixtures, line endings, and public-safety rules.
- `agency eval-new generate` proves Agency can materialize the authored tasks.
- `agency eval-new run` executes model-scored evaluations and requires an
  installed harness plus Agency authentication.

Do not make hosted CI pretend that a skipped model run passed. The public CI
workflow runs deterministic checks and an MCP protocol smoke test. The
separate manual workflow targets an explicitly configured Agency self-hosted
runner.
