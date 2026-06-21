# CS599 Project - IELTS 智能练习系统

## 项目简介

基于 AI Agent 的 IELTS（雅思）智能练习桌面应用，集成阅读、听力、写作练习功能，并通过 LLM 提供智能评估与反馈。

本项目借鉴了开源项目 [IELTS-practice](https://github.com/sallowayma-git/IELTS-practice)。

## 方向

方向一：Agentic AI 原生开发

## 技术栈

- AI IDE: Trae CN
- LLM: DeepSeek API
- 框架: LangGraph
- 前端: Vue 3 + Vite
- 桌面: Electron
- 后端: Fastify
- 数据库: SQLite (better-sqlite3)
- 容器: Docker

## 目录结构

```
src/
├── electron/                 # Electron 主进程：窗口管理、IPC 桥梁、安全存储
│   ├── main.js               # 主进程入口，创建窗口、启动 Fastify 服务器
│   ├── preload.js            # 预加载脚本，暴露 electronAPI 给渲染进程
│   ├── services/             # 核心服务：LLM 编排、API 配置管理、评估服务
│   └── db/                   # SQLite 数据库访问层
├── server/                   # Fastify 后端 API 服务器（端口 3000）
│   └── src/
│       ├── routes/           # 路由模块：management、practice、reading、writing
│       └── lib/              # 业务逻辑：LLM 编排、阅读教练、提示词管理
├── apps/
│   └── writing-vue/          # Vue 3 写作练习 SPA（AI 评分 + 题库管理 + 设置）
├── js/                       # 主壳渲染进程脚本（总览、题库浏览、练习记录）
├── css/                      # 主壳样式
├── assets/                   # 静态资源（题库数据、词汇表、图片）
├── templates/                # HTML 模板（考试占位、题目类型定义）
├── report-agent/             # LangGraph 报告生成 Agent（Python）
├── ListeningPractice/        # 听力练习题库（HTML 音频播放页面）
├── developer/                # 开发文档与测试（E2E、单元测试、CI 脚本）
└── index.html                # 渲染进程入口（主壳页面 + 导航）
```

## 环境搭建

### 1. 依赖安装

```bash
cd src
npm install
npm --prefix apps/writing-vue install --no-fund --no-audit
```

### 2. 环境变量配置

**⚠️ 不硬编码 API Key**

复制环境变量模板并填写 API Key：

```bash
cp src/report-agent/.env.example src/report-agent/.env
```

编辑 `src/report-agent/.env`：

```env
DEEPSEEK_API_KEY=your_api_key_here
```

或者启动后在写作练习的「更多工具 → 写作评分 → 设置 → API 配置」界面中添加 LLM 提供者（Provider: DeepSeek / OpenAI / OpenRouter），API Key 会通过 Electron `safeStorage` 加密存入 SQLite。

### 3. 启动步骤

```bash
cd src
npm run start
```

等价于依次执行：构建服务端 → 构建 Vue 写作应用 → 启动 Electron。如需快速重启（已构建过）：

```bash
npm run start:electron
```

## 项目状态

- [x] Proposal
- [x] MVP
- [ ] Final

## 许可证

本项目采用 [GNU General Public License v3](LICENSE) 许可。