import os
import yaml
import shutil
from pathlib import Path

def load_config():
    """
    加载配置文件
    优先级: 环境变量 > config/config.yaml > config/config.default.yaml
    """
    # 确保配置目录存在
    config_dir = Path('config')
    config_dir.mkdir(exist_ok=True)
    
    # 配置文件路径
    default_config_path = config_dir / 'config.default.yaml'
    config_path = config_dir / 'config.yaml'
    
    # 如果默认配置文件不存在，创建它
    if not default_config_path.exists():
        create_default_config(default_config_path)
    
    # 如果用户配置文件不存在，从默认配置文件复制
    if not config_path.exists():
        shutil.copy(default_config_path, config_path)
    
    # 加载默认配置
    with open(default_config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f) or {}
    
    # 如果用户配置文件存在，合并配置
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            user_config = yaml.safe_load(f) or {}
        config = merge_config(config, user_config)
    
    # 从环境变量加载配置
    config = load_config_from_env(config)
    
    return config

def create_default_config(config_path):
    """创建默认配置文件"""
    default_config = {
        'debug': False,
        'server': {
            'host': '127.0.0.1',
            'port': 5001
        },
        'weather_api': {
            'key': 'YOUR_HEFENG_WEATHER_API_KEY',
            'url': 'https://devapi.qweather.com/v7/weather/now'
        },
        'log': {
            'level': 'INFO',
            'file': 'logs/app.log',
            'max_bytes': 10485760,  # 10MB
            'backup_count': 5
        }
    }
    
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(default_config, f, default_flow_style=False, allow_unicode=True)

def merge_config(default, user):
    """合并默认配置和用户配置"""
    for key, value in user.items():
        if key in default and isinstance(default[key], dict) and isinstance(value, dict):
            default[key] = merge_config(default[key], value)
        else:
            default[key] = value
    return default

def load_config_from_env(config):
    """从环境变量加载配置"""
    # 服务器配置
    if 'HOST' in os.environ:
        config.setdefault('server', {})['host'] = os.environ['HOST']
    if 'PORT' in os.environ:
        config.setdefault('server', {})['port'] = int(os.environ.get('PORT', 5001))
    
    # 调试模式
    if 'DEBUG' in os.environ:
        config['debug'] = os.environ['DEBUG'].lower() in ('true', '1', 'yes')
    
    # 天气API配置
    if 'WEATHER_API_KEY' in os.environ:
        config.setdefault('weather_api', {})['key'] = os.environ['WEATHER_API_KEY']
    if 'WEATHER_API_URL' in os.environ:
        config.setdefault('weather_api', {})['url'] = os.environ['WEATHER_API_URL']
    
    # 日志配置
    if 'LOG_LEVEL' in os.environ:
        config.setdefault('log', {})['level'] = os.environ['LOG_LEVEL']
    if 'LOG_FILE' in os.environ:
        config.setdefault('log', {})['file'] = os.environ['LOG_FILE']
    
    return config