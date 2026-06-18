#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

LLVM_BIN="${LLVM_BIN:-/home/boss/llvm/llvm-build-debug/bin}"
ALIVE_TV="${ALIVE_TV:-/usr/local/bin/alive-tv}"

"${ROOT_DIR}/scripts/check_env.sh"

echo "======================================"
echo "Generating LLM candidate rewrites..."
echo "======================================"

python3 "${ROOT_DIR}/src/generate_candidates.py" \
  --llvm-dir "${ROOT_DIR}/testcases/llvm_ir" \
  --mlir-dir "${ROOT_DIR}/testcases/mlir"

echo
echo "======================================"
echo "Running LLVM experiments..."
echo "======================================"

python3 "${ROOT_DIR}/src/run_experiments.py" \
  --cases-dir "${ROOT_DIR}/testcases/llvm_ir" \
  --results-dir "${ROOT_DIR}/results" \
  --llvm-bin "${LLVM_BIN}" \
  --alive-tv "${ALIVE_TV}"

echo
echo "======================================"
echo "Running MLIR experiments..."
echo "======================================"

python3 "${ROOT_DIR}/src/run_mlir_experiments.py" \
  --cases-dir "${ROOT_DIR}/testcases/mlir" \
  --results-dir "${ROOT_DIR}/results_mlir"

echo
echo "Done. See:"
echo "  ${ROOT_DIR}/results/summary.md"
echo "  ${ROOT_DIR}/results/summary.json"
echo "  ${ROOT_DIR}/results_mlir/summary.md"
echo "  ${ROOT_DIR}/results_mlir/summary.json"