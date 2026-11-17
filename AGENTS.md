# AGENTS.md — working conventions for gen25

This file gives automated agents (and human contributors) the conventions that apply
when working in this repository. It is part of the repository's documentation; see
`docs/README.md` for the full documentation map.

## Repository facts

- Public submodule of the ActiveInferenceInstitute GitHub organization.
- Contents: documentation, InstituteOS metadata and maintenance Python/shell.
  `./run.sh test` covers maintenance and GNN gate regressions; no substantive gen25
  course or application sources are committed here.
- License: CC0 1.0 Universal (`LICENSE`); the `.aii` sidecar (`provenance.license`)
  declares the same.
- Purpose metadata lives in `.aii/config.yaml` (schema: `aii-sidecar/v1`):
  category `research`, capability `documentation`, federated via InstituteOS.
- The modular documentation lives in [`docs/`](docs/README.md): [`sidecar.md`](docs/sidecar.md),
  [`ci.md`](docs/ci.md), [`gnn-conformance.md`](docs/gnn-conformance.md) and
  [`review-process.md`](docs/review-process.md).

## Hard rules

1. **Never commit private information.** No local paths, personal tool names,
   internal workflow details, credentials, or secrets. This repository is public.
2. **Never fabricate.** Every claim must be grounded in files that exist in this
   repository, or in verifiable public facts. No invented statistics, links,
   citations, or features.
3. **Keep the sidecar accurate.** When files are added or removed, update the
   `artifacts:` list in `.aii/config.yaml` and bump `meta.updated`.
4. **Keep the backlog honest.** Docs work is tracked in `TO-DO.md`
   (Minor / Medium / Major). Review passes append a dated `REVIEW_LOG_<date>.md`.
5. **Keep the linters green.** `./run.sh check` must pass before a commit; run
   `./run.sh all` before opening a pull request. Both arms and the GNN check are
   documented in [`docs/RUN_GUIDE.md`](docs/RUN_GUIDE.md).

## Conventions

- Conventional commits: `docs:`, `chore:`, `fix:`, `ci:`.
- Docs changes must be accurate and concise; prefer targeted edits over gratuitous
  churn.
- Commit to `main` only after local verification passes.
- **Add a check in `run.sh`, never in the workflow.** Every CI step is a `./run.sh` arm,
  so the workflow must never carry a second copy of a command.
- **Never hand-write a number a script can produce.** Counts, gate pins and arm wall times
  live in [`docs/_generated/COUNTS.md`](docs/_generated/COUNTS.md); refresh it with
  `./run.sh counts` after changing tracked files, `scripts/gate_tools.json` or the timings,
  and re-measure with `./run.sh measure`.

## Local verification

```sh
./run.sh check   # generated counts, gate tests, markdownlint over the working tree, link check
./run.sh all     # the same, plus the pinned GNN conformance arm
python3 -B -m unittest discover -s tests -p 'test_maintenance.py' -v
```

The Node tools are pinned in [`scripts/gate_tools.json`](scripts/gate_tools.json) and
fetched by `npx`. There is no separate type-checker arm. `./run.sh test` runs maintenance
and GNN regressions. Maintenance tests need Python, bash and Git; GNN tests additionally
need the independently reviewed resources and prepared runtimes in
[`docs/gnn-conformance.md`](docs/gnn-conformance.md).
No-install source proof is not installed-origin, hosted, native or scientific proof.
CI's `markdown-link-check` job runs `links`, `lint`, `counts --check` and `test`;
the `gnn-conformance` job runs `gnn`. Hosted reviewed-resource delivery remains required.

## Documentation maintenance

- Update [`TO-DO.md`](TO-DO.md) for backlog work and append a dated
  `REVIEW_LOG_<date>.md` per review pass; the process is in
  [`docs/review-process.md`](docs/review-process.md).
- When files are added or removed, update `artifacts[]` in `.aii/config.yaml` and bump
  `meta.updated`, then regenerate all five projections with the canonical
  `aii-platform` generator. Never hand-sync them; unavailable producer custody means
  regeneration remains pending. See [`docs/sidecar.md`](docs/sidecar.md).
