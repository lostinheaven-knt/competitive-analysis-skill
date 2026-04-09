# Platform Evidence Deep Dive

Use this file when the task requires stronger public-market evidence, platform-specific validation, or a more defensible shortlist based on observable product and content signals.

## When to use
Read this file when any of these are true:
- The user asks for a real-world competitor report, not just a framework
- The first-pass shortlist feels too shallow or too small
- The user asks for platform evidence, hard proof, data depth, or a V4-style evidence pass
- You need to validate price bands, style overlap, content overlap, or category overlap
- You need to separate what is directly observed from what is inferred

## Core rule
Do not rely only on brand descriptions.
For each priority brand, try to collect both:
1. **Brand evidence** — official site, brand page, encyclopedia, reliable brand profile
2. **Platform evidence** — observable marketplace, content platform, or retail traces

If platform evidence cannot be collected, say that explicitly and log the gap instead of pretending certainty.

## Priority platforms
Prefer the platforms most likely to show real buyer-facing signals:
- **Taobao / Tmall**: public product titles, price samples, category mix, style words, store fragments
- **Douyin**: account positioning, content themes, creator-facing language, visible product style cues
- **Xiaohongshu**: style tags, search phrasing, aesthetic associations, buyer mindshare clues
- **Brand site / official flagship pages**: positioning, age band, product families, brand narrative
- **Encyclopedia / CNPP / credible industry profiles**: age band, founding year, category scope, distribution, public positioning

## Evidence hierarchy
Use this hierarchy when scoring confidence:
- **High**: official site, official flagship page, directly observed product or account pages, clearly attributable brand-owned pages
- **Medium-high**: reliable brand profiles, encyclopedia pages, strong industry directories, directly observed marketplace snippets with clear brand match
- **Medium**: vertical media, interviews, event coverage, multi-source indirect confirmation
- **Low**: search summaries, partial snippets, pages blocked by rendering, unattributed reposts

## Required collection fields
For each brand, capture as many of these as possible:
- brand
- platform
- evidence level
- source type
- direct observation summary
- style keywords
- age signal
- price signal
- content signal
- category / hot-SKU signal
- channel signal
- overlap with target
- main gap or uncertainty
- source reference or URL when available

## Minimum viable deep dive for priority brands
For the target brand and top 5-6 competitor candidates, try to capture:
1. 10+ price samples or a clear price band summary when visible
2. 5-10 product/style keywords actually observed on platform-facing pages
3. age or customer signal
4. content/account positioning where available
5. at least one explicit gap note for anything blocked or unverified

## Workflow
1. Start with the target brand.
   - Anchor the target's style, age, price, and channel signals first.
   - Without this anchor, platform comparison drifts.

2. Deepen the shortlist candidates.
   - Focus on the top 5-6 brands most likely to compete for the same user.
   - Prioritize the target brand and the most decision-relevant shortlist candidates first.
   - Do not spend equal time on broad market pressure brands unless the user asks.
   - Do not force equal coverage across all brands just because they are in the candidate pool.

3. Separate direct observation from inference.
   - "Observed on Taobao product titles" is different from "brand appears design-led from profile copy".
   - Mark inferred fields explicitly.

4. Build a platform evidence table.
   - Use `assets/templates/platform-evidence-table.csv` or `scripts/platform_evidence_template.py`.
   - One row per brand-platform observation is usually better than one row per brand if evidence is mixed.

5. Summarize at brand level.
   - Convert row-level observations into brand summaries only after the table is filled.
   - Keep the raw platform table available for audit.

6. Use evidence gaps as part of the answer.
   - If a candidate looks similar but platform proof is weak, lower confidence.
   - If a candidate has stable brand evidence but missing platform signals, note that it is directionally relevant but not fully validated.

## What counts as "platform hard proof"
Examples of stronger signals:
- repeated product-title keywords
- visible price ranges across multiple items
- explicit age-band wording
- official account positioning text
- recurring content themes
- directly observed product/category structure

Examples of weaker signals:
- one-off search snippets
- generic listicles
- unsupported summaries with no attributable page
- search results that do not clearly resolve to the brand

## Output expectation
A deeper competitor report should normally include:
- the shortlist
- platform evidence summary for each priority brand
- what is strongly observed
- what is still inferred
- a note on blocked or missing platforms
- confidence by brand or evidence bucket

## Anti-patterns
Avoid these mistakes:
- declaring a precise competitive ranking without platform-facing evidence
- using only corporate brand descriptions for style-heavy consumer brands
- confusing mass-market pressure brands with close style-neighbor brands
- hiding blocked pages or missing platform data
- collecting only one or two competitor names and calling it "deep dive"
