"""A public, dependency-free provider for ArchVerity Tools' extension SDK."""


def generate_manifest(context):
    service_id = context.get("serviceId", "demo-extension-service")
    if not isinstance(service_id, str) or not service_id.strip():
        raise ValueError("serviceId must be a nonempty string")
    return {"schemaVersion": 1, "id": "demo-extension",
            "services": [{"id": service_id, "name": "Demo extension service",
                          "modulePath": ".", "owner": "demo-team", "httpEndpoints": [],
                          "kafkaConsumers": [], "kafkaProducers": []}]}
