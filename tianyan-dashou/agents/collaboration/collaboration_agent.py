#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
协作服务 (Collaboration)
功能：飞书消息推送、多维表格同步、周报生成
"""

import os
import time
import yaml
import schedule
from loguru import logger
from datetime import datetime, timedelta

# 配置日志
logger.add("../../logs/collaboration-agent.log", rotation="7 days", retention="30 days")

# 加载配置
with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# 导入模块
from utils.feishu_client import FeishuClient
from utils.message_generator import MessageGenerator
from utils.database import DatabaseManager

class CollaborationAgent:
    def __init__(self):
        """初始化协作代理"""
        # 初始化飞书客户端
        self.feishu_client = FeishuClient(config['feishu'])
        
        # 初始化消息生成器
        self.message_generator = MessageGenerator(config['message'])
        
        # 初始化数据库
        self.db_manager = DatabaseManager(config['database'])
        
        # 存储配置
        self.storage_config = config['storage']
        
        # 创建模板目录
        os.makedirs(os.path.join(self.storage_config['templates_path']), exist_ok=True)
        
        logger.info("Collaboration Agent 初始化完成")
    
    def run(self):
        """运行协作服务"""
        logger.info("开始执行协作任务")
        
        try:
            # 1. 检查预警
            self.check_alerts()
            
            # 2. 生成周报（如果是周一）
            if datetime.now().weekday() == 0:  # 0表示周一
                self.generate_weekly_report()
            
            logger.info("协作任务执行完成")
            
        except Exception as e:
            logger.error(f"协作任务失败: {str(e)}")
            raise
    
    def check_alerts(self):
        """检查预警"""
        try:
            # 获取高风险地块
            high_risk_plots = self.db_manager.get_high_risk_plots()
            
            for plot in high_risk_plots:
                # 生成预警消息
                alert_message = self.message_generator.generate_alert_message(plot)
                
                # 发送预警消息
                if alert_message:
                    self.feishu_client.send_message(alert_message)
                    logger.info(f"发送预警消息: {plot['plot_name']}")
        except Exception as e:
            logger.error(f"检查预警失败: {str(e)}")
    
    def generate_weekly_report(self):
        """生成周报"""
        try:
            # 获取所有地块的周数据
            plots_data = self.db_manager.get_plots_weekly_data()
            
            # 生成周报内容
            report_content = self.message_generator.generate_weekly_report(plots_data)
            
            # 发送周报
            if report_content:
                self.feishu_client.send_message(report_content)
                logger.info("发送周报完成")
        except Exception as e:
            logger.error(f"生成周报失败: {str(e)}")
    
    def generate_insurance_report(self, plot_id):
        """生成保险风险简报"""
        try:
            # 获取地块保险相关数据
            plot_data = self.db_manager.get_plot_insurance_data(plot_id)
            
            # 生成保险风险简报
            report_content = self.message_generator.generate_insurance_report(plot_data)
            
            # 发送保险风险简报
            if report_content:
                self.feishu_client.send_message(report_content)
                logger.info(f"发送保险风险简报: {plot_id}")
        except Exception as e:
            logger.error(f"生成保险风险简报失败: {str(e)}")

def main():
    """主函数"""
    agent = CollaborationAgent()
    
    # 立即执行一次
    agent.run()
    
    # 设置定时任务
    if config['task']['weekly_report']['enabled']:
        day = config['task']['weekly_report']['day']
        time_str = config['task']['weekly_report']['time']
        getattr(schedule.every(), day).at(time_str).do(agent.generate_weekly_report)
        logger.info(f"设置每周{day} {time_str}生成周报")
    
    if config['task']['alert_check']['enabled']:
        interval = config['task']['alert_check']['interval']
        if 'minutes' in interval:
            minutes = int(interval.split()[0])
            schedule.every(minutes).minutes.do(agent.check_alerts)
            logger.info(f"设置每{minutes}分钟检查预警")
    
    # 运行调度器
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()