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

## Contents

| Path | Description |
| --- | --- |
| `README.md` | This file — repository orientation. |
| `docs/README.md` | [Documentation index](docs/README.md). |
| `AGENTS.md` | Working conventions for automated agents and contributors. |
| `LICENSE` | CC0 1.0 Universal public-domain dedication. |
| `.aii/config.yaml` | InstituteOS sidecar metadata (schema: `instituteos.platform.aii_sidecar`). |
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

The [documentation index](docs/README.md) maps every document in this repository.
CI keeps the documentation honest: markdown links are checked and markdown is linted
on every push and pull request that touches `.md` files.

## License

This repository is dedicated to the public domain under
[CC0 1.0 Universal](LICENSE). You may copy, modify, distribute, and use the
material for any purpose, commercial or otherwise, without asking permission.

## Citation

If you reference this repository, cite it as:

> Active Inference Institute — gen25.

Machine-readable citation metadata is available in
[`CITATION.cff`](CITATION.cff).
