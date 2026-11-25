# GNN conformance (pinned)

gen25 publishes a conformance gate for
[Generalized Notation Notation](https://github.com/ActiveInferenceInstitute/Generalized_Notation_Notation)
(GNN) sketches. The authoritative short pointer to what the job parses is
[`.github/GNN.md`](../.github/GNN.md); this page records how the arm works.

## The pin

[`.github/gnn-pin.json`](../.github/gnn-pin.json) is the canonical pin file and the only
place the pinned revision appears. It declares schema `gnn-importer-pin/v1`:

| Field | Value |
| --- | --- |
| `schema` | `gnn-importer-pin/v1` |
| `repository` | `ActiveInferenceInstitute/Generalized_Notation_Notation` |
| `tag` | `v5.1.0` |
| `revision` | `75c834bd8519dc7b5adc4d24f16bf393cfd1ecdf` |
| `recorded` | 2026-11-24 |

The current values are reported in
[`_generated/COUNTS.md`](_generated/COUNTS.md#gate-pins), which is generated from the pin
file rather than typed here.

[`../scripts/gnn_conformance.py`](../scripts/gnn_conformance.py) reads a standalone
bootstrap as data, verifies its frozen SHA-256 and executes exactly those checked bytes.
The bootstrap reads the pin and admits the candidate against an independently frozen,
complete source manifest before any GNN import. Every actual parser, syntax and type
check remains inside the qualified lifetime, including resource/source revalidation
before the verdict is published. A matching version alone is not provenance.

Installed mode requires genuine distribution ownership and exact Git PEP610 origin,
plus complete package-content agreement. Explicit source mode instead requires a
selected `gnn` package root and reports `origin.kind=explicit-source` and
`vcs_verified=false`. Neither mode claims native execution or scientific validity;
`execution_verified` remains false. A refused installation never falls back to source.

## What it verifies

- **Repository sketches.** If the working tree contains any `*.gnn.md` file, each one is
  parsed with `parse_gnn_formal`, syntax-validated with `validate_gnn_syntax`, and the
  collected sketches are type-checked with `GNNTypeChecker`, which must return exactly
  `True` (it returns `2` for invalid files or when no files are found, and `False` on a
  hard failure; anything but `True` fails the arm). The receipt reports
  `"source": "repository"` and `"result": "repository-content-passed"`.
- **Pinned exemplar (fallback).** When there is no sketch yet, the arm fetches
  `input/gnn_files/basics/static_perception.md` from the pinned revision, parses it,
  syntax-validates it and type-checks it, and reports `"source": "pinned-exemplar"` and
  `"result": "pinned-exemplar-baseline-passed"`. This is a pipeline and pin conformance baseline — **not** a claim that gen25 already contains
  a GNN model.

The script emits its actual JSON receipt after lifetime exit checks. Its nested
`source-qualification` records the manifest, runtime, full file inventory, loaded
modules and origin. Preserve this real output; a handwritten flat success example is
not qualification evidence.

## Running it

```sh
./run.sh gnn
```

Set `GNN_BOOTSTRAP` and `GNN_SOURCE_MANIFEST` to independently reviewed resources
matching the script's frozen digests. For offline source qualification also set
`GNN_ORIGIN_MODE=source`, `GNN_SOURCE_ROOT` to the complete selected `gnn` package,
and `GNN_PYTHON` to a prepared interpreter, then use `./run.sh gnn --no-install`.
With no repository sketches, the ordinary gate still needs its pinned remote exemplar;
source-mode regression fixtures instead stage actual local sketches. Do not advertise
the empty repository as an authored model or a network-free full gate.

Installed mode is the default and requires a genuine prepared exact-pin distribution
for `--no-install`. With installation authorized, the script can provision the exact
commit and required parser dependencies. An explicit invalid `GNN_PYTHON` is rejected,
not replaced by a default. CI uses `GNN_PYTHON_VERSION=3.12`, but reviewed-resource
delivery remains a separate hosted prerequisite.

## Offline regression selections

`./run.sh test` runs both regression files. `tests/test_maintenance.py` covers
interpreter selection and tracked-only counts. `tests/test_gnn_conformance.py` uses
real files, processes and parser/checker calls, including rejection of a genuine
dimension-inconsistent model when the checker returns `2`, not a substitute parser.
For separately scoped source and installed controls:

```sh
python -B -m unittest discover -s tests -p test_gnn_conformance.py -k SourceAdmissionTests -v
python -B -m unittest discover -s tests -p test_gnn_conformance.py -k InstalledAdmissionTests -v
```

Both require `GNN_BOOTSTRAP`, `GNN_SOURCE_MANIFEST`, `GNN_TEST_SOURCE_ROOT`,
`GNN_TEST_SPEC` and its `GNN_TEST_SPEC_SHA256`. The installed selection additionally
requires `GNN_TEST_INSTALLED_PYTHON` naming a genuine exact-pin installed runtime.
Missing prerequisites are not a pass. Do not synthesize package metadata, substitute a
parser, install implicitly or count source-mode success as installed acceptance.

## Adding a sketch

Add a `*.gnn.md` file anywhere in the tree and the repository branch of the arm takes over
automatically. Keep the file lint-clean and link-clean like any other Markdown, and do not
commit generated parser output.

## Why it is pinned

The upstream parser changes between releases. A checklist that floats would let a new
parser revision change the gate without a gen25 commit; pinning the revision keeps the
result reproducible and names the exact parser that produced it.
