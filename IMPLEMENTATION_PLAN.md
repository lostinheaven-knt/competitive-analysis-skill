# Competitive Analysis Skill — 逐文件实现计划

## 1. 项目目标

本项目用于实现一个可复用的 AgentSkill：`competitive-analysis`。

目标不是简单整理一篇竞品分析方法论文档，而是构建一个可以被代理稳定调用的技能包，用于完成以下任务：

- 澄清竞品分析范围与约束
- 构建候选竞品池
- 基于多维指标进行筛选与评分
- 生成结构化分析结果
- 输出可复用的报告骨架、模板和数据表
- 在信息不完整时，主动提示缺失项与不确定性

该 skill 应优先适配两类典型场景：

1. B2C 品牌/产品竞品分析
2. B2B SaaS / 软件产品竞品分析

参考底稿：`/root/.openclaw/workspace_coder/docs/competitive-analysis-report.md`

---

## 2. 建议目录结构

```text
competitive-analysis-skill/
├── IMPLEMENTATION_PLAN.md
└── competitive-analysis/
    ├── SKILL.md
    ├── references/
    │   ├── scoping.md
    │   ├── source-priority.md
    │   ├── competitor-identification-methods.md
    │   ├── scoring-framework.md
    │   ├── decision-rules.md
    │   ├── output-spec.md
    │   ├── risks-and-compliance.md
    │   ├── examples-b2c.md
    │   └── examples-b2b-saas.md
    ├── scripts/
    │   ├── validate_input_scope.py
    │   ├── normalize_scores.py
    │   ├── weighted_rank.py
    │   ├── generate_report_outline.py
    │   └── candidate_table_template.py
    └── assets/
        └── templates/
            ├── candidate-list.csv
            ├── scoring-sheet.csv
            ├── report-outline.md
            └── interview-questionnaire.md
```

说明：
- `competitive-analysis-skill/` 是项目目录
- `competitive-analysis/` 是最终 skill 根目录
- `IMPLEMENTATION_PLAN.md` 是项目级规划文档，不属于 skill 包本身

---

## 3. 实施原则

### 3.1 主 skill 保持轻量
`SKILL.md` 只保留：
- 触发描述
- 主流程
- 输入要求
- 判断逻辑
- 何时读取哪个 reference
- 核验清单

不要把整篇方法论文档直接堆进 `SKILL.md`。

### 3.2 大块知识放入 references/
所有方法库、评分维度、数据来源、案例、风险说明等，统一沉到 `references/`。

### 3.3 重复计算逻辑放入 scripts/
归一化、权重计算、输入检查、报告骨架生成等应脚本化，避免代理每次临时手搓。

### 3.4 可交付物格式放入 assets/
CSV 模板、Markdown 报告模板、访谈提纲模板等，放入 `assets/templates/`。

### 3.5 明确“不确定性”与“证据来源”
该 skill 不应伪造市场份额、估值或竞品关系。对缺失数据和估算值，应显式标记。

---

## 4. skill 触发目标设计

### 4.1 skill 名称
建议名称：`competitive-analysis`

### 4.2 frontmatter description 草案

```yaml
---
name: competitive-analysis
description: Identify, screen, score, and summarize competitors using structured market constraints, public data sources, weighted evaluation models, and reusable report templates. Use when the user asks for competitor analysis, competitor discovery, market landscape comparison, feature/price/channel benchmarking, shortlist selection, or a reusable framework for evaluating competing brands, products, or companies.
---
```

### 4.3 期望触发语句样例
- 帮我做某产品的竞品分析
- 给我找 5 个核心竞品
- 做一个 SaaS 竞品研究框架
- 帮我按功能和价格比较市场上的对手
- 需要一个竞品识别和筛选的 skill

---

## 5. 逐文件实现计划

---

# A. skill 根文件

## 5.1 `competitive-analysis/SKILL.md`

### 目标
作为主入口文件，定义该 skill 的适用场景、输入要求、执行流程、引用导航和质量检查标准。

### 应包含内容

#### 1) Frontmatter
- `name`
- `description`

#### 2) Purpose
简述 skill 的核心作用：
- 识别竞品
- 筛选竞品
- 打分排序
- 输出分析结构

#### 3) Inputs / Preconditions
列出最小输入集：
- target：分析对象
- analysis_scope：分析目标
- industry：行业
- region：地域
- target_customer：用户类型
- channel：渠道类型
- price_band：价格带
- time_horizon：时间范围
- output_depth：输出深度

#### 4) Fast triage / Decision logic
根据任务类型选择执行路径：
- 用户只要“框架” → 不强制搜数据，直接给框架
- 用户要“真实名单” → 走候选池 → 初筛 → 评分 → 复核
- 用户信息不足 → 先补齐关键约束
- 用户要求正式交付 → 生成结构化报告输出

#### 5) Main procedure
建议 7 步：
1. 明确任务目标
2. 校验输入约束
3. 构建候选竞品池
4. 选择评估指标与权重方案
5. 打分排序
6. 人工复核与纠偏
7. 输出结果、风险与后续建议

#### 6) Reference routing
明确“何时读取哪个文件”：
- 范围不清 → `references/scoping.md`
- 需要判断数据可信度 → `references/source-priority.md`
- 需要构建候选池 → `references/competitor-identification-methods.md`
- 需要打分 → `references/scoring-framework.md`
- 需要定名单 → `references/decision-rules.md`
- 需要交付格式 → `references/output-spec.md`
- 涉及风险或合规 → `references/risks-and-compliance.md`
- 需要类比场景 → `references/examples-b2c.md` / `references/examples-b2b-saas.md`

#### 7) Checks
定义完成条件：
- 是否明确市场范围
- 是否列出候选池
- 是否解释筛选依据
- 是否提供来源或证据类型
- 是否说明权重方案
- 是否标记缺失数据与不确定性

#### 8) Failure modes
至少覆盖：
- 用户约束不足
- 候选与真正竞品混淆
- 数据缺失过多
- 来源冲突
- 评分模型被错误套用到不适配行业

### 完成标准
- 不超过约 250 行为佳
- 具备清晰导航性
- 不重复引用文档的大段内容

---

# B. references 设计

## 5.2 `competitive-analysis/references/scoping.md`

### 目标
定义竞品分析前的澄清框架，避免在约束不明时直接开始筛选。

### 主要内容
1. 最小输入集定义
2. 常见约束维度
3. 缺省值处理规则（未指定）
4. 不同场景的追问模板

### 应覆盖的约束维度
- 行业
- 品类/产品线
- 地域范围
- 用户群体
- 公司规模
- 渠道类型
- 价格区间
- 品牌阶段/市场地位
- 分析目标（市场、产品、价格、渠道、品牌）

### 附录建议
- 通用追问模板
- B2C 场景追问模板
- B2B SaaS 场景追问模板

### 交付形式
Markdown 文档，建议带小节和 bullet list，不需要大段议论文式写法。

---

## 5.3 `competitive-analysis/references/source-priority.md`

### 目标
规定竞品分析时可接受的数据来源、优先级与引用规范。

### 主要内容
1. 来源分级模型
2. 不同来源适合回答的问题
3. 数据冲突时的处理原则
4. 引用与证据记录格式

### 建议结构
#### 一级来源（高可信）
- 公司官网
- 财报/年报
- 招股书
- 监管披露
- 行业协会/统计局

#### 二级来源（中高可信）
- 行业研究报告
- 第三方数据平台
- 知名咨询机构报告
- 垂直行业数据库

#### 三级来源（辅助）
- 新闻报道
- 媒体采访
- 社交媒体数据
- 电商平台评论
- 社区讨论

### 需要定义的规则
- 结论优先引用一、二级来源
- 三级来源主要用于线索，不宜单独支撑强结论
- 若数据为估算，需明确说明“估算”
- 若来源冲突，应保留差异并说明原因

### 建议附表
来源等级 / 可信度 / 适用场景 / 风险说明

---

## 5.4 `competitive-analysis/references/competitor-identification-methods.md`

### 目标
提供候选竞品识别方法库，支持不同业务场景下的候选池构建。

### 主要内容
1. 定性方法
2. 定量方法
3. 混合方法
4. 方法选择建议

### 定性方法部分
- 专家访谈
- 用户调研
- 销售/渠道反馈
- 渠道观察
- 神秘顾客/产品体验

### 定量方法部分
- 市场份额分析
- 搜索热度/SEO
- 网站流量
- 电商销量/价格
- 社媒声量
- 功能/定位相似度
- 聚类或相似度算法（仅作为高级可选）

### 混合方法部分
- 先定性提名，再定量筛选
- 先功能相似，再商业竞争关系校准
- 先平台榜单，再用户群重叠校验

### 需要增加的关键内容
- 不同行业的推荐方法映射
- “什么叫真正竞品”的判断提醒
- 不要把所有替代方案都当核心竞品

---

## 5.5 `competitive-analysis/references/scoring-framework.md`

### 目标
定义可参数化的评分体系，让不同任务下的竞品筛选具备一致性和可解释性。

### 主要内容
1. 指标体系
2. 评分方式
3. 归一化方式
4. 权重方案
5. 缺失值处理
6. 场景化建议

### 建议指标类别
- 市场表现
- 增长表现
- 产品/功能能力
- 价格策略
- 渠道覆盖
- 品牌影响力
- 用户口碑
- 创新能力

### 每个指标建议说明
- 指标名称
- 定义
- 数据来源候选
- 评分方向（高好/低好）
- 是否适用于 B2C
- 是否适用于 B2B
- 是否允许估算

### 权重方案
至少提供三套预设：
- 保守型：偏市场份额/渠道稳定
- 均衡型：各维度均衡
- 激进型：偏增长/创新/产品能力

### 额外建议
增加两套行业模板：
- B2C 品牌/快消模板
- B2B SaaS 模板

### 缺失值规则
必须明确：
- 缺失值默认不等于 0
- 缺失字段需显式标记
- 可选择剔除、插补或降低置信度

---

## 5.6 `competitive-analysis/references/decision-rules.md`

### 目标
把候选池到最终名单的筛选逻辑固化成明确规则。

### 主要内容
1. 候选池规模建议
2. 初筛规则
3. 短名单规则
4. 人工复核规则
5. Watchlist 规则

### 建议规则
- 候选池：10–30 个
- 初筛后：5–12 个
- 最终核心竞品：3–7 个

### 初筛规则建议
- 行业完全不一致 → 默认排除
- 产品线不重叠 → 默认排除
- 用户群不重叠 → 降权或排除
- 仅在局部细分市场重叠 → 标为次级竞品
- 数据严重缺失 → 放入 watchlist

### 人工复核关注点
- 是否遗漏真正的市场头部对手
- 是否把“曝光高但竞争弱”的对象误判为核心竞品
- 是否把“技术替代方案”误当直接商业竞品

---

## 5.7 `competitive-analysis/references/output-spec.md`

### 目标
统一 skill 输出形式，避免每次任务产物风格飘忽。

### 建议定义 4 个输出等级

#### Level 1: 快速版
- 候选名单
- 3–5 个核心竞品
- 每个一句理由
- 不做完整评分表

#### Level 2: 标准版
- 候选池
- 初筛结果
- 简化评分表
- shortlist
- 风险说明

#### Level 3: 报告版
- 完整结构化分析报告
- 数据来源说明
- 权重与方法说明
- 推荐后续动作

#### Level 4: 监控版
- watchlist
- 持续更新字段
- 周期性监控建议

### 需规定的输出字段
- 候选名
- 分类
- 入选原因
- 核心指标
- 数据来源/证据类型
- 评分/排序
- 置信度
- 风险/备注

---

## 5.8 `competitive-analysis/references/risks-and-compliance.md`

### 目标
约束 skill 的风险边界和表达方式。

### 应包含内容
1. 数据合规提醒
2. 商业信息边界
3. 对比宣传风险
4. 证据不足时的表述规范
5. 隐私与合法性提醒

### 必须强调
- 不伪造未公开数据
- 不把猜测包装成事实
- 不声称掌握商业机密
- 不使用非法方式采集竞品信息
- 如果结果可能用于对外传播，应提示法务复核

---

## 5.9 `competitive-analysis/references/examples-b2c.md`

### 目标
提供 B2C 场景的完整示范，让 skill 在类似任务中有参考路径。

### 内容结构建议
- 输入约束
- 候选池来源
- 初筛逻辑
- 指标与权重
- shortlist 样例
- 输出报告样式

### 推荐样例领域
- 快消饮料
- 零食品牌
- 美妆或消费电子也可作为备用例子

---

## 5.10 `competitive-analysis/references/examples-b2b-saas.md`

### 目标
提供 B2B SaaS 场景示范，突出与 B2C 不同的竞品判断逻辑。

### 内容结构建议
- 输入约束
- 目标客户定义
- 功能与商业模式对比
- 候选池构建方式
- 权重示例
- shortlist 与解释

### 推荐样例领域
- HR SaaS
- CRM SaaS
- 客服系统 / 项目管理系统

---

# C. scripts 设计

## 5.11 `competitive-analysis/scripts/validate_input_scope.py`

### 目标
检查输入的竞品分析约束是否足够，并给出缺失项与推荐追问。

### 预期输入
JSON 或 Python dict，例如：

```json
{
  "target": "某 SaaS 产品",
  "industry": "HR SaaS",
  "region": "中国",
  "target_customer": "中大型企业",
  "channel": "直销+官网",
  "price_band": "中高端",
  "goal": "找核心竞品并做评分"
}
```

### 预期输出

```json
{
  "status": "ok",
  "missing_fields": [],
  "recommended_questions": []
}
```

或：

```json
{
  "status": "needs_clarification",
  "missing_fields": ["region", "price_band"],
  "recommended_questions": [
    "目标市场主要是中国、全球还是某个区域？",
    "希望比较的是哪个价格带的产品？"
  ]
}
```

### 实现要点
- 预置最小字段列表
- 支持场景化规则：B2C 和 B2B 关注字段不同
- 支持输出“可继续分析”与“必须补问”的区分

### 验证方式
- 输入完整 → 返回 ok
- 输入缺失 → 输出明确缺失项
- 不同业务场景有不同追问建议

---

## 5.12 `competitive-analysis/scripts/normalize_scores.py`

### 目标
对多源异构指标进行归一化，便于统一比较。

### 支持能力
- min-max normalization
- rank-based normalization
- 可选 z-score
- 方向控制：higher_is_better / lower_is_better

### 输入格式
CSV 或 JSON：
- candidate
- metric_name
- raw_value
- direction

### 输出格式
- candidate
- metric_name
- normalized_score
- notes

### 实现要点
- 对缺失值保留 `null`
- 对常数列做特殊处理，避免除零错误
- 对方向相反的指标做翻转

### 测试点
- 正向指标归一化正确
- 反向指标归一化正确
- 缺失值不被错误转为 0
- 常数列不会报错

---

## 5.13 `competitive-analysis/scripts/weighted_rank.py`

### 目标
基于归一化后的指标和权重方案计算综合得分，并输出排名。

### 输入
1. 指标表
2. 权重表
3. 可选场景参数（B2C/B2B/保守型/均衡型/激进型）

### 输出
- 每个竞品总分
- 各指标得分
- 排名
- 缺失值提醒
- 置信度或数据完整性提示

### 实现要点
- 支持外部权重配置
- 支持预设权重模板
- 输出时保留 breakdown，不能只给总分
- 对关键指标缺失过多的对象给出 warning

### 测试用例
- 3 个竞品 + 5 个指标 + 1 套权重
- 存在缺失值场景
- 不同权重方案导致排名变化场景

---

## 5.14 `competitive-analysis/scripts/generate_report_outline.py`

### 目标
根据输入范围、候选池和评分结果，生成标准化报告骨架。

### 输入
- 分析对象
- 分析范围
- 候选清单
- shortlist
- 评分摘要
- 输出等级

### 输出
Markdown 文档结构，例如：
- 执行摘要
- 目标与范围
- 数据来源
- 方法与权重
- 候选池说明
- shortlist
- 核心发现
- 风险与局限
- 后续建议

### 实现要点
- 支持快速版和标准版
- 对缺失数据插入提示说明
- 自动插入来源说明占位符

### 测试点
- 能生成合法 Markdown
- 标题结构稳定
- 缺失字段时有占位提示，不直接崩溃

---

## 5.15 `competitive-analysis/scripts/candidate_table_template.py`

### 目标
快速生成候选竞品数据表模板，减少手工建表成本。

### 输出表头建议
- company_name
- brand_name
- product_name
- category
- region
- target_customer
- channel
- price_band
- why_candidate
- source
- confidence
- notes

### 实现要点
- 可输出 CSV
- 可输出带示例行版本
- 可根据 B2C/B2B 场景切换字段

---

# D. assets 设计

## 5.16 `competitive-analysis/assets/templates/candidate-list.csv`

### 目标
作为候选竞品池收集模板。

### 推荐字段
- company_name
- brand_name
- product_name
- segment
- region
- target_customer
- channel
- price_band
- why_candidate
- evidence_type
- source_url_or_note
- confidence
- status

### 备注
`status` 可用于标记：candidate / shortlisted / watchlist / excluded

---

## 5.17 `competitive-analysis/assets/templates/scoring-sheet.csv`

### 目标
作为评分计算前的结构化输入模板。

### 推荐字段
- candidate
- market_score
- growth_score
- product_score
- pricing_score
- channel_score
- brand_score
- review_score
- innovation_score
- total_score
- confidence
- notes

### 备注
如果要更严谨，也可拆成“原始值表”和“归一化结果表”两份。

---

## 5.18 `competitive-analysis/assets/templates/report-outline.md`

### 目标
作为报告输出模板，供代理直接复制填充。

### 推荐章节
1. 执行摘要
2. 分析目标与范围
3. 数据来源与证据说明
4. 候选竞品池
5. 评价指标与权重
6. shortlist 与原因
7. 核心发现
8. 风险与局限
9. 后续建议

### 设计要求
- 使用占位符而非长篇示例文本
- 标明哪些部分必须附证据

---

## 5.19 `competitive-analysis/assets/templates/interview-questionnaire.md`

### 目标
支持定性调研场景，如用户访谈、专家访谈或销售访谈。

### 推荐内容
- 访谈目的
- 访谈对象
- 核心问题清单
- 竞品提名问题
- 使用体验问题
- 替代方案问题
- 价格/渠道认知问题
- 记录模板

---

## 6. 分阶段实施顺序

### Phase 1: 信息架构
先完成：
1. 创建项目目录
2. 确定 skill 名称
3. 固化目录结构
4. 完成 `SKILL.md` 大纲

### Phase 2: 文档层落地
优先完成：
1. `SKILL.md`
2. `references/scoping.md`
3. `references/source-priority.md`
4. `references/scoring-framework.md`
5. `references/decision-rules.md`

### Phase 3: 脚本与模板
优先完成：
1. `validate_input_scope.py`
2. `weighted_rank.py`
3. `report-outline.md`
4. `candidate-list.csv`

### Phase 4: 扩展与案例
再补：
1. `competitor-identification-methods.md`
2. `output-spec.md`
3. `risks-and-compliance.md`
4. B2C / B2B 案例
5. `normalize_scores.py`
6. `generate_report_outline.py`

### Phase 5: 测试与打包
- 用 3–5 个真实或模拟任务测试 skill
- 修正触发描述
- 修正引用路由
- 修正模板字段
- 最后打包为 `.skill`

---

## 7. 建议的 MVP 范围

如果先做最小可用版本，建议只做以下文件：

### 必做
- `competitive-analysis/SKILL.md`
- `references/scoping.md`
- `references/source-priority.md`
- `references/scoring-framework.md`
- `references/decision-rules.md`
- `scripts/validate_input_scope.py`
- `scripts/weighted_rank.py`
- `assets/templates/candidate-list.csv`
- `assets/templates/report-outline.md`

### 暂缓
- 高级归一化脚本
- 自动报告生成器
- 完整案例库
- 监控版输出规范

MVP 完成后，skill 已经可以支持：
- 竞品分析范围澄清
- 候选池收集
- 基础评分排序
- 标准化报告骨架输出

---

## 8. 测试计划

### 8.1 功能测试
至少覆盖以下场景：

1. B2C 快消品牌竞品分析
2. B2B SaaS 竞品分析
3. 输入缺失严重场景
4. 数据来源冲突场景
5. 用户只要框架不要真实数据场景

### 8.2 验收问题
- skill 是否能正确判断需要先澄清？
- skill 是否会要求来源和证据？
- skill 是否能输出 shortlist 及理由？
- skill 是否避免把替代方案全算作核心竞品？
- 模板是否足够支撑结构化交付？

### 8.3 非功能要求
- 输出结构稳定
- 不编造数据
- 对不确定性表述清楚
- 对行业差异敏感，不硬套统一模型

---

## 9. 后续可扩展方向

### 9.1 数据接入扩展
后续可考虑增加：
- 网络搜索结果解析
- SimilarWeb / SEO 数据导入
- 电商价格抓取适配
- 简单新闻/社媒提及抓取

### 9.2 模型扩展
- 按行业动态选择指标集
- 支持“直接竞品 / 替代方案 / 观察对象”三层分类
- 引入置信度模型

### 9.3 输出扩展
- 自动生成 Mermaid 流程图
- 自动生成对比矩阵
- 自动生成管理层摘要版本

---

## 10. 推荐下一步动作

建议实际执行顺序如下：

1. 先创建 `competitive-analysis/` skill 目录
2. 先写 `SKILL.md` 初稿
3. 再拆四个核心 reference
4. 然后补两个 MVP 脚本
5. 最后做模板和案例

如果后续继续开发，本项目可直接按本计划逐文件推进，不需要重新设计信息架构。

---

## 11. 一句话总结

这个项目最重要的，不是把“竞品分析知识”写得多全，而是把它变成：

- 可触发
- 可执行
- 可解释
- 可复用
- 可交付

的 skill 工程。

换句话说：
把参考报告从“文章”升级成“技能系统”。
