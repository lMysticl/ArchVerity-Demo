"""Feature-specific mutations, each applied to a new exact Git baseline."""

from pathlib import Path

DTO = Path("payment-app/src/main/java/sample/payment/DemoContractsController.java")
AMQP = Path("payment-app/src/main/java/sample/payment/AmqpTopology.java")
CONFIG = Path(".archflow.yml")

EXTRA_SCENARIOS = {
    "nested-request-required": ((DTO, "@NotNull String city, String postalCode", "@NotNull String city, @NotNull String postalCode"),),
    "enum-response-added": ((DTO, "PENDING, PAID, DECLINED", "PENDING, PAID, DECLINED, REFUNDED"),),
    "http-media-type": ((DTO, 'consumes = "application/json"', 'consumes = "application/xml"'),),
    "http-header-condition": ((DTO, 'headers = "X-Demo=local"', 'headers = "X-Demo=changed"'),),
    "amqp-binding": ((AMQP, '.with("orders.*")', '.with("payments.*")'),),
    "dependency-deny": ((CONFIG, "  defaultCluster: core\n", "  defaultCluster: core\ndependencies:\n  policies:\n    demo-no-payments:\n      from: [order-service]\n      to: [payment-service]\n      protocols: [HTTP, KAFKA, AMQP]\n      mode: deny\n  cycles:\n    enabled: true\n    protocols: [HTTP, KAFKA, AMQP]\n    includeSelf: false\n    maxFindings: 100\n    maxVisitedEdges: 100000\n"),),
    "rule-severity": ((CONFIG, "  defaultCluster: core\n", "  defaultCluster: core\nrules:\n  AFG-KAFKA-001:\n    enabled: true\n    severity: INFO\n"),),
    "scope-change": ((CONFIG, "  profiles: [default, dev, demo]", "  profiles: [default]"),),
    "runtime-beans-missing": ((CONFIG, "  defaultCluster: core\n", "  defaultCluster: core\nruntimeBeans:\n  source: reports/beans.json\n  metadata: reports/beans-metadata.json\n  serviceId: payment-service\n  actuatorContextId: application\n  environment: demo\n  maxAgeSeconds: 300\n"),),
    "verification-missing": ((CONFIG, "  defaultCluster: core\n", "  defaultCluster: core\nverification:\n  demo-payments:\n    path: reports/payment.verification.archflow.json\n    specPath: qa-openapi.json\n    environment: demo\n    serviceVersions:\n      payment-service: demo-1\n      order-service: demo-1\n    verifiers:\n      pact: demo-fixture-1\n    maxAgeHours: 24\n"),),
}
