#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
风险评估器
功能：综合评估地块风险等级
"""

from loguru import logger

class RiskAssessor:
    def __init__(self, config):
        """初始化风险评估器"""
        self.config = config
        self.risk_levels = config['levels']
        
        logger.info("风险评估器初始化完成")
    
    def assess(self, yield_prediction, disease_risk):
        """综合评估风险"""
        try:
            # 计算产量风险
            yield_risk = self._assess_yield_risk(yield_prediction)
            
            # 计算病虫害风险
            disease_risk_level = disease_risk.get('risk_level', 1) if disease_risk else 1
            
            # 综合风险等级（取最大值）
            comprehensive_risk_level = max(yield_risk, disease_risk_level)
            
            # 获取风险描述
            risk_description = self._get_risk_description(comprehensive_risk_level)
            
            risk_assessment = {
                'assessment_date': yield_prediction['prediction_date'] if yield_prediction else None,
                'risk_level': comprehensive_risk_level,
                'risk_description': risk_description,
                'yield_risk': yield_risk,
                'disease_risk': disease_risk_level,
                'recommendation': self._get_recommendation(comprehensive_risk_level),
                'confidence': 0.85
            }
            
            return risk_assessment
            
        except Exception as e:
            logger.error(f"风险评估失败: {str(e)}")
            return None
    
    def _assess_yield_risk(self, yield_prediction):
        """评估产量风险"""
        if not yield_prediction:
            return 1  # 默认低风险
        
        predicted_yield = yield_prediction.get('predicted_yield', 500)
        
        # 基于产量水平评估风险
        if predicted_yield > 600:
            return 1  # 低风险
        elif predicted_yield > 500:
            return 2  # 中低风险
        elif predicted_yield > 400:
            return 3  # 中高风险
        else:
            return 4  # 高风险
    
    def _get_risk_description(self, risk_level):
        """获取风险描述"""
        descriptions = {
            1: '正常',
            2: '关注',
            3: '警告',
            4: '危险'
        }
        return descriptions.get(risk_level, '未知')
    
    def _get_recommendation(self, risk_level):
        """获取建议措施"""
        recommendations = {
            1: '正常管理，定期监测',
            2: '加强监测，注意异常变化',
            3: '立即采取措施，防止风险扩大',
            4: '紧急干预，必要时申请保险理赔'
        }
        return recommendations.get(risk_level, '请咨询专业人员')