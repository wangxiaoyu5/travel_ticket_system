#!/usr/bin/env python
"""
直接操作数据库，修复News模型的scenic_spot_id字段
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

print("=== 修复News模型的scenic_spot_id字段 ===")

try:
    with connection.cursor() as cursor:
        print("\n1. 检查ticket_news表是否存在scenic_spot_id字段：")
        cursor.execute("SHOW COLUMNS FROM ticket_news LIKE 'scenic_spot_id';")
        rows = cursor.fetchall()
        
        if rows:
            print("   ✓ 发现scenic_spot_id字段，准备删除")
            
            # 尝试删除scenic_spot_id字段
            print("\n2. 删除scenic_spot_id字段：")
            try:
                cursor.execute("ALTER TABLE ticket_news DROP COLUMN scenic_spot_id;")
                print("   ✓ 成功删除scenic_spot_id字段")
            except Exception as e:
                print(f"   ✗ 删除字段失败: {e}")
        else:
            print("   ✗ 未发现scenic_spot_id字段")
        
        # 再次检查字段是否存在
        print("\n3. 再次检查scenic_spot_id字段：")
        cursor.execute("SHOW COLUMNS FROM ticket_news LIKE 'scenic_spot_id';")
        rows = cursor.fetchall()
        if rows:
            print("   ✗ scenic_spot_id字段仍然存在")
        else:
            print("   ✓ scenic_spot_id字段已成功删除")
        
    print("\n=== 修复完成 ===")
    
except Exception as e:
    print(f"\n✗ 修复过程中出现错误: {e}")
    import traceback
    traceback.print_exc()
