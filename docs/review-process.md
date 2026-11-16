# Documentation pass process

gen25 contains documentation, metadata and maintenance Python/shell. Review maintenance
changes with their offline regressions as well as documentation checks. The audit trail
remains in the dated review logs.

## Backlog

[`../TO-DO.md`](../TO-DO.md) is the scoped backlog. Items are grouped by severity:

- **Minor** — a typo, a broken link, formatting, a one-line metadata fix.
- **Medium** — a missing guide or section, a stale-section rewrite, a doc restructure.
- **Major** — a large documentation overhaul or a new documentation system.

Completed items keep their commit reference and are not deleted. Items that cannot be
done truthfully are marked deferred **with the reason** — for example, substantive
content waits until the repository actually holds the material, because fabricating
documentation is not allowed.

## Review logs

Each documentation pass appends a dated `REVIEW_LOG_<YYYY-MM-DD>.md` recording the
preflight state, the findings by severity, what was implemented (with commit references),
and the verification performed. Review logs:
[`../REVIEW_LOG_2026-08-02.md`](../REVIEW_LOG_2026-08-02.md),
[`../REVIEW_LOG_2026-11-01.md`](../REVIEW_LOG_2026-11-01.md),
[`../REVIEW_LOG_2026-11-12.md`](../REVIEW_LOG_2026-11-12.md) and
[`../REVIEW_LOG_2026-11-16.md`](../REVIEW_LOG_2026-11-16.md).

## Rules that bind a pass

1. **Never fabricate.** Every claim must be grounded in a file that exists in this
   repository or in a verifiable public fact.
2. **Never commit private information.** This repository is public; no local paths,
   credentials or internal details.
3. **Keep the sidecar accurate.** Update `artifacts[]` and bump `meta.updated` in
   [`.aii/config.yaml`](../.aii/config.yaml) when files change — see
   [`sidecar.md`](sidecar.md).
4. **Keep the linters green.** Run the link check and markdownlint before committing —
   see [`ci.md`](ci.md).

## Verification before a commit

```sh
python3 -B -m unittest discover -s tests -p 'test_maintenance.py' -v
./run.sh all
```

Run regressions separately from the existing CI gate. `./run.sh all` contains the
generated-counts check, Markdown lint, link check and pinned GNN arm; `check` is its
fast subset. GNN source/installed tests require reviewed resources and real prepared
runtimes; link/exemplar/provisioning paths may need network.
See [`RUN_GUIDE.md`](RUN_GUIDE.md) and [`gnn-conformance.md`](gnn-conformance.md).

Also confirm every internal relative link resolves to a real file, that the `.aii` files
still parse, and that [`_generated/COUNTS.md`](_generated/COUNTS.md) was refreshed with
`./run.sh counts` after intended additions/removals are admitted to the Git index.
