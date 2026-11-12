#!/usr/bin/env bash
# Single gate entry point for gen25.
#
# Every CI step in .github/workflows/docs.yml calls one of these arms, so a local
# run and CI execute byte-identical commands. Add or change a check here, never in
# the workflow.
#
#   ./run.sh lint      markdownlint-cli2 over the working tree's Markdown
#   ./run.sh links     markdown-link-check over every tracked Markdown file
#   ./run.sh counts    regenerate docs/_generated/COUNTS.md (--check: verify it)
#   ./run.sh gnn       pinned GNN conformance check (network + uv required)
#   ./run.sh check     counts --check, then lint, then links (fast default arm)
#   ./run.sh all       check, then gnn (the complete gate)
#   ./run.sh measure   run each arm once and record docs/_generated/timings.json
#
# There is no type-checker or test-suite arm: this repository carries documentation
# and sidecar metadata only. See docs/RUN_GUIDE.md.
set -euo pipefail

ROOT="$(CDPATH='' cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

PYTHON="${PYTHON:-python3}"
TOOLS_JSON="$ROOT/scripts/gate_tools.json"
# Two glob dialects on purpose: markdownlint-cli2 needs an explicit recursive
# glob, while a git pathspec without a slash already matches at any depth.
MARKDOWN_LINT_GLOB='**/*.md'
MARKDOWN_GIT_PATHSPEC='*.md'

usage() {
  printf "usage: ./run.sh ARM\n\n"
  sed -n '/^#   \.\/run\.sh /p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
  printf "\nNo type-checker or test-suite arm: this repository carries documentation\n"
  printf "and sidecar metadata only. See docs/RUN_GUIDE.md.\n"
}

require() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "run.sh: '$1' is required but not on PATH" >&2
    return 1
  }
}

tool_version() {
  "$PYTHON" - "$TOOLS_JSON" "$1" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as handle:
    print(json.load(handle)[sys.argv[2]])
PY
}

arm_lint() {
  require npx
  npx --yes "markdownlint-cli2@$(tool_version markdownlint-cli2)" "$MARKDOWN_LINT_GLOB"
}

arm_links() {
  require npx
  require git
  local files=() file
  while IFS= read -r file; do
    files+=("$file")
  done < <(git ls-files -- "$MARKDOWN_GIT_PATHSPEC")
  if [ "${#files[@]}" -eq 0 ]; then
    echo "run.sh: no tracked Markdown files to check" >&2
    return 1
  fi
  npx --yes "markdown-link-check@$(tool_version markdown-link-check)" \
    -q -c mlc_config.json "${files[@]}"
}

arm_counts() {
  "$PYTHON" "$ROOT/scripts/docgen/counts.py" "$@"
}

arm_gnn() {
  local python="${GNN_PYTHON:-$ROOT/.venv/gnn/bin/python}"
  if [ ! -x "$python" ]; then
    require uv
    uv venv --no-project --seed --python "${GNN_PYTHON_VERSION:-3.12}" \
      "$ROOT/.venv/gnn" >&2
  fi
  "$python" "$ROOT/scripts/gnn_conformance.py"
}

arm_measure() {
  require node
  "$PYTHON" - "$ROOT" <<'PY'
import json
import platform
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

root = Path(sys.argv[1])
arms = (("lint",), ("links",), ("gnn",))
records = {}
for arm in arms:
    if arm[0] == "gnn":
        # Measure the arm from a cold interpreter environment, as CI sees it.
        shutil.rmtree(root / ".venv" / "gnn", ignore_errors=True)
    started = time.perf_counter()
    subprocess.run([str(root / "run.sh"), *arm], cwd=root, check=True)
    records[arm[0]] = round(time.perf_counter() - started, 2)

node = subprocess.run(
    ["node", "--version"], capture_output=True, text=True, check=True
).stdout.strip()
payload = {
    "recorded": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "host": f"{platform.system()} {platform.machine()}",
    "node": node,
    "protocol": (
        "one run per arm on this host with warm tool caches; "
        ".venv/gnn removed first so the GNN arm bootstraps its interpreter and parser"
    ),
    "arms": records,
}
target = root / "docs" / "_generated" / "timings.json"
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
for arm, seconds in records.items():
    print(f"{arm}\t{seconds:.2f}s")
print(f"wrote {target.relative_to(root)}")
PY
}

arm="${1:-}"
if [ -n "$arm" ]; then shift; fi

case "$arm" in
  lint) arm_lint "$@" ;;
  links) arm_links "$@" ;;
  counts) arm_counts "$@" ;;
  gnn) arm_gnn "$@" ;;
  check)
    arm_counts --check
    arm_lint
    arm_links
    ;;
  all)
    arm_counts --check
    arm_lint
    arm_links
    arm_gnn
    ;;
  measure) arm_measure "$@" ;;
  "" | help | -h | --help) usage ;;
  *)
    echo "run.sh: unknown arm '$arm'" >&2
    usage >&2
    exit 2
    ;;
esac
