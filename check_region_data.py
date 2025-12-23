#!/usr/bin/env python3
"""检查并更新地区数据脚本"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_ticket_system.settings')

import django
django.setup()

from ticket.models import ScenicSpot, Region

def check_and_update_region_data():
    """检查并更新地区数据"""
    print("=== 开始检查地区数据 ===")
    
    # 获取所有地区
    regions = Region.objects.all()
    region_names = [region.name for region in regions]
    print(f"找到 {len(region_names)} 个地区: {region_names}")
    
    # 添加一些常用地区，如果不存在的话
    common_regions = ['北京', '上海', '广州', '深圳', '成都', '杭州', '西安', '重庆', '武汉', '南京']
    for region_name in common_regions:
        if region_name not in region_names:
            region = Region(name=region_name)
            region.save()
            print(f"添加新地区: {region_name}")
    
    # 重新获取地区列表
    updated_regions = Region.objects.all()
    updated_region_names = [region.name for region in updated_regions]
    print(f"更新后的地区列表: {updated_region_names}")
    
    # 检查景点的地区数据
    spots = ScenicSpot.objects.all()
    print(f"找到 {spots.count()} 个景点")
    
    # 统计地区分布
    region_stats = {}
    for spot in spots:
        region = spot.region
        if region in region_stats:
            region_stats[region] += 1
        else:
            region_stats[region] = 1
    
    print("\n景点地区分布统计:")
    for region, count in region_stats.items():
        print(f"地区: {region}, 景点数量: {count}")
    
    # 显示前10个景点的地区信息
    print("\n前10个景点的地区信息:")
    for spot in spots[:10]:
        print(f"景点: {spot.name}, 地区: {spot.region}, 分类: {spot.category}")

if __name__ == "__main__":
    check_and_update_region_data()
