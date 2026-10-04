#!/usr/bin/env bats

@test "deploy requires a service" {
  run bash "$BATS_TEST_DIRNAME/../bin/deploy"
  [ "$status" -ne 0 ]
}

@test "deploy emits a bounded status" {
  run bash "$BATS_TEST_DIRNAME/../bin/deploy" payments
  [ "$status" -eq 0 ]
  [[ "$output" == *scheduled* ]]
}
