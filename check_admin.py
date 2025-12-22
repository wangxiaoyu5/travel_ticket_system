import os
import sys
import django

# 设置Django环境
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_ticket_system.settings')
django.setup()

from ticket.models import User

# 检查管理员用户
def check_admin_users():
    print("检查系统中的管理员用户...")
    
    # 查询所有用户
    users = User.objects.all()
    
    if not users:
        print("系统中没有任何用户")
        return
    
    print(f"系统中共有 {users.count()} 个用户")
    print("\n管理员用户列表：")
    
    # 角色对应的中文名称
    role_map = {
        0: '游客',
        1: '景点管理员',
        2: '网站管理员'
    }
    
    for user in users:
        role_name = role_map.get(user.role, '未知角色')
        print(f"用户名: {user.username}, 邮箱: {user.email}, 角色: {role_name}")

if __name__ == "__main__":
    check_admin_users()
