import requests
import urllib.parse
from datetime import datetime

def get_weather_data(city, config):
    """
    获取指定城市的完整天气数据
    
    Args:
        city (str): 城市名称
        config (dict): 配置字典
        
    Returns:
        dict: 完整的天气数据
    """
    # 从配置中获取API信息
    api_key = config.get('weather_api', {}).get('key')
    api_host = config.get('weather_api', {}).get('url')
    
    if not api_key or not api_host:
        raise ValueError("Weather API key or URL not configured")
    
    # 确保API主机不包含协议
    if api_host.startswith(('http://', 'https://')):
        api_host = api_host.split('://', 1)[1]
    
    try:
        # 获取城市位置信息
        geo_url = f"https://{api_host}/geo/v2/city/lookup?key={api_key}&location={urllib.parse.quote(city)}"
        
        geo_response = requests.get(geo_url, timeout=10)
        geo_response.raise_for_status()
        geo_data = geo_response.json()
        
        if not geo_data.get('location'):
            raise ValueError(f"City '{city}' not found")
        
        # 获取第一个匹配城市的ID和名称
        city_info = geo_data['location'][0]
        city_id = city_info['id']
        city_name = city_info['name']
        
        # 获取详细天气数据
        weather_url = f"https://{api_host}/v7/weather/now?location={city_id}&key={api_key}"
        
        weather_response = requests.get(weather_url, timeout=10)
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        
        if weather_data.get('code') != '200':
            raise ValueError(f"Weather API error: {weather_data.get('code')}")
        
        # 提取所有需要的天气信息
        now = weather_data['now']
        result = {
            'code': weather_data['code'],
            'updateTime': format_datetime(weather_data['updateTime']),
            'fxLink': weather_data.get('fxLink', ''),
            'city': city_name,
            'now': {
                'obsTime': format_datetime(now['obsTime']),
                'temp': now['temp'],
                'feelsLike': now['feelsLike'],
                'icon': now['icon'],
                'text': now['text'],
                'wind360': now['wind360'],
                'windDir': now['windDir'],
                'windScale': now['windScale'],
                'windSpeed': now['windSpeed'],
                'humidity': now['humidity'],
                'precip': now.get('precip', '0.0'),
                'pressure': now['pressure'],
                'vis': now['vis'],
                'cloud': now.get('cloud', '0'),
                'dew': now.get('dew', '')
            },
            'refer': weather_data.get('refer', {
                'sources': ['QWeather'],
                'license': ['QWeather Developers License']
            })
        }
        
        return result
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Network error when fetching weather data: {str(e)}")
    except ValueError as e:
        raise e
    except Exception as e:
        raise Exception(f"Error processing weather data: {str(e)}")

def format_datetime(dt_str):
    """格式化日期时间为页面需要的格式"""
    try:
        # 处理形如"2020-06-30T22:00+08:00"的格式
        dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M')
    except:
        return dt_str