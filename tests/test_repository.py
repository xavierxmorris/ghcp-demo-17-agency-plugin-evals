from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

from scripts import check_repo, render_catalog

ROOT = Path(__file__).resolve().parents[1]
MCP_PROJECT = ROOT / "projects/02-mcp-tool-selection"


def load_runbook_catalog():
    path = MCP_PROJECT / "runbook_catalog.py"
    spec = importlib.util.spec_from_file_location("runbook_catalog", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load runbook_catalog")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class RepositoryTests(unittest.TestCase):
    def test_repository_contracts(self) -> None:
        self.assertEqual(check_repo.main(), 0)

    def test_catalog_contains_all_tasks(self) -> None:
        rows = render_catalog.collect_rows()
        self.assertEqual(len(rows), 9)
        self.assertEqual(
            sum(row["expected_tool"] == "NONE" for row in rows),
            3,
        )

    def test_report_is_explicit_about_no_model_run(self) -> None:
        page = render_catalog.render(render_catalog.collect_rows())
        self.assertIn("No model run occurred", page)
        self.assertIn("agency eval-new run", page)

    def test_runbook_lookup_is_deterministic(self) -> None:
        catalog = load_runbook_catalog()
        result = catalog.lookup_runbook("checkout-api", "requests timing out")
        self.assertEqual(result["status"], "matched")
        self.assertEqual(result["runbook_id"], "RB-CHK-017")
        self.assertEqual(result["service"], "checkout-api")

    def test_unknown_runbook_does_not_fabricate(self) -> None:
        catalog = load_runbook_catalog()
        result = catalog.lookup_runbook("unknown-service", "latency")
        self.assertEqual(result["status"], "not_found")
        self.assertNotIn("runbook_id", result)

    def test_catalog_json_is_serializable(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "catalog.json"
            output.write_text(
                json.dumps(render_catalog.collect_rows()),
                encoding="utf-8",
            )
            self.assertGreater(output.stat().st_size, 100)


if __name__ == "__main__":
    unittest.main()
