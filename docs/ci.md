# Documentation CI

[`.github/workflows/docs.yml`](../.github/workflows/docs.yml) is the repository's CI. It
has no path filter on purpose: a documentation check must report a verdict on every tip,
including a change that touches no Markdown. It runs on `push` to `main`, on every
`pull_request` and on `workflow_dispatch`.

## Jobs

| Job | What it does |
| --- | --- |
| `markdown-link-check` | Checks every Markdown link with `gaurav-nelson/github-action-markdown-link-check`, then lints every Markdown file with `DavidAnson/markdownlint-cli2-action`. |
| `gnn conformance (pinned)` | Conformance-checks Generalized Notation Notation sketches against a pinned parser — see [`gnn-conformance.md`](gnn-conformance.md). |

Each job declares `timeout-minutes`; the workflow declares `concurrency` with
`cancel-in-progress: true` and read-only `permissions: contents: read`. Action `uses:`
refs are pinned to 40-hex commit SHAs with a `# vX.Y.Z` comment.

## Link checking

The link check reads [`mlc_config.json`](../mlc_config.json) from the repository root. It
retries HTTP 429 responses three times with a 30-second fallback delay and a 20-second
per-link timeout. External links are therefore checked live; add a known-flaky or
intentionally unavailable host to that file only with a reason.

## Markdownlint

Configuration is [`.markdownlint-cli2.yaml`](../.markdownlint-cli2.yaml). It disables
`MD013` (line length) and `MD041` (first line must be a top-level heading) with the
reasons recorded there.

## Run the checks locally

The tools run through `npx`, so no global install is needed:

```sh
npx --yes markdownlint-cli2 "**/*.md"
npx --yes markdown-link-check -q -c mlc_config.json README.md
```

CI runs the link check across every Markdown file; the command above checks one file,
which is enough while editing. Remember that markdownlint applies to every `*.md` file in
the repository, not only the one you changed.
