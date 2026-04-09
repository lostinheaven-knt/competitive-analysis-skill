# Scoring Framework

Use this file when the task needs more than a simple competitor list and requires a defensible ranking or shortlist.

## Core principle
Score only what is relevant to the user's decision. Avoid fake precision.

## Common metric families
Choose from these families based on business context.

### 1. Market position
- market share
- sales volume
- growth rate
- account count or customer base

### 2. Product or feature strength
- capability coverage
- quality of core workflows
- technical depth
- ecosystem and integrations

### 3. Pricing and packaging
- price level
- discount intensity
- pricing transparency
- packaging flexibility

### 4. Channel and distribution
- retail presence
- marketplace presence
- direct sales coverage
- partner or reseller network

### 5. Brand and attention
- branded search interest
- share of voice
- traffic visibility
- social reach

### 6. User feedback
- ratings
- review sentiment
- retention proxies
- customer references

### 7. Innovation and momentum
- launch velocity
- roadmap visibility
- hiring signals
- R&D or patent proxies

## Good scoring behavior
For each metric, define:
- what it means
- where the data comes from
- whether higher is better or lower is better
- whether the metric applies to this market
- whether the number is official, estimated, or inferred

## Weight presets
Use these as defaults, then adapt.

### Conservative
Use when scale and incumbency matter most.
- Market position: 30
- Growth: 15
- Product strength: 15
- Pricing: 10
- Channel: 15
- Brand: 10
- User feedback: 5

### Balanced
Use when the user wants an all-around view.
- Market position: 20
- Growth: 15
- Product strength: 20
- Pricing: 10
- Channel: 10
- Brand: 10
- User feedback: 10
- Innovation: 5

### Aggressive
Use when disruption, growth, or product momentum matter more than incumbent scale.
- Market position: 10
- Growth: 25
- Product strength: 20
- Pricing: 10
- Channel: 10
- Brand: 10
- User feedback: 5
- Innovation: 10

## B2C hint
Usually weight these higher:
- market share or sell-through
- channel reach
- price position
- brand attention
- review signals
- platform-facing style overlap, content overlap, and buyer-visible product signals when the category is style-led or consumer-branded

## Platform-evidence scoring hint
When you have a platform evidence table, convert it into candidate-level rows and consider these metric families:
- style overlap score
- age overlap score
- price fit score
- content overlap score
- channel fit score
- platform evidence score
- evidence confidence score

Treat platform evidence score and evidence confidence score as guardrails against fake precision. If overlap looks high but evidence confidence is weak, lower confidence or fall back to qualitative ranking.

## Small-sample normalization caution
When the candidate set is small, min-max normalization can exaggerate separation and push the weakest visible candidate toward 0 even when the real-world gap is modest.
If the rank order or score spread changes materially between `minmax` and `rank` normalization, mention that sensitivity in the output instead of pretending the ordering is exact.

## B2B / SaaS hint
Usually weight these higher:
- feature fit
- customer overlap
- pricing model fit
- implementation or deployment fit
- ecosystem and integration depth
- revenue or growth proxies when reliable

## Missing data rules
- Do not convert missing values to zero unless the metric definition explicitly says absence means zero.
- Mark missing fields as `unknown`.
- If too many core metrics are missing, downgrade confidence or fall back to qualitative ranking.

## Transparency rule
Always show either:
- metric-level score breakdown, or
- a short explanation for qualitative ranking

A single total score without explanation is not enough.
