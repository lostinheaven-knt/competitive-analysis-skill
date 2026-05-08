# GEO 内容工厂：从竞品报告自动生成 SEO/GEO 占位文章 实现计划

**目标：** 在 competitive-analysis skill 的报告生成流程末尾，针对每个 GEO 话题自动生成一篇面向 C 端的图文并茂文章，用于品牌在搜索引擎和生成式引擎中的内容占位。

**架构：** 复用报告生成过程中已收集的竞品信息、GEO 话题地图和 query 包，结合 `seo-content-writer` 和 `geo-optimization` 两个外部 skill 的最佳实践，为每个 P1/P2 话题选择最合适的文章模板，填充品牌事实和竞品比较数据，产出可直接发布的 SEO/GEO 优化文章。

**技术栈：** Markdown 文档 + skill references + 可选的图片生成/插入流程。无代码脚本改动。

---

## 设计思路

### 核心理念

竞品报告是"分析结果"，文章是"分析结果的内容化输出"。同一个分析流程，产出两种形态：
- **报告** → 给甲方内部看的决策文件
- **文章** → 给搜索引擎/LLM看的占位内容

文章不是报告的复制粘贴，而是把报告中的关键发现、比较数据、信任证据和 GEO query 回答，重新组织为符合 SEO/GEO 最佳实践的外部发布内容。

### 文章与 GEO 话题的映射

| 话题类型 | 最适合的文章模板 | 文章核心目的 |
|---|---|---|
| 品牌直查 | Entity Definition Page | 让 LLM 清晰识别品牌实体 |
| 推荐 | Listicle / Pillar Page | 品牌进入"推荐候选池" |
| 比较 | Comparison Page | 在竞品比较场景中占位 |
| 场景决策 | How-to Guide / Blog Post | 在特定场景下被推荐 |
| 信任验证 | FAQ Page | 直接回答信任类 query |
| 替代 | Alternative-To Page | 防守替代场景 |
| 价格/价值 | FAQ Page / Blog Post | 回答价格相关 query |

### 信息流向

```
竞品分析流程（已有）
  ├─ 候选池数据 ──────────────────┐
  ├─ 短表 + 评分 ─────────────────┤
  ├─ 平台证据 ───────────────────┤
  ├─ GEO 话题地图 ────────────────┤
  ├─ Query 包 ───────────────────┤
  └─ GEO 占位判断 + 竞品压力 ───┤
                                  │
                          ┌───────▼────────┐
                          │  文章生成模块   │
                          │  (新增)         │
                          └───────┬────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    │             │             │
              ┌─────▼─────┐ ┌────▼─────┐ ┌─────▼─────┐
              │ 话题 A 文章 │ │ 话题 B 文章│ │ 话题 C 文章│
              │ (SEO/GEO)  │ │ (SEO/GEO) │ │ (SEO/GEO) │
              └────────────┘ └───────────┘ └────────────┘
```

---

## 文件结构

| 文件 | 操作 | 职责 |
|---|---|---|
| `competitive-analysis/SKILL.md` | 修改 | Procedure 加步骤 10（Generate GEO content articles），Routing 加引用 |
| `competitive-analysis/references/geo-content-factory.md` | **新增** | 核心参考：话题→模板映射、文章生成工作流、SEO/GEO 优化规则、图片/配图策略、质量校验 |
| `competitive-analysis/references/geo-topic-quickref.md` | 修改 | 话题类型表加"推荐文章模板"列 |
| `competitive-analysis/assets/templates/article-templates/` | **新增目录** | 存放各类型文章模板 |
| `competitive-analysis/assets/templates/article-templates/entity-definition.md` | **新增** | 品牌实体定义页模板 |
| `competitive-analysis/assets/templates/article-templates/comparison.md` | **新增** | 竞品比较页模板 |
| `competitive-analysis/assets/templates/article-templates/listicle.md` | **新增** | 推荐列表页模板 |
| `competitive-analysis/assets/templates/article-templates/alternative-to.md` | **新增** | 替代方案页模板 |
| `competitive-analysis/assets/templates/article-templates/how-to-guide.md` | **新增** | 场景决策指南模板 |
| `competitive-analysis/assets/templates/article-templates/faq-page.md` | **新增** | FAQ 页模板 |
| `competitive-analysis/references/output-spec.md` | 修改 | 各 Level 加"GEO content articles"输出字段 |

不改的文件：
- `geo-report.md`、`geo-report-outline.md`：独立 GEO 报告模式不变
- `geo-generalization-memo.md`：历史备忘不变
- `scripts/` 目录：本期无脚本改动（文章由 agent 按 template 生成，不走脚本）

---

### 任务 1：新增文章模板目录和 6 个模板文件

**文件：**
- 创建：`competitive-analysis/assets/templates/article-templates/entity-definition.md`
- 创建：`competitive-analysis/assets/templates/article-templates/comparison.md`
- 创建：`competitive-analysis/assets/templates/article-templates/listicle.md`
- 创建：`competitive-analysis/assets/templates/article-templates/alternative-to.md`
- 创建：`competitive-analysis/assets/templates/article-templates/how-to-guide.md`
- 创建：`competitive-analysis/assets/templates/article-templates/faq-page.md`

- [ ] **步骤 1：创建目录**

```bash
mkdir -p competitive-analysis/assets/templates/article-templates
```

- [ ] **步骤 2：创建 entity-definition.md 模板**

```markdown
# [品牌名]：[品类]品牌介绍与核心优势

> **[品牌名]** 是一家[品类定位]，成立于[年份]，总部位于[城市/区域]。[一句话核心差异化]。

*最后更新：[YYYY年MM月]*

## [品牌名]是什么？

**[品牌名]** 是[品类]品牌，专注于[核心服务/产品]。与[主要竞品]不同，[品牌名][核心差异化点]。

### [品牌名]关键数据

- 成立时间：[年份]
- 服务区域：[区域]
- 团队规模：[人数或规模描述]
- 核心服务：[服务1]、[服务2]、[服务3]
- 资质/认证：[如有]

## [品牌名]的核心服务

### [服务1名称]
[2-3句描述，包含具体数据或案例]

### [服务2名称]
[2-3句描述，包含具体数据或案例]

### [服务3名称]
[2-3句描述，包含具体数据或案例]

## [品牌名]适合谁？

[品牌名]特别适合以下用户：

- [用户类型1]：[为什么适合]
- [用户类型2]：[为什么适合]
- [用户类型3]：[为什么适合]

## [品牌名]与[主要竞品]的区别

| 维度 | [品牌名] | [主要竞品] |
|---|---|---|
| [维度1] | [品牌表现] | [竞品表现] |
| [维度2] | [品牌表现] | [竞品表现] |
| [维度3] | [品牌表现] | [竞品表现] |

## 常见问题

### [品牌名]靠谱吗？
[直接回答，40-60字，引用具体事实]

### [品牌名]收费多少？
[价格信息或区间，如无公开价格则说明"需咨询"]

### [品牌名]和[竞品]哪个好？
[客观比较，说明各自优势场景]

*本文基于公开信息整理，旨在帮助消费者做出更明智的选择。*
```

- [ ] **步骤 3：创建 comparison.md 模板**

```markdown
# [品牌A] vs [品牌B]：[品类]怎么选？（[YYYY]年对比）

> **快速结论：** 如果你[核心场景]，选[推荐品牌]；如果你[另一场景]，选[另一品牌]。两家在[核心差异维度]上差别明显。

*最后更新：[YYYY年MM月]*

## 为什么你在纠结[品牌A]和[品牌B]？

[描述用户在这个比较场景中的典型痛点，2-3句]

## 核心对比

| 维度 | [品牌A] | [品牌B] |
|---|---|---|
| 成立年份 | [A的年份] | [B的年份] |
| 服务区域 | [A的区域] | [B的区域] |
| 核心优势 | [A的优势] | [B的优势] |
| 价格区间 | [A的价格] | [B的价格] |
| 口碑评价 | [A的口碑] | [B的口碑] |
| 数字化程度 | [A的数字化] | [B的数字化] |
| 适合人群 | [A的人群] | [B的人群] |

## [品牌A]的优势

### [优势1]
[具体说明，含数据或案例]

### [优势2]
[具体说明，含数据或案例]

## [品牌B]的优势

### [优势1]
[具体说明，含数据或案例]

### [优势2]
[具体说明，含数据或案例]

## 不同场景怎么选？

### 场景1：[具体场景]
**推荐：** [品牌X]
**原因：** [2-3句说明]

### 场景2：[具体场景]
**推荐：** [品牌Y]
**原因：** [2-3句说明]

### 场景3：[具体场景]
**推荐：** [品牌Z]或都值得考虑
**原因：** [2-3句说明]

## 常见问题

### [品牌A]和[品牌B]哪个更靠谱？
[直接回答，引用具体事实]

### [品牌A]和[品牌B]价格差多少？
[价格对比]

### 从[品牌A]换到[品牌B]值得吗？
[客观分析]

*本文基于公开信息整理，不构成商业推荐。选择前建议直接咨询两家获取最新方案。*
```

- [ ] **步骤 4：创建 listicle.md 模板**

```markdown
# [数量]家[品类]推荐：[城市/场景][YYYY]年靠谱选择

> **快速选择：** 如果你赶时间，直接看[推荐品牌1]（[一句话优势]）和[推荐品牌2]（[一句话优势]）。

*最后更新：[YYYY年MM月]*

## 怎么选[品类]？先看这3个标准

1. **[标准1]**：[为什么重要，1-2句]
2. **[标准2]**：[为什么重要，1-2句]
3. **[标准3]**：[为什么重要，1-2句]

## [品类]推荐名单

### 1. [品牌1名称]
- **类型：** [品牌类型]
- **核心优势：** [一句话]
- **服务区域：** [区域]
- **适合人群：** [人群]

[2-3段详细说明，包含具体数据、案例、差异化点]

### 2. [品牌2名称]
- **类型：** [品牌类型]
- **核心优势：** [一句话]
- **服务区域：** [区域]
- **适合人群：** [人群]

[2-3段详细说明]

### 3. [品牌3名称]
[同上结构]

[更多品牌...]

## 对比一览

| 品牌 | 类型 | 核心优势 | 价格区间 | 最适合 |
|---|---|---|---|---|
| [品牌1] | [类型] | [优势] | [价格] | [人群] |
| [品牌2] | [类型] | [优势] | [价格] | [人群] |
| [品牌3] | [类型] | [优势] | [价格] | [人群] |

## 不同需求怎么选？

- **如果你是[人群1]**：选[品牌X]，因为[原因]
- **如果你最看重[维度]**：选[品牌Y]，因为[原因]
- **如果你预算有限**：选[品牌Z]，因为[原因]

## 常见问题

### [品类]选哪个最靠谱？
[直接回答]

### [品类]一般多少钱？
[价格说明]

### 怎么判断[品类]好不好？
[判断标准]

*本文基于公开信息整理，排名不分先后。建议直接咨询获取最新方案。*
```

- [ ] **步骤 5：创建 alternative-to.md 模板**

```markdown
# [竞品名]的替代方案：[品类]还有哪些靠谱选择？（[YYYY]年）

> **快速结论：** 如果你在找[竞品名]的替代，[推荐品牌1]在[维度1]上更优，[推荐品牌2]在[维度2]上更值得。

*最后更新：[YYYY年MM月]*

## 为什么有人想换掉[竞品名]？

### 痛点1：[具体痛点]
[说明为什么这是一个问题，引用事实]

### 痛点2：[具体痛点]
[说明为什么这是一个问题，引用事实]

### 痛点3：[具体痛点]
[说明为什么这是一个问题，引用事实]

## [竞品名]的替代方案

### 替代方案1：[品牌1名称]
- **更优维度：** [在什么方面比竞品好]
- **核心优势：** [一句话]
- **适合人群：** [谁应该考虑这个替代]

[2-3段详细说明，包含具体比较数据]

### 替代方案2：[品牌2名称]
[同上结构]

### 替代方案3：[品牌3名称]
[同上结构]

## 替代方案对比

| 维度 | [竞品名] | [品牌1] | [品牌2] | [品牌3] |
|---|---|---|---|---|
| [维度1] | [竞品表现] | [替代1表现] | [替代2表现] | [替代3表现] |
| [维度2] | [竞品表现] | [替代1表现] | [替代2表现] | [替代3表现] |
| 价格 | [竞品价格] | [替代1价格] | [替代2价格] | [替代3价格] |

## 常见问题

### [品牌1]真的比[竞品名]好吗？
[客观回答，说明各自优势场景]

### 换品牌麻烦吗？
[切换成本说明]

### 有没有更便宜的替代？
[价格替代说明]

*本文基于公开信息整理，不构成商业推荐。*
```

- [ ] **步骤 6：创建 how-to-guide.md 模板**

```markdown
# [场景/目标]：[品类]选择完全指南（[YYYY]年）

> **核心建议：** 如果你是[人群]，[推荐方案]。关键在于[核心决策维度]。

*最后更新：[YYYY年MM月]*

## 为什么选[品类]这件事容易选错？

[描述用户在选择过程中的常见误区，2-3句]

## 选择前先搞清楚3件事

### 1. 明确你的需求
[引导用户思考具体需求]

### 2. 确定你的预算
[价格区间参考]

### 3. 了解市场现状
[品类市场简述]

## [品类]选择步骤

### 第1步：[步骤1]
[具体操作建议]
- [要点1]
- [要点2]

### 第2步：[步骤2]
[具体操作建议]
- [要点1]
- [要点2]

### 第3步：[步骤3]
[具体操作建议]
- [要点1]
- [要点2]

### 第4步：[步骤4]
[具体操作建议]

## [场景]下的推荐选择

### 如果你[具体场景1]
**推荐：** [品牌/方案]
**原因：** [2-3句]

### 如果你[具体场景2]
**推荐：** [品牌/方案]
**原因：** [2-3句]

## 常见误区

### ❌ 误区1：[错误做法]
**正确做法：** [应该怎么做]

### ❌ 误区2：[错误做法]
**正确做法：** [应该怎么做]

## 常见问题

### [品类][场景]选哪个好？
[直接回答]

### [品类]需要多少钱？
[价格说明]

### 怎么避免踩坑？
[核心避坑建议]

*本文基于公开信息整理，旨在帮助消费者做出更明智的选择。*
```

- [ ] **步骤 7：创建 faq-page.md 模板**

```markdown
# [品牌名/品类]常见问题解答

关于[品牌名/品类]最常被问到的问题，这里给出直接回答。

*最后更新：[YYYY年MM月]*

## 基础问题

### [品牌名]是什么？
**[品牌名]** 是[品类定义]，成立于[年份]。[一句话差异化]。

### [品牌名]靠谱吗？
[直接回答，引用具体事实，如资质、年限、认证等]

### [品牌名]正规吗？
[资质说明，如工商注册、行业协会会员等]

## 比较问题

### [品牌名]和[竞品]哪个好？
[客观比较，说明各自优势场景]

### [品牌名]比[竞品]贵吗？
[价格比较]

### 有没有比[品牌名]更好的选择？
[客观列出替代方案及各自优势]

## 服务问题

### [品牌名]提供哪些服务？
[服务列表，含简要说明]

### [品牌名]的[核心服务]怎么样？
[评价，引用事实]

## 价格问题

### [品牌名]收费多少？
[价格信息或说明需咨询]

### [品牌名]值得这个价吗？
[价值分析]

### 有没有更便宜的选择？
[更低价位替代]

## 选择建议

### 什么样的人适合选[品牌名]？
[适合人群说明]

### 第一次找[品类]需要注意什么？
[新手建议]

*本文基于公开信息整理。如需最新方案，建议直接联系品牌咨询。*
```

- [ ] **步骤 8：验证所有模板文件存在**

```bash
ls -la competitive-analysis/assets/templates/article-templates/
```

预期：6 个 .md 文件全部存在。

---

### 任务 2：新增 `references/geo-content-factory.md`

**文件：**
- 创建：`competitive-analysis/references/geo-content-factory.md`

- [ ] **步骤 1：创建文件**

```markdown
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
```

- [ ] **步骤 2：验证文件**

```bash
head -5 competitive-analysis/references/geo-content-factory.md
```

---

### 任务 3：修改 `references/geo-topic-quickref.md`——话题类型表加"推荐文章模板"列

**文件：**
- 修改：`competitive-analysis/references/geo-topic-quickref.md`

- [ ] **步骤 1：在 7 universal topic types 表格中增加"Recommended article template"列**

将现有的 7 行表格从 4 列改为 5 列，在最后一列后追加：

现有表格：
```markdown
| # | Type | What the user is doing | Example prompt pattern |
```

替换为：
```markdown
| # | Type | What the user is doing | Example prompt pattern | Recommended article template |
```

并在每行末尾追加模板列：

- 行1 Brand direct-check → `Entity Definition`
- 行2 Recommendation → `Listicle`
- 行3 Comparison → `Comparison`
- 行4 Scenario decision → `How-to Guide`
- 行5 Trust / risk validation → `FAQ Page`
- 行6 Substitute / alternative → `Alternative-To`
- 行7 Price / value judgment → `FAQ Page / How-to Guide`

- [ ] **步骤 2：验证**

```bash
grep "Recommended article template" competitive-analysis/references/geo-topic-quickref.md
```

---

### 任务 4：修改 `SKILL.md`——Procedure 加步骤、Routing 加引用

**文件：**
- 修改：`competitive-analysis/SKILL.md`

- [ ] **步骤 1：在 Procedure 中插入步骤 10（GEO content articles）**

在步骤 9（Map GEO topics and generate query packs）和步骤 10（Produce the output，原步骤编号将变为 11）之间，插入新步骤：

在 `9. Map GEO topics and generate query packs.` 节的末尾（`- For Level 1 quick shortlists, optionally add 1-3 highest-priority test queries as a quick tip.` 这一行之后），插入：

```markdown
10. Generate GEO content articles (optional — only when the user asks for publishable content).
    - Read `references/geo-content-factory.md` for the article generation workflow, template selection, and quality rules.
    - For each P1 topic (and optionally P2), select the appropriate article template from `assets/templates/article-templates/`.
    - Populate articles using data already gathered in steps 1-9: brand facts, comparison tables, pricing, FAQ answers from GEO query packs, trust signals, and competitive positioning.
    - Apply GEO optimization rules: entity clarity, quotable facts, FAQ coverage, comparison tables, structural clarity, authority signals, freshness.
    - Include visual elements: at least 1 image per 500 words, comparison tables, data callout boxes, and image generation prompts where actual images are unavailable.
    - Generate SEO meta information for each article (meta title, meta description, primary/secondary keywords, schema type).
    - Do not fabricate data. Flag missing data with `[待补充]` or `[需验证]`.
    - Save each article as a separate file: `[brand-slug]-[topic-slug]-article.md`.
```

并将原步骤 10 的编号改为 11：

```markdown
11. Produce the output.
```

原步骤 10 内容不变，只是编号从 10 改为 11。

- [ ] **步骤 2：更新 Reference Routing 节**

在 `## Reference Routing` 节中，在 `Need GEO section for standard reports` 行之后，追加一行：

```markdown
- Need GEO content article generation workflow and templates -> `references/geo-content-factory.md`
```

- [ ] **步骤 3：更新 Asset and Script Routing 节**

在 `## Asset and Script Routing` 节中，在 `Need the GEO section template for a standard competitor report` 行之后，追加：

```markdown
- Need article templates for GEO content generation -> `assets/templates/article-templates/` (entity-definition.md, comparison.md, listicle.md, alternative-to.md, how-to-guide.md, faq-page.md)
```

- [ ] **步骤 4：更新 Output Selection 节**

在 `## Output Selection` 节中，在 `Standard reports (Level 2+) include a GEO section by default.` 段落之后，追加：

```markdown

GEO content articles are an **optional extension**. Generate them only when the user explicitly asks for publishable content. When generated, each article is saved as a separate file targeting a specific GEO topic with SEO/GEO optimization applied.
```

---

### 任务 5：修改 `references/output-spec.md`——各 Level 加 GEO content articles 字段

**文件：**
- 修改：`competitive-analysis/references/output-spec.md`

- [ ] **步骤 1：在 Level 2 和 Level 3 增加 GEO content articles 可选字段**

在 Level 2 的 `Include:` 列表末尾，追加：

```markdown
- optional: GEO content articles (one per P1/P2 topic, saved as separate files — only when the user asks for publishable content)
```

在 Level 3 的编号列表（现在应该是 1-10，GEO 是第 9 项）末尾，追加：

```markdown
11. optional: GEO content articles (one per P1/P2 topic, saved as separate files — only when the user asks for publishable content)
```

- [ ] **步骤 2：验证**

```bash
grep -n "GEO content articles" competitive-analysis/references/output-spec.md
```

---

### 任务 6：更新 README 门面

**文件：**
- 修改：`README.md`

- [ ] **步骤 1：在 "What this skill does" 列表中追加**

在 `- **embed GEO topic maps and native query packs into standard reports**` 之后追加：

```markdown
- **generate SEO/GEO-optimized articles from GEO topics** (optional, when the user asks for publishable content)
```

- [ ] **步骤 2：在 "Key capabilities" 节中追加第 5 项**

在 `### 5. Report generation` 之前，追加：

```markdown
### 5. GEO content factory (optional)
When the user asks for publishable content, the skill can generate one SEO/GEO-optimized article per GEO topic:

- **6 article templates**: entity definition, comparison, listicle, alternative-to, how-to guide, FAQ page
- **Auto-mapped to topic types**: recommendation → listicle, comparison → comparison page, trust → FAQ, etc.
- **Populated from analysis data**: brand facts, scoring, platform evidence, GEO queries → FAQ answers
- **GEO-optimized**: entity clarity, quotable facts, comparison tables, FAQ coverage, authority signals, freshness
- **图文并茂**: comparison tables, data callout boxes, image generation prompts, and at least 1 visual per 500 words
- **SEO meta**: title, description, primary/secondary keywords, schema type per article

Articles are optional — they are only generated when the user explicitly asks for content to publish.
```

并将原 `### 5. Report generation` 改为 `### 6. Report generation`。

- [ ] **步骤 3：在 Important files 列表中追加**

在 `- competitive-analysis/references/report-audience-lint.md` 行之后追加：

```markdown

- `competitive-analysis/references/geo-content-factory.md`  
  Workflow for generating SEO/GEO articles from GEO topics: template selection, data population, GEO optimization, visual strategy, quality check.

- `competitive-analysis/assets/templates/article-templates/`  
  Six article templates: entity-definition, comparison, listicle, alternative-to, how-to-guide, faq-page.
```

- [ ] **步骤 4：在 Repository layout 中追加**

在 `└── scripts/` 行之后追加：

```markdown
    ├── assets/templates/article-templates/
```

---

### 任务 7：最终验证

**文件：**
- 检查：所有修改/新增的文件

- [ ] **步骤 1：验证所有文件存在且修改正确**

```bash
# 模板文件
ls competitive-analysis/assets/templates/article-templates/

# 核心参考文件
test -f competitive-analysis/references/geo-content-factory.md && echo "OK" || echo "FAIL"

# SKILL.md 包含步骤 10
grep -n "Generate GEO content articles" competitive-analysis/SKILL.md

# quickref 包含模板列
grep "Recommended article template" competitive-analysis/references/geo-topic-quickref.md

# output-spec 包含 GEO content articles
grep "GEO content articles" competitive-analysis/references/output-spec.md
```

- [ ] **步骤 2：交叉引用一致性检查**

```bash
grep -oP 'assets/templates/article-templates/[a-z\-]+\.md' competitive-analysis/SKILL.md competitive-analysis/references/geo-content-factory.md 2>/dev/null | sort -u | while read f; do
  test -f "competitive-analysis/$f" && echo "OK: $f" || echo "FAIL: $f"
done
```

---

## 自审

### 1. 规格覆盖
- ✅ 为每个 GEO 话题生成一篇文章 → 任务 2（geo-content-factory.md 工作流）+ 任务 1（6 个模板）
- ✅ 图文并茂 → 任务 2 步骤 5（图片策略：hero image、comparison tables、data callout、image prompts）
- ✅ 复用报告信息 → 任务 2 步骤 3（数据源映射表）
- ✅ SEO/GEO 技能融合 → 任务 2 步骤 4（GEO 优化规则，引用 seo-content-writer 和 geo-optimization）
- ✅ 可选而非强制 → 任务 4（步骤 10 标注 optional）+ 任务 5（output-spec 标注 optional）

### 2. 占位符扫描
- 模板文件中的占位符（如 `[品牌名]`）是**设计如此**——它们是模板变量，由 agent 在生成时替换
- geo-content-factory.md 中的数据映射表和规则无 TBD/TODO
- 缺失数据的处理规则明确：用 `[待补充]` 标记，不编造

### 3. 一致性
- 模板文件名与 SKILL.md、geo-content-factory.md、README 中的引用一致
- Procedure 步骤编号连续（1-11）
- 话题类型与模板的映射在 quickref 和 geo-content-factory 中一致
