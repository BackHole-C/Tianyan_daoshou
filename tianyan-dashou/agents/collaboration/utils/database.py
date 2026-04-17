#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
协作服务数据库管理器
功能：从数据库获取协作所需的数据
"""

from sqlalchemy import create_engine, text
from loguru import logger

class DatabaseManager:
    def __init__(self, config):
        """初始化数据库管理器"""
        self.config = config
        self.postgres_url = config['postgres']['url']
        
        # 初始化数据库连接
        self.engine = create_engine(self.postgres_url)
        
        logger.info("协作服务数据库管理器初始化完成")
    
    def get_high_risk_plots(self):
        """获取高风险地块"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text('''
                    SELECT p.plot_id, p.plot_name, p.area_mu, 
                           y.predicted_yield_kg_mu as predicted_yield, 
                           y.risk_level, y.growth_stage
                    FROM plot_base p
                    LEFT JOIN plot_yield_prediction y ON p.plot_id = y.plot_id
                    WHERE y.risk_level >= 3
                    ORDER BY y.risk_level DESC
                '''))
                high_risk_plots = [dict(row) for row in result]
                return high_risk_plots
        except Exception as e:
            logger.error(f"获取高风险地块失败: {str(e)}")
            # 返回模拟数据
            return self._generate_mock_high_risk_plots()
    
    def get_plots_weekly_data(self):
        """获取地块周数据"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text('''
                    SELECT p.plot_id, p.plot_name, p.area_mu, 
                           y.predicted_yield_kg_mu as predicted_yield, 
                           y.risk_level, y.growth_stage
                    FROM plot_base p
                    LEFT JOIN plot_yield_prediction y ON p.plot_id = y.plot_id
                    ORDER BY p.plot_name
                '''))
                plots_data = [dict(row) for row in result]
                return plots_data
        except Exception as e:
            logger.error(f"获取地块周数据失败: {str(e)}")
            # 返回模拟数据
            return self._generate_mock_plots_data()
    
    def get_plot_insurance_data(self, plot_id):
        """获取地块保险相关数据"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text('''
                    SELECT p.plot_id, p.plot_name, p.area_mu, 
                           y.predicted_yield_kg_mu as predicted_yield, 
                           y.risk_level
                    FROM plot_base p
                    LEFT JOIN plot_yield_prediction y ON p.plot_id = y.plot_id
                    WHERE p.plot_id = :plot_id
                '''), {'plot_id': plot_id})
                plot_data = [dict(row) for row in result]
                if plot_data:
                    return plot_data[0]
                return None
        except Exception as e:
            logger.error(f"获取地块保险数据失败: {str(e)}")
            # 返回模拟数据
            return self._generate_mock_insurance_data(plot_id)
    
    def _generate_mock_high_risk_plots(self):
        """生成模拟高风险地块数据"""
        return [
            {
                'plot_id': 'PLOT_001',
                'plot_name': '王大哥-示范田',
                'area_mu': 50.5,
                'predicted_yield': 420.5,
                'risk_level': 3,
                'growth_stage': '抽穗期',
                'recommendation': '立即喷施杀菌剂，控制病虫害'
            }
        ]
    
    def _generate_mock_plots_data(self):
        """生成模拟地块数据"""
        return [
            {
                'plot_id': 'PLOT_001',
                'plot_name': '王大哥-示范田',
                'area_mu': 50.5,
                'predicted_yield': 420.5,
                'risk_level': 3,
                'growth_stage': '抽穗期',
                'recommendation': '立即喷施杀菌剂，控制病虫害'
            },
            {
                'plot_id': 'PLOT_002',
                'plot_name': '李大姐-试验田',
                'area_mu': 30.0,
                'predicted_yield': 580.0,
                'risk_level': 2,
                'growth_stage': '灌浆期',
                'recommendation': '加强田间管理，注意通风'
            }
        ]
    
    def _generate_mock_insurance_data(self, plot_id):
        """生成模拟保险数据"""
        return {
            'plot_id': plot_id,
            'plot_name': '王大哥-示范田',
            'area_mu': 50.5,
            'predicted_yield': 420.5,
            'risk_level': 3,
            'historical_yield': '550斤/亩',
            'premium_suggestion': '建议保费：80元/亩'
        }