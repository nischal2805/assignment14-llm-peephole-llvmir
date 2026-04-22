#!/usr/bin/env bash
set -euo pipefail

LLVM_BIN="${LLVM_BIN:-/home/boss/llvm/llvm-build-debug/bin}"
ALIVE_TV="${ALIVE_TV:-/usr/local/bin/alive-tv}"

echo "== Environment check =="
echo "LLVM_BIN=${LLVM_BIN}"
echo "ALIVE_TV=${ALIVE_TV}"
echo

need_exec() {
  local p="$1"
  if [[ ! -x "$p" ]]; then
    echo "Missing executable: $p" >&2
    exit 1
  fi
}

need_exec "${LLVM_BIN}/opt"
need_exec "${LLVM_BIN}/llvm-as"
need_exec "${LLVM_BIN}/llvm-dis"
need_exec "${LLVM_BIN}/llc"
need_exec "${LLVM_BIN}/llvm-diff"
need_exec "${ALIVE_TV}"
command -v python3 >/dev/null 2>&1 || { echo "Missing python3" >&2; exit 1; }

echo "== Versions =="
"${LLVM_BIN}/opt" --version | head -n 2
"${ALIVE_TV}" --version | head -n 3
python3 --version

echo
echo "Environment is ready."
