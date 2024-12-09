# backend/feedback.py

import os
from flask import jsonify
from utils import wrapSuccess, wrapFailData, logMessage
from utils import saveFeedback, loadFeedbacks, wrapSuccess, wrapFailData, logMessage
import json

FEEDBACK_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "feedback.json"))


def submitFeedback(feedback):
    """
    保存用户反馈到文件。

    参数:
        feedback (dict): 反馈内容，包括用户ID、评分、评论等。

    返回:
        dict: API响应。
    """
    try:
        if not os.path.exists(FEEDBACK_FILE):
            with open(FEEDBACK_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=4)

        with open(FEEDBACK_FILE, 'r+', encoding='utf-8') as f:
            data = json.load(f)
            data.append(feedback)
            f.seek(0)
            json.dump(data, f, ensure_ascii=False, indent=4)

        logMessage(f"收到反馈: {feedback}")
        return wrapSuccess({"message": "反馈提交成功，谢谢您的宝贵意见！"})
    except Exception as e:
        logMessage(f"反馈提交失败: {e}")
        return wrapFailData(**{
            "status": "fail",
            "errorCode": 2,
            "errorMessage": "反馈提交失败，请稍后再试。"
        })
    

def submitFeedback(feedback):
    """
    保存用户反馈。

    参数:
        feedback (dict): 反馈内容，包括用户ID、评分、评论等。

    返回:
        dict: API响应。
    """
    try:
        # 使用 utils.py 中的 saveFeedback 函数
        saveFeedback(feedback)
        logMessage(f"收到反馈: {feedback}")
        return wrapSuccess({"message": "反馈提交成功，谢谢您的宝贵意见！"})
    except Exception as e:
        logMessage(f"反馈提交失败: {e}")
        return wrapFailData(**{
            "status": "fail",
            "errorCode": 2,
            "errorMessage": "反馈提交失败，请稍后再试。"
        })

def getFeedbacks():
    """
    获取所有反馈信息。

    返回:
        dict: 包含反馈列表的响应。
    """
    try:
        feedbacks = loadFeedbacks()
        return wrapSuccess({"feedbacks": feedbacks})
    except Exception as e:
        logMessage(f"获取反馈信息失败: {e}")
        return wrapFailData(**{
            "status": "fail",
            "errorCode": 3,
            "errorMessage": "获取反馈信息失败，请稍后再试。"
        })
