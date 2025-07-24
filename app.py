import os
import sys
from flask import Flask, request, jsonify, render_template
from utils.config_utils import load_config
from utils.logger_utils import setup_logger
from utils.weather_api import get_weather_data
import urllib.parse

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 初始化Flask应用
app = Flask(__name__, static_folder='static', template_folder='templates')

# 加载配置
config = load_config()

# 设置日志
logger = setup_logger(config)

# 打印配置信息用于调试
logger.debug("Loaded configuration:")
for key, value in config.items():
    if key != 'weather_api':  # 避免打印API密钥
        logger.debug(f"  {key}: {value}")

logger.debug(f"  weather_api: {{'url': '{config.get('weather_api', {}).get('url', 'N/A')}'}}")

@app.route('/')
def index():
    """渲染主页"""
    logger.info("Home page accessed")
    return render_template('index.html')

@app.route('/api/weather', methods=['GET'])
def get_weather():
    # 从URL参数中获取城市名（与前端fetch一致）
    city = request.args.get('city', '').strip()
    
    if not city:
        logger.warning("城市名未提供")
        return jsonify({
            'error': '城市名未提供',
            'message': '请输入城市名'
        }), 400
    
    try:
        # 调用优化后的get_weather_data，获取完整天气数据
        # 包含温度、体感、风向、气压、能见度等所有字段
        weather_data = get_weather_data(city, config)
        logger.info(f"成功获取完整天气数据: {city}")
        return jsonify(weather_data)  # 直接返回原始数据，与前端预期结构一致
    except Exception as e:
        logger.error(f"获取天气数据失败: {str(e)}")
        return jsonify({
            'error': str(e),
            'message': '未能获取天气信息'
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'error',
        'error': 'Not Found',
        'message': '请求的资源不存在'
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'status': 'error',
        'error': 'Method Not Allowed',
        'message': '不支持的请求方法'
    }), 405

if __name__ == '__main__':
    host = config.get('server', {}).get('host', '127.0.0.1')
    port = config.get('server', {}).get('port', 5001)
    
    # 确保端口是整数
    try:
        port = int(port)
    except (ValueError, TypeError):
        port = 5001
        logger.warning(f"Invalid port value, using default: {port}")
    
    logger.info(f"Starting server on {host}:{port}")
    # 生产环境强制关闭调试模式
    debug_mode = config.get('debug', False)
    if os.getenv('FLASK_ENV') == 'production' or os.getenv('ENV') == 'prod':
        debug_mode = False
        logger.info("Production environment detected, debug mode disabled")
    
    app.run(host=host, port=port, debug=debug_mode)