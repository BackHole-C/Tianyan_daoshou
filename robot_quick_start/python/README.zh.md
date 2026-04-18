# 飞书智能机器人 - 快速开发指南

> ⚠️ 本教程为了方便实现，使用了反向代理工具（ngrok），该工具仅适用于开发测试阶段，不可用于生产环境。

本示例介绍如何使用飞书开放平台机器人能力，集成通义千问大模型，实现智能农业助手功能。

## 核心功能

### 🤖 AI智能对话
- **通义千问大模型**：集成阿里云通义千问，支持农业知识智能问答
- **病虫害咨询**：识别水稻常见病害，提供防治建议
- **农业知识问答**：解答种植技术、农业保险等问题

## 运行环境

- [Python 3](https://www.python.org/)
- [ngrok](https://ngrok.com/download) （内网穿透工具）
- [阿里云DashScope](https://dashscope.console.aliyun.com/) （通义千问API）

## 准备工作

### 1. 飞书应用配置
1. 在[开发者后台](https://open.feishu.cn/app/) **新建企业自建应用**
2. 获取应用凭证：
   - `App ID` 和 `App Secret`（凭证与基础信息页面）
   - `Encrypt Key` 和 `Verification Token`（事件订阅页面）

### 2. 通义千问API配置
1. 登录 [阿里云DashScope](https://dashscope.console.aliyun.com/)
2. 开通服务（有免费额度：100万tokens/月）
3. 创建API密钥，复制 `API Key`

## 快速开始

### 1. 配置环境变量

修改 `robot_quick_start/python/.env` 文件：

```env
# 飞书应用信息
APP_ID=cli_xxxxxxxxxxxxx
APP_SECRET=xxxxxxxxxxxxxxxx
VERIFICATION_TOKEN=xxxxxxxxxxxxxxxx
ENCRYPT_KEY=
LARK_HOST=https://open.feishu.cn

# 通义千问API（AI功能）
DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxxxxx
```

### 2. 本地运行

**Windows**

```commandline
cd c:\Users\86156\Desktop\Tianyan_daoshou\robot_quick_start\python

# 激活虚拟环境
robot_venv\Scripts\activate

# 启动服务
python server.py
```

**macOS/Linux**

```commandline
cd robot_quick_start/python

# 激活虚拟环境
source robot_venv/bin/activate

# 启动服务
python server.py
```

### 3. 配置内网穿透

```commandline
# 启动 ngrok
ngrok http 3000

# 复制生成的公网地址（如 https://xxxx.ngrok.io）
```

### 4. 飞书开发者后台配置

1. **启用机器人**：点击机器人 → 打开启用机器人开关

2. **配置事件订阅**：
   - 请求网址 URL：`https://你的ngrok地址`
   - 添加事件：`im.message.receive_v1`

3. **申请权限**：
   - `im:message` - 获取与发送消息
   - `im:message:send_as_bot` - 以机器人身份发送消息

4. **发布应用**：
   - 版本管理与发布 → 创建版本 → 申请发布

## 使用方法

### 体验AI对话

1. 在飞书群聊中@机器人并发送消息
2. 或直接给机器人发私信
3. 机器人将调用通义千问AI进行智能回复

### 示例问题

```
- "水稻叶片发黄是什么原因？"
- "如何防治稻瘟病？"
- "推荐一下水稻品种"
- "农业保险怎么办理？"
```

## 项目结构

```
robot_quick_start/python/
├── .env                 # 环境变量配置
├── server.py           # 机器人主服务 ⭐
├── api.py              # 飞书API客户端
├── event.py            # 事件处理
├── qianwen_ai.py       # 通义千问AI模块 ⭐新增
├── decrypt.py          # 消息解密
├── utils.py            # 工具函数
└── robot_venv/        # Python虚拟环境
```

## 消息处理流程

```
用户发送消息
    ↓
飞书服务器 → POST / （回调事件）
    ↓
ngrok公网 → 机器人服务（http://127.0.0.1:3000）
    ↓
server.py 接收并解析消息
    ↓
调用通义千问API（qianwen_ai.py）
    ↓
获取AI回复
    ↓
通过飞书API发送回复
    ↓
用户收到AI智能回复
```

## AI配置说明

### 通义千问模型

| 配置项 | 说明 |
|-------|------|
| 模型名称 | qwen-turbo |
| API接口 | https://dashscope.aliyuncs.com |
| 免费额度 | 100万tokens/月 |
| 响应速度 | 快（适合对话） |

### 可升级模型

如需更强能力，可修改 `qianwen_ai.py` 中的模型配置：

```python
self.model = "qwen-turbo"      # 当前使用
# self.model = "qwen-plus"     # 更强
# self.model = "qwen-max"      # 最强
```

## 故障排查

### 机器人不响应
```bash
# 检查服务是否运行
netstat -an | findstr :3000

# 检查ngrok状态
curl http://localhost:4040/api/tunnels
```

### AI不回复
- 检查 `DASHSCOPE_API_KEY` 是否配置正确
- 检查通义千问API余额
- 查看服务日志中的错误信息

### 权限问题
- 确保已申请 `im:message:send_as_bot` 权限
- 确保应用已发布

## 技术栈

| 组件 | 技术 |
|-----|------|
| AI大模型 | 通义千问 (qwen-turbo) |
| 后端框架 | Flask |
| 消息处理 | 飞书开放平台 API |
| 内网穿透 | ngrok |

## 注意事项

- ⚠️ ngrok 仅用于开发测试
- ⚠️ `.env` 文件包含敏感信息，请勿提交到版本控制
- ⚠️ 使用前确认公司网络安全政策
