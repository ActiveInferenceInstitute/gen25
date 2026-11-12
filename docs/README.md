# Documentation

Index for the gen25 repository documentation. gen25 is a **documentation and
InstituteOS metadata repository**: it contains no application source code and no build
system, and its only executable tests cover the gate script itself, so the documentation
describes the repository's own conventions, metadata and CI rather than an application.

Start with the repository [README](../README.md) for orientation, then use the map below.
Every long-lived document is also listed in the flat
[documentation index](documentation-index.md).

## Map

| Document | Purpose |
| --- | --- |
| [`../README.md`](../README.md) | Repository orientation (start here). |
| [`../AGENTS.md`](../AGENTS.md) | Working conventions for automated agents and contributors. |
| [`RUN_GUIDE.md`](RUN_GUIDE.md) | The `./run.sh` gate: arms, what CI runs, requirements, measurement protocol. |
| [`ci.md`](ci.md) | The `docs` CI workflow: jobs, action pins, link checking and markdownlint. |
| [`gnn-conformance.md`](gnn-conformance.md) | The pinned Generalized Notation Notation conformance arm. |
| [`sidecar.md`](sidecar.md) | The `.aii` InstituteOS sidecar and `readiness.json`: schema, roles and how to keep them accurate. |
| [`review-process.md`](review-process.md) | How documentation passes are scoped, logged and verified. |
| [`documentation-index.md`](documentation-index.md) | Flat index of every long-lived document in the repository. |
| [`_generated/COUNTS.md`](_generated/COUNTS.md) | Generated: inventory counts, gate pins and arm wall times. |
| [`../CONTRIBUTING.md`](../CONTRIBUTING.md) | How to contribute. |
| [`../SECURITY.md`](../SECURITY.md) | Security reporting policy. |
| [`../CITATION.cff`](../CITATION.cff) | Machine-readable citation metadata. |
| [`../LICENSE`](../LICENSE) | CC0 1.0 Universal public-domain dedication. |
| [`../TO-DO.md`](../TO-DO.md) | Scoped documentation backlog. |
| [`../REVIEW_LOG_2026-08-02.md`](../REVIEW_LOG_2026-08-02.md), [`../REVIEW_LOG_2026-11-01.md`](../REVIEW_LOG_2026-11-01.md), [`../REVIEW_LOG_2026-11-12.md`](../REVIEW_LOG_2026-11-12.md) | Dated audit logs for documentation review passes. |

## Conventions

- Every claim in this documentation must be grounded in the repository's actual
  files, or in verifiable public facts — nothing fabricated.
- The gate is `./run.sh`; every CI step calls one of its arms. Run
  `./run.sh check` before committing and `./run.sh all` before opening a pull request —
  see [`RUN_GUIDE.md`](RUN_GUIDE.md).
- Markdown is linted and links are checked by those arms; keep both green. See
  [`ci.md`](ci.md).
- Numbers a script can produce live in [`_generated/COUNTS.md`](_generated/COUNTS.md),
  which `./run.sh counts` refreshes and `./run.sh check` verifies. Prose links there
  instead of copying a count or a wall time.
- Documentation backlog items live in [`../TO-DO.md`](../TO-DO.md); review passes
  append a dated `REVIEW_LOG_<date>.md`. See [`review-process.md`](review-process.md).
