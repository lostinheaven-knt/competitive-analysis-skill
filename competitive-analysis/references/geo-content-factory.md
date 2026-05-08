# GEO Content Factory Reference

Use this reference when generating SEO/GEO-optimized articles from the competitive analysis results.

## Purpose
After completing a competitive analysis with GEO topics and query packs, generate one article per P1 (and optionally P2) topic. These articles are **external-facing content** designed for search engine and generative-engine visibility — not internal analysis documents.

## When to generate articles
Generate articles when the user:
- explicitly asks for content to publish
- wants SEO/GEO content for brand visibility
- asks for "articles", "blog posts", "landing pages", or "content" based on the analysis
- wants to populate content gaps identified in the GEO section

Do **not** auto-generate articles unless the user requests them. The default output is the report with its embedded GEO section.

## Workflow

### Step 1: Select topics for article generation
- Start with all P1 topics from the GEO topic map.
- Include P2 topics if the user wants broader coverage or if P2 topics map to high-value content gaps.
- Skip P3 topics unless the user explicitly asks.

### Step 2: Choose article template per topic
Use the topic-type-to-template mapping:

| Topic type | Article template | Template file |
|---|---|---|
| Brand direct-check | Entity Definition Page | `assets/templates/article-templates/entity-definition.md` |
| Recommendation | Listicle | `assets/templates/article-templates/listicle.md` |
| Comparison | Comparison Page | `assets/templates/article-templates/comparison.md` |
| Scenario decision | How-to Guide | `assets/templates/article-templates/how-to-guide.md` |
| Trust / risk validation | FAQ Page | `assets/templates/article-templates/faq-page.md` |
| Substitute / alternative | Alternative-To Page | `assets/templates/article-templates/alternative-to.md` |
| Price / value judgment | FAQ Page or How-to Guide | `assets/templates/article-templates/faq-page.md` or `how-to-guide.md` |

If a topic fits multiple templates, prefer the one that best matches the user's primary intent.

### Step 3: Populate articles from analysis data
For each article, pull data from the already-completed analysis:

| Article element | Data source in the analysis |
|---|---|
| Brand facts (founding, scale, region) | Candidate pool / competitor detail cards |
| Service descriptions | Platform evidence / competitor detail cards |
| Comparison tables | Scoring summary / competitor detail cards |
| Pricing information | Platform evidence / public data |
| Customer segments | Scope definition / target user segment |
| FAQ answers | GEO query packs → rewrite as FAQ Q&A |
| Trust signals | Evidence quality notes / certifications |
| Competitive positioning | GEO brand position judgment |

**Key rule:** Do not fabricate data. If a data point is missing from the analysis, leave the placeholder and flag it clearly with `[待补充]` or `[需验证]`.

### Step 4: Apply GEO optimization rules
Every article must follow these GEO rules (derived from the `geo-optimization` skill):

#### Entity clarity
- First paragraph clearly defines what the brand is
- Brand name used consistently throughout
- Clear category placement ("X is a [type of thing]")

#### Quotable facts
- Specific numbers, not vague claims ("成立于2008年" not "历史悠久")
- Key facts in standalone sentences (easy for LLMs to extract)
- Include a "by the numbers" or key facts section

#### FAQ coverage
- Every article must include an FAQ section
- FAQ questions should directly mirror the GEO query pack for that topic
- Answers must be direct and complete (40-60 words each)

#### Comparison positioning
- When a comparison is relevant, include a comparison table
- Be factual and fair — do not write marketing copy
- Name competitors explicitly (LLMs need to see the relationship)

#### Structural clarity
- Clear H1→H2→H3 hierarchy
- Short paragraphs (2-4 sentences)
- Tables for decisions and comparisons
- Summary or TL;DR at top

#### Authority signals
- Include founding year, company size, certifications
- Mention third-party validation (industry association membership, awards, government备案)
- Add "last updated" date

#### Freshness
- Always include the current year in the title
- Add "最后更新：YYYY年MM月" at the top
- Do not use outdated references

#### GEO anti-patterns (DO NOT)
- Do not use vague superlatives ("最好的", "领先的", "行业Top")
- Do not keyword-stuff
- Do not write marketing copy or promotional language
- Do not hide competitors — address them directly and fairly
- Do not use outdated statistics without dates

### Step 5: Add images and visual elements
Articles should be "图文并茂" (rich with visuals). For each article:

#### Required visual elements
1. **Hero image or illustration**: At the top of the article. Prefer a real brand photo from search results. If no real image is available, use the placeholder format: `<!-- 📷 待补充图片：[品牌名]品牌/门店实景，可从品牌官网/大众点评/小红书获取 -->`
2. **Comparison tables**: Already included in templates — these count as visual elements.
3. **Data callout boxes**: Use blockquote format for key statistics and facts:
   ```markdown
   > **关键数据：** 品牌成立于2008年，团队规模50-99人，注册资本510万元。
   ```
4. **Infographic suggestions**: For articles with complex comparisons, suggest an infographic layout in a placeholder block with sourcing guidance.

#### Image sourcing strategy
Priority order:
1. **Real images with URLs from search results**: When web_search or web_fetch captures brand-related pages, actively extract image URLs from the page HTML (look for `<img src=...>`, `data-src=...`, `data-original=...`). Verify the URL is accessible (HTTP 200) before using. This is the **primary and preferred** method — always try this first.
2. **Brand's own images**: If platform evidence collection captured brand site images, use those (with attribution).
3. **Image placeholder with sourcing guidance**: If no real image can be found from search results or brand sites, do NOT generate images. Instead, insert a clearly marked placeholder block that describes what image is needed and where to find it:
   ```markdown
   <!-- 📷 待补充图片：[品牌名]门店实景照片，可从品牌官网/大众点评/小红书获取 -->
   ```
   The placeholder must include:
   - What the image should show (subject/content)
   - Where to source it (brand site, review platforms, social media, etc.)
   - Approximate size or aspect ratio if relevant

**Key principle: Get real image URLs wherever possible. Placeholders are the last resort, not the default.**

**Do NOT generate images.** Only use real images found through search or brand evidence collection. When no real image is available, use the placeholder format above.

#### Image placement rules
- At least 1 image per 500 words (real images from search results, or placeholders if unavailable)
- Every comparison table is a visual element
- FAQ sections do not need images
- Hero image at the very top of every article (real brand photo preferred; placeholder if unavailable)
- When inserting a real image found from search, include the source URL:
  ```markdown
  ![图片说明](image-url) 
  *图片来源：[来源平台/网站]*
  ```

### Step 6: SEO meta information
For each article, generate:

| Element | Content |
|---|---|
| **Meta title** | [Primary keyword]: [Benefit] ([Year]) — keep under 60 characters |
| **Meta description** | Include primary keyword, value proposition, and CTA — keep under 155 characters |
| **Primary keyword** | The core GEO query this article targets |
| **Secondary keywords** | 2-3 related GEO queries from the same or adjacent topics |
| **Canonical topic** | Which GEO topic this article addresses |
| **Schema type** | FAQPage, Article, or Organization (recommend which to implement) |

### Step 7: Quality check
Before delivering articles, verify:

- [ ] Every placeholder from the template is filled (no `[品牌名]` left unreplaced)
- [ ] No fabricated data — missing data flagged with `[待补充]`
- [ ] FAQ section directly mirrors GEO query pack queries
- [ ] Comparison tables are fair and factual
- [ ] Article reads naturally — not like a stuffed keyword page
- [ ] GEO anti-patterns are absent (no vague superlatives, no marketing copy)
- [ ] "Last updated" date is present
- [ ] At least 1 visual element per 500 words
- [ ] SEO meta information is complete

## Article output format
Save each article as a separate file:
```
competitive-analysis-skill/[brand-slug]-[topic-slug]-article.md
```

Example:
```
competitive-analysis-skill/jinbei-guangzhou-jiazheng-tuijian-article.md
competitive-analysis-skill/jinbei-vs-yierbao-article.md
competitive-analysis-skill/jinbei-kaopuma-article.md
```

## Integration with competitive analysis workflow
Article generation happens **after** the competitive report is complete. It is an optional extension, not a mandatory part of the standard workflow.

The standard workflow now looks like:
1. Scope → 2. Evidence → 3. Candidates → 4. Platform evidence → 5. Filter → 6. Scoring → 7. Rank → 8. Review → 9. GEO topics & queries → 10. **GEO content articles (optional)** → 11. Produce report

Step 10 is only executed when the user asks for articles.

## Template routing
- Need entity definition article → `assets/templates/article-templates/entity-definition.md`
- Need comparison article → `assets/templates/article-templates/comparison.md`
- Need listicle article → `assets/templates/article-templates/listicle.md`
- Need alternative-to article → `assets/templates/article-templates/alternative-to.md`
- Need how-to guide article → `assets/templates/article-templates/how-to-guide.md`
- Need FAQ page article → `assets/templates/article-templates/faq-page.md`

## External skill references
The following external skills provide additional best practices that inform this content factory:
- `seo-content-writer`: SEO on-page optimization, CORE-EEAT constraints, content structure templates
- `geo-optimization`: GEO audit checklist, platform-specific tactics, schema markup, monitoring

When these skills are installed in the workspace, the agent may read them for deeper guidance. When they are not installed, the rules in this reference file are sufficient for generating quality articles.
