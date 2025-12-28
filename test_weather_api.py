#!/usr/bin/env python3
# 天气API测试脚本

import sys
import os
from datetime import date

# 添加项目路径到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 配置日志
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 导入天气API模块
from ticket.weather_api import get_weather_by_region

if __name__ == '__main__':
    print("测试天气API功能")
    print("=" * 50)
    
    # 测试参数
    region_name = "北京"
    test_date = date.today()
    
    print(f"测试地区: {region_name}")
    print(f"测试日期: {test_date}")
    print("=" * 50)
    
    # 调用天气API
    result = get_weather_by_region(region_name, test_date)
    
    print("测试结果:")
    print(result)
    print("=" * 50)
    
    if result['success']:
        print("✅ 天气查询成功")
    else:
        print(f"❌ 天气查询失败: {result['error']}")
