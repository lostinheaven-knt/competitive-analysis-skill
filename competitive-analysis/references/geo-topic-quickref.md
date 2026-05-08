# GEO Topic Quick Reference

Use this quick reference when you need to add a GEO section to a standard competitor report (Level 2+).
For a standalone deep GEO report, use `references/geo-report.md` instead.

## What this file is for
This is a **condensed reference** for the most common GEO decisions you need while drafting a standard report:
- which topic types to cover
- how to write queries
- how to judge brand position
- how to prioritize

All GEO content in standard reports is **inference-based** (derived from competitive analysis), not empirically tested. Label it accordingly.

---

## 7 universal topic types

| # | Type | What the user is doing | Example prompt pattern |
|---|---|---|---|
| 1 | Brand direct-check | Already knows the brand, wants a judgment | `[brand]怎么样？` / `Is [brand] reliable?` |
| 2 | Recommendation | Wants candidates, doesn't know specific brands | `有什么[category]推荐？` / `Which [category] should I pick?` |
| 3 | Comparison | Choosing between two or more candidates | `[brand A]和[brand B]哪个好？` / `[A] vs [B]?` |
| 4 | Scenario decision | Asking from a specific use case or user type | `如果我是[人群]，选哪个？` / `Which is best for [scenario]?` |
| 5 | Trust / risk validation | Checking legitimacy, quality, or hidden risks | `[brand]靠谱吗？` / `Is this legit? Any catch?` |
| 6 | Substitute / alternative | Wants a replacement, cheaper option, or upgrade | `有没有比[brand]更好的替代？` / `Alternatives to [brand]?` |
| 7 | Price / value judgment | Asking whether the price or paid tier is worth it | `[brand]付费版值得买吗？` / `Is the paid version worth it?` |

These are cross-industry. Do not add industry-specific topic types to the main skill; keep those in case reports or industry references.

---

## Query-writing rules

### Do
- Write like a real user talking to GPT / 豆包 / DeepSeek / Kimi
- Express a clear decision, comparison, doubt, or selection intent
- Make queries ready to paste into an LLM
- Mix styles: direct ask, comparison ask, scenario ask, skeptical ask, filtering ask
- Keep queries in the user's natural language (Chinese for Chinese-market brands, English for global brands, etc.)

### Don't
- Don't write SEO-style headlines (e.g., "2026最好用的XX排行榜")
- Don't write marketing copy (e.g., "体验极致XX")
- Don't use excessive jargon that normal users wouldn't say
- Don't make queries so extreme they're unnatural
- Don't keyword-stuff

---

## Brand position judgment (4-level scale)

For each topic, judge where the target brand is likely to land in LLM answers:

| Position | Meaning | Implication |
|---|---|---|
| **Default recommendation** | LLM is likely to recommend this brand first or prominently | Strong position; defend it |
| **Candidate option** | LLM mentions this brand among several options | Moderate; needs differentiation content |
| **Defensive mention** | LLM mentions this brand only when specifically asked | Weak; needs proactive content |
| **Replaceable** | LLM is likely to suggest alternatives over this brand | At risk; needs trust proof and comparison content |

This judgment is **inference-based**. State it as "based on competitive analysis, the brand is likely to..." rather than "empirically verified to...".

---

## Priority logic

| Priority | Criteria | Typical topic types |
|---|---|---|
| **P1** | Strong recommendation/comparison/trust/substitution intent + competitor co-occurrence likely | Recommendation, Comparison, Trust validation, Substitute |
| **P2** | Useful scenario extensions, narrower audiences, needs brand explanation | Scenario decision, Brand direct-check |
| **P3** | Low differentiation, edge-case, or low impact on recommendation outcomes | Price/value (when brand has no paid tier), overly broad topics |

---

## Minimum GEO section for each report level

| Report level | GEO section requirement |
|---|---|
| Level 1 (quick shortlist) | Optional: 1-3 highest-priority test queries as a quick tip |
| Level 2 (standard analysis) | Required: topic map (compact table) + P1 query packs + brand position judgment + key GEO actions |
| Level 3 (formal report) | Required: full topic map + P1+P2 topic packs with query packs + brand position per topic + competitor GEO pressure + recommended GEO actions + priority test query list |
| Level 4 (monitoring pack) | Required: GEO monitoring queries field (queries to re-run periodically) |

---

## Contamination guard (quick check)

Before writing any GEO rule into the main skill, ask:
1. Would this still hold in a different industry?
2. Can it be expressed with variables like `[brand]`, `[competitor]`, `[scenario]`?
3. Is it a GEO method rule or a market-specific insight?

If mostly no → keep it in the case report, not the skill.
