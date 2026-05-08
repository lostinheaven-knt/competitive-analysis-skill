# GEO Report Reference

> **Routing note:** This file is for **standalone deep GEO reports** only. If you are adding a GEO section to a standard competitor report (Level 2+), use `references/geo-topic-quickref.md` instead — it is shorter and tailored for embedded use.

Use this reference when the user wants a **GEO / generative engine** version of a competitor analysis, or asks for:
- GEO / generative search / generative engine optimization
- LLM visibility or recommendation analysis
- topics and query packs for GPT / 豆包 / DeepSeek / Kimi / similar tools
- native prompts users would naturally ask in AI chat products
- brand recommendation risk/opportunity in AI answers

## What GEO means here
GEO is **not** a rewrite of SEO keywords.

For this skill, GEO means:
> Analyze how a brand, product, or platform may appear inside generative-engine answers when real users ask natural questions, then produce topic maps and native query packs for testing and strategy.

## When to use GEO mode
Use GEO mode when the user needs one or more of these:
- topic maps for AI-answer visibility
- query packs that mimic real user prompts
- brand/competitor comparison prompts for LLM testing
- recommendations on what content or proof to prepare so the brand is more likely to be recommended

Do **not** force GEO mode when the user only wants a normal competitor shortlist.

Note: Standard competitor reports (Level 2+) now include a GEO section by default. You only need this full GEO mode when the user explicitly asks for a standalone deep GEO report, or when the GEO analysis needs to be much deeper than what a standard report section can provide.

## GEO prerequisites
Before writing a GEO report, gather the minimum viable scope:
- target brand / product / platform
- market or category
- region / language scope
- target user segment if relevant
- whether the goal is brand exposure, comparison defense, trust repair, conversion, or substitution defense

If this scope is incomplete, clarify only what is necessary.

## GEO workflow
1. Reuse or build a minimal competitor picture first.
   - GEO still needs competitive context.
   - Identify the target and the most relevant direct competitors or substitutes.

2. Translate the market into user-intent topics.
   - Think in terms of how a user would naturally ask for recommendations, comparisons, validation, or alternatives.
   - Avoid keyword stuffing and avoid turning prompts into blog titles.

3. Build a topic map.
   - For each topic, include:
     - topic name
     - topic type
     - priority
     - why it matters to the target brand

4. Generate native query packs.
   - Each topic should have several realistic queries.
   - Queries should sound like a real user talking to GPT / 豆包 / DeepSeek / Kimi.

5. Judge brand position within each topic.
   - Is the target likely to be:
     - a default recommendation
     - a candidate option
     - a defensive mention
     - a replaceable option
   - Note which competitors are most likely to outrank or outframe the target.

6. Recommend follow-up actions.
   - Suggest what the brand should prepare for better GEO performance:
     - comparison pages
     - FAQ content
     - trust signals
     - pricing/value explanations
     - scenario-specific content

## Universal GEO topic taxonomy
These topic types are broadly reusable across industries and are safe to use in the skill itself:

### 1. Brand direct-check
The user already knows the brand and wants a judgment.
Examples:
- Is [brand] good?
- Is [brand] worth buying/using?
- Is [brand] reliable?

### 2. Recommendation
The user wants candidates, not necessarily a specific brand.
Examples:
- What are good options in [category]?
- Which [product/platform] would you recommend?

### 3. Comparison
The user is choosing between candidates.
Examples:
- [brand A] vs [brand B]
- Which is better for [goal]?

### 4. Scenario decision
The user is asking from a concrete use case.
Examples:
- Which is better for [user type]?
- What should I choose if I want [outcome]?

### 5. Trust / risk validation
The user is checking legitimacy, quality, risk, or value.
Examples:
- Is [brand] legit?
- Is this worth paying for?
- Any catch?

### 6. Substitute / alternative
The user wants a replacement, stronger option, cheaper option, or safer option.
Examples:
- Is there a better alternative to [brand]?
- If I skip [brand], what else should I try?

### 7. Price / value judgment
Useful when there is a paid offer or price ladder.
Examples:
- Is the paid version worth it?
- Is this price reasonable?

## Query-writing rules
Queries in GEO reports should:
- sound like real user prompts
- be ready to paste into GPT / 豆包 / DeepSeek / Kimi
- express a clear decision, comparison, doubt, or selection intent
- avoid SEO headline style
- avoid awkward keyword stuffing

Mix query styles deliberately:
- direct ask
- comparison ask
- scenario ask
- skeptical ask
- filtering ask

## GEO output structure
A solid GEO report should include:
1. Executive summary
2. Scope and GEO assumptions
3. Topic map
4. Core topic packs
5. Likely competitor pressure by topic
6. Brand opportunities and risks
7. Recommended GEO actions
8. Priority test query list

For each core topic, include:
- topic name
- topic intent
- target brand position judgment
- key competitors
- query pack
- recommended action

## Audience guardrail for GEO deliverables
A GEO report delivered to a brand/client is still a client-facing report.

Exclude analyst-facing or skill-facing content such as:
- “how we will improve the skill next”
- sample-to-skill abstraction notes
- internal QA or prompt-design commentary
- maturity labels like V1/V2/V3+
- instructions meant for the analyst rather than the brand

Keep reader-facing GEO recommendations focused on:
- what topics matter
- where the brand is strong or weak
- what content, proof, comparison pages, or FAQ material should be prepared
- what prompt sets are most important to test for business insight

If you need to preserve internal GEO methodology notes, store them outside the formal client report.
For detailed rewrite rules and report hygiene, read `references/report-audience-lint.md`.

## Priority logic
Use P1 / P2 / P3 priorities:
- **P1**: recommendation, comparison, trust, paid-value, or substitution topics with strong decision intent
- **P2**: useful scenario extensions or narrower audiences
- **P3**: lower-leverage, low-differentiation, or edge-case topics

## Guardrail against case contamination
When writing or updating skill rules from a GEO sample:
- keep only cross-industry rules in the main SKILL
- keep case-specific topic nuances in sample reports or other references
- if a rule only makes sense for one industry, do not promote it into the main skill body

Use this quick check before promoting a GEO rule:
1. Would this still hold in a different industry?
2. Can it be expressed with variables like [brand], [competitor], [scenario], [risk], [user goal]?
3. Is it a GEO method rule or a market-specific insight?

If the answer is mostly no, keep it out of the main SKILL.

## Template routing
For a formal GEO deliverable, use:
- `assets/templates/geo-report-outline.md`

For sample-specific inspiration, rely on case files in the workspace rather than copying industry-specific queries into the skill.