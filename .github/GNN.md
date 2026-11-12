# GNN conformance

The `gnn-conformance` job (display name `gnn conformance (pinned)`) is defined in
[`workflows/docs.yml`](workflows/docs.yml) and runs `./run.sh gnn`, which calls
[`../scripts/gnn_conformance.py`](../scripts/gnn_conformance.py).

It reads [`gnn-pin.json`](gnn-pin.json), the canonical pin document (schema
`gnn-importer-pin/v1`), which pins
`ActiveInferenceInstitute/Generalized_Notation_Notation` at `v5.0.3`
(`8f293d9ba810e6eda5c09842d9c7ed9ffa5f92c1`). The current values are mirrored from the
pin file into [`../docs/_generated/COUNTS.md`](../docs/_generated/COUNTS.md).

The job verifies the pin and the installed parser, parses every `*.gnn.md` sketch in the
repository, and type-checks them. When the repository has no sketch yet, it parses the
pinned upstream `input/gnn_files/basics/static_perception.md` exemplar; this is a pipeline
and pin conformance baseline, not a claim that the repository already contains a model.
Full description: [`../docs/gnn-conformance.md`](../docs/gnn-conformance.md).
