#!/usr/bin/env python3.8

import os
import logging
import requests
from api import MessageApiClient
from event import MessageReceiveEvent, UrlVerificationEvent, EventManager
from flask import Flask, jsonify
from dotenv import load_dotenv, find_dotenv
from qianwen_ai import QianWenAI

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

load_dotenv(find_dotenv())

app = Flask(__name__)

APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")
VERIFICATION_TOKEN = os.getenv("VERIFICATION_TOKEN")
ENCRYPT_KEY = os.getenv("ENCRYPT_KEY")
LARK_HOST = os.getenv("LARK_HOST")
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

message_api_client = MessageApiClient(APP_ID, APP_SECRET, LARK_HOST)
event_manager = EventManager()

ai_client = None
if DASHSCOPE_API_KEY:
    ai_client = QianWenAI(DASHSCOPE_API_KEY)
    logging.info("通义千问AI客户端初始化成功")
else:
    logging.warning("未配置DASHSCOPE_API_KEY，AI功能将不可用")


@event_manager.register("url_verification")
def request_url_verify_handler(req_data: UrlVerificationEvent):
    if req_data.event.token != VERIFICATION_TOKEN:
        raise Exception("VERIFICATION_TOKEN is invalid")
    return jsonify({"challenge": req_data.event.challenge})


@event_manager.register("im.message.receive_v1")
def message_receive_event_handler(req_data: MessageReceiveEvent):
    sender_id = req_data.event.sender.sender_id
    message = req_data.event.message
    logging.info(f"收到消息: chat_type={message.chat_type}, message_type={message.message_type}")
    logging.info(f"消息内容: {message.content}")

    if message.message_type != "text":
        logging.warn("暂不支持非文本消息")
        return jsonify()

    import json
    content = json.loads(message.content)
    user_text = content.get("text", "").strip()

    if not user_text:
        return jsonify()

    logging.info(f"用户输入: {user_text}")

    ai_response = None
    if ai_client:
        try:
            logging.info("正在调用通义千问AI...")
            ai_response = ai_client.get_response(user_text)
            logging.info(f"AI回复: {ai_response}")
        except Exception as e:
            logging.error(f"AI调用失败: {str(e)}")
            ai_response = "抱歉，AI服务暂时不可用，请稍后重试。"
    else:
        ai_response = "AI功能未启用，请联系管理员配置API密钥。"
        if message.chat_type == "group":
            message_api_client.send_text_with_chat_id(message.chat_id, json.dumps({"text": ai_response}))
        else:
            message_api_client.send_text_with_open_id(sender_id.open_id, json.dumps({"text": ai_response}))
        return jsonify()

    try:
        if message.chat_type == "group":
            message_api_client.send_text_with_chat_id(message.chat_id, json.dumps({"text": ai_response}))
        else:
            message_api_client.send_text_with_open_id(sender_id.open_id, json.dumps({"text": ai_response}))
        logging.info("消息发送成功")
    except Exception as e:
        logging.error(f"发送消息失败: {str(e)}")
        logging.error(f"错误类型: {e.__class__.__name__}")

    return jsonify()


@app.errorhandler
def msg_error_handler(ex):
    logging.error(ex)
    response = jsonify(message=str(ex))
    response.status_code = (
        ex.response.status_code if isinstance(ex, requests.HTTPError) else 500
    )
    return response


@app.route("/", methods=["POST"])
def callback_event_handler():
    event_handler, event = event_manager.get_handler_with_event(VERIFICATION_TOKEN, ENCRYPT_KEY)
    return event_handler(event)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
