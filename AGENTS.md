# AGENTS.md — working conventions for gen25

This file gives automated agents (and human contributors) the conventions that apply
when working in this repository. It is part of the repository's documentation; see
`docs/README.md` for the full documentation map.

## Repository facts

- Public submodule of the ActiveInferenceInstitute GitHub organization.
- Contents: documentation and InstituteOS metadata only — no source code, no build
  system, no test suite.
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
5. **Keep the linters green.** CI runs markdown link checks and markdownlint;
   verify locally before pushing.

## Conventions

- Conventional commits: `docs:`, `chore:`, `fix:`, `ci:`.
- Docs changes must be accurate and concise; prefer targeted edits over gratuitous
  churn.
- Commit to `main` only after local verification passes.

## Local verification

```sh
npx --yes markdownlint-cli2 "**/*.md"
npx --yes markdown-link-check -q -c mlc_config.json README.md
```

The link check reads `mlc_config.json` from the repository root. CI runs both tools
over **every** Markdown file through `.github/workflows/docs.yml`, so a change to any
`*.md` file must pass both. The workflow also runs a pinned GNN conformance job (see
[`docs/gnn-conformance.md`](docs/gnn-conformance.md)); there is no code, build or test
suite to run.

## Documentation maintenance

- Update [`TO-DO.md`](TO-DO.md) for backlog work and append a dated
  `REVIEW_LOG_<date>.md` per review pass; the process is in
  [`docs/review-process.md`](docs/review-process.md).
- When files are added or removed, update `artifacts[]` in `.aii/config.yaml` and bump
  `meta.updated`, then hand-sync `.aii/docs/INTEGRATION.md` when the `aii-platform`
  kernel is unavailable; see [`docs/sidecar.md`](docs/sidecar.md).
