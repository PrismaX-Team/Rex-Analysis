#!/usr/bin/env python3
"""Build content/1.0 leaderboard + runs from the official RCB-Home leaderboard snapshot.

Reads only paths listed in sources/content.lock.json. Ranking follows the official site:
mean over scored tasks, compared at one decimal, then by coverage, then raw mean.
Standalone LLMs (ResearchHarness) are ranked in their own group.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"

# Copied from the official site's app.js; these are presentation facts, not in the JSON.
COMMUNITY = {"EvoScientist (0.1.1)", "Qiushi Engine", "InnoClaw", "AutoSciRub", "EvoLab", "Ligase", "jiutian-DeepInsight"}
SOURCE_URLS = {
    "ARIS Codex": "https://github.com/wanshuiyin/auto-claude-code-research-in-sleep",
    "EvoScientist": "https://github.com/EvoScientist/EvoScientist",
    "Nanobot": "https://github.com/HKUDS/nanobot",
    "Open Science": "https://github.com/ai4s-research/open-science",
    "Qiushi Engine": "https://oxelra.com/",
    "InnoClaw": "https://github.com/SpectrAI-Initiative/InnoClaw",
    "AutoSciRub": "https://github.com/zjunlp/AutoSciRub",
    "EvoLab": "https://evo-lab.org/",
    "Ligase": "https://gradence.com.cn/products/wecode.html#biopharma",
}
HOME = "https://internscience.github.io/ResearchClawBench-Home/"
# Fields that must never reach content/ (architecture §7).
FORBIDDEN = ("checklist", "target_study", "paper.pdf", "tolerance")


def base_label(name: str) -> str:
    m = re.match(r"^(.*?) \([^()]+\)$", name)
    return m.group(1) if m else name


def slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def mean(values):
    return sum(values) / len(values) if values else None


def run_date(entries) -> str:
    # run_id carries a YYYYMMDD stamp; the latest one is the submission date.
    stamps = [m.group(1) for e in entries if (m := re.search(r"_(20\d{6})", e.get("run_id", "")))]
    if not stamps:
        return ""
    s = max(stamps)
    return f"{s[:4]}-{s[4:6]}-{s[6:]}"


def build_v1(src: Path) -> None:
    data = json.loads(src.read_text())
    tasks = sorted(data["tasks"])
    domains = list(dict.fromkeys(t.split("_")[0] for t in tasks))
    out_runs = CONTENT / "rcb" / "1.0" / "runs"

    rows = []
    for agent in data["agents"]:
        scores = {t: e for t, e in (data["scores"].get(agent) or {}).items() if isinstance(e, dict) and isinstance(e.get("score"), (int, float))}
        if not scores:
            continue
        values = [e["score"] for e in scores.values()]
        models = {e.get("model_display") or e.get("model") for e in scores.values()} - {None}
        harness = agent.startswith("ResearchHarness")
        model = next(iter(models)) if len(models) == 1 else ""
        system = model if harness else agent
        by_domain = {}
        for d in domains:
            dv = [scores[t]["score"] for t in tasks if t.startswith(f"{d}_") and t in scores]
            by_domain[d] = round(mean(dv), 2) if dv else None
        cost = [e["cost_usd"] for e in scores.values() if isinstance(e.get("cost_usd"), (int, float))]
        dur = [e["duration_seconds"] for e in scores.values() if isinstance(e.get("duration_seconds"), (int, float))]
        run_id = slug(agent)
        rows.append({
            "run_id": run_id,
            "group": "llm" if harness else "agent",
            "system": system,
            "model": "" if harness else model,
            "source": "community" if agent in COMMUNITY or base_label(agent) in COMMUNITY else "internal",
            "source_url": SOURCE_URLS.get(base_label(agent)) or SOURCE_URLS.get(agent) or "",
            "score": round(mean(values), 2),
            "task_count": len(values),
            "date": run_date(scores.values()),
            "cost_usd": round(mean(cost), 3) if cost else None,
            "duration_seconds": round(mean(dur)) if dur else None,
            "domains": by_domain,
            "new_count": sum(1 for v in values if v >= 50),
            "_raw": mean(values),
            "_agent": agent,
            "_scores": scores,
        })

    def key(r):
        return (-round(r["_raw"], 1), -r["task_count"], -r["_raw"], r["system"])

    ordered = []
    for group in ("llm", "agent"):
        part = sorted((r for r in rows if r["group"] == group), key=key)
        for i, r in enumerate(part, 1):
            r["rank"] = i
        ordered += part

    frontier = {}
    for t in tasks:
        best = max((r for r in rows if t in r["_scores"]), key=lambda r: r["_scores"][t]["score"], default=None)
        if best:
            frontier[t] = {"score": best["_scores"][t]["score"], "run_id": best["run_id"]}

    board = {
        "version": "1.0",
        "source": "InternScience/ResearchClawBench-Home data/leaderboard.json",
        "note": "均分取已评分题目的平均。大模型与智能体分开排名。",
        "domains": domains,
        # Models come first: the home carousel, the overall table and the leaderboard's default tab all read groups[0].
        "groups": [
            {"id": "llm", "label": "大模型", "en": "Models", "note": "所有模型在同一套 ResearchHarness 流程下运行，只比模型本身。"},
            {"id": "agent", "label": "智能体", "en": "Agents"},
        ],
        "frontier": frontier,
        "rows": [{k: v for k, v in r.items() if not k.startswith("_")} for r in ordered],
    }

    runs = {}
    for r in ordered:
        runs[r["run_id"]] = {
            "run_id": r["run_id"],
            "version": "1.0",
            "system": r["system"],
            "model": r["model"],
            "group": r["group"],
            "source": r["source"],
            "source_url": r["source_url"],
            "date": r["date"],
            "score": r["score"],
            "task_count": r["task_count"],
            "cost_usd": r["cost_usd"],
            "duration_seconds": r["duration_seconds"],
            "report_note": "分题报告、代码和评分理由仍在原项目站。",
            "report_url": HOME,
            "tasks": [
                {
                    "task_id": t,
                    "score": r["_scores"][t]["score"] if t in r["_scores"] else None,
                    "cost_usd": r["_scores"].get(t, {}).get("cost_usd"),
                    "duration_seconds": r["_scores"].get(t, {}).get("duration_seconds"),
                }
                for t in tasks
            ],
        }

    blob = json.dumps([board, runs], ensure_ascii=False).lower()
    bad = [w for w in FORBIDDEN if w in blob]
    if bad:
        sys.exit(f"refusing to write: forbidden fields {bad}")

    out_runs.mkdir(parents=True, exist_ok=True)
    for old in out_runs.glob("*.json"):
        old.unlink()
    for run_id, run in runs.items():
        (out_runs / f"{run_id}.json").write_text(json.dumps(run, ensure_ascii=False, indent=2) + "\n")
    (CONTENT / "rcb" / "1.0" / "leaderboard.json").write_text(json.dumps(board, ensure_ascii=False, indent=2) + "\n")
    print(f"1.0: {len(ordered)} rows, {len(runs)} runs")


def spread(values: list) -> dict:
    """Mean and population std, rounded like the official pass@5 file."""
    if not values:
        return {"mean": None, "std": None}
    m = sum(values) / len(values)
    return {"mean": round(m, 2), "std": round((sum((v - m) ** 2 for v in values) / len(values)) ** 0.5, 2)}


def build_v1_pass5(src: Path) -> None:
    """Pass@5: five attempts per task, best attempt counts, failed or unscored attempts are 0.

    Ranked the same way as pass@1 (mean at one decimal, then raw mean). Every task is counted,
    so coverage never differs between rows here.
    """
    data = json.loads(src.read_text())
    tasks = sorted(data["tasks"])
    domains = list(dict.fromkeys(t.split("_")[0] for t in tasks))

    rows = []
    for agent in data["agents"]:
        scores = data["scores"].get(agent) or {}
        best = {t: float((scores.get(t) or {}).get("score") or 0) for t in tasks}
        runs_of = {t: [v for v in ((scores.get(t) or {}).get("runs") or []) if isinstance(v, (int, float))] for t in tasks}
        attempts = [v for t in tasks for v in runs_of[t]]
        models = {e.get("model_display") or e.get("model") for e in scores.values()} - {None}
        mean_best = sum(best.values()) / len(tasks)
        att_mean = sum(attempts) / len(attempts) if attempts else None
        att_std = (sum((v - att_mean) ** 2 for v in attempts) / len(attempts)) ** 0.5 if attempts else None
        rows.append({
            "run_id": slug(agent),
            "group": "llm" if agent.startswith("ResearchHarness") else "agent",
            "system": next(iter(models)) if len(models) == 1 and agent.startswith("ResearchHarness") else agent,
            "model": "",
            "score": round(mean_best, 2),
            "attempt_mean": round(att_mean, 2) if att_mean is not None else None,
            "attempt_std": round(att_std, 2) if att_std is not None else None,
            "task_count": len(tasks),
            "domains": {d: round(sum(best[t] for t in tasks if t.startswith(f"{d}_")) / sum(1 for t in tasks if t.startswith(f"{d}_")), 2) for d in domains},
            # Same convention as the official site: mean ± population std over every attempt in the domain.
            "domain_spread": {d: spread([v for t in tasks if t.startswith(f"{d}_") for v in runs_of[t]]) for d in domains},
            "new_count": sum(1 for t in tasks if best[t] >= 50),
            "tasks": [
                {
                    "task_id": t,
                    "score": best[t],
                    "runs": runs_of[t],
                    "attempts": (scores.get(t) or {}).get("attempts", len(runs_of[t])),
                    "scored_runs": (scores.get(t) or {}).get("scored_runs", len(runs_of[t])),
                    **spread(runs_of[t]),
                    "min": min(runs_of[t]) if runs_of[t] else None,
                    "max": max(runs_of[t]) if runs_of[t] else None,
                }
                for t in tasks
            ],
            "_raw": mean_best,
        })

    rows.sort(key=lambda r: (-round(r["_raw"], 1), -r["_raw"], r["system"]))
    for i, r in enumerate(rows, 1):
        r["rank"] = i
        del r["_raw"]

    board = {
        "version": "1.0",
        "pass_mode": "pass5",
        "source": "InternScience/ResearchClawBench-Home data/pass5_leaderboard.json",
        "generated_at": data.get("generated_at", ""),
        "note": "每题跑 5 次取最高分；失败或未评分的尝试按 0 计。只覆盖部分独立大模型。",
        "domains": domains,
        "frontier": {
            t: (lambda top: {"score": top["tasks"][i]["score"], "run_id": top["run_id"]})(max(rows, key=lambda r: r["tasks"][i]["score"]))
            for i, t in enumerate(tasks)
        },
        "rows": rows,
    }
    blob = json.dumps(board, ensure_ascii=False).lower()
    bad = [w for w in FORBIDDEN if w in blob]
    if bad:
        sys.exit(f"refusing to write pass5: forbidden fields {bad}")
    (CONTENT / "rcb" / "1.0" / "pass5.json").write_text(json.dumps(board, ensure_ascii=False, indent=2) + "\n")
    print(f"1.0 pass@5: {len(rows)} rows")


def main() -> None:
    lock = json.loads((ROOT / "sources" / "content.lock.json").read_text())
    build_v1(ROOT / lock["rcb"]["1.0"]["leaderboard"]["path"])
    if "pass5" in lock["rcb"]["1.0"]:
        build_v1_pass5(ROOT / lock["rcb"]["1.0"]["pass5"]["path"])


if __name__ == "__main__":
    main()
