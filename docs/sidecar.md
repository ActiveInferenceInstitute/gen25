# The InstituteOS sidecar

`.aii/` is gen25's committed [InstituteOS](https://github.com/ActiveInferenceInstitute/InstituteOS)
sidecar. It records curated institutional metadata that the GitHub API cannot provide, so
InstituteOS can federate a consistent view across Institute repositories without reading
this repository's content.

## Files

| File | Role |
| --- | --- |
| [`.aii/config.yaml`](../.aii/config.yaml) | The single source of truth: identity, category, maturity, ecosystem relations, key artifacts, provenance and portable tasks. Schema `aii-sidecar/v1`. |
| [`.aii/readiness.json`](../.aii/readiness.json) | This repository's tier, baseline commit and waivers for the organization readiness standard. Schema `aii-readiness/v1`. |
| `.aii/README.md`, `.aii/AGENTS.md` | Human and agent guidance for the folder. |
| `.aii/docs/` | Rendered sidecar documents: `README.md`, `AGENTS.md` and `INTEGRATION.md`. |

## config.yaml

The fields that matter for accuracy:

- `repo` — name, slug, full name and the GitHub description.
- `institute` — `category` (`research`), `maturity` (`wip`) and steward.
- `ecosystem.relations[]` — `owner/repo` entries from the sidecar relation vocabulary;
  gen25 records `referenced-by` InstituteOS.
- `artifacts[]` — the curated entry points, each a repository-relative path that must
  exist. **When a file is added or removed, update this list and bump `meta.updated`.**
- `provenance` — licence (`CC0-1.0`) and the citation text used by `CITATION.cff`.
- `capabilities`, `instituteos.tags`, `tasks` — the declared capability set, topics and
  the portable commands (`inventory` runs `git ls-files`).

Readiness metadata deliberately lives in `readiness.json`, not in `config.yaml`: the
sidecar schema is validated by `aii-platform`, and a readiness change must not break it.

## readiness.json

gen25 is measured against the standard's `content-data` tier. The manifest declares the
tier, the catalogue `standard_version` it was written against, a baseline commit and any
waivers. A waiver needs a non-empty reason and only converts a measured `fail` to
`waived`.

## Rendered documents

`.aii/README.md`, `.aii/AGENTS.md`, `.aii/docs/README.md`, `.aii/docs/AGENTS.md` and
`.aii/docs/INTEGRATION.md` are rendered from `config.yaml` by:

```bash
python -m aii_platform.aii_sidecar docs <repo> --overwrite
```

That package ships in the private `aii-platform` kernel and is not available in every
environment. When it is unavailable, a `config.yaml` change must be **hand-synced** into
`.aii/docs/INTEGRATION.md` (the key-artifacts table mirrors `artifacts[]`). Say so when
you do it, and regenerate once the private environment is available.

## Validation

```bash
python -m aii_platform.aii_sidecar.validate <repo> --completeness
python -m aii_platform.aii_sidecar.run <repo> --list
```

If the kernel is unavailable, review `config.yaml` as plain YAML and confirm every
declared path exists in the repository.
