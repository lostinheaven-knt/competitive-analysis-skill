# Qualitative Fallback

Use this file when quantitative ranking is not defensible because metric coverage is sparse, variance is too low, or evidence quality is too weak.

## When to switch
Use qualitative fallback when any of these are true:
- `normalize_scores.py` recommends `qualitative-fallback-recommended`
- `weighted_rank.py` recommends `qualitative-fallback-recommended`
- Fewer than two discriminative metrics remain after normalization
- Average weighted metric coverage is too low to defend a numeric ranking
- The evidence is mostly inferred, stale, conflicting, or market definitions do not line up

## Output goal
Do not pretend to rank precisely. Produce a structured shortlist that still supports decisions.

## Minimum output structure
Include all of the following:
1. Why quantitative ranking was not used
2. Shortlist tiers or ordered groups, not fake decimal precision
3. For each shortlisted candidate:
   - name
   - competitor type
   - inclusion reason
   - major evidence points
   - major uncertainty points
4. Evidence strength note across the whole shortlist
5. Next steps needed to upgrade confidence

## Recommended tier labels
Use one of these patterns:
- Tier 1 / Tier 2 / Watchlist
- Strong fit / Plausible fit / Secondary fit
- Primary shortlist / Secondary shortlist / Monitor

Choose the simplest label set that matches the task.

## Qualitative reasoning rules
- Prefer grouped tiers over exact ranks when the evidence does not justify exact ordering.
- If one candidate clearly dominates on reliable evidence, it is acceptable to place it alone in the top tier.
- Explain why each candidate is in scope using customer overlap, product overlap, price overlap, channel overlap, or workflow overlap.
- State what would change the shortlist: better pricing data, more channel evidence, fresher usage signals, clearer geographic scope, etc.

## Suggested wording
Use concise wording such as:
- "Quantitative ranking was not used because the remaining metrics were too sparse to support a defensible score."
- "This is a qualitative shortlist grouped by evidence strength rather than a precise numeric ranking."
- "Confidence is limited by weak variance in observed metrics and incomplete channel evidence."

## Quality bar
A qualitative fallback is successful only if it is more honest, not less useful.
Avoid vague prose. The reader should still know:
- who is most likely in the shortlist
- why they are included
- what is uncertain
- what evidence would most improve the analysis
