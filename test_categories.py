#!/usr/bin/env python3
"""测试分类和景点数据的脚本"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_ticket_system.settings')

import django
django.setup()

from ticket.models import ScenicSpot, Category, Region

print("=== 分类数据测试 ===")
categories = Category.objects.all()
print(f"分类总数: {categories.count()}")
for category in categories:
    print(f"分类ID: {category.id}, 名称: {category.name}")
    # 检查该分类下的景点数量
    spot_count = ScenicSpot.objects.filter(category=category).count()
    print(f"  - 关联景点数量: {spot_count}")

print("\n=== 景点数据测试 ===")
spots = ScenicSpot.objects.all()
print(f"景点总数: {spots.count()}")

# 检查有分类的景点
spots_with_category = ScenicSpot.objects.exclude(category__isnull=True)
print(f"有分类的景点数量: {spots_with_category.count()}")
for spot in spots_with_category[:5]:  # 只显示前5个
    print(f"景点: {spot.name}, 分类: {spot.category.name if spot.category else '无'}")

# 检查无分类的景点
spots_without_category = ScenicSpot.objects.filter(category__isnull=True)
print(f"无分类的景点数量: {spots_without_category.count()}")
for spot in spots_without_category[:5]:  # 只显示前5个
    print(f"景点: {spot.name}, 分类: 无")

print("\n=== 地区数据测试 ===")
regions = Region.objects.all()
print(f"地区总数: {regions.count()}")
for region in regions[:5]:  # 只显示前5个
    print(f"地区: {region.name}")
    # 检查该地区下的景点数量
    spot_count = ScenicSpot.objects.filter(region=region.name).count()
    print(f"  - 关联景点数量: {spot_count}")
