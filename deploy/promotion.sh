#!/usr/bin/env bash
set -euo pipefail

# Simple promotion helper to push a revision through dev -> staging -> prod with gates.
REVISION=${1:-${GITHUB_SHA:-HEAD}}

if [[ -z "${ARGOCD_SERVER:-}" || -z "${ARGOCD_AUTH_TOKEN:-}" ]]; then
  echo "ARGOCD_SERVER and ARGOCD_AUTH_TOKEN must be set" >&2
  exit 1
fi

./argocd login "$ARGOCD_SERVER" --auth-token "$ARGOCD_AUTH_TOKEN" --insecure

promote() {
  local app=$1
  local wait_ns=$2
  echo "Promoting ${REVISION} to ${app}"
  ./argocd app sync "$app" --revision "$REVISION" --timeout "$wait_ns"
  ./argocd app wait "$app" --health --timeout "$wait_ns"
}

promote dom-management-dev 300
# smoke hooks run via Argo CD annotation; ensure success before continuing.
promote dom-management-staging 600
# e2e hooks ensure stability; manual approval recommended before production.
promote dom-management-prod 900
