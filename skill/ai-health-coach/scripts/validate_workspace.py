#!/usr/bin/env python3
"""Validate an AI Health Coach workspace without changing it."""

from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
from pathlib import Path


REQUIRED_FILES = {
    "AGENTS.md",
    ".gitignore",
    "onboarding/status.md",
    "profile/health-profile.md",
    "goals/active-goals.md",
    "journal/index.md",
    "data/checkins.csv",
    "data/metrics.csv",
    "data/activities.csv",
    "data/nutrition.csv",
    "knowledge/index.md",
    "plans/current-plan.md",
    "audit/log.md",
}

EXPECTED_HEADERS = {
    "data/checkins.csv": [
        "date",
        "timezone",
        "sleep_hours",
        "sleep_quality_1_5",
        "energy_1_5",
        "stress_1_5",
        "soreness_1_5",
        "pain_or_symptoms",
        "notes",
    ],
    "data/metrics.csv": [
        "timestamp",
        "timezone",
        "metric",
        "value",
        "unit",
        "source",
        "capture_method",
        "notes",
    ],
    "data/activities.csv": [
        "start_time",
        "timezone",
        "activity",
        "duration_minutes",
        "distance",
        "distance_unit",
        "effort_1_10",
        "source",
        "notes",
    ],
    "data/nutrition.csv": [
        "timestamp",
        "timezone",
        "meal_or_context",
        "description",
        "energy_kcal_optional",
        "protein_g_optional",
        "source",
        "notes",
    ],
}

SENSITIVE_PATHS = [
    "onboarding/status.md",
    "profile/health-profile.md",
    "goals/active-goals.md",
    "journal/index.md",
    "data/checkins.csv",
    "knowledge/index.md",
    "plans/current-plan.md",
    "audit/log.md",
]


def git_ignored(root: Path, relative_path: str) -> bool | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "check-ignore", "-q", relative_path],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except FileNotFoundError:
        return None
    if result.returncode == 0:
        return True
    if result.returncode == 1:
        return False
    return None


def validate_csv(path: Path, expected: list[str]) -> str | None:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            header = next(csv.reader(handle), None)
    except (OSError, UnicodeError) as exc:
        return f"cannot read {path.name}: {exc}"
    if header != expected:
        return f"unexpected CSV header in {path.name}"
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a private coach workspace")
    parser.add_argument("workspace", help="Path to the private workspace")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    args = parser.parse_args()

    root = Path(args.workspace).expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []

    if not root.is_dir():
        print(f"ERROR: Workspace not found: {root}", file=sys.stderr)
        return 2

    for relative in sorted(REQUIRED_FILES):
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")

    for relative, expected in EXPECTED_HEADERS.items():
        path = root / relative
        if path.is_file():
            problem = validate_csv(path, expected)
            if problem:
                errors.append(problem)

    status_path = root / "onboarding/status.md"
    if status_path.is_file():
        text = status_path.read_text(encoding="utf-8", errors="replace")
        match = re.search(r"(?m)^status:\s*(\S+)", text)
        if not match:
            errors.append("onboarding/status.md has no status field")
        elif match.group(1) != "complete":
            warnings.append(f"onboarding status is {match.group(1)!r}, not 'complete'")

    for relative in SENSITIVE_PATHS:
        ignored = git_ignored(root, relative)
        if ignored is False:
            warnings.append(f"sensitive path is not ignored by Git: {relative}")

    inbox = root / "knowledge" / "inbox"
    if inbox.is_dir():
        for note in sorted(inbox.glob("*.md")):
            head = note.read_text(encoding="utf-8", errors="replace")[:4000]
            if not head.startswith("---\n"):
                warnings.append(f"clipping has no YAML frontmatter: {note.name}")
                continue
            for key in ("title:", "source:", "clipped:", "status:"):
                if key not in head:
                    warnings.append(f"clipping missing {key[:-1]}: {note.name}")

    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARNING: {message}")

    if errors or (args.strict and warnings):
        print(f"Validation failed: {len(errors)} errors, {len(warnings)} warnings.")
        return 1
    print(f"Workspace valid: {len(warnings)} warnings.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
