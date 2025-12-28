#!/usr/bin/env python3
"""
初始化景点的display_id字段
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 配置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_ticket_system.settings')

import django
django.setup()

from ticket.models import ScenicSpot

def main():
    """初始化display_id"""
    # 获取所有景点，按id升序排序
    scenic_spots = ScenicSpot.objects.all().order_by('id')
    
    # 为每个景点分配连续的display_id
    for index, spot in enumerate(scenic_spots, start=1):
        spot.display_id = index
        spot.save()
    
    print(f'成功更新了 {len(scenic_spots)} 个景点的display_id')
    print('所有景点的display_id已连续分配')

if __name__ == '__main__':
    main()
