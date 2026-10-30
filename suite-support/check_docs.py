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
              "projects/runtime-evidence/README.md", "projects/kafka-profile-lab/README.md",
              "projects/workspace/QA_MATRIX_RU.md", "projects/boot-upgrade/README.md",
              "docs/PRODUCT_TOUR_RU.md", "docs/PRODUCT_TOUR_EN.md",
              "projects/kafka-boot-lab/README.md")
CURRENT_PRODUCT_VERSION = "5.8.2"
PRIMARY_TABS = {"Changes", "Map", "Problems", "Agents", "Tools"}


def check_current_product(root=ROOT):
    """Reject a reachable guide that still describes the previous product/API."""
    root = Path(root)
    readme = (root / "README.md").read_text(encoding="utf-8")
    if CURRENT_PRODUCT_VERSION not in readme[:700]:
        raise ValueError("README introduction must identify current ArchVerity 5.8.2")
    paragraphs = re.split(r"\n\s*\n", readme)
    tab_claims = [p for p in paragraphs if "primary tabs" in p.lower()]
    if not any(PRIMARY_TABS.issubset(set(re.findall(r"\b[A-Za-z]+\b", p)))
               and not re.search(r"\b(?:Overview|Review|Architecture|Findings)\b", p)
               for p in tab_claims):
        raise ValueError("Current primary tabs must name Changes, Map, Problems, Agents and Tools")
    for name in ("PRODUCT_TOUR_EN.md", "PRODUCT_TOUR_RU.md", "MCP_TOUR_RU.md"):
        text = (root / "docs" / name).read_text(encoding="utf-8")
        if CURRENT_PRODUCT_VERSION not in text[:700]:
            raise ValueError(f"Current product tour is stale: {name}")
    mcp = (root / "docs/MCP_TOUR_RU.md").read_text(encoding="utf-8")
    rows = re.findall(r"(?m)^\|\s*`(archverity_[a-z_]+)`\s*\|([^\n]+)", mcp)
    tools = [name for name, _ in rows]
    registered = json.loads((root / "projects/workspace/qa-support/coverage.json").read_text(encoding="utf-8"))["mcp"]
    if len(tools) != 19 or len(set(tools)) != 19 or set(tools) != set(registered):
        raise ValueError("MCP tour must retain exactly all 19 registered tool recipes")
    simulation = next(text for name, text in rows if name == "archverity_simulate_change")
    if "edits_json" not in simulation or "planned_changes_json" in mcp:
        raise ValueError("Simulation recipe must use the released edits_json argument")
    if not all(token in mcp for token in ("20", "old", "new", "path")):
        raise ValueError("Simulation guide must retain the ordered bounded replacement contract")
    return {"status": "CURRENT_PRODUCT_GUIDES_PASS", "version": CURRENT_PRODUCT_VERSION,
            "primary_tabs": sorted(PRIMARY_TABS), "mcp_tools": len(tools)}


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
