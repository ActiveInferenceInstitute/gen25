# TO-DO — gen25 Documentation Backlog

Date: 2026-08-02 · Last reviewed: 2026-11-12

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
      alongside the link check; the action's default glob lints the repository-root
      Markdown only (see the open item below). Front-matter validation
      is not applicable — repo docs carry no front matter.
      ✓ (`01f09c5`, `.github/workflows/docs.yml`)
- [ ] The sidecar declares capability `documentation` but the repository contains no
      substantive documentation content beyond its own metadata. A modular `docs/` tree
      now documents the repository's infrastructure (sidecar, CI, GNN conformance,
      review process), but architecture notes and usage guides for gen25's own material
      should be added **when that material exists in this repo**. Deferred: there is no
      paper or source content committed here to document, and fabricating documentation
      is out of scope.

- [ ] **Education contract migration blocked:** the `gen25` member step in the
      `courses` repository's `docs/workflows/education.md` requires
      `specs/education/gen25.json` for generated course units. `git ls-files`
      contains no course units or authored learning objectives; `README.md` describes
      this checkout as documentation and metadata only. Commit the actual generated
      course sources and their authored objectives before transcribing the bundle.
      Do not invent units, reinterpret repository-maintenance guides as courses, or
      publish an empty bundle as completed adoption. See the Education migration
      entry in `REVIEW_LOG_2026-11-12.md`.

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
- Minor: `DavidAnson/markdownlint-cli2-action` runs with its default
  `*.{md,markdown}` glob, so `.github/workflows/docs.yml` lints only the
  repository-root Markdown, while `AGENTS.md` and `docs/ci.md` previously implied
  every page. A recursive local run (`npx --yes markdownlint-cli2 "**/*.md"`) reports
  four findings in the rendered `.aii/` documents: MD012 in `.aii/docs/AGENTS.md` and
  `.aii/docs/README.md`, and MD034 in `.aii/README.md`. Broadening the CI glob to
  `**/*.md` requires regenerating those rendered files or fixing the findings first.
  Decide whether to broaden the glob or keep root-only linting.
  ✓ **Resolved 2026-11-12**: the lint step is now the `lint` arm of `./run.sh` and covers
  the working tree's `**/*.md`, so CI and a local run use the same scope; the four
  findings were fixed (two trailing blank lines removed, two bare URLs converted to
  autolinks) and `**/.venv/**` is excluded because the GNN arm installs its parser
  there. See `REVIEW_LOG_2026-11-12.md`.

## Documentation pass 3 (2026-11-11)

- [x] Grew `docs/` from a single index into a modular tree: `sidecar.md` (the `.aii`
      sidecar and `readiness.json`), `ci.md` (the docs workflow, link checking and
      markdownlint), `gnn-conformance.md` (the pinned GNN job) and `review-process.md`
      (backlog, review logs and verification), all linked from the index.
- [x] Corrected `README.md` and `AGENTS.md` for accuracy: the repository is
      documentation and metadata only, CI runs the link check over **every** Markdown
      file (not only `README.md`), and the GNN conformance job exists.
- [x] Bumped `.aii/readiness.json`'s `standard_version` to the current catalogue `1.1.0`.
- [x] Registered `.github/workflows/docs.yml`, `.github/gnn-pin.json` and the two
      `REVIEW_LOG_*.md` files as sidecar artifacts and hand-synced the rendered
      `.aii/docs/INTEGRATION.md` (the `aii-platform` kernel is unavailable offline).

## Readiness standard gaps (measured 2026-11-11)

Measured with the organization checker in the `ActiveInferenceInstitute/.github`
repository (`scripts/check_readiness.py --repo ActiveInferenceInstitute/gen25 --path .`):
the declared `content-data` tier reports 15 pass, **3 fail**, 3 unavailable (the
`CORE-INHERIT-*` `github-api` criteria, offline) and 66 not-applicable.

- [ ] **`CORE-LOCK`** (blocking): the tier expects a tracked lock file
      (`uv.lock`, `package-lock.json`, `Cargo.lock`, …) and this repository has no
      package manager at all. Either the tier's `content-data` definition should not
      require a lock file for a documentation-only repository, or the repository needs a
      reasoned waiver. Owner decision — do not add a lock file just to satisfy the gate.
- [ ] **`CORE-DEPENDABOT-ECOSYSTEM`** (blocking): follows from the same cause —
      `.github/dependabot.yml` exists but no tracked lock file matches a known
      ecosystem. The workflow actions are still watched; only the ecosystem entry is
      unmatched.
- [ ] **`CD-FRONTMATTER`** (non-blocking): the docs workflow has no front-matter
      validation step. The repository's documents carry no front matter, so this is a
      deliberate non-applicability rather than an oversight; record it as such or add a
      validator if front matter is ever introduced.
- [ ] The three `CORE-INHERIT-*` criteria (`CODEOWNERS`, `CONTRIBUTING`, `SECURITY`)
      need `--github`; offline the checker reports them `unavailable` and the gate exits
      `3`, never claiming a pass.

## Gate and docs pass 4 (2026-11-12)

- [x] One gate entry point: `run.sh` exposes `lint`, `links`, `counts`, `gnn`, `check`,
      `all` and `measure` as separately runnable arms, and every step in
      `.github/workflows/docs.yml` calls one of them, so CI holds no second copy of a
      command. Documented in `docs/RUN_GUIDE.md`. ✓
- [x] CI de-duplication: the two marketplace Markdown actions became pinned `npx`
      invocations of the same tools (`scripts/gate_tools.json`), and the GNN job's three
      inline steps (two `pip` invocations plus an inline heredoc, with a duplicated pin
      assertion) became one `./run.sh gnn` step over `scripts/gnn_conformance.py`. The
      pin revision now appears only in `.github/gnn-pin.json`. ✓
- [x] The link check could not pass: `https://github.com/ActiveInferenceInstitute/InstituteOS`
      is a private repository, so GitHub answers 404 to unauthenticated clients and the
      full-tree check reported one dead link. Recorded a reasoned `ignorePatterns` entry
      in `mlc_config.json` instead of removing the prose link. ✓
- [x] Measured numbers moved into a generated document: `docs/_generated/COUNTS.md` is
      written by `scripts/docgen/counts.py` from tracked files, the gate pins and
      `docs/_generated/timings.json` (recorded by `./run.sh measure`), and
      `./run.sh counts --check` fails when it is stale. ✓
- [x] `docs/documentation-index.md` added as the flat index of long-lived documents (the
      repository had a hub but no flat index), and the hub, `README.md` and `AGENTS.md`
      now point at the gate and the generated numbers. ✓
- [ ] The `gnn` arm's wall time is dominated by the interpreter bootstrap and the network:
      four observations on this host ranged from 11.65 s to 17.08 s. Not treated as a
      regression; re-measure with `./run.sh measure` before drawing a conclusion from the
      recorded number.
- [ ] No manuscript directory exists in this repository, so there is no render path to
      align with the estate manuscript conventions. Nothing to do until manuscript
      material is committed here.
