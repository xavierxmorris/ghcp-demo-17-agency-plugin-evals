# Project 02 — MCP tool selection

This plugin exposes a synthetic runbook catalog through a local MCP server.
The catalog is deterministic and performs no network access.

Install its pinned SDK:

```powershell
python -m pip install -r requirements.txt
```

Load the plugin:

```powershell
agency copilot --plugin local:.
```

The evals distinguish:

- calling `lookup_runbook` for grounded operational data;
- using the correct service and symptom;
- returning an honest no-match result; and
- avoiding the MCP for unrelated work.
