# competitive-analysis-skill

A reusable agent skill for competitor discovery, platform evidence collection, structured scoring, shortlist generation, and report drafting.

This repository publishes the **skill source only**.
Case-specific trial reports and local working files stay out of the public repo.

## What this skill does

This skill helps an agent:

- clarify market scope before analysis
- build a broad competitor pool
- deepen public platform evidence for the most relevant brands
- distinguish direct competitors from substitutes and watchlist names
- convert evidence into structured scoring inputs
- rank candidates with confidence and fallback rules
- generate formal report outlines and qualitative shortlists

It is designed for tasks such as:

- competitor analysis
- competitor discovery
- market landscape comparison
- feature / price / channel benchmarking
- shortlist selection
- reusable competitive-analysis workflows

## Key capabilities

### 1. Scope-first workflow
The skill starts by tightening:

- target
- industry / category
- region
- customer segment
- channel
- price band
- analysis goal

This reduces fake precision and weak shortlists.

### 2. Platform evidence deep dive
For real-world consumer-brand analysis, the skill supports a deeper evidence pass across sources such as:

- Taobao / Tmall
- Douyin
- Xiaohongshu
- brand sites / flagship pages
- encyclopedia / credible brand profile sources

It explicitly separates:

- directly observed platform signals
- inferred brand positioning
- blocked or missing evidence

### 3. Structured scoring with guardrails
The skill includes scripts for:

- input validation
- score normalization
- weighted ranking
- qualitative fallback when quantitative ranking is not defensible

It is designed to avoid common mistakes such as:

- treating missing data as zero
- ranking on weak evidence without saying so
- pretending exact precision when platform evidence is sparse

### 4. Report generation
The skill supports both:

- formal structured reports
- qualitative shortlist outputs

It also supports merging ranking output with candidate metadata into report-ready input.

## Repository layout

```text
competitive-analysis/
├── SKILL.md
├── references/
├── assets/templates/
└── scripts/
```

### Important files

- `competitive-analysis/SKILL.md`  
  Core workflow and routing logic.

- `competitive-analysis/references/platform-evidence-deep-dive.md`  
  Guidance for stronger public-market and platform-facing evidence collection.

- `competitive-analysis/references/scoring-framework.md`  
  Scoring logic, weighting guidance, and normalization cautions.

- `competitive-analysis/references/qualitative-fallback.md`  
  Rules for switching from quantitative ranking to qualitative shortlist mode.

## Main scripts

- `validate_input_scope.py`  
  Checks whether the analysis scope is defined enough to proceed.

- `platform_evidence_template.py`  
  Generates a CSV scaffold for platform evidence collection.

- `platform_evidence_to_candidates.py`  
  Converts row-level platform evidence into candidate-level scoring inputs and merge-ready metadata.

- `normalize_scores.py`  
  Normalizes numeric metrics and flags low-information conditions.

- `weighted_rank.py`  
  Produces weighted rankings with confidence and fallback recommendations.

- `merge_report_input.py`  
  Merges ranking output with candidate metadata into report-ready JSON.

- `generate_report_outline.py`  
  Produces a structured report outline from merged report input.

## End-to-end workflow

A typical structured path looks like this:

```text
scope
-> candidate pool
-> platform evidence table
-> candidate-level scoring inputs
-> normalization
-> weighted ranking
-> merge into report input
-> formal report outline or qualitative shortlist
```

## Design principles

This skill is built around a few practical principles:

- **scope before scoring**
- **evidence before confidence**
- **platform-facing proof for style-heavy consumer brands**
- **qualitative fallback when numeric ranking is not defensible**
- **structured outputs over vague summaries**

## Notes

- The public repo intentionally keeps only the reusable skill source.
- Runtime behavior is defined by `competitive-analysis/SKILL.md`, not by this README.
- Heuristic conversions inside scripts are intended to support shortlist workflows, not replace analyst judgment.

## Status

Current state: actively iterated, suitable for repeated real-world competitive-analysis trials with explicit uncertainty handling.
