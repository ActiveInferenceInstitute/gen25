# TO-DO — gen25 Documentation Backlog

Date: 2026-08-02 · Last reviewed: 2026-08-02

Scoping for the docs-deep pass and the ambitious follow-up pass (see
`REVIEW_LOG_2026-08-02.md` for the full audit trail).

Severity scale:

- **Minor** — typo, broken link, formatting, one-line metadata fix.
- **Medium** — missing guide or section, stale section rewrite, doc restructure, small doc-adjacent additions.
- **Major** — large doc system overhaul, new documentation site, cross-cutting refactors.

## Minor

- [x] Commit `1ca023f` message says "CC-BY-4.0 LICENSE" while the committed file is CC0 1.0
      Universal (the `.aii` sidecar agrees with the file: `provenance.license: CC0-1.0`).
      Historical commit-message drift — cannot be rewritten; noted in the review log.
      ✓ (documented in `REVIEW_LOG_2026-08-02.md`)
- [ ] GitHub repository description is unset (API returns `None`). Setting it via
      `gh repo edit` or `gh api -X PATCH` returns HTTP 404 — the push token has
      contents-write scope only, no admin access. **Open**: requires an admin token
      or a manual edit on github.com.

## Medium

- [x] No `README.md` — add repository orientation grounded in `.aii/config.yaml` metadata.
      ✓ (`8f514bb`)
- [x] No `CONTRIBUTING.md` — add a contribution guide matching this repo's reality
      (metadata/docs only, CC0, public submodule). ✓ (`6da7f50`)
- [x] No `SECURITY.md` — add a security reporting policy. ✓ (`6da7f50`); bare URLs
      converted to autolinks for markdownlint. ✓ (`224cf6c`)
- [x] No `CITATION.cff` — add citation metadata grounded in the sidecar
      `provenance.citation` text ("Active Inference Institute — gen25.").
      ✓ (`2aeeb82`)
- [x] No CI config — add a lightweight markdown link-check workflow so docs links stay
      valid as the repo grows. ✓ (`1a2e1df`, `.github/workflows/docs.yml`)
- [x] `.aii/config.yaml` `artifacts:` lists only `LICENSE`; extend it to cover the
      doc artifacts so sidecar metadata stays accurate, and bump `meta.updated`.
      ✓ (`165414c`; extended again in `ead1e55`)
- [x] No top-level TODO/roadmap file — create this `TO-DO.md`. ✓ (`1e0932d`)
- [x] No `AGENTS.md` — add working conventions for automated agents and contributors.
      ✓ (`2f3bc22`)
- [x] No `docs/` index — add `docs/README.md` mapping every document in the repo.
      ✓ (`2f3bc22`)
- [x] No issue/PR templates — add a documentation issue form and a PR template that
      encodes the verification checklist. ✓ (`e753644`)

## Major

- [x] Docs-adjacent automation: markdownlint added to CI
      (`.markdownlint-cli2.yaml`, `DavidAnson/markdownlint-cli2-action@v24`)
      alongside the link check; all markdown files pass lint. Front-matter validation
      is not applicable — repo docs carry no front matter.
      ✓ (`01f09c5`, `.github/workflows/docs.yml`)
- [ ] The sidecar declares capability `documentation` but the repository contains no
      documentation content beyond metadata. A `docs/` folder now exists (index in
      `docs/README.md`), but architecture notes and usage guides should be added
      **when actual gen25 material exists in this repo**. Deferred: there is no source
      content in the repository to document, and fabricating documentation is out of
      scope for this pass.

## Open / deferred

- Minor: GitHub repository description — needs an admin token or a manual edit on
  github.com (verified: `gh api -X PATCH` → 404 with the current push token).
- Major: substantive `docs/` content (architecture notes, usage guides) — deferred
  until real gen25 material exists in this repository.
- Optional: GitHub topics on the repository (no grounded taxonomy source in-repo).
  Not applied in this pass.
