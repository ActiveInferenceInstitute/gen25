# REVIEW_LOG_2026-08-02 — gen25 docs-deep pass

Date: 2026-08-02
Repo: ActiveInferenceInstitute/gen25
Branch: main (default; `origin/HEAD -> origin/main`)

## Phase 0 — Preflight

- `git fetch origin` clean; working tree clean on `main`, fast-forward not needed.
- Inventory (tracked files): `LICENSE` (CC0 1.0 Universal, official legal text) and
  `.aii/config.yaml` (InstituteOS sidecar, schema `instituteos.platform.aii_sidecar`).
- No README, no `docs/` folder, no AGENTS.md/CLAUDE.md, no CI config (`.github/`
  absent), no existing TODO/roadmap files.
- HEAD before pass: `1ca023f` ("add .aii sidecar (100% complete) + CC-BY-4.0 LICENSE
  (InstituteOS metadata)"). Repo created 2025-03-14 (`1260b3c` "Initial commit").
- The `.git` entry is a gitdir pointer file — this is a git submodule, as expected.

## Phase 1 — Mega-deep docs review (findings)

Repository has essentially no documentation: the only human-facing artifact was the
LICENSE file. Findings by severity:

**Minor**
1. Commit `1ca023f` message says "CC-BY-4.0 LICENSE", but the committed file is
   CC0 1.0 Universal. The `.aii` sidecar (`provenance.license: CC0-1.0`) agrees with
   the file, so the file/sidecar are consistent and the drift is in the historical
   commit message only. Cannot be rewritten without history rewrite; not done.
2. GitHub repository description unset (API returns `None`); no topics set.
3. `.aii/config.yaml` `meta.updated` would go stale on any sidecar edit.

**Medium**
4. No `README.md` — visitors get no orientation; GitHub renders no description.
5. No `CONTRIBUTING.md`.
6. No `SECURITY.md`.
7. No `CITATION.cff` (sidecar already carries a citation text).
8. No CI; docs links would be unguarded.
9. `.aii` sidecar `artifacts:` lists only `LICENSE`; would drift as docs were added.
10. No top-level TODO/roadmap file for tracking docs work.

**Major**
11. Sidecar declares capability `documentation` but the repo contains no documentation
    content beyond metadata — nothing to index in a `docs/` folder yet. Deferred until
    real gen25 content exists (no fabrication).
12. No docs-adjacent automation beyond link checking. Deferred as disproportionate for
    the current doc count.

Accuracy checks: LICENSE is the verbatim CC0 1.0 legal text (no drift). Sidecar facts
(repo name, slug, license, citation, capability, category) verified against the files
and the GitHub API. No code exists to cross-check docstrings against.

## Phase 2 — Scoping

Created `TO-DO.md` (Minor / Medium / Major sections, per-repo conventions established
fresh since none existed).

## Phase 3 — Implementation

Commits (chronological):

1. `8f514bb` docs: add README with repository orientation
2. `6da7f50` docs: add CONTRIBUTING and SECURITY guides
3. `2aeeb82` docs: add CITATION.cff citation metadata
4. `1a2e1df` ci: add markdown link check workflow for docs
5. `165414c` chore: refresh .aii sidecar artifact metadata
6. (this commit) docs: add TO-DO backlog and review log

Details:
- `README.md`: orientation grounded strictly in `.aii/config.yaml` (description,
  category, capability, ecosystem relation, license) and git history; contents table;
  inventory command (`git ls-files`, the sidecar-declared task); license and citation
  sections.
- `CONTRIBUTING.md`: public-repo ground rules (no private info, no fabrication, CC0
  dedication, sidecar metadata upkeep), contribution flow, review notes.
- `SECURITY.md`: private reporting via GitHub security advisories
  (URL verified live, HTTP 200) and the Institute website; scope statement.
- `CITATION.cff`: cff-version 1.2.0; title/abstract/authors/license/url grounded in
  sidecar and LICENSE; `date-released: 2025-03-14` from initial commit.
- `.github/workflows/docs.yml`: `gaurav-nelson/github-action-markdown-link-check@v1`
  on push/PR touching markdown; read-only permissions.
- `.aii/config.yaml`: `artifacts:` extended to the six doc artifacts; `meta.updated`
  bumped to 2026-08-02.
- Not applied: `gh repo edit` to set the GitHub description — API 404 for the push
  token (no admin access); recorded as open in `TO-DO.md`.

## Phase 4 — Verification

- YAML validity checked for `.aii/config.yaml`, `CITATION.cff`, workflow file.
- Internal relative links in all markdown verified to resolve to real files.
- External links verified live: `https://www.activeinference.org` (200),
  `https://github.com/ActiveInferenceInstitute/gen25/security/advisories` (200).
- `https://github.com/ActiveInferenceInstitute/InstituteOS` returns 404 publicly
  (repo not publicly reachable) — the README therefore references InstituteOS by
  name only, without a dead hyperlink.
- Heavy test suites: none exist in this repo (no code); CI is a docs link check only.
- Push to `origin/main` verified; `git status` clean.

## Notes

- Nothing private was referenced or committed; the repo contains no secrets (checked
  `.aii/config.yaml` and all added files for placeholders/credentials).
