#!/usr/bin/env python
"""
检查数据库结构与模型定义的一致性
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

print("=== 数据库结构检查 ===")

try:
    with connection.cursor() as cursor:
        print("\n1. 检查ticket_scenicspot表结构：")
        cursor.execute("DESCRIBE ticket_scenicspot;")
        rows = cursor.fetchall()
        for row in rows:
            print(f"   {row}")
        
        print("\n2. 检查ticket_category表结构：")
        cursor.execute("DESCRIBE ticket_category;")
        rows = cursor.fetchall()
        for row in rows:
            print(f"   {row}")
        
        print("\n3. 检查ticket_region表结构：")
        cursor.execute("DESCRIBE ticket_region;")
        rows = cursor.fetchall()
        for row in rows:
            print(f"   {row}")
            
    print("\n=== 检查完成 ===")
    
except Exception as e:
    print(f"\n✗ 检查过程中出现错误: {e}")
    import traceback
    traceback.print_exc()
    print("\n=== 检查失败 ===")
