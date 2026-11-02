# REVIEW_LOG_2026-11-01 — gen25 CI currency pass

## Scope

Reviewed `.github/workflows/docs.yml`, `TO-DO.md`, `README.md`, `docs/README.md`,
`AGENTS.md`, and `.aii/config.yaml`. The repository is documentation and metadata
only — no source, no build system, no test suite — so this pass checks the CI
configuration and the accuracy of the repository's own records. It does not add
documentation content.

## Findings

- Minor: the workflow pinned `actions/checkout@v4` while the fleet has moved to
  `v7`. The two documentation actions (`markdown-link-check`, `markdownlint-cli2`)
  stay on their current major versions.
- Minor: `TO-DO.md` recorded the unset GitHub repository description as blocked on
  an admin token. As of this pass the live description is set (verified below);
  the blocker no longer applies to this machine, and the item is closed. The
  sidecar's own `repo.description` still carries the earlier short text, which is
  recorded as an open decision rather than changed here.
- Nothing else: the link check and markdownlint cover every markdown file, and all
  of them pass locally.

## Verification

- `npx --yes markdownlint-cli2 "**/*.md"`: all markdown files pass (0 issues).
- `gh api repos/ActiveInferenceInstitute/gen25 --jq .description`: returns
  "Documentation-focused Active Inference Institute project repository, federated
  through InstituteOS via the .aii sidecar manifest." — the description is set,
  `default_branch` is `main`, and the topics `active-inference` and
  `documentation` are present.
- `.github/workflows/docs.yml` parses as YAML; its jobs, steps, and action
  references were read back after the edit. The workflow only triggers on
  markdown changes, so this pass touches `.md` files to make the checks run.
- `git ls-files` inventory unchanged except for this log.

## Decisions

- The checkout action moves to the newest stable major (`v7`) and keeps the
  workflow's existing floating-major style; the two documentation actions are left
  alone because they are not part of this pass.
- The sidecar `repo.description` is **not** rewritten to match the live GitHub
  description in this pass: that text is a repository identity field, and the
  change is recorded here and in `TO-DO.md` so it is decided deliberately rather
  than slipped into a CI-currency change.

## Follow-up

- Decide whether `.aii/config.yaml` `repo.description` should mirror the live
  GitHub description.
- Substantive `docs/` content stays deferred until real gen25 material exists in
  this repository (unchanged from the 2026-08-02 pass).
