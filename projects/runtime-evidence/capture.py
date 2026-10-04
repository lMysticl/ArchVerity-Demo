"""Capture real local beans and a labelled local HTTP verifier report together."""

import argparse
import hashlib
import json
import os
import subprocess
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def read_http(path):
    try:
        response = urllib.request.urlopen(f"http://127.0.0.1:18430{path}", timeout=5)
    except urllib.error.HTTPError as error:
        response = error
    with response:
        body = response.read(8 * 1024 * 1024 + 1)
        if len(body) > 8 * 1024 * 1024:
            raise ValueError("Local response exceeds 8 MiB")
        return response.status, body


def write_new(path, payload):
    if path.exists():
        raise ValueError(f"Refusing to overwrite existing evidence: {path.name}")
    temporary = path.with_name(path.name + ".tmp")
    created = False
    try:
        with temporary.open("xb") as stream:
            created = True
            stream.write(payload)
        os.replace(temporary, path)
    finally:
        if created:
            temporary.unlink(missing_ok=True)


def capture(snapshot_path, source_format="pact", negative=False):
    def git(*args):
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT or git("status", "--porcelain"):
        raise ValueError("Expected the clean isolated project used by run_local.py")
    head = git("rev-parse", "HEAD")
    config_sha = hashlib.sha256((ROOT / ".archflow.yml").read_bytes()).hexdigest()
    snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    context_fingerprint = snapshot.get("analysisContext", {}).get("fingerprint")
    if snapshot.get("projectId") != "runtime-evidence-demo" or snapshot.get("runStatus") != "COMPLETE" or snapshot.get("partial") or not context_fingerprint:
        raise ValueError("Export the current COMPLETE runtime-evidence-demo snapshot after configuring these imports")
    status, identity_bytes = read_http("/demo-identity")
    identity = json.loads(identity_bytes)
    if status != 200 or identity != {"repositoryRevision": head, "configurationSha256": config_sha,
                                    "environment": "demo", "providerVersion": "demo-1"}:
        raise ValueError("WRONG_TARGET: running application revision/configuration differs")
    status, beans = read_http("/actuator/beans")
    observed = time.time_ns() // 1_000_000
    if status != 200 or "application" not in json.loads(beans).get("contexts", {}):
        raise ValueError("Expected actual Actuator context application")

    status, payment = read_http("/intentional-error" if negative else "/payments/42")
    executed = time.time_ns() // 1_000_000
    passed = status == 200 and json.loads(payment) == {"id": "42", "status": "PAID", "version": "demo-1"}
    if passed == negative:
        raise ValueError("Local verifier outcome differs from requested positive/negative control")
    spec = ROOT / "contracts/payment-openapi.json"
    context = {"schemaVersion": 1, "repositoryRevision": head, "environment": "demo",
               "configurationFingerprint": context_fingerprint,
               "serviceVersions": {"payment-service": "demo-1"},
               "specSha256": hashlib.sha256(spec.read_bytes()).hexdigest()}
    metadata = {"providerServiceId": "payment-service", "verifierVersion": "local-demo-http-1",
                "runId": "local-demo-" + str(uuid.uuid4()), "executedAtEpochMs": executed, "context": context}
    if source_format == "pact":
        raw_name = "pact-result.json"
        raw = json.dumps({"success": passed, "providerName": "payment-service", "providerApplicationVersion": "demo-1"}).encode()
        importer_format = "pact-broker-verification"
    else:
        raw_name = "drift-result.xml"
        failure = "" if passed else '<failure message="Intentional local HTTP failure" />'
        raw = f'<testsuite name="local-demo-http" tests="1" failures="{int(not passed)}"><testcase name="payment-shape">{failure}</testcase></testsuite>'.encode()
        importer_format = "drift-junit"
    imported = time.time_ns() // 1_000_000
    envelope = {"schemaVersion": 1, "evidence": [{**metadata, "verifierId": source_format,
                 "outcome": "PASS" if passed else "FAIL",
                 "provenance": {"sourceFormat": importer_format, "sourcePath": f"reports/{raw_name}",
                                "sourceSha256": hashlib.sha256(raw).hexdigest(),
                                "importedAtEpochMs": imported, "trust": "LOCAL_FILE"}}]}
    bean_metadata = {"schemaVersion": 1, "serviceId": "payment-service", "actuatorContextId": "application",
                     "repositoryRevision": head, "environment": "demo", "configurationFingerprint": context_fingerprint,
                     "observedAtEpochMs": observed, "sourceSha256": hashlib.sha256(beans).hexdigest()}
    if git("rev-parse", "HEAD") != head or git("status", "--porcelain") or hashlib.sha256((ROOT / ".archflow.yml").read_bytes()).hexdigest() != config_sha:
        raise ValueError("Source/configuration changed during capture")
    encode = lambda value: (json.dumps(value, indent=2) + "\n").encode()
    outputs = {"beans.json": beans, "beans-metadata.json": encode(bean_metadata), raw_name: raw,
               "verification-metadata.json": encode(metadata), "payment.verification.archflow.json": encode(envelope)}
    directory = ROOT / "reports"
    if any((directory / name).exists() for name in outputs):
        raise ValueError("Use a new project copy for each evidence scenario; existing outputs are preserved")
    directory.mkdir(exist_ok=True)
    for name, payload in outputs.items():
        write_new(directory / name, payload)
    return {"status": "CAPTURED", "revision": head, "outcome": "PASS" if passed else "FAIL",
            "verifier": "local-demo-http-1", "trust": "LOCAL_FILE", "files": list(outputs),
            "note": "Real local HTTP check; Pact/Drift report shape only, no vendor execution claim"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--format", choices=("pact", "drift"), default="pact")
    parser.add_argument("--negative", action="store_true")
    args = parser.parse_args()
    try:
        print(json.dumps(capture(args.snapshot, args.format, args.negative)))
    except ValueError as error:
        parser.error(str(error))
