#!/usr/bin/env python
"""
直接使用SQL命令修复ticket_scenicspot.region字段
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

print("=== 修复ticket_scenicspot.region字段 ===")

try:
    with connection.cursor() as cursor:
        print("\n1. 检查ticket_scenicspot表是否存在region字段：")
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'ticket_scenicspot' AND column_name = 'region';")
        rows = cursor.fetchall()
        
        if rows:
            print("   ✓ region字段已存在")
        else:
            print("   ✗ region字段不存在，准备添加")
            
            # 直接添加region字段
            print("\n2. 添加region字段：")
            try:
                cursor.execute("ALTER TABLE ticket_scenicspot ADD COLUMN region VARCHAR(50) NOT NULL DEFAULT '全国';")
                print("   ✓ 成功添加region字段")
            except Exception as e:
                print(f"   ✗ 添加字段失败: {e}")
                print(f"   错误类型: {type(e).__name__}")
        
        # 再次检查字段是否存在
        print("\n3. 再次检查region字段：")
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'ticket_scenicspot' AND column_name = 'region';")
        rows = cursor.fetchall()
        if rows:
            print("   ✓ region字段已存在")
        else:
            print("   ✗ region字段仍然不存在")
        
        # 测试查询ScenicSpot表
        print("\n4. 测试查询ScenicSpot表：")
        try:
            cursor.execute("SELECT COUNT(*) FROM ticket_scenicspot;")
            count = cursor.fetchone()[0]
            print(f"   ✓ 查询成功，景点数量：{count}")
        except Exception as e:
            print(f"   ✗ 查询失败: {e}")
            print(f"   错误类型: {type(e).__name__}")
        
    print("\n=== 修复完成 ===")
    
except Exception as e:
    print(f"\n✗ 修复过程中出现错误: {e}")
    print(f"错误类型: {type(e).__name__}")
    import traceback
    traceback.print_exc()
