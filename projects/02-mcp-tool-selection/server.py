from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from runbook_catalog import list_runbooks as catalog_list_runbooks
from runbook_catalog import lookup_runbook as catalog_lookup_runbook

mcp = FastMCP("Synthetic Runbook Catalog")


@mcp.tool()
def list_runbooks(service: str | None = None) -> list[dict[str, object]]:
    """List synthetic runbooks, optionally filtered by exact service name."""
    return catalog_list_runbooks(service)


@mcp.tool()
def lookup_runbook(service: str, symptom: str) -> dict[str, object]:
    """Find a synthetic runbook by exact service and a natural-language symptom."""
    return catalog_lookup_runbook(service, symptom)


if __name__ == "__main__":
    mcp.run()
