#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
产量预测器
功能：基于NDVI和气象数据预测产量
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import StandardScaler
from loguru import logger

class YieldPredictor:
    def __init__(self, config):
        """初始化产量预测器"""
        self.config = config
        self.model_type = config['model_type']
        self.input_features = config['input_features']
        self.output_features = config['output_features']
        
        # 初始化模型
        self.model = self._initialize_model()
        self.scaler = StandardScaler()
        
        logger.info(f"产量预测器初始化完成，模型类型: {self.model_type}")
    
    def _initialize_model(self):
        """初始化预测模型"""
        if self.model_type == 'linear':
            return LinearRegression()
        elif self.model_type == 'ridge':
            return Ridge(alpha=1.0)
        elif self.model_type == 'lstm':
            # 这里使用简单模型作为占位符
            # 实际项目中需要实现LSTM模型
            return LinearRegression()
        else:
            return LinearRegression()
    
    def predict(self, ndvi_data, weather_data):
        """预测产量"""
        try:
            # 准备特征数据
            features = self._extract_features(ndvi_data, weather_data)
            
            # 模拟预测结果
            # 实际项目中需要使用训练好的模型进行预测
            predicted_yield = self._mock_prediction(features)
            
            # 计算置信区间
            confidence_interval = self._calculate_confidence_interval(predicted_yield)
            
            prediction = {
                'prediction_date': pd.Timestamp.now().strftime('%Y-%m-%d'),
                'expected_harvest_date': (pd.Timestamp.now() + pd.DateOffset(days=60)).strftime('%Y-%m-%d'),
                'predicted_yield': predicted_yield,
                'confidence_level': 0.85,
                'confidence_interval': confidence_interval,
                'growth_stage': '抽穗期',  # 模拟生长阶段
                'risk_level': self._calculate_risk_level(predicted_yield)
            }
            
            return prediction
            
        except Exception as e:
            logger.error(f"产量预测失败: {str(e)}")
            return None
    
    def _extract_features(self, ndvi_data, weather_data):
        """提取特征"""
        # 转换为DataFrame
        ndvi_df = pd.DataFrame(ndvi_data)
        weather_df = pd.DataFrame(weather_data)
        
        # 计算NDVI特征
        ndvi_features = {
            'ndvi_mean': ndvi_df['ndvi'].mean(),
            'ndvi_peak': ndvi_df['ndvi'].max(),
            'ndvi_slope': self._calculate_slope(ndvi_df['ndvi'])
        }
        
        # 计算气象特征
        weather_features = {
            'cum_temp': weather_df['temperature_max'].sum(),
            'cum_rainfall': weather_df['precipitation'].sum()
        }
        
        # 合并特征
        features = {**ndvi_features, **weather_features}
        features['area_mu'] = 50.5  # 模拟地块面积
        
        return features
    
    def _calculate_slope(self, values):
        """计算斜率"""
        if len(values) < 2:
            return 0
        x = np.arange(len(values))
        slope = np.polyfit(x, values, 1)[0]
        return slope
    
    def _mock_prediction(self, features):
        """模拟预测"""
        # 基于NDVI均值和积温模拟产量
        ndvi_mean = features['ndvi_mean']
        cum_temp = features['cum_temp']
        
        # 简单的线性模型
        base_yield = 500  # 基础产量
        ndvi_factor = (ndvi_mean - 0.5) * 200  # NDVI影响
        temp_factor = (cum_temp - 1000) * 0.1  # 积温影响
        
        predicted_yield = base_yield + ndvi_factor + temp_factor
        
        # 确保产量在合理范围内
        predicted_yield = max(300, min(800, predicted_yield))
        
        return round(predicted_yield, 2)
    
    def _calculate_confidence_interval(self, predicted_yield):
        """计算置信区间"""
        # 简单模拟置信区间
        margin = predicted_yield * 0.15  # 15%的误差范围
        return {
            'lower': round(predicted_yield - margin, 2),
            'upper': round(predicted_yield + margin, 2)
        }
    
    def _calculate_risk_level(self, predicted_yield):
        """计算风险等级"""
        # 基于预测产量计算风险等级
        if predicted_yield > 600:
            return 1  # 低风险
        elif predicted_yield > 500:
            return 2  # 中低风险
        elif predicted_yield > 400:
            return 3  # 中高风险
        else:
            return 4  # 高风险