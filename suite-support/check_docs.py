"""Check local Markdown targets and the integrated demo launch navigation."""

import json
import os
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {"node_modules", "build", "work", ".gradle", ".git", "__pycache__", ".idea", ".expo", ".kotlin"}
NAVIGATION = ("README.md", "docs/README.md", "docs/ALL_FUNCTIONS_RU.md",
              "projects/first-result/README.md", "projects/workspace/README.md",
              "projects/api-lab/README.md", "projects/mobile-lab/README.md",
              "projects/runtime-evidence/README.md", "projects/workspace/QA_MATRIX_RU.md")


def anchors(text):
    result = set(re.findall(r'<a\s+(?:id|name)="([^"]+)"', text))
    used = {}
    for heading in re.findall(r"^#{1,6}\s+(.+)$", re.sub(r"```.*?```", "", text, flags=re.S), re.M):
        slug = re.sub(r"[^\w\s-]", "", heading.strip().lower()).replace(" ", "-")
        number = used.get(slug, 0)
        used[slug] = number + 1
        result.add(slug + (f"-{number}" if number else ""))
    return result


def check(root=ROOT, documents=None, navigation=NAVIGATION):
    root = root.resolve()
    if documents is None:
        documents = []
        for directory, children, files in os.walk(root):
            children[:] = [child for child in children if child not in EXCLUDED]
            documents.extend(Path(directory) / name for name in files if name.endswith(".md"))
    destinations = {}
    links = 0
    for document in documents:
        document = document.resolve()
        content = re.sub(r"```.*?```", "", document.read_text(encoding="utf-8"), flags=re.S)
        targets = set()
        for link in re.findall(r"\[[^\]]*\]\(([^)]+)\)", content):
            parsed = urlsplit(link.strip("<>"))
            if parsed.scheme or parsed.netloc:
                continue
            target = (document.parent / unquote(parsed.path)).resolve() if parsed.path else document
            if not target.exists():
                raise ValueError(f"Missing Markdown target in {document.relative_to(root)}: {link}")
            if parsed.fragment and target.suffix == ".md" and unquote(parsed.fragment) not in anchors(target.read_text(encoding="utf-8")):
                raise ValueError(f"Missing Markdown anchor in {document.relative_to(root)}: {link}")
            targets.add(target)
            links += 1
        destinations[document] = targets
    runbook = root / "docs/DEMO_RUNBOOK_RU.md"
    for origin in navigation:
        if runbook not in destinations.get(root / origin, set()):
            raise ValueError(f"Demo instructions are not linked from {origin}")
    return {"status": "DOC_NAVIGATION_PASS", "documents": len(documents),
            "local_links": links, "demo_navigation_entries": len(navigation)}


if __name__ == "__main__":
    print(json.dumps(check()))
