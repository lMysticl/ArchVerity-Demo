package sample.payment;

import com.fasterxml.jackson.annotation.*;
import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.annotation.JsonNaming;

@JsonNaming(PropertyNamingStrategies.SnakeCaseStrategy.class)
public class BasicWireDto extends WireParent {
    @JsonProperty("wire_id") public String id;
    @JsonProperty(access = JsonProperty.Access.READ_ONLY) public String serverReference;
    @JsonProperty(access = JsonProperty.Access.WRITE_ONLY) public String clientNote;
    @JsonIgnore public String ignoredInternalValue;
    @JsonIgnore(false) public String visibleValue;
    public PaymentMethod method;
}
class WireParent { public String inheritedName; }

@JsonTypeInfo(use = JsonTypeInfo.Id.NAME, include = JsonTypeInfo.As.PROPERTY, property = "kind")
@JsonSubTypes({@JsonSubTypes.Type(value = CardMethod.class, name = "card"),
              @JsonSubTypes.Type(value = BankMethod.class, name = "bank")})
interface PaymentMethod {}
record CardMethod(String lastDigits) implements PaymentMethod {}
record BankMethod(String bankCode) implements PaymentMethod {}
