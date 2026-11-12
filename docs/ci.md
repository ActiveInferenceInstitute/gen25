# Documentation CI

[`.github/workflows/docs.yml`](../.github/workflows/docs.yml) is the repository's CI. It
has no path filter on purpose: a documentation check must report a verdict on every tip,
including a change that touches no Markdown. It runs on `push` to `main`, on every
`pull_request` and on `workflow_dispatch`, with `permissions: contents: read` and a
`concurrency` group that cancels superseded runs.

**CI holds no commands of its own.** Every step is a `./run.sh` arm, the same command a
contributor runs locally; the arms and their requirements are in
[`RUN_GUIDE.md`](RUN_GUIDE.md).

## Jobs

| Job key | Display name | What it runs |
| --- | --- | --- |
| `markdown-link-check` | `markdown-link-check` | `./run.sh links`, `./run.sh lint`, `./run.sh counts --check` (60-minute timeout). |
| `gnn-conformance` | `gnn conformance (pinned)` | `./run.sh gnn` (15-minute timeout). |

`markdown-link-check` is the repository's **required status-check context**. Its job key
must not be renamed or removed; a check-run name change would silently wait for a context
that never reports.

## Action pins

`uses:` refs are pinned to 40-hex commit SHAs with a `# vX.Y.Z` comment:

| Action | Pin |
| --- | --- |
| `actions/checkout` | `3d3c42e5aac5ba805825da76410c181273ba90b1` (`v7.0.1`) |
| `ActiveInferenceInstitute/.github/.github/actions/setup-python-uv` | `7159e67315330aac8e414aebae0ad1e999a41448` (AII standard `7159e67`) |

The `gnn-conformance` job uses the organization's composite action rather than
`actions/setup-python`: it installs a pinned `uv` (default `0.13.7`, via the SHA-pinned
`astral-sh/setup-uv`) and the CPython the job asks for, then `./run.sh gnn` bootstraps its
own seeded interpreter from it. The job passes `python-version` from `GNN_PYTHON_VERSION`
(`3.12`) and `enable-cache: "false"`, because this repository has no lockfile for a uv
cache key.

The Node tools are pinned in [`../scripts/gate_tools.json`](../scripts/gate_tools.json)
and are invoked as `npx --yes <tool>@<version>`; there is no second copy of a version
string in the workflow.

## Link checking

`./run.sh links` runs `markdown-link-check` over every tracked Markdown file, using
[`mlc_config.json`](../mlc_config.json) from the repository root. The configuration
retries HTTP 429 responses three times with a 30-second fallback delay and a 20-second
per-link timeout, so external links are checked live.

`ignorePatterns` is the only way a link is skipped, and each entry carries a `reason`:

- `https://github.com/ActiveInferenceInstitute/InstituteOS` — the InstituteOS repository
  is private, so GitHub answers 404 to an unauthenticated client. The prose link is
  correct and stays; only its unverifiable status is skipped.

Add an entry only for a link that is correct but cannot be verified publicly, and never
to hide a link that is actually broken. See [`RUN_GUIDE.md`](RUN_GUIDE.md#link-check-policy).

## Markdownlint

`./run.sh lint` runs `markdownlint-cli2` over the working tree's `**/*.md`, so a page is
checked before it is staged — the same scope CI sees after checkout.
[`../.markdownlint-cli2.yaml`](../.markdownlint-cli2.yaml) disables `MD013` (line length)
and `MD041` (first line must be a heading) with the reasons recorded there, and ignores
`**/.venv/**` and `**/node_modules/**`: the GNN arm installs its pinned parser under
`.venv/gnn`, and those package documents are not this repository's Markdown.

## Generated numbers

`./run.sh counts --check` fails when
[`_generated/COUNTS.md`](_generated/COUNTS.md) no longer matches tracked files, the gate's
pins or the recorded arm timings. Refresh it with `./run.sh counts`; re-measure the timings
with `./run.sh measure`.

## Run the checks locally

```sh
./run.sh check   # counts --check, lint, links: the fast default arm
./run.sh all     # the complete gate, including the pinned GNN arm
```

Individual arms (`./run.sh lint`, `./run.sh links`, `./run.sh gnn`) are listed in
[`RUN_GUIDE.md`](RUN_GUIDE.md).
