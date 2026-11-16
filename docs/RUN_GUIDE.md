# Gate and run guide

`run.sh` in the repository root is the **single gate entry point**. Every step in
[`.github/workflows/docs.yml`](../.github/workflows/docs.yml) is a `./run.sh` arm, so a
local run and CI execute the same command; the workflow holds no second copy of a check.
Change a check in `run.sh`, never in the workflow.

```sh
./run.sh check   # fast default arm: generated-counts check, lint, links
./run.sh all     # the complete gate: check + the pinned GNN conformance arm
```

## Arms

| Arm | What it runs | When to use it |
| --- | --- | --- |
| `./run.sh lint` | `markdownlint-cli2` over the working tree's Markdown | After editing prose. |
| `./run.sh links` | `markdown-link-check` over every tracked Markdown file with [`mlc_config.json`](../mlc_config.json) | After editing a link or adding a page. |
| `./run.sh counts` | Regenerates [`_generated/COUNTS.md`](_generated/COUNTS.md); `--check` verifies it instead of writing | After changing tracked files, the gate tool pins or the arm timings. |
| `./run.sh gnn` | Pinned GNN conformance — see [`gnn-conformance.md`](gnn-conformance.md) | After touching a `*.gnn.md` sketch or the pin. |
| `./run.sh check` | `counts --check`, then `lint`, then `links` | Before every commit: the fast arm. |
| `./run.sh all` | `check`, then `gnn` | Before opening a pull request. |
| `./run.sh measure` | Runs `lint`, `links` and `gnn` once each and records [`_generated/timings.json`](_generated/timings.json) | After changing what an arm does. |

There is no type-checker or regression-test arm. Run maintenance regressions separately:

```sh
python3 -B -m unittest discover -s tests -p 'test_maintenance.py' -v
```

They need Python, bash, Git and `dirname`; they use real temporary files and Git
indexes without installation or network. The separate GNN regressions require the
reviewed resources and prepared runtimes in [`gnn-conformance.md`](gnn-conformance.md).

The `links` arm checks the **tracked** file list rather than walking the checkout. That
keeps a local run identical to CI and keeps it away from `.venv/gnn`, where the GNN arm
installs a parser that ships its own documentation. The `lint` arm deliberately covers the
working tree, so a page is linted before it is staged; `.venv` and `node_modules` are
ignored in [`.markdownlint-cli2.yaml`](../.markdownlint-cli2.yaml).

## What CI runs

| Workflow job | Display name | Arms |
| --- | --- | --- |
| `markdown-link-check` | `markdown-link-check` (required status-check context) | `links`, `lint`, `counts --check` |
| `gnn-conformance` | `gnn conformance (pinned)` | `gnn` |

[`ci.md`](ci.md) records the workflow's action pins, its Python setup and the
link-check configuration. Do not rename or drop the `markdown-link-check` job: it is
the required context.

## Requirements

| Arm | Needs |
| --- | --- |
| `lint`, `links` | `node`/`npx`, `git`, `python3` (reads the tool pins) |
| `counts` | `python3`, `git` |
| `gnn` | Prepared Python and reviewed bootstrap/manifest; default provisioning or exemplar acquisition also needs network/`uv` |

The Node tools are pinned in [`../scripts/gate_tools.json`](../scripts/gate_tools.json)
and are fetched by `npx`. With `GNN_PYTHON` unset, the `gnn` arm selects its default
interpreter in `.venv/gnn`, bootstrapping it with `uv` if absent.
An explicit `GNN_PYTHON` must name an executable regular file: empty, missing,
directory and non-executable selections fail before default bootstrap.
`GNN_PYTHON_VERSION` chooses the bootstrap version; CI selects `3.12`.
`--no-install` prohibits parser installation, not missing-interpreter bootstrap:
for strictly offline use, select an existing interpreter explicitly and supply all
reviewed inputs. Source mode also requires explicit `GNN_PACKAGE_ROOT`.
See [`gnn-conformance.md`](gnn-conformance.md); hosted resource delivery is not yet proved.

## Measured numbers

Numbers that a script can produce are never typed into prose. The gate's wall times and
the repository's counts live in [`_generated/COUNTS.md`](_generated/COUNTS.md), generated
from tracked files and from `_generated/timings.json` by
[`../scripts/docgen/counts.py`](../scripts/docgen/counts.py). `./run.sh check` fails when
the generated document is stale. Canonical inventory is the Git index: untracked or
ignored scratch does not count. Admit intended additions/removals before final
generation. Inventory regeneration preserves the recorded timing values.

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
