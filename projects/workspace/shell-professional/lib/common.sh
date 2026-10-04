#!/bin/sh

LOG_PREFIX="archflow"

common_log() {
  printf '%s: %s\n' "$LOG_PREFIX" "$1"
}
