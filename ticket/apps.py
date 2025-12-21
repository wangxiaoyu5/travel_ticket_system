# 导入Django的AppConfig类
# 用于定义Django应用的配置信息
from django.apps import AppConfig


# 门票应用配置类
# 用于在Django应用注册表中注册ticket应用
class TicketConfig(AppConfig):
    # 应用名称，必须与应用目录名一致
    name = "ticket"