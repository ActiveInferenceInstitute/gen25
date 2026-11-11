# Documentation pass process

gen25 is maintained as a documentation and metadata repository, so its changes are
reviewed as documentation changes. This page records the process the repository already
follows; the audit trail is in the dated review logs.

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
and the verification performed. Two logs exist today:
[`../REVIEW_LOG_2026-08-02.md`](../REVIEW_LOG_2026-08-02.md) and
[`../REVIEW_LOG_2026-11-01.md`](../REVIEW_LOG_2026-11-01.md).

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
npx --yes markdownlint-cli2 "**/*.md"
npx --yes markdown-link-check -q -c mlc_config.json README.md
```

Also confirm every internal relative link resolves to a real file, and that the `.aii`
files still parse. There is no code, build or test suite in this repository, so these are
the strongest checks available.
