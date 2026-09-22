from __future__ import annotations

import json
import re
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Project:
    path: Path
    component_type: str
    component_name: str


PROJECTS = (
    Project(ROOT / "projects/01-skill-routing", "skill", "incident-brief"),
    Project(ROOT / "projects/02-mcp-tool-selection", "mcp", "lookup_runbook"),
    Project(
        ROOT / "projects/03-custom-agent-regression",
        "agent",
        "change-risk-reviewer",
    ),
)

SENSITIVE_PATTERNS = (
    re.compile(r"\b(?:password|secret|api[_-]?key)\s*[:=]\s*\S+", re.IGNORECASE),
    re.compile(r"https://(?:dev\.azure|microsoft)\.com/", re.IGNORECASE),
)


def load_json(path: Path) -> dict[str, object]:
    with path.open(encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain a JSON object")
    return value


def load_task(path: Path) -> dict[str, object]:
    with path.open("rb") as stream:
        value = tomllib.load(stream)
    metadata = value.get("metadata")
    if not isinstance(metadata, dict):
        raise ValueError(f"{path.relative_to(ROOT)} is missing [metadata]")
    return metadata


def task_directories(project: Project) -> list[Path]:
    tasks = project.path / "evals/tasks"
    if not tasks.is_dir():
        raise ValueError(f"{tasks.relative_to(ROOT)} is missing")
    return sorted(path for path in tasks.iterdir() if path.is_dir())


def validate_project(project: Project, errors: list[str]) -> None:
    try:
        plugin = load_json(project.path / "plugin.json")
        agency = load_json(project.path / "agency.json")
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as exc:
        errors.append(str(exc))
        return

    plugin_name = plugin.get("name")
    if not isinstance(plugin_name, str) or not plugin_name:
        errors.append(f"{project.path.relative_to(ROOT)}/plugin.json has no name")

    if agency.get("engines") != ["copilot"]:
        errors.append(
            f"{project.path.relative_to(ROOT)}/agency.json must target copilot"
        )

    negatives = 0
    positives = 0
    try:
        directories = task_directories(project)
    except ValueError as exc:
        errors.append(str(exc))
        return

    if len(directories) < 3:
        errors.append(
            f"{project.path.relative_to(ROOT)} needs at least three authored tasks"
        )

    for task_dir in directories:
        task_file = task_dir / "task.toml"
        instruction_file = task_dir / "instruction.md"
        if not task_file.is_file() or not instruction_file.is_file():
            errors.append(
                f"{task_dir.relative_to(ROOT)} needs task.toml and instruction.md"
            )
            continue

        try:
            metadata = load_task(task_file)
        except (tomllib.TOMLDecodeError, ValueError) as exc:
            errors.append(str(exc))
            continue

        instance_id = metadata.get("instance_id")
        if instance_id != task_dir.name:
            errors.append(
                f"{task_dir.relative_to(ROOT)} must match instance_id {instance_id!r}"
            )

        if metadata.get("plugin") != plugin_name:
            errors.append(
                f"{task_file.relative_to(ROOT)} plugin must be {plugin_name!r}"
            )

        if metadata.get("plugin_type") != project.component_type:
            errors.append(
                f"{task_file.relative_to(ROOT)} plugin_type must be "
                f"{project.component_type!r}"
            )

        criteria = metadata.get("criteria")
        if not isinstance(criteria, list) or len(criteria) < 2:
            errors.append(f"{task_file.relative_to(ROOT)} needs at least two criteria")

        expected_tool = metadata.get("expected_tool")
        if expected_tool == "NONE":
            negatives += 1
        else:
            positives += 1
            if expected_tool != project.component_name:
                errors.append(
                    f"{task_file.relative_to(ROOT)} expected_tool must be "
                    f"{project.component_name!r} or 'NONE'"
                )

        prompt = instruction_file.read_text(encoding="utf-8")
        if len(prompt.strip()) < 30:
            errors.append(f"{instruction_file.relative_to(ROOT)} is too short")
        if "expected_tool" in prompt or "expected_outcome" in prompt:
            errors.append(
                f"{instruction_file.relative_to(ROOT)} leaks grader vocabulary"
            )

    if negatives < 1:
        errors.append(f"{project.path.relative_to(ROOT)} needs a negative task")
    if positives < 2:
        errors.append(f"{project.path.relative_to(ROOT)} needs two positive tasks")


def validate_line_endings(errors: list[str]) -> None:
    files = list(ROOT.glob("projects/**/SKILL.md"))
    files.extend(ROOT.glob("projects/**/agents/*.md"))
    for path in files:
        if b"\r" in path.read_bytes():
            errors.append(f"{path.relative_to(ROOT)} must use LF line endings")


def validate_public_safety(errors: list[str]) -> None:
    for path in ROOT.glob("projects/**/*"):
        if not path.is_file() or path.suffix not in {".md", ".json", ".toml", ".csv"}:
            continue
        text = path.read_text(encoding="utf-8")
        for pattern in SENSITIVE_PATTERNS:
            if pattern.search(text):
                errors.append(
                    f"{path.relative_to(ROOT)} matches sensitive pattern "
                    f"{pattern.pattern!r}"
                )


def validate_mcp_project(errors: list[str]) -> None:
    project = ROOT / "projects/02-mcp-tool-selection"
    config = load_json(project / ".mcp.json")
    servers = config.get("mcpServers")
    if not isinstance(servers, dict) or "synthetic-runbooks" not in servers:
        errors.append("MCP config must define synthetic-runbooks")

    requirement = (project / "requirements.txt").read_text(encoding="utf-8").strip()
    if requirement != "mcp==1.30.0":
        errors.append("MCP SDK must remain pinned to mcp==1.30.0")


def main() -> int:
    errors: list[str] = []
    for project in PROJECTS:
        validate_project(project, errors)
    validate_line_endings(errors)
    validate_public_safety(errors)
    validate_mcp_project(errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    task_count = sum(len(task_directories(project)) for project in PROJECTS)
    print(f"OK: 3 plugins, {task_count} authored tasks, negative coverage in each")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
