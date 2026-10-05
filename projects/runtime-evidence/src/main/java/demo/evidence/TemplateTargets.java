package demo.evidence;

import org.springframework.core.env.Environment;

/** Editable targets for afvalue and afgetprop; afcfgrecord uses a new Java file. */
public final class TemplateTargets {
    // Put the caret above this field and expand afvalue with demo.value/default.
    private String demoValue = "default";

    public String read(Environment environment) {
        // Expand afgetprop in a scratch method; this existing call is the oracle.
        return environment.getRequiredProperty("demo.value");
    }
}
