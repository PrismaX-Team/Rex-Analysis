#!/usr/bin/env python3
"""Build content/afe/1.0/ from the AFE workspace.

Reads only the public side of each Harbor task package:
  task.toml                 metadata
  instruction.md            the task statement the agent sees
  environment/data/*        file names and sizes (not contents)
  environment/task_info.json  data descriptions (Earth)

Never reads tests/, solution/, authoring/, judge results, sources/*/target_study or any job artifact.
The output is also scanned for words that would only appear if private material leaked; any hit
aborts the whole build and nothing is written.

Usage: python3 tools/build_afe.py [path to the AFE workspace]   (or set AFE_WORKSPACE)
"""
from __future__ import annotations

import json
import re
import shutil
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "content" / "afe" / "1.0"

# Site-facing domain names and colours. Track = which AFE 1.0 line the domain belongs to.
DOMAINS = {
    "chem": {"label": "计算化学", "en": "Computational Chemistry", "field": "化学", "color": "#0e9f86", "color_dark": "#19b597"},
    "earth": {"label": "地球科学", "en": "Earth Science", "field": "地球", "color": "#9a6b34", "color_dark": "#b87e3a"},
}

# Words that only appear in private material. Statements are checked separately below.
FORBIDDEN = ("target_study", "checklist", "paper.pdf", "rubric", "reference_quotes", "judge_code", "test_outputs", "solve.sh")

# Short Chinese titles: the source statements are long English questions.
LABELS = {
    "chem_duration_01": "酯交换中活性亲核体的动力学可辨识性",
    "chem_duration_02": "吡啶催化碳酸酯生成的添加剂缔合与物种分布",
    "chem_duration_03": "乙酸酯选择性断裂的局部描述符与反离子对照",
    "chem_duration_04": "锌增强肟根断裂芳基乙酸酯的来源",
    "chem_duration_05": "硼上溴换苯基为何减慢芳基硅烷–硼交换",
    "chem_duration_06": "Salophen 有机催化剂活化环氧的立体化学后果",
    "chem_duration_07": "钯催化 2-甲基苯甲酸内酯化的位点选择性",
    "chem_duration_08": "钯催化脱羧菲啶环化中添加剂效应的机理",
    "chem_duration_09": "双膦配体控制硅氢化选择性翻转的机理",
    "chem_duration_10": "N-磺酰亚胺在敏化光烯胺化–环加成中的分化",
    "earthcosci_0373f23f8fcf1abc": "格陵兰冰芯中粉尘来源的冰期–间冰期变化",
    "earthcosci_0808f6d46726249d": "北大西洋沉积芯中海洋指标与碎屑碳酸盐的同步性",
    "earthcosci_08ad2b8d9ac5aa31": "草地样方中物种丰富度与地上生物量的关系",
    "earthcosci_4e1528ed76e20041": "雨量站网中异常降雨与观测错误的区分",
    "earthcosci_631afea31ef42598": "冻土融化后地表的氧化亚氮交换差异",
    "earthcosci_917270d2bd6b0cc4": "定年不确定性对石笋氧同位素记录的影响",
    "earthcosci_b6f09f90fa568589": "华北克拉通南缘火山–深成岩组合的地化与年代关系",
    "earthcosci_dbee00e3ed8d67d2": "大型火山喷发后热带太平洋冬季变率的变化",
    "earthcosci_dfb2f8ce0264f8fc": "温度、盐度与压力对海水碳酸盐体系的影响",
    "earthcosci_e1e0f2682bc3c4cf": "扰动后生态恢复的累积亏缺",
}


def human_size(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024
    return f"{n} B"


def public_statement(domain: str, text: str) -> str:
    """The statement the agent reads, minus the harness boilerplate around it."""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S).strip()
    if domain == "chem":
        # Drop the "# Workspace and delivery" runtime block; keep the research question onwards.
        parts = re.split(r"^# (?!Workspace)", text, maxsplit=1, flags=re.M)
        text = "# " + parts[1] if len(parts) == 2 else text
        # The trailing time-budget line is runtime, shown in the side card instead.
        text = re.sub(r"\n+You have \d+ seconds to complete this task\..*$", "", text.strip(), flags=re.S)
    else:
        # Earth: the opening paragraph is the question; Workspace/Deliverables follow.
        m = re.search(r"^# [^\n]*\n\n(.+?)\n\n## Workspace", text, flags=re.S | re.M)
        question = m.group(1).strip() if m else text
        deliver = text.split("## Deliverables", 1)[1] if "## Deliverables" in text else ""
        deliver = re.split(r"\n\s*The task budget is", deliver)[0].strip()
        # Container paths are runtime detail; show the relative layout the site uses elsewhere.
        deliver = re.sub(r"`?/app/", "`", deliver).replace("``", "`")
        deliver = re.sub(r"\s*Work in /app and leave the final report in place before you stop\.", "", deliver)
        # Unwrap hard-wrapped prose: the site's markdown treats each line as a paragraph.
        deliver = re.sub(r"(?<=[^\n])\n(?=[^\n\-#])", " ", deliver)
        text = f"## Research question\n\n{question}\n\n## Deliverables\n\n{deliver}".strip()
    return text.strip()


def question_of(domain: str, text: str) -> str:
    if domain == "chem":
        m = re.search(r"## 1\. Research problem\n\n(.+?)\n", text, flags=re.S)
    else:
        m = re.search(r"^# [^\n]*\n\n(.+?)\n", text, flags=re.S | re.M)
    q = re.sub(r"\s+", " ", m.group(1)).strip() if m else ""
    return q


def summary_of(question: str, limit: int = 220) -> str:
    if len(question) <= limit:
        return question
    cut = question[:limit].rsplit(" ", 1)[0]
    return cut.rstrip(",;:") + "…"


def data_files(task_dir: Path, domain: str) -> list[dict]:
    data_dir = task_dir / "environment" / "data"
    described = {}
    info = task_dir / "environment" / "task_info.json"
    if info.is_file():
        for item in json.loads(info.read_text()).get("data", []):
            described[Path(item["path"]).name] = item.get("description", "").strip()
    out = []
    for f in sorted(p for p in data_dir.iterdir() if p.is_file()):
        desc = described.get(f.name, "")
        if not desc and domain == "chem":
            desc = {
                "chemical_system.json": "分子身份、实验体系和声明的反应表示。",
                "observations.json": "每条观测及其条件、局限和必需 / 背景标记。",
            }.get(f.name, "")
        out.append({"name": f.name, "path": f"data/{f.name}", "size": human_size(f.stat().st_size), "description": desc})
    return out


def main() -> None:
    import os
    given = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("AFE_WORKSPACE", "")
    if not given:
        sys.exit("give the AFE workspace path as an argument or in AFE_WORKSPACE")
    src = Path(given).resolve()
    manifest = [json.loads(l) for l in (src / "manifests" / "tasks.jsonl").read_text().splitlines() if l.strip()]

    tasks = []
    for entry in manifest:
        domain = entry["domain"]
        if domain not in DOMAINS:
            sys.exit(f"unknown AFE domain {domain}; add it to DOMAINS")
        task_dir = src / entry["path"]
        meta = tomllib.loads((task_dir / "task.toml").read_text())
        raw = (task_dir / "instruction.md").read_text()
        statement = public_statement(domain, raw)
        question = question_of(domain, raw)
        heading = re.search(r"^# (?!Workspace)(?!Earth Co-Scientist)(.+)$", raw, flags=re.M)
        # task.toml's description and keywords are one placeholder across all Earth tasks: not used.
        first_sentence = re.split(r"(?<=[.?!])\s", question, maxsplit=1)[0]
        tasks.append({
            "task_id": entry["task_id"],
            "domain": domain,
            "domain_label": DOMAINS[domain]["label"],
            "label": LABELS.get(entry["task_id"], ""),
            "title": heading.group(1).strip() if heading else first_sentence,
            "summary": summary_of(question),
            "statement": statement,
            "data": data_files(task_dir, domain),
        })

    by_domain = {}
    for t in tasks:
        by_domain.setdefault(t["domain"], 0)
        by_domain[t["domain"]] += 1
    doc = {
        "version": "1.0",
        "source": "AFE task packages (public side only)",
        "domains": [{"id": k, **v, "count": by_domain.get(k, 0)} for k, v in DOMAINS.items() if by_domain.get(k)],
        "tasks": tasks,
    }

    blob = json.dumps(doc, ensure_ascii=False).lower()
    bad = [w for w in FORBIDDEN if w in blob]
    if bad:
        sys.exit(f"refusing to write AFE content: private markers found {bad}")
    missing = [t["task_id"] for t in tasks if not t["label"]]
    if missing:
        sys.exit(f"missing Chinese short titles for {missing}; add them to LABELS")

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "tasks.json").write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n")
    print(f"AFE 1.0: {len(tasks)} tasks", by_domain)


if __name__ == "__main__":
    main()
