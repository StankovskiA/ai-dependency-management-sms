# Search queries

# Query Pack v0.5 (CANONICAL, wildcarded) — ready to paste

Window: **2023-01-01 → search date**. Language: English.
Validated against 35 seeds: **12/14** in-scope recalled; **0/8** non-AI dependency papers;
1 polysemy false positive (LLM supply chain).

---

## Scopus, Web of Science, ACM DL, SpringerLink, ScienceDirect

### Block A — AI / LLM / agentic

```
("large language model*" OR LLM* OR "generative AI" OR GenAI OR "foundation model*" OR ChatGPT OR "GPT-3*" OR "GPT-4*" OR Codex OR "GitHub Copilot" OR "AI agent*" OR "LLM agent*" OR "LLM-based agent*" OR agentic OR "multi-agent" OR multiagent OR "autonomous agent*" OR "coding agent*" OR "code agent*" OR "AI code generation")
```

### Block B — dependency management

```
("dependency management" OR "dependency resolution" OR "dependency conflict*" OR "version conflict*" OR "version resolution" OR "package management" OR "package manager*" OR "transitive dependenc*" OR "lock file*" OR lockfile* OR "dependency upgrad*" OR "dependency updat*" OR "dependency migration" OR "library upgrad*" OR "library migration" OR "library evolution" OR "library version*" OR "version incompatib*" OR "incompatible dependenc*" OR "version-aware" OR "version-controllable" OR "version-conditioned" OR "API migration" OR "API updat*" OR "API chang*" OR "deprecated API*" OR "API deprecat*" OR "breaking change*" OR "dependency breaking change*" OR "dependency-breaking change*" OR "code migration" OR "codebase migration" OR "project migration" OR "version migration" OR "vulnerable dependenc*" OR "library vulnerabilit*" OR "dependency vulnerabilit*" OR "vulnerability remediation" OR "vulnerability mitigation" OR "dependency remediation")
```

**Query = A AND B.**

Per-database wrappers:

- **Scopus**: `TITLE-ABS-KEY( A AND B ) AND PUBYEAR > 2022 AND ( LIMIT-TO ( LANGUAGE , "English" ) )`
- **Web of Science**: `TS=( A AND B )` → refine Years 2023–2026; English; Article/Proceedings Paper
- **ACM DL**: field = **Any Field**, query `(A) AND (B)` — or the explicit union `([Title: A] OR [Abstract: A] OR [Keyword: A]) AND ([Title: B] OR [Abstract: B] OR [Keyword: B])`
- **SpringerLink**: `(A) AND (B)` → 2023–2026, English, Computer Science
- **ScienceDirect**: `(A) AND (B)` → if rejected for complexity, split Block A in halves and merge

---

## IEEE Xplore (SPECIAL: two compact queries, then merge)

> IEEE caps wildcards at **10 per query** **and** rejects long Boolean strings ("use fewer
> keywords"). Run **both** queries below and merge the exports. Each uses ≤10 wildcards.

### IEEE shared Block A (10 concepts, 6 wildcards)
```
("large language model*" OR LLM* OR "generative AI" OR "foundation model*" OR ChatGPT OR "AI agent*" OR "LLM agent*" OR agentic OR "multi-agent" OR "coding agent*")
```

### IEEE Query 1 — core tasks (no field prefix — searches all metadata)
```
("large language model*" OR LLM* OR "generative AI" OR "foundation model*" OR ChatGPT OR "AI agent*" OR "LLM agent*" OR agentic OR "multi-agent" OR "coding agent*") AND ("dependency management" OR "dependency resolution" OR "dependency upgrad*" OR "dependency updat*" OR "dependency conflict" OR "version conflict" OR "package manager" OR "library migration" OR "breaking change*" OR "deprecated API*")
```
*(wildcards: 6 + 4 = **10**)*

### IEEE Query 2 — recall extension (no field prefix)
```
("large language model*" OR LLM* OR "generative AI" OR "foundation model*" OR ChatGPT OR "AI agent*" OR "LLM agent*" OR agentic OR "multi-agent" OR "coding agent*") AND ("API update" OR "API change" OR "API deprecation" OR "version incompatibility" OR "incompatible dependency" OR "library evolution" OR "library version" OR "vulnerable dependency" OR "vulnerability remediation" OR "dependency remediation" OR "code migration" OR "dependency breaking change" OR "transitive dependency" OR "lock file" OR "version resolution" OR "dependency vulnerability" OR "dependency migration" OR "library upgrade")
```
*(wildcards: 6 + 0 = **6**)*

Save as `ieee_v0.5_run1_<date>.ris` and `ieee_v0.5_run2_<date>.ris`; the dedup script merges them.

> If IEEE still returns zero, the field code is the suspect — use the **prefix-free** forms in
> `queries/v0.5_queries.md`, or drop to the minimal query there.

---

## arXiv

> **UI:** set the field to **All fields**, not *Abstract* (an abstract-only AND of large OR groups
> returns zero). **API:** no wildcard (`*`) support — use the explicit expansion in `v0.4_queries.md`.
> The pipeline can also fetch arXiv directly and write it to `search/raw/` as a canonical CSV.

---

## Runbook — fill in on execution

| Source | Date run | Query ver. | Hits | Exported to | Notes |
|---|---|---|---|---|---|
| Scopus | | v0.5 | | | |
| Web of Science | | v0.5 | | | |
| IEEE Xplore | | v0.5 Q1+Q2 | | | two exports to merge |
| ACM DL | | v0.5 | | | |
| SpringerLink | | v0.5 | 813 | | Keywords field only; Boolean OK |
| ScienceDirect | | v0.5 | | | |
| arXiv | | v0.4 explicit | | auto | ~1,300 |
| OpenAlex | | v0.5 | | auto | not a primary source |

---

## Notes for the paper

- Present the string as a **two-row facet table** (A: intervention; B: task) with the seed-recall
  validation, not as a bare block of text.
- Wildcards remove singular/plural redundancy (a prior-rejection complaint).
- IEEE uses a reduced two-query form due to its engine limits; document this as a
  per-database adaptation (prior rejection asked for exactly this transparency).

---

# Query Pack v0.4 (FINAL candidate) — ready to paste

Window: **2023-01-01 → search date**. Language: English.
Validated: recalls **12/14** in-scope seeds; **0/8** non-AI dependency papers; 1 polysemy false positive.
Supersedes v0.3 (drops polysemy magnets and broad agent words; seed recall unchanged).

---

## Block A — AI / LLM / agentic

```
("large language model" OR "large language models" OR LLM OR LLMs OR "generative AI" OR GenAI OR "foundation model" OR "foundation models" OR ChatGPT OR "GPT-3" OR "GPT-4" OR "GPT-4o" OR Codex OR "GitHub Copilot" OR "AI agent" OR "AI agents" OR "LLM agent" OR "LLM agents" OR "LLM-based agent" OR "LLM-based agents" OR agentic OR "multi-agent" OR multiagent OR "autonomous agent" OR "autonomous agents" OR "coding agent" OR "coding agents" OR "code agent" OR "code agents" OR "AI code generation")
```

## Block B — dependency management

```
("dependency management" OR "dependency resolution" OR "dependency conflict" OR "dependency conflicts" OR "version conflict" OR "version conflicts" OR "version resolution" OR "package management" OR "package manager" OR "package managers" OR "transitive dependency" OR "transitive dependencies" OR "lock file" OR "lock files" OR lockfile OR "dependency upgrade" OR "dependency upgrades" OR "dependency update" OR "dependency updates" OR "dependency migration" OR "library upgrade" OR "library upgrades" OR "library migration" OR "library evolution" OR "library version" OR "library versions" OR "version incompatibility" OR "version incompatibilities" OR "incompatible dependency" OR "incompatible dependencies" OR "version-aware" OR "version-controllable" OR "version-conditioned" OR "API migration" OR "API update" OR "API updates" OR "API change" OR "API changes" OR "deprecated API" OR "deprecated APIs" OR "API deprecation" OR "breaking change" OR "breaking changes" OR "dependency breaking change" OR "dependency-breaking change" OR "code migration" OR "codebase migration" OR "repository migration" OR "repository-level migration" OR "project migration" OR "version migration" OR "vulnerable dependency" OR "vulnerable dependencies" OR "library vulnerability" OR "dependency vulnerability" OR "dependency vulnerabilities" OR "vulnerability remediation" OR "vulnerability mitigation" OR "dependency remediation")
```

---

## Scopus
```
TITLE-ABS-KEY( A AND B ) AND PUBYEAR > 2022 AND ( LIMIT-TO ( LANGUAGE , "English" ) )
```

## Web of Science (Core Collection)
```
TS=( A AND B )
```
Refine: Publication Years 2023–2026; English; Document Types Article OR Proceedings Paper.

## IEEE Xplore (Command Search; field = All Metadata)
```
("All Metadata": A) AND ("All Metadata": B)
```

## ACM Digital Library (Advanced Search; Any/Abstract field)
```
([Abstract: A]) AND ([Abstract: B])
```

## SpringerLink
```
(A) AND (B)
```
Refine: 2023–2026; English; Computer Science.

## ScienceDirect (Title, abstract, keywords)
```
(A) AND (B)
```
If rejected for complexity, split Block A into core-LLM and agentic halves and merge results.

## arXiv (API / advanced search)
```
(all: A) AND (all: B) AND submittedDate:[202301010000 TO 202312312359] AND (cat:cs.SE OR cat:cs.AI OR cat:cs.SW OR cat:cs.CL)
```
Adjust the end date to the search day.

---

## Runbook — fill in on execution

| Source | Date run | Query ver. | Hits | Exported to | Notes |
|---|---|---|---|---|---|
| Scopus | | v0.4 | | | |
| Web of Science | | v0.4 | | | |
| IEEE Xplore | | v0.4 | | | |
| ACM DL | | v0.4 | | | |
| SpringerLink | | v0.4 | | | |
| ScienceDirect | | v0.4 | | | |
| arXiv | | v0.4 | | auto | ~1,329 (v0.3 estimate) |
| OpenAlex | | v0.4 | | auto | not a primary source |
