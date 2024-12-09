from flask import Flask, request, session, jsonify
from flask_cors import CORS
from flask_session import Session
from datetime import datetime
from const import DEFAULT_ANSWER
from views import processQuestion
from questionParser import QuestionParser
from answerSearch import AnswerSearcher
from questionClassifier import QuestionClassifier
from utils import wrapSuccess, wrapFailData, logMessage, saveFeedback, loadFeedbacks
from flask import Flask
from flask_cors import CORS
from flask_session import Session

app = Flask(__name__)

# Session 配置
import os
app.secret_key = os.getenv('SECRET_KEY', '88888888')  # 第二个参数是默认值

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'None'  # 允许跨站点请求携带 Cookies
app.config['SESSION_COOKIE_SECURE'] = True     # 若使用 HTTPS，需设置为 True



# 初始化 Session
# Session(app)

# CORS 配置
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://10.21.169.215:8080"}})


# 初始化处理器
handle = {
    'questionClassifier': QuestionClassifier(),
    'questionParser': QuestionParser(),
    'answerSearcher': AnswerSearcher(),
}


@app.route('/getAnswer', methods=['POST'])
def get_answer():
    """
    主接口：接收前端传来的问题（JSON 格式），处理问题并返回答案。
    """
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({"status": "fail", "message": "Invalid input: 'question' is required"}), 400

    question = data['question']
    logMessage(f"Received data: {data}")

    # 打印当前 Session 状态
    logMessage(f"Current session data: {dict(session)}")

    # 调用问题处理逻辑
    response = processQuestion(handle, question, session)

    # 返回响应
    logMessage(f"Returning response: {response}")
    return jsonify(response)


VALID_FEEDBACK_TYPES = ["功能问题", "错误报告", "体验不好", "性能问题", "其他"]


@app.route('/submitFeedback', methods=['POST'])
def submit_feedback():
    """
    提交用户反馈的接口。
    """
    data = request.get_json()
    user_id = data.get('user_id')
    rating = data.get('rating')
    comment = data.get('comment')
    feedback_type = data.get('feedback_type')  # 新增字段：反馈类型
    contact_info = data.get('contact_info')    # 新增字段：联系方式
    privacy_policy_accepted = data.get('privacy_policy_accepted')  # 新增字段：用户是否同意隐私政策

    if feedback_type not in VALID_FEEDBACK_TYPES:
        return wrapFailData(**{
            "status": "fail",
            "errorCode": 2,
            "errorMessage": "无效的反馈类型。"
        })

    # 验证必要参数
    if not rating or not comment or privacy_policy_accepted is not True:
        return wrapFailData(**{
            "status": "fail",
            "errorCode": 1,
            "errorMessage": "缺少反馈参数或未同意隐私政策。"
        })

    # 构建反馈数据
    feedback_data = {
        "user_id": user_id,
        "rating": rating,
        "comment": comment,
        "feedback_type": feedback_type,
        "contact_info": contact_info,
        "timestamp": datetime.utcnow().isoformat() + 'Z'  # 添加时间戳
    }

    # 保存反馈信息
    saveFeedback(feedback_data)

    # 日志中不记录个人敏感信息
    logMessage(f"收到反馈: {{'rating': {rating}, 'feedback_type': '{feedback_type}'}}")

    return wrapSuccess({
        "message": "反馈提交成功，谢谢您的宝贵意见！"
    })


@app.route('/health', methods=['GET'])
def health_check():
    """
    健康检查接口，返回服务状态。
    """
    return jsonify({"status": "up"})


@app.route('/getFeedbacks', methods=['GET'])
def get_feedbacks():
    """
    获取用户反馈的接口。
    """
    feedbacks = loadFeedbacks()
    return jsonify({
        "status": "success",
        "data": {
            "feedbacks": feedbacks
        }
    })


if __name__ == '__main__':
    app.run(debug=True)
