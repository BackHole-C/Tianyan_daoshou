#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据模型定义
功能：定义API请求和响应的数据模型
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import date, datetime

# 用户相关模型
class UserBase(BaseModel):
    """用户基础模型"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None
    role: Optional[str] = "user"

class UserCreate(UserBase):
    """用户创建模型"""
    password: str = Field(..., min_length=6)

class UserUpdate(BaseModel):
    """用户更新模型"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    """用户响应模型"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# 认证相关模型
class Token(BaseModel):
    """令牌模型"""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """令牌数据模型"""
    username: Optional[str] = None

class LoginRequest(BaseModel):
    """登录请求模型"""
    username: str
    password: str

# 地块相关模型
class PlotBase(BaseModel):
    """地块基础模型"""
    plot_id: str
    plot_name: str
    area_mu: float
    crop_type: Optional[str] = "rice"
    variety: Optional[str] = None
    owner_name: Optional[str] = None
    owner_phone: Optional[str] = None
    geom: Optional[str] = None  # GeoJSON格式

class PlotCreate(PlotBase):
    """地块创建模型"""
    pass

class PlotUpdate(BaseModel):
    """地块更新模型"""
    plot_name: Optional[str] = None
    area_mu: Optional[float] = None
    crop_type: Optional[str] = None
    variety: Optional[str] = None
    owner_name: Optional[str] = None
    owner_phone: Optional[str] = None
    geom: Optional[str] = None

class PlotResponse(PlotBase):
    """地块响应模型"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# NDVI相关模型
class NDVIData(BaseModel):
    """NDVI数据模型"""
    observation_date: date
    ndvi_mean: float
    ndvi_min: float
    ndvi_max: float
    cloud_coverage: float
    source: str

class NDVIResponse(NDVIData):
    """NDVI响应模型"""
    id: int
    plot_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# 气象数据模型
class WeatherData(BaseModel):
    """气象数据模型"""
    observation_date: date
    temperature_max: float
    temperature_min: float
    precipitation: float
    sunshine_hours: float
    humidity: float
    wind_speed: float

class WeatherResponse(WeatherData):
    """气象数据响应模型"""
    id: int
    plot_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# 产量预测模型
class YieldPrediction(BaseModel):
    """产量预测模型"""
    prediction_date: date
    expected_harvest_date: date
    predicted_yield_kg_mu: float
    confidence_level: float
    growth_stage: str
    risk_level: int

class YieldPredictionResponse(YieldPrediction):
    """产量预测响应模型"""
    id: int
    plot_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# 病虫害风险模型
class DiseaseRisk(BaseModel):
    """病虫害风险模型"""
    detection_date: date
    disease_type: str
    risk_level: int
    confidence: float
    affected_area_percent: float
    recommendation: str

class DiseaseRiskResponse(DiseaseRisk):
    """病虫害风险响应模型"""
    id: int
    plot_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# 分析响应模型
class PlotAnalysisResponse(BaseModel):
    """地块分析响应模型"""
    plot_id: str
    plot_name: str
    ndvi_latest: Optional[float] = None
    predicted_yield: Optional[float] = None
    risk_level: Optional[int] = None
    disease_risk: Optional[str] = None
    recommendation: Optional[str] = None

class WeeklyReportResponse(BaseModel):
    """周报响应模型"""
    report_date: date
    total_plots: int
    high_risk_plots: int
    average_yield: float
    plots: List[PlotAnalysisResponse]

# 通用响应模型
class Response(BaseModel):
    """通用响应模型"""
    code: int = 0
    message: str = "success"
    data: Optional[Any] = None