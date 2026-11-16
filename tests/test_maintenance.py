"""Offline consumer regressions for interpreter admission and tracked inventory.

Run with Python's standard-library unittest runner. All shell and Git operations
use disposable directories; no parser installation or external service is used.
"""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SOURCE_ROOT = Path(__file__).resolve().parents[1]


def required_program(name: str) -> str:
    path = shutil.which(name)
    if path is None:
        raise RuntimeError(f"The offline regression suite requires {name} on PATH")
    return path


class TemporaryWorkspace(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="gen25 maintenance ")
        self.addCleanup(temporary.cleanup)
        self.workspace = Path(temporary.name)
        self.repo = self.workspace / "repository with spaces"
        self.repo.mkdir()
        self.caller = self.workspace / "outside caller"
        self.caller.mkdir()
        home = self.workspace / "home"
        home.mkdir()
        self.environment = {
            name: value
            for name, value in os.environ.items()
            if not name.startswith(("GIT_", "GNN_"))
            and name not in {"PYTHONHOME", "PYTHONPATH"}
        }
        self.environment.update(
            HOME=str(home),
            GIT_CONFIG_GLOBAL=os.devnull,
            GIT_CONFIG_NOSYSTEM="1",
            GIT_OPTIONAL_LOCKS="0",
            GIT_TERMINAL_PROMPT="0",
            PYTHONDONTWRITEBYTECODE="1",
            PYTHONNOUSERSITE="1",
        )

    def command(self, argv: list[str], *, environment: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            argv,
            cwd=self.caller,
            env=self.environment if environment is None else environment,
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )

    def copy_source(self, relative: str) -> Path:
        target = self.repo / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SOURCE_ROOT / relative, target)
        return target


class InterpreterAdmissionTests(TemporaryWorkspace):
    def setUp(self) -> None:
        super().setUp()
        self.bash = required_program("bash")
        self.copy_source("run.sh")
        self.copy_source("scripts/gnn_conformance.py")
        self.default_python = self.repo / ".venv" / "gnn" / "bin" / "python"
        tools = self.workspace / "tools"
        tools.mkdir()
        # A real dirname is needed by run.sh. Excluding uv makes all old-code
        # failure paths finite and offline, rather than simulating bootstrap.
        (tools / "dirname").symlink_to(required_program("dirname"))
        self.environment["PATH"] = str(tools)

    def run_gnn(self, override: str | None = None) -> subprocess.CompletedProcess[str]:
        environment = dict(self.environment)
        if override is not None:
            environment["GNN_PYTHON"] = override
        return self.command([self.bash, str(self.repo / "run.sh"), "gnn"], environment=environment)

    def assert_conformance_preflight(self, result: subprocess.CompletedProcess[str]) -> None:
        # The real conformance script rejects the deliberately absent pin before
        # ensure_parser can install anything. This is not a fake successful run.
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("gnn-conformance: .github/gnn-pin.json is missing", result.stderr)
        self.assertNotIn("GNN_PYTHON is not an executable file", result.stderr)
        self.assertNotIn("'uv' is required", result.stderr)

    def test_invalid_explicit_interpreters_fail_before_bootstrap(self) -> None:
        non_executable = self.workspace / "non executable python"
        non_executable.write_text("raise SystemExit(99)\n", encoding="utf-8")
        non_executable.chmod(0o600)
        directory = self.workspace / "interpreter directory"
        directory.mkdir()
        overrides = [str(self.workspace / "missing python"), str(non_executable), str(directory), ""]
        for override in overrides:
            with self.subTest(override=override):
                result = self.run_gnn(override)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("run.sh: GNN_PYTHON is not an executable file:", result.stderr)
                self.assertNotIn("'uv' is required", result.stderr)
                self.assertNotIn("gnn-conformance:", result.stderr)
                self.assertFalse((self.repo / ".venv").exists())

    def test_valid_explicit_interpreter_runs_real_conformance_without_bootstrap(self) -> None:
        interpreter = self.workspace / "explicit interpreter"
        interpreter.symlink_to(sys.executable)
        self.assert_conformance_preflight(self.run_gnn(str(interpreter)))
        self.assertFalse((self.repo / ".venv").exists())

    def test_existing_default_interpreter_is_used_when_override_is_unset(self) -> None:
        self.default_python.parent.mkdir(parents=True)
        self.default_python.symlink_to(sys.executable)
        self.assert_conformance_preflight(self.run_gnn())
        self.assertEqual(self.default_python.resolve(), Path(sys.executable).resolve())

    def test_missing_default_retains_uv_prerequisite_when_override_is_unset(self) -> None:
        result = self.run_gnn()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("'uv' is required but not on PATH", result.stderr)
        self.assertNotIn("GNN_PYTHON is not an executable file", result.stderr)
        self.assertFalse((self.repo / ".venv").exists())


class TrackedInventoryTests(TemporaryWorkspace):
    BASE_METRICS = {
        "Tracked files": 9,
        "Tracked Markdown files": 4,
        "Pages under `docs/`": 3,
        "GNN sketches (`*.gnn.md`)": 1,
    }

    def setUp(self) -> None:
        super().setUp()
        self.git_program = required_program("git")
        self.generator = self.copy_source("scripts/docgen/counts.py")
        for relative in ("scripts/gate_tools.json", ".github/gnn-pin.json", "docs/_generated/timings.json"):
            self.copy_source(relative)
        self.output = self.repo / "docs" / "_generated" / "COUNTS.md"
        self.output.write_text("", encoding="utf-8")
        for relative, text in {
            ".gitignore": "ignored/\n",
            "README.md": "# Fixture\n",
            "docs/guide.md": "# Guide\n",
            "docs/model.gnn.md": "# Inventory-only sketch fixture\n",
        }.items():
            (self.repo / relative).write_text(text, encoding="utf-8")
        self.git("init", "--quiet")
        self.git(
            "add", "--", ".gitignore", "README.md", "docs/guide.md", "docs/model.gnn.md",
            "docs/_generated/COUNTS.md", "docs/_generated/timings.json",
            "scripts/docgen/counts.py", "scripts/gate_tools.json", ".github/gnn-pin.json",
        )

    def git(self, *args: str) -> None:
        result = self.command([self.git_program, "-c", "core.fsmonitor=false", "-C", str(self.repo), *args])
        self.assertEqual(result.returncode, 0, result.stderr)

    def counts(self, *args: str) -> subprocess.CompletedProcess[str]:
        return self.command([sys.executable, "-B", str(self.generator), *args])

    def generate(self) -> bytes:
        result = self.counts()
        self.assertEqual(result.returncode, 0, result.stderr)
        return self.output.read_bytes()

    def metrics(self) -> dict[str, int]:
        rows = {}
        for line in self.output.read_text(encoding="utf-8").splitlines():
            columns = [column.strip() for column in line.split("|")]
            if len(columns) == 4 and columns[1] in self.BASE_METRICS:
                rows[columns[1]] = int(columns[2])
        return rows

    def test_report_counts_the_complete_real_git_index(self) -> None:
        self.generate()
        self.assertEqual(self.metrics(), self.BASE_METRICS)
        result = self.counts("--check")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_untracked_and_ignored_files_do_not_change_canonical_report(self) -> None:
        baseline = self.generate()
        (self.repo / "scratch.bin").write_bytes(b"untracked")
        (self.repo / "notes.md").write_text("# Scratch\n", encoding="utf-8")
        (self.repo / "docs" / "scratch.gnn.md").write_text("# Untracked sketch\n", encoding="utf-8")
        ignored = self.repo / "ignored"
        ignored.mkdir()
        (ignored / "draft.md").write_text("# Ignored\n", encoding="utf-8")
        result = self.counts("--check")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.output.read_bytes(), baseline)
        self.assertEqual(self.generate(), baseline)
        self.assertEqual(self.metrics(), self.BASE_METRICS)

    def test_staged_addition_and_removal_change_only_tracked_inventory(self) -> None:
        self.generate()
        relative = "docs/new model.gnn.md"
        (self.repo / relative).write_text("# New sketch\n", encoding="utf-8")
        self.git("add", "--", relative)
        stale = self.counts("--check")
        self.assertEqual(stale.returncode, 1, stale.stderr)
        self.assertIn("COUNTS.md is stale", stale.stderr)
        self.generate()
        self.assertEqual(self.metrics(), {
            "Tracked files": 10, "Tracked Markdown files": 5,
            "Pages under `docs/`": 4, "GNN sketches (`*.gnn.md`)": 2,
        })
        self.git("rm", "--cached", "--", "docs/guide.md")
        self.assertTrue((self.repo / "docs" / "guide.md").is_file())
        stale = self.counts("--check")
        self.assertEqual(stale.returncode, 1, stale.stderr)
        self.generate()
        self.assertEqual(self.metrics(), {
            "Tracked files": 9, "Tracked Markdown files": 4,
            "Pages under `docs/`": 3, "GNN sketches (`*.gnn.md`)": 2,
        })
        result = self.counts("--check")
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
