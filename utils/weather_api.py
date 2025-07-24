import requests
import urllib.parse

def get_weather_data(city, config):
    """
    获取指定城市的天气数据
    
    Args:
        city (str): 城市名称
        config (dict): 配置字典
        
    Returns:
        dict: 天气数据
    """
    # 从配置中获取API信息
    api_key = config.get('weather_api', {}).get('key')
    api_host = config.get('weather_api', {}).get('url')
    
    if not api_key or not api_host:
        raise ValueError("Weather API key or URL not configured")
    
    # 确保API主机不包含协议
    if api_host.startswith(('http://', 'https://')):
        # 移除协议部分
        api_host = api_host.split('://', 1)[1]
    
    try:
        # 使用配置的API主机进行地理位置查询，使用正确的路径
        geo_url = f"https://{api_host}/geo/v2/city/lookup?key={api_key}&location={urllib.parse.quote(city)}"
        print(f"Geolocation API URL: {geo_url}")  # 调试信息
        
        # 获取城市位置信息
        geo_response = requests.get(geo_url, timeout=10)
        print(f"Geolocation API Response Status: {geo_response.status_code}")  # 调试信息
        geo_response.raise_for_status()
        geo_data = geo_response.json()
        
        if not geo_data.get('location'):
            raise ValueError(f"City '{city}' not found")
        
        # 获取第一个匹配城市的ID
        city_id = geo_data['location'][0]['id']
        
        # 构建API请求URL，使用正确的路径
        weather_url = f"https://{api_host}/v7/weather/now?location={city_id}&key={api_key}"
        print(f"Weather API URL: {weather_url}")  # 调试信息
        
        # 获取天气数据
        weather_response = requests.get(weather_url, timeout=10)
        print(f"Weather API Response Status: {weather_response.status_code}")  # 调试信息
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        
        if weather_data.get('code') != '200':
            raise ValueError(f"Weather API error: {weather_data.get('code')}")
        
        # 提取需要的天气信息
        result = {
            'city': city,
            'temperature': weather_data['now']['temp'],
            'condition': weather_data['now']['text'],
            'wind_dir': weather_data['now']['windDir'],
            'wind_scale': weather_data['now']['windScale'],
            'humidity': weather_data['now']['humidity'],
            'icon': weather_data['now']['icon']
        }
        
        return result
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Network error when fetching weather data: {str(e)}")
    except ValueError as e:
        raise e
    except Exception as e:
        raise Exception(f"Error processing weather data: {str(e)}")