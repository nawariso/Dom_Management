#!/usr/bin/env bash
set -euo pipefail

project_root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$project_root"

missing=0
for file in README.md docs/system-architecture.md; do
  if [[ ! -f "$file" ]]; then
    echo "[ERROR] Missing required document: $file"
    missing=1
  fi
done

if [[ "$missing" -ne 0 ]]; then
  exit 1
fi

check_section() {
  local file="$1"; shift
  local header="$1"; shift
  if ! grep -qE "^#+ +${header}" "$file"; then
    echo "[ERROR] Missing section '${header}' in ${file}"
    return 1
  fi
}

errors=0
check_section README.md "System Overview" || errors=1
check_section README.md "Architecture" || errors=1
check_section README.md "Deployment" || errors=1
check_section docs/system-architecture.md "CI/CD Workflow" || errors=1
check_section docs/system-architecture.md "Operational Playbooks" || errors=1

if [[ "$errors" -ne 0 ]]; then
  exit 1
fi

echo "[OK] Documentation smoke tests passed."
