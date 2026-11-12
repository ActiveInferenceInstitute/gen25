"""Regression tests for the GNN conformance gate's accept sentinel.

``GNNTypeChecker.validate_gnn_files`` returns ``True`` (every file valid), ``2``
(invalid files, or no files found) or ``False`` (a hard failure). The gate accepts
only ``True``: a bare ``if not outcome`` treats ``2`` as success and prints a
``"verified"`` receipt. Each test runs the real ``scripts/gnn_conformance.py`` in a
subprocess against a stubbed ``gnn`` package, so the acceptance is repeatable in
``./run.sh test`` instead of an ad-hoc probe.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "gnn_conformance.py"
PIN = ROOT / ".github" / "gnn-pin.json"

# Stands in for the pinned parser: `check_sketches` imports both names.
STUB_BASIC = '''\
class _Parsed:
    parse_errors = ()


def parse_gnn_formal(path):
    return _Parsed()


def validate_gnn_syntax(text, is_content=False):
    return True, []
'''

# Stands in for the pinned type checker and returns the documented sentinels.
STUB_TYPE_CHECKER = '''\
import os

_OUTCOMES = {"true": True, "invalid-files": 2, "hard-failure": False}


class GNNTypeChecker:
    def validate_gnn_files(self, model_dir, output_dir):
        return _OUTCOMES[os.environ["STUB_TYPE_CHECKER_OUTCOME"]]
'''

SKETCH = """\
# Sample
Static Perception
=================
"""


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def run_gate(outcome: str) -> subprocess.CompletedProcess[str]:
    """Run the real gate script against a stub reporting ``outcome``."""
    pin = json.loads(PIN.read_text(encoding="utf-8"))
    version = pin["tag"].removeprefix("v")
    with tempfile.TemporaryDirectory(prefix="gnn-conformance-test-") as tmp:
        scratch = Path(tmp)
        repo = scratch / "repo"
        script = repo / "scripts" / "gnn_conformance.py"
        script.parent.mkdir(parents=True)
        shutil.copy2(SCRIPT, script)
        pin_copy = repo / ".github" / "gnn-pin.json"
        pin_copy.parent.mkdir(parents=True)
        shutil.copy2(PIN, pin_copy)
        _write(repo / "sample.gnn.md", SKETCH)
        stub = scratch / "stub" / "gnn"
        _write(stub / "__init__.py", f'__version__ = "{version}"\n')
        _write(stub / "parsers" / "__init__.py", "")
        _write(stub / "parsers" / "basic.py", STUB_BASIC)
        _write(stub / "type_checker.py", STUB_TYPE_CHECKER)
        env = dict(
            os.environ,
            PYTHONPATH=str(stub.parent),
            STUB_TYPE_CHECKER_OUTCOME=outcome,
        )
        return subprocess.run(
            [sys.executable, str(script)],
            cwd=repo,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )


class TypeCheckerSentinelTest(unittest.TestCase):
    def test_invalid_files_result_fails_the_gate(self):
        result = run_gate("invalid-files")
        self.assertEqual(1, result.returncode, msg=result.stderr or result.stdout)
        self.assertIn("did not accept", result.stderr)
        self.assertIn("returned 2", result.stderr)
        self.assertEqual("", result.stdout)

    def test_hard_failure_fails_the_gate(self):
        result = run_gate("hard-failure")
        self.assertEqual(1, result.returncode, msg=result.stderr or result.stdout)
        self.assertIn("GNN type checker", result.stderr)
        self.assertEqual("", result.stdout)

    def test_accepting_result_passes_the_gate(self):
        result = run_gate("true")
        self.assertEqual(0, result.returncode, msg=result.stderr)
        receipt = json.loads(result.stdout)
        self.assertEqual("repository", receipt["source"])
        self.assertEqual(1, receipt["models"])
        pin = json.loads(PIN.read_text(encoding="utf-8"))
        self.assertEqual(pin["revision"], receipt["pin-revision"])


if __name__ == "__main__":
    unittest.main()
