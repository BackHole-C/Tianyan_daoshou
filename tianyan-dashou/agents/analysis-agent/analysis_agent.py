#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析服务 (Analysis Agent)
功能：产量预测、病虫害识别、风险评估
"""

import os
import time
import yaml
import schedule
import numpy as np
import pandas as pd
from loguru import logger
from datetime import datetime, timedelta

# 配置日志
logger.add("../../logs/analysis-agent.log", rotation="7 days", retention="30 days")

# 加载配置
with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# 导入模块
from utils.yield_predictor import YieldPredictor
from utils.disease_detector import DiseaseDetector
from utils.risk_assessor import RiskAssessor
from utils.database import DatabaseManager

class AnalysisAgent:
    def __init__(self):
        """初始化分析代理"""
        # 初始化模型
        self.yield_predictor = YieldPredictor(config['model']['yield_prediction'])
        self.disease_detector = DiseaseDetector(config['model']['disease_detection'])
        self.risk_assessor = RiskAssessor(config['analysis']['risk'])
        
        # 初始化数据库
        self.db_manager = DatabaseManager(config['database'])
        
        # 分析配置
        self.analysis_config = config['analysis']
        
        # 创建输出目录
        self.output_path = config['storage']['output_path']
        os.makedirs(self.output_path, exist_ok=True)
        
        logger.info("Analysis Agent 初始化完成")
    
    def run(self):
        """运行分析服务"""
        logger.info("开始执行分析任务")
        
        try:
            # 1. 获取所有地块
            plots = self.db_manager.get_all_plots()
            logger.info(f"获取到 {len(plots)} 个地块")
            
            # 2. 分析每个地块
            for plot in plots:
                plot_id = plot['plot_id']
                self.process_plot(plot_id)
            
            logger.info("分析任务执行完成")
            
        except Exception as e:
            logger.error(f"分析任务失败: {str(e)}")
            raise
    
    def process_plot(self, plot_id):
        """处理单个地块"""
        logger.info(f"分析地块: {plot_id}")
        
        try:
            # 1. 获取历史NDVI数据
            ndvi_data = self.db_manager.get_ndvi_timeseries(plot_id)
            
            # 2. 获取历史气象数据
            weather_data = self.db_manager.get_weather_data(plot_id)
            
            if not ndvi_data or not weather_data:
                logger.warning(f"地块 {plot_id} 数据不足，跳过分析")
                return
            
            # 3. 产量预测
            yield_prediction = self.yield_predictor.predict(ndvi_data, weather_data)
            if yield_prediction:
                self.db_manager.insert_yield_prediction(plot_id, yield_prediction)
                logger.info(f"产量预测完成: {plot_id}, 预测产量: {yield_prediction['predicted_yield']}")
            
            # 4. 病虫害识别
            disease_risk = self.disease_detector.detect(ndvi_data, weather_data)
            if disease_risk:
                self.db_manager.insert_disease_risk(plot_id, disease_risk)
                logger.info(f"病虫害识别完成: {plot_id}, 风险等级: {disease_risk['risk_level']}")
            
            # 5. 风险评估
            risk_assessment = self.risk_assessor.assess(yield_prediction, disease_risk)
            if risk_assessment:
                self.db_manager.insert_risk_assessment(plot_id, risk_assessment)
                logger.info(f"风险评估完成: {plot_id}, 综合风险等级: {risk_assessment['risk_level']}")
                
        except Exception as e:
            logger.error(f"分析地块 {plot_id} 失败: {str(e)}")

def main():
    """主函数"""
    agent = AnalysisAgent()
    
    # 立即执行一次
    agent.run()
    
    # 设置定时任务
    if config['task']['schedule']['enabled']:
        interval = config['task']['schedule']['interval']
        time_str = config['task']['schedule'].get('time', '10:00')
        
        if interval == 'daily':
            schedule.every().day.at(time_str).do(agent.run)
            logger.info(f"设置每天{time_str}执行分析任务")
        elif interval == 'weekly':
            schedule.every().monday.at(time_str).do(agent.run)
            logger.info(f"设置每周一{time_str}执行分析任务")
        
        # 运行调度器
        while True:
            schedule.run_pending()
            time.sleep(60)

if __name__ == "__main__":
    main()