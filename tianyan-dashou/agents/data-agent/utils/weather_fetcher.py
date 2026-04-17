#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
气象数据获取器
功能：从气象API获取温度、降水、日照等数据
"""

import requests
from datetime import datetime, timedelta
from loguru import logger

class WeatherFetcher:
    def __init__(self, config):
        """初始化气象数据获取器"""
        self.config = config
        self.nmc_api_url = config['nmc_api_url']
        self.nmc_api_key = config['nmc_api_key']
        self.qweather_api_url = config['qweather_api_url']
        self.qweather_api_key = config['qweather_api_key']
    
    def fetch_weather(self, lat, lon):
        """获取气象数据"""
        try:
            logger.info(f"获取气象数据，位置: {lat}, {lon}")
            
            # 这里使用模拟数据，实际项目中需要调用真实API
            # 尝试调用国家气象局API
            try:
                weather_data = self._fetch_from_nmc(lat, lon)
            except Exception as e:
                logger.warning(f"调用国家气象局API失败: {str(e)}")
                # 尝试调用和风天气API
                weather_data = self._fetch_from_qweather(lat, lon)
            
            logger.info("气象数据获取完成")
            return weather_data
            
        except Exception as e:
            logger.error(f"获取气象数据失败: {str(e)}")
            return None
    
    def _fetch_from_nmc(self, lat, lon):
        """从国家气象局API获取数据"""
        # 模拟数据
        return self._generate_mock_weather()
    
    def _fetch_from_qweather(self, lat, lon):
        """从和风天气API获取数据"""
        # 模拟数据
        return self._generate_mock_weather()
    
    def _generate_mock_weather(self):
        """生成模拟气象数据"""
        import random
        
        # 生成过去7天的数据
        weather_data = []
        end_date = datetime.now()
        
        for i in range(7):
            date = end_date - timedelta(days=i)
            weather_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'temperature_max': round(random.uniform(20, 35), 1),
                'temperature_min': round(random.uniform(15, 25), 1),
                'precipitation': round(random.uniform(0, 50), 1),
                'sunshine_hours': round(random.uniform(0, 12), 1),
                'humidity': round(random.uniform(40, 90), 1),
                'wind_speed': round(random.uniform(0, 10), 1)
            })
        
        return weather_data