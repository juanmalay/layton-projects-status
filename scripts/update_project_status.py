#!/usr/bin/env python3
"""Sync public project status metadata into a status JSON repository."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


METADATA_FIELDS = {"lastCommit", "updatedAt"}


def run_git(args: list[str], cwd: Path) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as file:
        return json.load(file)


def write_json(path: Path, payload: Any) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)
        file.write("\n")


def current_metadata(source_repo: Path, branch: str | None) -> dict[str, Any]:
    message = run_git(["show", "-s", "--format=%s", "HEAD"], source_repo)
    commit_date = run_git(["show", "-s", "--format=%cI", "HEAD"], source_repo)
    resolved_branch = branch or os.environ.get("GITHUB_REF_NAME")
    if not resolved_branch:
        resolved_branch = run_git(["rev-parse", "--abbrev-ref", "HEAD"], source_repo)

    return {
        "lastCommit": {
            "message": message.strip(),
            "date": commit_date,
            "branch": resolved_branch,
        },
        "updatedAt": datetime.now(timezone.utc).isoformat(),
    }


def apply_metadata(project: dict[str, Any], metadata: dict[str, Any]) -> None:
    for field in METADATA_FIELDS:
        project[field] = metadata[field]


def update_detail_file(path: Path, metadata: dict[str, Any]) -> None:
    detail = read_json(path)
    if not isinstance(detail, dict):
        raise ValueError(f"{path} must contain a JSON object.")

    apply_metadata(detail, metadata)
    write_json(path, detail)


def update_projects_index(
    path: Path,
    project_id: str,
    metadata: dict[str, Any],
) -> None:
    projects = read_json(path)
    if not isinstance(projects, list):
        raise ValueError(f"{path} must contain a JSON array.")

    for item in projects:
        if isinstance(item, dict) and item.get("id") == project_id:
            apply_metadata(item, metadata)
            write_json(path, projects)
            return

    raise ValueError(f'Project id "{project_id}" was not found in {path}.')


def validate_json(paths: list[Path]) -> None:
    for path in paths:
        read_json(path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Update public status metadata for one project.",
    )
    parser.add_argument(
        "--source-repo",
        default=".",
        help="Repository containing the commit metadata to publish.",
    )
    parser.add_argument(
        "--status-repo",
        required=True,
        help="Checked-out status repository path.",
    )
    parser.add_argument(
        "--project-id",
        default="layton-projects-status",
        help="Project id to update in projects.json.",
    )
    parser.add_argument(
        "--detail-path",
        default="projects/layton-projects-status.json",
        help="Project detail JSON path inside the status repository.",
    )
    parser.add_argument(
        "--branch",
        default=None,
        help="Branch name to publish in lastCommit.branch.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source_repo = Path(args.source_repo).resolve()
    status_repo = Path(args.status_repo).resolve()
    detail_path = status_repo / args.detail_path
    index_path = status_repo / "projects.json"

    if not detail_path.is_file():
        raise FileNotFoundError(f"Detail JSON not found: {detail_path}")
    if not index_path.is_file():
        raise FileNotFoundError(f"Projects index not found: {index_path}")

    metadata = current_metadata(source_repo, args.branch)
    update_detail_file(detail_path, metadata)
    update_projects_index(index_path, args.project_id, metadata)
    validate_json([detail_path, index_path])

    print(f'Updated public metadata for "{args.project_id}".')


if __name__ == "__main__":
    main()
