# InstituteOS integration — gen25

## Identity

| Field | Value |
| --- | --- |
| Repository | `ActiveInferenceInstitute/gen25` |
| Affiliation | `institute` |
| Category | `research` |
| Status | `active` |
| Maturity | `wip` |
| Steward | Active Inference Institute |
| Default branch | `main` |
| Current release | — |
| License | `CC0-1.0` |
| Citation | Active Inference Institute — gen25. |

## Federation

| Setting | Value |
| --- | --- |
| Dashboard mode | `repos` |
| Analytics | `true` |
| Dashboard | `true` |
| Sync policy | `pull` |
| Registries | — |
| Tags | gen25 |

## Ecosystem relations

| Repository | Relation | Note |
| --- | --- | --- |
| `ActiveInferenceInstitute/InstituteOS` | `referenced-by` | Federated via the InstituteOS .aii manifest. |

## Key artifacts

| Path | Kind | Description |
| --- | --- | --- |
| `LICENSE` | `doc` | License. |
| `README.md` | `doc` | Repository orientation. |
| `docs/README.md` | `doc` | Documentation index. |
| `AGENTS.md` | `doc` | Working conventions for agents and contributors. |
| `CONTRIBUTING.md` | `doc` | Contribution guide. |
| `SECURITY.md` | `doc` | Security reporting policy. |
| `CITATION.cff` | `doc` | Citation metadata. |
| `TO-DO.md` | `doc` | Documentation backlog. |
| `docs` | `doc` | Documentation tree. |
| `docs/sidecar.md` | `doc` | The InstituteOS sidecar and readiness manifest. |
| `docs/ci.md` | `doc` | The docs CI workflow, link checking and markdownlint. |
| `docs/gnn-conformance.md` | `doc` | The pinned Generalized Notation Notation conformance job. |
| `docs/review-process.md` | `doc` | Documentation backlog, review logs and verification. |
| `.github/workflows/docs.yml` | `code` | Docs CI workflow (link check, markdownlint, GNN conformance). |
| `.github/gnn-pin.json` | `data` | The pinned GNN parser revision the conformance job reads. |
| `REVIEW_LOG_2026-11-01.md` | `doc` | Dated audit log for the 2026-11-01 CI-currency pass. |

## Portable tasks

| Task | Command | Working directory | Description |
| --- | --- | --- | --- |
| `inventory` | `git ls-files` | `.` | List tracked files. |

## Validation

```bash
python -m aii_platform.aii_sidecar.validate <repo> --completeness
python -m aii_platform.aii_sidecar docs <repo> --overwrite
python -m aii_platform.aii_sidecar.run <repo> --list
```

The sidecar is valid when `validate` prints `OK` and reports no missing artifact,
manifest, link, or declared-doc path. Completeness is a curation target, not a
runtime requirement.

## Data boundary

This sidecar carries metadata only. It does not grant execution permission, does not
replace the repository's own documentation, and must not be used to move private
content into a public repository. Task execution is limited to trusted checkouts.
