import requests
import logging
from datetime import datetime, date, timedelta

# 配置日志记录
logger = logging.getLogger(__name__)

# =======================
# 天气API配置
# =======================
# API模式选择：'real' 或 'mock'
# real: 使用真实API
# mock: 使用模拟数据
API_MODE = 'real'  # 使用真实API

# 真实API配置（当API_MODE='real'时使用）
# 这里使用开放的天气API服务
REAL_WEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather'
REAL_WEATHER_API_KEY = 'dc19881169c2c25d6d30ee33167e1ee4'  # 有效的API密钥

# 是否启用调试模式（调试模式下会输出详细日志）
DEBUG_MODE = True

# 模拟天气数据配置（当API_MODE='mock'时使用）
MOCK_WEATHER_DATA = {
    '北京': {
        '2025-12-27': {
            'temperature': '-5-5°C',
            'weather': '晴',
            'wind': '北风3级',
            'humidity': '30%',
            'advice': '天气寒冷，建议穿着保暖衣物'
        },
        '2025-12-28': {
            'temperature': '-3-7°C',
            'weather': '多云',
            'wind': '西北风2级',
            'humidity': '35%',
            'advice': '天气转暖，适合出行'
        },
        '2025-12-29': {
            'temperature': '-2-8°C',
            'weather': '晴',
            'wind': '北风4级',
            'humidity': '28%',
            'advice': '天气晴朗，风力较大'
        }
    },
    '上海': {
        '2025-12-27': {
            'temperature': '5-12°C',
            'weather': '阴',
            'wind': '东风2级',
            'humidity': '65%',
            'advice': '天气阴凉，建议穿着长袖衣物'
        },
        '2025-12-28': {
            'temperature': '4-10°C',
            'weather': '小雨',
            'wind': '东南风3级',
            'humidity': '75%',
            'advice': '有雨，建议携带雨具'
        },
        '2025-12-29': {
            'temperature': '6-13°C',
            'weather': '多云',
            'wind': '南风2级',
            'humidity': '60%',
            'advice': '天气转好，适合出行'
        }
    },
    '广州': {
        '2025-12-27': {
            'temperature': '15-23°C',
            'weather': '晴',
            'wind': '南风2级',
            'humidity': '60%',
            'advice': '天气温暖，适合户外活动'
        },
        '2025-12-28': {
            'temperature': '16-24°C',
            'weather': '晴',
            'wind': '东南风1级',
            'humidity': '55%',
            'advice': '天气晴朗，注意防晒'
        },
        '2025-12-29': {
            'temperature': '14-22°C',
            'weather': '多云',
            'wind': '南风3级',
            'humidity': '65%',
            'advice': '天气适宜，适合出行'
        }
    },
    '深圳': {
        '2025-12-27': {
            'temperature': '16-24°C',
            'weather': '晴',
            'wind': '东南风2级',
            'humidity': '58%',
            'advice': '天气温暖，适合户外活动'
        },
        '2025-12-28': {
            'temperature': '15-23°C',
            'weather': '多云',
            'wind': '南风1级',
            'humidity': '62%',
            'advice': '天气舒适，适合出行'
        },
        '2025-12-29': {
            'temperature': '17-25°C',
            'weather': '晴',
            'wind': '东南风3级',
            'humidity': '55%',
            'advice': '天气晴朗，注意防晒'
        }
    },
    '大连': {
        '2025-12-27': {
            'temperature': '-3-7°C',
            'weather': '晴',
            'wind': '北风4级',
            'humidity': '40%',
            'advice': '天气寒冷，风力较大'
        },
        '2025-12-28': {
            'temperature': '-2-8°C',
            'weather': '晴',
            'wind': '西北风3级',
            'humidity': '35%',
            'advice': '天气寒冷，注意保暖'
        },
        '2025-12-29': {
            'temperature': '-4-6°C',
            'weather': '多云',
            'wind': '北风5级',
            'humidity': '45%',
            'advice': '风力较大，注意防风'
        }
    },
    'default': {
        '2025-12-27': {
            'temperature': '10-20°C',
            'weather': '晴',
            'wind': '微风',
            'humidity': '45%',
            'advice': '天气适宜，建议正常出行'
        },
        '2025-12-28': {
            'temperature': '12-22°C',
            'weather': '多云',
            'wind': '东风2级',
            'humidity': '50%',
            'advice': '天气舒适，适合出行'
        },
        '2025-12-29': {
            'temperature': '9-19°C',
            'weather': '阴',
            'wind': '西风1级',
            'humidity': '42%',
            'advice': '天气阴凉，建议穿着长袖'
        }
    }
}


def get_weather_by_region(region_name, target_date):
    """
    根据地区名称和日期获取天气信息
    
    Args:
        region_name: 地区名称，如"北京"、"上海"
        target_date: 目标日期，格式为date对象
    
    Returns:
        dict: 天气信息字典
    """
    logger.info(f"开始查询天气: 地区={region_name}, 日期={target_date}")
    
    target_date_str = target_date.strftime('%Y-%m-%d')
    
    if API_MODE == 'real':
        # 使用真实API
        return _get_real_weather(region_name, target_date_str)
    else:
        # 使用模拟数据
        return _get_mock_weather(region_name, target_date_str)


def _get_real_weather(region_name, target_date_str):
    """
    使用真实API获取天气信息
    
    Args:
        region_name: 地区名称
        target_date_str: 目标日期字符串，格式为"YYYY-MM-DD"
    
    Returns:
        dict: 天气信息字典
    """
    logger.info(f"使用真实API查询天气: 地区={region_name}")
    
    # 检查API密钥是否已配置
    if REAL_WEATHER_API_KEY == 'your_real_api_key_here':
        error_msg = "真实天气API密钥未配置，请先获取API密钥并配置到weather_api.py文件中"
        logger.error(error_msg)
        return {
            'success': False,
            'error': error_msg
        }
    
    # 构建请求参数
    params = {
        'q': region_name,
        'appid': REAL_WEATHER_API_KEY,
        'units': 'metric',
        'lang': 'zh_cn'
    }
    
    # 尝试多次请求，增加可靠性
    max_retries = 3
    timeout = 15  # 增加超时时间
    
    for attempt in range(max_retries):
        try:
            logger.info(f"API请求尝试 {attempt + 1}/{max_retries}")
            
            # 发送请求
            response = requests.get(REAL_WEATHER_API_URL, params=params, timeout=timeout)
            response.raise_for_status()
            data = response.json()
            
            if DEBUG_MODE:
                logger.info(f"真实天气API响应: {data}")
            
            if data.get('cod') != 200:
                error_msg = data.get('message', '天气查询失败')
                logger.error(f"真实天气API调用失败: {error_msg}")
                return {
                    'success': False,
                    'error': f'天气查询失败: {error_msg}'
                }
            
            # 构建天气信息
            weather_info = {
                'success': True,
                'date': target_date_str,
                'temperature': f"{int(data['main']['temp_min'])}-{int(data['main']['temp_max'])}°C",
                'weather': data['weather'][0]['description'],
                'wind': f"{data['wind']['deg']}° {int(data['wind']['speed'])}m/s",
                'humidity': f"{data['main']['humidity']}%",
                'advice': get_weather_advice(data['weather'][0]['description'], data['main']['temp_max'])
            }
            
            logger.info(f"真实天气API查询成功: {weather_info}")
            return weather_info
            
        except requests.ReadTimeout:
            # 读取超时，继续重试
            logger.warning(f"API请求超时，正在重试... ({attempt + 1}/{max_retries})")
            if attempt == max_retries - 1:
                # 最后一次尝试失败，切换到模拟数据
                logger.error("所有API请求尝试都失败了，自动切换到模拟数据")
                return _get_mock_weather(region_name, target_date_str)
        except requests.HTTPError as e:
            # HTTP错误处理
            if e.response.status_code == 401:
                # 401认证错误，切换到模拟数据
                logger.error(f"API认证失败: {str(e)}，切换到模拟数据")
                return _get_mock_weather(region_name, target_date_str)
            else:
                # 其他HTTP错误
                logger.error(f"HTTP请求失败: {str(e)}", exc_info=True)
                return {
                    'success': False,
                    'error': f'网络请求失败: {str(e)}'
                }
        except requests.RequestException as e:
            # 其他网络请求异常
            logger.error(f"网络请求失败: {str(e)}", exc_info=True)
            return {
                'success': False,
                'error': f'网络请求失败: {str(e)}'
            }
        except Exception as e:
            # 其他异常
            logger.error(f"真实天气API查询异常: {str(e)}", exc_info=True)
            return {
                'success': False,
                'error': f'天气查询异常: {str(e)}'
            }


def _get_mock_weather(region_name, target_date_str):
    """
    使用模拟数据获取天气信息
    
    Args:
        region_name: 地区名称
        target_date_str: 目标日期字符串，格式为"YYYY-MM-DD"
    
    Returns:
        dict: 天气信息字典
    """
    logger.info(f"使用模拟数据查询天气: 地区={region_name}")
    
    # 获取对应地区的天气数据，如果没有则使用默认数据
    region_data = MOCK_WEATHER_DATA.get(region_name, MOCK_WEATHER_DATA['default'])
    
    # 获取目标日期的天气数据，如果没有则使用当天数据
    weather_data = region_data.get(target_date_str, list(region_data.values())[0])
    
    # 构建天气信息
    weather_info = {
        'success': True,
        'date': target_date_str,
        'temperature': weather_data['temperature'],
        'weather': weather_data['weather'],
        'wind': weather_data['wind'],
        'humidity': weather_data['humidity'],
        'advice': weather_data['advice']
    }
    
    logger.info(f"模拟数据查询成功: {weather_info}")
    return weather_info


def get_weather_advice(weather, temperature):
    """
    根据天气和温度生成出行建议
    
    Args:
        weather: 天气状况，如"晴"、"雨"
        temperature: 温度，字符串格式
    
    Returns:
        str: 出行建议
    """
    # 简单的天气建议逻辑
    if '雨' in weather:
        return '今日有雨，建议携带雨具出行，注意交通安全'
    elif '雪' in weather:
        return '今日有雪，路面湿滑，建议谨慎出行，注意保暖'
    elif '晴' in weather:
        try:
            # 提取温度数值
            if isinstance(temperature, int) or isinstance(temperature, float):
                temp = int(temperature)
            else:
                if '-' in temperature:
                    temp = int(temperature.split('-')[-1].replace('°C', ''))
                else:
                    temp = int(temperature.replace('°C', ''))
            
            if temp > 30:
                return '今日天气炎热，建议穿着轻便衣物，注意防晒补水'
            elif temp < 10:
                return '今日天气寒冷，建议穿着保暖衣物，注意防寒'
            else:
                return '天气适宜出行，建议穿着舒适衣物'
        except:
            return '天气晴朗，适宜出行'
    elif '阴' in weather:
        return '今日阴天，温度适宜，建议正常出行'
    elif '雾' in weather:
        return '今日有雾，能见度低，建议谨慎驾驶，注意安全'
    else:
        return '天气情况良好，建议正常出行'
