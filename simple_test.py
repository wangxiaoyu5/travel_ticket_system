#!/usr/bin/env python3
"""简单测试脚本"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_ticket_system.settings')

import django
django.setup()

from ticket.models import ScenicSpot, Category

print("=== 简单分类测试 ===")

# 获取第一个景点
first_spot = ScenicSpot.objects.first()
if first_spot:
    print(f"第一个景点: {first_spot.name}")
    print(f"分类ID: {first_spot.category}")
    print(f"分类类型: {type(first_spot.category)}")
    
    # 尝试直接用分类ID筛选
    if first_spot.category:
        category_id = first_spot.category
        spots_by_category = ScenicSpot.objects.filter(category=category_id)
        print(f"用分类ID {category_id} 筛选到的景点数量: {spots_by_category.count()}")
        
        # 尝试用category__id筛选
        spots_by_category_id = ScenicSpot.objects.filter(category__id=category_id)
        print(f"用category__id {category_id} 筛选到的景点数量: {spots_by_category_id.count()}")

print("\n=== 分类列表 ===")
categories = Category.objects.all()
for category in categories:
    print(f"分类: {category.name}, ID: {category.id}")
