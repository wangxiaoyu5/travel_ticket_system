#!/usr/bin/env python
"""
直接使用SQL命令修复数据库问题
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

print("=== 直接使用SQL命令修复数据库 ===")

try:
    with connection.cursor() as cursor:
        print("\n1. 连接到数据库：")
        cursor.execute("SELECT DATABASE();")
        db_name = cursor.fetchone()[0]
        print(f"   ✓ 成功连接到数据库：{db_name}")
        
        print("\n2. 检查ticket_news表结构：")
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'ticket_news' AND column_name = 'scenic_spot_id';")
        rows = cursor.fetchall()
        
        if rows:
            print("   ✓ 发现scenic_spot_id字段")
            
            # 直接删除字段
            print("\n3. 尝试删除scenic_spot_id字段：")
            try:
                cursor.execute("ALTER TABLE ticket_news DROP COLUMN scenic_spot_id;")
                print("   ✓ 成功删除scenic_spot_id字段")
            except Exception as e:
                print(f"   ✗ 删除字段失败: {e}")
                print(f"   错误类型: {type(e).__name__}")
        else:
            print("   ✗ 未发现scenic_spot_id字段")
        
        # 再次检查
        print("\n4. 再次检查scenic_spot_id字段：")
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'ticket_news' AND column_name = 'scenic_spot_id';")
        rows = cursor.fetchall()
        if rows:
            print("   ✗ scenic_spot_id字段仍然存在")
        else:
            print("   ✓ scenic_spot_id字段已不存在")
        
        # 测试查询News表
        print("\n5. 测试查询News表：")
        try:
            cursor.execute("SELECT COUNT(*) FROM ticket_news;")
            count = cursor.fetchone()[0]
            print(f"   ✓ 查询成功，News表行数：{count}")
        except Exception as e:
            print(f"   ✗ 查询失败: {e}")
            print(f"   错误类型: {type(e).__name__}")
        
    print("\n=== 修复完成 ===")
    
except Exception as e:
    print(f"\n✗ 修复过程中出现错误: {e}")
    print(f"错误类型: {type(e).__name__}")
    import traceback
    traceback.print_exc()
