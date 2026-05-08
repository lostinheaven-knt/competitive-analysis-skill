# competitive-analysis-skill

A reusable agent skill for competitor discovery, platform evidence collection, structured scoring, shortlist generation, report drafting, and **GEO (Generative Engine Optimization) topic & query analysis**.

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
- **embed GEO topic maps and native query packs into standard reports**
- **generate SEO/GEO-optimized articles from GEO topics** (optional, when the user asks for publishable content)

It is designed for tasks such as:

- competitor analysis
- competitor discovery
- market landscape comparison
- feature / price / channel benchmarking
- shortlist selection
- GEO / generative-engine visibility analysis
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

### 4. GEO topic & query analysis (embedded in standard reports)
Every standard competitor report (Level 2+) now includes a **GEO section** by default, covering:

- topic map based on 7 universal topic types (brand direct-check, recommendation, comparison, scenario decision, trust validation, substitute, price/value)
- native query packs for each P1/P2 topic — queries that mimic how real users ask GPT / 豆包 / DeepSeek / Kimi
- brand position judgment per topic (default recommendation / candidate / defensive / replaceable)
- competitor GEO pressure analysis
- recommended GEO actions (what content, proof, or comparison pages to prepare)

GEO content is **inference-based** (derived from competitive analysis), not empirically tested. The skill labels it as "topics and queries worth testing" rather than verified results.

For users who need a standalone deep GEO report, the skill also supports a **GEO-only mode** with a full 10-section structure.

### 5. GEO content factory (optional)
When the user asks for publishable content, the skill can generate one SEO/GEO-optimized article per GEO topic:

- **6 article templates**: entity definition, comparison, listicle, alternative-to, how-to guide, FAQ page
- **Auto-mapped to topic types**: recommendation → listicle, comparison → comparison page, trust → FAQ, etc.
- **Populated from analysis data**: brand facts, scoring, platform evidence, GEO queries → FAQ answers
- **GEO-optimized**: entity clarity, quotable facts, comparison tables, FAQ coverage, authority signals, freshness
- **图文并茂**: comparison tables, data callout boxes, real images from search results (or sourcing placeholders), at least 1 visual per 500 words
- **SEO meta**: title, description, primary/secondary keywords, schema type per article

Articles are optional — they are only generated when the user explicitly asks for content to publish.

### 6. Report generation
The skill supports both:

- formal structured reports (with embedded GEO section)
- qualitative shortlist outputs

It also supports merging ranking output with candidate metadata into report-ready input.

## Repository layout

```text
competitive-analysis/
├── SKILL.md
├── references/
├── assets/templates/
└── scripts/
    ├── assets/templates/article-templates/
```

### Important files

- `competitive-analysis/SKILL.md`  
  Core workflow, routing logic, and GEO mode integration.

- `competitive-analysis/references/geo-topic-quickref.md`  
  Condensed GEO reference for standard reports: 7 universal topic types, query-writing rules, brand position judgment, priority logic.

- `competitive-analysis/references/geo-report.md`  
  Full reference for standalone deep GEO reports (10-section structure, workflow, audience guardrails).

- `competitive-analysis/references/output-spec.md`  
  Output levels (L1–L4) with GEO section requirements per level and data honesty rules.

- `competitive-analysis/references/platform-evidence-deep-dive.md`  
  Guidance for stronger public-market and platform-facing evidence collection.

- `competitive-analysis/references/scoring-framework.md`  
  Scoring logic, weighting guidance, and normalization cautions.

- `competitive-analysis/references/qualitative-fallback.md`  
  Rules for switching from quantitative ranking to qualitative shortlist mode.

- `competitive-analysis/references/report-audience-lint.md`  
  Rewrite rules to keep reports client-facing and free of internal process leakage.

- `competitive-analysis/references/geo-content-factory.md`  
  Workflow for generating SEO/GEO articles from GEO topics: template selection, data population, GEO optimization, visual strategy, quality check.

- `competitive-analysis/assets/templates/article-templates/`  
  Six article templates: entity-definition, comparison, listicle, alternative-to, how-to-guide, faq-page.

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
- **GEO embedded by default — every competitive report includes topics and queries worth testing**
- **inference honesty — GEO content is labeled as derived analysis, not empirical data**

## Notes

- The public repo intentionally keeps only the reusable skill source.
- Runtime behavior is defined by `competitive-analysis/SKILL.md`, not by this README.
- Heuristic conversions inside scripts are intended to support shortlist workflows, not replace analyst judgment.

## Status

Current state: actively iterated, suitable for repeated real-world competitive-analysis trials with explicit uncertainty handling and embedded GEO analysis.
