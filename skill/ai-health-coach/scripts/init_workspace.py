#!/usr/bin/env python3
"""Create a private AI Health Coach workspace without overwriting user files."""

from __future__ import annotations

import argparse
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


SCHEMA_VERSION = "1.0"


def safe_destination(raw_path: str) -> Path:
    destination = Path(raw_path).expanduser().resolve()
    home = Path.home().resolve()
    if destination == Path(destination.anchor) or destination == home:
        raise ValueError("Choose a dedicated subfolder, not the filesystem root or home folder.")

    script_path = Path(__file__).resolve()
    for ancestor in script_path.parents:
        if (ancestor / ".git").exists():
            if destination == ancestor or destination.is_relative_to(ancestor):
                raise ValueError(
                    "Keep private health data outside the cloned public repository."
                )
            break
    return destination


def copy_missing(source: Path, destination: Path) -> tuple[int, int]:
    created = 0
    skipped = 0
    for source_path in sorted(source.rglob("*")):
        relative = source_path.relative_to(source)
        if relative.name == "gitignore.template":
            relative = relative.with_name(".gitignore")
        destination_path = destination / relative
        if source_path.is_dir():
            destination_path.mkdir(parents=True, exist_ok=True)
            continue
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        if destination_path.exists():
            skipped += 1
            continue
        shutil.copy2(source_path, destination_path)
        created += 1
    return created, skipped


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a local, private AI Health Coach data workspace."
    )
    parser.add_argument("destination", help="Dedicated folder for private health data")
    parser.add_argument(
        "--merge",
        action="store_true",
        help="Add missing starter files to an existing folder; never overwrite files",
    )
    args = parser.parse_args()

    try:
        destination = safe_destination(args.destination)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    template_root = Path(__file__).resolve().parent.parent / "assets" / "starter-workspace"
    if not template_root.is_dir():
        print(f"ERROR: Starter workspace not found: {template_root}", file=sys.stderr)
        return 2

    if destination.exists() and any(destination.iterdir()) and not args.merge:
        print(
            "ERROR: Destination is not empty. Choose another folder or pass --merge "
            "to add only missing files.",
            file=sys.stderr,
        )
        return 2


    destination.mkdir(parents=True, exist_ok=True)
    created, skipped = copy_missing(template_root, destination)

    marker = destination / ".ai-health-coach-workspace"
    if not marker.exists():
        marker.write_text(
            f"schema_version: {SCHEMA_VERSION}\n"
            f"created_utc: {datetime.now(timezone.utc).isoformat()}\n",
            encoding="utf-8",
        )
        created += 1

    print(f"Workspace ready: {destination}")
    print(f"Created {created} files; skipped {skipped} existing files.")
    print("Next: open this folder as an Obsidian vault, then ask the coach to start onboarding.")
    print("Privacy: keep this data folder separate from the public skill repository.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
