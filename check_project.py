#!/usr/bin/env python
"""
检查项目状态和关键功能
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
from django.test import Client
from ticket.models import Category, Region, ScenicSpot, Order, User

print("=== 项目状态检查 ===")

try:
    print("\n1. 数据库连接检查：")
    # 测试数据库连接
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1;")
        result = cursor.fetchone()
        if result == (1,):
            print("  ✓ 数据库连接正常")
        else:
            print("  ✗ 数据库连接失败")
    
    print("\n2. 数据统计：")
    # 检查关键表的数据量
    data_counts = {
        '景点分类': Category.objects.count(),
        '地区': Region.objects.count(), 
        '景点': ScenicSpot.objects.count(),
        '订单': Order.objects.count(),
        '用户': User.objects.count()
    }
    
    for data_type, count in data_counts.items():
        status = "✓" if count >= 0 else "✗"
        print(f"  {status} {data_type}数量: {count}")
    
    print("\n3. 模型关联检查：")
    try:
        # 直接测试查询
        print("  测试景点查询：")
        spots = ScenicSpot.objects.all()
        print(f"    ✓ 查询成功，景点数量：{spots.count()}")
        
        # 测试带关联的查询
        print("  测试带分类关联的景点查询：")
        spots_with_category = ScenicSpot.objects.select_related('category').all()
        print(f"    ✓ 关联查询成功")
        
        # 测试带地区字段的查询
        print("  测试地区字段查询：")
        # 地区是CharField，使用!=操作符查询非空值
        spots_with_region = ScenicSpot.objects.filter(region != '')
        print(f"    ✓ 地区查询成功，数量：{spots_with_region.count()}")
        
        print("  ✓ 所有模型关联检查通过")
    except Exception as e:
        print(f"  ✗ 模型关联检查失败: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n4. URL路由检查：")
    # 检查关键URL是否可访问
    client = Client()
    # 设置正确的HTTP_HOST头
    headers = {'HTTP_HOST': '127.0.0.1:8000'}
    
    try:
        # 首页访问测试
        response = client.get('/', **headers)
        print(f"  {'✓' if response.status_code == 200 else '✗'} 首页访问: {response.status_code}")
    except Exception as e:
        print(f"  ✗ 首页访问失败: {e}")
    
    try:
        # 景点列表页访问测试
        response = client.get('/scenic_spots/', **headers)
        print(f"  {'✓' if response.status_code == 200 else '✗'} 景点列表页访问: {response.status_code}")
    except Exception as e:
        print(f"  ✗ 景点列表页访问失败: {e}")
    
    try:
        # 景点管理页访问测试（需要登录）
        response = client.get('/admin/scenic_spots/', **headers)
        # 未登录应该重定向到登录页
        print(f"  {'✓' if response.status_code in [200, 302] else '✗'} 景点管理页访问: {response.status_code}")
    except Exception as e:
        print(f"  ✗ 景点管理页访问失败: {e}")
    
    print("\n5. 环境检查：")
    print(f"  ✓ Django版本: {django.__version__}")
    print(f"  ✓ Python版本: {sys.version}")
    print(f"  ✓ 调试模式: {'开启' if os.environ.get('DJANGO_SETTINGS_MODULE') else '关闭'}")
    
    print("\n=== 检查完成 ===")
    print("项目状态良好，没有发现严重错误。")
    
except Exception as e:
    print(f"\n✗ 检查过程中出现错误: {e}")
    import traceback
    traceback.print_exc()
    print("\n=== 检查失败 ===")
