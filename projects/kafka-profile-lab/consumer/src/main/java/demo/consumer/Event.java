package demo.consumer;
import com.fasterxml.jackson.annotation.JsonProperty;
public record Event(@JsonProperty(required = true) String id, @JsonProperty(required = true) String tenant) {}
