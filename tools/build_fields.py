#!/usr/bin/env python3
"""Build content/fields.json: the field coverage of every dataset on the site.

Datasets counted now:
- RCB: live tasks, read from content/rcb/1.0/tasks.json and content/rcb/1.0/atlas.json.
- AFE: only the domain taxonomy from the version sheet (domain names and sub-field names). AFE task
  content is not public, so no task titles or counts are exported.

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
]
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
            domains.append({"name": clean_domain(cells["A"]), "subfields": [], "topics": [], "counts": {"rcb": 0}})
        if not domains:
            continue
        if cells.get("B"):
            domains[-1]["subfields"].append(cells["B"])

    by_name = {d["name"]: d for d in domains}
    labels = json.loads((CONTENT / "rcb" / "1.0" / "atlas.json").read_text())["labels"]
    for task in json.loads((CONTENT / "rcb" / "1.0" / "tasks.json").read_text())["tasks"]:
        target = by_name.get(RCB_DOMAINS.get(task["domain"], ""))
        if target is None:
            sys.exit(f"RCB domain {task['domain']} has no match in the sheet; update RCB_DOMAINS")
        target["counts"]["rcb"] += 1
        target["topics"].append(labels.get(task["task_id"], task["task_id"]))

    for d in domains:
        d["total"] = sum(d["counts"].values())
        # The sheet defines the taxonomy; domains without a public task keep their sub-field list.

    doc = {
        "note": "由 tools/build_fields.py 生成。任务数来自 RCB 公开任务；领域和二级领域名来自 AFE 版本管理表，不含任何 AFE 题目。",
        "updated": "2026-11",
        "datasets": [{**ds, "total": sum(d["counts"][ds["id"]] for d in domains)} for ds in DATASETS],
        "domains": sorted(domains, key=lambda d: -d["total"]),  # stable: ties keep sheet order
    }
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n")
    print(f"{len(domains)} domains, {sum(len(d['subfields']) for d in domains)} sub-fields", {ds["short"]: ds["total"] for ds in doc["datasets"]})
    for d in doc["domains"]:
        print(f"  {d['name']}: {d['counts']} total {d['total']}")


if __name__ == "__main__":
    main()
