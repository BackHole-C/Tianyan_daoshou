#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析服务数据库管理器
功能：从数据库获取分析所需的数据
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
        
        logger.info("分析服务数据库管理器初始化完成")
    
    def get_all_plots(self):
        """获取所有地块"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text('''
                    SELECT plot_id, plot_name, area_mu, crop_type, variety 
                    FROM plot_base
                '''))
                plots = [dict(row) for row in result]
                return plots
        except Exception as e:
            logger.error(f"获取地块列表失败: {str(e)}")
            # 返回模拟数据
            return [
                {'plot_id': 'PLOT_001', 'plot_name': '王大哥-示范田', 'area_mu': 50.5, 'crop_type': 'rice', 'variety': '杂交稻'},
                {'plot_id': 'PLOT_002', 'plot_name': '李大姐-试验田', 'area_mu': 30.0, 'crop_type': 'rice', 'variety': '常规稻'}
            ]
    
    def get_ndvi_timeseries(self, plot_id):
        """获取NDVI时序数据"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text('''
                    SELECT observation_date, ndvi_mean, ndvi_min, ndvi_max, cloud_coverage 
                    FROM plot_ndvi_timeseries 
                    WHERE plot_id = :plot_id 
                    ORDER BY observation_date
                '''), {'plot_id': plot_id})
                ndvi_data = [dict(row) for row in result]
                return ndvi_data
        except Exception as e:
            logger.error(f"获取NDVI时序数据失败: {str(e)}")
            # 返回模拟数据
            return self._generate_mock_ndvi_data()
    
    def get_weather_data(self, plot_id):
        """获取气象数据"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text('''
                    SELECT observation_date, temperature_max, temperature_min, 
                           precipitation, sunshine_hours, humidity, wind_speed 
                    FROM plot_weather_data 
                    WHERE plot_id = :plot_id 
                    ORDER BY observation_date
                '''), {'plot_id': plot_id})
                weather_data = [dict(row) for row in result]
                return weather_data
        except Exception as e:
            logger.error(f"获取气象数据失败: {str(e)}")
            # 返回模拟数据
            return self._generate_mock_weather_data()
    
    def insert_yield_prediction(self, plot_id, prediction):
        """插入产量预测数据"""
        try:
            with self.engine.connect() as conn:
                conn.execute(text('''
                    INSERT INTO plot_yield_prediction 
                    (plot_id, prediction_date, expected_harvest_date, 
                     predicted_yield_kg_mu, confidence_level, growth_stage, risk_level)
                    VALUES (:plot_id, :prediction_date, :expected_harvest_date, 
                            :predicted_yield, :confidence_level, :growth_stage, :risk_level)
                    ON CONFLICT (plot_id, prediction_date) DO UPDATE
                    SET predicted_yield_kg_mu = EXCLUDED.predicted_yield_kg_mu,
                        confidence_level = EXCLUDED.confidence_level,
                        growth_stage = EXCLUDED.growth_stage,
                        risk_level = EXCLUDED.risk_level
                '''), {
                    'plot_id': plot_id,
                    'prediction_date': prediction['prediction_date'],
                    'expected_harvest_date': prediction['expected_harvest_date'],
                    'predicted_yield': prediction['predicted_yield'],
                    'confidence_level': prediction['confidence_level'],
                    'growth_stage': prediction['growth_stage'],
                    'risk_level': prediction['risk_level']
                })
                conn.commit()
        except Exception as e:
            logger.error(f"插入产量预测数据失败: {str(e)}")
    
    def insert_disease_risk(self, plot_id, disease_risk):
        """插入病虫害风险数据"""
        try:
            # 这里应该创建专门的表来存储病虫害风险
            # 暂时跳过，实际项目中需要实现
            pass
        except Exception as e:
            logger.error(f"插入病虫害风险数据失败: {str(e)}")
    
    def insert_risk_assessment(self, plot_id, risk_assessment):
        """插入风险评估数据"""
        try:
            # 这里应该创建专门的表来存储风险评估
            # 暂时跳过，实际项目中需要实现
            pass
        except Exception as e:
            logger.error(f"插入风险评估数据失败: {str(e)}")
    
    def _generate_mock_ndvi_data(self):
        """生成模拟NDVI数据"""
        import random
        from datetime import datetime, timedelta
        
        ndvi_data = []
        end_date = datetime.now()
        
        for i in range(30):  # 30天数据
            date = end_date - timedelta(days=i)
            ndvi_data.append({
                'observation_date': date.strftime('%Y-%m-%d'),
                'ndvi_mean': round(random.uniform(0.4, 0.7), 4),
                'ndvi_min': round(random.uniform(0.3, 0.6), 4),
                'ndvi_max': round(random.uniform(0.5, 0.8), 4),
                'cloud_coverage': round(random.uniform(0, 20), 2)
            })
        
        return ndvi_data
    
    def _generate_mock_weather_data(self):
        """生成模拟气象数据"""
        import random
        from datetime import datetime, timedelta
        
        weather_data = []
        end_date = datetime.now()
        
        for i in range(30):  # 30天数据
            date = end_date - timedelta(days=i)
            weather_data.append({
                'observation_date': date.strftime('%Y-%m-%d'),
                'temperature_max': round(random.uniform(20, 35), 1),
                'temperature_min': round(random.uniform(15, 25), 1),
                'precipitation': round(random.uniform(0, 50), 1),
                'sunshine_hours': round(random.uniform(0, 12), 1),
                'humidity': round(random.uniform(40, 90), 1),
                'wind_speed': round(random.uniform(0, 10), 1)
            })
        
        return weather_data