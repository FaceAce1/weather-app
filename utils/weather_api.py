import requests
import urllib.parse

def get_weather_data(city, config):
    """
    获取指定城市的天气数据，包含完整信息
    
    Args:
        city (str): 城市名称
        config (dict): 配置字典
        
    Returns:
        dict: 完整天气数据
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
            raise ValueError(f"城市 '{city}' 未找到")
        
        # 获取第一个匹配城市的ID和名称
        city_info = geo_data['location'][0]
        city_id = city_info['id']
        city_name = city_info['name']
        
        # 获取天气数据
        weather_url = f"https://{api_host}/v7/weather/now?location={city_id}&key={api_key}"
        weather_response = requests.get(weather_url, timeout=10)
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        
        if weather_data.get('code') != '200':
            raise ValueError(f"天气API错误: {weather_data.get('code')}")
        
        # 提取完整天气信息
        return {
            'city': city_name,
            'code': weather_data['code'],
            'updateTime': weather_data['updateTime'],
            'fxLink': weather_data.get('fxLink', ''),
            'now': weather_data['now'],
            'refer': weather_data.get('refer', {})
        }
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"获取天气数据时网络错误: {str(e)}")
    except ValueError as e:
        raise e
    except Exception as e:
        raise Exception(f"处理天气数据时出错: {str(e)}")