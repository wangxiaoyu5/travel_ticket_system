# 导入Django的admin模块
# 用于在Django默认后台管理系统中注册和管理模型
from django.contrib import admin

# Register your models here.
# 示例：admin.site.register(YourModel)  # 将模型注册到admin后台
# 注意：当前项目使用自定义admin后台，未使用Django默认admin
# 如需启用默认admin，需在根urls.py中取消注释 path("admin/", admin.site.urls)