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
| `tag` | `v5.0.3` |
| `revision` | `8f293d9ba810e6eda5c09842d9c7ed9ffa5f92c1` |
| `recorded` | 2026-11-12 |

The current values are reported in
[`_generated/COUNTS.md`](_generated/COUNTS.md#gate-pins), which is generated from the pin
file rather than typed here.

[`../scripts/gnn_conformance.py`](../scripts/gnn_conformance.py) validates the pin
document (schema, `owner/name` repository, 40-hex revision), installs exactly the pinned
commit (`git+https://github.com/<repository>.git@<revision>`) in a single resolver pass
together with the `defusedxml`, `psutil` and `pyyaml` imports the parser needs, and then
checks that the installed `gnn.__version__` equals the pin's tag without its `v`. No
revision is repeated in the workflow or the script, so a floating tag or branch cannot
silently satisfy the gate.

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

The arm prints one JSON receipt and exits non-zero on any mismatch:

```json
{"gnn-version": "5.0.3", "models": 1, "pin-revision": "8f293d9ba810e6eda5c09842d9c7ed9ffa5f92c1", "result": "pinned-exemplar-baseline-passed", "source": "pinned-exemplar"}
```

## Running it

```sh
./run.sh gnn
```

The arm bootstraps a seeded interpreter in `.venv/gnn` (git-ignored) with `uv`, then runs
the script. Set `GNN_PYTHON` to use an existing interpreter, or `GNN_PYTHON_VERSION` to
bootstrap a different CPython; CI sets it to `3.12`. The CI job key is `gnn-conformance`
and its display name is `gnn conformance (pinned)` — see [`ci.md`](ci.md).

## Adding a sketch

Add a `*.gnn.md` file anywhere in the tree and the repository branch of the arm takes over
automatically. Keep the file lint-clean and link-clean like any other Markdown, and do not
commit generated parser output.

## Why it is pinned

The upstream parser changes between releases. A checklist that floats would let a new
parser revision change the gate without a gen25 commit; pinning the revision keeps the
result reproducible and names the exact parser that produced it.
