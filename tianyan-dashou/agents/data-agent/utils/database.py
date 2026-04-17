#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库管理器
功能：连接数据库、存储和查询数据
"""

import psycopg2
from sqlalchemy import create_engine, text
from loguru import logger

class DatabaseManager:
    def __init__(self, config):
        """初始化数据库管理器"""
        self.config = config
        self.postgres_url = config['postgres']['url']
        self.timescale_enabled = config.get('timescale', {}).get('enabled', False)
        
        # 初始化数据库连接
        self.engine = create_engine(self.postgres_url)
        self.connection = None
        self.cursor = None
        
        # 初始化表结构
        self._init_tables()
    
    def _init_tables(self):
        """初始化数据库表结构"""
        try:
            with self.engine.connect() as conn:
                # 创建地块表
                conn.execute(text('''
                    CREATE TABLE IF NOT EXISTS plot_base (
                        id SERIAL PRIMARY KEY,
                        plot_id VARCHAR(50) UNIQUE NOT NULL,
                        plot_name VARCHAR(100),
                        area_mu DECIMAL(10,2),
                        crop_type VARCHAR(20),
                        variety VARCHAR(50),
                        owner_name VARCHAR(50),
                        owner_phone VARCHAR(20),
                        geom GEOMETRY(Polygon, 4326),
                        created_at TIMESTAMP DEFAULT NOW(),
                        updated_at TIMESTAMP DEFAULT NOW()
                    )
                '''))
                
                # 创建NDVI时序表
                conn.execute(text('''
                    CREATE TABLE IF NOT EXISTS plot_ndvi_timeseries (
                        id BIGSERIAL,
                        plot_id VARCHAR(50) NOT NULL,
                        observation_date DATE NOT NULL,
                        ndvi_mean DECIMAL(5,4),
                        ndvi_min DECIMAL(5,4),
                        ndvi_max DECIMAL(5,4),
                        cloud_coverage DECIMAL(5,2),
                        source VARCHAR(50),
                        created_at TIMESTAMP DEFAULT NOW(),
                        UNIQUE(plot_id, observation_date)
                    )
                '''))
                
                # 创建气象数据表
                conn.execute(text('''
                    CREATE TABLE IF NOT EXISTS plot_weather_data (
                        id SERIAL PRIMARY KEY,
                        plot_id VARCHAR(50) NOT NULL,
                        observation_date DATE NOT NULL,
                        temperature_max DECIMAL(5,2),
                        temperature_min DECIMAL(5,2),
                        precipitation DECIMAL(5,2),
                        sunshine_hours DECIMAL(5,2),
                        humidity DECIMAL(5,2),
                        wind_speed DECIMAL(5,2),
                        created_at TIMESTAMP DEFAULT NOW(),
                        UNIQUE(plot_id, observation_date)
                    )
                '''))
                
                # 创建产量预测表
                conn.execute(text('''
                    CREATE TABLE IF NOT EXISTS plot_yield_prediction (
                        id SERIAL PRIMARY KEY,
                        plot_id VARCHAR(50) NOT NULL,
                        prediction_date DATE NOT NULL,
                        expected_harvest_date DATE,
                        predicted_yield_kg_mu DECIMAL(10,2),
                        confidence_level DECIMAL(5,2),
                        growth_stage VARCHAR(20),
                        risk_level INTEGER CHECK (risk_level BETWEEN 1 AND 4),
                        PRIMARY KEY(plot_id, prediction_date)
                    )
                '''))
                
                conn.commit()
                logger.info("数据库表结构初始化完成")
                
        except Exception as e:
            logger.error(f"初始化数据库表结构失败: {str(e)}")
    
    def insert_ndvi_timeseries(self, plot_id, timeseries):
        """插入NDVI时序数据"""
        try:
            with self.engine.connect() as conn:
                for item in timeseries:
                    conn.execute(text('''
                        INSERT INTO plot_ndvi_timeseries 
                        (plot_id, observation_date, ndvi_mean, ndvi_min, ndvi_max, cloud_coverage, source)
                        VALUES (:plot_id, :observation_date, :ndvi_mean, :ndvi_min, :ndvi_max, :cloud_coverage, :source)
                        ON CONFLICT (plot_id, observation_date) DO UPDATE
                        SET ndvi_mean = EXCLUDED.ndvi_mean,
                            ndvi_min = EXCLUDED.ndvi_min,
                            ndvi_max = EXCLUDED.ndvi_max,
                            cloud_coverage = EXCLUDED.cloud_coverage,
                            source = EXCLUDED.source
                    '''), {
                        'plot_id': plot_id,
                        'observation_date': item['date'],
                        'ndvi_mean': item['ndvi'],
                        'ndvi_min': item['ndvi'] - 0.1,
                        'ndvi_max': item['ndvi'] + 0.1,
                        'cloud_coverage': item.get('cloud_coverage', 0),
                        'source': 'Sentinel-2'
                    })
                conn.commit()
        except Exception as e:
            logger.error(f"插入NDVI时序数据失败: {str(e)}")
    
    def insert_weather_data(self, plot_id, weather_data):
        """插入气象数据"""
        try:
            with self.engine.connect() as conn:
                for item in weather_data:
                    conn.execute(text('''
                        INSERT INTO plot_weather_data 
                        (plot_id, observation_date, temperature_max, temperature_min, 
                         precipitation, sunshine_hours, humidity, wind_speed)
                        VALUES (:plot_id, :observation_date, :temperature_max, :temperature_min, 
                                :precipitation, :sunshine_hours, :humidity, :wind_speed)
                        ON CONFLICT (plot_id, observation_date) DO UPDATE
                        SET temperature_max = EXCLUDED.temperature_max,
                            temperature_min = EXCLUDED.temperature_min,
                            precipitation = EXCLUDED.precipitation,
                            sunshine_hours = EXCLUDED.sunshine_hours,
                            humidity = EXCLUDED.humidity,
                            wind_speed = EXCLUDED.wind_speed
                    '''), {
                        'plot_id': plot_id,
                        'observation_date': item['date'],
                        'temperature_max': item['temperature_max'],
                        'temperature_min': item['temperature_min'],
                        'precipitation': item['precipitation'],
                        'sunshine_hours': item['sunshine_hours'],
                        'humidity': item['humidity'],
                        'wind_speed': item['wind_speed']
                    })
                conn.commit()
        except Exception as e:
            logger.error(f"插入气象数据失败: {str(e)}")
    
    def commit(self):
        """提交事务"""
        pass  # SQLAlchemy自动管理事务
    
    def close(self):
        """关闭数据库连接"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()