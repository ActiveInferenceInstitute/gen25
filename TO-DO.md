# TO-DO — gen25 Documentation Backlog

Date: 2026-08-02 · Last reviewed: 2026-08-02

Scoping for the docs-deep pass (see `REVIEW_LOG_2026-08-02.md` for the full audit trail).

Severity scale:
- **Minor** — typo, broken link, formatting, one-line metadata fix.
- **Medium** — missing guide or section, stale section rewrite, doc restructure, small doc-adjacent additions.
- **Major** — large doc system overhaul, new documentation site, cross-cutting refactors.

## Minor

- [x] Commit `1ca023f` message says "CC-BY-4.0 LICENSE" while the committed file is CC0 1.0
      Universal (the `.aii` sidecar agrees with the file: `provenance.license: CC0-1.0`).
      Historical commit-message drift — cannot be rewritten; noted in the review log.
      ✓ (documented in `REVIEW_LOG_2026-08-02.md`)
- [ ] GitHub repository description is unset (API returns `None`) and the README now
      provides on-repo orientation. Setting the description via `gh repo edit` was
      attempted but is **not permitted** for the push token (API 404 — no admin
      access). Open: requires an admin token or manual edit on github.com.

## Medium

- [x] No `README.md` — add repository orientation grounded in `.aii/config.yaml` metadata.
      ✓ (`8f514bb`)
- [x] No `CONTRIBUTING.md` — add a contribution guide matching this repo's reality
      (metadata/docs only, CC0, public submodule). ✓ (`6da7f50`)
- [x] No `SECURITY.md` — add a security reporting policy. ✓ (`6da7f50`)
- [x] No `CITATION.cff` — add citation metadata grounded in the sidecar
      `provenance.citation` text ("Active Inference Institute — gen25.").
      ✓ (`2aeeb82`)
- [x] No CI config — add a lightweight markdown link-check workflow so docs links stay
      valid as the repo grows. ✓ (`1a2e1df`, `.github/workflows/docs.yml`)
- [x] `.aii/config.yaml` `artifacts:` lists only `LICENSE`; extend it to cover the new
      doc artifacts so sidecar metadata stays accurate, and bump `meta.updated`.
      ✓ (`165414c`)
- [x] No top-level TODO/roadmap file — create this `TO-DO.md`. ✓ (this commit)

## Major

- [ ] The sidecar declares capability `documentation` but the repository contains no
      documentation content beyond metadata. A `docs/` folder (architecture notes,
      usage guides, index) should be established **when actual gen25 material exists in
      this repo**. Deferred: there is no source content in the repository to document,
      and fabricating documentation is out of scope for this pass.
- [ ] No automated docs-adjacent checks beyond link checking (e.g. markdown lint,
      front-matter validation). Deferred: disproportionate while the repo holds a
      handful of markdown files; revisit once `docs/` content exists.

## Open / deferred

- Minor: GitHub repository description — needs an admin token or manual edit on
  github.com.
- Major: `docs/` content (see above) — deferred until real content exists.
- Optional: GitHub topics on the repository (requires a decision on taxonomy;
  no grounded source in-repo). Not applied in this pass.
