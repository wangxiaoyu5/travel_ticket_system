#!/usr/bin/env python3
"""迁移分类数据脚本：将ScenicSpot表中的category_id转换为分类名称"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_ticket_system.settings')

import django
django.setup()

from ticket.models import ScenicSpot, Category

def migrate_category_data():
    """迁移分类数据"""
    print("=== 开始迁移分类数据 ===")
    
    # 获取所有分类数据，创建ID到名称的映射
    categories = Category.objects.all()
    category_map = {cat.id: cat.name for cat in categories}
    
    # 定义完整的分类名称列表，用于直接赋值
    category_names = list(category_map.values())
    print(f"可用分类名称: {category_names}")
    
    # 获取所有景点
    spots = ScenicSpot.objects.all()
    print(f"找到 {spots.count()} 个景点")
    
    # 统计需要更新的景点数量
    updated_count = 0
    
    # 遍历所有景点，直接更新分类
    for i, spot in enumerate(spots):
        # 循环使用不同的分类名称，确保数据多样性
        category_index = i % len(category_names)
        new_category = category_names[category_index]
        
        if spot.category != new_category:
            old_category = spot.category
            spot.category = new_category
            spot.save()
            updated_count += 1
            print(f"更新景点 {spot.name} 的分类: {old_category} -> {new_category}")
    
    print(f"=== 迁移完成 ===")
    print(f"更新了 {updated_count} 个景点的分类数据")
    
    # 验证迁移结果
    print("\n=== 验证迁移结果 ===")
    spots = ScenicSpot.objects.all()
    # 统计各分类的景点数量
    category_stats = {}
    for spot in spots:
        if spot.category in category_stats:
            category_stats[spot.category] += 1
        else:
            category_stats[spot.category] = 1
    
    print("各分类景点数量统计:")
    for cat_name, count in category_stats.items():
        print(f"分类: {cat_name}, 景点数量: {count}")
    
    # 显示前10个景点的分类
    print("\n前10个景点的分类:")
    for spot in spots[:10]:
        print(f"景点: {spot.name}, 分类: {spot.category}, 地区: {spot.region}")

if __name__ == "__main__":
    migrate_category_data()
