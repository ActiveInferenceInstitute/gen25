# TO-DO — gen25 Documentation Backlog

Date: 2026-08-02 · Last reviewed: 2026-11-01

Scoping for the docs-deep pass and the ambitious follow-up pass (see
`REVIEW_LOG_2026-08-02.md` for the full audit trail). The 2026-11-01 CI-currency
pass is logged in `REVIEW_LOG_2026-11-01.md`.

Severity scale:

- **Minor** — typo, broken link, formatting, one-line metadata fix.
- **Medium** — missing guide or section, stale section rewrite, doc restructure, small doc-adjacent additions.
- **Major** — large doc system overhaul, new documentation site, cross-cutting refactors.

## Minor

- [x] Commit `1ca023f` message says "CC-BY-4.0 LICENSE" while the committed file is CC0 1.0
      Universal (the `.aii` sidecar agrees with the file: `provenance.license: CC0-1.0`).
      Historical commit-message drift — cannot be rewritten; noted in the review log.
      ✓ (documented in `REVIEW_LOG_2026-08-02.md`)
- [x] GitHub repository description was unset (API returned `None`). **Resolved
      2026-11-01**: the live description reads "Documentation-focused Active
      Inference Institute project repository, federated through InstituteOS via the
      `.aii` sidecar manifest." (verified with `gh api repos/ActiveInferenceInstitute/gen25`).
      The 2026-08-02 blocker — a push token without admin scope — no longer applies
      on this machine. ✓ (see `REVIEW_LOG_2026-11-01.md`)
- [x] `actions/checkout` pinned to `v4` while the fleet has moved to `v7`. Bumped
      to the newest stable major in `.github/workflows/docs.yml`; the two
      documentation actions keep their current majors. ✓ (completed in this change,
      `REVIEW_LOG_2026-11-01.md`)

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

- Minor: the sidecar's `repo.description` ("gen25 — an Active Inference Institute
  repository.") is shorter than the live GitHub description. Decide whether the
  sidecar should mirror the live text; not changed in the 2026-11-01 pass so the
  identity field is not edited incidentally.
- Major: substantive `docs/` content (architecture notes, usage guides) — deferred
  until real gen25 material exists in this repository.
- Optional: GitHub topics on the repository. Partially resolved: `active-inference`
  and `documentation` are now set on the repository; any further topics still need a
  grounded taxonomy source.
