#!/usr/bin/env python3
"""Pinned GNN conformance with pre-import source admission.

``./run.sh gnn`` and CI use this entry point. GNN_BOOTSTRAP and
GNN_SOURCE_MANIFEST select independently reviewed producer resources; their
frozen digests below are not learned from the parser being checked. The pin
stays in .github/gnn-pin.json and is read by the checked producer bootstrap.

Installed mode requires the complete pinned package and matching PEP 610 Git
origin. An absent parser may be installed at the pin unless --no-install is
set; an existing but unqualified package is never replaced or trusted by
version alone. Source mode is deliberate: --origin-mode source additionally
requires --source-root (the exact src/gnn package), without installed claims.

Parser imports, syntax verdicts and serial type checking stay inside the
producer's qualified_source lifetime. Only its successful exit revalidation
permits a verified receipt. No scientific execution is attested.
"""

from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import importlib.metadata
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from types import ModuleType
from typing import Any, Iterator
import urllib.request
from pathlib import Path

PIN_PATH = Path(".github/gnn-pin.json")
# Independently frozen producer bootstrap and COMPLETE v5.1.0 package manifest.
BOOTSTRAP_SHA256 = "f638d4c01fe7de31e43d793e59bf382d0c3d1a82f365c59238334a2b40adfb37"
MANIFEST_SHA256 = "43b33c0b2b40386afa3f306fec4cc13bc1fd7c3b570fbf11d5008bad5c8e6b51"
# Dependencies the pinned parser imports but does not declare. Installed in the
# same resolver pass as the parser itself.
PARSER_DEPS = ("defusedxml", "psutil", "pyyaml")
EXEMPLAR = "input/gnn_files/basics/static_perception.md"
SKIPPED_DIRS = {".git", ".venv", "node_modules"}


class ConformanceError(RuntimeError):
    """A pin, parse or type-check failure."""


def checked_bytes(path: Path, expected: str, label: str) -> bytes:
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != expected:
        raise ConformanceError(f"{label} SHA-256 does not match the reviewed producer resource")
    return data


@contextmanager
def reviewed_bootstrap(path: Path) -> Iterator[ModuleType]:
    """Execute the same checked bytes, never an import loader or cached .pyc."""
    path = path.resolve(strict=True)
    data = checked_bytes(path, BOOTSTRAP_SHA256, "bootstrap")
    name = "_gen25_gnn_bootstrap"
    module = ModuleType(name)
    module.__file__ = str(path)
    previous = sys.modules.get(name)
    sys.modules[name] = module
    try:
        exec(compile(data, str(path), "exec", dont_inherit=True), module.__dict__)
        yield module
        checked_bytes(path, BOOTSTRAP_SHA256, "bootstrap")
    finally:
        if previous is None:
            sys.modules.pop(name, None)
        else:
            sys.modules[name] = previous


def ensure_parser(pin: Any) -> None:
    """Provision only a genuinely absent distribution, without importing GNN."""
    try:
        importlib.metadata.distribution("generalized-notation-notation")
    except importlib.metadata.PackageNotFoundError:
        if importlib.util.find_spec("gnn") is not None:
            raise ConformanceError("gnn resolves without its installed distribution; refusing installation")
    else:
        # Existing content/origin is admitted by qualified_source, not metadata
        # version equality. Failed admission never triggers an install fallback.
        return
    spec = (
        "generalized-notation-notation @ "
        f"git+https://github.com/{pin.repository}.git@{pin.commit}"
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


def repository_sketches(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*.gnn.md")
        if not SKIPPED_DIRS.intersection(path.relative_to(root).parts)
    )


def verify(
    root: Path,
    *,
    bootstrap_path: Path | None,
    manifest_path: Path | None,
    origin_mode: str = "installed",
    package_root: Path | None = None,
    install_missing: bool = False,
) -> dict[str, object]:
    """Own the entire admission/verdict lifetime; return JSON data, not GNN code."""
    root = root.resolve()
    pin_path = root / PIN_PATH
    if not pin_path.is_file():
        raise ConformanceError(f"{PIN_PATH} is missing")
    if bootstrap_path is None or manifest_path is None:
        raise ConformanceError(
            "GNN_BOOTSTRAP/--bootstrap and GNN_SOURCE_MANIFEST/--manifest "
            "must select the reviewed producer resources"
        )
    if origin_mode not in {"installed", "source"}:
        raise ConformanceError("origin mode must be installed or source")
    if origin_mode == "source" and package_root is None:
        raise ConformanceError("source mode requires GNN_SOURCE_ROOT/--source-root")
    if origin_mode == "installed" and package_root is not None:
        raise ConformanceError("GNN_SOURCE_ROOT/--source-root requires explicit source mode")
    manifest = checked_bytes(manifest_path, MANIFEST_SHA256, "source manifest")

    with reviewed_bootstrap(bootstrap_path) as bootstrap:
        pin = bootstrap.read_pin(pin_path)
        if pin.schema != bootstrap.PIN_SCHEMA:
            raise ConformanceError(f"{PIN_PATH} must declare {bootstrap.PIN_SCHEMA}")
        if pin.repository != bootstrap.UPSTREAM_REPOSITORY:
            raise ConformanceError(f"{PIN_PATH} must name {bootstrap.UPSTREAM_REPOSITORY}")
        if re.fullmatch(r"[0-9a-f]{40}", pin.commit) is None or not pin.tag:
            raise ConformanceError(f"{PIN_PATH} needs a full lowercase commit and non-empty tag")
        if pin.commit != json.loads(manifest)["commit"]:
            raise ConformanceError("source-pin-mismatch: reviewed manifest does not bind the consumer pin")

        original_path = sys.path[:]
        try:
            if origin_mode == "source":
                package_root = package_root.resolve(strict=True)
                sys.path.insert(0, str(package_root.parent))
                importlib.invalidate_caches()
            elif install_missing:
                ensure_parser(pin)
            with bootstrap.qualified_source(
                pin,
                manifest=manifest,
                manifest_sha256=MANIFEST_SHA256,
                package_root=package_root,
                origin_mode=origin_mode,
            ) as qualification:
                from gnn import __version__
                from gnn.parsers.basic import parse_gnn_formal, validate_gnn_syntax
                from gnn.type_checker import GNNTypeChecker

                if __version__ != pin.tag.removeprefix("v"):
                    raise ConformanceError(
                        f"installed GNN {__version__!r} does not match pin tag {pin.tag!r}"
                    )

                def check_sketches(sketches: list[Path], prefix: str) -> int:
                    for sketch in sketches:
                        parsed = parse_gnn_formal(sketch)
                        if parsed is None or getattr(parsed, "parse_errors", None):
                            raise ConformanceError(f"{sketch} did not parse cleanly")
                        valid, errors = validate_gnn_syntax(
                            sketch.read_text(encoding="utf-8"), is_content=True
                        )
                        if not valid:
                            raise ConformanceError(f"{sketch} syntax errors: {errors!r}")
                    with tempfile.TemporaryDirectory(prefix=prefix) as output_dir:
                        model_dir = Path(output_dir) / "models"
                        model_dir.mkdir()
                        for index, sketch in enumerate(sketches):
                            shutil.copy2(sketch, model_dir / f"{index:03d}_{sketch.name}")
                        # A spawned interpreter would not inherit this admission.
                        # The producer's one-worker path runs in this process.
                        outcome = GNNTypeChecker().validate_gnn_files(
                            model_dir, Path(output_dir), file_workers=1
                        )
                        if outcome is not True:
                            raise ConformanceError(
                                "GNN type checker did not accept the checked sketches "
                                f"(returned {outcome!r})"
                            )
                    return len(sketches)

                sketches = repository_sketches(root)
                if sketches:
                    models, source = check_sketches(sketches, "repo-gnn-"), "repository"
                else:
                    exemplar_url = (
                        "https://raw.githubusercontent.com/"
                        f"{pin.repository}/{pin.commit}/{EXEMPLAR}"
                    )
                    with tempfile.TemporaryDirectory(prefix="pinned-exemplar-") as output_dir:
                        exemplar = Path(output_dir) / Path(EXEMPLAR).name
                        urllib.request.urlretrieve(exemplar_url, exemplar)
                        models = check_sketches([exemplar], "pinned-exemplar-")
                        source = "pinned-exemplar"
        finally:
            sys.path[:] = original_path

        receipt = {
            "gnn-version": __version__,
            "pin-revision": qualification["commit"],
            "models": models,
            "source": source,
            "qualification": qualification,
            "result": (
                "repository-content-passed"
                if source == "repository"
                else "pinned-exemplar-baseline-passed"
            ),
        }
    return receipt


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bootstrap", type=Path, default=os.environ.get("GNN_BOOTSTRAP"))
    parser.add_argument("--manifest", type=Path, default=os.environ.get("GNN_SOURCE_MANIFEST"))
    parser.add_argument(
        "--origin-mode", choices=("installed", "source"),
        default=os.environ.get("GNN_ORIGIN_MODE", "installed"),
    )
    parser.add_argument("--source-root", type=Path, default=os.environ.get("GNN_SOURCE_ROOT"))
    parser.add_argument("--no-install", action="store_true")
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parent.parent
    try:
        receipt = verify(
            root,
            bootstrap_path=args.bootstrap,
            manifest_path=args.manifest,
            origin_mode=args.origin_mode,
            package_root=args.source_root,
            install_missing=not args.no_install,
        )
    except (ConformanceError, OSError, ValueError, ImportError) as exc:
        code = getattr(exc, "code", None)
        detail = f"{code}: {exc}" if code else str(exc)
        print(f"gnn-conformance: {detail}", file=sys.stderr)
        return 1
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
