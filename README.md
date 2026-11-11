# gen25

[![License: CC0-1.0](https://img.shields.io/github/license/ActiveInferenceInstitute/gen25)](LICENSE)
[![Docs CI](https://github.com/ActiveInferenceInstitute/gen25/actions/workflows/docs.yml/badge.svg)](.github/workflows/docs.yml)

gen25 — an Active Inference Institute repository.

This repository is part of the [Active Inference Institute](https://www.activeinference.org)
organization. It is federated through InstituteOS via the `.aii` sidecar manifest
(`ecosystem.relations` in `.aii/config.yaml`), which classifies it as a
research-category repository whose declared capability is **documentation**. The
Institute's public [open-source map](https://activeinference.institute/knowledge/)
lists gen25 in the open-source projects family as a project materials repository.

This repository holds documentation and InstituteOS metadata only: there is no source
code, build system or test suite. Its CI checks Markdown links and lint, and runs a
pinned GNN conformance check.

## Contents

| Path | Description |
| --- | --- |
| `README.md` | This file — repository orientation. |
| `docs/README.md` | [Documentation index](docs/README.md). |
| `AGENTS.md` | Working conventions for automated agents and contributors. |
| `LICENSE` | CC0 1.0 Universal public-domain dedication. |
| `.aii/config.yaml` | InstituteOS sidecar metadata (schema: `aii-sidecar/v1`). |
| `mlc_config.json` | `markdown-link-check` configuration used by CI. |
| `TO-DO.md` | Scoped documentation backlog, maintained across docs passes. |
| `CONTRIBUTING.md` | How to contribute to this repository. |
| `SECURITY.md` | Security reporting policy. |
| `CITATION.cff` | Machine-readable citation metadata. |
| `REVIEW_LOG_*.md` | Dated audit logs for documentation review passes. |

## Inventory

List all tracked files (the canonical inventory task declared in the sidecar):

```sh
git ls-files
```

## Documentation

The [documentation index](docs/README.md) maps every document in this repository. The
modular pages are:

| Document | Covers |
| --- | --- |
| [docs/sidecar.md](docs/sidecar.md) | the `.aii` InstituteOS sidecar and `readiness.json` |
| [docs/ci.md](docs/ci.md) | the docs CI workflow, link checking and markdownlint |
| [docs/gnn-conformance.md](docs/gnn-conformance.md) | the pinned GNN conformance job |
| [docs/review-process.md](docs/review-process.md) | backlog severities, review logs and verification |

CI keeps the documentation honest: markdown links are checked and markdown is linted
on every push to `main` and on every pull request. The workflow deliberately has no
path filter, so the checks report a verdict on every tip even when a change touches
no Markdown.

## Readiness

The repository is measured against the organization readiness standard's
`content-data` tier. As of 2026-11-11 the offline report has two blocking gaps — a
lock file and a matching Dependabot ecosystem are expected of the tier but this
repository has no package manager — plus one non-blocking front-matter criterion. The
list and the reason each is deferred are in
[TO-DO.md](TO-DO.md#readiness-standard-gaps-measured-2026-11-11). The `github-api`
criteria need an authenticated token; offline they report `unavailable`, never a pass.

## License

This repository is dedicated to the public domain under
[CC0 1.0 Universal](LICENSE). You may copy, modify, distribute, and use the
material for any purpose, commercial or otherwise, without asking permission.

## Citation

If you reference this repository, cite it as:

> Active Inference Institute — gen25.

Machine-readable citation metadata is available in
[`CITATION.cff`](CITATION.cff).
