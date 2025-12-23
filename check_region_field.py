#!/usr/bin/env python
"""
检查ScenicSpot模型的region字段是否存在
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_ticket_system.settings')

import django
django.setup()

from django.db import connection

print("=== 检查ScenicSpot模型的region字段 ===")

try:
    with connection.cursor() as cursor:
        print("\n1. 检查ticket_scenicspot表结构：")
        cursor.execute("DESCRIBE ticket_scenicspot;")
        rows = cursor.fetchall()
        print("   字段名 | 类型 | 是否为空 | 主键 | 默认值 | 额外信息")
        print("   " + "-" * 60)
        
        region_exists = False
        for row in rows:
            field_name = row[0]
            field_type = row[1]
            is_null = row[2]
            key = row[3]
            default = row[4]
            extra = row[5]
            print(f"   {field_name:<15} | {field_type:<25} | {is_null:<8} | {key:<6} | {default:<10} | {extra}")
            
            if field_name == 'region':
                region_exists = True
        
        print(f"\n2. region字段存在: {region_exists}")
        
        if not region_exists:
            print("\n3. 添加region字段：")
            try:
                cursor.execute("ALTER TABLE ticket_scenicspot ADD COLUMN region VARCHAR(50) DEFAULT '全国';")
                print("   ✓ 成功添加region字段")
            except Exception as e:
                print(f"   ✗ 添加字段失败: {e}")
        
        # 再次检查字段是否存在
        print("\n4. 再次检查region字段：")
        cursor.execute("DESCRIBE ticket_scenicspot;")
        rows = cursor.fetchall()
        region_exists = any(row[0] == 'region' for row in rows)
        print(f"   region字段存在: {region_exists}")
        
    print("\n=== 检查完成 ===")
    
except Exception as e:
    print(f"\n✗ 检查过程中出现错误: {e}")
    import traceback
    traceback.print_exc()
