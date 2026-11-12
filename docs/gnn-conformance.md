# GNN baseline (pinned)

gen25 publishes a baseline gate for
[Generalized Notation Notation](https://github.com/ActiveInferenceInstitute/Generalized_Notation_Notation)
(GNN) sketches. The authoritative short note is [`.github/GNN.md`](../.github/GNN.md);
this page records how the job works.

The workflow job id is `gnn-conformance`, but its display name is
`gnn baseline (pinned)`. gen25 ships no `*.gnn.md`, so the job validates the
pinned upstream exemplar rather than repository content.

## The pin

The job reads [`.github/gnn-pin.json`](../.github/gnn-pin.json), which pins the upstream
repository `ActiveInferenceInstitute/Generalized_Notation_Notation` at tag `v5.0.3`,
revision `8f293d9ba810e6eda5c09842d9c7ed9ffa5f92c1`. No GNN revision is baked into the
workflow: it asserts the pin's `repository`, `tag` and `revision`, installs exactly that
commit (`git+https://github.com/<repository>.git@<revision>`), and checks the installed
`gnn.__version__` matches the tag. A floating tag or branch cannot silently satisfy it.

## What it verifies

- **Repository sketches.** If the repository contains any `*.gnn.md` file, each one is
  parsed with `parse_gnn_formal`, syntax-validated with `validate_gnn_syntax`, and the
  collected sketches are type-checked with `GNNTypeChecker`. Results are printed as JSON
  with `"source": "repository"` and `"result": "repository-content-passed"`.
- **Pinned exemplar baseline (what runs today).** gen25 ships no sketch, so the
  job fetches `input/gnn_files/basics/static_perception.md` from the pinned
  revision, parses and type-checks it, and prints `"source": "pinned-exemplar"`
  and `"result": "pinned-exemplar-baseline-passed"`. This is a pipeline and pin
  baseline — **not** a claim that gen25 contains a GNN model.

## Adding a sketch

Add a `*.gnn.md` file anywhere in the tree and the repository branch of the job takes
over automatically. Keep the file lint-clean and link-clean like any other Markdown, and
do not commit generated parser output.

## Why it is pinned

The upstream parser changes between releases. A checklist that floats would let a new
parser revision change the gate without a gen25 commit; pinning the revision keeps the
result reproducible and names the exact parser that produced it.
