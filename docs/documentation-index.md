# Documentation index

Flat index of every long-lived document in `ActiveInferenceInstitute/gen25`. The hub is
[`README.md`](README.md); this page is the complete list, so a page is either linked
here or it is a generated report.

## Orientation

| Document | Purpose |
| --- | --- |
| [`../README.md`](../README.md) | Repository orientation and contents. |
| [`../AGENTS.md`](../AGENTS.md) | Working conventions for automated agents and contributors. |
| [`../CONTRIBUTING.md`](../CONTRIBUTING.md) | How to contribute, and what to verify. |
| [`../SECURITY.md`](../SECURITY.md) | Security reporting policy. |
| [`../CITATION.cff`](../CITATION.cff) | Machine-readable citation metadata. |
| [`../LICENSE`](../LICENSE) | CC0 1.0 Universal public-domain dedication. |

## Operating the repository

| Document | Purpose |
| --- | --- |
| [`RUN_GUIDE.md`](RUN_GUIDE.md) | The `run.sh` gate: arms, what CI runs, requirements, measurement protocol. |
| [`ci.md`](ci.md) | The `docs` workflow: jobs, action pins, link checking, markdownlint. |
| [`gnn-conformance.md`](gnn-conformance.md) | The pinned Generalized Notation Notation conformance arm. |
| [`sidecar.md`](sidecar.md) | The `.aii` InstituteOS sidecar and `readiness.json`. |
| [`review-process.md`](review-process.md) | Backlog severities, review logs and pre-commit verification. |

## Measured and generated

| Document | Producer |
| --- | --- |
| [`_generated/COUNTS.md`](_generated/COUNTS.md) | `./run.sh counts` — inventory counts, gate pins and arm wall times. Do not edit. |
| [`_generated/timings.json`](_generated/timings.json) | `./run.sh measure` — the arm timings `COUNTS.md` reports. Do not edit. |

## Backlog and audit trail

| Document | Purpose |
| --- | --- |
| [`../TO-DO.md`](../TO-DO.md) | Scoped documentation backlog by severity. |
| [`../REVIEW_LOG_2026-08-02.md`](../REVIEW_LOG_2026-08-02.md) | Audit log for the 2026-08-02 documentation pass. |
| [`../REVIEW_LOG_2026-11-01.md`](../REVIEW_LOG_2026-11-01.md) | Audit log for the 2026-11-01 CI-currency pass. |
| [`../REVIEW_LOG_2026-11-12.md`](../REVIEW_LOG_2026-11-12.md) | Audit log for the 2026-11-12 gate and docs pass. |

## InstituteOS sidecar

| Document | Purpose |
| --- | --- |
| [`../.aii/config.yaml`](../.aii/config.yaml) | Sidecar metadata, schema `aii-sidecar/v1` — the single source of truth. |
| [`../.aii/readiness.json`](../.aii/readiness.json) | Declared readiness tier, baseline commit and waivers, schema `aii-readiness/v1`. |
| [`../.aii/README.md`](../.aii/README.md) · [`../.aii/AGENTS.md`](../.aii/AGENTS.md) | Folder guides for the sidecar. |
| [`../.aii/docs/README.md`](../.aii/docs/README.md) · [`../.aii/docs/AGENTS.md`](../.aii/docs/AGENTS.md) · [`../.aii/docs/INTEGRATION.md`](../.aii/docs/INTEGRATION.md) | Rendered sidecar documents. |

## GitHub configuration

| Document | Purpose |
| --- | --- |
| [`../.github/workflows/docs.yml`](../.github/workflows/docs.yml) | The `docs` workflow; each step calls a `run.sh` arm. |
| [`../.github/gnn-pin.json`](../.github/gnn-pin.json) | The GNN importer pin, schema `gnn-importer-pin/v1`. |
| [`../.github/GNN.md`](../.github/GNN.md) | Short pointer: what the conformance job parses. |
| [`../.github/PULL_REQUEST_TEMPLATE.md`](../.github/PULL_REQUEST_TEMPLATE.md) | Pull request checklist. |
| [`../.github/ISSUE_TEMPLATE/documentation.md`](../.github/ISSUE_TEMPLATE/documentation.md) | Documentation issue form. |
| [`../.github/dependabot.yml`](../.github/dependabot.yml) | Dependabot coverage for the workflow actions. |

## Gate implementation

| File | Purpose |
| --- | --- |
| [`../run.sh`](../run.sh) | The gate entry point; every arm lives here. |
| [`../scripts/gate_tools.json`](../scripts/gate_tools.json) | Pinned `markdownlint-cli2` and `markdown-link-check` versions. |
| [`../scripts/gnn_conformance.py`](../scripts/gnn_conformance.py) | The pinned GNN conformance check behind `./run.sh gnn`. |
| [`../scripts/docgen/counts.py`](../scripts/docgen/counts.py) | Generates and verifies `_generated/COUNTS.md`. |
| [`../mlc_config.json`](../mlc_config.json) | `markdown-link-check` configuration, including reasoned exclusions. |
| [`../.markdownlint-cli2.yaml`](../.markdownlint-cli2.yaml) | markdownlint configuration and lint scope. |
