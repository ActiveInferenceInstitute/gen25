# Contributing to gen25

Thanks for your interest in contributing. This repository is a **public** submodule of
the Active Inference Institute organization — anything merged here is visible to the
public, so please keep the ground rules below in mind.

## Ground rules

- **Public by default.** Never commit private information: local file paths, personal
  tool names, internal workflow details, credentials, or other secrets. If a file
  carries a secrets placeholder, leave it a placeholder.
- **No fabrication.** Documentation must reflect what actually exists in this
  repository. Verify claims against the files on disk before writing them; do not
  invent statistics, links, citations, or features.
- **CC0 licensing.** The repository is dedicated to the public domain under
  [CC0 1.0 Universal](LICENSE). By contributing, you agree that your contribution is
  made available under those terms.
- **Keep metadata accurate.** If you add or remove artifacts, update the `artifacts:`
  list in [`.aii/config.yaml`](.aii/config.yaml) (and bump `meta.updated`) so the
  InstituteOS sidecar reflects repository reality.

## What lives here

This repository currently contains metadata and documentation only: the `.aii` sidecar,
the license, and the repository's documentation files. There is no source code, build
system, or test suite to run; a lightweight markdown link check runs in CI (see
[`.github/workflows/docs.yml`](.github/workflows/docs.yml)).

## How to contribute

1. Create a branch off `main`: `git checkout -b <your-branch>`.
2. Make your changes, keeping them scoped and grounded (see ground rules).
3. Verify relative links in any markdown you touch resolve to real files.
4. Commit with a clear conventional message (`docs: ...`, `chore: ...`, `fix: ...`).
5. Open a pull request against `main` and describe what you changed and why.

## Review

Maintainers review pull requests for accuracy, licensing compliance, and scope. Small,
focused PRs are reviewed faster than large ones.
