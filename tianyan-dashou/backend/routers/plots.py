#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
地块路由
功能：地块管理相关接口
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db, Plot, User
from schemas import PlotCreate, PlotUpdate, PlotResponse, NDVIData, WeatherData, YieldPrediction, DiseaseRisk
from routers.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=PlotResponse, status_code=status.HTTP_201_CREATED)
def create_plot(plot: PlotCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """创建地块"""
    # 检查地块ID是否已存在
    db_plot = db.query(Plot).filter(Plot.plot_id == plot.plot_id).first()
    if db_plot:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Plot ID already exists"
        )
    
    # 创建新地块
    db_plot = Plot(
        plot_id=plot.plot_id,
        plot_name=plot.plot_name,
        area_mu=plot.area_mu,
        crop_type=plot.crop_type,
        variety=plot.variety,
        owner_name=plot.owner_name,
        owner_phone=plot.owner_phone,
        geom=plot.geom
    )
    db.add(db_plot)
    db.commit()
    db.refresh(db_plot)
    return db_plot

@router.get("/", response_model=List[PlotResponse])
def get_plots(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """获取地块列表"""
    plots = db.query(Plot).offset(skip).limit(limit).all()
    return plots

@router.get("/{plot_id}", response_model=PlotResponse)
def get_plot(plot_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """获取地块详情"""
    plot = db.query(Plot).filter(Plot.plot_id == plot_id).first()
    if not plot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plot not found"
        )
    return plot

@router.put("/{plot_id}", response_model=PlotResponse)
def update_plot(plot_id: str, plot_update: PlotUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """更新地块"""
    plot = db.query(Plot).filter(Plot.plot_id == plot_id).first()
    if not plot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plot not found"
        )
    
    # 更新地块信息
    if plot_update.plot_name:
        plot.plot_name = plot_update.plot_name
    if plot_update.area_mu:
        plot.area_mu = plot_update.area_mu
    if plot_update.crop_type:
        plot.crop_type = plot_update.crop_type
    if plot_update.variety:
        plot.variety = plot_update.variety
    if plot_update.owner_name:
        plot.owner_name = plot_update.owner_name
    if plot_update.owner_phone:
        plot.owner_phone = plot_update.owner_phone
    if plot_update.geom:
        plot.geom = plot_update.geom
    
    db.commit()
    db.refresh(plot)
    return plot

@router.delete("/{plot_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_plot(plot_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """删除地块"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    plot = db.query(Plot).filter(Plot.plot_id == plot_id).first()
    if not plot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plot not found"
        )
    db.delete(plot)
    db.commit()
    return None