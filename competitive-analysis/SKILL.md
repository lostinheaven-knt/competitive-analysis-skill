---
name: competitive-analysis
description: Identify, screen, score, and summarize competitors using structured market constraints, public data sources, weighted evaluation models, and reusable report templates. Use when the user asks for competitor analysis, competitor discovery, market landscape comparison, feature/price/channel benchmarking, shortlist selection, or a reusable framework for evaluating competing brands, products, or companies.
---

# Competitive Analysis

## Purpose
Identify likely competitors, narrow them into a defensible shortlist, and produce a structured comparison with clear assumptions, sources, scoring logic, and uncertainty notes.

## Inputs / Preconditions
Collect the minimum viable scope before doing deep analysis:
- Target being analyzed: company, brand, product, or solution
- Analysis goal: framework only, candidate discovery, shortlist, benchmark, or full report
- Industry / category
- Region / market scope
- Target customer segment
- Channel type
- Price band or commercial positioning
- Time horizon if trend or growth matters

If key scope is missing, read `references/scoping.md` and ask only the minimum questions needed to proceed.

## Fast Triage
Use this path selection early:
- If the user wants only a methodology or reusable framework, provide the framework and templates without pretending to have real market data.
- If the user wants a real competitor list, build a candidate pool first, then filter and score.
- If the user wants a formal deliverable, also read `references/output-spec.md` before drafting the final output.
- If the task touches claims, legal risk, or weak evidence, read `references/risks-and-compliance.md`.

## Procedure
1. Clarify the scope.
   - Read `references/scoping.md` when the target market, customer, channel, or price band is underspecified.
   - Prefer 3-5 focused clarification questions over a large questionnaire.

2. Decide the evidence standard.
   - Read `references/source-priority.md`.
   - Prefer primary and high-quality secondary sources.
   - Mark estimates and unresolved conflicts explicitly.

3. Build a candidate pool.
   - Read `references/competitor-identification-methods.md`.
   - Generate a broad list first, typically 10-30 names for non-trivial tasks.
   - Record why each candidate is included and what evidence supports inclusion.
   - For real-world consumer brands or style-heavy categories, do not stop at brand descriptions alone; plan a platform evidence pass for the target and top 5-6 candidates.

4. Deepen platform evidence when the task needs a defensible shortlist.
   - Read `references/platform-evidence-deep-dive.md` when the user wants a real competitor report, stronger proof, or deeper public data.
   - Anchor the target brand first, then gather platform-facing evidence for the top 5-6 candidate brands.
   - Separate directly observed platform signals from inferred brand positioning.
   - Keep an explicit gap note for blocked or unavailable platform data.

5. Filter obvious mismatches.
   - Read `references/decision-rules.md`.
   - Exclude entities with no meaningful overlap in industry, product line, customer, or route to market.
   - Separate direct competitors from substitutes, adjacent players, and watchlist names.

6. Select a scoring model.
   - Read `references/scoring-framework.md`.
   - Choose a standard preset or adapt weights to the business context.
   - Do not treat missing values as zero by default.
   - Weight platform-facing evidence more heavily when the competitive question depends on style overlap, content overlap, or buyer-facing product signals.

7. Score and rank candidates.
   - Use scripts in `scripts/` when structured data exists.
   - If you collected platform evidence rows, convert them into candidate-level scoring inputs with `scripts/platform_evidence_to_candidates.py` before normalization and ranking.
   - Prefer transparent scoring breakdowns over a single unexplained total.
   - Run `scripts/normalize_scores.py` before `scripts/weighted_rank.py` when using structured metrics.
   - If normalization or ranking recommends qualitative fallback, read `references/qualitative-fallback.md` and provide a qualitative shortlist instead of pretending precision.

8. Review the shortlist.
   - Check whether any market-defining competitor is missing.
   - Check whether high-visibility but weakly overlapping players were overrated.
   - Revisit the distinction between direct competitors and substitutes.

9. Produce the output.
   - Read `references/output-spec.md` for output level and format.
   - Include: shortlist, reasons, evidence quality, scoring logic, risks, and next steps.
   - When evidence is incomplete, say so plainly.
   - For Level 3 formal reports, use `assets/templates/report-outline.md` or generate the same structure with `scripts/generate_report_outline.py`.
   - For every shortlisted competitor, include name, competitor type, inclusion reason, major evidence points, major uncertainty points, and score or ranking logic.

## Reference Routing
Read only what is needed:
- Scope unclear -> `references/scoping.md`
- Need evidence hierarchy or citation discipline -> `references/source-priority.md`
- Need ways to discover candidates -> `references/competitor-identification-methods.md`
- Need platform-facing evidence collection and public proof standards -> `references/platform-evidence-deep-dive.md`
- Need metrics, normalization, or weighting -> `references/scoring-framework.md`
- Need shortlist rules -> `references/decision-rules.md`
- Need delivery format -> `references/output-spec.md`
- Need qualitative fallback rules when scoring is not defensible -> `references/qualitative-fallback.md`
- Need caution on legality, certainty, or public-facing claims -> `references/risks-and-compliance.md`
- Need a worked example -> `references/examples-b2c.md` or `references/examples-b2b-saas.md`

## Asset and Script Routing
Use bundled assets and scripts deliberately:
- Need a candidate intake sheet for discovery work -> `assets/templates/candidate-list.csv`
- Need interview prompts for expert calls, distributor checks, or channel validation -> `assets/templates/interview-questionnaire.md`
- Need a structured scoring table with evidence and uncertainty fields -> `assets/templates/scoring-sheet.csv`
- Need a platform evidence collection sheet for target and competitor brands -> `assets/templates/platform-evidence-table.csv`
- Need a qualitative shortlist scaffold when ranking is not defensible -> `assets/templates/qualitative-shortlist.md`
- Need a formal Level 3 report scaffold -> `assets/templates/report-outline.md`
- Need to validate whether scope is sufficient before analysis -> `scripts/validate_input_scope.py`
- Need to create a platform evidence row scaffold for multiple brands and platforms -> `scripts/platform_evidence_template.py`
- Need to convert platform evidence rows into candidate-level scoring inputs and merge-ready metadata -> `scripts/platform_evidence_to_candidates.py`
- Need to normalize raw metric values before ranking -> `scripts/normalize_scores.py`
- Need weighted ranking with weight validation and confidence warnings -> `scripts/weighted_rank.py`
- Need to merge ranking output with candidate metadata into a complete report input -> `scripts/merge_report_input.py`
- Need a report skeleton from structured JSON input -> `scripts/generate_report_outline.py`

## Formal Report Closure Rules
When producing a Level 3 formal report:
- Do not stop at section headers alone; fill the competitor detail cards.
- Ensure the final report covers all required output fields from `references/output-spec.md`.
- If quantitative ranking is low-confidence or sparse, downgrade confidence and consider a qualitative shortlist instead of pretending precision.
- Keep shortlist overview and competitor detail cards aligned so the report and score sheet do not contradict each other.

## Checks
Before finishing, verify all of the following:
- The market scope is explicit enough to defend the shortlist.
- Each shortlisted competitor has a clear inclusion reason.
- Important evidence sources are named or described.
- Any scoring model and weights are explained.
- Missing data, estimation, and uncertainty are clearly labeled.
- Direct competitors are distinguished from substitutes or adjacent players.

## Failure Modes
Watch for these common mistakes:
- Starting analysis before the market boundary is clear
- Treating all alternatives as direct competitors
- Treating missing data as poor performance
- Over-weighting vanity metrics such as buzz or traffic without overlap in customer or product
- Mixing evidence from different regions, time ranges, or market definitions without saying so

## Output Style
Prefer compact, decision-friendly outputs:
- Quick ask -> shortlist plus brief reasons
- Standard ask -> candidate pool, filtered shortlist, scoring summary, risks
- Formal ask -> structured report with method, evidence, shortlist, findings, limitations, and recommendations

Use bundled templates and scripts when they reduce repeated work or improve consistency.
