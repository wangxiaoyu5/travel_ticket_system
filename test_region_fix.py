#!/usr/bin/env python
"""
测试地区管理页面修复
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_ticket_system.settings')

import django
django.setup()

from django.test import Client
from django.contrib.auth.models import User

print("Testing region management fix...")

# 创建测试客户端
client = Client()

# 创建测试管理员用户（如果不存在）
admin_user, created = User.objects.get_or_create(
    username='test_admin',
    defaults={'password': 'test_password', 'is_superuser': True, 'is_staff': True}
)
if created:
    admin_user.set_password('test_password')
    admin_user.save()

print("\n1. 测试未登录状态访问地区管理页面")
try:
    response = client.get('/admin/regions/', HTTP_HOST='127.0.0.1')
    print(f"Status code: {response.status_code}")
    print(f"重定向到登录页面: {response.status_code == 302}")
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()

print("\n2. 测试管理员登录")
login_response = client.login(username='test_admin', password='test_password')
print(f"登录成功: {login_response}")

print("\n3. 测试登录后访问地区管理页面")
try:
    response = client.get('/admin/regions/', HTTP_HOST='127.0.0.1')
    print(f"Status code: {response.status_code}")
    print(f"访问成功: {response.status_code == 200}")
    if response.status_code == 200:
        print("地区管理页面访问成功！NoReverseMatch错误已修复。")
    else:
        print(f"访问失败，状态码：{response.status_code}")
except Exception as e:
    print(f"访问地区管理页面时出错：{e}")
    import traceback
    traceback.print_exc()

# 清理测试用户
admin_user.delete()

print("\nTest completed.")
