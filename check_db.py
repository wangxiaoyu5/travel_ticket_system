#!/usr/bin/env python
"""
查看数据库表结构
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

print("=== 检查数据库表结构 ===")

try:
    # 查看ticket_scenicspot表的region字段
    with connection.cursor() as cursor:
        print("\n1. ticket_scenicspot表的region字段：")
        cursor.execute('SHOW COLUMNS FROM ticket_scenicspot WHERE Field = "region";')
        rows = cursor.fetchall()
        for row in rows:
            print(f"字段名: {row[0]}, 类型: {row[1]}, 是否为空: {row[2]}, 默认值: {row[4]}")
        
    # 查看ticket_scenicspot表的category字段（用于对比）
    with connection.cursor() as cursor:
        print("\n2. ticket_scenicspot表的category字段：")
        cursor.execute('SHOW COLUMNS FROM ticket_scenicspot WHERE Field = "category";')
        rows = cursor.fetchall()
        for row in rows:
            print(f"字段名: {row[0]}, 类型: {row[1]}, 是否为空: {row[2]}, 默认值: {row[4]}")
        
    # 查看ticket_region表的基本信息
    with connection.cursor() as cursor:
        print("\n3. ticket_region表是否存在：")
        cursor.execute('SHOW TABLES LIKE "ticket_region";')
        rows = cursor.fetchall()
        print(f"表存在: {len(rows) > 0}")
        
        if len(rows) > 0:
            print("\n4. ticket_region表结构：")
            cursor.execute('DESCRIBE ticket_region;')
            rows = cursor.fetchall()
            for row in rows:
                print(f"字段名: {row[0]}, 类型: {row[1]}, 是否为空: {row[2]}, 默认值: {row[4]}")
            
            print("\n5. ticket_region表中的数据：")
            cursor.execute('SELECT id, name FROM ticket_region;')
            rows = cursor.fetchall()
            if len(rows) > 0:
                for row in rows:
                    print(f"ID: {row[0]}, 名称: {row[1]}")
            else:
                print("表中没有数据")
            
except Exception as e:
    print(f"\n错误: {e}")
    import traceback
    traceback.print_exc()

print("\n=== 检查完成 ===")
