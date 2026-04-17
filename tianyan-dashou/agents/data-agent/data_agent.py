#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据采集服务 (Data Agent)
功能：定时采集Sentinel-2卫星数据、气象数据、地块边界数据
"""

import os
import time
import yaml
import schedule
import logging
from loguru import logger
from datetime import datetime, timedelta

# 配置日志
logger.add("../../logs/data-agent.log", rotation="7 days", retention="30 days")

# 加载配置
with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# 导入模块
from utils.sentinel_downloader import SentinelDownloader
from utils.weather_fetcher import WeatherFetcher
from utils.plot_processor import PlotProcessor
from utils.database import DatabaseManager

class DataAgent:
    def __init__(self):
        """初始化数据采集代理"""
        # 初始化下载器
        self.sentinel_downloader = SentinelDownloader(config['sentinel'])
        self.weather_fetcher = WeatherFetcher(config['weather'])
        self.plot_processor = PlotProcessor(config['plots'])
        
        # 初始化数据库
        self.db_manager = DatabaseManager(config['database'])
        
        # 存储配置
        self.storage_config = config['storage']
        
        logger.info("Data Agent 初始化完成")
    
    def run(self):
        """运行数据采集服务"""
        logger.info("开始执行数据采集任务")
        
        try:
            # 1. 加载地块数据
            plots = self.plot_processor.load_plots()
            logger.info(f"加载到 {len(plots)} 个地块")
            
            # 2. 处理每个地块
            for plot in plots:
                self.process_plot(plot)
                
            # 3. 数据入库
            self.db_manager.commit()
            
            logger.info("数据采集任务执行完成")
            
        except Exception as e:
            logger.error(f"数据采集任务失败: {str(e)}")
            raise
    
    def process_plot(self, plot):
        """处理单个地块"""
        plot_id = plot['properties']['plot_id']
        plot_name = plot['properties']['plot_name']
        
        logger.info(f"处理地块: {plot_name} ({plot_id})")
        
        # 1. 下载卫星数据
        bounds = self.plot_processor.get_plot_bounds(plot)
        imagery_path = self.sentinel_downloader.download(
            bounds=bounds,
            start_date=datetime.now() - timedelta(days=7),
            end_date=datetime.now()
        )
        
        if imagery_path:
            logger.info(f"卫星数据下载完成: {imagery_path}")
            
            # 2. 计算NDVI
            ndvi_data = self.sentinel_downloader.calculate_ndvi(imagery_path)
            if ndvi_data:
                # 3. 提取时序数据
                ndvi_timeseries = self.sentinel_downloader.extract_timeseries(ndvi_data, plot)
                
                # 4. 存储NDVI数据
                self.db_manager.insert_ndvi_timeseries(plot_id, ndvi_timeseries)
                logger.info(f"NDVI数据存储完成: {plot_id}")
        
        # 5. 获取气象数据
        weather_data = self.weather_fetcher.fetch_weather(
            lat=plot['geometry']['coordinates'][0][0][1],
            lon=plot['geometry']['coordinates'][0][0][0]
        )
        
        if weather_data:
            # 6. 存储气象数据
            self.db_manager.insert_weather_data(plot_id, weather_data)
            logger.info(f"气象数据存储完成: {plot_id}")

def main():
    """主函数"""
    agent = DataAgent()
    
    # 立即执行一次
    agent.run()
    
    # 设置定时任务
    if config['task']['schedule']['enabled']:
        interval = config['task']['schedule']['interval']
        day = config['task']['schedule'].get('day', 'monday')
        time_str = config['task']['schedule'].get('time', '09:00')
        
        if interval == 'weekly':
            getattr(schedule.every(), day).at(time_str).do(agent.run)
            logger.info(f"设置每周{day} {time_str}执行数据采集")
        elif interval == 'daily':
            schedule.every().day.at(time_str).do(agent.run)
            logger.info(f"设置每天{time_str}执行数据采集")
        
        # 运行调度器
        while True:
            schedule.run_pending()
            time.sleep(60)

if __name__ == "__main__":
    main()