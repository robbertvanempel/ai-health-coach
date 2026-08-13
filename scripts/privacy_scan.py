#!/usr/bin/env python3
"""Fail when public-repository files contain likely secrets or private data."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", "dist"}
TEXT_SUFFIXES = {
    "",
    ".md",
    ".py",
    ".json",
    ".yaml",
    ".yml",
    ".csv",
    ".txt",
    ".toml",
    ".gitignore",
}

RULES = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "secret assignment": re.compile(
        r"(?i)\b(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\b\s*[:=]\s*['\"][^'\"]{8,}"
    ),
    "OpenAI-style key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "GitHub token": re.compile(r"\bgh[opsu]_[A-Za-z0-9]{20,}\b"),
    "xAI key": re.compile(r"\bxai-[A-Za-z0-9_-]{20,}\b"),
    "local home path": re.compile(r"/(?:Users|home)/[^/\s]+/"),
    "private memory path": re.compile(r"\.codex/(?:memory|agents)/"),
    "health-record identifier": re.compile(r"(?i)\b(?:patient id|medical record number|bsn)\s*[:#]"),
}

EMAIL = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
ALLOWED_EMAIL_DOMAINS = {"example.com", "users.noreply.github.com"}


def text_files(root: Path):
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.name == ".gitignore" or path.suffix.lower() in TEXT_SUFFIXES:
            yield path


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan the public repo for likely private data")
    parser.add_argument("path", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.path).resolve()
    findings: list[str] = []

    for path in text_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeError:
            continue
        relative = path.relative_to(root)
        for line_number, line in enumerate(text.splitlines(), start=1):
            for label, pattern in RULES.items():
                if pattern.search(line):
                    findings.append(f"{relative}:{line_number}: {label}")
            for address in EMAIL.findall(line):
                domain = address.rsplit("@", 1)[1].lower()
                if domain not in ALLOWED_EMAIL_DOMAINS:
                    findings.append(f"{relative}:{line_number}: email address")

    if findings:
        for finding in findings:
            print(f"FAIL: {finding}")
        print(f"Privacy scan failed with {len(findings)} finding(s).")
        return 1
    print("Privacy scan passed: no likely secrets, local paths, or personal identifiers found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
