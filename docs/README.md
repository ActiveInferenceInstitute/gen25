# Documentation

Index for the gen25 repository documentation. gen25 is a **documentation and
InstituteOS metadata repository**: it contains no source code, no build system and no
test suite, so the documentation describes the repository's own conventions, metadata and
CI rather than an application.

Start with the repository [README](../README.md) for orientation, then use the map below.

## Map

| Document | Purpose |
| --- | --- |
| [`../README.md`](../README.md) | Repository orientation (start here). |
| [`../AGENTS.md`](../AGENTS.md) | Working conventions for automated agents and contributors. |
| [`sidecar.md`](sidecar.md) | The `.aii` InstituteOS sidecar and `readiness.json`: schema, roles and how to keep them accurate. |
| [`ci.md`](ci.md) | The `docs` CI workflow: markdown link checking, markdownlint and how to run both locally. |
| [`gnn-conformance.md`](gnn-conformance.md) | The pinned Generalized Notation Notation conformance job. |
| [`review-process.md`](review-process.md) | How documentation passes are scoped, logged and verified. |
| [`../CONTRIBUTING.md`](../CONTRIBUTING.md) | How to contribute. |
| [`../SECURITY.md`](../SECURITY.md) | Security reporting policy. |
| [`../CITATION.cff`](../CITATION.cff) | Machine-readable citation metadata. |
| [`../LICENSE`](../LICENSE) | CC0 1.0 Universal public-domain dedication. |
| [`../TO-DO.md`](../TO-DO.md) | Scoped documentation backlog. |
| [`../REVIEW_LOG_2026-08-02.md`](../REVIEW_LOG_2026-08-02.md), [`../REVIEW_LOG_2026-11-01.md`](../REVIEW_LOG_2026-11-01.md) | Dated audit logs for documentation review passes. |

## Conventions

- Every claim in this documentation must be grounded in the repository's actual
  files, or in verifiable public facts — nothing fabricated.
- Markdown is linted (markdownlint) and links are checked (markdown-link-check) in
  CI; keep both green. See [`ci.md`](ci.md).
- Documentation backlog items live in [`../TO-DO.md`](../TO-DO.md); review passes
  append a dated `REVIEW_LOG_<date>.md`. See [`review-process.md`](review-process.md).
