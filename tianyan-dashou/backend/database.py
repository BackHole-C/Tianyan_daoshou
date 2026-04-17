#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库模块
功能：数据库连接、模型定义
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, Date, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from passlib.context import CryptContext

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 数据库连接URL
DATABASE_URL = "postgresql://user:pass@db:5432/tianyan"

# 创建数据库引擎
engine = create_engine(DATABASE_URL)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()

# 依赖项：获取数据库会话
def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class User(Base):
    """用户模型"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100))
    password_hash = Column(String(100), nullable=False)
    role = Column(String(20), default="user")  # admin, user, farmer, insurance
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password):
        """设置密码"""
        self.password_hash = pwd_context.hash(password)
    
    def verify_password(self, password):
        """验证密码"""
        return pwd_context.verify(password, self.password_hash)

class Plot(Base):
    """地块模型"""
    __tablename__ = "plot_base"
    
    id = Column(Integer, primary_key=True, index=True)
    plot_id = Column(String(50), unique=True, index=True, nullable=False)
    plot_name = Column(String(100), nullable=False)
    area_mu = Column(Float, nullable=False)
    crop_type = Column(String(20), default="rice")
    variety = Column(String(50))
    owner_name = Column(String(50))
    owner_phone = Column(String(20))
    geom = Column(Text)  # 存储GeoJSON格式的几何数据
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class NDVI_Timeseries(Base):
    """NDVI时序数据模型"""
    __tablename__ = "plot_ndvi_timeseries"
    
    id = Column(Integer, primary_key=True, index=True)
    plot_id = Column(String(50), ForeignKey("plot_base.plot_id"), nullable=False)
    observation_date = Column(Date, nullable=False)
    ndvi_mean = Column(Float)
    ndvi_min = Column(Float)
    ndvi_max = Column(Float)
    cloud_coverage = Column(Float)
    source = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

class WeatherData(Base):
    """气象数据模型"""
    __tablename__ = "plot_weather_data"
    
    id = Column(Integer, primary_key=True, index=True)
    plot_id = Column(String(50), ForeignKey("plot_base.plot_id"), nullable=False)
    observation_date = Column(Date, nullable=False)
    temperature_max = Column(Float)
    temperature_min = Column(Float)
    precipitation = Column(Float)
    sunshine_hours = Column(Float)
    humidity = Column(Float)
    wind_speed = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class YieldPrediction(Base):
    """产量预测模型"""
    __tablename__ = "plot_yield_prediction"
    
    id = Column(Integer, primary_key=True, index=True)
    plot_id = Column(String(50), ForeignKey("plot_base.plot_id"), nullable=False)
    prediction_date = Column(Date, nullable=False)
    expected_harvest_date = Column(Date)
    predicted_yield_kg_mu = Column(Float)
    confidence_level = Column(Float)
    growth_stage = Column(String(20))
    risk_level = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

class DiseaseRisk(Base):
    """病虫害风险模型"""
    __tablename__ = "plot_disease_risk"
    
    id = Column(Integer, primary_key=True, index=True)
    plot_id = Column(String(50), ForeignKey("plot_base.plot_id"), nullable=False)
    detection_date = Column(Date, nullable=False)
    disease_type = Column(String(50))
    risk_level = Column(Integer)
    confidence = Column(Float)
    affected_area_percent = Column(Float)
    recommendation = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)