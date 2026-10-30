package demo.boot.consumer;

import com.fasterxml.jackson.annotation.JsonProperty;

public record Event(String id, @JsonProperty(value = "tenant", required = true) String tenant) {}
