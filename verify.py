#!/usr/bin/env python3
"""Recompute the paper's systematic-mapping numbers from the public tables.

    python verify.py
"""
from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
failures: list[str] = []


def read_csv(name: str) -> list[dict]:
    with (ROOT / name).open(encoding="utf-8-sig", newline="", errors="replace") as fh:
        return list(csv.DictReader(fh))


def check(label: str, actual, expected) -> None:
    if actual != expected:
        failures.append(f"{label}: got {actual!r}, expected {expected!r}")
    else:
        print(f"PASS  {label}: {actual}")


extraction = read_csv("extraction.csv")
screening = read_csv("screening.csv")
funnel = json.loads((ROOT / "search_funnel.json").read_text(encoding="utf-8"))
dedup = json.loads((ROOT / "dedup_report.json").read_text(encoding="utf-8"))

# ---------------------------------------------------------------- extraction
check("extraction rows", len(extraction), 88)
check("database rows", sum(1 for r in extraction if r["arm"] == "database"), 79)
check("snowball rows", sum(1 for r in extraction if r["arm"] == "snowball"), 9)
check("full extraction rows", sum(1 for r in extraction if r["extraction_status"] == "full"), 79)
check("targeted extraction rows", sum(1 for r in extraction if r["extraction_status"] == "targeted"), 9)

# ---------------------------------------------------------------- cost extraction (separate table)
cost = read_csv("cost_extraction.csv")
check("cost rows", len(cost), 88)
check("cost unique ids", len({r["record_id"] for r in cost}), 88)
check("cost ids match extraction", {r["record_id"] for r in cost} == {r["record_id"] for r in extraction}, True)
cost_fields = ["tokens", "monetary_cost", "wall_clock", "agent_steps", "human_effort", "hardware"]
expected_cost = {"tokens": 23, "monetary_cost": 19, "wall_clock": 27,
                 "agent_steps": 31, "human_effort": 18, "hardware": 32}
for f in cost_fields:
    check(f"cost {f}", sum(int(r[f]) for r in cost), expected_cost[f])
check("cost no signal", sum(1 for r in cost if not any(int(r[f]) for f in cost_fields)), 22)
check("cost money and effort", sum(1 for r in cost if int(r["monetary_cost"]) and int(r["human_effort"])), 5)
check("cost binary values", all(int(r[f]) in (0, 1) for r in cost for f in cost_fields), True)

# complexity constructs
constructs = []
for r in extraction:
    items = json.loads(r["complexity_constructs"])
    check(f"{r['record_id']} construct count", int(r["n_complexity_constructs"]), len(items))
    for item in items:
        check(f"{r['record_id']} construct keys", set(item), {"class", "nature", "construct"})
    constructs.extend(items)

check("construct rows", len(constructs), 312)
check("distinct constructs", len({c["construct"].strip() for c in constructs}), 312)
check("ordinal constructs", sum(1 for c in constructs if c["class"] == "ordinal_label"), 106)
check("reliability constructs", sum(1 for c in constructs if "reliab" in c["construct"].lower()), 2)
check("empty constructs", sum(1 for r in extraction for item in json.loads(r["complexity_constructs"])
                           if not item["construct"].strip()), 0)
check("papers with zero constructs", sum(1 for r in extraction if int(r["n_complexity_constructs"]) == 0), 16)

# database-arm distributions
db = [r for r in extraction if r["arm"] == "database"]
check("task distribution", dict(Counter(r["task"] for r in db)),
      {"migration": 45, "breaking_change": 12, "other": 6, "vuln_driven_update": 5,
       "upgrade": 5, "resolution": 4, "conflict_repair": 2})
check("study-type distribution", dict(Counter(r["study_type"] for r in db)),
      {"tool": 33, "benchmark": 20, "empirical": 19, "mixed": 6, "industry": 1})

# ---------------------------------------------------------------- screening
check("screening rows", len(screening), 2208)
ta = [r for r in screening if r["stage"] == "title_abstract"]
ft = [r for r in screening if r["stage"] == "fulltext"]
sb = [r for r in screening if r["stage"] == "snowball_fulltext"]
check("title/abstract rows", len(ta), 2112)
check("full-text rows", len(ft), 85)
check("snowball rows", len(sb), 11)

check("LLM includes", sum(1 for r in ta if r["llm_decision"] == "include"), 83)
check("LLM excludes", sum(1 for r in ta if r["llm_decision"] == "exclude"), 1617)
check("LLM uncertain", sum(1 for r in ta if r["llm_decision"] == "uncertain"), 412)
check("title/abstract excluded", sum(1 for r in ta if r["llm_decision"] in ("exclude", "uncertain")), 2029)
check("R1-final title/abstract includes", sum(1 for r in ta if r["final_decision"] == "include"), 85)
check("full-text includes", sum(1 for r in ft if r["final_decision"] == "include"), 79)
check("full-text excludes", sum(1 for r in ft if r["final_decision"] == "exclude"), 4)
check("full-text without verdict", sum(1 for r in ft if not r["final_decision"]), 2)
check("title/abstract unique ids", len({r["record_id"] for r in ta}), len(ta))
check("full-text unique ids", len({r["record_id"] for r in ft}), len(ft))
check("snowball unique ids", len({r["record_id"] for r in sb}), len(sb))
check("extraction unique ids", len({r["record_id"] for r in extraction}), 88)
check("TA r1 excludes with final include", sum(1 for r in ta if r["r1_decision"] == "exclude" and r["final_decision"] == "include"), 0)
check("fulltext includes equal database extraction",
      {r["record_id"] for r in ft if r["final_decision"] == "include"} ==
      {r["record_id"] for r in extraction if r["arm"] == "database"}, True)
check("snowball includes", sum(1 for r in sb if r["final_decision"] == "include"), 9)
check("snowball excludes", sum(1 for r in sb if r["final_decision"] == "exclude"), 2)
check("snowball excluded ids", sorted(r["record_id"] for r in sb if r["final_decision"] == "exclude"),
      ["C0067", "C0187"])

# ---------------------------------------------------------------- funnel
check("identified", dedup["records_total"], 2408)
check("duplicates", dedup["duplicates_removed"], 296)
check("unique", dedup["unique_total"], 2112)
check("per-source sum", sum(dedup["per_source_records"].values()), 2408)
check("funnel identified", funnel["records_total"], 2408)
check("funnel unique", funnel["unique_total"], 2112)
check("funnel screened", funnel["title_abstract"]["screened"], 2112)
check("funnel LLM include", funnel["title_abstract"]["llm_include"], 83)
check("funnel R1 include", funnel["title_abstract"]["r1_final_include"], 85)
check("funnel fulltext rows", funnel["fulltext"]["rows"], 85)
check("funnel database included", funnel["database_included"], 79)
check("funnel total included", funnel["total_included"], 88)
check("snowball identified", funnel["snowball"]["identified"], 687)
check("snowball new since 2023", funnel["snowball"]["new_since_2023"], 286)
check("snowball with abstract", funnel["snowball"]["with_abstract"], 250)

if failures:
    print("\nFAILURES:")
    for f in failures:
        print("  -", f)
    sys.exit(1)
print("\nAll checks passed.")
