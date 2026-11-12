# Gate and run guide

`run.sh` in the repository root is the **single gate entry point**. Every step in
[`.github/workflows/docs.yml`](../.github/workflows/docs.yml) is a `./run.sh` arm, so a
local run and CI execute the same command; the workflow holds no second copy of a check.
Change a check in `run.sh`, never in the workflow.

```sh
./run.sh check   # fast default arm: generated-counts check, tests, lint, links
./run.sh all     # the complete gate: check + the pinned GNN conformance arm
```

## Arms

| Arm | What it runs | When to use it |
| --- | --- | --- |
| `./run.sh lint` | `markdownlint-cli2` over the working tree's Markdown | After editing prose. |
| `./run.sh links` | `markdown-link-check` over every tracked Markdown file with [`mlc_config.json`](../mlc_config.json) | After editing a link or adding a page. |
| `./run.sh counts` | Regenerates [`_generated/COUNTS.md`](_generated/COUNTS.md); `--check` verifies it instead of writing | After changing tracked files, the gate tool pins or the arm timings. |
| `./run.sh test` | The gate's own regression tests, stdlib `unittest` over `tests/` | After changing a gate script or the acceptance rule it enforces. |
| `./run.sh gnn` | Pinned GNN conformance — see [`gnn-conformance.md`](gnn-conformance.md) | After touching a `*.gnn.md` sketch or the pin. |
| `./run.sh check` | `counts --check`, then `test`, then `lint`, then `links` | Before every commit: the fast arm. |
| `./run.sh all` | `check`, then `gnn` | Before opening a pull request. |
| `./run.sh measure` | Runs `lint`, `links` and `gnn` once each and records [`_generated/timings.json`](_generated/timings.json) | After changing what an arm does. |

There is deliberately no type-checker arm: this repository contains documentation and
InstituteOS metadata, not an application. The one executable suite is `./run.sh test`,
which covers the gate's own acceptance logic — for example that the pinned GNN type
checker must return exactly `True` and not the truthy-adjacent `2`. Each test builds a
throwaway repository with a stubbed `gnn` package, so the arm needs no network and no
parser install. `./run.sh all` is therefore the complete gate.

The `links` arm checks the **tracked** file list rather than walking the checkout. That
keeps a local run identical to CI and keeps it away from `.venv/gnn`, where the GNN arm
installs a parser that ships its own documentation. The `lint` arm deliberately covers the
working tree, so a page is linted before it is staged; `.venv` and `node_modules` are
ignored in [`.markdownlint-cli2.yaml`](../.markdownlint-cli2.yaml).

## What CI runs

| Workflow job | Display name | Arms |
| --- | --- | --- |
| `markdown-link-check` | `markdown-link-check` (required status-check context) | `links`, `lint`, `counts --check`, `test` |
| `gnn-conformance` | `gnn conformance (pinned)` | `gnn` |

[`ci.md`](ci.md) records the workflow's action pins, its Python setup and the
link-check configuration. Do not rename or drop the `markdown-link-check` job: it is
the required context.

## Requirements

| Arm | Needs |
| --- | --- |
| `lint`, `links` | `node`/`npx`, `git`, `python3` (reads the tool pins) |
| `counts` | `python3`, `git` |
| `test` | `python3` (stdlib only; no network, no GNN install) |
| `gnn` | `python3`, `uv` (creates `.venv/gnn`), network access |

The Node tools are pinned in [`../scripts/gate_tools.json`](../scripts/gate_tools.json)
and are fetched by `npx`; that file is the only place their versions appear. The `gnn`
arm creates a seeded interpreter in `.venv/gnn` (git-ignored) and installs the pinned
parser there. Override the interpreter with `GNN_PYTHON=/path/to/python` (existing
environment, no bootstrap) or `GNN_PYTHON_VERSION=3.12` (version to bootstrap). CI sets
`GNN_PYTHON_VERSION` to `3.12`; the job installs that interpreter with the
organization's `setup-python-uv` composite action.

## Measured numbers

Numbers that a script can produce are never typed into prose. The gate's wall times and
the repository's counts live in [`_generated/COUNTS.md`](_generated/COUNTS.md), generated
from tracked files and from `_generated/timings.json` by
[`../scripts/docgen/counts.py`](../scripts/docgen/counts.py). `./run.sh check` fails when
the generated document is stale.

`./run.sh measure` records one run per arm on the machine that runs it, with the tool
caches warm and `.venv/gnn` removed first so the GNN arm bootstraps its interpreter and
parser. The JSON carries the host, the Node version and that protocol, so a number is
never presented without the conditions that produced it. The `gnn` arm is dominated by
the interpreter install and the network; expect it to vary between runs on one host.

## Link-check policy

[`mlc_config.json`](../mlc_config.json) retries HTTP 429 three times with a 30-second
fallback delay and a 20-second per-link timeout, so external links are checked live.
`ignorePatterns` entries are the only way a link is skipped, and every entry carries a
`reason`. Today there is one: `https://github.com/ActiveInferenceInstitute/InstituteOS`
is a private repository, which GitHub answers with 404 for unauthenticated clients, so
the public prose link cannot be verified from CI. Add an entry only for a link that is
correct but unverifiable, and never to hide a broken one.
