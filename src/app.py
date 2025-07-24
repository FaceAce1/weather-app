import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 加载环境变量
from dotenv import load_dotenv
load_dotenv()

# 立即加载配置
import config
config.load_config()  # 在这里就加载配置

import logging

# 初始化日志记录器
logger = logging.getLogger(__name__)

# 现在可以安全地使用配置
print(f"DEBUG配置值: {config.DEBUG}")
print(f"DEBUG类型: {type(config.DEBUG)}")
# 打印配置信息到日志
logger.debug("=== 配置信息 ===")
logger.debug(f"DEBUG = {config.DEBUG}")
logger.debug(f"HOST = {config.HOST}")
logger.debug(f"PORT = {config.PORT}")
logger.debug("===============")

from flask import Flask, request, jsonify, render_template
import utils.weather_api as weather_api

# 获取项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(
    __name__,
    template_folder=os.path.join(PROJECT_ROOT, 'templates'),
    static_folder=os.path.join(PROJECT_ROOT, 'static')
)

# 添加API主机地址的路由
@app.route('/api/host')
def get_api_host():
    return jsonify({'host': config.API_HOST})

@app.route('/')
def index():
    logger.info("提供首页页面")
    return render_template('index.html')

@app.route('/api/get_weather', methods=['POST'])
def get_weather():
    data = request.json
    city = data.get('city', '')
    
    if not city:
        logger.warning("城市名未提供")
        return jsonify({
            'status': 'error',
            'error': '城市名未提供',
            'message': '请输入城市名'
        })
    
    # 获取天气数据
    weather_data = weather_api.get_weather_data(city)
    
    if weather_data.get('error'):
        logger.error(f"获取天气数据失败: {weather_data.get('message')}")
        return jsonify({
            'status': 'error',
            'error': weather_data.get('error', '未知错误'),
            'message': weather_data.get('message', '未能获取天气信息')
        })
    
    logger.info(f"成功获取天气数据: {weather_data}")
    return jsonify({
        'status': 'success',
        'data': weather_data
    })

if __name__ == '__main__':
    # 配置已经在文件顶部加载了
    
    # 启动应用
    logger.info("启动应用")
    logger.info(f"配置详情 - DEBUG: {config.DEBUG}, HOST: {config.HOST}, PORT: {config.PORT}")
    
    # 正确地将字符串转换为布尔值
    debug_value = str(config.DEBUG).lower() if config.DEBUG is not None else "false"
    debug_mode = debug_value in ('true', '1', 'yes', 'on')
    
    logger.info(f"解析后的调试模式: {debug_mode}")
    
    # 设置Flask应用配置
    app_config = {
        'debug': debug_mode,
        'host': config.HOST,
        'port': int(config.PORT) if str(config.PORT).isdigit() else 5000,
    }
    
    # 如果在生产环境中运行，禁用调试模式
    if os.getenv('FLASK_ENV') == 'production' or os.getenv('ENV') == 'prod':
        app_config['debug'] = False
        logger.warning("生产环境禁用调试模式")
    
    logger.info(f"最终应用配置: {app_config}")
    app.run(**app_config)