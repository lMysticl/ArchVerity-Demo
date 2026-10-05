import copy
import hashlib
import json
import unittest

from check_public_tree import ROOT, MEDIA_PATHS, check_media


class PublicMediaBoundaryTest(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads((ROOT / "suite-support/public_media.json").read_text(encoding="utf-8"))
        self.relative = "docs/media/first-result-3.0.4.mp4"
        self.data = (ROOT / self.relative).read_bytes()

    def test_inspected_recording_and_poster_are_accepted(self):
        for relative in MEDIA_PATHS:
            with self.subTest(path=relative):
                check_media(relative, (ROOT / relative).read_bytes(), self.manifest)

    def test_another_video_cannot_be_admitted_by_expanding_the_manifest(self):
        changed = copy.deepcopy(self.manifest)
        changed["files"]["docs/media/unreviewed.mp4"] = changed["files"][self.relative]
        with self.assertRaisesRegex(ValueError, "Unreviewed media path"):
            check_media("docs/media/unreviewed.mp4", self.data, changed)

    def test_changed_recording_bytes_are_rejected(self):
        for relative in MEDIA_PATHS:
            with self.subTest(path=relative):
                data = (ROOT / relative).read_bytes()
                modified = data[:-1] + bytes([data[-1] ^ 1])
                with self.assertRaisesRegex(ValueError, "Unreviewed media bytes"):
                    check_media(relative, modified, self.manifest)

    def test_even_reviewed_bytes_cannot_bypass_the_public_size_limit(self):
        large = b"x" * 2_000_001
        for relative in MEDIA_PATHS:
            with self.subTest(path=relative):
                changed = copy.deepcopy(self.manifest)
                changed["files"][relative] = {"bytes": len(large), "sha256": hashlib.sha256(large).hexdigest()}
                with self.assertRaisesRegex(ValueError, "large staged artifact"):
                    check_media(relative, large, changed)


if __name__ == "__main__":
    unittest.main()
