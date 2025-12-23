#!/usr/bin/env python
"""
初始化默认的分类和地区数据
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_ticket_system.settings')

import django
django.setup()

from ticket.models import Category, Region

print("=== 初始化默认数据 ===")

try:
    # 检查并添加默认景点分类
    print("\n1. 初始化景点分类：")
    default_categories = [
        "自然风光类",
        "历史遗迹类", 
        "民俗文化类",
        "现代都市类",
        "休闲度假类",
        "主题乐园类",
        "宗教文化类",
        "农业乡村类"
    ]
    
    for cat_name in default_categories:
        category, created = Category.objects.get_or_create(name=cat_name)
        if created:
            print(f"  ✓ 添加分类: {cat_name}")
        else:
            print(f"  ✓ 分类已存在: {cat_name}")
    
    # 检查并添加默认地区
    print("\n2. 初始化地区：")
    default_regions = [
        "北京",
        "上海",
        "广州",
        "深圳",
        "杭州",
        "成都",
        "西安",
        "重庆",
        "武汉",
        "南京",
        "天津",
        "苏州",
        "青岛",
        "厦门",
        "三亚",
        "张家界",
        "桂林",
        "黄山",
        "故宫",
        "长城"
    ]
    
    for region_name in default_regions:
        region, created = Region.objects.get_or_create(name=region_name)
        if created:
            print(f"  ✓ 添加地区: {region_name}")
        else:
            print(f"  ✓ 地区已存在: {region_name}")
    
    # 显示当前所有数据
    print("\n3. 当前数据统计：")
    print(f"  - 景点分类数量: {Category.objects.count()}")
    print(f"  - 地区数量: {Region.objects.count()}")
    
    print("\n=== 初始化完成 ===")
    
except Exception as e:
    print(f"\n错误: {e}")
    import traceback
    traceback.print_exc()
