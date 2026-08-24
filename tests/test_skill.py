from __future__ import annotations

import csv
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "skill" / "ai-health-coach"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SkillStructureTests(unittest.TestCase):
    def test_skill_frontmatter(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\nname: ai-health-coach\n"))
        self.assertIn("\ndescription:", text)
        self.assertNotIn("TODO", text)

    def test_openai_metadata(self):
        text = (SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn('display_name: "AI Health Coach"', text)
        self.assertIn("$ai-health-coach", text)

    def test_clipper_templates_are_valid(self):
        clipper = SKILL / "assets" / "obsidian-web-clipper"
        for path in sorted(clipper.glob("*.json")):
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(data["schemaVersion"], "0.1.0")
            self.assertEqual(data["path"], "knowledge/inbox")
            self.assertEqual(data["behavior"], "create")
            names = {item["name"] for item in data["properties"]}
            self.assertTrue({"title", "source", "clipped", "status"}.issubset(names))


class WorkspaceTests(unittest.TestCase):
    def test_initialize_validate_and_preserve_existing_file(self):
        init_script = SKILL / "scripts" / "init_workspace.py"
        validate_script = SKILL / "scripts" / "validate_workspace.py"
        with tempfile.TemporaryDirectory() as temp:
            workspace = Path(temp) / "private-health-data"
            first = subprocess.run(
                [sys.executable, str(init_script), str(workspace)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(first.returncode, 0, first.stderr)
            profile = workspace / "profile" / "health-profile.md"
            profile.write_text("private test sentinel\n", encoding="utf-8")
            merge = subprocess.run(
                [sys.executable, str(init_script), str(workspace), "--merge"],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(merge.returncode, 0, merge.stderr)
            self.assertEqual(profile.read_text(encoding="utf-8"), "private test sentinel\n")
            valid = subprocess.run(
                [sys.executable, str(validate_script), str(workspace)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(valid.returncode, 0, valid.stdout + valid.stderr)

    def test_csv_headers(self):
        template = SKILL / "assets" / "starter-workspace" / "data"
        for path in sorted(template.glob("*.csv")):
            with path.open(newline="", encoding="utf-8") as handle:
                header = next(csv.reader(handle))
            self.assertGreater(len(header), 4)
            self.assertEqual(len(header), len(set(header)))

    def test_refuses_home_and_root(self):
        module = load_module("init_workspace", SKILL / "scripts" / "init_workspace.py")
        with self.assertRaises(ValueError):
            module.safe_destination(str(Path.home()))
        with self.assertRaises(ValueError):
            module.safe_destination(Path.home().anchor)
        with self.assertRaises(ValueError):
            module.safe_destination(str(REPO / "private-health-data"))


class DistributionTests(unittest.TestCase):
    def test_claude_plugin_and_marketplace_metadata(self):
        plugin = json.loads(
            (REPO / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        marketplace = json.loads(
            (REPO / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8")
        )
        self.assertEqual(plugin["name"], "ai-health-coach")
        self.assertEqual(plugin["skills"], ["./skill/ai-health-coach"])
        self.assertEqual(marketplace["name"], "ai-health-coach")
        self.assertEqual(marketplace["plugins"][0]["name"], "ai-health-coach")
        self.assertEqual(marketplace["plugins"][0]["source"], "./")

    def test_package_contains_skill_at_single_root(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "ai-health-coach.zip"
            result = subprocess.run(
                [
                    sys.executable,
                    str(REPO / "scripts" / "build_package.py"),
                    "--output",
                    str(output),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            with zipfile.ZipFile(output) as archive:
                names = archive.namelist()
            self.assertIn("ai-health-coach/SKILL.md", names)
            self.assertTrue(all(name.startswith("ai-health-coach/") for name in names))


if __name__ == "__main__":
    unittest.main()
