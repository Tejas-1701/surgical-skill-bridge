#!/usr/bin/env bash
set -euo pipefail

SURROL_COMMIT=b151ad6
REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
SURROL_DIR="$REPO_ROOT/ext/SurRoL"

if [ ! -d "$SURROL_DIR" ]; then
  git clone -q https://github.com/med-air/SurRoL.git "$SURROL_DIR"
  git -C "$SURROL_DIR" checkout -q "$SURROL_COMMIT"
fi

pip install -q -r "$REPO_ROOT/requirements.txt"
pip install -q --no-deps -e "$SURROL_DIR"
pip install -q --no-deps -e "$REPO_ROOT"
echo "setup complete"
