"""Build/run real Spring Boot; exercise evidence producers without claiming IDEA QA."""

import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from prepare_project import prepare


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path, help="New disposable directory outside the suite")
    parser.add_argument("--tools-source", type=Path, help="Optional separately supplied ArchVerity Tools directory")
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        parser.error("Refusing to overwrite existing output directory")
    output.mkdir(parents=True)
    projects = {mode: output / mode for mode in ("pact-pass", "pact-fail", "drift-pass")}
    for project in projects.values():
        prepare("runtime-evidence", project)
    baseline = projects["pact-pass"]
    wrapper = baseline / ("gradlew.bat" if os.name == "nt" else "gradlew")
    command = [str(wrapper), "installDist", "--console=plain", "--no-daemon", "--warning-mode", "all"]
    if os.name == "nt":
        command = [os.environ.get("COMSPEC", "cmd.exe"), "/d", "/c", *command]
    with (output / "build.log").open("wb") as log:
        subprocess.run(command, cwd=baseline, stdout=log, stderr=subprocess.STDOUT, check=True, timeout=180)
    java_home = os.environ.get("JAVA_HOME")
    java = str(Path(java_home) / "bin/java.exe") if java_home and os.name == "nt" else (str(Path(java_home) / "bin/java") if java_home else shutil.which("java"))
    if not java:
        parser.error("Java runtime unavailable")
    classpath = str(baseline / "build/install/archverity-runtime-evidence/lib/*")
    importer = None
    if args.tools_source:
        sys.path.insert(0, str(args.tools_source.resolve()))
        from archflow_tools.verification_import import import_verification
        importer = import_verification
    observations = []
    for mode, project in projects.items():
        revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=project, text=True).strip()
        environment = os.environ.copy()
        environment["DEMO_SOURCE_REVISION"] = revision
        environment["DEMO_CONFIG_SHA256"] = hashlib.sha256((project / ".archflow.yml").read_bytes()).hexdigest()
        with (output / f"{mode}.log").open("wb") as log:
            process = subprocess.Popen([java, "-Xmx384m", "-cp", classpath, "demo.evidence.DemoApplication"],
                                       cwd=project, env=environment, stdout=log, stderr=subprocess.STDOUT)
            try:
                deadline = time.monotonic() + 45
                while True:
                    try:
                        with urllib.request.urlopen("http://127.0.0.1:18430/demo-identity", timeout=1) as response:
                            identity = json.load(response)
                        if identity["repositoryRevision"] != revision or identity["configurationSha256"] != environment["DEMO_CONFIG_SHA256"]:
                            raise AssertionError("WRONG_TARGET: unexpected server occupies port 18430")
                        break
                    except (urllib.error.URLError, TimeoutError):
                        if process.poll() is not None or time.monotonic() >= deadline:
                            raise RuntimeError(f"Demo app did not become ready; see {mode}.log")
                        time.sleep(0.25)
                work = project / "work"
                work.mkdir()
                fixture = work / "explicit-producer-test-input.json"
                fixture.write_text(json.dumps({"projectId": "runtime-evidence-demo", "runStatus": "COMPLETE", "partial": False,
                                                "analysisContext": {"fingerprint": hashlib.sha256(b"explicitly synthetic producer-test context").hexdigest()},
                                                "producerTestOnly": True}), encoding="utf-8")
                spec = importlib.util.spec_from_file_location(f"capture_{mode.replace('-', '_')}", project / "capture.py")
                capture_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(capture_module)
                receipt = capture_module.capture(fixture, "drift" if mode.startswith("drift") else "pact", mode.endswith("fail"))
                with (project / "reports/beans.json").open(encoding="utf-8") as stream:
                    beans = json.load(stream)["contexts"]["application"]["beans"]
                expected = {"demoTemplate": ("org.springframework.kafka.core.KafkaTemplate", "demoProducerFactory"),
                            "demoListenerFactory": ("org.springframework.kafka.config.ConcurrentKafkaListenerContainerFactory", "demoConsumerFactory")}
                for name, (kind, dependency) in expected.items():
                    if beans[name]["type"] != kind or dependency not in beans[name]["dependencies"]:
                        raise AssertionError(f"Runtime bean dependency missing: {name}")
                canonical = json.loads((project / "reports/payment.verification.archflow.json").read_text())
                evidence = canonical["evidence"][0]
                if evidence["outcome"] != ("FAIL" if mode.endswith("fail") else "PASS"):
                    raise AssertionError("Wrong local verifier outcome")
                if importer:
                    raw = project / evidence["provenance"]["sourcePath"]
                    reference = importer(raw, source_format=evidence["provenance"]["sourceFormat"],
                                         metadata_path=project / "reports/verification-metadata.json",
                                         spec_path=project / "contracts/payment-openapi.json")
                    actual = reference["evidence"][0]
                    if actual["outcome"] != evidence["outcome"] or actual["context"] != evidence["context"] or actual["provenance"]["sourceSha256"] != evidence["provenance"]["sourceSha256"]:
                        raise AssertionError("Canonical producer differs from supplied Tools importer")
                observations.append({"mode": mode, "revision": revision, "outcome": receipt["outcome"],
                                     "real_bean_chains": list(expected), "canonical_importer": "MATCH" if importer else "NOT RUN"})
            finally:
                process.terminate()
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=5)
    result = {"status": "PRODUCER_SMOKE_PASS", "observations": observations,
              "boundary": "Real Boot/TCP/evidence producer; synthetic test context is not an IDEA scan or vendor verification"}
    (output / "receipt.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
