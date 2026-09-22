from __future__ import annotations

import sys
import unittest
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "projects/02-mcp-tool-selection"


class McpProtocolTests(unittest.IsolatedAsyncioTestCase):
    async def test_server_lists_and_calls_lookup_tool(self) -> None:
        parameters = StdioServerParameters(
            command=sys.executable,
            args=[str(PROJECT / "server.py")],
            cwd=PROJECT,
        )
        async with stdio_client(parameters) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools = await session.list_tools()
                self.assertIn("lookup_runbook", [tool.name for tool in tools.tools])

                result = await session.call_tool(
                    "lookup_runbook",
                    arguments={
                        "service": "checkout-api",
                        "symptom": "requests timing out",
                    },
                )
                self.assertFalse(result.isError)
                self.assertEqual(
                    result.structuredContent["runbook_id"],
                    "RB-CHK-017",
                )


if __name__ == "__main__":
    unittest.main()
