package sample.payment;

import org.springframework.beans.factory.annotation.Value;

public final class SpringPropertyReferences {
    @Value("${server.port:8085}")
    private int serverPort;

    @Value("#{1 + 2}")
    private int injectedExpression;
}
