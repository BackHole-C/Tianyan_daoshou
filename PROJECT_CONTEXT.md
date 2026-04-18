# 天眼稻守 - 项目上下文文件

> 本文件用于帮助AI助手快速了解项目状态，继续未完成的工作
> 最后更新：2026-04-18

## 项目概述

**项目名称**：天眼稻守 (Tianyan Daoshou)
**项目描述**：基于多源遥感数据 + AI大模型的智慧水稻风险管理与协作平台
**仓库地址**：https://github.com/BackHole-C/Tianyan_daoshou.git

### 核心功能
- 🤖 飞书智能机器人（已集成通义千问AI）
- 🔧 Web管理后台（Vue3 + FastAPI）
- 📊 农业数据分析Agent系统
- 🌾 水稻产量预测与病虫害识别

---

## 项目结构

```
Tianyan_daoshou/
├── robot_quick_start/              # 飞书机器人项目 ⭐当前工作目录
│   └── python/
│       ├── server.py              # 机器人主服务（集成AI对话）
│       ├── api.py                 # 飞书API客户端
│       ├── event.py               # 事件处理
│       ├── qianwen_ai.py          # 通义千问AI模块（新增）
│       ├── .env                   # 敏感配置（已被gitignore）
│       ├── .env.example           # 配置模板
│       └── robot_venv/            # Python虚拟环境
├── tianyan-dashou/                # 管理后台
│   ├── frontend/                  # Vue3前端
│   └── agents/                    # AI Agent系统
│       ├── data-agent/            # 数据采集Agent
│       ├── analysis-agent/        # 分析Agent
│       └── collaboration/         # 协作Agent
├── README.md                      # 项目主文档
├── Project_Requirements.md         # 需求文档
└── Technical_Solution.md          # 技术方案
```

---

## 关键技术栈

### AI能力
- **大模型**：通义千问 qwen-turbo（阿里云）
- **免费额度**：100万tokens/月
- **API配置**：DASHSCOPE_API_KEY

### 机器人技术
- **框架**：Flask
- **消息处理**：飞书开放平台 API
- **内网穿透**：ngrok
- **端口**：3000

### 管理后台技术
- **前端**：Vue3, Vite, Element Plus, Leaflet
- **后端**：FastAPI, PostgreSQL, TimescaleDB
- **数据处理**：GDAL, rasterio, PyTorch, scikit-learn

---

## 当前配置状态

### 飞书应用配置 (.env)
```env
APP_ID=cli_a9684f10c5f91cc2
APP_SECRET=TrT10VVRRGfQkDJ65z9nqb1ieFR0GSXn
VERIFICATION_TOKEN=rGock8G80B1Pdbers19RghZCuJBgpZZo
ENCRYPT_KEY=
LARK_HOST=https://open.feishu.cn
DASHSCOPE_API_KEY=sk-b3cb30a8f9d14aee92676a5bbd2eac31
```

### AI配置
- **模型**：qwen-turbo
- **系统角色**：农业智能助手"天眼稻守"
- **功能**：水稻种植咨询、病虫害识别、农业保险问答

---

## 服务启动命令

### 机器人服务
```bash
cd c:\Users\86156\Desktop\Tianyan_daoshou\robot_quick_start\python
robot_venv\bin\python.exe server.py
```

### ngrok内网穿透
```bash
ngrok http 3000
```

### 验证服务状态
```bash
netstat -an | findstr :3000
```

---

## Git状态

### 最新提交 (2026-04-18)
```
commit 2b59267
feat: 集成通义千问大模型，实现AI智能对话功能

- 新增 qianwen_ai.py 模块，集成通义千问API
- 修复 api.py 中消息发送的JSON格式问题
- 更新 server.py，集成AI对话功能
- 更新 README.md 和 README.zh.md 文档
- 创建 .env.example 配置模板
```

### 分支
- **main**: 当前工作分支
- **origin**: git@github.com:BackHole-C/Tianyan_daoshou.git

---

## 已完成工作

### 飞书机器人
✅ 修复消息API格式问题
✅ 实现群组消息和私聊消息处理
✅ 集成通义千问AI对话功能
✅ 配置ngrok内网穿透
✅ 完善日志记录

### AI集成
✅ 创建 qianwen_ai.py 模块
✅ 配置通义千问API密钥
✅ 设置农业助手系统提示词
✅ 实现异步HTTP调用通义千问API

### 文档
✅ 更新主项目 README.md
✅ 更新机器人 README.zh.md
✅ 创建 .env.example 配置模板
✅ 完成Git提交并推送

---

## 后续工作建议

### 短期（可选）
1. 测试AI对话效果，根据反馈调整提示词
2. 升级模型（如需更强能力）：qwen-turbo → qwen-plus
3. 添加更多AI使用场景

### 中期
1. 实现数据采集Agent的数据源对接
2. 完成产量预测模型的训练
3. 实现病虫害识别功能

### 长期
1. 部署到正式服务器（替代ngrok）
2. 添加用户认证和权限管理
3. 实现完整的保险理赔流程

---

## 常见问题排查

### 机器人不响应
1. 检查服务：`netstat -an | findstr :3000`
2. 检查ngrok：`curl http://localhost:4040/api/tunnels`
3. 检查飞书事件订阅配置

### AI不回复
1. 确认 DASHSCOPE_API_KEY 配置正确
2. 检查通义千问API余额
3. 查看服务日志中的错误信息

### Git问题
```bash
# 查看状态
git status

# 查看提交历史
git log --oneline

# 查看远程仓库
git remote -v
```

---

## 关键文件说明

| 文件路径 | 功能 | 重要度 |
|---------|------|--------|
| `robot_quick_start/python/server.py` | 机器人主服务 | ⭐⭐⭐ |
| `robot_quick_start/python/qianwen_ai.py` | 通义千问AI模块 | ⭐⭐⭐ |
| `robot_quick_start/python/.env` | 敏感配置 | ⭐⭐⭐ |
| `tianyan-dashou/agents/*/config.yaml` | Agent配置 | ⭐⭐ |
| `Project_Requirements.md` | 项目需求文档 | ⭐⭐ |

---

## 工作上下文

### 当前终端状态
- 机器人服务：**已关闭**
- ngrok：**未运行**
- 所有服务均已正常关闭

### 用户目标
- 完成飞书机器人部署和AI集成
- 完善项目文档
- 代码安全上传GitHub

### 用户技能水平
- 了解Python基础
- 了解Git基本操作
- 了解飞书开发者平台

---

**提示**：如需继续工作，只需阅读本文件即可快速了解项目状态和配置。
