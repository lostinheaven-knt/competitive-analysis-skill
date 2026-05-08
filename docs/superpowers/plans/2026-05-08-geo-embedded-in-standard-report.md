# 竞品报告内嵌 GEO 话题与 Query 推荐 实现计划

**目标：** 将 GEO 从独立报告模式升级为标准竞品报告的标配章节（Level 2+），同时保留独立深度 GEO 报告的向后兼容性。

**架构：** 在现有竞品分析流程的第 8 步（审核短表）和第 9 步（产出报告）之间插入"GEO 话题地图与 query 包生成"步骤；新增 `references/geo-topic-quickref.md` 速查文件供标准报告流程使用；修改 `SKILL.md`、`output-spec.md`、`report-outline.md` 三个核心文件，微调 `geo-report.md` 头部说明。所有 GEO 内容均标注为"基于竞品分析的推演建议"，不装成实证数据。

**技术栈：** Markdown 文档编辑，无代码变更（无 Python 脚本改动）。

---

## 文件结构

| 文件 | 操作 | 职责 |
|---|---|---|
| `competitive-analysis/SKILL.md` | 修改 | Report Modes 重写、Procedure 加步骤、Reference/Asset Routing 加路由、Checks 加 GEO 检查项 |
| `competitive-analysis/references/output-spec.md` | 修改 | Level 1/2/3/4 各级增加 GEO 章节定义 |
| `competitive-analysis/references/geo-topic-quickref.md` | **新增** | 精简速查版：7 大话题类型 + query 写法规则 + 优先级判定 + 占位判断 4 分法 |
| `competitive-analysis/assets/templates/report-outline.md` | 修改 | 在 Recommended Next Steps 前加 GEO 话题与 Query 章节模板 |
| `competitive-analysis/references/geo-report.md` | 微调 | 头部加"深度 GEO 专用"路由说明 |

不改的文件：
- `geo-generalization-memo.md`：历史设计备忘，不动
- `assets/templates/geo-report-outline.md`：独立 GEO 报告模板保留
- `references/geo-report.md` 的主体内容：保留，不删不改
- 所有样例报告文件：不动
- `scripts/` 目录：不动

---

### 任务 1：新增 `references/geo-topic-quickref.md`

**文件：**
- 创建：`competitive-analysis/references/geo-topic-quickref.md`

- [ ] **步骤 1：创建文件并写入完整内容**

```markdown
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
```

- [ ] **步骤 2：验证文件内容完整性**

运行：`cat competitive-analysis/references/geo-topic-quickref.md | head -5`
预期：文件头部为 `# GEO Topic Quick Reference`

- [ ] **步骤 3：Commit**

```bash
cd ~/.openclaw/workspace_coder/competitive-analysis-skill
git add competitive-analysis/references/geo-topic-quickref.md
git commit -m "feat: add geo-topic-quickref.md for standard report GEO section"
```

---

### 任务 2：修改 `references/output-spec.md`——各 Level 增加 GEO 章节

**文件：**
- 修改：`competitive-analysis/references/output-spec.md`

- [ ] **步骤 1：在 Level 1 增加 GEO 可选字段**

在 Level 1 的 `Include:` 列表末尾，`brief note on scope and uncertainty` 之后，追加一行：

```markdown
- optional: 1-3 highest-priority GEO test queries as a quick tip
```

- [ ] **步骤 2：在 Level 2 增加 GEO 必选章节**

在 Level 2 的 `Include:` 列表末尾，`risks or limitations` 之后，追加：

```markdown
- GEO topic and query section:
  - compact topic map (topic name / type / priority / one-line significance)
  - P1 topic query packs (3-5 queries per P1 topic)
  - brand position judgment per topic (default recommendation / candidate / defensive / replaceable)
  - key competitor GEO pressure
  - recommended GEO actions (what content, proof, or comparison pages to prepare)
```

- [ ] **步骤 3：在 Level 3 增加 GEO 必选章节**

在 Level 3 的编号列表 `9. Recommended next steps` 之前，插入新编号项：

```markdown
9. GEO topic and query recommendations
   - full topic map
   - P1 and P2 topic packs with query packs (3-5 queries per topic)
   - brand position judgment per topic
   - competitor GEO pressure summary
   - recommended GEO actions
   - priority test query list (P1 / P2 / P3)
```

原 `9. Recommended next steps` 改为 `10. Recommended next steps`。

- [ ] **步骤 4：在 Level 4 增加 GEO 监测字段**

在 Level 4 的 `Include:` 列表末尾，`fields to monitor over time` 之后，追加：

```markdown
- GEO monitoring queries (queries to re-run periodically in LLMs to track brand visibility changes)
```

- [ ] **步骤 5：在 Quality rule 节末尾追加 GEO 诚实标注规则**

在 `## Quality rule` 节的现有内容之后，追加：

```markdown

## GEO data honesty rule
All GEO content in standard competitor reports is inference-based, derived from competitive analysis and general topic frameworks. It is not empirically tested against real LLM outputs.

When writing the GEO section:
- Frame judgments as "based on competitive analysis, the brand is likely to..." rather than "verified to..."
- Do not present query packs as search volume data or empirical evidence
- State clearly that the GEO section provides "topics and queries worth testing" rather than "tested results"
- If the user needs empirical GEO data, recommend running the query packs against actual LLM APIs separately
```

- [ ] **步骤 6：验证修改结果**

运行：`grep -n "GEO" competitive-analysis/references/output-spec.md`
预期：应看到 Level 1/2/3/4 各有 GEO 相关行，以及 `GEO data honesty rule` 节标题。

- [ ] **步骤 7：Commit**

```bash
cd ~/.openclaw/workspace_coder/competitive-analysis-skill
git add competitive-analysis/references/output-spec.md
git commit -m "feat: add GEO section to all output levels in output-spec"
```

---

### 任务 3：修改 `assets/templates/report-outline.md`——增加 GEO 章节模板

**文件：**
- 修改：`competitive-analysis/assets/templates/report-outline.md`

- [ ] **步骤 1：在 `# Key Findings` 和 `# Risks and Limitations` 之间插入 GEO 章节**

在 `# Key Findings` 节之后、`# Risks and Limitations` 节之前，插入以下完整内容：

```markdown
# GEO 话题与 Query 推荐

> **注：** 本章节基于竞品分析推演，提供"值得探测的话题与 query"，非实证数据。建议将 query 包实际投入 GPT / 豆包 / DeepSeek / Kimi 测试以获取真实占位数据。

## 话题地图

| 话题 | 类型 | 优先级 | 对品牌的意义 |
|---|---|---:|---|
|  |  |  |  |

## P1 话题 Query 包

### [话题 1 名称]
- 占位判断：
- 核心竞品压力：
- query：
  -
  -
  -
- 建议 GEO 动作：

### [话题 2 名称]
- 占位判断：
- 核心竞品压力：
- query：
  -
  -
  -
- 建议 GEO 动作：

## P2 话题 Query 包

### [话题 3 名称]
- 占位判断：
- 核心竞品压力：
- query：
  -
  -
- 建议 GEO 动作：

## 关键 GEO 竞争压力
- 品牌更容易被推荐的场景：
- 品牌容易吃亏的场景：
- 最可能抢默认推荐位的竞品：

## 建议 GEO 动作
- 补比较内容：
- 补信任证据：
- 补场景内容：
- 补价值/价格解释：

## 优先测试 Query 清单
- P1：
  -
  -
- P2：
  -
- P3：
  -
```

- [ ] **步骤 2：验证修改结果**

运行：`grep -n "GEO" competitive-analysis/assets/templates/report-outline.md`
预期：应看到 `# GEO 话题与 Query 推荐`、`## 话题地图`、`## P1 话题 Query 包`、`## 关键 GEO 竞争压力`、`## 建议 GEO 动作`、`## 优先测试 Query 清单` 等标题。

- [ ] **步骤 3：Commit**

```bash
cd ~/.openclaw/workspace_coder/competitive-analysis-skill
git add competitive-analysis/assets/templates/report-outline.md
git commit -m "feat: add GEO section template to standard report outline"
```

---

### 任务 4：修改 `SKILL.md`——Report Modes、Procedure、Routing、Checks

**文件：**
- 修改：`competitive-analysis/SKILL.md`

- [ ] **步骤 1：重写 Report Modes 节**

将 `## Report Modes` 节的完整内容替换为：

```markdown
## Report Modes
Choose the mode explicitly based on the user request:
- **Standard competitor mode** (default): identify, filter, score, summarize competitors, and include a GEO topic and query section in the output (Level 2+).
- **GEO-only mode**: produce a standalone deep GEO report. Use when the user explicitly asks for a separate GEO report or deep GEO analysis. Read `references/geo-report.md` for this mode.

Standard mode includes GEO by default. You do not need a separate request to add GEO content to a competitor report.

GEO content in standard reports is inference-based (derived from competitive analysis), not empirically tested. Frame it as "topics and queries worth testing" rather than "tested results".

When writing GEO content (standard or GEO-only mode):
- Keep the method cross-industry and avoid promoting sample-specific industry rules into the main skill body.
- Prefer topic types like recommendation, comparison, trust validation, scenario decision, substitute, and price/value judgment.
- Write queries as natural user prompts for GPT / 豆包 / DeepSeek / Kimi rather than SEO-style keyword strings.
- For standard reports, read `references/geo-topic-quickref.md` for the condensed topic taxonomy, query rules, and priority logic.
- For GEO-only deep reports, use `assets/templates/geo-report-outline.md`.
- Keep case-specific query nuances in the report or references, not in the core skill rules.

For sample-driven skill updates, apply a contamination check before generalizing:
1. Would this rule still hold in another industry?
2. Can it be expressed with variables like `[brand]`, `[competitor]`, `[scenario]`, `[risk]`, or `[user goal]`?
3. Is it a GEO method rule rather than a market-specific insight?
If not, keep it out of the main skill body.
```

- [ ] **步骤 2：重写 Output Selection 节**

将 `## Output Selection` 节的完整内容替换为：

```markdown
## Output Selection
Use `references/output-spec.md` for standard competitor outputs.
Use `references/geo-topic-quickref.md` for the GEO section within standard reports.
Use `references/geo-report.md` plus `assets/templates/geo-report-outline.md` for standalone deep GEO deliverables.
For any reader-facing deliverable, also read `references/report-audience-lint.md` before finalizing.

Standard reports (Level 2+) include a GEO section by default. The GEO section in standard reports covers:
1. Compact topic map
2. P1 (and P2 for Level 3) topic packs with query packs
3. Brand position judgment per topic
4. Key competitor GEO pressure
5. Recommended GEO actions
6. Priority test query list

For standalone deep GEO reports, use the 10-section structure defined in `references/geo-report.md`.

If evidence is thin, narrow the confidence and state only reader-relevant business limits or research gaps.
Do not include internal workflow, skill-maintenance, maturity-stage, or sample-generalization commentary in formal client-facing reports unless the user explicitly asks for methodology documentation.
Run the reader-facing output through `references/report-audience-lint.md` before delivery.
```

- [ ] **步骤 3：在 Procedure 中插入 GEO 生成步骤**

在步骤 8（Review the shortlist）和步骤 9（Produce the output）之间，插入新的步骤 9，原步骤 9 改为步骤 10：

将：

```markdown
9. Produce the output.
   - Read `references/output-spec.md` for output level and format.
   - Include: shortlist, reasons, evidence quality, scoring logic, risks, and next steps.
   - When evidence is incomplete, say so plainly.
   - For Level 3 formal reports, use `assets/templates/report-outline.md` or generate the same structure with `scripts/generate_report_outline.py`.
   - For every shortlisted competitor, include name, competitor type, inclusion reason, major evidence points, major uncertainty points, and score or ranking logic.
```

替换为：

```markdown
9. Map GEO topics and generate query packs.
   - Read `references/geo-topic-quickref.md` for the condensed topic taxonomy, query rules, and priority logic.
   - Based on the competitive context already gathered, identify which of the 7 universal topic types are most relevant for the target brand.
   - Build a compact topic map: topic name, type, priority, one-line significance.
   - Generate native query packs for P1 topics (3-5 queries each), and P2 topics for Level 3 reports.
   - Judge brand position per topic using the 4-level scale (default recommendation / candidate / defensive / replaceable).
   - Identify key competitor GEO pressure: which competitors are most likely to outrank the target in each topic.
   - Recommend GEO actions: what content, comparison pages, trust signals, or scenario-specific material the brand should prepare.
   - Frame all GEO content as inference-based ("based on competitive analysis, the brand is likely to..."), not empirically tested.
   - For Level 1 quick shortlists, optionally add 1-3 highest-priority test queries as a quick tip.

10. Produce the output.
    - Read `references/output-spec.md` for output level and format.
    - Include: shortlist, reasons, evidence quality, scoring logic, GEO section, risks, and next steps.
    - When evidence is incomplete, say so plainly.
    - For Level 3 formal reports, use `assets/templates/report-outline.md` or generate the same structure with `scripts/generate_report_outline.py`.
    - For every shortlisted competitor, include name, competitor type, inclusion reason, major evidence points, major uncertainty points, and score or ranking logic.
    - Ensure the GEO section is included for Level 2+ reports. For Level 1, include GEO quick tip if it adds value.
```

- [ ] **步骤 4：更新 Fast Triage 节**

将 `## Fast Triage` 节中的 GEO 相关行：

```markdown
- If the user wants a GEO / generative-engine version, read `references/geo-report.md` after you have enough competitive context to map topics and query packs.
```

替换为：

```markdown
- If the user wants a GEO / generative-engine version, or if the standard report already includes competitive context, read `references/geo-topic-quickref.md` for the GEO section. For a standalone deep GEO report, read `references/geo-report.md` instead.
```

- [ ] **步骤 5：更新 Reference Routing 节**

在 `## Reference Routing` 节中，将 GEO 路由行：

```markdown
- Need GEO mode, topic maps, native query packs, or AI-answer visibility guidance -> `references/geo-report.md`
```

替换为：

```markdown
- Need GEO section for standard reports (topic map, query packs, brand position) -> `references/geo-topic-quickref.md`
- Need standalone deep GEO report (full 10-section structure) -> `references/geo-report.md`
```

- [ ] **步骤 6：更新 Asset and Script Routing 节**

在 `## Asset and Script Routing` 节中，在 `Need a formal GEO report scaffold` 行之前，插入一行：

```markdown
- Need the GEO section template for a standard competitor report -> embedded in `assets/templates/report-outline.md` (GEO 话题与 Query 推荐 section)
```

- [ ] **步骤 7：更新 Checks 节**

在 `## Checks` 节的列表末尾追加两项：

```markdown
- The GEO section is present for Level 2+ reports (or a quick tip for Level 1).
- GEO content is framed as inference-based, not empirically tested.
```

- [ ] **步骤 8：更新 Failure Modes 节**

在 `## Failure Modes` 节的列表末尾追加一项：

```markdown
- Omitting the GEO section in a Level 2+ report, or treating GEO inference as empirical data
```

- [ ] **步骤 9：验证修改结果**

运行：`grep -n "GEO" competitive-analysis/SKILL.md | head -30`
预期：应看到 Report Modes、Output Selection、Procedure 步骤 9、Fast Triage、Reference Routing、Asset Routing、Checks、Failure Modes 各处都有 GEO 相关行。

- [ ] **步骤 10：Commit**

```bash
cd ~/.openclaw/workspace_coder/competitive-analysis-skill
git add competitive-analysis/SKILL.md
git commit -m "feat: embed GEO as standard report section in SKILL.md"
```

---

### 任务 5：微调 `references/geo-report.md`——加"深度 GEO 专用"路由说明

**文件：**
- 修改：`competitive-analysis/references/geo-report.md`

- [ ] **步骤 1：在文件头部（`# GEO Report Reference` 标题之后、`Use this reference when` 之前）插入路由说明**

插入以下内容：

```markdown
> **Routing note:** This file is for **standalone deep GEO reports** only. If you are adding a GEO section to a standard competitor report (Level 2+), use `references/geo-topic-quickref.md` instead — it is shorter and tailored for embedded use.

```

- [ ] **步骤 2：在 `## When to use GEO mode` 节末尾追加说明**

在 `Do **not** force GEO mode when the user only wants a normal competitor shortlist.` 之后追加：

```markdown

Note: Standard competitor reports (Level 2+) now include a GEO section by default. You only need this full GEO mode when the user explicitly asks for a standalone deep GEO report, or when the GEO analysis needs to be much deeper than what a standard report section can provide.
```

- [ ] **步骤 3：验证修改结果**

运行：`head -10 competitive-analysis/references/geo-report.md`
预期：前几行应包含 `Routing note` 和 `standalone deep GEO reports` 字样。

- [ ] **步骤 4：Commit**

```bash
cd ~/.openclaw/workspace_coder/competitive-analysis-skill
git add competitive-analysis/references/geo-report.md
git commit -m "docs: add routing note to geo-report.md clarifying deep GEO vs standard report GEO"
```

---

### 任务 6：最终验证与清理

**文件：**
- 检查：所有修改过的文件

- [ ] **步骤 1：验证所有文件修改的一致性**

运行以下命令逐项检查：

```bash
# 检查 geo-topic-quickref.md 存在且内容正确
test -f competitive-analysis/references/geo-topic-quickref.md && echo "OK: quickref exists" || echo "FAIL: quickref missing"

# 检查 output-spec.md 包含 GEO 各级定义
grep -c "GEO" competitive-analysis/references/output-spec.md

# 检查 report-outline.md 包含 GEO 章节模板
grep -c "GEO" competitive-analysis/assets/templates/report-outline.md

# 检查 SKILL.md 包含 Procedure 步骤 9 (GEO)
grep -n "Map GEO topics" competitive-analysis/SKILL.md

# 检查 geo-report.md 包含路由说明
grep -n "Routing note" competitive-analysis/references/geo-report.md
```

预期：所有检查通过，无 FAIL。

- [ ] **步骤 2：检查交叉引用一致性**

验证 SKILL.md 的 Reference Routing 和 Asset Routing 中提到的文件路径都存在：

```bash
# 从 SKILL.md 中提取所有引用的 references/ 文件并检查存在性
grep -oP 'references/[a-z\-]+\.md' competitive-analysis/SKILL.md | sort -u | while read f; do
  test -f "competitive-analysis/$f" && echo "OK: $f" || echo "FAIL: $f missing"
done

# 从 SKILL.md 中提取所有引用的 assets/templates/ 文件并检查存在性
grep -oP 'assets/templates/[a-z\-]+\.\w+' competitive-analysis/SKILL.md | sort -u | while read f; do
  test -f "competitive-analysis/$f" && echo "OK: $f" || echo "FAIL: $f missing"
done
```

预期：所有文件存在，无 FAIL。

- [ ] **步骤 3：最终 Commit（如有遗漏修复）**

```bash
cd ~/.openclaw/workspace_coder/competitive-analysis-skill
git diff --stat
# 如果有未提交的修改，补充 commit
# git add -A && git commit -m "chore: final cleanup for GEO embedding"
```

---

## 自审

### 1. 规格覆盖
- ✅ GEO 从独立模式升级为标准报告标配章节 → 任务 4（SKILL.md Report Modes + Procedure）
- ✅ Level 2/3 报告默认包含 GEO 章节 → 任务 2（output-spec.md）
- ✅ Level 1 可选 GEO 快速提示 → 任务 2
- ✅ Level 4 包含 GEO 监测 query → 任务 2
- ✅ report-outline.md 模板增加 GEO 章节 → 任务 3
- ✅ 新增 geo-topic-quickref.md 速查 → 任务 1
- ✅ geo-report.md 微调路由说明 → 任务 5
- ✅ GEO 数据诚实标注（推演非实证）→ 任务 1 quickref + 任务 2 output-spec + 任务 4 SKILL.md Procedure
- ✅ 向后兼容：独立 GEO 报告模式保留 → 任务 4 + 任务 5
- ✅ Checks 和 Failure Modes 更新 → 任务 4

### 2. 占位符扫描
- 无 "TBD"、"TODO"、"稍后实现" 等占位符
- 所有步骤包含具体内容或代码

### 3. 类型/命名一致性
- `geo-topic-quickref.md` 在 SKILL.md 的 Reference Routing 和 Procedure 步骤 9 中引用一致
- `geo-report.md` 在 SKILL.md 的 Fast Triage、Report Modes、Output Selection、Reference Routing 中引用一致
- `report-outline.md` 在 SKILL.md 的 Asset Routing 和 Procedure 步骤 10 中引用一致
- 占位判断 4 分法在 quickref 和 output-spec 中一致：default recommendation / candidate / defensive / replaceable
