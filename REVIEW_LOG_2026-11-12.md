# Review log — 2026-11-12

Documentation and gate pass on this repository only. Baseline commit: `e250b9d`
(`origin/main`, "ci(docs): adopt the setup-python-uv composite action (#6)").

## Preflight state

- **No gate entry point.** Every check lived in `.github/workflows/docs.yml`: two
  marketplace actions (`gaurav-nelson/github-action-markdown-link-check`,
  `DavidAnson/markdownlint-cli2-action`) in `markdown-link-check`, and three inline
  steps in `gnn-conformance` — a `uv venv` bootstrap, two separate `pip install`
  invocations, and an inline heredoc that re-asserted the pin's `repository`, `tag` and
  `revision`. The same facts were therefore written three times (workflow comment,
  workflow assertions, `.github/gnn-pin.json`), and no local command ran what CI ran.
- **The link check could not pass.** `markdown-link-check` over the tracked Markdown
  reported one dead link: `https://github.com/ActiveInferenceInstitute/InstituteOS`
  returns 404 because that repository is private. `gh api` confirms it exists and is
  private; the link in `docs/sidecar.md` and `.aii/README.md` is correct.
- **Four lint findings, outside CI's scope.** The actions' default glob lints only the
  repository root, so CI never saw them; a recursive local run reported MD012 twice
  (`.aii/docs/AGENTS.md`, `.aii/docs/README.md` — a trailing blank line in each) and
  MD034 twice (`.aii/README.md` — bare URLs).
- **No flat documentation index and no generated numbers document.** `docs/README.md`
  was a hub with five pages; measured counts and arm runtimes existed nowhere.

## Implemented

| Change | Files |
| --- | --- |
| Single gate entry point with separately runnable arms (`lint`, `links`, `counts`, `gnn`, `check`, `all`, `measure`). | `run.sh` |
| Every CI step is a `./run.sh` arm; the required job key `markdown-link-check` and the `gnn conformance (pinned)` display name are unchanged. | `.github/workflows/docs.yml` |
| One implementation of the pinned GNN check: pin validation, one resolver pass for the parser and its three imports, sketch or exemplar verification, JSON receipt. | `scripts/gnn_conformance.py` |
| Node tool versions have one home. | `scripts/gate_tools.json` |
| Generated measured numbers, with `--check` staleness enforcement. | `scripts/docgen/counts.py`, `docs/_generated/COUNTS.md`, `docs/_generated/timings.json` |
| Reasoned link-check exclusion instead of a broken required check. | `mlc_config.json` |
| Lint scope covers the working tree and excludes the GNN arm's virtual environment. | `.markdownlint-cli2.yaml` |
| Gate and run guide; flat documentation index; hub, README and agent conventions updated. | `docs/RUN_GUIDE.md`, `docs/documentation-index.md`, `docs/README.md`, `README.md`, `AGENTS.md`, `CONTRIBUTING.md`, `docs/review-process.md` |
| CI and pin documentation matches the workflow: job key and display name, the pinned composite action, the tool pins, the exclusion and its reason, the pin schema. | `docs/ci.md`, `docs/gnn-conformance.md`, `.github/GNN.md` |
| Four lint findings fixed. | `.aii/README.md`, `.aii/docs/README.md`, `.aii/docs/AGENTS.md` |
| Sidecar artifacts and the rendered integration record. | `.aii/config.yaml`, `.aii/docs/INTEGRATION.md` |

## Measurements

Host: Darwin arm64, Node v26.13.0, one run per arm with warm tool caches; `lint` and
`links` are additionally reported as the median of three consecutive runs on the same
host. No CI run was measured: GitHub Actions is billing-locked org-wide, so hosted-CI
savings are **not claimed**.

| Arm | Before (command available before) | Before (s) | After (`./run.sh`) | After (s) |
| --- | --- | --- | --- | --- |
| lint | `npx --yes markdownlint-cli2 "**/*.md"` (unpinned) | 4.63 (median of 3; 4 findings) | `./run.sh lint` (pinned 0.24.1) | 4.70 (median of 3); 5.21 recorded (0 findings) |
| links | `npx --yes markdown-link-check -q -c mlc_config.json .` (whole checkout, unpinned) | 7.42 (1 run; 1 dead link) | `./run.sh links` (pinned 3.15.0, tracked files) | 7.56 recorded; 5.17 (median of 3, warm) |
| gnn | the job's three steps, verbatim, in a fresh seeded interpreter | 14.66 | `./run.sh gnn` | 17.08 |
| check | — (no such command) | — | `./run.sh check` | not measured separately; equals `counts --check` + `lint` + `links` |

`lint` and `links` show no meaningful difference: both are dominated by `npx` startup,
and the 4.63 → 4.70 s and 7.42 → 7.56 s pairs sit inside the run-to-run spread. The
change to those arms is scope and determinism, not speed.

**Scope, measured.** The pre-change link command walked the whole checkout, so once the
GNN arm had created its interpreter it descended into `.venv/gnn` and linted dependency
documentation: on that tree the same command took 51.82, 56.75 and 62.31 s and failed,
while `./run.sh links` over the tracked file list took 4.97, 5.17 and 5.59 s. The
tracked-file list is also what makes the local arm identical to CI, where the checkout
holds no virtual environment.

The GNN arm shows **no measured improvement**: repeated observations were 8.41, 13.85 and
14.66 s before, and 11.65, 14.80, 15.09 and 17.08 s after. The variance dominates the
difference, and the cost is the interpreter bootstrap plus the network (wheel fetch,
exemplar fetch). The deduplication is structural, not temporal:

| Property | Before | After |
| --- | --- | --- |
| `pip` invocations in the GNN job | 2 | 1 |
| Places the pinned revision is written | 3 (workflow comment, workflow assertion, pin file) | 1 (pin file) |
| Check definitions | 4 (two actions, two inline heredocs) | 2 arms + 1 generated-counts check |
| Workflow steps | 8 | 7 (the added `counts --check` step is new coverage) |

The recorded per-arm numbers live in
[`docs/_generated/COUNTS.md`](docs/_generated/COUNTS.md), generated by
`scripts/docgen/counts.py` from `docs/_generated/timings.json`; re-measure with
`./run.sh measure`.

## Verification performed

```text
./run.sh lint                 -> 0 issues
./run.sh links                -> exit 0 (InstituteOS skipped by reasoned ignorePattern)
./run.sh counts --check       -> docs/_generated/COUNTS.md is current
./run.sh gnn                  -> {"gnn-version": "5.0.3", "models": 1, "result": "verified", "source": "pinned-exemplar"}
./run.sh all                  -> exit 0
```

Failure paths exercised in a scratch copy: an unknown arm exits `2` with usage; a wrong
pin schema, a non-40-hex revision and a missing pin each exit `1` with a named reason.
The workflow file parses, and its job keys remain `markdown-link-check` and
`gnn-conformance` with display name `gnn conformance (pinned)`.

## Not done, and why

- **No manuscript work.** The repository has no `manuscript/` directory and no render
  script, so there is no render path to align with the estate manuscript conventions.
- **No type-checker or test-suite arm.** The repository contains documentation and
  sidecar metadata only; adding an arm that has nothing to check would be decoration.
- **GNN arm timing.** Left as an observation rather than a claim; see the table above.

## Education migration — blocked

The `gen25` step in the lead `courses` repository's
`docs/workflows/education.md` requires emitting `specs/education/gen25.json`
for the generated course units. The working tree was clean before this review.
`git ls-files` lists repository-maintenance documentation, sidecar metadata and
gate tooling, but no generated course units or authored learning objectives.
`README.md` and the existing Major backlog item independently describe the
absence of substantive project material.

The canonical schema requires a verbatim title and learning objectives for each
unit. There is no authored course source here to transcribe. No bundle, adoption
pointer or vendored schema is added: an empty bundle could pass structural
validation without performing the requested migration. The contract and every
other member remain unchanged.

**Unblock:** commit the actual generated course units with their authored titles
and objectives, then transcribe them and run the lead's checker. Until then,
leave the migration pull request open rather than merge a claim of adoption.
