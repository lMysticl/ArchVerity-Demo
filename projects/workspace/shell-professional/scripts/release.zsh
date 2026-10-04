#!/usr/bin/env zsh

typeset RELEASE_CHANNEL="stable"
source "${0:A:h}/../lib/common.sh"

function publish_release {
  common_log "publishing ${RELEASE_CHANNEL}"
}

publish_release
