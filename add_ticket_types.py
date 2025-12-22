#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为景点添加合适的门票类型脚本
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 初始化Django环境
import django
django.setup()

from ticket.models import ScenicSpot, TicketType


def add_ticket_types():
    """为各个景点添加合适的门票类型"""
    
    # 获取所有景点
    scenic_spots = ScenicSpot.objects.all()
    
    print(f"开始为 {len(scenic_spots)} 个景点添加门票类型...")
    
    for spot in scenic_spots:
        print(f"\n处理景点：{spot.id} - {spot.name}")
        
        # 跳过测试数据
        if spot.name == "111" or spot.region == "111":
            print(f"  跳过测试数据")
            continue
        
        # 基本门票类型配置
        base_tickets = [
            # 单票类型
            {
                "name": "成人票",
                "type": "single",
                "price": spot.price,  # 使用景点默认价格
                "stock": 1000,
                "is_active": True
            },
            {
                "name": "学生票",
                "type": "single",
                "price": round(spot.price * 0.5, 2),  # 学生票半价
                "stock": 500,
                "is_active": True
            },
            {
                "name": "老人票",
                "type": "single",
                "price": round(spot.price * 0.5, 2),  # 老人票半价
                "stock": 300,
                "is_active": True
            },
            {
                "name": "儿童票",
                "type": "single",
                "price": round(spot.price * 0.3, 2),  # 儿童票3折
                "stock": 400,
                "is_active": True
            },
            {
                "name": "军人票",
                "type": "single",
                "price": 0.00,  # 军人免票
                "stock": 200,
                "is_active": True
            },
            {
                "name": "记者票",
                "type": "single",
                "price": 0.00,  # 记者免票
                "stock": 100,
                "is_active": True
            }
        ]
        
        # 添加套票（根据景点类型选择性添加）
        theme_parks = ["迪士尼", "环球影城", "方特", "恐龙园", "长隆", "欢乐谷"]
        is_theme_park = any(park in spot.name for park in theme_parks)
        
        if is_theme_park:
            # 主题乐园添加家庭套票
            base_tickets.extend([
                {
                    "name": "家庭套票（2大1小）",
                    "type": "package",
                    "price": round(spot.price * 2.2, 2),  # 2大1小优惠价格
                    "stock": 200,
                    "is_active": True
                },
                {
                    "name": "家庭套票（2大2小）",
                    "type": "package",
                    "price": round(spot.price * 2.5, 2),  # 2大2小优惠价格
                    "stock": 150,
                    "is_active": True
                }
            ])
        
        # 自然景观和历史遗迹添加联票
        natural_historical = ["故宫", "长城", "黄山", "九寨沟", "张家界", "桂林", "长白山", "青海湖", "莫高窟", "兵马俑", "龙门石窟"]
        is_natural_historical = any(spot in spot.name for spot in natural_historical) or spot.category in ["natural", "historical"]
        
        if is_natural_historical:
            base_tickets.append(
                {
                    "name": "景区联票",
                    "type": "package",
                    "price": round(spot.price * 1.2, 2),  # 联票优惠价格
                    "stock": 300,
                    "is_active": True
                }
            )
        
        # 开始添加门票类型
        added_count = 0
        for ticket_data in base_tickets:
            try:
                # 检查是否已存在相同名称的门票类型
                existing_ticket = TicketType.objects.filter(
                    scenic_spot=spot,
                    name=ticket_data["name"]
                ).first()
                
                if existing_ticket:
                    print(f"  跳过已存在的门票类型：{ticket_data['name']}")
                    continue
                
                # 创建门票类型
                TicketType.objects.create(
                    scenic_spot=spot,
                    **ticket_data
                )
                print(f"  添加门票类型：{ticket_data['name']} ({ticket_data['type']}) - ￥{ticket_data['price']}")
                added_count += 1
            except Exception as e:
                print(f"  错误：添加门票类型 {ticket_data['name']} 失败 - {str(e)}")
        
        print(f"  完成：成功添加 {added_count} 个门票类型")
    
    print(f"\n所有景点门票类型添加完成！")


if __name__ == "__main__":
    add_ticket_types()
