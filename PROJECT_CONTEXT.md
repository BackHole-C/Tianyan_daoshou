# 项目上下文文档

## 项目概述
- **项目名称**: 飞书机器人 + 通义千问AI集成
- **创建时间**: 2026-04-18
- **项目目标**: 部署具备AI对话能力的飞书机器人

## 技术栈
- **后端框架**: Flask (Python 3.8+)
- **AI模型**: 通义千问 (qwen-turbo)
- **部署工具**: ngrok (本地开发)
- **依赖管理**: Python虚拟环境

## 核心功能
- ✅ 飞书消息接收与处理
- ✅ 通义千问AI对话集成
- ✅ 消息去重（避免重复回复）
- ✅ 详细错误日志
- ✅ 即时日志输出

## 项目结构
```
Tianyan_daoshou/
├── robot_quick_start/
│   └── python/
│       ├── api/              # 飞书API客户端
│       ├── event/            # 事件处理
│       ├── qianwen_ai.py     # 通义千问AI集成
│       ├── server.py         # 主服务器
│       ├── .env              # 环境变量配置
│       └── robot_venv/       # Python虚拟环境
├── README.md                 # 项目文档
└── .gitignore                # Git忽略配置
```

## 环境变量配置
**文件**: `robot_quick_start/python/.env`

## 启动流程
1. **启动ngrok**:
   ```bash
   ngrok http 3000
   ```

2. **启动机器人服务**:
   ```bash
   cd robot_quick_start/python
   robot_venv/bin/python.exe -u server.py
   ```

## 关键模块说明

### qianwen_ai.py
- 通义千问AI客户端
- 处理AI API调用和错误处理
- 支持系统提示和用户消息

### server.py
- 主Flask服务器
- 事件处理和消息路由
- 消息去重功能
- 错误处理和日志记录

## 常见问题与解决方案

1. **AI服务不可用**
   - 检查API密钥是否正确
   - 查看终端日志获取详细错误信息

2. **消息重复回复**
   - 已实现消息去重功能，通过message_id去重

3. **日志不显示**
   - 使用 `python -u server.py` 启动服务，确保即时输出

4. **500错误**
   - 检查网络连接
   - 查看详细错误日志

## 注意事项
- 不要将API密钥上传到Git
- 定期更新ngrok地址并在飞书开发者后台配置
- 监控API调用频率，避免超出配额

## 未来扩展
- 添加更多AI模型支持
- 实现消息上下文管理
- 增加多语言支持
- 开发Web管理界面