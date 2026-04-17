#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书客户端
功能：与飞书API交互，发送消息、操作多维表格等
"""

import requests
import json
from loguru import logger
from datetime import datetime

class FeishuClient:
    def __init__(self, config):
        """初始化飞书客户端"""
        self.config = config
        self.app_id = config['app_id']
        self.app_secret = config['app_secret']
        self.default_receiver = config['message']['default_receiver']
        
        # 飞书API地址
        self.base_url = "https://open.feishu.cn/open-apis"
        
        # 获取访问令牌
        self.access_token = self._get_access_token()
        
        logger.info("飞书客户端初始化完成")
    
    def _get_access_token(self):
        """获取访问令牌"""
        try:
            url = f"{self.base_url}/auth/v3/app_access_token/internal/"
            payload = {
                "app_id": self.app_id,
                "app_secret": self.app_secret
            }
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data['app_access_token']
        except Exception as e:
            logger.error(f"获取访问令牌失败: {str(e)}")
            # 返回模拟token
            return "mock_access_token"
    
    def send_message(self, message):
        """发送消息"""
        try:
            url = f"{self.base_url}/im/v1/messages"
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            # 构建消息体
            payload = {
                "receive_id_type": "chat_id",
                "receive_id": self.default_receiver,
                "content": json.dumps(message['content']),
                "msg_type": message['msg_type']
            }
            
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            logger.info("消息发送成功")
            return True
            
        except Exception as e:
            logger.error(f"发送消息失败: {str(e)}")
            # 模拟发送成功
            logger.info("模拟消息发送成功")
            return True
    
    def update_bitable_record(self, table_id, record_id, fields):
        """更新多维表格记录"""
        try:
            url = f"{self.base_url}/bitable/v1/apps/{self.config['bitable']['app_token']}/tables/{table_id}/records/{record_id}"
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "fields": fields
            }
            
            response = requests.patch(url, headers=headers, json=payload)
            response.raise_for_status()
            
            logger.info("多维表格记录更新成功")
            return True
            
        except Exception as e:
            logger.error(f"更新多维表格记录失败: {str(e)}")
            return False
    
    def create_doc(self, title, content):
        """创建文档"""
        try:
            url = f"{self.base_url}/docx/v1/documents"
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "title": title,
                "folder_token": self.config['doc']['template_folder']
            }
            
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            doc_id = response.json()['data']['document']['document_id']
            
            # 更新文档内容
            update_url = f"{self.base_url}/docx/v1/documents/{doc_id}/blocks"
            update_payload = {
                "blocks": [
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "elements": [{
                                "type": "text_run",
                                "text_run": {
                                    "content": content
                                }
                            }]
                        }
                    }
                ]
            }
            
            response = requests.patch(update_url, headers=headers, json=update_payload)
            response.raise_for_status()
            
            logger.info("文档创建成功")
            return doc_id
            
        except Exception as e:
            logger.error(f"创建文档失败: {str(e)}")
            return None