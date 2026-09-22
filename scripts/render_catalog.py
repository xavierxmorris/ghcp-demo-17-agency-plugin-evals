from __future__ import annotations

import argparse
import html
import json
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = (
    ROOT / "projects/01-skill-routing",
    ROOT / "projects/02-mcp-tool-selection",
    ROOT / "projects/03-custom-agent-regression",
)


def collect_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for project in PROJECTS:
        with (project / "plugin.json").open(encoding="utf-8") as stream:
            plugin = json.load(stream)
        for task_dir in sorted((project / "evals/tasks").iterdir()):
            if not task_dir.is_dir():
                continue
            with (task_dir / "task.toml").open("rb") as stream:
                metadata = tomllib.load(stream)["metadata"]
            prompt = (task_dir / "instruction.md").read_text(encoding="utf-8").strip()
            rows.append(
                {
                    "project": project.name,
                    "plugin": str(plugin["name"]),
                    "type": str(metadata["plugin_type"]),
                    "task": str(metadata["instance_id"]),
                    "expected_tool": str(metadata["expected_tool"]),
                    "prompt": prompt,
                }
            )
    return rows


def render(rows: list[dict[str, str]]) -> str:
    table_rows = "\n".join(
        "<tr>"
        f"<td>{html.escape(row['project'])}</td>"
        f"<td>{html.escape(row['type'])}</td>"
        f"<td><code>{html.escape(row['task'])}</code></td>"
        f"<td><code>{html.escape(row['expected_tool'])}</code></td>"
        f"<td>{html.escape(row['prompt'])}</td>"
        "</tr>"
        for row in rows
    )
    negatives = sum(row["expected_tool"] == "NONE" for row in rows)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Agency plugin eval demo</title>
  <style>
    body {{ font-family: Segoe UI, sans-serif; margin: 2rem; color: #202124; }}
    h1 {{ margin-bottom: .25rem; }}
    .summary {{ display: flex; gap: 1rem; margin: 1.5rem 0; }}
    .card {{ border: 1px solid #d0d7de; border-radius: .5rem; padding: 1rem; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #d0d7de; padding: .65rem; vertical-align: top; }}
    th {{ background: #f6f8fa; text-align: left; }}
    code {{ white-space: nowrap; }}
    .note {{ background: #fff8c5; border-left: 4px solid #9a6700; padding: 1rem; }}
  </style>
</head>
<body>
  <h1>Agency plugin eval workshop</h1>
  <p>Three component types, with grading definitions kept separate from user prompts.</p>
  <div class="summary">
    <div class="card"><strong>3</strong><br>plugins</div>
    <div class="card"><strong>{len(rows)}</strong><br>authored tasks</div>
    <div class="card"><strong>{negatives}</strong><br>negative cases</div>
  </div>
  <p class="note"><strong>No model run occurred.</strong> This report inventories the
  committed scenarios. Run <code>agency eval-new run</code> with a configured
  harness to produce scores.</p>
  <table>
    <thead><tr><th>Project</th><th>Type</th><th>Task</th><th>Expected activation</th><th>User prompt</th></tr></thead>
    <tbody>{table_rows}</tbody>
  </table>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    rows = collect_rows()
    (args.out / "catalog.json").write_text(
        json.dumps(rows, indent=2) + "\n",
        encoding="utf-8",
    )
    (args.out / "report.html").write_text(render(rows), encoding="utf-8")
    print(f"Wrote {args.out / 'report.html'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
