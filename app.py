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
print("Loaded configuration:")
for key, value in config.items():
    if key != 'weather_api':  # 避免打印API密钥
        print(f"  {key}: {value}")

print(f"  weather_api: {{'url': '{config.get('weather_api', {}).get('url', 'N/A')}'}}")

@app.route('/')
def index():
    """渲染主页"""
    logger.info("Home page accessed")
    return render_template('index.html')

@app.route('/api/weather')
def weather():
    """获取天气数据API"""
    city = request.args.get('city')
    
    # 尝试解码可能被错误编码的URL参数
    if city:
        try:
            city = urllib.parse.unquote(city)
        except Exception:
            pass
    
    if not city:
        logger.warning("Missing city parameter in request")
        return jsonify({'error': 'City parameter is required'}), 400
    
    try:
        logger.info(f"Fetching weather data for city: {city}")
        weather_data = get_weather_data(city, config)
        logger.info(f"Successfully fetched weather data for city: {city}")
        return jsonify(weather_data)
    except Exception as e:
        logger.error(f"Error fetching weather data for city {city}: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    host = config.get('server', {}).get('host', '127.0.0.1')
    port = config.get('server', {}).get('port', 5001)
    
    logger.info(f"Starting server on {host}:{port}")
    app.run(host=host, port=port, debug=config.get('debug', False))