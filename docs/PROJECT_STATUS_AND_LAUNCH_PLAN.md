# AI LeetCode Coach 项目现状与上线规划

报告日期：2026-07-23  
评估基线：`main` 分支，提交 `34bc691`

## 1. 执行摘要

AI LeetCode Coach 已经从概念验证进入“可用原型”阶段：

- Chrome Manifest V3 扩展可在 LeetCode 页面显示悬浮入口并打开 Side Panel；
- 用户可以手动粘贴或通过右键选中文本发起九类辅导请求；
- FastAPI 后端已接入 DeepSeek，并通过服务层和 provider 抽象隔离；
- Python 代码可以进行 AST 静态上下文分析；
- PostgreSQL、SQLAlchemy 和 Alembic 已承载做题记录、复习计划和学习计划；
- 本地 Dashboard 可以生成计划、录入做题结果、查看到期复习和近期记录；
- 当前后端自动化测试为 23 项。

但当前产品仍是单机、单用户、本地开发形态，不能直接作为公网服务开放。主要上线阻断项是：

1. 扩展后端地址硬编码为 `http://127.0.0.1:8000`；
2. 后端没有真实身份认证和用户隔离，所有数据属于同一个 “Local learner”；
3. 没有限流、配额和成本保护，公网暴露后 DeepSeek Key 可被间接滥用；
4. 没有隐私告知、用户同意、数据导出/删除和保留策略；
5. 没有生产容器、CI/CD、监控、备份、恢复演练和安全响应流程；
6. Side Panel 的辅导行为与 Dashboard 的做题记录仍是两个割裂流程；
7. Chrome Web Store 发布材料、权限说明和数据使用披露尚未准备。

综合判断：

- 产品验证成熟度：中等，可以本地自用和演示；
- 学习闭环成熟度：中低，关键流程尚未连通；
- 工程架构成熟度：中等，分层方向正确；
- 生产运行成熟度：低；
- 当前建议发布范围：本地 Alpha；
- 当前不建议：公开 Beta、公开 API、Chrome Web Store 正式发布。

## 2. 当前产品设计

### 2.1 产品定位

产品定位清晰：它是 LeetCode 旁边的学习教练，不是题库、编辑器或在线判题系统。

核心价值不是“再提供一个聊天框”，而是把以下四个问题串成一个学习循环：

1. 今天应该练什么；
2. 当前题目应该如何思考；
3. 代码、语法或错误具体是什么意思；
4. 什么时候应该再次复习。

这个定位有明显差异化，也能避免复制题库、执行任意代码和重建 Judge 所带来的范围、版权与安全风险。

### 2.2 目标用户

当前设计最适合：

- 算法初学者和中级学习者；
- 准备技术面试的学生或开发者；
- 会写基础代码，但难以独立拆解题目或理解答案的人；
- 依赖 AI 辅助，但希望逐级获得提示而不是立即看到答案的人；
- 需要复习节奏与学习记录的人。

首发用户不应定义得过宽。建议首轮验证聚焦“使用 Python 刷 LeetCode、每周至少学习三次的初中级用户”。

### 2.3 当前核心体验

当前已经存在两条体验链路：

```text
LeetCode 页面
→ 悬浮 AI 按钮或右键选中文本
→ Side Panel
→ 选择辅导模式
→ FastAPI
→ DeepSeek
→ 显示解释
```

```text
本地 Dashboard
→ 输入可用时间并生成计划
→ 手动录入题目 URL、结果和耗时
→ PostgreSQL 保存记录
→ 确定性算法更新复习日期
→ 查看到期复习与近期历史
```

主要产品缺口是两条链路尚未闭合。用户完成一次辅导后，还要切到 Dashboard 再手动输入题目。这个摩擦会显著降低记录率，也会削弱复习系统的数据质量。

### 2.4 MVP 边界保持情况

当前实现较好地遵守了以下边界：

- 没有复制完整题库；
- 没有在线 Judge；
- 没有执行用户代码；
- 没有自动批量抓取 LeetCode；
- 没有 `<all_urls>`；
- 没有支付和社交功能；
- 没有把 DeepSeek Key 放入扩展；
- 没有让 DeepSeek 直接修改持久化状态；
- 只对 LeetCode 指定域名使用内容脚本；
- 问题文本和代码默认作为请求上下文，不自动持久化。

## 3. 当前工程现状

### 3.1 浏览器扩展

已实现：

- Manifest V3；
- Chrome 116+ Side Panel；
- toolbar action；
- LeetCode 专用悬浮按钮；
- 用户选中文本的右键菜单；
- background service worker；
- `storage.local` 作为 Side Panel 尚未就绪时的可靠交接；
- 九种辅导模式；
- Python/auto 语言选择；
- 选中行号输入；
- 安全的 DOM 文本渲染，没有直接使用 `innerHTML` 注入模型输出；
- 指定域名权限，没有通配网页权限。

当前问题：

- 后端 URL 硬编码，无法区分本地、测试和生产环境；
- 没有“完成本题并记录”入口；
- 没有当前题目身份状态，Side Panel 不知道一段代码属于哪道题；
- 没有会话历史、取消请求、超时反馈和重新生成；
- 没有扩展自动化测试与端到端浏览器测试；
- 悬浮按钮只有文字，没有正式图标与品牌资产；
- 版本发布仍是手动加载 unpacked extension；
- UI 主要为英文，和目标用户语言策略尚未统一。

### 3.2 FastAPI API 层

当前端点：

- `GET /health`
- `POST /api/v1/coach/echo`
- `POST /api/v1/coach/explain`
- `POST /api/v1/attempts`
- `GET /api/v1/reviews/due`
- `POST /api/v1/plans`
- `GET /api/v1/dashboard/summary`

优点：

- Pydantic 请求和响应模型明确；
- API、服务、LLM provider、repository 和数据库层边界基本清楚；
- 请求正文有长度限制；
- DeepSeek Key 只从后端环境变量读取；
- LLM 有超时、有限重试、空结果和异常处理；
- 复习间隔由确定性服务计算，不交给 LLM 控制。

当前问题：

- 无认证、授权和租户隔离；
- CORS 正则允许任意格式匹配的扩展来源，不适用于生产；
- 无速率限制、并发限制、每日额度和请求成本核算；
- `/health` 只报告进程存活，未覆盖数据库 readiness；
- 无统一错误码、请求 ID 和结构化生产日志；
- API 文档默认公开；
- 没有幂等键，重复点击可能写入重复 attempt；
- 没有 API 版本兼容与废弃策略；
- 自定义 `.env` 解析器功能有限，长期应改为成熟配置方案；
- 只对 LLM 层做了有限错误映射，数据库和未知异常没有统一处理。

### 3.3 应用服务与 LLM 层

已实现：

- `CoachExplanationService`
- `PythonCodeAnalysisService`
- `LearningRecordService`
- `ReviewService`
- `StudyPlanService`
- LLM provider 接口与 DeepSeek 实现；
- 集中式 prompt 与 prompt version；
- Python AST 导入、调用、标准库和行上下文识别。

当前问题：

- “progressive hint” 目前是请求模式，不是有状态的逐级提示会话；
- 没有保存用户已经看过的最高提示级别；
- 学习计划是规则分配，不是真正基于主题、难度和能力的推荐；
- `focus` 被保存，但没有实质影响计划内容；
- 新题计划项只能告诉用户去 LeetCode 选择一题，没有推荐来源；
- 没有响应质量评估、用户反馈或 prompt 回归样本；
- 没有流式输出，长回复的感知延迟较高。

### 3.4 数据库与 repository 层

当前表：

- `users`
- `problem_references`
- `attempts`
- `review_schedules`
- `study_plans`
- `study_plan_items`

优点：

- PostgreSQL 为目标数据库；
- SQLAlchemy ORM 与 Alembic migration 已建立；
- API 路由没有直接操作数据库；
- `(platform, url)` 和 `(user_id, problem_reference_id)` 有唯一约束；
- 复习状态与 attempt 分离，支持后续演进。

当前问题：

- 用户通过固定 display name 查找，不是真实身份；
- 缺少用户 email、认证主体和安全会话；
- 缺少 conversation、message、hint event、study session 和 usage 表；
- Dashboard 生成的计划刷新页面后不会重新读取；
- plan item 没有开始、完成和跳过 API；
- 没有数据导出、删除和软删除策略；
- 没有生产备份、恢复目标和 migration 回滚演练；
- Docker Compose 使用公开的开发账号密码，并把数据库端口映射到宿主机；这只适合本地开发。

### 3.5 Web Dashboard

已实现：

- 今日可用时间输入；
- 学习计划生成；
- 到期复习列表；
- 尝试结果录入；
- 最近历史与汇总数字；
- 原生 HTML/CSS/JS，无大型前端框架和额外构建链。

当前问题：

- 是本地工具页面，不是完整 Web App；
- 没有路由、登录、用户设置和错误边界；
- 没有读取已保存的当日计划；
- 没有复习日历、趋势统计和分页；
- 录入仍依赖手动复制 LeetCode URL；
- 存在字符编码显示风险，应统一检查源码和响应为 UTF-8；
- 缺少 Content Security Policy 和生产安全响应头；
- 没有可访问性、移动端和主流浏览器的系统化验收。

### 3.6 测试、交付与运维

当前状态：

- 后端有 23 项单元/API 测试；
- DeepSeek 测试使用 mock，不消耗付费调用；
- 有一次手动真实 DeepSeek smoke check；
- 有 PostgreSQL migration 和本地 Docker Compose；
- GitHub `main` 与本地同步。

主要缺口：

- 没有 GitHub Actions；
- 没有 lint、format、type check 和依赖安全扫描；
- 没有前端/扩展测试；
- 没有 Playwright 端到端测试；
- 没有后端 Dockerfile；
- 没有 staging 环境；
- 没有部署脚本或基础设施定义；
- 没有监控、告警、错误追踪和 LLM 成本监控；
- 没有数据库自动备份与恢复验证；
- 没有发布版本、变更日志和回滚方案。

## 4. 架构评价

当前分层方向正确，适合继续演进：

```text
Chrome Extension / Web Dashboard
               ↓
          FastAPI API
               ↓
      Application Services
          ↙          ↘
 DeepSeek Provider   Repositories
                         ↓
                    PostgreSQL
```

应继续保持：

- 扩展不持有模型 Key；
- API 路由只负责协议、校验与依赖注入；
- 业务规则位于 service；
- provider 只负责 LLM 通信；
- repository 只负责持久化查询；
- 复习状态只由确定性代码修改；
- LeetCode 继续负责代码编辑、执行和判题。

不建议现在引入：

- 微服务拆分；
- 消息队列；
- Kubernetes；
- 多模型智能路由；
- 多代理系统；
- 复杂前端状态管理框架；
- 向量数据库；
- 自建代码执行沙箱。

这些能力目前不会解决最关键的用户摩擦，反而会显著增加运维面。

## 5. 风险清单

### 5.1 P0：公开上线阻断

1. **用户数据串读**
   当前所有请求都映射到同一个本地用户。多人访问会共享学习记录。

2. **DeepSeek 费用滥用**
   无认证、限流和额度时，任何能访问 API 的人都可以消耗开发者 Key。

3. **HTTP 与硬编码 localhost**
   生产扩展必须使用 HTTPS API，并支持独立环境配置。

4. **隐私与同意缺失**
   用户提供的代码、网页选中文本和 URL 属于用户数据。Chrome Web Store 要求透明披露数据收集、用途和共享方式；即使数据仅在本地处理，也仍需披露。[Chrome Web Store User Data FAQ](https://developer.chrome.com/docs/webstore/program-policies/user-data-faq)

5. **第三方处理披露**
   用户输入会发送给 DeepSeek。必须在产品界面和隐私政策中清楚说明处理方、目的、保留策略和用户权利。DeepSeek 当前政策说明其开放平台下游应用的数据处理责任不由该隐私政策直接覆盖，因此本项目仍需自行建立面向终端用户的隐私规则。[DeepSeek Privacy Policy](https://cdn.deepseek.com/policies/en-US/deepseek-privacy-policy.html)

6. **无删除与退出机制**
   公开产品至少需要删除账户、删除学习记录、导出数据和撤回同意的可执行路径。

7. **无生产运行保障**
   没有备份、恢复、监控和回滚时，公开承诺持久化学习数据风险过高。

### 5.2 P1：上线前高风险

- CORS 应只允许正式扩展 ID 和正式 Web 域名；
- 必须设置 API body、并发、速率和每日成本上限；
- 应禁止日志记录完整代码和 prompt，默认只记录元数据；
- 应添加 CSP、HSTS、`X-Content-Type-Options` 等安全头；
- 应将数据库置于私有网络，不映射公开端口；
- 应轮换生产 secret，禁止复用本地数据库密码；
- 应增加依赖锁定、漏洞扫描和 secret scanning；
- 应为 LLM 请求增加可追踪但不含正文的 request ID；
- 应定义服务降级：LLM 不可用时，学习记录和复习查询仍应可用。

### 5.3 法律与平台风险

- LeetCode 条款明确禁止 crawling、scraping 和 spidering。当前用户主动选择文本的方式风险较低；任何自动读取完整题目、批量获取内容或绕过页面限制的计划都应停止并先做法律评估。[LeetCode Terms of Service](https://leetcode.com/terms/)
- 产品名称直接包含 “LeetCode”，可能产生商标、关联关系和商店审核风险。上线前应评估更中性的品牌名，并在描述中声明“独立第三方工具，与 LeetCode 无隶属或官方合作关系”。
- Chrome Web Store 要求最小权限、清晰的单一用途、准确的数据使用披露和用户同意。当前权限范围较克制，这是优势，但仍要准备隐私政策、权限理由和商店 Data Use 表单。[Chrome Web Store Program Policies](https://developer.chrome.com/docs/webstore/program-policies)
- 若面向不同司法辖区用户，应分别评估个人信息保护、跨境传输、儿童使用和数据主体权利。本报告不是法律意见，公开上线前应让专业人士审阅隐私政策和服务条款。

## 6. 下一步产品改进优先级

### Milestone A：打通学习闭环

目标：让用户无需离开 Side Panel 就能完成一次学习记录。

范围：

- Side Panel 增加“完成本题”入口；
- 允许用户主动确认当前题目标题和 URL；
- 自动预填当前标签页 URL，但不读取完整页面；
- 记录 outcome、耗时、最高提示级别、是否查看完整答案和笔记；
- 保存成功后显示下一次复习日期；
- Dashboard 和 Side Panel 读取同一条记录；
- 防止重复点击产生重复 attempt。

验收：

- 用户从打开题目到记录完成不需要切换页面；
- 一次保存后，Dashboard 历史立即可见；
- 到期日期由 `ReviewService` 计算；
- 不新增自动题目抓取权限；
- API、service、repository 和扩展交互都有测试。

这是当前最高优先级，也是验证产品价值最关键的一步。

### Milestone B：让计划真正可持续使用

目标：让计划不是一次性响应，而是可以恢复和完成的状态。

范围：

- 获取今天的最新计划；
- plan item 支持 pending、started、completed、skipped；
- Side Panel 展示今天的下一项；
- 完成 attempt 时可关联 plan item；
- Dashboard 刷新后保留计划；
- focus 至少影响计划说明或筛选逻辑。

暂不做：

- 复制题库；
- 自动推荐具体新题；
- AI 自主抓取题目；
- 复杂推荐算法。

### Milestone C：产品质量与可观测性

目标：在邀请真实用户前，能发现错误、衡量价值并控制成本。

范围：

- GitHub Actions：测试、compile、lint、migration check；
- Python formatter/linter 和基础 type check；
- 扩展消息流和 Side Panel 的 Playwright 测试；
- API 结构化日志与 request ID；
- 不记录正文的 LLM 延迟、错误率和 token/cost 指标；
- 请求取消、超时、重试提示；
- 中英文产品语言决策和 UTF-8 编码清理；
- 可访问性和窄 Side Panel 布局验收。

### Milestone D：私有 Alpha 基础设施

目标：支持少量受邀用户安全使用。

范围：

- 生产域名和 HTTPS；
- 容器化 FastAPI；
- 托管 PostgreSQL 或隔离的生产 PostgreSQL；
- 用户认证与数据隔离；
- 正式扩展 ID 和生产 API URL；
- CORS allowlist；
- 每用户限流、每日额度和总预算熔断；
- 数据备份和一次恢复演练；
- staging 与 production 分离；
- 隐私政策、服务条款、删除与导出；
- 只对受邀账号开放。

### Milestone E：Chrome Web Store Beta

目标：通过商店审核并进行可控公开测试。

范围：

- 正式品牌名、图标、截图和商店文案；
- 单一用途声明；
- 权限理由；
- Data Use 披露；
- 隐私政策公开 URL；
- 支持邮箱和问题反馈流程；
- extension package 可复现构建；
- 版本升级和回滚流程；
- 首批用户逐步放量。

## 7. 推荐上线架构

### 7.1 私有 Alpha

```text
Chrome Extension
       ↓ HTTPS
Application Load Balancer / Reverse Proxy
       ↓
FastAPI Container
   ↙          ↘
DeepSeek API   Managed PostgreSQL
       ↓
Metrics / Error Tracking / Cost Alerts
```

Web Dashboard 可以继续由 FastAPI 同域静态托管，减少首发部署复杂度。用户量和前端需求明显增长后，再考虑独立前端应用。

### 7.2 环境

至少建立：

- `local`：开发者本机、Docker PostgreSQL、开发 Key；
- `staging`：独立数据库、测试扩展版本、低额度 Key；
- `production`：正式域名、正式扩展 ID、独立 secrets 和备份。

三个环境不得共享数据库、API Key 或 cookie/session secret。

### 7.3 配置

扩展构建应注入：

- API base URL；
- environment name；
- build version；
- 可选的错误追踪环境标识。

后端应从受控 secret store 获取：

- DeepSeek API Key；
- database URL；
- authentication secret；
- observability credentials。

### 7.4 身份与访问

建议：

- 私有 Alpha 使用邀请制账号；
- Web 使用安全 session cookie；
- 扩展使用短期 access token 和可撤销 refresh/device credential；
- 所有 repository 查询强制带 `user_id`；
- 禁止继续通过 display name 推断身份；
- 管理接口与普通用户 API 分离。

## 8. 上线阶段与 Go/No-Go

### 阶段 0：本地 Dogfood

目标用户：开发者本人。  
建议周期：完成 Milestone A 和 B 后连续使用 1 至 2 周。

Go 标准：

- 侧边栏完成记录成功率高于 95%；
- 连续使用中没有丢失记录；
- 复习日期计算与预期一致；
- 不需要手动修改数据库；
- DeepSeek 错误有明确反馈；
- 每次模型调用成本可见。

### 阶段 1：邀请制 Alpha

目标用户：5 至 20 名已知测试者。

Go 标准：

- 用户身份和数据隔离测试通过；
- HTTPS、限流、预算熔断和 CORS allowlist 生效；
- 有隐私政策、服务条款和删除入口；
- 数据库每日备份，完成一次恢复演练；
- P95 API 延迟和 LLM 错误率有监控；
- 严重错误能在 15 分钟内通知维护者；
- 可以暂停所有 LLM 请求而不影响历史和复习查询。

### 阶段 2：Chrome Web Store 封闭或非公开 Beta

目标用户：20 至 100 名。

Go 标准：

- 商店材料和数据披露完整；
- 扩展安装、升级和卸载测试通过；
- 权限未超出当前功能；
- 无自动抓取和完整题库存储；
- 支持渠道和隐私联系邮箱有效；
- 关键体验指标达到预设目标；
- 成本上限能够覆盖最坏流量。

### 阶段 3：公开 Beta

公开 Beta 前仍需：

- 经过真实用户验证的留存信号；
- 稳定的用户隔离和删除流程；
- 容量和成本模型；
- 事故响应与状态公告机制；
- 对 DeepSeek 数据处理和目标市场法律要求完成专项审阅；
- 明确是否继续使用当前品牌名称。

## 9. 首发指标

产品指标：

- 激活率：首次安装后 24 小时内完成一次 AI 辅导并保存一次 attempt；
- 闭环率：发起辅导后最终保存 outcome 的比例；
- 复习完成率：到期 review 在 48 小时内完成的比例；
- D7 学习留存；
- 每周有效学习天数；
- 用户主动逐级提示与直接完整答案的比例。

质量指标：

- Side Panel 打开成功率；
- API 成功率；
- DeepSeek 错误率；
- P50/P95 首次响应时间；
- 数据写入失败率；
- 重复 attempt 率；
- 每活跃用户每日模型成本。

隐私原则：

- 默认不把完整代码、题目文本和模型回复写入业务日志；
- 指标使用长度、模式、延迟、错误码和 token 等元数据；
- 用户明确选择保存后，才持久化正文类内容。

## 10. 建议的近期执行顺序

建议接下来按以下顺序推进：

1. Side Panel 完成本题并写入 attempt；
2. 今日计划可恢复、计划项可完成；
3. 统一中英文、清理编码和交互状态；
4. GitHub Actions、lint、type check、扩展 E2E；
5. 生产配置、API URL 构建和安全响应头；
6. 身份认证与所有 repository 的 user isolation；
7. 限流、预算、usage metadata 和可观测性；
8. 隐私政策、删除/导出、服务条款；
9. staging 部署与备份恢复演练；
10. 邀请制 Alpha；
11. Chrome Web Store 非公开 Beta；
12. 根据留存、质量和成本数据决定是否公开。

## 11. 当前明确不做

在公开 Beta 前仍不建议加入：

- 复制的 LeetCode 题库；
- 自动批量抓取；
- 在线 Judge；
- 任意代码执行；
- 多语言编译环境；
- 支付系统；
- 排行榜或社交；
- 多代理编排；
- 模型训练；
- 复杂推荐引擎；
- 原生移动应用。

## 12. 最终建议

当前项目最有价值的资产不是 Dashboard，也不是某一个 prompt，而是已经形成的边界清晰的学习闭环架构：

```text
用户主动提供上下文
→ 分层辅导
→ 记录真实学习结果
→ 确定性安排复习
→ 下一次学习计划
```

下一阶段应优先证明这条循环是否让用户持续学习，而不是扩张功能数量。

最合理的近期目标是：先把项目做到“一个 Python 学习者可以连续使用两周，不需要手动补数据，也不会丢失学习状态”；达到这个标准后，再投入认证、托管和商店发布。这样可以避免在核心体验尚未验证前承担公开服务的安全、法律和成本责任。
