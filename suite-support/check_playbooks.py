"""Validate and render complete, source-bound function and entry-point guides."""

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GROUPS = {"DEV": "Иконки", "KEY": "Keystore и X.509", "DEVS": "Инструменты разработчика",
          "ARC": "Анализ контрактов", "UI": "Навигация и граф", "CFG": "Конфигурация",
          "IMP": "Impact и review", "EVD": "Внешние evidence", "TEAM": "Экспорты",
          "IDE": "Редактор", "CLI": "Tools и CI", "MCP": "MCP"}
FIELDS = {"id", "title", "source_capability", "capability_ids", "inputs", "purpose", "setup",
          "steps", "negative", "restore", "capture", "consumer_status"}


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate(data, entry_points, root=ROOT):
    if not isinstance(data, dict) or set(data) != {"schema_version", "source_product_version", "source_inventory_commit", "features"}:
        raise ValueError("Abbreviated catalog is not a complete function playbook")
    if data["schema_version"] != 1:
        raise ValueError("Unsupported function playbook schema")
    features = data["features"]
    ids = [f["id"] for f in features]
    if not ids or len(ids) != len(set(ids)):
        raise ValueError("Function IDs must be nonempty and unique")
    inventory = read(root / "suite-support/function_inventory.json")
    expected_functions = {f["id"]: f["capability"] for f in inventory["functions"]}
    if {f["id"]: f["source_capability"] for f in features} != expected_functions:
        raise ValueError("A source function was omitted or its capability was weakened")
    capability_ids = {f["id"] for f in read(root / "suite-support/features.json")}
    covered = set()
    for feature in features:
        if set(feature) != FIELDS:
            raise ValueError(f"Incomplete playbook fields: {feature['id']}")
        if feature["consumer_status"] != "NOT_RUN":
            raise ValueError("A prepared guide cannot invent a consumer PASS; store observed runs separately")
        for field in ("title", "source_capability", "purpose", "setup", "restore", "capture"):
            if not isinstance(feature[field], str) or not feature[field].strip():
                raise ValueError(f"Missing {field}: {feature['id']}")
        if not feature["steps"] or not feature["inputs"] or not feature["capability_ids"]:
            raise ValueError(f"Missing executable recipe/input/capability: {feature['id']}")
        for step in [*feature["steps"], feature["negative"]]:
            if set(step) != {"do", "expect"} or any(not isinstance(step[k], str) or not step[k].strip() for k in step):
                raise ValueError(f"Missing concrete trigger/oracle: {feature['id']}")
        for relative in feature["inputs"]:
            path = Path(relative)
            if path.is_absolute() or ".." in path.parts or not (root / path).is_file():
                raise ValueError(f"Missing/unsafe input: {feature['id']}: {relative}")
        covered.update(feature["capability_ids"])
    if covered != capability_ids:
        raise ValueError(f"Previous capability coverage changed: missing={capability_ids-covered}, unknown={covered-capability_ids}")
    registered = read(root / "projects/workspace/qa-support/coverage.json")
    expected = {f"{group}:{name}" for group, entries in registered.items() for name in entries}
    actual = [entry["id"] for entry in entry_points]
    if set(actual) != expected or len(actual) != len(set(actual)):
        raise ValueError("Every registered entry point needs its own guide binding")
    for entry in entry_points:
        if set(entry) != {"id", "feature_id", "trigger", "expect", "inputs"} or entry["feature_id"] not in ids:
            raise ValueError(f"Invalid entry-point playbook: {entry['id']}")
        if not entry["trigger"].strip() or not entry["expect"].strip() or not entry["inputs"]:
            raise ValueError(f"Missing entry-point trigger/oracle: {entry['id']}")
        for relative in entry["inputs"]:
            path = Path(relative)
            if path.is_absolute() or ".." in path.parts or not (root / path).is_file():
                raise ValueError(f"Missing entry-point input: {entry['id']}: {relative}")
    return {"functions": len(features), "entry_points": len(actual), "previous_capabilities": len(covered)}


def guides(data, entry_points):
    lines = ["# Все функции ArchVerity: демонстрация и проверка", "",
             f"Source scope: ArchVerity {data['source_product_version']}; исходный inventory commit `{data['source_inventory_commit']}`.",
             "62 пользовательские возможности, все 87 registered entry points и все 41 прежние capability recipes связаны с конкретными входами.",
             "Статус ниже относится к подготовленным сценариям. Реальное выполнение отмечайте отдельно в [RUN_RECORD](RUN_RECORD.md).", "",
             "[Пошаговый запуск всех пяти лабораторий](DEMO_RUNBOOK_RU.md) · [Оглавление документации](README.md)", "",
             "## Подготовка", "", "Для первого finding подготовьте отдельную first-result copy через `suite-support/prepare_project.py` и откройте её с JDK 21. Для архитектуры и Impact создайте новую workspace copy тем же helper и получите настоящий полный снимок чистого HEAD в IDEA.",
             "API запускается через `projects/api-lab/serve.py`. Mobile имеет свой lockfile/native prerequisites. Runtime evidence требует настоящего current IDEA export; producer smoke явно использует synthetic test context.",
             "При отсутствии SDK/device, SSH, real entitlement, PasswordSafe/Vault input или Tools distribution записывайте точную недоступную зависимость. Остальные независимые проверки продолжаются. Signing, credentials и device install/clear/uninstall требуют отдельного разрешения.", "",
             "[Каталог входов](FEATURE_CATALOG.md) · [87 точек входа](ENTRY_POINTS_RU.md) · [Архитектура и 19 мутаций](ARCHITECTURE_WALKTHROUGH_RU.md) · [Средовые команды и MCP](ENVIRONMENT_CHECKS_RU.md)", "",
             "## Содержание", "", "| ID | Функция |", "| --- | --- |"]
    for f in data["features"]:
        lines.append(f"| {f['id']} | [{f['title']}](#{f['id'].lower()}) |")
    previous = None
    for f in data["features"]:
        group = f["id"].split("-", 1)[0]
        if group != previous:
            lines.extend(["", f"## {GROUPS[group]}"])
            previous = group
        lines.extend(["", f"<a id=\"{f['id'].lower()}\"></a>", f"### {f['id']} — {f['title']}", "",
                      f"**Зачем:** {f['purpose']}", "", f"**Подготовка:** {f['setup']}", "",
                      "**Входы:** " + ", ".join(f"[{Path(p).name}](../{p})" for p in f["inputs"]), ""])
        for index, step in enumerate(f["steps"], 1):
            lines.extend([f"{index}. {step['do']}", f"   Ожидаемое наблюдение: {step['expect']}"])
        lines.extend(["", f"**Контрпример:** {f['negative']['do']}", f"Ожидаемое наблюдение: {f['negative']['expect']}", "",
                      f"**Восстановление:** {f['restore']}", "", f"**Доказательство:** {f['capture']}", "",
                      f"**Consumer run:** `{f['consumer_status']}`. Capability IDs: " + ", ".join(f["capability_ids"]) + "."])
    entries = ["# Все зарегистрированные точки входа", "",
               "Каждая из 87 записей имеет отдельные trigger, oracle и inputs. Подробные positive/negative/recovery сценарии — в [полном руководстве](ALL_FUNCTIONS_RU.md).",
               "Это prepared coverage; фактический consumer run записывается отдельно в [RUN_RECORD](RUN_RECORD.md).", ""]
    previous = None
    for e in entry_points:
        group = e["id"].split(":", 1)[0]
        if group != previous:
            entries.extend(["", f"## {group}", "", "| Entry point | Действие | Видимое наблюдение | Вход / подробности |", "| --- | --- | --- | --- |"])
            previous = group
        inputs = ", ".join(f"[{Path(p).name}](../{p})" for p in e["inputs"])
        guide = f"[{e['feature_id']}](ALL_FUNCTIONS_RU.md#{e['feature_id'].lower()})"
        cells = [e["id"], e["trigger"], e["expect"], inputs + "; " + guide]
        entries.append("| " + " | ".join(v.replace("|", "\\|").replace("\n", " ") for v in cells) + " |")
    return {"docs/ALL_FUNCTIONS_RU.md": "\n".join(lines).rstrip()+"\n",
            "docs/ENTRY_POINTS_RU.md": "\n".join(entries).rstrip()+"\n"}


def check(plugin_source=None, require_source=False, write_guides=False):
    data = read(ROOT / "suite-support/function_playbooks.json")
    entries = read(ROOT / "suite-support/entry_point_playbooks.json")
    result = validate(data, entries)
    if plugin_source:
        source = read(plugin_source / "marketplace/media/feature-coverage.json")
        actual = {f["id"]: f["source_capability"] for f in data["features"]}
        expected = {f["id"]: f["capability"] for f in source["features"]}
        if actual != expected:
            raise ValueError("Complete user-facing feature inventory drifted from plugin source")
        result["source"] = "62 source capabilities match"
    elif require_source:
        raise ValueError("Plugin source is required")
    else:
        result["source"] = "source comparison skipped (portable copy)"
    for relative, text in guides(data, entries).items():
        target = ROOT / relative
        if write_guides:
            temporary = target.with_name(target.name + ".tmp")
            temporary.write_text(text, encoding="utf-8", newline="\n")
            temporary.replace(target)
        elif not target.is_file() or target.read_text(encoding="utf-8") != text:
            raise ValueError(f"Guide drifted: {relative}; review data and use --write-guides")
    result.update(status="COMPLETE_PLAYBOOK_INPUTS_PASS", consumer_runs="NOT_RUN; see actual run records")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--plugin-source", type=Path)
    parser.add_argument("--require-source", action="store_true")
    parser.add_argument("--write-guides", action="store_true")
    args = parser.parse_args()
    try:
        print(json.dumps(check(args.plugin_source, args.require_source, args.write_guides)))
    except (ValueError, KeyError, TypeError) as error:
        parser.error(str(error))
