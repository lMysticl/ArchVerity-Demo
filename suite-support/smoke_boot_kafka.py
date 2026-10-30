"""Compile every public Boot Kafka recipe against real libraries, without a broker."""

import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path

from check_boot_kafka import check_project
from prepare_boot_kafka_case import CASE_NAMES, prepare_case


def smoke(output):
    output = Path(output).resolve()
    if output.exists():
        raise ValueError(f"Refusing to overwrite existing output: {output}")
    output.mkdir(parents=True)
    rows = []
    for boot_line in ("35", "40"):
        for case in CASE_NAMES:
            project = output / f"boot{boot_line}-{case}"
            prepared = prepare_case(case, project, boot_line=boot_line)
            inputs = check_project(project)
            log = output / f"boot{boot_line}-{case}-compile.log"
            wrapper = project / ("gradlew.bat" if os.name == "nt" else "gradlew")
            command = [str(wrapper), "classes", "--console=plain", "--warning-mode", "all", "--no-daemon"]
            print(f"Compile Boot{boot_line} {case}: {project}", flush=True)
            with log.open("xb") as stream:
                completed = subprocess.run(command, cwd=project, stdout=stream,
                                           stderr=subprocess.STDOUT, timeout=600)
            if completed.returncode:
                raise ValueError(f"Compilation failed for Boot{boot_line} {case}; inspect {log}")
            checked = check_project(project)
            rows.append({"bootLine": boot_line, "case": case, "project": str(project),
                         "prepared": prepared, "inputs": inputs, "afterCompile": checked,
                         "compileExitCode": completed.returncode, "compileLog": str(log),
                         "compileLogSha256": hashlib.sha256(log.read_bytes()).hexdigest()})
    report = {"status": "REAL_LIBRARY_COMPILE_PASS", "cases": rows,
              "caseCount": len(rows), "brokerStarted": False,
              "boundary": "Real Boot3.5/4 libraries compile all prepared Java recipes. No plugin scan, installed IDEA, MCP, delivery or broker result is claimed."}
    (output / "result.json").write_bytes((json.dumps(report,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        report = smoke(args.output)
    except (ValueError, subprocess.TimeoutExpired) as error:
        parser.error(str(error))
    print(json.dumps({"status": report["status"], "caseCount": report["caseCount"],
                      "brokerStarted": False, "result": str(args.output / "result.json")}))
