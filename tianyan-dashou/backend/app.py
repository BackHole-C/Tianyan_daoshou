#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web后台API服务
功能：提供RESTful API接口，支持地块管理、数据分析、用户认证等
"""

import os
import yaml
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from loguru import logger

# 配置日志
logger.add("../logs/backend.log", rotation="7 days", retention="30 days")

# 加载配置
with open("../config/config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# 导入模块
from database import get_db, engine, Base
from routers import plots, analysis, auth, users
from models import User
from schemas import UserCreate, UserResponse

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建FastAPI应用
app = FastAPI(
    title="天眼稻守 API",
    description="智能农业病虫害检测与产量预测平台API",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(users.router, prefix="/api/users", tags=["用户"])
app.include_router(plots.router, prefix="/api/plots", tags=["地块"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["分析"])

@app.get("/")
def read_root():
    """根路径"""
    return {
        "message": "欢迎使用天眼稻守 API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    """健康检查"""
    return {"status": "healthy"}

# 初始化默认管理员用户
@app.on_event("startup")
async def startup_event():
    """启动事件"""
    db = next(get_db())
    try:
        # 检查是否已有管理员用户
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            # 创建默认管理员用户
            admin_user = User(
                username="admin",
                email="admin@example.com",
                full_name="系统管理员",
                role="admin"
            )
            admin_user.set_password("admin123")  # 设置默认密码
            db.add(admin_user)
            db.commit()
            logger.info("默认管理员用户创建成功")
    except Exception as e:
        logger.error(f"初始化默认管理员失败: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )