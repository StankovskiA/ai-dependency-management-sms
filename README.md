# LLM and Agentic AI for Software Dependency Management: A Systematic Mapping Study — Verification Data

Repository: <https://github.com/StankovskiA/ai-dependency-management-sms>

This is the verification package for the systematic mapping study (SMS) of LLM and
agentic AI for software dependency management. 

## Files

| File | Content |
|---|---|
| `extraction.csv` | one row per included paper (88 rows), with extracted fields and normalized complexity constructs |
| `screening.csv` | title/abstract, full-text and snowball decisions |
| `search_funnel.json` | identification, deduplication and screening counts |
| `dedup_report.json` | per-source counts and duplicate groups behind the funnel |
| `queries.md` | the exact database and arXiv queries |
| `verify.py` | recomputes the paper's extraction and funnel numbers from the CSV/JSON |
| `CITATION.cff` | citation metadata |
| `LICENSE` | data and code licences |
| `checksums.sha256` | SHA-256 checksums for the package |

## Funnel

| Stage | n |
|---|---:|
| Records identified | 2,408 |
| Duplicates removed | 296 |
| Unique records | 2,112 |
| Screened at title/abstract | 2,112 |
| LLM first-pass includes | 83 |
| LLM first-pass excludes | 1,617 |
| LLM first-pass uncertain | 412 |
| Excluded at title/abstract (exclude + uncertain) | 2,029 |
| R1-final title/abstract includes | 85 |
| Full-text records | 85 |
| Included from the database search | 79 |
| Snowball candidates identified | 687 |
| New since 2023 | 286 |
| With abstract | 250 |
| Snowball candidates carried to full text | 11 |
| Snowball included after full text | 9 |
| **Included in the review** | **88** |

The paper's "83 provisional includes" is the LLM first pass. R1 overrides raise the final
title/abstract count to 85; the full-text file has 85 rows. Records dated 2027 were screened and
excluded; one of them (`R01272`) reached full text and was excluded by R1. The two snowball exclusions are
`C0067` (EC3) and `C0187` (EC5).

Full-text decisions apply the R1 overrides: `R00071` is included and `R01272` is excluded. The two
blank verdicts, `R00011` and `R01519`, are EC2 (full text unavailable), not undecided includes. The
79 full-text includes therefore match the 79 database rows in `extraction.csv`. Title/abstract
`r1_decision` is stage-specific; full-text overrides are not copied into it.

## Extraction table

`extraction.csv` has **88 rows**, one per included paper.

- `arm`: `database` (79) or `snowball` (9).
- `extraction_status`: `full` for the 79 database studies (41-field extraction, reduced here to
  the substantive fields), `targeted` for the 9 snowball studies.
- The 9 snowball studies have blank non-targeted fields. They were extracted only for the
  complexity constructs used in the review's gap analysis.
- `complexity_constructs`: JSON list of `{class, nature, construct}` entries for the paper.
- `n_complexity_constructs`: length of that list.

The expected totals are:

| Quantity | Value |
|---|---:|
| Complexity-construct rows | 312 |
| Distinct constructs | 312 |
| Ordinal-label constructs | 106 |
| Constructs whose text mentions reliability | 2 |
| Papers with no complexity construct | 16 |
| Database-arm task distribution | migration 45, breaking_change 12, other 6, vuln_driven_update 5, upgrade 5, resolution 4, conflict_repair 2 |
| Database-arm study types | tool 33, benchmark 20, empirical 19, mixed 6, industry 1 |

The 16 papers with no construct are not padded with empty rows: the source table contains 16
`(none)` placeholders, which are omitted here. The truthful totals are 312 construct rows and 312
distinct non-empty constructs, not 328/313.

## Screening table

`screening.csv` has 2,208 rows:

- `stage = title_abstract`: 2,112 rows. `llm_decision` is the first-pass decision
  (`include` / `exclude` / `uncertain`); `r1_decision` records overrides; `final_decision` is
  the post-R1 decision.
- `stage = fulltext`: 85 rows. `final_decision` is `include`, `exclude`, or blank for a missing
  verdict.
- `stage = snowball_fulltext`: 11 rows; 9 include and 2 exclude.

## Reproduce

Requires Python 3.11+ and only the standard library:

```bash
python verify.py
```

The verifier recomputes every number above from `extraction.csv`, `screening.csv`, and
`search_funnel.json`, and exits nonzero on any mismatch.

## Method

- **Study type:** systematic mapping study (scoping review); no effectiveness synthesis.
- **Mapping questions:** dependency-management tasks; techniques and architectures; evolution,
  ecosystems and dependency scope; evaluation designs and artifacts.
- **Search window:** 2023-01-01 to 2026-10-05.
- **Sources:** Scopus, Web of Science, IEEE Xplore, ACM Digital Library, SpringerLink and arXiv.
- **Screening:** LLM-assisted first pass (`deepseek-v4.1-flash`, temperature 0), R1 verification
  of every include and every LLM exclude. The R2 audit is pending; this is stated as a
  limitation.
- **Snowballing:** backward and forward from the 79 database includes; 687 candidates, 286 new
  since 2023, 11 carried to full text, 9 included.
- **Extraction:** the 79 database studies received the full extraction; the 9 snowball studies
  received a targeted extraction of complexity constructs.

The review is a mapping study, not an SLR with quality appraisal and effectiveness synthesis.
Full texts, abstracts and verbatim evidence quotes are not redistributed.

## Licence

Data: CC-BY-4.0. Code: MIT. Bibliographic metadata (titles, venues, DOIs) remains subject to the
original publishers' terms. See `LICENSE`.
