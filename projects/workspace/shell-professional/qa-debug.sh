#!/usr/bin/env bash
set -euo pipefail

qa_value="start"
qa_step() {
  local input="$1"
  qa_value="${input}-checked"
}

qa_step "$qa_value"
printf '%s\n' "$qa_value"
