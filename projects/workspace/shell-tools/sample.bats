#!/usr/bin/env bats

@test "ArchFlow Bats runner passes" {
  run bash -c 'printf ArchFlow'
  [ "$status" -eq 0 ]
  [ "$output" = "ArchFlow" ]
}

@test "ArchFlow Bats runner reports failure" {
  false
}
