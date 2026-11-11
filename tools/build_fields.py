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
    {"id": "rcb", "name": "ResearchClaw Bench", "short": "RCB", "status": "live", "legend": "RCB 已上线", "legend_en": "RCB live"},
]
# English for the sheet's Chinese field names. Missing entries fall back to Chinese on the site.
EN_DOMAINS = {
    "医学": "Medicine", "生命": "Life sciences", "化学": "Chemistry", "材料": "Materials",
    "物理": "Physics", "天文": "Astronomy", "地球": "Earth science", "能源": "Energy",
    "信息": "Information", "神经科学": "Neuroscience", "数学": "Mathematics", "多领域综合": "Multi-domain",
}
EN_SUBFIELDS = {
    "肿瘤生物学": "Tumour biology", "免疫学与免疫治疗": "Immunology and immunotherapy",
    "RNA 生物学": "RNA biology", "遗传学与基因组学": "Genetics and genomics",
    "细胞生物学": "Cell biology", "理论与计算化学": "Theoretical and computational chemistry",
    "有机化学": "Organic chemistry", "物理化学": "Physical chemistry", "无机化学": "Inorganic chemistry",
    "分析化学": "Analytical chemistry", "材料计算与设计": "Materials computation and design",
    "高分子与有机功能材料": "Polymers and organic functional materials", "量子材料": "Quantum materials",
    "无机材料": "Inorganic materials", "能源材料": "Energy materials",
    "粒子物理与高能物理": "Particle and high-energy physics", "凝聚态物理": "Condensed matter physics",
    "光学与量子信息": "Optics and quantum information", "核物理": "Nuclear physics",
    "等离子体物理": "Plasma physics", "高能天体物理": "High-energy astrophysics", "宇宙学": "Cosmology",
    "星系与恒星": "Galaxies and stars", "太阳与空间物理": "Solar and space physics",
    "行星科学": "Planetary science", "大气科学与气候": "Atmospheric science and climate",
    "海洋科学": "Ocean science", "地质学与地球化学": "Geology and geochemistry",
    "冰冻圈科学": "Cryosphere science", "生态学": "Ecology", "电力系统": "Power systems",
    "电池与储能": "Batteries and storage", "太阳能与风能": "Solar and wind energy",
    "氢能": "Hydrogen energy", "核能": "Nuclear energy", "理论计算机科学": "Theoretical computer science",
    "人工智能": "Artificial intelligence", "计算机系统": "Computer systems",
    "软件工程": "Software engineering", "数据科学与数据库": "Data science and databases",
    "系统与环路神经科学": "Systems and circuits neuroscience",
    "分子与细胞神经科学": "Molecular and cellular neuroscience",
    "认知神经科学": "Cognitive neuroscience", "计算神经科学": "Computational neuroscience",
    "神经疾病": "Neurological disease", "代数与数论": "Algebra and number theory",
    "几何与拓扑": "Geometry and topology", "分析与微分方程": "Analysis and differential equations",
    "概率论与数理统计": "Probability and statistics",
    "计算数学与优化": "Computational mathematics and optimisation", "肿瘤学": "Oncology",
    "医学影像与智能诊断": "Medical imaging and intelligent diagnosis",
    "临床医学": "Clinical medicine", "心脑血管疾病": "Cardiovascular and cerebrovascular disease",
    "公共卫生与流行病学": "Public health and epidemiology", "专业知识工作": "Professional knowledge work",
    "芯片设计": "Chip design", "网络安全": "Cybersecurity", "生物医药研发": "Biomedical R&D",
    "科学工作流": "Scientific workflows",
}

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
            domains.append({"name": clean_domain(cells["A"]), "name_en": EN_DOMAINS.get(clean_domain(cells["A"]), ""), "subfields": [], "subfields_en": [], "topics": [], "counts": {"rcb": 0}})
        if not domains:
            continue
        if cells.get("B"):
            domains[-1]["subfields"].append(cells["B"])
            domains[-1]["subfields_en"].append(EN_SUBFIELDS.get(cells["B"].strip(), ""))

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
