#!/usr/bin/env bash
# Run the submitted agent and preserve its complete, unedited stdout/stderr.
# The agent itself writes artifacts under /out; this wrapper owns run.log.
set -uo pipefail

mkdir -p /out
: > /out/run.log
export CAPTURE_STDIO_RUN_LOG=1

python baseline/agent_predict.py \
  --dataset-dir /data \
  --out-dir /out \
  --config config/qwen.yaml \
  --base-model Qwen/Qwen3.8-27B \
  "$@" 2>&1 | tee /out/run.log

exit "${PIPESTATUS[0]}"
