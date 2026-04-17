#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析路由
功能：数据分析相关接口
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime, timedelta

from database import get_db, Plot, YieldPrediction as YieldPredictionModel, NDVI_Timeseries, User
from schemas import PlotAnalysisResponse, WeeklyReportResponse, NDVIResponse, WeatherResponse, YieldPredictionResponse, DiseaseRiskResponse
from routers.auth import get_current_user

router = APIRouter()

@router.get("/plot/{plot_id}", response_model=PlotAnalysisResponse)
def get_plot_analysis(plot_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """获取地块分析"""
    # 获取地块信息
    plot = db.query(Plot).filter(Plot.plot_id == plot_id).first()
    if not plot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plot not found"
        )
    
    # 获取最新NDVI数据
    latest_ndvi = db.query(NDVI_Timeseries).filter(
        NDVI_Timeseries.plot_id == plot_id
    ).order_by(NDVI_Timeseries.observation_date.desc()).first()
    
    # 获取最新产量预测
    latest_yield = db.query(YieldPredictionModel).filter(
        YieldPredictionModel.plot_id == plot_id
    ).order_by(YieldPredictionModel.prediction_date.desc()).first()
    
    # 构建响应
    analysis = PlotAnalysisResponse(
        plot_id=plot.plot_id,
        plot_name=plot.plot_name,
        ndvi_latest=latest_ndvi.ndvi_mean if latest_ndvi else None,
        predicted_yield=latest_yield.predicted_yield_kg_mu if latest_yield else None,
        risk_level=latest_yield.risk_level if latest_yield else None,
        disease_risk="无" if not latest_yield or latest_yield.risk_level <= 2 else "有",
        recommendation="正常管理" if not latest_yield or latest_yield.risk_level <= 2 else "需要采取措施"
    )
    
    return analysis

@router.get("/weekly-report", response_model=WeeklyReportResponse)
def get_weekly_report(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """获取周报"""
    # 获取所有地块
    plots = db.query(Plot).all()
    
    # 分析每个地块
    plot_analyses = []
    high_risk_count = 0
    total_yield = 0
    valid_yield_count = 0
    
    for plot in plots:
        # 获取最新产量预测
        latest_yield = db.query(YieldPredictionModel).filter(
            YieldPredictionModel.plot_id == plot.plot_id
        ).order_by(YieldPredictionModel.prediction_date.desc()).first()
        
        risk_level = latest_yield.risk_level if latest_yield else 1
        if risk_level >= 3:
            high_risk_count += 1
        
        predicted_yield = latest_yield.predicted_yield_kg_mu if latest_yield else 0
        if predicted_yield > 0:
            total_yield += predicted_yield
            valid_yield_count += 1
        
        # 获取最新NDVI
        latest_ndvi = db.query(NDVI_Timeseries).filter(
            NDVI_Timeseries.plot_id == plot.plot_id
        ).order_by(NDVI_Timeseries.observation_date.desc()).first()
        
        plot_analysis = PlotAnalysisResponse(
            plot_id=plot.plot_id,
            plot_name=plot.plot_name,
            ndvi_latest=latest_ndvi.ndvi_mean if latest_ndvi else None,
            predicted_yield=predicted_yield,
            risk_level=risk_level,
            disease_risk="无" if risk_level <= 2 else "有",
            recommendation="正常管理" if risk_level <= 2 else "需要采取措施"
        )
        plot_analyses.append(plot_analysis)
    
    # 计算平均产量
    average_yield = total_yield / valid_yield_count if valid_yield_count > 0 else 0
    
    # 构建周报响应
    weekly_report = WeeklyReportResponse(
        report_date=date.today(),
        total_plots=len(plots),
        high_risk_plots=high_risk_count,
        average_yield=round(average_yield, 2),
        plots=plot_analyses
    )
    
    return weekly_report

@router.get("/ndvi/{plot_id}", response_model=List[NDVIResponse])
def get_ndvi_timeseries(plot_id: str, start_date: Optional[date] = None, end_date: Optional[date] = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """获取NDVI时序数据"""
    query = db.query(NDVI_Timeseries).filter(NDVI_Timeseries.plot_id == plot_id)
    
    if start_date:
        query = query.filter(NDVI_Timeseries.observation_date >= start_date)
    if end_date:
        query = query.filter(NDVI_Timeseries.observation_date <= end_date)
    
    ndvi_data = query.order_by(NDVI_Timeseries.observation_date).all()
    return ndvi_data

@router.get("/yield/{plot_id}", response_model=List[YieldPredictionResponse])
def get_yield_predictions(plot_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """获取产量预测历史"""
    predictions = db.query(YieldPredictionModel).filter(
        YieldPredictionModel.plot_id == plot_id
    ).order_by(YieldPredictionModel.prediction_date.desc()).all()
    return predictions