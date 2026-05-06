import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class SampleGenerationTest(unittest.TestCase):
    def run_reporter(self, script_name, input_dir, output_dir, home_dir):
        env = os.environ.copy()
        env["HOME"] = str(home_dir)
        return subprocess.run(
            [
                sys.executable,
                str(ROOT / script_name),
                "--device",
                "sample",
                "--input-dir",
                str(ROOT / input_dir),
                "--output-dir",
                str(output_dir),
                "--week",
                "2026-W15",
            ],
            cwd=str(ROOT),
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )

    def test_claude_sample_generates_markdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            output_dir = tmp_path / "reports"
            home_dir = tmp_path / "home"
            home_dir.mkdir()

            self.run_reporter(
                "claude_weekly_summary.py",
                "samples/claude-code",
                output_dir,
                home_dir,
            )

            report = output_dir / "2026-W15" / "cc-sample.md"
            content = report.read_text(encoding="utf-8")
            self.assertIn("Claude Code Weekly Summary - 2026-W15", content)
            self.assertIn("Project Stats", content)
            self.assertIn("sample-web-app", content)
            self.assertFalse((home_dir / ".claude").exists())
            self.assertFalse((home_dir / ".codex").exists())

    def test_codex_sample_generates_markdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            output_dir = tmp_path / "reports"
            home_dir = tmp_path / "home"
            home_dir.mkdir()

            self.run_reporter(
                "codex_weekly_summary.py",
                "samples/codex",
                output_dir,
                home_dir,
            )

            report = output_dir / "2026-W15" / "cd-sample.md"
            content = report.read_text(encoding="utf-8")
            self.assertIn("Codex Weekly Summary - 2026-W15", content)
            self.assertIn("Project Stats", content)
            self.assertIn("sample-workflow-demo", content)
            self.assertFalse((home_dir / ".claude").exists())
            self.assertFalse((home_dir / ".codex").exists())


if __name__ == "__main__":
    unittest.main()

