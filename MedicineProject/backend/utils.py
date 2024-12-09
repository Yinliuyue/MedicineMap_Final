import logging
import json
import os
from datetime import datetime
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import base64

load_dotenv()

# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 读取环境变量
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', '').strip()

# 打印密钥值和长度
print(f"ENCRYPTION_KEY: '{ENCRYPTION_KEY}'")
print(f"Length of ENCRYPTION_KEY: {len(ENCRYPTION_KEY)}")

# 如果密钥为空，则退出
if not ENCRYPTION_KEY:
    print("ENCRYPTION_KEY 未设置或为空，程序退出。")
    raise ValueError("ENCRYPTION_KEY is required.")

# 检查并修复 Base64 格式（如果需要）
if len(ENCRYPTION_KEY) % 4 != 0:
    ENCRYPTION_KEY += '=' * (4 - len(ENCRYPTION_KEY) % 4)

try:
    decoded_key = base64.b64decode(ENCRYPTION_KEY.encode(), validate=True)
    print("ENCRYPTION_KEY is a valid Base64 encoded string")
except Exception as e:
    print(f"Base64 decoding failed: {e}")




try:
    # 初始化 Fernet
    fernet = Fernet(ENCRYPTION_KEY)
    print("Fernet 初始化成功")
except ValueError as e:
    print("Fernet 初始化失败，请检查 ENCRYPTION_KEY 是否有效:", e)
    raise

def logMessage(message):
    """记录日志信息"""
    logging.info(message)

def wrapSuccess(data):
    """封装成功响应"""
    return {
        "status": "success",
        "data": data
    }

def wrapFailData(**kwargs):
    """封装失败响应"""
    return kwargs

def encrypt_data(data):
    """加密数据"""
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(token):
    """解密数据"""
    return fernet.decrypt(token.encode()).decode()

def saveFeedback(feedback_data):
    """将反馈信息保存到文件（或数据库）"""

    # 对敏感信息进行加密
    if 'contact_info' in feedback_data and feedback_data['contact_info']:
        feedback_data['contact_info'] = encrypt_data(feedback_data['contact_info'])

    feedback_file = os.path.join(os.path.dirname(__file__), 'feedbacks.json')

    # 读取现有的反馈数据
    if os.path.exists(feedback_file):
        with open(feedback_file, 'r', encoding='utf-8') as f:
            feedbacks = json.load(f)
    else:
        feedbacks = []

    # 添加新的反馈
    feedbacks.append(feedback_data)

    # 保存到文件
    with open(feedback_file, 'w', encoding='utf-8') as f:
        json.dump(feedbacks, f, ensure_ascii=False, indent=4)

def loadFeedbacks():
    """加载并解密反馈信息"""
    feedback_file = os.path.join(os.path.dirname(__file__), 'feedbacks.json')

    if not os.path.exists(feedback_file):
        return []

    with open(feedback_file, 'r', encoding='utf-8') as f:
        feedbacks = json.load(f)

    # 解密敏感信息
    for feedback in feedbacks:
        if 'contact_info' in feedback and feedback['contact_info']:
            try:
                feedback['contact_info'] = decrypt_data(feedback['contact_info'])
            except Exception as e:
                logMessage(f"解密 contact_info 时发生错误：{e}")
                feedback['contact_info'] = "[解密失败]"

    return feedbacks