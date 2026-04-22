#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

LLVM_BIN="${LLVM_BIN:-/home/boss/llvm/llvm-build-debug/bin}"
ALIVE_TV="${ALIVE_TV:-/usr/local/bin/alive-tv}"

"${ROOT_DIR}/scripts/check_env.sh"

python3 "${ROOT_DIR}/scripts/run_experiments.py" \
  --cases-dir "${ROOT_DIR}/cases" \
  --results-dir "${ROOT_DIR}/results" \
  --llvm-bin "${LLVM_BIN}" \
  --alive-tv "${ALIVE_TV}"

echo
echo "Done. See:"
echo "  ${ROOT_DIR}/results/summary.md"
echo "  ${ROOT_DIR}/results/summary.json"
