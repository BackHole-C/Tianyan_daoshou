#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
病虫害检测器
功能：基于NDVI时序突变检测病虫害
"""

import numpy as np
import pandas as pd
from loguru import logger

class DiseaseDetector:
    def __init__(self, config):
        """初始化病虫害检测器"""
        self.config = config
        self.enabled = config['enabled']
        self.models = config['models']
        
        logger.info("病虫害检测器初始化完成")
    
    def detect(self, ndvi_data, weather_data):
        """检测病虫害"""
        try:
            if not self.enabled:
                logger.info("病虫害检测已禁用")
                return None
            
            # 转换为DataFrame
            ndvi_df = pd.DataFrame(ndvi_data)
            weather_df = pd.DataFrame(weather_data)
            
            # 计算NDVI差分
            ndvi_df['ndvi_diff'] = ndvi_df['ndvi'].diff()
            
            # 检测每种病虫害
            disease_risks = []
            for model in self.models:
                risk = self._detect_disease(model, ndvi_df, weather_df)
                if risk:
                    disease_risks.append(risk)
            
            # 综合风险评估
            if disease_risks:
                max_risk = max(disease_risks, key=lambda x: x['risk_level'])
                comprehensive_risk = {
                    'detection_date': pd.Timestamp.now().strftime('%Y-%m-%d'),
                    'disease_type': max_risk['disease_type'],
                    'risk_level': max_risk['risk_level'],
                    'confidence': max_risk['confidence'],
                    'affected_area_percent': max_risk['affected_area_percent'],
                    'recommendation': max_risk['recommendation'],
                    'all_risks': disease_risks
                }
                return comprehensive_risk
            else:
                return {
                    'detection_date': pd.Timestamp.now().strftime('%Y-%m-%d'),
                    'disease_type': '无',
                    'risk_level': 1,
                    'confidence': 0.95,
                    'affected_area_percent': 0,
                    'recommendation': '正常管理',
                    'all_risks': []
                }
                
        except Exception as e:
            logger.error(f"病虫害检测失败: {str(e)}")
            return None
    
    def _detect_disease(self, model, ndvi_df, weather_df):
        """检测特定病虫害"""
        disease_name = model['name']
        threshold = model['threshold']
        window_days = model['window_days']
        
        # 检测NDVI突变
        consecutive_drops = 0
        risk_level = 1
        affected_area = 0
        
        for i in range(1, len(ndvi_df)):
            ndvi_diff = ndvi_df.iloc[i]['ndvi_diff']
            if ndvi_diff < -threshold:
                consecutive_drops += 1
            else:
                consecutive_drops = 0
            
            if consecutive_drops >= window_days:
                risk_level = 3  # 中等风险
                affected_area = min(50, consecutive_drops * 10)  # 估计受影响面积
                break
        
        # 结合气象条件调整风险等级
        weather_risk = self._assess_weather_risk(disease_name, weather_df)
        if weather_risk:
            risk_level = min(4, risk_level + 1)  # 提高风险等级
        
        if risk_level > 1:
            return {
                'disease_type': disease_name,
                'risk_level': risk_level,
                'confidence': 0.7 + (risk_level - 1) * 0.1,
                'affected_area_percent': affected_area,
                'recommendation': self._get_recommendation(disease_name, risk_level)
            }
        else:
            return None
    
    def _assess_weather_risk(self, disease_name, weather_df):
        """评估气象风险"""
        if disease_name == 'rice_blast':
            # 稻瘟病：低温高湿
            avg_temp = weather_df['temperature_max'].mean()
            avg_humidity = weather_df['humidity'].mean()
            return avg_temp < 25 and avg_humidity > 80
        
        elif disease_name == 'sheath_blight':
            # 纹枯病：高温高湿
            avg_temp = weather_df['temperature_max'].mean()
            avg_humidity = weather_df['humidity'].mean()
            return avg_temp > 28 and avg_humidity > 85
        
        elif disease_name == 'brown_planthopper':
            # 褐飞虱：持续高温
            avg_temp = weather_df['temperature_max'].mean()
            return avg_temp > 30
        
        return False
    
    def _get_recommendation(self, disease_name, risk_level):
        """获取防治建议"""
        recommendations = {
            'rice_blast': {
                2: '加强田间管理，注意通风',
                3: '喷施三环唑等杀菌剂',
                4: '立即喷施高效杀菌剂，控制病情蔓延'
            },
            'sheath_blight': {
                2: '及时排水，降低田间湿度',
                3: '喷施井冈霉素等杀菌剂',
                4: '立即喷施高效杀菌剂，控制病情蔓延'
            },
            'brown_planthopper': {
                2: '加强田间调查，监测虫情',
                3: '喷施吡虫啉等杀虫剂',
                4: '立即喷施高效杀虫剂，控制虫口密度'
            }
        }
        
        return recommendations.get(disease_name, {}).get(risk_level, '加强田间管理')