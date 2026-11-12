#!/usr/bin/env python3
"""Pinned Generalized Notation Notation (GNN) conformance check.

The single implementation of the repository's GNN gate: ``./run.sh gnn`` runs it
locally and the ``gnn-conformance`` CI job runs the same arm. Everything the check
installs or compares comes from ``.github/gnn-pin.json``; no revision is repeated
in this file or in the workflow.

The check
1. validates the pin document (schema ``gnn-importer-pin/v1``),
2. installs exactly the pinned revision when the interpreter does not already
   have the pinned parser version,
3. parses and syntax-validates every ``*.gnn.md`` sketch in the working tree and
   type-checks the collection, or falls back to the pinned upstream exemplar when
   the repository has no sketch, and
4. prints one JSON receipt and exits non-zero on any mismatch.

Exit codes: 0 verified, 1 pin/parse/type-check failure, 2 unusable environment.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

PIN_PATH = Path(".github/gnn-pin.json")
PIN_SCHEMA = "gnn-importer-pin/v1"
# Dependencies the pinned parser imports but does not declare. Installed in the
# same resolver pass as the parser itself.
PARSER_DEPS = ("defusedxml", "psutil", "pyyaml")
EXEMPLAR = "input/gnn_files/basics/static_perception.md"
SKIPPED_DIRS = {".git", ".venv", "node_modules"}


class ConformanceError(RuntimeError):
    """A pin, parse or type-check failure."""


def load_pin(root: Path) -> dict[str, str]:
    path = root / PIN_PATH
    try:
        pin = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ConformanceError(f"{PIN_PATH} is missing") from None
    except json.JSONDecodeError as exc:
        raise ConformanceError(f"{PIN_PATH} is not valid JSON: {exc}") from None
    if not isinstance(pin, dict):
        raise ConformanceError(f"{PIN_PATH} must contain a JSON object")
    if pin.get("schema") != PIN_SCHEMA:
        raise ConformanceError(
            f"{PIN_PATH} declares schema {pin.get('schema')!r}, expected {PIN_SCHEMA!r}"
        )
    for key in ("repository", "revision", "tag"):
        if not isinstance(pin.get(key), str) or not pin[key]:
            raise ConformanceError(f"{PIN_PATH} needs a non-empty string '{key}'")
    if not re.fullmatch(r"[^/\s]+/[^/\s]+", pin["repository"]):
        raise ConformanceError(f"pin repository {pin['repository']!r} is not 'owner/name'")
    if not re.fullmatch(r"[0-9a-f]{40}", pin["revision"]):
        raise ConformanceError(f"pin revision {pin['revision']!r} is not a 40-hex commit")
    return pin


def installed_parser_version() -> str | None:
    """Return ``gnn.__version__`` from a fresh interpreter, or ``None``."""
    probe = subprocess.run(
        [sys.executable, "-c", "import gnn; print(gnn.__version__)"],
        capture_output=True,
        text=True,
        check=False,
    )
    if probe.returncode != 0:
        return None
    return probe.stdout.strip() or None


def ensure_parser(pin: dict[str, str]) -> str:
    """Install the pinned revision in one pip pass unless it is already present."""
    expected = pin["tag"].removeprefix("v")
    installed = installed_parser_version()
    if installed == expected:
        return installed
    spec = (
        "generalized-notation-notation @ "
        f"git+https://github.com/{pin['repository']}.git@{pin['revision']}"
    )
    install = subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--disable-pip-version-check",
            "--no-deps",
            *PARSER_DEPS,
            spec,
        ],
        check=False,
    )
    if install.returncode != 0:
        raise ConformanceError(f"pip could not install {spec}")
    installed = installed_parser_version()
    if installed != expected:
        raise ConformanceError(
            f"installed GNN {installed!r} does not match pin tag {pin['tag']!r}"
        )
    return installed


def repository_sketches(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*.gnn.md")
        if not SKIPPED_DIRS.intersection(path.relative_to(root).parts)
    )


def check_sketches(sketches: list[Path], prefix: str) -> int:
    from gnn.parsers.basic import parse_gnn_formal, validate_gnn_syntax
    from gnn.type_checker import GNNTypeChecker

    for sketch in sketches:
        parsed = parse_gnn_formal(sketch)
        if parsed is None or getattr(parsed, "parse_errors", None):
            raise ConformanceError(f"{sketch} did not parse cleanly")
        valid, errors = validate_gnn_syntax(sketch.read_text(encoding="utf-8"))
        if not valid:
            raise ConformanceError(f"{sketch} syntax errors: {errors!r}")
    with tempfile.TemporaryDirectory(prefix=prefix) as output_dir:
        model_dir = Path(output_dir) / "models"
        model_dir.mkdir()
        for index, sketch in enumerate(sketches):
            shutil.copy2(sketch, model_dir / f"{index:03d}_{sketch.name}")
        if not GNNTypeChecker().validate_gnn_files(model_dir, Path(output_dir)):
            raise ConformanceError("GNN type checker rejected the checked sketches")
    return len(sketches)


def verify(root: Path, pin: dict[str, str]) -> dict[str, object]:
    from gnn import __version__

    expected = pin["tag"].removeprefix("v")
    if __version__ != expected:
        raise ConformanceError(
            f"installed GNN {__version__!r} does not match pin tag {pin['tag']!r}"
        )

    sketches = repository_sketches(root)
    if sketches:
        models, source = check_sketches(sketches, "repo-gnn-"), "repository"
    else:
        exemplar_url = (
            "https://raw.githubusercontent.com/"
            f"{pin['repository']}/{pin['revision']}/{EXEMPLAR}"
        )
        with tempfile.TemporaryDirectory(prefix="pinned-exemplar-") as output_dir:
            exemplar = Path(output_dir) / Path(EXEMPLAR).name
            urllib.request.urlretrieve(exemplar_url, exemplar)
            models, source = check_sketches([exemplar], "pinned-exemplar-"), "pinned-exemplar"

    return {
        "gnn-version": __version__,
        "pin-revision": pin["revision"],
        "models": models,
        "source": source,
        "result": "verified",
    }


def main(argv: list[str]) -> int:
    root = Path(__file__).resolve().parent.parent
    try:
        pin = load_pin(root)
        ensure_parser(pin)
        receipt = verify(root, pin)
    except ConformanceError as exc:
        print(f"gnn-conformance: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
