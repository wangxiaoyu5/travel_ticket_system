#!/usr/bin/env python3
"""更新景点地区数据脚本"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_ticket_system.settings')

import django
django.setup()

from ticket.models import ScenicSpot, Region

def update_region_data():
    """更新景点地区数据"""
    print("=== 开始更新景点地区数据 ===")
    
    # 获取所有地区
    regions = Region.objects.all()
    region_names = [region.name for region in regions]
    print(f"可用地区列表: {region_names}")
    
    # 获取所有景点
    spots = ScenicSpot.objects.all()
    print(f"找到 {spots.count()} 个景点")
    
    # 统计需要更新的景点数量
    updated_count = 0
    
    # 遍历所有景点，为每个景点分配一个具体的地区
    for i, spot in enumerate(spots):
        # 循环使用不同的地区名称
        region_index = i % len(region_names)
        new_region = region_names[region_index]
        
        if spot.region != new_region:
            old_region = spot.region
            spot.region = new_region
            spot.save()
            updated_count += 1
            print(f"更新景点 {spot.name} 的地区: {old_region} -> {new_region}")
    
    print(f"=== 更新完成 ===")
    print(f"更新了 {updated_count} 个景点的地区数据")
    
    # 验证更新结果
    print("\n=== 验证更新结果 ===")
    spots = ScenicSpot.objects.all()
    
    # 统计地区分布
    region_stats = {}
    for spot in spots:
        region = spot.region
        if region in region_stats:
            region_stats[region] += 1
        else:
            region_stats[region] = 1
    
    print("景点地区分布统计:")
    for region, count in region_stats.items():
        print(f"地区: {region}, 景点数量: {count}")
    
    # 显示前10个景点的完整信息
    print("\n前10个景点的完整信息:")
    for spot in spots[:10]:
        print(f"景点: {spot.name}, 地区: {spot.region}, 分类: {spot.category}")

if __name__ == "__main__":
    update_region_data()
