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
├── src/                      # 项目源代码
│   ├── electron/             # Electron 主进程
│   │   ├── main.js           # 主进程入口
│   │   ├── preload.js        # 预加载脚本
│   │   ├── services/         # 后端服务（LLM、评估等）
│   │   └── db/               # 数据库访问层
│   ├── apps/
│   │   └── writing-vue/      # Vue 写作应用
│   ├── assets/               # 静态资源
│   ├── js/                   # 前端 JavaScript
│   ├── css/                  # 样式文件
│   ├── ListeningPractice/    # 听力练习题库
│   ├── developer/            # 开发者文档和测试
│   ├── package.json          # 项目配置
│   └── index.html            # 渲染进程入口
├── README.md                 # 项目入口
├── .gitignore                # 排除编译文件
└── LICENSE                   # 开源协议 (GPL v3)
```

## 环境搭建

### 1. 依赖安装

```bash
cd src
npm install
npm run prepare:writing
```

### 2. 环境变量配置

⚠️ **不硬编码 API Key**

复制 `src/.env.example` 为 `src/.env` 并填写 API Key：

```env
DEEPSEEK_API_KEY=your_api_key_here
```

或在 Electron 设置页面配置 LLM 提供者。

### 3. 启动步骤

```bash
cd src
npm run start
```

## 项目状态

- [x] Proposal
- [x] MVP
- [ ] Final

## 许可证

本项目采用 [GNU General Public License v3](LICENSE) 许可。