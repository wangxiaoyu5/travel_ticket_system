#!/usr/bin/env python3
"""修复数据脚本：确保景点有正确的地区和分类数据"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_ticket_system.settings')

import django
django.setup()

from ticket.models import ScenicSpot, Category, Region

def fix_scenic_spot_data():
    """修复景点数据"""
    print("=== 开始修复景点数据 ===")
    
    # 1. 获取所有分类名称
    categories = Category.objects.all()
    category_names = [cat.name for cat in categories]
    print(f"分类列表: {category_names}")
    
    # 2. 获取所有地区名称
    regions = Region.objects.all()
    region_names = [reg.name for reg in regions]
    print(f"地区列表: {region_names}")
    
    # 3. 如果没有地区，添加一些常用地区
    if not region_names:
        common_regions = ['北京', '上海', '广州', '深圳', '成都', '杭州', '西安', '重庆', '武汉', '南京']
        for region_name in common_regions:
            Region.objects.create(name=region_name)
        # 重新获取地区列表
        regions = Region.objects.all()
        region_names = [reg.name for reg in regions]
        print(f"添加常用地区后: {region_names}")
    
    # 4. 获取所有景点
    spots = ScenicSpot.objects.all()
    print(f"找到 {spots.count()} 个景点")
    
    # 5. 修复每个景点的数据
    for i, spot in enumerate(spots):
        # 修复分类
        if not spot.category or spot.category not in category_names:
            # 分配一个随机分类
            category_index = i % len(category_names)
            spot.category = category_names[category_index]
            
        # 修复地区
        if not spot.region or spot.region == '全国' or spot.region not in region_names:
            # 分配一个随机地区
            region_index = i % len(region_names)
            spot.region = region_names[region_index]
        
        # 保存修改
        spot.save()
        
        # 打印进度
        if (i + 1) % 10 == 0:
            print(f"已修复 {i + 1} 个景点")
    
    print("=== 数据修复完成 ===")
    
    # 6. 验证修复结果
    print("\n=== 验证修复结果 ===")
    
    # 统计分类分布
    category_stats = {}
    region_stats = {}
    
    for spot in spots:
        # 统计分类
        if spot.category in category_stats:
            category_stats[spot.category] += 1
        else:
            category_stats[spot.category] = 1
        
        # 统计地区
        if spot.region in region_stats:
            region_stats[spot.region] += 1
        else:
            region_stats[spot.region] = 1
    
    print("分类分布:")
    for cat, count in category_stats.items():
        print(f"  {cat}: {count} 个景点")
    
    print("\n地区分布:")
    for reg, count in region_stats.items():
        print(f"  {reg}: {count} 个景点")
    
    print("\n前5个景点数据:")
    for spot in spots[:5]:
        print(f"  景点: {spot.name}, 分类: {spot.category}, 地区: {spot.region}")

if __name__ == "__main__":
    fix_scenic_spot_data()
