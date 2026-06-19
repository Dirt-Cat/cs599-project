"""
报告各章节的提示词模板。
每个章节对应一个精确的 prompt，引导 DeepSeek 生成学术级内容。
"""

# ── 封面信息 ──
COVER_META = {
    "course": "企业级应用软件设计与开发",
    "project_name": "IELTS 智能练习系统",
    "direction": "方向一：Agentic AI 原生开发",
    "student_id": "—",
    "name": "—",
    "major": "计算机技术",
    "instructor": "戚欣",
    "date": "2026年6月22日",
}

# ── 系统提示词（全局） ──
SYSTEM_PROMPT = """你是一位资深的软件工程研究生，正在撰写《企业级应用软件设计与开发》课程的大作业报告。
你的报告对象是课程评审老师，需要有技术深度、逻辑清晰、图文并茂。

写作要求：
1. 使用中文撰写，专业术语可保留英文
2. 对代码片段使用 Markdown 代码块，标注语言
3. 架构图使用 Mermaid 语法，确保可渲染
4. 数据流程使用 ASCII 图或 Mermaid 时序图
5. 章节编号使用中文数字（一、二、三...）
6. 每章独立生成，最终合并为完整报告

项目信息：
- 项目名称：IELTS 智能练习系统
- 技术栈：Electron + Vue 3 + Vite，后端服务 Node.js，LLM 使用 DeepSeek API
- 数据库：SQLite (better-sqlite3)
- 功能模块：阅读练习、听力练习、写作练习（AI 评估）、用户设置、数据备份
- Agent 架构：LLM Provider 管理 → 评估服务 → 数据持久化，IPC 通信层
"""

# ── 各章节提示词 ──
CHAPTER_PROMPTS = {
    "1": {
        "title": "选题背景与设计思想",
        "prompt": """请撰写「选题背景与设计思想」章节，包含以下内容：

## 1.1 问题定义
- IELTS 备考者的核心痛点是什么？
- 传统练习平台（如纸质题库、简单在线练习）的不足：
  - 缺乏个性化反馈
  - 无法智能评估写作质量
  - 学习数据分散，无法追踪进步

## 1.2 现有方案分析
- 市面上已有方案（如新东方在线、小站教育等）的局限性
- 为什么需要 AI Agent 驱动的方案

## 1.3 项目价值
- 对用户的价值（即时反馈、个性化学习路径）
- 技术价值（Agentic AI 在垂直教育领域的应用）

## 1.4 技术路线
- 选择 Electron 作为桌面框架的原因
- 选择 DeepSeek API 作为 LLM 后端的考量
- 整体技术架构概述

请用专业、学术的语气撰写，不少于 800 字。""",
    },
    "2": {
        "title": "Specs 规格文档",
        "prompt": """请撰写「Specs 规格文档」章节，这是一份 SDD（Software Design Document），包含以下三个部分：

## 2.1 Product Spec（产品规格）
- 目标用户画像：IELTS 备考学生
- 核心功能列表：
  - 阅读练习：P1/P2/P3 三级难度，约 147 篇题库，交互式答题
  - 听力练习：P1/P4 套题，HTML 交互界面
  - 写作练习：AI 智能评估（Task 1 / Task 2），雷达图分析
  - 系统功能：数据备份、多主题切换、自动更新
- 非功能需求：本地优先、离线可用、API Key 安全存储

## 2.2 Architecture Spec（架构规格）
- 整体架构：Electron 主进程 + 渲染进程 + Vue 子应用
- 进程间通信（IPC）设计
- 服务层设计：LLM Provider、评估服务、作文服务
- 数据层设计：SQLite DAO 层

## 2.3 API Spec（接口规格）
- LLM Provider 接口定义
- 评估服务 API
- 作文 CRUD API
- 设置管理 API

请使用表格和代码块清晰展示接口定义，不少于 800 字。""",
    },
    "3": {
        "title": "系统架构与设计",
        "prompt": """请撰写「系统架构与设计」章节，重点展示架构图和流程设计，图文并茂。

## 3.1 核心架构图
使用 Mermaid 绘制系统架构图：
```mermaid
flowchart TB
    subgraph Desktop[Electron 桌面应用]
        RP[渲染进程<br/>index.html]
        MP[主进程<br/>main.js]
        VUE[Vue 写作应用<br/>writing-vue]
    end
    subgraph Services[后端服务层]
        LLM[LLM Provider]
        EVAL[评估服务]
        TOPIC[题目服务]
        CONFIG[配置服务]
    end
    subgraph Data[数据层]
        DB[(SQLite)]
    end
    RP --> MP
    VUE --> MP
    MP --> Services
    LLM -->|API| DEEPSEEK[DeepSeek API]
    Services --> Data
```

## 3.2 Agent 交互流程
使用 Mermaid 时序图展示写作评估的完整流程：
1. 用户输入作文
2. IPC 传递到主进程
3. LLM Provider 调用 DeepSeek API
4. 评估服务解析结果
5. 存储到数据库
6. 返回结果给前端

## 3.3 数据流设计
- 用户数据流：设置 → 题目选择 → 练习 → 评估 → 存储
- 评估数据流：作文文本 → Prompt 构建 → LLM 调用 → 结果解析 → 评分展示
- 数据持久化方案：SQLite 表结构设计

要求：少量文字说明，以图为主，一图胜千言。每一张图都配简要文字说明。""",
    },
    "4": {
        "title": "关键实现与代码展示",
        "prompt": """请撰写「关键实现与代码展示」章节，展示核心代码和 AI IDE 使用过程。

## 4.1 Agent 核心循环
展示 LLM Provider 的核心实现（伪代码或关键代码片段）：

```javascript
// LLM Provider 核心循环
class LLMProvider {
    async call(prompt, options) {
        const response = await fetch(this.baseURL, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${this.apiKey}` },
            body: JSON.stringify({
                model: this.model,
                messages: [{ role: 'user', content: prompt }],
                ...options
            })
        });
        return response.json();
    }
}
```

## 4.2 工具定义
展示评估服务如何构建 Prompt 和解析 LLM 响应：

```javascript
// 评估 Prompt 构建
function buildEvaluationPrompt(essay) {
    return `请对以下 IELTS ${essay.type} 作文进行评分...
    
评分维度：
1. Task Achievement (任务完成度)
2. Coherence & Cohesion (连贯与衔接)
3. Lexical Resource (词汇资源)
4. Grammatical Range & Accuracy (语法范围与准确性)
...`;
}
```

## 4.3 配置文件
展示关键配置文件（package.json、vite.config.js 等）的设计思路

## 4.4 AI IDE 使用截图
说明使用 Trae CN IDE 进行开发的过程：
- 代码补全和生成
- Agent 辅助调试
- 项目结构规划

（注：实际截图在 PDF 编译时插入）

请确保代码块使用正确的语法高亮，代码有适当注释。不少于 800 字。""",
    },
    "5": {
        "title": "测试与评估",
        "prompt": """请撰写「测试与评估」章节，包含以下内容：

## 5.1 功能测试
- 阅读练习模块测试：题库加载、答题交互、评分正确性
- 听力练习模块测试：音频播放、题目展示、答案校验
- 写作练习模块测试：作文输入、AI 评估调用、结果展示
- 系统功能测试：数据备份/恢复、主题切换、设置管理

## 5.2 Agent 行为评估
- LLM 响应质量评估
  - 作文评分的准确性（与人工评分对比）
  - 评语的相关性和建设性
  - 响应时间（P50/P95/P99）
- Prompt 工程效果评估
  - 不同 Prompt 模板对评估质量的影响
  - Token 消耗分析

## 5.3 Benchmark
- 系统性能指标
  - 应用启动时间
  - 题库加载速度
  - 内存占用
- API 调用性能
  - 平均响应时间
  - 成功率
  - 并发处理能力

## 5.4 Demo 截图/录屏
（注：实际截图在 PDF 编译时插入）

请使用表格展示测试结果，不少于 600 字。""",
    },
    "6": {
        "title": "系统升级与扩展",
        "prompt": """请撰写「系统升级与扩展」章节，包含以下内容：

## 6.1 可扩展架构设计
- 当前架构的扩展点分析
- 插件化 LLM Provider 设计（支持多模型切换）
- 模块化题目加载机制
- 主题系统的扩展性

## 6.2 下一阶段计划
- 短期（1-3 个月）：
  - 集成 LangGraph 实现多 Agent 协作
  - 添加口语练习模块
  - 实现自适应学习路径推荐
- 中期（3-6 个月）：
  - Docker 容器化部署
  - 云端同步和协作功能
  - 更多 LLM 提供者支持（OpenAI、Claude 等）
- 长期（6-12 个月）：
  - 基于用户数据的个性化推荐
  - 社区题库共享
  - 移动端适配

## 6.3 AI 能力演进路径
- 从单一 LLM 调用 → 多 Agent 协作
- 从静态评估 → 动态学习路径生成
- 从规则驱动 → 数据驱动的自适应学习
- 未来可能的 AI 能力集成（语音识别、图像识别等）

请用专业、前瞻性的视角撰写，不少于 600 字。""",
    },
    "7": {
        "title": "课程总结",
        "prompt": """请撰写「课程总结」章节，包含以下内容：

## 7.1 个人收获
- 技术层面：
  - 掌握了 Electron 桌面应用开发
  - 深入理解了 LLM API 集成和 Prompt 工程
  - 学习了 Agentic AI 的设计模式
- 工程层面：
  - 理解了完整的软件开发生命周期
  - 实践了从需求分析到部署的全流程
  - 学会了测试驱动开发和质量保证

## 7.2 工程思维转变
- 从"写代码"到"设计系统"的转变
- 从"功能实现"到"用户体验"的转变
- 从"本地开发"到"工程化协作"的转变
- AI 辅助开发对传统软件工程的影响思考

## 7.3 对课程的建议
- 课程内容的优点
- 可能的改进方向
- 对未来学生的建议

请用真诚、反思性的语气撰写，不少于 600 字。""",
    },
}