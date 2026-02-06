"""
URL configuration for travel_ticket_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# 导入Django默认的admin模块
# 注意：当前项目未使用默认admin，已注释掉相关配置
from django.contrib import admin

# 导入URL路由相关函数
from django.urls import path, include

# 导入项目设置
from django.conf import settings

# 导入静态文件URL配置函数
from django.conf.urls.static import static

# URL路由列表 - 定义项目的所有URL映射
urlpatterns = [
    # 将所有URL请求转发到ticket应用的urls.py处理
    # 空字符串表示根路径，所有请求都会被ticket应用处理e
    # 这种配置方式使得ticket应用成为项目的主要应用
    path('', include('ticket.urls')),
    
    # 注意：已移除默认Django admin配置，避免与自定义admin冲突
    # path("admin/", admin.site.urls),
]

# 在开发模式下添加媒体文件URL配置
# 生产环境中，媒体文件通常由Web服务器直接处理
if settings.DEBUG:
    # 添加媒体文件URL映射，将/media/路径的请求映射到MEDIA_ROOT目录
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)