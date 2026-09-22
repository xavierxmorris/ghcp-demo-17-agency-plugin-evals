---
name: runbook-routing
description: Use the synthetic-runbooks MCP when a user asks for an operational runbook, first checks, or a grounded response to a named service symptom. Do not use it for creative writing, general coding, or requests with no operational lookup.
---

When a request needs a runbook:

1. Extract the service name and symptom from the user's evidence.
2. Call `lookup_runbook` rather than guessing from general knowledge.
3. Report the returned runbook ID, title, and first checks.
4. If the tool returns `not_found`, say that the synthetic catalog has no
   match. Do not fabricate a runbook or silently switch services.
5. Use `list_runbooks` only when the user asks what the catalog contains or
   when the service is known but the symptom is genuinely ambiguous.

Never present this synthetic catalog as a production source.
