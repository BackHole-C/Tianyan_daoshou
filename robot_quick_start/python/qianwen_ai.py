#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通义千问AI模块
功能：调用阿里云通义千问API实现智能对话
"""

import os
import json
import logging
import requests

logger = logging.getLogger(__name__)

class QianWenAI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.model = "qwen-turbo"
        self.api_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

    def get_response(self, user_message, system_prompt=None):
        """
        获取AI回复
        :param user_message: 用户消息
        :param system_prompt: 系统提示词
        :return: AI回复内容
        """
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }

            if system_prompt is None:
                system_prompt = """你是一个农业智能助手，名为"天眼稻守"。
你的职责是：
1. 回答关于水稻种植、作物管理的问题
2. 提供农业病虫害识别和防治建议
3. 解答农业保险相关问题
4. 辅助农业管理者进行决策支持
请用简洁、专业的方式回答，如果不确定答案，请说明需要咨询专业人士。"""

            prompt = f"{system_prompt}\n\n用户：{user_message}\n\n助手："

            payload = {
                "model": self.model,
                "input": {
                    "prompt": prompt
                },
                "parameters": {
                    "temperature": 0.7,
                    "max_tokens": 500
                }
            }

            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                if 'output' in result and 'text' in result['output']:
                    return result['output']['text']
                elif 'choices' in result and len(result['choices']) > 0:
                    return result['choices'][0]['text']
                else:
                    logger.error(f"API返回格式异常：{result}")
                    return "抱歉，AI返回格式异常"
            else:
                logger.error(f"API调用失败：{response.status_code} - {response.text}")
                error_msg = response.json().get('error', {}).get('message', '未知错误')
                return f"抱歉，AI服务暂时不可用：{error_msg}"

        except requests.exceptions.Timeout:
            logger.error("AI API调用超时")
            return "抱歉，AI响应超时，请稍后重试"
        except Exception as e:
            logger.error(f"AI调用异常：{str(e)}")
            return f"抱歉，AI服务暂时不可用：{str(e)}"


def create_ai_client():
    """创建AI客户端"""
    api_key = os.getenv("DASHSCOPE_API_KEY") or os.getenv("API_KEY")
    if not api_key:
        logger.warning("未配置DASHSCOPE_API_KEY或API_KEY，AI功能将不可用")
        return None
    return QianWenAI(api_key)
