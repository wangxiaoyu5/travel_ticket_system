import os
import django
from django.conf import settings

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_ticket_system.settings')
django.setup()

# 导入数据库连接
from django.db import connection

# 修复数据库函数
def fix_database():
    with connection.cursor() as cursor:
        print("开始修复数据库...")
        
        # 1. 检查scenicspot表中是否存在category字段
        cursor.execute("SHOW COLUMNS FROM ticket_scenicspot LIKE 'category';")
        category_column = cursor.fetchone()
        
        if not category_column:
            # 如果不存在，添加category字段
            print("添加category字段...")
            cursor.execute("ALTER TABLE ticket_scenicspot ADD COLUMN category VARCHAR(50) DEFAULT '自然风光类';")
            print("category字段添加成功")
        else:
            print(f"category字段已存在，类型为: {category_column[1]}")
            
            # 如果类型不是VARCHAR，修改为VARCHAR
            if 'varchar' not in category_column[1].lower():
                print("修改category字段类型为VARCHAR...")
                cursor.execute("ALTER TABLE ticket_scenicspot MODIFY COLUMN category VARCHAR(50) DEFAULT '自然风光类';")
                print("category字段类型修改成功")
        
        # 2. 检查scenicspot表中是否存在region字段
        cursor.execute("SHOW COLUMNS FROM ticket_scenicspot LIKE 'region';")
        region_column = cursor.fetchone()
        
        if not region_column:
            # 如果不存在，添加region字段
            print("添加region字段...")
            cursor.execute("ALTER TABLE ticket_scenicspot ADD COLUMN region VARCHAR(50) DEFAULT '全国';")
            print("region字段添加成功")
        else:
            print(f"region字段已存在，类型为: {region_column[1]}")
            
            # 如果类型不是VARCHAR，修改为VARCHAR
            if 'varchar' not in region_column[1].lower():
                print("修改region字段类型为VARCHAR...")
                cursor.execute("ALTER TABLE ticket_scenicspot MODIFY COLUMN region VARCHAR(50) DEFAULT '全国';")
                print("region字段类型修改成功")
        
        # 3. 检查是否存在category表
        cursor.execute("SHOW TABLES LIKE 'ticket_category';")
        category_table = cursor.fetchone()
        
        if not category_table:
            print("创建category表...")
            cursor.execute("""CREATE TABLE ticket_category (
                id BIGINT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50) UNIQUE NOT NULL,
                description TEXT NULL,
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;""")
            print("category表创建成功")
        else:
            print("category表已存在")
        
        # 4. 检查是否存在region表
        cursor.execute("SHOW TABLES LIKE 'ticket_region';")
        region_table = cursor.fetchone()
        
        if not region_table:
            print("创建region表...")
            cursor.execute("""CREATE TABLE ticket_region (
                id BIGINT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) UNIQUE NOT NULL,
                parent_id BIGINT NULL,
                level INT NOT NULL DEFAULT 1,
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;""")
            print("region表创建成功")
        else:
            print("region表已存在")
        
        print("数据库修复完成！")

# 运行修复函数
if __name__ == "__main__":
    fix_database()
