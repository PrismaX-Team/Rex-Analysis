#!/usr/bin/env python3
"""Build content/fields.json: the field coverage of every dataset on the site.

Datasets counted now:
- RCB: live tasks, read from content/rcb/1.0/tasks.json and content/rcb/1.0/atlas.json.
- AFE: live tasks from content/afe/1.0/tasks.json (run tools/build_afe.py first), plus the
  directions still planned in the version sheet. A direction that already went live is not counted twice.

The sheet also holds owners, partners, funding sources, progress and in-house 2.0 plans. Those stay
out: only domain names, sub-field names and the number of planned task directions are written.

To add a dataset: add it to DATASETS, fill its count in each domain's "counts", and the page follows.

Usage: python3 tools/build_fields.py <path to _AgentFrontierExam版本管理.xlsx>
"""
from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
CONTENT = Path(__file__).resolve().parent.parent / "content"
OUT = CONTENT / "fields.json"
HEADER_ROW = 4

DATASETS = [
    {"id": "rcb", "name": "ResearchClaw Bench", "short": "RCB", "status": "live", "legend": "RCB 已上线"},
    {"id": "afe", "name": "AgentFrontierExam 1.0", "short": "AFE", "status": "live", "legend": "AFE 已上线"},
    {"id": "afe_plan", "name": "AgentFrontierExam 规划", "short": "AFE 规划", "status": "planned", "legend": "AFE 规划中"},
]
# Sheet directions whose tasks are already in AFE 1.0.
AFE_LIVE_DIRECTIONS = {"反应机理", "大气、海洋、地质、极地"}
# RCB domain id -> the domain name used by the version sheet.
RCB_DOMAINS = {
    "Astronomy": "天文", "Chemistry": "化学", "Earth": "地球", "Energy": "能源", "Information": "信息",
    "Life": "生命", "Material": "材料", "Math": "数学", "Neuroscience": "神经科学", "Physics": "物理",
}


def read_rows(path: str) -> dict[int, dict[str, str]]:
    with zipfile.ZipFile(path) as z:
        strings = ["".join(t.text or "" for t in si.iter(f"{NS}t")) for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall(f"{NS}si")]
        sheet = ET.fromstring(z.read("xl/worksheets/sheet1.xml"))
    rows = {}
    for row in sheet.iter(f"{NS}row"):
        cells = {}
        for c in row.findall(f"{NS}c"):
            v = c.find(f"{NS}v")
            if v is None or v.text is None:
                continue
            text = strings[int(v.text)] if c.get("t") == "s" else v.text
            cells[re.match(r"[A-Z]+", c.get("r")).group()] = text.strip()
        rows[int(row.get("r"))] = cells
    return rows


def clean_domain(name: str) -> str:
    return re.split(r"[*（(]", name)[0].strip()


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    rows = read_rows(sys.argv[1])
    header = rows[HEADER_ROW]
    if header.get("A") != "科学领域" or not header.get("B", "").startswith("二级领域") or header.get("C") != "任务方向":
        sys.exit(f"unexpected header row: {header}")

    domains: list[dict] = []
    for n in sorted(k for k in rows if k > HEADER_ROW):
        cells = rows[n]
        if cells.get("A"):
            domains.append({"name": clean_domain(cells["A"]), "subfields": [], "topics": [], "counts": {"rcb": 0, "afe": 0, "afe_plan": 0}})
        if not domains:
            continue
        if cells.get("B"):
            domains[-1]["subfields"].append(cells["B"])
        # "-" marks a sub-field with no planned direction yet; a merged sub-field cell can carry several.
        if cells.get("C") and cells["C"] != "-" and cells["C"] not in AFE_LIVE_DIRECTIONS:
            domains[-1]["counts"]["afe_plan"] += 1

    by_name = {d["name"]: d for d in domains}
    labels = json.loads((CONTENT / "rcb" / "1.0" / "atlas.json").read_text())["labels"]
    for task in json.loads((CONTENT / "rcb" / "1.0" / "tasks.json").read_text())["tasks"]:
        target = by_name.get(RCB_DOMAINS.get(task["domain"], ""))
        if target is None:
            sys.exit(f"RCB domain {task['domain']} has no match in the sheet; update RCB_DOMAINS")
        target["counts"]["rcb"] += 1
        target["topics"].append(labels.get(task["task_id"], task["task_id"]))

    afe = json.loads((CONTENT / "afe" / "1.0" / "tasks.json").read_text())
    afe_field = {d["id"]: d["field"] for d in afe["domains"]}
    for task in afe["tasks"]:
        target = by_name.get(afe_field.get(task["domain"], ""))
        if target is None:
            sys.exit(f"AFE domain {task['domain']} has no match in the sheet; update DOMAINS in build_afe.py")
        target["counts"]["afe"] += 1
        target["topics"].append(task["label"])

    for d in domains:
        d["total"] = sum(d["counts"].values())

    doc = {
        "note": "由 tools/build_fields.py 生成。已上线部分来自公开任务；规划部分来自版本管理表，只含领域名、二级领域名和方向数。",
        "updated": "2026-11",
        "datasets": [{**ds, "total": sum(d["counts"][ds["id"]] for d in domains)} for ds in DATASETS],
        "domains": sorted(domains, key=lambda d: -d["total"]),
    }
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n")
    print(f"{len(domains)} domains, {sum(len(d['subfields']) for d in domains)} sub-fields", {ds["short"]: ds["total"] for ds in doc["datasets"]})
    for d in doc["domains"]:
        print(f"  {d['name']}: {d['counts']} total {d['total']}")


if __name__ == "__main__":
    main()
