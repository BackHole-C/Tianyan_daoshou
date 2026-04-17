# 天眼稻守 - 本地开发指南

## 前端运行

### 1. 安装依赖
```bash
cd frontend
npm install
```

### 2. 运行开发服务器
```bash
npm run dev
```

前端将在 http://localhost:3000 运行

### 3. 构建生产版本
```bash
npm run build
```

## 后端运行

### 1. 安装Python依赖
```bash
cd backend
pip install -r requirements.txt
```

### 2. 运行开发服务器
```bash
uvicorn app:app --reload
```

后端将在 http://localhost:8000 运行

### 3. 查看API文档
访问 http://localhost:8000/api/docs

## Docker部署

### 启动所有服务
```bash
docker-compose up -d
```

### 停止所有服务
```bash
docker-compose down
```

## 默认登录账号
- 用户名：admin
- 密码：admin123