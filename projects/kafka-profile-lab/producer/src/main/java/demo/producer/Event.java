package demo.producer;
import com.fasterxml.jackson.annotation.JsonProperty;
public record Event(@JsonProperty(required = true) String id) {}
