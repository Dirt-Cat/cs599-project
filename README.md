# CS599 Project - IELTS 智能练习系统

## 项目简介

本项目是一个基于 AI Agent 的 IELTS（雅思）智能练习系统，集成了阅读、听力、写作练习功能，并通过 LLM 提供智能评估和反馈。

## 方向

方向一：Agentic AI 原生开发

## 技术栈

- AI IDE: Trae CN
- LLM: DeepSeek API
- 框架: LangGraph
- 前端框架: Vue 3 + Vite
- 桌面应用: Electron
- 数据库: SQLite (better-sqlite3)
- 容器: Docker

## 目录结构

```
cs599-project/
├── docs/                    # 项目文档
│   ├── CS599_大作业报告.pdf   # 最终提交的报告（PDF）
│   └── architecture.md       # 详细架构说明
├── src/                      # 项目源代码（原 src 目录，已整合）
├── electron/                 # Electron 主进程
│   ├── main.js               # 主进程入口
│   ├── preload.js           # 预加载脚本
│   ├── services/            # 后端服务（LLM、评估等）
│   └── db/                  # 数据库访问层
├── apps/
│   └── writing-vue/         # Vue 写作应用
│       ├── src/
│       │   ├── api/         # API 客户端
│       │   ├── components/  # Vue 组件
│       │   ├── views/       # 页面视图
│       │   └── utils/       # 工具函数
│       └── vite.config.js   # Vite 配置
├── assets/                   # 静态资源
│   ├── data/                # 数据文件
│   ├── generated/           # 生成的题库数据
│   └── wordlists/           # 词表数据
├── ListeningPractice/        # 听力练习题库
├── css/                      # 样式文件
├── js/                       # 前端 JavaScript
├── developer/                # 开发者文档和测试
├── README.md                 # 项目入口
├── .gitignore                # Git 忽略配置
├── package.json              # 项目配置
└── LICENSE                   # 开源协议 (GPL v3)
```

`src/` 下各模块的职责：
- `electron/services/`: 后端服务，包括 LLM 提供者、评估服务、作文服务等
- `electron/db/`: 数据库访问层，管理题目、设置、作文等数据
- `apps/writing-vue/`: Vue 写作练习前端应用
- `assets/generated/`: 预生成的阅读题库数据

## 环境搭建

### 1. 依赖安装

```bash
# 安装主项目依赖
npm install

# 安装 Vue 写作应用依赖
npm run prepare:writing
```

### 2. 环境变量配置

⚠️ **不硬编码 API Key**

创建 `.env` 文件：

```env
DEEPSEEK_API_KEY=your_api_key_here
```

或在 Electron 设置页面配置 LLM 提供者。

### 3. 启动步骤

```bash
# 构建并启动 Electron 应用
npm run start

# 仅启动 Electron（跳过构建）
npm run start:electron

# 开发模式启动 Vue 写作应用
cd apps/writing-vue && npm run dev
```

## 主要功能

### 📚 阅读练习
- P1/P2/P3 三级难度题库（约 147 篇）
- 交互式答题和自动评分
- 练习记录和统计分析

### 🎧 听力练习
- P1/P4 听力套题
- HTML 交互式练习界面

### ✍️ 写作练习
- AI 智能评估（基于 DeepSeek API）
- 作文历史记录和雷达图分析
- 题目管理和自定义题目

### ⚙️ 系统功能
- 数据备份和导入
- 多主题切换（Academic/Bloom/Melody）
- 自动更新机制

## 项目状态

- [x] Proposal
- [x] MVP
- [ ] Final

## 许可证

本项目采用 [GNU General Public License v3](LICENSE) 许可。