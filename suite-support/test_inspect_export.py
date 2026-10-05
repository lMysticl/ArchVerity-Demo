import copy
import json
import struct
import tempfile
import unittest
import zlib
from pathlib import Path

from inspect_export import inspect


def snapshot():
    return {"schemaVersion": 1, "projectId": "demo", "runStatus": "COMPLETE",
            "partial": False, "analysisContext": {"fingerprint": "demo-context"},
            "coverage": {}, "nodes": [], "edges": [], "findings": []}


def chunk(kind, data):
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))


def png():
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(b"\x00\x00\x00\x00")) + chunk(b"IEND", b""))


class ExportInspectionTest(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.path = Path(self.folder.name) / "export"

    def inspect_bytes(self, data, kind, **options):
        self.path.write_bytes(data)
        return inspect(self.path, kind, **options)

    def test_all_export_formats_accept_real_minimal_inputs(self):
        impact = {"schemaVersion": 1, "baseIdentity": "base", "headIdentity": "head",
                  "complete": True, "changedPaths": [], "deltas": [], "impacts": [],
                  "diagnostics": [], "summary": {"breaking": 0, "safe": 0, "unknown": 0}}
        sarif = {"version": "2.1.0", "runs": [{"tool": {"driver": {"name": "ArchVerity"}}, "results": []}]}
        samples = {"png": png(), "svg": b'<svg xmlns="http://www.w3.org/2000/svg"/>',
                   "mermaid": b"flowchart LR\n  order --> payment\n", "markdown": b"# Review\n\nNo changes.\n",
                   "analysis": json.dumps(snapshot()).encode(), "impact": json.dumps(impact).encode(),
                   "sarif": json.dumps(sarif).encode()}
        for kind, data in samples.items():
            with self.subTest(kind=kind):
                self.assertGreater(self.inspect_bytes(data, kind)["bytes"], 0)

    def test_png_signature_and_dimensions_do_not_make_an_image(self):
        bad = b"\x89PNG\r\n\x1a\n" + b"x" * 8 + (1).to_bytes(4, "big") * 2
        with self.assertRaises(ValueError):
            self.inspect_bytes(bad, "png")

    def test_png_rejects_truncation_bad_crc_and_missing_image_or_trailer(self):
        valid = png()
        header = valid[:33]
        for bad in (valid[:8], valid[:-1], valid[:-12], header + chunk(b"IEND", b""),
                    valid[:29] + b"\x00\x00\x00\x00" + valid[33:], valid + b"extra"):
            with self.subTest(bytes=len(bad)), self.assertRaises(ValueError):
                self.inspect_bytes(bad, "png")

    def test_analysis_rejects_wrong_shapes_types_and_blank_identity(self):
        for field, wrong in (("schemaVersion", True), ("projectId", " "), ("runStatus", "success"),
                             ("partial", "false"), ("coverage", []), ("nodes", {}), ("edges", [None]),
                             ("findings", "none"), ("analysisContext", {"fingerprint": ""})):
            bad = copy.deepcopy(snapshot())
            bad[field] = wrong
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.inspect_bytes(json.dumps(bad).encode(), "analysis")

    def test_partial_analysis_is_inspectable_but_cannot_prove_complete_or_another_project(self):
        partial = snapshot()
        partial.update(runStatus="PARTIAL", partial=True)
        self.inspect_bytes(json.dumps(partial).encode(), "analysis")
        for options in ({"require_complete": True}, {"expected_project_id": "other"}):
            with self.subTest(options=options), self.assertRaises(ValueError):
                self.inspect_bytes(json.dumps(partial).encode(), "analysis", **options)
        result = self.inspect_bytes(json.dumps(snapshot()).encode(), "analysis",
                                    require_complete=True, expected_project_id="demo")
        self.assertEqual("demo", result["format_inspection"]["projectId"])

    def test_non_diagrams_whitespace_and_malformed_json_cannot_pass(self):
        for kind, data in (("mermaid", b"# A paragraph mentions flowchart"), ("markdown", b" \n\t"),
                           ("svg", b"<html/>"), ("svg", b"<svg"), ("analysis", b"[]"), ("impact", b"null"),
                           ("sarif", b'{"version":"2.1.0","runs":[{}]}'),
                           ("analysis", b'{"schemaVersion":1,"schemaVersion":2}')):
            with self.subTest(kind=kind, data=data), self.assertRaises(ValueError):
                self.inspect_bytes(data, kind)


if __name__ == "__main__":
    unittest.main()
