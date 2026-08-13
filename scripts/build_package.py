#!/usr/bin/env python3
"""Build a deterministic skill ZIP for UI-based installers."""

from __future__ import annotations

import argparse
import hashlib
import zipfile
from pathlib import Path


FIXED_TIMESTAMP = (2026, 1, 1, 0, 0, 0)


def build(source: Path, output: Path) -> str:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source.rglob("*")):
            if path.is_dir() or path.name in {".DS_Store"} or "__pycache__" in path.parts:
                continue
            relative = Path(source.name) / path.relative_to(source)
            info = zipfile.ZipInfo(relative.as_posix(), FIXED_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o755 if path.suffix == ".py" else 0o644) << 16
            archive.writestr(info, path.read_bytes())
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    output.with_suffix(output.suffix + ".sha256").write_text(
        f"{digest}  {output.name}\n", encoding="utf-8"
    )
    return digest


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the AI Health Coach skill ZIP")
    parser.add_argument("--output", default="dist/ai-health-coach.zip")
    args = parser.parse_args()

    repo = Path(__file__).resolve().parent.parent
    source = repo / "skill" / "ai-health-coach"
    output = Path(args.output)
    if not output.is_absolute():
        output = repo / output
    if not (source / "SKILL.md").is_file():
        raise SystemExit(f"Missing skill source: {source}")

    digest = build(source, output)
    print(f"Built {output}")
    print(f"SHA-256 {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
