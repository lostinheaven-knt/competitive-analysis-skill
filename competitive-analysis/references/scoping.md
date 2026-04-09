# Scoping

Use this file when the user asks for competitor analysis but the market boundary is still fuzzy.

## Minimum viable scope
Collect enough information to avoid comparing the wrong things:
- Target under analysis
- Industry or category
- Region or market scope
- Target customer
- Analysis goal

If any of the above is missing, analysis can still start in light mode, but the output must be labeled provisional.

## Optional but high-value constraints
Add these when available:
- Product line or subcategory
- Company size or maturity stage
- Channel model: online, offline, direct sales, marketplace, reseller, partner-led
- Price band or commercial positioning
- Buying motion: self-serve, sales-led, enterprise procurement
- Time horizon: current state vs. trend over time
- Output depth: quick list, benchmark table, or full report

## Ask only what matters
Prefer a few targeted questions over a giant intake form.

### Compact clarification set
Use these first:
1. What exactly are we analyzing: company, brand, product, or solution?
2. Which market or region matters most?
3. Who is the target customer?
4. Do you care most about market position, product capability, price, channel, or brand?

### If still unclear
Ask one or two more:
- What price band or segment should count as comparable?
- Which sales channel matters most?
- Are substitutes in scope, or only direct competitors?

## Default handling
If the user does not specify a field:
- Mark it as `unspecified`
- Do not silently invent a constraint
- If the missing field materially changes the shortlist, ask before going deeper

## B2C prompts
Use these when analyzing consumer products or brands:
- Which category and subcategory?
- Which geography matters: local, national, global?
- Which channels matter most: e-commerce, retail, DTC, social commerce?
- What price tier should count as comparable?
- Is brand awareness more important than raw sales?

## B2B / SaaS prompts
Use these when analyzing software or enterprise solutions:
- What buyer segment matters: SMB, mid-market, enterprise?
- Which function is core: HR, CRM, analytics, support, security, etc.?
- Is deployment model relevant: cloud, hybrid, on-prem?
- Is pricing model relevant: seat-based, usage-based, annual contract?
- Are we comparing direct feature overlap, customer overlap, or go-to-market overlap?

## Scope quality check
Proceed confidently only when these are clear enough:
- There is a defined target
- There is a plausible market boundary
- There is at least one basis for comparability: customer, category, price, channel, or workflow

If not, produce a framework or provisional candidate pool rather than a hard shortlist.
