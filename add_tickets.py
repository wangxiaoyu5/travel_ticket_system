from ticket.models import ScenicSpot, TicketType

print('开始为景点添加门票类型...')

scenic_spots = ScenicSpot.objects.all()

for spot in scenic_spots:
    print('\n处理景点：', spot.id, '-', spot.name)
    
    # 跳过测试数据
    if spot.name == '111' or spot.region == '111':
        print('  跳过测试数据')
        continue
    
    # 基本门票类型配置
    base_tickets = [
        {'name': '成人票', 'type': 'single', 'price': spot.price, 'stock': 1000, 'is_active': True},
        {'name': '学生票', 'type': 'single', 'price': round(spot.price * 0.5, 2), 'stock': 500, 'is_active': True},
        {'name': '老人票', 'type': 'single', 'price': round(spot.price * 0.5, 2), 'stock': 300, 'is_active': True},
        {'name': '儿童票', 'type': 'single', 'price': round(spot.price * 0.3, 2), 'stock': 400, 'is_active': True},
        {'name': '军人票', 'type': 'single', 'price': 0.00, 'stock': 200, 'is_active': True},
        {'name': '记者票', 'type': 'single', 'price': 0.00, 'stock': 100, 'is_active': True}
    ]
    
    # 添加套票
    theme_parks = ['迪士尼', '环球影城', '方特', '恐龙园', '长隆', '欢乐谷']
    is_theme_park = any(park in spot.name for park in theme_parks)
    
    if is_theme_park:
        base_tickets.extend([
            {'name': '家庭套票（2大1小）', 'type': 'package', 'price': round(spot.price * 2.2, 2), 'stock': 200, 'is_active': True},
            {'name': '家庭套票（2大2小）', 'type': 'package', 'price': round(spot.price * 2.5, 2), 'stock': 150, 'is_active': True}
        ])
    
    # 自然景观和历史遗迹添加联票
    natural_historical = ['故宫', '长城', '黄山', '九寨沟', '张家界', '桂林', '长白山', '青海湖', '莫高窟', '兵马俑', '龙门石窟']
    is_natural_historical = any(nh in spot.name for nh in natural_historical) or spot.category in ['natural', 'historical']
    
    if is_natural_historical:
        base_tickets.append(
            {'name': '景区联票', 'type': 'package', 'price': round(spot.price * 1.2, 2), 'stock': 300, 'is_active': True}
        )
    
    added_count = 0
    for ticket_data in base_tickets:
        try:
            existing_ticket = TicketType.objects.filter(scenic_spot=spot, name=ticket_data['name']).first()
            if existing_ticket:
                print('  跳过已存在的门票类型：', ticket_data['name'])
                continue
            
            TicketType.objects.create(scenic_spot=spot, **ticket_data)
            print('  添加门票类型：', ticket_data['name'], '(', ticket_data['type'], ') - ￥', ticket_data['price'])
            added_count += 1
        except Exception as e:
            print('  错误：添加门票类型', ticket_data['name'], '失败 -', str(e))
    
    print('  完成：成功添加', added_count, '个门票类型')

print('\n所有景点门票类型添加完成！')
