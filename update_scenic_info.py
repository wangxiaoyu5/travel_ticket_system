#!/usr/bin/env python
"""
从网上获取真实的景点信息，更新数据库中的景点数据
"""
import os
import sys
import requests
from bs4 import BeautifulSoup
import random

# 设置Django环境变量
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_ticket_system.settings')

import django
django.setup()

from ticket.models import ScenicSpot

def get_scenic_info_from_web():
    """从网上获取景点信息"""
    # 这里使用模拟数据，实际项目中可以替换为真实的API或爬虫
    # 实际应用中可以使用携程、马蜂窝等API获取真实数据
    
    scenic_info = {
        '故宫': {
            'price': 60.00,
            'rating': 4.8,
            'description': '故宫博物院是中国明清两代的皇家宫殿，旧称紫禁城，位于北京中轴线的中心。是世界上现存规模最大、保存最为完整的木质结构古建筑之一，是国家AAAAA级旅游景区，1961年被列为第一批全国重点文物保护单位，1987年被列为世界文化遗产。',
        },
        '长城': {
            'price': 40.00,
            'rating': 4.9,
            'description': '长城又称万里长城，是中国古代的军事防御工事，是一道高大、坚固而且连绵不断的长垣，用以限隔敌骑的行动。长城不是一道单纯孤立的城墙，而是以城墙为主体，同大量的城、障、亭、标相结合的防御体系。',
        },
        '黄山': {
            'price': 190.00,
            'rating': 4.9,
            'description': '黄山位于安徽省南部黄山市境内，是中华十大名山之一，天下第一奇山。黄山有72峰，主峰莲花峰海拔1864米，与光明顶、天都峰并称三大黄山主峰，为36大峰之一。黄山是安徽旅游的标志，是中国十大风景名胜唯一的山岳风光。',
        },
        '九寨沟': {
            'price': 190.00,
            'rating': 4.9,
            'description': '九寨沟位于四川省阿坝藏族羌族自治州九寨沟县境内，是中国第一个以保护自然风景为主要目的的自然保护区。九寨沟的翠海、叠瀑、彩林、雪峰、藏情、蓝冰，被称为“六绝”。神奇的九寨，被世人誉为“童话世界”，号称“水景之王”。',
        },
        '张家界国家森林公园': {
            'price': 224.00,
            'rating': 4.8,
            'description': '张家界国家森林公园位于湖南省西北部张家界市境内，是中国第一个国家森林公园，被列入《世界自然遗产名录》。公园自然风光以峰称奇、以谷显幽、以林见秀。其间有奇峰3000多座，如人如兽、如器如物，形象逼真，气势壮观，有“三千奇峰，八百秀水”之美称。',
        },
        '上海迪士尼度假区': {
            'price': 439.00,
            'rating': 4.7,
            'description': '上海迪士尼度假区是中国内地首座迪士尼主题乐园，位于上海市浦东新区川沙新镇。上海迪士尼乐园拥有七大主题园区：米奇大街、奇想花园、探险岛、宝藏湾、明日世界、梦幻世界、迪士尼·皮克斯玩具总动员。',
        },
        '三亚亚龙湾': {
            'price': 110.00,
            'rating': 4.7,
            'description': '亚龙湾位于海南省三亚市东南28公里处，是海南最南端的一个半月形海湾，全长约7.5公里，是海南名景之一。亚龙湾沙滩绵延7公里且平缓宽阔，浅海区宽达50-60米。沙粒洁白细软，海水澄澈晶莹，而且蔚蓝。能见度7-9米。海底世界资源丰富，有珊瑚礁、各种热带鱼、名贵贝类等。',
        },
        '布达拉宫': {
            'price': 100.00,
            'rating': 4.9,
            'description': '布达拉宫位于中国西藏自治区首府拉萨市区西北的玛布日山上，是一座宫堡式建筑群，最初是吐蕃王朝赞普松赞干布为迎娶文成公主而兴建。于17世纪重建后，成为历代达赖喇嘛的冬宫居所，为西藏政教合一的统治中心。1961年，布达拉宫成为了中华人民共和国国务院第一批全国重点文物保护单位之一。1994年，布达拉宫被列为世界文化遗产。',
        },
        '桂林漓江': {
            'price': 210.00,
            'rating': 4.8,
            'description': '漓江，属珠江流域西江水系，为支流桂江上游河段的通称，位于广西壮族自治区东北部。传统意义上的漓江起点为桂江源头越城岭猫儿山，现代水文定义为兴安县溶江镇灵渠口，终点为平乐三江口。漓江段全长164公里。沿江河床多为水质卵石，泥沙量小，水质清澈，两岸多为岩溶地貌。旅游资源丰富，著名的桂林山水就在漓江上。',
        },
        '秦始皇兵马俑': {
            'price': 120.00,
            'rating': 4.8,
            'description': '秦始皇兵马俑，简称秦兵马俑或秦俑，第一批全国重点文物保护单位，第一批中国世界遗产，位于今陕西省西安市临潼区秦始皇陵以东1.5千米处的兵马俑坑内。兵马俑是古代墓葬雕塑的一个类别。古代实行人殉，奴隶是奴隶主生前的附属品，奴隶主死后奴隶要作为殉葬品为奴隶主陪葬。兵马俑即制成兵马（战车、战马、士兵）形状的殉葬品。',
        },
        '苏州园林': {
            'price': 70.00,
            'rating': 4.7,
            'description': '苏州古典园林，亦称“苏州园林”，是位于江苏省苏州市境内的中国古典园林的总称。苏州古典园林溯源于春秋，发展于晋唐，繁荣于两宋，全盛于明清。苏州素有“园林之城”的美誉，境内私家园林始建于前6世纪，清末时城内外有园林170多处，现存50多处。',
        },
    }
    
    return scenic_info

def update_scenic_info():
    """更新景点信息"""
    # 获取景点信息
    scenic_info = get_scenic_info_from_web()
    
    print("开始更新景点信息...")
    
    updated_count = 0
    skipped_count = 0
    
    # 遍历景点信息，更新数据库
    for spot_name, info in scenic_info.items():
        try:
            # 查找景点
            spot = ScenicSpot.objects.get(name=spot_name)
            
            # 更新景点信息
            spot.price = info['price']
            spot.rating = info['rating']
            spot.description = info['description']
            spot.save()
            
            print(f"✓ 更新成功: {spot_name} - 价格: {info['price']}, 评分: {info['rating']}")
            updated_count += 1
        except ScenicSpot.DoesNotExist:
            print(f"✗ 景点不存在: {spot_name}")
            skipped_count += 1
    
    print(f"\n✅ 更新完成！")
    print(f"- 总更新景点数: {updated_count}")
    print(f"- 跳过景点数: {skipped_count}")
    print(f"- 景点总数: {ScenicSpot.objects.count()}")

if __name__ == "__main__":
    update_scenic_info()