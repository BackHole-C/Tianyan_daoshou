#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
消息生成器
功能：生成飞书消息内容，包括预警消息、周报、保险风险简报等
"""

import os
from jinja2 import Template
from loguru import logger
from datetime import datetime

class MessageGenerator:
    def __init__(self, config):
        """初始化消息生成器"""
        self.config = config
        self.alert_template = config['alert_template']
        self.weekly_report_template = config['weekly_report_template']
        self.insurance_report_template = config['insurance_report_template']
        
        # 加载模板
        self.templates = self._load_templates()
        
        logger.info("消息生成器初始化完成")
    
    def _load_templates(self):
        """加载模板"""
        templates = {}
        
        # 加载预警模板
        alert_template_path = os.path.join("templates", "alert_template.md")
        if os.path.exists(alert_template_path):
            with open(alert_template_path, 'r', encoding='utf-8') as f:
                templates['alert'] = Template(f.read())
        else:
            templates['alert'] = Template(self._get_default_alert_template())
        
        # 加载周报模板
        weekly_report_template_path = os.path.join("templates", "weekly_report_template.md")
        if os.path.exists(weekly_report_template_path):
            with open(weekly_report_template_path, 'r', encoding='utf-8') as f:
                templates['weekly_report'] = Template(f.read())
        else:
            templates['weekly_report'] = Template(self._get_default_weekly_report_template())
        
        # 加载保险风险简报模板
        insurance_report_template_path = os.path.join("templates", "insurance_report_template.md")
        if os.path.exists(insurance_report_template_path):
            with open(insurance_report_template_path, 'r', encoding='utf-8') as f:
                templates['insurance_report'] = Template(f.read())
        else:
            templates['insurance_report'] = Template(self._get_default_insurance_report_template())
        
        return templates
    
    def generate_alert_message(self, plot):
        """生成预警消息"""
        try:
            # 构建消息数据
            data = {
                'plot_name': plot['plot_name'],
                'plot_id': plot['plot_id'],
                'risk_level': plot['risk_level'],
                'risk_description': self._get_risk_description(plot['risk_level']),
                'ndvi_value': plot.get('ndvi_mean', 'N/A'),
                'yield_prediction': plot.get('predicted_yield', 'N/A'),
                'recommendation': plot.get('recommendation', '请咨询专业人员'),
                'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # 生成消息内容
            content = self.templates['alert'].render(**data)
            
            # 构建飞书消息
            message = {
                'msg_type': 'interactive',
                'content': {
                    'config': {
                        'wide_screen_mode': True
                    },
                    'elements': [
                        {
                            'tag': 'markdown',
                            'content': content
                        },
                        {
                            'tag': 'action',
                            'actions': [
                                {
                                    'tag': 'button',
                                    'text': {
                                        'content': '确认收到',
                                        'tag': 'plain_text'
                                    },
                                    'type': 'primary'
                                },
                                {
                                    'tag': 'button',
                                    'text': {
                                        'content': '申请现场查勘',
                                        'tag': 'plain_text'
                                    },
                                    'type': 'default'
                                }
                            ]
                        }
                    ]
                }
            }
            
            return message
            
        except Exception as e:
            logger.error(f"生成预警消息失败: {str(e)}")
            return None
    
    def generate_weekly_report(self, plots_data):
        """生成周报"""
        try:
            # 构建消息数据
            data = {
                'report_date': datetime.now().strftime('%Y-%m-%d'),
                'plots': plots_data,
                'total_plots': len(plots_data),
                'high_risk_plots': sum(1 for p in plots_data if p.get('risk_level', 1) >= 3),
                'average_yield': sum(p.get('predicted_yield', 0) for p in plots_data) / max(1, len(plots_data))
            }
            
            # 生成消息内容
            content = self.templates['weekly_report'].render(**data)
            
            # 构建飞书消息
            message = {
                'msg_type': 'interactive',
                'content': {
                    'config': {
                        'wide_screen_mode': True
                    },
                    'elements': [
                        {
                            'tag': 'markdown',
                            'content': content
                        }
                    ]
                }
            }
            
            return message
            
        except Exception as e:
            logger.error(f"生成周报失败: {str(e)}")
            return None
    
    def generate_insurance_report(self, plot_data):
        """生成保险风险简报"""
        try:
            # 构建消息数据
            data = {
                'plot_name': plot_data['plot_name'],
                'plot_id': plot_data['plot_id'],
                'area_mu': plot_data['area_mu'],
                'risk_level': plot_data.get('risk_level', 1),
                'risk_description': self._get_risk_description(plot_data.get('risk_level', 1)),
                'predicted_yield': plot_data.get('predicted_yield', 'N/A'),
                'historical_yield': plot_data.get('historical_yield', 'N/A'),
                'premium_suggestion': plot_data.get('premium_suggestion', '请咨询保险专员'),
                'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # 生成消息内容
            content = self.templates['insurance_report'].render(**data)
            
            # 构建飞书消息
            message = {
                'msg_type': 'interactive',
                'content': {
                    'config': {
                        'wide_screen_mode': True
                    },
                    'elements': [
                        {
                            'tag': 'markdown',
                            'content': content
                        }
                    ]
                }
            }
            
            return message
            
        except Exception as e:
            logger.error(f"生成保险风险简报失败: {str(e)}")
            return None
    
    def _get_risk_description(self, risk_level):
        """获取风险等级描述"""
        descriptions = {
            1: '正常',
            2: '关注',
            3: '警告',
            4: '危险'
        }
        return descriptions.get(risk_level, '未知')
    
    def _get_default_alert_template(self):
        """默认预警模板"""
        return """## 🌾 【风险预警】{{ plot_name }}

**地块编号**：{{ plot_id }}
**风险等级**：{% if risk_level == 4 %}🔴 危险{% elif risk_level == 3 %}🟠 警告{% elif risk_level == 2 %}🟡 关注{% else %}🟢 正常{% endif %}
**当前NDVI**：{{ ndvi_value }}
**预测产量**：{{ yield_prediction }} 斤/亩

**风险描述**：{{ risk_description }}

**建议措施**：{{ recommendation }}

**预警时间**：{{ current_time }}
"""
    
    def _get_default_weekly_report_template(self):
        """默认周报模板"""
        return """## 📊 【农情周报】{{ report_date }}

**本周概况**：
- 监测地块：{{ total_plots }} 个
- 高风险地块：{{ high_risk_plots }} 个
- 平均预测产量：{{ "%.1f"|format(average_yield) }} 斤/亩

**地块详情**：
{% for plot in plots %}
- **{{ plot.plot_name }}** ({{ plot.plot_id }})
  - 风险等级：{% if plot.risk_level == 4 %}🔴 危险{% elif plot.risk_level == 3 %}🟠 警告{% elif plot.risk_level == 2 %}🟡 关注{% else %}🟢 正常{% endif %}
  - 预测产量：{{ plot.predicted_yield }} 斤/亩
  - 建议措施：{{ plot.recommendation }}
{% endfor %}

**下周重点**：
- 继续监测高风险地块
- 关注天气变化对作物生长的影响
- 及时采取防治措施
"""
    
    def _get_default_insurance_report_template(self):
        """默认保险风险简报模板"""
        return """## 📋 【保险风险简报】{{ plot_name }}

**地块信息**：
- 地块编号：{{ plot_id }}
- 地块面积：{{ area_mu }} 亩
- 风险等级：{% if risk_level == 4 %}🔴 危险{% elif risk_level == 3 %}🟠 警告{% elif risk_level == 2 %}🟡 关注{% else %}🟢 正常{% endif %}

**产量情况**：
- 预测产量：{{ predicted_yield }} 斤/亩
- 历史产量：{{ historical_yield }} 斤/亩

**保费建议**：{{ premium_suggestion }}

**评估时间**：{{ current_time }}
"""