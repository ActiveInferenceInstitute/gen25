"""Real-file/process controls for the exact-pin GNN consumer.

These tests require the reviewed producer resources in GNN_BOOTSTRAP and
GNN_SOURCE_MANIFEST, the matching package in GNN_TEST_SOURCE_ROOT, and the
qualified syntax input in GNN_TEST_SPEC. Missing inputs FAIL rather than skip.
Use a prepared interpreter with the pinned parser's actual dependencies. All
mutations are confined to disposable copies; no install or network is used.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import marshal
import os
from pathlib import Path
import shutil
import struct
import sys
import textwrap
import unittest

from test_maintenance import TemporaryWorkspace, required_program


BOOTSTRAP_SHA256 = "f638d4c01fe7de31e43d793e59bf382d0c3d1a82f365c59238334a2b40adfb37"
MANIFEST_SHA256 = "17a35bb2114e76a38119128d290d12377cb641652d70788000482366dca0a14a"
SPEC_SHA256 = "8d08f3e951c7efc05dc5d84bbbece6765a40c3795bdac13ad8d7b33dde79567f"


class GNNWorkspace(TemporaryWorkspace):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        inputs = {}
        for name in ("GNN_BOOTSTRAP", "GNN_SOURCE_MANIFEST", "GNN_TEST_SOURCE_ROOT", "GNN_TEST_SPEC"):
            value = os.environ.get(name)
            if not value:
                raise RuntimeError(f"{name} must select the actual qualified producer input")
            inputs[name] = Path(value).resolve(strict=True)
        cls.producer_bootstrap = inputs["GNN_BOOTSTRAP"]
        cls.producer_manifest = inputs["GNN_SOURCE_MANIFEST"]
        cls.producer_package = inputs["GNN_TEST_SOURCE_ROOT"]
        cls.producer_spec = inputs["GNN_TEST_SPEC"]
        for path, digest in (
            (cls.producer_bootstrap, BOOTSTRAP_SHA256),
            (cls.producer_manifest, MANIFEST_SHA256),
            (cls.producer_spec, SPEC_SHA256),
        ):
            if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                raise RuntimeError(f"{path.name} is not the frozen qualified producer input")

    def setUp(self) -> None:
        super().setUp()
        # Match the consumer's resolved paths, including systems with a
        # symlinked temporary-directory prefix.
        self.workspace = self.workspace.resolve()
        self.repo = self.repo.resolve()
        self.caller = self.caller.resolve()
        self.script = self.copy_source("scripts/gnn_conformance.py")
        self.copy_source("run.sh")
        self.pin = self.copy_source(".github/gnn-pin.json")
        resources = self.workspace / "reviewed resources"
        resources.mkdir()
        self.bootstrap = resources / "gnn_bootstrap.py"
        self.manifest = resources / "source-manifest.json"
        shutil.copy2(self.producer_bootstrap, self.bootstrap)
        shutil.copy2(self.producer_manifest, self.manifest)
        self.package = self.workspace / "selected source" / "src" / "gnn"
        shutil.copytree(
            self.producer_package,
            self.package,
            symlinks=True,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"),
        )
        models = self.repo / "models"
        models.mkdir()
        self.sketch = models / "first.gnn.md"
        shutil.copy2(self.producer_spec, self.sketch)
        # Two real inputs exercise the checker's collection/worker selection.
        shutil.copy2(self.producer_spec, models / "second.gnn.md")
        self.marker = self.workspace / "unchecked execution"
        self.arguments = [
            "--bootstrap", str(self.bootstrap),
            "--manifest", str(self.manifest),
            "--origin-mode", "source",
            "--source-root", str(self.package),
            "--no-install",
        ]

    def gate(self, *, arguments=None, environment=None, code=None, flags=(), interpreter=None):
        argv = [str(interpreter or sys.executable), "-B", *flags]
        if code is None:
            argv.append(str(self.script))
        else:
            argv.extend(["-c", textwrap.dedent(code), str(self.script)])
        argv.extend(self.arguments if arguments is None else arguments)
        return self.command(argv, environment=environment)

    def receipt(self, result, *, origin="explicit-source"):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        receipts = []
        for line in result.stdout.splitlines():
            try:
                payload = json.loads(line)
            except ValueError:
                continue
            if isinstance(payload, dict) and payload.get("result") == "verified":
                receipts.append(payload)
        self.assertEqual(len(receipts), 1, result.stdout)
        receipt = receipts[0]
        qualification = receipt["qualification"]
        self.assertEqual(receipt["models"], 2)
        self.assertEqual(receipt["source"], "repository")
        self.assertEqual(receipt["pin-revision"], json.loads(self.pin.read_text())["revision"])
        self.assertEqual(qualification["manifest_sha256"], MANIFEST_SHA256)
        self.assertTrue(qualification["ok"])
        self.assertTrue(qualification["imports_verified"])
        self.assertEqual(qualification["status"], "qualified")
        self.assertEqual(qualification["origin"]["kind"], origin)
        self.assertEqual(qualification["origin"]["vcs_verified"], origin == "installed-vcs")
        self.assertFalse(qualification["execution_verified"])
        self.assertIn("gnn.parsers.basic", qualification["loaded_modules"])
        self.assertIn("gnn.type_checker.checking.core", qualification["loaded_modules"])
        self.assertEqual(
            qualification["loaded_modules"]["gnn.parsers.basic"]["sha256"],
            json.loads(self.manifest.read_bytes())["files"]["src/gnn/parsers/basic.py"],
        )
        return receipt

    def rejected(self, result, reason):
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(reason, result.stderr)
        self.assertNotIn('"result": "verified"', result.stdout)
        self.assertFalse(self.marker.exists(), "unchecked producer code executed")

    def marker_statement(self) -> bytes:
        return f"\nfrom pathlib import Path\nPath({str(self.marker)!r}).write_text('executed')\n".encode()


class SourceAdmissionTests(GNNWorkspace):
    def test_direct_api_keeps_every_real_gnn_call_inside_qualified_lifetime(self) -> None:
        record = self.workspace / "lifetime.json"
        environment = dict(self.environment, GNN_TEST_RECORD=str(record))
        result = self.gate(environment=environment, code="""
            import json, os, runpy, sys
            from pathlib import Path

            gate = runpy.run_path(sys.argv[1])
            options = dict(zip(sys.argv[2:-1:2], sys.argv[3:-1:2]))
            package = Path(options['--source-root'])
            prefix = str(package) + os.sep
            calls = set()
            worker_pids = []

            def profile(frame, event, arg):
                if event != 'call' or not frame.f_code.co_filename.startswith(prefix):
                    return
                bootstrap = sys.modules.get('_gen25_gnn_bootstrap')
                if bootstrap is None or bootstrap._ACTIVE_SOURCE is None:
                    raise AssertionError('GNN code executed outside qualified_source')
                calls.add(frame.f_globals.get('__name__', '') + ':' + frame.f_code.co_name)
                if frame.f_globals.get('__name__') == 'gnn.utils.file_workers' and frame.f_code.co_name == '_invoke':
                    worker_pids.append(os.getpid())

            sys.setprofile(profile)
            try:
                receipt = gate['verify'](
                    Path(sys.argv[1]).parents[1],
                    bootstrap_path=Path(options['--bootstrap']),
                    manifest_path=Path(options['--manifest']),
                    origin_mode='source', package_root=package,
                )
            finally:
                sys.setprofile(None)
            Path(os.environ['GNN_TEST_RECORD']).write_text(json.dumps({
                'calls': sorted(calls), 'worker_pids': worker_pids, 'pid': os.getpid(),
            }))
            print(json.dumps(receipt, sort_keys=True))
        """)
        self.receipt(result)
        actual = json.loads(record.read_text())
        for call in (
            "gnn.parsers.basic:parse_gnn_formal",
            "gnn.parsers.basic:validate_gnn_syntax",
            "gnn.type_checker.checking.core:validate_gnn_files",
        ):
            self.assertIn(call, actual["calls"])
        self.assertEqual(actual["worker_pids"], [actual["pid"], actual["pid"]])

    def test_runner_forwards_source_selection_to_the_explicit_interpreter(self) -> None:
        # Invoke the selected runtime by its actual path: resolving or moving a
        # venv's interpreter symlink can silently select the base interpreter.
        environment = dict(self.environment, GNN_PYTHON=sys.executable)
        result = self.command(
            [required_program("bash"), str(self.repo / "run.sh"), "gnn", *self.arguments],
            environment=environment,
        )
        self.receipt(result)
        self.assertFalse((self.repo / ".venv").exists())

    def test_corrupt_bootstrap_is_rejected_before_its_top_level_code_executes(self) -> None:
        with self.bootstrap.open("ab") as handle:
            handle.write(self.marker_statement())
        self.rejected(self.gate(), "bootstrap SHA-256")

    def test_checked_bootstrap_bytes_ignore_a_valid_timestamp_poisoned_cache(self) -> None:
        code = compile(self.marker_statement(), str(self.bootstrap), "exec")
        info = self.bootstrap.stat()
        cache = Path(importlib.util.cache_from_source(str(self.bootstrap)))
        cache.parent.mkdir()
        cache.write_bytes(
            importlib.util.MAGIC_NUMBER
            + struct.pack("<III", 0, int(info.st_mtime) & 0xffffffff, info.st_size)
            + marshal.dumps(code)
        )
        self.receipt(self.gate())
        self.assertFalse(self.marker.exists())

    def test_corrupt_manifest_refuses_without_executing_candidate_package(self) -> None:
        with self.manifest.open("ab") as handle:
            handle.write(b" \n")
        with (self.package / "__init__.py").open("ab") as handle:
            handle.write(self.marker_statement())
        self.rejected(self.gate(), "source manifest SHA-256")

    def test_changed_commit_with_the_same_tag_is_not_revision_attestation(self) -> None:
        pin = json.loads(self.pin.read_text())
        pin["revision"] = "0" * 40
        self.pin.write_text(json.dumps(pin))
        with (self.package / "__init__.py").open("ab") as handle:
            handle.write(self.marker_statement())
        self.rejected(self.gate(), "source-pin-mismatch")

    def test_shared_pin_reader_rejects_duplicate_revision_before_gnn_import(self) -> None:
        pin = self.pin.read_text().rstrip()
        self.pin.write_text(pin[:-1] + ', "revision": "' + "0" * 40 + '"}\n')
        with (self.package / "__init__.py").open("ab") as handle:
            handle.write(self.marker_statement())
        self.rejected(self.gate(), "duplicate JSON member")

    def test_modified_package_and_parser_top_level_code_never_executes(self) -> None:
        for relative in ("__init__.py", "parsers/basic.py"):
            path = self.package / relative
            original = path.read_bytes()
            with self.subTest(relative=relative):
                path.write_bytes(original + self.marker_statement())
                self.rejected(self.gate(), "source-content-mismatch")
            path.write_bytes(original)

    def test_complete_manifest_rejects_missing_extra_and_noncode_members(self) -> None:
        member = self.package / "README.md"
        original = member.read_bytes()
        member.write_bytes(original + b"\nchanged\n")
        self.rejected(self.gate(), "source-content-mismatch")
        member.unlink()
        self.rejected(self.gate(), "source-content-mismatch")
        member.write_bytes(original)
        (self.package / "unreviewed.txt").write_text("undeclared member\n")
        self.rejected(self.gate(), "source-content-mismatch")

    def test_source_change_during_actual_type_check_prevents_a_verified_receipt(self) -> None:
        changed = self.workspace / "changed during checker"
        environment = dict(
            self.environment, GNN_TEST_PACKAGE=str(self.package), GNN_TEST_CHANGED=str(changed)
        )
        result = self.gate(environment=environment, code="""
            import os, runpy, sys
            from pathlib import Path

            gate = runpy.run_path(sys.argv[1])
            changed = False
            def audit(event, args):
                global changed
                if event != 'open' or changed or not isinstance(args[0], (str, bytes)):
                    return
                if Path(os.fsdecode(args[0])).name != 'type_check_results.json':
                    return
                changed = True
                with (Path(os.environ['GNN_TEST_PACKAGE']) / 'README.md').open('ab') as handle:
                    handle.write(b'\\nchanged during real type checking\\n')
                Path(os.environ['GNN_TEST_CHANGED']).write_text('actual checker reached')
            sys.addaudithook(audit)
            raise SystemExit(gate['main'](sys.argv[2:]))
        """)
        self.rejected(result, "source-content-mismatch")
        self.assertEqual(changed.read_text(), "actual checker reached")

    def test_bootstrap_change_after_execution_is_revalidated_before_publication(self) -> None:
        environment = dict(
            self.environment,
            GNN_TEST_PIN=str(self.pin), GNN_TEST_BOOTSTRAP=str(self.bootstrap),
            GNN_TEST_MARKER=str(self.marker),
        )
        result = self.gate(environment=environment, code="""
            import os, runpy, sys
            from pathlib import Path

            gate = runpy.run_path(sys.argv[1])
            changed = False
            def audit(event, args):
                global changed
                if event != 'open' or changed or args[0] != os.environ['GNN_TEST_PIN']:
                    return
                changed = True
                statement = '\\nfrom pathlib import Path\\nPath(%r).write_text("executed")\\n' % os.environ['GNN_TEST_MARKER']
                with Path(os.environ['GNN_TEST_BOOTSTRAP']).open('ab') as handle:
                    handle.write(statement.encode())
            sys.addaudithook(audit)
            raise SystemExit(gate['main'](sys.argv[2:]))
        """)
        self.rejected(result, "bootstrap SHA-256")
        self.assertNotEqual(hashlib.sha256(self.bootstrap.read_bytes()).hexdigest(), BOOTSTRAP_SHA256)

    def test_installed_mode_does_not_fall_back_to_complete_source_without_origin(self) -> None:
        environment = dict(self.environment, PYTHONPATH=str(self.package.parent))
        arguments = [
            "--bootstrap", str(self.bootstrap), "--manifest", str(self.manifest), "--no-install"
        ]
        # -S removes actual installed metadata. The complete real producer source
        # remains resolvable, but is not an installed distribution/PEP 610 origin.
        result = self.gate(arguments=arguments, environment=environment, flags=("-S",), code="""
            import os, runpy, sys
            from pathlib import Path

            prefix = os.environ['PYTHONPATH'] + os.sep + 'gnn' + os.sep
            def audit(event, args):
                if event == 'exec' and args[0].co_filename.startswith(prefix):
                    raise AssertionError('unqualified installed-mode package executed')
            sys.addaudithook(audit)
            gate = runpy.run_path(sys.argv[1])
            raise SystemExit(gate['main'](sys.argv[2:]))
        """)
        self.rejected(result, "source-origin-unavailable")

    def test_source_root_alone_cannot_silently_select_source_mode(self) -> None:
        arguments = [
            "--bootstrap", str(self.bootstrap), "--manifest", str(self.manifest),
            "--source-root", str(self.package), "--no-install",
        ]
        self.rejected(self.gate(arguments=arguments), "requires explicit source mode")

    def test_explicit_source_uses_its_selected_artifact_not_ambient_gnn(self) -> None:
        foreign = self.workspace / "ambient source" / "gnn"
        shutil.copytree(self.package, foreign)
        with (foreign / "__init__.py").open("ab") as handle:
            handle.write(self.marker_statement())
        environment = dict(self.environment, PYTHONPATH=str(foreign.parent))
        receipt = self.receipt(self.gate(environment=environment))
        self.assertEqual(receipt["qualification"]["package_root"], str(self.package))
        self.assertFalse(self.marker.exists())


class InstalledAdmissionTests(GNNWorkspace):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        value = os.environ.get("GNN_TEST_INSTALLED_PYTHON")
        if not value:
            raise RuntimeError("GNN_TEST_INSTALLED_PYTHON must select the actual exact-pin installed runtime")
        cls.installed_python = Path(value).absolute()
        if not cls.installed_python.is_file() or not os.access(cls.installed_python, os.X_OK):
            raise RuntimeError("GNN_TEST_INSTALLED_PYTHON is not an executable file")

    def test_actual_installed_origin_and_real_metadata_failure_controls(self) -> None:
        arguments = [
            "--bootstrap", str(self.bootstrap), "--manifest", str(self.manifest), "--no-install",
        ]
        # This must be the actual prepared installation: never synthesize a
        # distribution or accept the source-mode receipt as installed proof.
        self.receipt(
            self.gate(arguments=arguments, interpreter=self.installed_python),
            origin="installed-vcs",
        )

        stage = self.workspace / "copied installed distribution"
        copied = self.command([
            str(self.installed_python), "-B", "-c", textwrap.dedent("""
                import importlib.metadata, json, shutil, sys
                from pathlib import Path

                distribution = importlib.metadata.distribution('generalized-notation-notation')
                metadata = [
                    Path(distribution.locate_file(path)).parent
                    for path in distribution.files or ()
                    if path.name == 'METADATA' and path.parent.name.endswith('.dist-info')
                ]
                if len(metadata) != 1:
                    raise RuntimeError('actual installed metadata ownership is unavailable')
                destination = Path(sys.argv[1])
                destination.mkdir()
                package = Path(distribution.locate_file('gnn/__init__.py')).resolve().parent
                shutil.copytree(
                    package, destination / 'gnn', symlinks=True,
                    ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '*.pyo'),
                )
                shutil.copytree(metadata[0], destination / metadata[0].name, symlinks=True)
                (destination / 'copied-metadata.json').write_text(json.dumps({
                    'metadata_directory': metadata[0].name,
                }))
            """), str(stage),
        ])
        self.assertEqual(copied.returncode, 0, copied.stdout + copied.stderr)
        metadata = json.loads((stage / "copied-metadata.json").read_text())
        direct_url = stage / metadata["metadata_directory"] / "direct_url.json"
        original = direct_url.read_bytes()
        environment = dict(self.environment, PYTHONPATH=str(stage), GNN_TEST_STAGE=str(stage))
        no_unchecked_import = """
            import os, runpy, sys

            prefix = os.environ['GNN_TEST_STAGE'] + os.sep + 'gnn' + os.sep
            def audit(event, args):
                if event == 'exec' and args[0].co_filename.startswith(prefix):
                    raise AssertionError('unqualified installed package executed')
            sys.addaudithook(audit)
            gate = runpy.run_path(sys.argv[1])
            raise SystemExit(gate['main'](sys.argv[2:]))
        """
        for failure, reason in (
            ("missing", "source-origin-unavailable"),
            ("different-commit", "source-origin-mismatch"),
            ("non-git", "source-origin-unavailable"),
            ("malformed", "source-origin-unavailable"),
        ):
            with self.subTest(origin=failure):
                if failure == "missing":
                    direct_url.unlink()
                elif failure == "malformed":
                    direct_url.write_bytes(b"not JSON\n")
                else:
                    payload = json.loads(original)
                    if failure == "different-commit":
                        payload["vcs_info"]["commit_id"] = "0" * 40
                    else:
                        payload["vcs_info"]["vcs"] = "hg"
                    direct_url.write_text(json.dumps(payload))
                self.rejected(
                    self.gate(
                        arguments=arguments, environment=environment, code=no_unchecked_import,
                        interpreter=self.installed_python,
                    ),
                    reason,
                )
                direct_url.write_bytes(original)

        # The copied real metadata, tag and __version__ remain unchanged.
        # Altering even one actual parser member still refuses before execution.
        with (stage / "gnn" / "parsers" / "basic.py").open("ab") as handle:
            handle.write(self.marker_statement())
        self.rejected(
            self.gate(
                arguments=arguments, environment=environment, code=no_unchecked_import,
                interpreter=self.installed_python,
            ),
            "source-content-mismatch",
        )


if __name__ == "__main__":
    unittest.main()
