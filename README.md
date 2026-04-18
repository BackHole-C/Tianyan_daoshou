# 天眼助手 (Tianyan Assistant)

一个集成飞书机器人和管理后台的智能助手项目，支持群组消息和私聊消息处理。

## 项目结构

```
Tianyan_daoshou/
├── robot_quick_start/         # 飞书机器人快速启动项目
│   └── python/                # Python版本的机器人实现
│       ├── .env               # 环境变量配置（本地开发用）
│       ├── .env.example       # 环境变量模板
│       ├── server.py          # 机器人主服务
│       ├── api.py             # 飞书API客户端
│       ├── event.py           # 事件处理
│       ├── requirements.txt   # 依赖包
│       └── robot_venv/        # 虚拟环境
├── tianyan-dashou/            # 管理后台
│   ├── frontend/              # 前端代码
│   └── agents/                # 智能代理
├── .gitignore                 # Git忽略文件
├── Project_Requirements.md    # 项目需求文档
├── Technical_Solution.md      # 技术解决方案
└── README.md                  # 项目说明
```

## 功能特性

### 🤖 飞书机器人
- 支持群组消息和私聊消息
- 消息自动回复功能
- 基于飞书开放平台API
- 本地部署，安全可控

### 🔧 管理后台
- Vue3 + Vite前端框架
- 智能代理系统
- 飞书集成

## 快速开始

### 1. 环境准备

#### Python环境
```bash
# 推荐使用Python 3.8+
# 已创建虚拟环境 robot_venv
```

#### 飞书应用配置
1. 在 [飞书开发者平台](https://open.feishu.cn) 创建应用
2. 启用机器人功能
3. 申请必要权限：
   - `im:message`
   - `im:message:send_as_bot`
4. 配置事件订阅：
   - 事件：`im.message.receive_v1`
   - 请求地址：你的公网地址 + `/webhook/event`

### 2. 配置环境变量

复制环境变量模板并填写实际值：

```bash
cp robot_quick_start/python/.env.example robot_quick_start/python/.env
```

编辑 `.env` 文件：

```
# 飞书应用信息
APP_ID=your_app_id
APP_SECRET=your_app_secret
VERIFICATION_TOKEN=your_verification_token
ENCRYPT_KEY=
LARK_HOST=https://open.feishu.cn
```

### 3. 安装依赖

```bash
# 使用虚拟环境安装依赖
robot_quick_start/python/robot_venv/bin/python -m pip install -r robot_quick_start/python/requirements.txt
```

### 4. 启动服务

```bash
# 启动机器人服务
robot_quick_start/python/robot_venv/bin/python robot_quick_start/python/server.py

# 服务将运行在 http://127.0.0.1:3000
```

### 5. 配置内网穿透

使用 ngrok 实现公网访问：

```bash
# 安装 ngrok（如果尚未安装）
# 注册账号并获取 authtoken

# 启动 ngrok
ngrok authtoken your_token
ngrok http 3000

# 获取生成的公网地址，配置到飞书开发者后台
```

## 使用方法

### 在飞书群聊中使用
1. 将机器人添加到群组
2. @机器人并发送消息
3. 机器人会自动回复相同的消息

### 私聊机器人
1. 直接与机器人对话
2. 机器人会自动回复相同的消息

## 技术栈

- **后端**：Python 3.8+, Flask
- **前端**：Vue3, Vite
- **机器人**：飞书开放平台 API
- **部署**：本地部署 + ngrok 内网穿透

## 项目配置

### 飞书开发者后台配置

1. **事件订阅**：
   - 启用事件订阅
   - 请求地址：`https://your-ngrok-address.ngrok.io/webhook/event`
   - 验证令牌：与 `.env` 文件中的 `VERIFICATION_TOKEN` 一致

2. **权限管理**：
   - 申请 `im:message` 权限
   - 申请 `im:message:send_as_bot` 权限

3. **版本管理**：
   - 创建版本
   - 配置可用范围
   - 申请发布

## 开发说明

### 机器人代码结构

- `server.py`：主服务文件，处理HTTP请求和事件
- `api.py`：飞书API客户端，封装API调用
- `event.py`：事件定义和管理器
- `decrypt.py`：消息解密工具
- `utils.py`：工具函数

### 消息处理流程

1. 飞书发送事件到机器人服务
2. 服务接收并解析事件
3. 根据事件类型调用相应的处理函数
4. 处理函数生成回复
5. 发送回复到飞书

## 故障排查

### 常见问题

1. **机器人不响应**：
   - 检查服务是否运行：`http://127.0.0.1:3000`
   - 检查 ngrok 连接是否正常
   - 检查飞书事件订阅配置

2. **权限错误**：
   - 确保已申请必要权限
   - 确保应用已发布

3. **环境变量错误**：
   - 检查 `.env` 文件配置
   - 确保 `APP_ID` 和 `APP_SECRET` 正确

## 安全提示

- **敏感信息**：`.env` 文件包含敏感信息，请勿提交到版本控制系统
- **权限管理**：仅授予必要的权限
- **网络安全**：使用 HTTPS 连接

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

如有问题，请联系项目维护者。
