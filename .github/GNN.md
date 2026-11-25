# GNN conformance

The `gnn-conformance` job (display name `gnn conformance (pinned)`) is defined in
[`workflows/docs.yml`](workflows/docs.yml) and runs `./run.sh gnn`, which calls
[`../scripts/gnn_conformance.py`](../scripts/gnn_conformance.py).

It reads [`gnn-pin.json`](gnn-pin.json), the canonical pin document (schema
`gnn-importer-pin/v1`), which pins
`ActiveInferenceInstitute/Generalized_Notation_Notation` at `v5.1.0`
(`75c834bd8519dc7b5adc4d24f16bf393cfd1ecdf`). The current values are mirrored from the
pin file into [`../docs/_generated/COUNTS.md`](../docs/_generated/COUNTS.md).

The job first verifies a standalone bootstrap and independent complete source manifest
selected by `GNN_BOOTSTRAP` and `GNN_SOURCE_MANIFEST`, then admits parser ownership,
origin and content before import. All parsing/checking and exit revalidation share one
qualified lifetime. Installed mode requires genuine exact Git distribution provenance;
explicit source mode reports its weaker origin and cannot silently replace a refused
installation. Hosted delivery of these reviewed resources remains required.

Repository `*.gnn.md` sketches take precedence; without any, the gate fetches the pinned
upstream `input/gnn_files/basics/static_perception.md` exemplar. This is a pipeline
baseline, not an authored gen25 model or scientific/native-execution qualification.
Offline inputs and no-install regression selections:
[`../docs/gnn-conformance.md`](../docs/gnn-conformance.md).
