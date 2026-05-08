# Output Spec

Use this file to choose the right output format for the task.

## Output levels

### Level 1: quick shortlist
Use when the user wants a fast answer.
Include:
- 3-5 likely competitors
- one-line reason for each
- brief note on scope and uncertainty
- optional: 1-3 highest-priority GEO test queries as a quick tip

### Level 2: standard analysis
Use for most practical requests.
Include:
- scope summary
- candidate pool summary
- filtered shortlist
- scoring or comparison summary
- evidence notes
- risks or limitations
- GEO topic and query section:
  - compact topic map (topic name / type / priority / one-line significance)
  - P1 topic query packs (3-5 queries per P1 topic)
  - brand position judgment per topic (default recommendation / candidate / defensive / replaceable)
  - key competitor GEO pressure
  - recommended GEO actions (what content, proof, or comparison pages to prepare)

### Level 3: formal report
Use when the output is intended for review, circulation, or decision support.
Include:
1. Executive summary
2. Scope and assumptions
3. Sources and evidence quality
4. Candidate pool
5. Method and weighting
6. Final shortlist
7. Key findings
8. Risks and limitations
9. GEO topic and query recommendations
   - full topic map
   - P1 and P2 topic packs with query packs (3-5 queries per topic)
   - brand position judgment per topic
   - competitor GEO pressure summary
   - recommended GEO actions
   - priority test query list (P1 / P2 / P3)
10. Recommended next steps

### Level 4: monitoring pack
Use when the user wants a repeatable tracking setup.
Include:
- core competitor list
- watchlist
- metrics to refresh
- update cadence
- fields to monitor over time
- GEO monitoring queries (queries to re-run periodically in LLMs to track brand visibility changes)

## Required output fields
No matter the level, include as many of these as the task supports:
- name
- competitor type: direct, secondary, substitute, or watchlist
- inclusion reason
- major evidence points
- major uncertainty points
- score or ranking logic if used

## Audience rule for formal deliverables
Level 3 formal reports and any reader-facing deliverable must be written for the report audience, not for the analyst or skill maintainer.

Exclude internal production chatter such as:
- workflow optimization notes
- skill design or skill update notes
- sample contamination checks
- model/tool testing instructions meant for the analyst
- maturity labels like V1, V2, V3+, V4
- meta commentary about how the report could later be improved as an internal process artifact

If the reader needs follow-up guidance, rewrite it as business-facing recommendations, decision-oriented next steps, or research gaps that matter to the client.
For detailed rewrite rules and heading hygiene, read `references/report-audience-lint.md`.

## GEO data honesty rule
All GEO content in standard competitor reports is inference-based, derived from competitive analysis and general topic frameworks. It is not empirically tested against real LLM outputs.

When writing the GEO section:
- Frame judgments as "based on competitive analysis, the brand is likely to..." rather than "verified to..."
- Do not present query packs as search volume data or empirical evidence
- State clearly that the GEO section provides "topics and queries worth testing" rather than "tested results"
- If the user needs empirical GEO data, recommend running the query packs against actual LLM APIs separately

## Quality rule
If evidence is thin, shorten the confidence of the output instead of pretending precision.
In formal reports, state business-relevant limitations only; do not expose internal drafting or optimization process notes unless the user explicitly asks for methodology or internal QA commentary.
