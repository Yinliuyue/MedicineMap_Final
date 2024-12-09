运行：
1.进入backend文件夹运行app.py
2.进入frontedn文件夹运行run npm serve
每次使用需要将backend/app.py中的CORS路径改为前端运行后路径   
即将CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://10.21.169.215:8080"}})中的http://10.21.169.215:8080改为network路径
