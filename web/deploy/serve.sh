#!/usr/bin/env bash
# Build dist/ and serve it on :8090 inside a tmux session, so it outlives the shell.
set -euo pipefail
cd "$(dirname "$0")/.."          # web/
SESSION="${SESSION:-rex-analysis}"
PORT="${PORT:-8090}"

npm run build
tmux has-session -t "$SESSION" 2>/dev/null && tmux kill-session -t "$SESSION"
tmux new-session -d -s "$SESSION" -n web \
  "cd '$PWD' && exec python3 serve_dist.py --host 0.0.0.0 --port '$PORT' --directory dist"
sleep 1
tmux ls | grep "$SESSION"
