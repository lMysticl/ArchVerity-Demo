package sample.order;

import org.springframework.web.client.RestClient;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

/** Fixed literal targets permit conservative source inference; no requests run. */
public class FluentPaymentClients {
    private final RestTemplate restTemplate = new RestTemplate();
    private final RestClient restClient = RestClient.create("http://payments");
    private final WebClient webClient = WebClient.create("http://payments");

    public PaymentView restTemplate() {
        return restTemplate.getForObject("http://payments/demo/42", PaymentView.class);
    }
    public PaymentView restClient() {
        return restClient.get().uri("/demo/42").retrieve().body(PaymentView.class);
    }
    public Mono<PaymentView> webClient() {
        return webClient.get().uri("/demo/42").retrieve().bodyToMono(PaymentView.class);
    }
}
