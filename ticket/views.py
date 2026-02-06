# 导入Django的快捷函数，用于渲染模板、重定向和生成URL
# 导入消息框架，用于向用户显示提示信息
from django.contrib import messages
# 导入Django的认证函数，用于用户登录、退出和认证
from django.contrib.auth import login, logout
# 导入登录装饰器，用于保护需要登录才能访问的视图
from django.contrib.auth.decorators import login_required
# 导入Django ORM模型模块
from django.db import models
# 导入时区模块，用于处理时间
from django.utils import timezone
# 导入JsonResponse，用于返回JSON响应
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse
# 导入分页模块
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# 导入自定义模型，用于数据库查询
from .models import ScenicSpot, News, Carousel, User, Cart, Order, ScenicSpotComment, TicketType, BrowseHistory, Category, Region, Collection, DateStock


# 首页视图函数，处理网站首页的请求
# request: HTTP请求对象，包含用户请求的所有信息
def index(request):
    # 从数据库中获取所有激活状态的轮播图，按轮播顺序排序
    carousels = Carousel.objects.filter(is_active=True)
    # 从数据库中获取所有标记为公告的资讯，按创建时间倒序排列，只取前3条
    announcements = News.objects.filter(is_announcement=True).order_by('-created_at')[:3]
    # 从数据库中获取所有非公告的旅游资讯，按创建时间倒序排列，只取前4条
    latest_news = News.objects.filter(is_announcement=False).order_by('-created_at')[:4]
    # 从数据库中获取所有标记为热门的景点，按创建时间倒序排列，只取前6条
    hot_spots = ScenicSpot.objects.filter(is_hot=True).order_by('-created_at')[:6]

    # 构建上下文字典，将查询到的数据传递给模板
    context = {
        'carousels': carousels,  # 轮播图数据
        'announcements': announcements,  # 公告数据
        'latest_news': latest_news,  # 最新资讯数据
        'hot_spots': hot_spots,  # 热门景点数据
    }
    # 渲染index.html模板，将上下文数据传递给模板
    return render(request, 'index.html', context)


# 登录视图函数，处理用户登录请求
def user_login(request):
    # 获取next参数，用于登录后跳转回原页面
    next_url = request.GET.get('next', '')
    
    # 判断请求方法是否为POST（表单提交）
    if request.method == 'POST':
        # 从POST请求中获取用户名
        username = request.POST.get('username')
        # 从POST请求中获取密码
        password = request.POST.get('password')
        # 从POST请求中获取角色
        role = request.POST.get('role')
        # 从POST请求中获取景点ID
        scenic_spot_id = request.POST.get('scenic_spot')
        # 从POST请求中获取next参数
        next_url = request.POST.get('next', '')

        try:
            # 根据用户名查找用户
            user = User.objects.get(username=username)
            # 验证密码
            if user.check_password(password):
                # 验证角色是否匹配
                if str(user.role) == role:
                    # 使用Django的login函数登录用户，创建会话
                    login(request, user)
                    
                    # 优先检查是否有next参数，如果有则跳转到该页面
                    if next_url:
                        return redirect(next_url)
                    
                    # 检查会话中是否有购票选择，如果有则跳转到购票页面
                    buy_ticket_selection = request.session.get('buy_ticket_selection')
                    if buy_ticket_selection and user.role == 0:  # 只有游客角色需要
                        # 删除会话中的购票选择，避免重复使用
                        spot_id = buy_ticket_selection.pop('spot_id')
                        request.session.save()
                        # 跳转到购票页面
                        return redirect(reverse('ticket:buy_ticket', kwargs={'spot_id': spot_id}))
                    
                    # 根据用户角色重定向到不同页面
                    if user.role == 2:  # 网站管理员
                        return redirect(reverse('ticket:admin_user_list'))  # 跳转到用户管理页面
                    elif user.role == 1:  # 景点管理员
                        return redirect(reverse('ticket:scenic_admin_scenic_spots'))  # 跳转到景点管理页面
                    else:  # 游客
                        return redirect(reverse('ticket:index'))
                else:
                    # 角色不匹配
                    messages.error(request, '角色不匹配')
            else:
                # 密码错误
                messages.error(request, '用户名或密码错误')
        except User.DoesNotExist:
            # 用户不存在
            messages.error(request, '用户名或密码错误')
    # 如果请求方法不是POST，或者验证失败，渲染login.html模板，传递next参数
    return render(request, 'login.html', {'next': next_url})


# 退出登录视图函数，处理用户退出请求
def user_logout(request):
    # 使用Django的logout函数退出用户，清除会话
    logout(request)
    # 重定向到首页，使用reverse函数根据URL名称生成URL，需要包含命名空间
    return redirect(reverse('ticket:index'))


# 忘记密码视图函数，处理用户忘记密码请求
def forgot_password(request):
    if request.method == 'POST':
        # 获取用户输入的邮箱、新密码和确认密码
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        # 验证密码
        if new_password != confirm_password:
            messages.error(request, '两次输入的密码不一致')
            return render(request, 'forgot_password.html')
        
        try:
            # 根据邮箱查找用户
            user = User.objects.get(email=email)
            # 更新密码
            user.set_password(new_password)
            user.save()
            # 显示成功消息
            messages.success(request, '密码重置成功，请使用新密码登录')
            # 重定向到登录页面
            return redirect(reverse('ticket:login'))
        except User.DoesNotExist:
            # 用户不存在，显示错误消息
            messages.error(request, '该邮箱未注册')
    # GET请求，渲染忘记密码模板
    return render(request, 'forgot_password.html')


# 景点管理员后台视图函数，需要登录且角色为景点管理员才能访问
def scenic_admin_required(view_func):
    @login_required
    def wrapped_view(request, *args, **kwargs):
        if request.user.role == 1:  # 1表示景点管理员
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, '您没有权限访问该页面')
            return redirect(reverse('ticket:index'))

    return wrapped_view





# 景点信息管理视图
@scenic_admin_required
def scenic_admin_scenic_spots(request):
    # 获取当前景点管理员
    admin = request.user
    
    # 获取当前页码，默认为1
    page = request.GET.get('page', 1)

    # 从数据库获取该管理员管理的景点
    scenic_spots = ScenicSpot.objects.filter(admin=admin).order_by('-created_at')

    # 分页处理，每页显示10个景点
    paginator = Paginator(scenic_spots, 10)
    try:
        # 获取当前页的景点列表
        scenic_spots_paginated = paginator.page(page)
    except PageNotAnInteger:
        # 如果页码不是整数，返回第一页
        scenic_spots_paginated = paginator.page(1)
    except EmptyPage:
        # 如果页码超出范围，返回最后一页
        scenic_spots_paginated = paginator.page(paginator.num_pages)

    # 构建上下文数据
    context = {
        'scenic_spots': scenic_spots_paginated,
        'paginator': paginator,
        'page_obj': scenic_spots_paginated
    }

    return render(request, 'scenic_admin/scenic_spots.html', context)


# 编辑景点视图
@scenic_admin_required
def scenic_admin_edit_scenic_spot(request, spot_id):
    try:
        # 获取当前景点管理员
        admin = request.user

        # 根据spot_id从数据库获取景点信息，确保该景点属于当前管理员
        scenic_spot = ScenicSpot.objects.get(id=spot_id, admin=admin)
    except ScenicSpot.DoesNotExist:
        # 景点不存在或不属于当前管理员，显示错误消息并重定向
        messages.error(request, '景点不存在或您没有权限访问')
        return redirect(reverse('ticket:scenic_admin_scenic_spots'))

    if request.method == 'POST':
        # 从POST请求中获取表单数据
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('cover')  # 模板中是cover，不是image
        address = request.POST.get('address')
        category = request.POST.get('category')
        stock = request.POST.get('stock')  # 模板中是stock，不是total_tickets
        status = request.POST.get('status')  # 模板中是status，用于设置is_active

        # 表单验证
        if not name or not description or not price or not address or not category or not stock:
            messages.error(request, '请填写所有必填字段')
            return render(request, 'scenic_admin/edit_scenic_spot.html', {'scenic_spot': scenic_spot})

        try:
            # 更新景点信息
            scenic_spot.name = name
            scenic_spot.description = description
            scenic_spot.price = float(price)
            scenic_spot.address = address
            scenic_spot.category = category
            scenic_spot.total_tickets = int(stock)
            scenic_spot.is_active = status == '1'  # 将status转换为is_active

            # 处理图片上传
            if image:
                scenic_spot.image = image

            # 保存更新后的景点信息到数据库
            scenic_spot.save()

            # 显示成功消息
            messages.success(request, '景点信息更新成功')

            # 重定向到景点列表页面
            return redirect(reverse('ticket:scenic_admin_scenic_spots'))
        except Exception as e:
            # 显示错误消息
            messages.error(request, f'更新景点失败: {str(e)}')
            return render(request, 'scenic_admin/edit_scenic_spot.html', {'scenic_spot': scenic_spot})

    # GET请求，渲染编辑景点表单，传递当前景点数据
    return render(request, 'scenic_admin/edit_scenic_spot.html', {'scenic_spot': scenic_spot})


# 新增景点视图
@scenic_admin_required
def scenic_admin_add_scenic_spot(request):
    if request.method == 'POST':
        # 获取当前景点管理员
        admin = request.user
        
        # 从POST请求中获取表单数据
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('cover')  # 模板中是cover，不是image
        address = request.POST.get('address')
        category = request.POST.get('category')
        stock = request.POST.get('stock')  # 模板中是stock，不是total_tickets
        status = request.POST.get('status')  # 模板中有status字段，用于设置is_active
        
        # 表单验证
        if not name or not description or not price or not address or not category or not stock or not image:
            messages.error(request, '请填写所有必填字段')
            return render(request, 'scenic_admin/add_scenic_spot.html')
        
        try:
            # 创建新景点，关联到当前管理员
            scenic_spot = ScenicSpot.objects.create(
                admin=admin,
                name=name,
                description=description,
                price=float(price),
                image=image,
                address=address,
                category=category,
                total_tickets=int(stock),
                is_active=status == '1',
                # 设置默认值，因为模板中没有这些字段
                opening_hours='',
                is_hot=False,
                region=None,
                tags=''
            )
            
            # 重新排序display_id
            reorder_scenic_display_ids()
            
            # 显示成功消息
            messages.success(request, '景点添加成功')
            
            # 重定向到景点列表页面
            return redirect(reverse('ticket:scenic_admin_scenic_spots'))
        except Exception as e:
            # 显示错误消息
            messages.error(request, f'添加景点失败: {str(e)}')
            return render(request, 'scenic_admin/add_scenic_spot.html')
    
    # GET请求，渲染新增景点表单
    return render(request, 'scenic_admin/add_scenic_spot.html')


# 景点批量操作视图
@scenic_admin_required
def scenic_admin_batch_operate_scenic_spots(request):
    if request.method == 'POST':
        # 获取操作类型
        operation = request.POST.get('operation')
        
        try:
            # 获取当前景点管理员
            admin = request.user
            
            # 处理单个景点操作
            if operation.startswith('activate_single_') or operation.startswith('deactivate_single_') or operation.startswith('delete_single_'):
                # 提取景点ID
                spot_id = int(operation.split('_')[-1])
                
                # 获取单个景点
                scenic_spot = ScenicSpot.objects.get(admin=admin, id=spot_id)
                
                if operation.startswith('activate_single_'):
                    # 单个景点上架
                    scenic_spot.is_active = True
                    scenic_spot.save()
                    messages.success(request, f'成功上架景点: {scenic_spot.name}')
                elif operation.startswith('deactivate_single_'):
                    # 单个景点下架
                    scenic_spot.is_active = False
                    scenic_spot.save()
                    messages.success(request, f'成功下架景点: {scenic_spot.name}')
                elif operation.startswith('delete_single_'):
                    # 单个景点删除
                    scenic_spot.delete()
                    # 重新排序display_id
                    reorder_scenic_display_ids()
                    messages.success(request, '成功删除景点')
            else:
                # 处理批量操作
                spot_ids = request.POST.getlist('spot_ids')
                
                if not spot_ids:
                    messages.error(request, '请选择要操作的景点')
                    return redirect(reverse('ticket:scenic_admin_scenic_spots'))
                
                # 获取当前管理员管理的景点
                scenic_spots = ScenicSpot.objects.filter(admin=admin, id__in=spot_ids)
                
                if operation == 'activate':
                    # 批量上架：设置is_active=True
                    scenic_spots.update(is_active=True)
                    messages.success(request, f'成功上架 {scenic_spots.count()} 个景点')
                elif operation == 'deactivate':
                    # 批量下架：设置is_active=False
                    scenic_spots.update(is_active=False)
                    messages.success(request, f'成功下架 {scenic_spots.count()} 个景点')
                elif operation == 'delete':
                    # 批量删除
                    scenic_spots.delete()
                    # 重新排序display_id
                    reorder_scenic_display_ids()
                    messages.success(request, f'成功删除 {len(spot_ids)} 个景点')
        except ScenicSpot.DoesNotExist:
            messages.error(request, '景点不存在或无权限访问')
        except Exception as e:
            messages.error(request, f'操作失败: {str(e)}')
    
    return redirect(reverse('ticket:scenic_admin_scenic_spots'))


# 门票类型管理视图
@scenic_admin_required
def scenic_admin_ticket_types(request):
    # 获取当前景点管理员
    admin = request.user
    
    # 获取当前页码，默认为1
    page = request.GET.get('page', 1)
    
    # 获取当前管理员管理的景点
    scenic_spots = ScenicSpot.objects.filter(admin=admin)
    scenic_ids = scenic_spots.values_list('id', flat=True)
    
    # 获取当前管理员管理的景点的门票类型
    ticket_types = TicketType.objects.filter(scenic_spot__id__in=scenic_ids).order_by('-created_at')
    
    # 分页处理，每页显示10个门票类型
    paginator = Paginator(ticket_types, 10)
    try:
        # 获取当前页的门票类型列表
        ticket_types_paginated = paginator.page(page)
    except PageNotAnInteger:
        # 如果页码不是整数，返回第一页
        ticket_types_paginated = paginator.page(1)
    except EmptyPage:
        # 如果页码超出范围，返回最后一页
        ticket_types_paginated = paginator.page(paginator.num_pages)
    
    # 获取选择的日期，如果没有或为空则使用当天日期
    from datetime import date
    today = date.today().strftime('%Y-%m-%d')
    selected_date = request.GET.get('selected_date') or today
    
    # 预处理日期库存数据
    ticket_data = []
    for ticket in ticket_types_paginated:
        # 解析日期字符串为date对象
        from datetime import datetime
        selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
        # 获取对应日期的库存记录
        date_stock = ticket.datestock_set.filter(use_date=selected_date_obj).first()
        
        # 添加到数据列表
        ticket_data.append({
            'ticket': ticket,
            'date_stock': date_stock
        })
    
    # 构建上下文数据
    context = {
        'ticket_data': ticket_data,
        'selected_date': selected_date,
        'today': today,
        'paginator': paginator,
        'page_obj': ticket_types_paginated
    }
    
    return render(request, 'scenic_admin/ticket_types.html', context)


# 新增门票类型视图
@scenic_admin_required
def scenic_admin_add_ticket_type(request):
    # 获取当前景点管理员
    admin = request.user
    
    # 获取当前管理员管理的景点
    scenic_spots = ScenicSpot.objects.filter(admin=admin)
    
    if request.method == 'POST':
        # 获取表单数据
        name = request.POST.get('name')
        type = request.POST.get('type')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        is_active = request.POST.get('is_active') == '1'
        
        # 创建门票类型
        try:
            # 假设当前管理员只有一个景点，实际情况可能需要选择景点
            scenic_spot = scenic_spots.first()
            
            ticket_type = TicketType(
                scenic_spot=scenic_spot,
                name=name,
                type=type,
                price=price,
                stock=stock,
                is_active=is_active
            )
            ticket_type.save()
            
            # 如果有selected_date参数，同时为该日期创建库存记录
            selected_date = request.GET.get('selected_date')
            if selected_date:
                from datetime import datetime
                selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
                # 创建对应日期的库存记录
                ticket_type.datestock_set.create(
                    use_date=selected_date_obj,
                    stock=stock
                )
            
            messages.success(request, '新增门票类型成功')
            # 重定向时保留当前选择的日期
            from datetime import date
            today = date.today().strftime('%Y-%m-%d')
            selected_date = request.GET.get('selected_date') or today
            return redirect(f"{reverse('ticket:scenic_admin_ticket_types')}?selected_date={selected_date}")
        except Exception as e:
            messages.error(request, f'新增门票类型失败: {str(e)}')
    
    # GET请求，渲染新增门票类型表单
    context = {
        'scenic_spots': scenic_spots
    }
    return render(request, 'scenic_admin/add_ticket_type.html', context)


# 编辑门票类型视图
@scenic_admin_required
def scenic_admin_edit_ticket_type(request, ticket_id):
    # 获取当前景点管理员
    admin = request.user
    
    # 获取当前管理员管理的景点
    scenic_spots = ScenicSpot.objects.filter(admin=admin)
    scenic_ids = scenic_spots.values_list('id', flat=True)
    
    # 获取要编辑的门票类型
    try:
        ticket_type = TicketType.objects.get(id=ticket_id, scenic_spot__id__in=scenic_ids)
    except TicketType.DoesNotExist:
        messages.error(request, '门票类型不存在或无权限访问')
        # 重定向时保留当前选择的日期
        from datetime import date
        today = date.today().strftime('%Y-%m-%d')
        selected_date = request.GET.get('selected_date') or today
        return redirect(f"{reverse('ticket:scenic_admin_ticket_types')}?selected_date={selected_date}")
    
    if request.method == 'POST':
        # 获取表单数据
        name = request.POST.get('name')
        type = request.POST.get('type')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        is_active = request.POST.get('is_active') == '1'
        
        # 更新门票类型
        try:
            # 保存门票类型的基本信息
            ticket_type.name = name
            ticket_type.type = type
            ticket_type.price = price
            ticket_type.stock = stock
            ticket_type.is_active = is_active
            ticket_type.save()
            
            # 如果有selected_date参数，同时更新该日期的库存记录
            selected_date = request.GET.get('selected_date')
            if selected_date:
                from datetime import datetime
                selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
                # 获取或创建对应日期的库存记录
                date_stock, created = ticket_type.datestock_set.get_or_create(
                    use_date=selected_date_obj,
                    defaults={'stock': stock}
                )
                # 更新该日期的库存数量
                date_stock.stock = stock
                date_stock.save()
            
            messages.success(request, '编辑门票类型成功')
            # 重定向时保留当前选择的日期
            from datetime import date
            today = date.today().strftime('%Y-%m-%d')
            selected_date = request.GET.get('selected_date') or today
            return redirect(f"{reverse('ticket:scenic_admin_ticket_types')}?selected_date={selected_date}")
        except Exception as e:
            messages.error(request, f'编辑门票类型失败: {str(e)}')
    
    # GET请求，渲染编辑门票类型表单
    context = {
        'scenic_spots': scenic_spots,
        'ticket_type': ticket_type
    }
    return render(request, 'scenic_admin/add_ticket_type.html', context)


# 批量操作门票类型视图
@scenic_admin_required
def scenic_admin_batch_operate_ticket_types(request):
    if request.method == 'POST':
        # 获取操作类型和选中的门票类型ID
        operation = request.POST.get('operation')
        ticket_ids = request.POST.getlist('ticket_ids')
        
        if not ticket_ids:
            messages.error(request, '请选择要操作的门票类型')
            # 重定向时保留当前选择的日期
            from datetime import date
            today = date.today().strftime('%Y-%m-%d')
            # 从请求中获取selected_date参数，POST请求中可能没有，所以从GET中获取
            selected_date = request.GET.get('selected_date', today)
            return redirect(f"{reverse('ticket:scenic_admin_ticket_types')}?selected_date={selected_date}")
        
        try:
            # 获取当前景点管理员
            admin = request.user
            scenic_spots = ScenicSpot.objects.filter(admin=admin)
            scenic_ids = scenic_spots.values_list('id', flat=True)
            
            # 获取当前管理员管理的景点的门票类型
            tickets = TicketType.objects.filter(
                id__in=ticket_ids,
                scenic_spot__id__in=scenic_ids
            )
            
            if operation == 'activate':
                # 批量上架
                tickets.update(is_active=True)
                messages.success(request, f'成功上架 {tickets.count()} 个门票类型')
            elif operation == 'deactivate':
                # 批量下架
                tickets.update(is_active=False)
                messages.success(request, f'成功下架 {tickets.count()} 个门票类型')
            elif operation == 'delete':
                # 批量删除
                tickets.delete()
                messages.success(request, f'成功删除 {len(ticket_ids)} 个门票类型')
        except Exception as e:
            messages.error(request, f'操作失败: {str(e)}')
    
    # 重定向时保留当前选择的日期
    from datetime import date
    today = date.today().strftime('%Y-%m-%d')
    # 从请求中获取selected_date参数，POST请求中可能没有，所以从GET中获取
    selected_date = request.GET.get('selected_date', today)
    return redirect(f"{reverse('ticket:scenic_admin_ticket_types')}?selected_date={selected_date}")

# 更新日期库存视图
@scenic_admin_required
def scenic_admin_update_date_stock(request):
    if request.method == 'POST':
        # 获取门票类型ID、使用日期和库存数量
        ticket_type_id = request.POST.get('ticket_type_id')
        use_date = request.POST.get('use_date')
        stock = request.POST.get('stock')
        
        try:
            # 获取当前景点管理员
            admin = request.user
            scenic_spots = ScenicSpot.objects.filter(admin=admin)
            scenic_ids = scenic_spots.values_list('id', flat=True)
            
            # 验证门票类型是否属于当前管理员
            ticket_type = TicketType.objects.get(
                id=ticket_type_id,
                scenic_spot__id__in=scenic_ids
            )
            
            # 更新或创建DateStock记录
            date_stock, created = DateStock.objects.update_or_create(
                ticket_type=ticket_type,
                use_date=use_date,
                defaults={'stock': stock}
            )
            
            messages.success(request, f'成功更新 {use_date} 的库存')
        except Exception as e:
            messages.error(request, f'操作失败: {str(e)}')
    
    # 重定向回门票类型列表页，保留选中的日期
    return redirect(f"{reverse('ticket:scenic_admin_ticket_types')}?selected_date={use_date}")


# 订单管理视图
@scenic_admin_required
def scenic_admin_orders(request):
    # 获取当前景点管理员
    admin = request.user

    # 从数据库获取该管理员管理的景点
    scenic_spots = ScenicSpot.objects.filter(admin=admin)

    # 获取景点ID列表，用于后续查询
    scenic_ids = scenic_spots.values_list('id', flat=True)

    # 从请求中获取筛选条件
    status = request.GET.get('status')
    search_query = request.GET.get('q') or ''
    # 获取当前页码，默认为1
    page = request.GET.get('page', 1)

    # 构建查询
    orders = Order.objects.filter(scenic_spot__id__in=scenic_ids)

    # 根据状态筛选
    if status is not None:
        orders = orders.filter(status=status)

    # 根据搜索条件筛选
    if search_query:
        orders = orders.filter(
            models.Q(order_number__icontains=search_query) |
            models.Q(user__username__icontains=search_query) |
            models.Q(user__email__icontains=search_query)
        )

    # 按创建时间倒序排序
    orders = orders.order_by('-created_at')

    # 分页处理，每页显示10条订单
    paginator = Paginator(orders, 10)
    try:
        # 获取当前页的订单列表
        orders_paginated = paginator.page(page)
    except PageNotAnInteger:
        # 如果页码不是整数，返回第一页
        orders_paginated = paginator.page(1)
    except EmptyPage:
        # 如果页码超出范围，返回最后一页
        orders_paginated = paginator.page(paginator.num_pages)

    # 构建上下文数据
    context = {
        'orders': orders_paginated,
        'current_status': status,
        'search_query': search_query,
        'paginator': paginator,
        'page_obj': orders_paginated
    }

    return render(request, 'scenic_admin/orders.html', context)


# 留言管理视图
@scenic_admin_required
def scenic_admin_comments(request):
    # 获取当前景点管理员
    admin = request.user

    # 从数据库获取该管理员管理的景点
    scenic_spots = ScenicSpot.objects.filter(admin=admin)

    # 获取景点ID列表，用于后续查询
    scenic_ids = scenic_spots.values_list('id', flat=True)

    # 从请求中获取筛选条件
    replied = request.GET.get('replied')
    search_query = request.GET.get('q')
    # 获取当前页码，默认为1
    page = request.GET.get('page', 1)

    # 构建查询
    comments = ScenicSpotComment.objects.filter(scenic_spot__id__in=scenic_ids)

    # 根据回复状态筛选
    if replied == 'replied':
        comments = comments.filter(is_replied=True)
    elif replied == 'unreplied':
        comments = comments.filter(is_replied=False)

    # 根据搜索条件筛选
    if search_query:
        comments = comments.filter(
            models.Q(user__username__icontains=search_query) |
            models.Q(content__icontains=search_query)
        )

    # 按创建时间倒序排序
    comments = comments.order_by('-created_at')

    # 分页处理，每页显示10条留言
    paginator = Paginator(comments, 10)
    try:
        # 获取当前页的留言列表
        comments_paginated = paginator.page(page)
    except PageNotAnInteger:
        # 如果页码不是整数，返回第一页
        comments_paginated = paginator.page(1)
    except EmptyPage:
        # 如果页码超出范围，返回最后一页
        comments_paginated = paginator.page(paginator.num_pages)

    # 构建上下文数据
    context = {
        'comments': comments_paginated,
        'current_replied': replied,
        'search_query': search_query,
        'paginator': paginator,
        'page_obj': comments_paginated
    }

    return render(request, 'scenic_admin/comments.html', context)


# 回复留言视图
@scenic_admin_required
def scenic_admin_reply_comment(request, comment_id):
    if request.method == 'POST':
        # 获取回复内容
        reply_content = request.POST.get('reply_content')
        
        if not reply_content:
            messages.error(request, '请输入回复内容')
            return redirect(reverse('ticket:scenic_admin_comments'))
        
        try:
            # 获取当前景点管理员
            admin = request.user
            
            # 获取要回复的留言
            comment = ScenicSpotComment.objects.get(id=comment_id, scenic_spot__admin=admin)
            
            # 更新留言的回复信息
            comment.reply = reply_content
            comment.is_replied = True
            comment.reply_time = timezone.now()
            comment.save()
            
            messages.success(request, '回复留言成功')
        except ScenicSpotComment.DoesNotExist:
            messages.error(request, '留言不存在或无权限访问')
        except Exception as e:
            messages.error(request, f'回复留言失败: {str(e)}')
    
    return redirect(reverse('ticket:scenic_admin_comments'))


# 删除留言视图
@scenic_admin_required
def scenic_admin_delete_comment(request, comment_id):
    try:
        # 获取当前景点管理员
        admin = request.user
        
        # 获取要删除的留言
        comment = ScenicSpotComment.objects.get(id=comment_id, scenic_spot__admin=admin)
        comment.delete()
        messages.success(request, '删除留言成功')
    except ScenicSpotComment.DoesNotExist:
        messages.error(request, '留言不存在或无权限访问')
    except Exception as e:
        messages.error(request, f'删除留言失败: {str(e)}')
    
    return redirect(reverse('ticket:scenic_admin_comments'))


# 数据统计视图
@scenic_admin_required
def scenic_admin_statistics(request):
    # 导入日期处理模块
    from datetime import date, timedelta
    import json

    # 获取当前景点管理员
    admin = request.user

    # 从数据库获取该管理员管理的景点
    scenic_spots = ScenicSpot.objects.filter(admin=admin)
    # 获取景点ID列表，用于后续查询
    scenic_ids = scenic_spots.values_list('id', flat=True)

    # 总订单数：查询该景点的所有订单
    total_orders = Order.objects.filter(scenic_spot__id__in=scenic_ids).count()

    # 总销售额：计算该景点所有已支付订单的总价之和
    total_sales = Order.objects.filter(scenic_spot__id__in=scenic_ids, status=1).aggregate(
        total=models.Sum('total_price')
    )['total'] or 0

    # 平均订单金额：总销售额 / 已支付订单数
    paid_orders_count = Order.objects.filter(scenic_spot__id__in=scenic_ids, status=1).count()
    avg_order_amount = total_sales / paid_orders_count if paid_orders_count > 0 else 0

    # 总访问量：查询该景点的所有浏览历史记录数
    total_visits = BrowseHistory.objects.filter(scenic_spot__id__in=scenic_ids).count()

    # 近7天订单趋势和销售额趋势
    # 生成近7天的日期列表
    today = date.today()
    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    # 格式化日期为字符串，用于图表标签
    date_labels = [d.strftime('%Y-%m-%d') for d in last_7_days]
    # 初始化订单数和销售额列表
    order_counts = []
    sales_amounts = []

    # 计算每天的订单数和销售额
    for d in last_7_days:
        # 当天订单数
        day_orders = Order.objects.filter(
            scenic_spot__id__in=scenic_ids,
            created_at__date=d
        ).count()
        order_counts.append(day_orders)
        
        # 当天销售额
        day_sales = Order.objects.filter(
            scenic_spot__id__in=scenic_ids,
            created_at__date=d,
            status=1
        ).aggregate(
            total=models.Sum('total_price')
        )['total'] or 0
        sales_amounts.append(float(day_sales))

    # 构建上下文数据
    context = {
        'total_orders': total_orders,
        'total_sales': total_sales,
        'avg_order_amount': avg_order_amount,
        'total_visits': total_visits,
        'date_labels': json.dumps(date_labels),
        'order_counts': json.dumps(order_counts),
        'sales_amounts': json.dumps(sales_amounts)
    }

    return render(request, 'scenic_admin/statistics.html', context)


# 账户信息管理视图
@scenic_admin_required
def scenic_admin_account(request):
    return render(request, 'scenic_admin/account.html')


# 资讯公告管理视图
@scenic_admin_required
def scenic_admin_news_announcements(request):
    return render(request, 'scenic_admin/news_announcements.html')


# 公告管理视图
@scenic_admin_required
def scenic_admin_announcements(request):
    # 获取当前页码，默认为1
    page = request.GET.get('page', 1)
    
    # 获取公告列表（is_announcement=True）
    announcements = News.objects.filter(is_announcement=True).order_by('-created_at')
    
    # 分页处理，每页显示10条公告
    paginator = Paginator(announcements, 10)
    try:
        # 获取当前页的公告列表
        announcements_paginated = paginator.page(page)
    except PageNotAnInteger:
        # 如果页码不是整数，返回第一页
        announcements_paginated = paginator.page(1)
    except EmptyPage:
        # 如果页码超出范围，返回最后一页
        announcements_paginated = paginator.page(paginator.num_pages)
    
    # 构建上下文数据
    context = {
        'announcements': announcements_paginated,
        'paginator': paginator,
        'page_obj': announcements_paginated
    }
    
    return render(request, 'scenic_admin/announcements.html', context)


# 新增公告视图
@scenic_admin_required
def scenic_admin_add_announcement(request):
    if request.method == 'POST':
        # 获取表单数据
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        
        # 创建公告
        try:
            announcement = News(
                title=title,
                content=content,
                image=image,
                is_announcement=True
            )
            announcement.save()
            
            messages.success(request, '新增公告成功')
            return redirect(reverse('ticket:scenic_admin_announcements'))
        except Exception as e:
            messages.error(request, f'新增公告失败: {str(e)}')
    
    # GET请求，渲染新增公告表单
    return render(request, 'scenic_admin/add_announcement.html')


# 编辑公告视图
@scenic_admin_required
def scenic_admin_edit_announcement(request, announcement_id):
    # 获取要编辑的公告
    try:
        announcement = News.objects.get(id=announcement_id, is_announcement=True)
    except News.DoesNotExist:
        messages.error(request, '公告不存在或无权限访问')
        return redirect(reverse('ticket:scenic_admin_announcements'))
    
    if request.method == 'POST':
        # 获取表单数据
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        
        # 更新公告
        try:
            announcement.title = title
            announcement.content = content
            if image:
                announcement.image = image
            announcement.save()
            
            messages.success(request, '编辑公告成功')
            return redirect(reverse('ticket:scenic_admin_announcements'))
        except Exception as e:
            messages.error(request, f'编辑公告失败: {str(e)}')
    
    # GET请求，渲染编辑公告表单
    context = {
        'announcement': announcement
    }
    return render(request, 'scenic_admin/edit_announcement.html', context)


# 删除公告视图
@scenic_admin_required
def scenic_admin_delete_announcement(request, announcement_id):
    # 获取要删除的公告
    try:
        announcement = News.objects.get(id=announcement_id, is_announcement=True)
        announcement.delete()
        messages.success(request, '删除公告成功')
    except News.DoesNotExist:
        messages.error(request, '公告不存在或无权限访问')
    except Exception as e:
        messages.error(request, f'删除公告失败: {str(e)}')
    
    return redirect(reverse('ticket:scenic_admin_announcements'))


# 批量删除公告视图
@scenic_admin_required
def scenic_admin_batch_delete_announcements(request):
    if request.method == 'POST':
        # 获取选中的公告ID
        announcement_ids = request.POST.getlist('announcement_ids')
        
        if not announcement_ids:
            messages.error(request, '请选择要删除的公告')
            return redirect(reverse('ticket:scenic_admin_announcements'))
        
        try:
            # 删除选中的公告
            News.objects.filter(id__in=announcement_ids, is_announcement=True).delete()
            messages.success(request, f'成功删除 {len(announcement_ids)} 条公告')
        except Exception as e:
            messages.error(request, f'批量删除失败: {str(e)}')
    
    return redirect(reverse('ticket:scenic_admin_announcements'))


# 资讯管理视图
@scenic_admin_required
def scenic_admin_news(request):
    # 获取当前页码，默认为1
    page = request.GET.get('page', 1)
    
    # 获取资讯列表（is_announcement=False）
    news = News.objects.filter(is_announcement=False).order_by('-created_at')
    
    # 分页处理，每页显示10条资讯
    paginator = Paginator(news, 10)
    try:
        # 获取当前页的资讯列表
        news_paginated = paginator.page(page)
    except PageNotAnInteger:
        # 如果页码不是整数，返回第一页
        news_paginated = paginator.page(1)
    except EmptyPage:
        # 如果页码超出范围，返回最后一页
        news_paginated = paginator.page(paginator.num_pages)
    
    # 构建上下文数据
    context = {
        'news': news_paginated,
        'paginator': paginator,
        'page_obj': news_paginated
    }
    
    return render(request, 'scenic_admin/news.html', context)


# 新增资讯视图
@scenic_admin_required
def scenic_admin_add_news(request):
    if request.method == 'POST':
        # 获取表单数据
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        
        # 创建资讯
        try:
            news_item = News(
                title=title,
                content=content,
                image=image,
                is_announcement=False
            )
            news_item.save()
            
            messages.success(request, '新增资讯成功')
            return redirect(reverse('ticket:scenic_admin_news'))
        except Exception as e:
            messages.error(request, f'新增资讯失败: {str(e)}')
    
    # GET请求，渲染新增资讯表单
    return render(request, 'scenic_admin/add_news.html')


# 编辑资讯视图
@scenic_admin_required
def scenic_admin_edit_news(request, news_id):
    # 获取要编辑的资讯
    try:
        news_item = News.objects.get(id=news_id, is_announcement=False)
    except News.DoesNotExist:
        messages.error(request, '资讯不存在或无权限访问')
        return redirect(reverse('ticket:scenic_admin_news'))
    
    if request.method == 'POST':
        # 获取表单数据
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        
        # 更新资讯
        try:
            news_item.title = title
            news_item.content = content
            if image:
                news_item.image = image
            news_item.save()
            
            messages.success(request, '编辑资讯成功')
            return redirect(reverse('ticket:scenic_admin_news'))
        except Exception as e:
            messages.error(request, f'编辑资讯失败: {str(e)}')
    
    # GET请求，渲染编辑资讯表单
    context = {
        'news_item': news_item
    }
    return render(request, 'scenic_admin/edit_news.html', context)


# 删除资讯视图
@scenic_admin_required
def scenic_admin_delete_news(request, news_id):
    # 获取要删除的资讯
    try:
        news_item = News.objects.get(id=news_id, is_announcement=False)
        news_item.delete()
        messages.success(request, '删除资讯成功')
    except News.DoesNotExist:
        messages.error(request, '资讯不存在或无权限访问')
    except Exception as e:
        messages.error(request, f'删除资讯失败: {str(e)}')
    
    return redirect(reverse('ticket:scenic_admin_news'))


# 批量删除资讯视图
@scenic_admin_required
def scenic_admin_batch_delete_news(request):
    if request.method == 'POST':
        # 获取选中的资讯ID
        news_ids = request.POST.getlist('news_ids')
        
        if not news_ids:
            messages.error(request, '请选择要删除的资讯')
            return redirect(reverse('ticket:scenic_admin_news'))
        
        try:
            # 删除选中的资讯
            News.objects.filter(id__in=news_ids, is_announcement=False).delete()
            messages.success(request, f'成功删除 {len(news_ids)} 条资讯')
        except Exception as e:
            messages.error(request, f'批量删除失败: {str(e)}')
    
    return redirect(reverse('ticket:scenic_admin_news'))


# 平台管理员后台视图函数，需要登录且角色为平台管理员才能访问
def admin_required(view_func):
    @login_required
    def wrapped_view(request, *args, **kwargs):
        if request.user.role == 2:  # 2表示平台管理员
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, '您没有权限访问该页面')
            return redirect(reverse('ticket:index'))

    return wrapped_view


# 平台管理员控制台视图
@admin_required
def admin_index(request):
    # 导入日期处理模块
    from datetime import date

    # 从数据库获取统计数据
    total_users = User.objects.count()  # 总用户数
    total_scenic_spots = ScenicSpot.objects.count()  # 总景点数

    # 今日订单数：查询今天创建的订单
    today = date.today()
    today_orders = Order.objects.filter(created_at__date=today).count()  # 今日订单

    # 总销售额：计算所有已支付订单的总价之和
    total_sales = Order.objects.filter(status=1).aggregate(
        total=models.Sum('total_price')
    )['total'] or 0  # 总销售额

    # 最近订单：获取最新的2个订单
    recent_orders = Order.objects.order_by('-created_at')[:2]

    # 待处理留言：获取未回复的留言
    pending_comments = ScenicSpotComment.objects.filter(is_replied=False).order_by('-created_at')[:2]

    # 构建上下文数据
    context = {
        'total_users': total_users,
        'total_scenic_spots': total_scenic_spots,
        'today_orders': today_orders,
        'total_sales': total_sales,
        'recent_orders': recent_orders,
        'pending_comments': pending_comments
    }

    return render(request, 'admin/index.html', context)


# 用户管理视图
@admin_required
def admin_user_list(request):
    # 获取请求参数中的角色筛选条件
    role_filter = request.GET.get('role', '')
    # 获取当前页码，默认为1
    page = request.GET.get('page', 1)

    # 基础查询集
    users = User.objects.all()

    # 根据角色筛选用户
    if role_filter:
        users = users.filter(role=role_filter)

    # 统计不同角色的用户数量
    total_users = User.objects.count()
    visitor_count = User.objects.filter(role=0).count()
    scenic_admin_count = User.objects.filter(role=1).count()
    platform_admin_count = User.objects.filter(role=2).count()

    # 分页处理
    paginator = Paginator(users, 10)  # 每页显示10个用户
    try:
        users_paginated = paginator.page(page)
    except PageNotAnInteger:
        users_paginated = paginator.page(1)
    except EmptyPage:
        users_paginated = paginator.page(paginator.num_pages)

    # 构建上下文数据
    context = {
        'users': users_paginated,
        'total_users': total_users,
        'visitor_count': visitor_count,
        'scenic_admin_count': scenic_admin_count,
        'platform_admin_count': platform_admin_count,
        'role_filter': role_filter
    }

    return render(request, 'admin/user_list.html', context)


# 新增用户视图
@admin_required
def admin_add_user(request):
    # 获取系统中的所有景点
    scenic_spots = ScenicSpot.objects.all()
    
    if request.method == 'POST':
        # 从POST请求中获取表单数据
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role')  # 获取角色值
        scenic_spot_id = request.POST.get('scenic_spot')

        # 确保role有值，默认为'0'
        if not role:
            role = '0'
        
        try:
            # 调试信息
            print(f"=== 表单提交调试信息 ===")
            print(f"用户名: {username}")
            print(f"邮箱: {email}")
            print(f"角色: {role}")
            print(f"景点ID: {scenic_spot_id}")
            print(f"密码: {password}")
            print(f"确认密码: {confirm_password}")
            
            # 表单验证
            if not username or not email or not password:
                print("错误: 用户名、邮箱和密码不能为空")
                messages.error(request, '用户名、邮箱和密码不能为空')
                return render(request, 'admin/add_user.html', {'scenic_spots': scenic_spots})

            if password != confirm_password:
                messages.error(request, '两次输入的密码不一致')
                return render(request, 'admin/add_user.html', {'scenic_spots': scenic_spots})

            # 检查用户名是否已存在
            if User.objects.filter(username=username).exists():
                messages.error(request, '用户名已存在')
                return render(request, 'admin/add_user.html', {'scenic_spots': scenic_spots})

            # 检查邮箱是否已存在
            if User.objects.filter(email=email).exists():
                messages.error(request, '邮箱已被注册')
                return render(request, 'admin/add_user.html', {'scenic_spots': scenic_spots})
            
            print(f"最终角色值: {role}")
            
            # 计算下一个连续的用户ID
            # 先获取所有已存在的用户ID
            existing_ids = User.objects.values_list('id', flat=True).order_by('id')
            # 如果没有现有用户，直接使用ID=1
            if not existing_ids:
                next_id = 1
            else:
                # 查找最小的空缺ID
                next_id = 1
                for id in existing_ids:
                    if id == next_id:
                        next_id += 1
                    else:
                        break
            
            # 创建新用户，使用create_user方法会自动加密密码，并指定连续的ID
            user = User.objects.create_user(
                id=next_id,
                username=username,
                email=email,
                password=password
            )
            
            print(f"用户创建成功: {user.username}")
            
            # 设置用户角色
            user.role = int(role)
            
            # 如果是景点管理员，关联景点
            if int(role) == 1 and scenic_spot_id:
                # 获取关联的景点
                try:
                    scenic_spot = ScenicSpot.objects.get(id=scenic_spot_id)
                    user.managed_scenic_spots.add(scenic_spot)
                    print(f"关联景点成功: {scenic_spot.name}")
                except ScenicSpot.DoesNotExist:
                    print(f"景点不存在: {scenic_spot_id}")
            
            user.save()
            print(f"用户角色设置成功: {user.role}")
            
            print(f"用户角色设置成功: {user.role}")

            # 显示成功消息
            messages.success(request, '用户添加成功')
            print("准备重定向到用户列表页面")

            # 重定向到用户列表页面
            return redirect(reverse('ticket:admin_user_list'))
        except Exception as e:
            # 显示错误消息
            messages.error(request, f'添加用户失败: {str(e)}')
            return render(request, 'admin/add_user.html', {'scenic_spots': scenic_spots})
    
    # GET请求时，渲染表单页面
    return render(request, 'admin/add_user.html', {'scenic_spots': scenic_spots})


# 删除用户视图
@admin_required
def admin_delete_user(request, user_id):
    if request.method == 'POST':
        try:
            # 根据user_id从数据库获取用户
            user = User.objects.get(id=user_id)

            # 删除用户
            user.delete()

            # 显示成功消息
            messages.success(request, '用户删除成功')
        except User.DoesNotExist:
            # 用户不存在
            messages.error(request, '用户不存在')
        except Exception as e:
            # 删除失败
            messages.error(request, f'删除用户失败: {str(e)}')

    # 无论成功还是失败，都重定向到用户列表页面
    return redirect(reverse('ticket:admin_user_list'))


# 批量删除用户视图
@admin_required
def admin_batch_delete_users(request):
    if request.method == 'POST':
        # 获取选中的用户ID列表
        user_ids = request.POST.getlist('user_ids')
        role_filter = request.POST.get('role_filter', '')
        
        if user_ids:
            try:
                # 删除选中的用户
                deleted_count, _ = User.objects.filter(id__in=user_ids).delete()
                # 显示成功消息
                messages.success(request, f'成功删除 {deleted_count} 个用户')
            except Exception as e:
                # 删除失败
                messages.error(request, f'批量删除用户失败: {str(e)}')
        else:
            # 没有选中用户
            messages.warning(request, '请至少选择一个用户进行删除')
    
    # 构建重定向URL，保持筛选条件
    redirect_url = reverse('ticket:admin_user_list')
    if role_filter:
        redirect_url += f'?role={role_filter}'
    
    # 重定向到用户列表页面
    return redirect(redirect_url)


# 编辑用户视图
@admin_required
def admin_edit_user(request, user_id):
    try:
        # 根据user_id从数据库获取用户信息
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        # 用户不存在，显示错误消息并重定向
        messages.error(request, '用户不存在')
        return redirect(reverse('ticket:admin_user_list'))

    if request.method == 'POST':
        # 从POST请求中获取表单数据
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        birthdate_str = request.POST.get('birthdate')
        role = request.POST.get('role')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # 表单验证
        if not username or not email:
            messages.error(request, '用户名和邮箱不能为空')
            return render(request, 'admin/edit_user.html', {'user': user})

        # 检查用户名是否已被其他用户使用
        if User.objects.filter(username=username).exclude(id=user_id).exists():
            messages.error(request, '用户名已存在')
            return render(request, 'admin/edit_user.html', {'user': user})

        # 检查邮箱是否已被其他用户使用
        if User.objects.filter(email=email).exclude(id=user_id).exists():
            messages.error(request, '邮箱已被注册')
            return render(request, 'admin/edit_user.html', {'user': user})

        # 处理密码修改
        if password:
            if password != confirm_password:
                messages.error(request, '两次输入的密码不一致')
                return render(request, 'admin/edit_user.html', {'user': user})
            user.set_password(password)  # 使用set_password方法加密密码

        # 更新用户信息
        user.username = username
        user.email = email
        user.phone = phone
        user.gender = gender
        user.role = int(role)

        # 处理出生日期
        if birthdate_str:
            from datetime import datetime
            user.birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d').date()
        else:
            user.birthdate = None

        # 处理头像上传
        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']

        try:
            # 保存更新后的用户信息到数据库
            user.save()

            # 显示成功消息
            messages.success(request, '用户信息更新成功')

            # 重定向到用户列表页面
            return redirect(reverse('ticket:admin_user_list'))
        except Exception as e:
            # 显示错误消息
            messages.error(request, f'更新用户失败: {str(e)}')
            return render(request, 'admin/edit_user.html', {'user': user})

    # GET请求，渲染编辑用户表单，传递当前用户数据
    return render(request, 'admin/edit_user.html', {'user': user})


# 景点分类管理视图
@admin_required
def admin_category_list(request):
    # 获取请求参数中的搜索关键词
    search_keyword = request.GET.get('search', '')
    # 获取当前页码，默认为1
    page = request.GET.get('page', 1)

    # 基础查询集
    categories = Category.objects.all()

    # 根据搜索关键词筛选分类
    if search_keyword:
        categories = categories.filter(
            models.Q(name__icontains=search_keyword) |
            models.Q(description__icontains=search_keyword)
        )

    # 分页处理，每页显示10个分类
    paginator = Paginator(categories, 10)
    try:
        # 获取当前页的分类列表
        categories_paginated = paginator.page(page)
    except PageNotAnInteger:
        # 如果页码不是整数，返回第一页
        categories_paginated = paginator.page(1)
    except EmptyPage:
        # 如果页码超出范围，返回最后一页
        categories_paginated = paginator.page(paginator.num_pages)

    # 构建上下文数据
    context = {
        'categories': categories_paginated,
        'search_keyword': search_keyword,
        'paginator': paginator,
        'page_obj': categories_paginated
    }

    return render(request, 'admin/category_list.html', context)


# 添加景点分类视图
@admin_required
def admin_add_category(request):
    if request.method == 'POST':
        # 获取表单数据
        name = request.POST.get('name')
        description = request.POST.get('description')

        # 表单验证
        if not name:
            messages.error(request, '分类名称不能为空')
            return render(request, 'admin/add_category.html')

        try:
            # 创建分类
            Category.objects.create(
                name=name,
                description=description
            )
            messages.success(request, '景点分类添加成功')
            return redirect(reverse('ticket:admin_category_list'))
        except Exception as e:
            messages.error(request, f'添加分类失败: {str(e)}')

    return render(request, 'admin/add_category.html')


# 编辑景点分类视图
@admin_required
def admin_edit_category(request, category_id):
    try:
        # 获取要编辑的分类
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        messages.error(request, '分类不存在')
        return redirect(reverse('ticket:admin_category_list'))

    if request.method == 'POST':
        # 获取表单数据
        name = request.POST.get('name')
        description = request.POST.get('description')

        # 表单验证
        if not name:
            messages.error(request, '分类名称不能为空')
            return render(request, 'admin/edit_category.html', {'category': category})

        try:
            # 更新分类
            category.name = name
            category.description = description
            category.save()
            messages.success(request, '景点分类更新成功')
            return redirect(reverse('ticket:admin_category_list'))
        except Exception as e:
            messages.error(request, f'更新分类失败: {str(e)}')

    # GET请求，渲染编辑表单
    return render(request, 'admin/edit_category.html', {'category': category})


# 删除景点分类视图
@admin_required
def admin_delete_category(request, category_id):
    if request.method == 'POST':
        try:
            # 获取要删除的分类
            category = Category.objects.get(id=category_id)
            category.delete()
            messages.success(request, '景点分类删除成功')
        except Category.DoesNotExist:
            messages.error(request, '分类不存在')
        except Exception as e:
            messages.error(request, f'删除分类失败: {str(e)}')

    return redirect(reverse('ticket:admin_category_list'))


# 景点管理视图
@admin_required
def admin_scenic_list(request):
    # 获取请求参数中的搜索关键词
    search_keyword = request.GET.get('search', '')
    # 获取当前页码，默认为1
    page = request.GET.get('page', 1)

    # 基础查询集
    scenic_spots = ScenicSpot.objects.all()

    # 根据搜索关键词筛选景点
    if search_keyword:
        scenic_spots = scenic_spots.filter(
            models.Q(name__icontains=search_keyword) |
            models.Q(address__icontains=search_keyword) |
            models.Q(region__name__icontains=search_keyword)
        )

    # 统计不同状态的景点数量
    total_scenic_spots = ScenicSpot.objects.count()
    hot_spots = ScenicSpot.objects.filter(is_hot=True).count()
    recommended_spots = ScenicSpot.objects.filter(is_hot=True).count()  # 可以根据实际字段调整

    # 获取所有地区（用于筛选）
    regions = Region.objects.all()

    # 景点分类选项：从Category模型获取所有分类
    categories = Category.objects.all()

    # 分页处理
    paginator = Paginator(scenic_spots, 10)  # 每页显示10个景点
    try:
        scenic_spots_paginated = paginator.page(page)
    except PageNotAnInteger:
        scenic_spots_paginated = paginator.page(1)
    except EmptyPage:
        scenic_spots_paginated = paginator.page(paginator.num_pages)

    # 构建上下文数据
    context = {
        'scenic_spots': scenic_spots_paginated,
        'total_scenic_spots': total_scenic_spots,
        'hot_spots': hot_spots,
        'recommended_spots': recommended_spots,
        'regions': regions,
        'categories': categories,
        'search_keyword': search_keyword
    }

    return render(request, 'admin/scenic_list.html', context)


# 地区分类管理视图
@admin_required
def admin_region_list(request):
    # 获取请求参数中的搜索关键词
    search_keyword = request.GET.get('search', '')
    # 获取当前页码，默认为1
    page = request.GET.get('page', 1)

    # 基础查询集
    regions = Region.objects.all()

    # 根据搜索关键词筛选地区
    if search_keyword:
        regions = regions.filter(name__icontains=search_keyword)

    # 分页处理，每页显示10个地区
    paginator = Paginator(regions, 10)
    try:
        # 获取当前页的地区列表
        regions_paginated = paginator.page(page)
    except PageNotAnInteger:
        # 如果页码不是整数，返回第一页
        regions_paginated = paginator.page(1)
    except EmptyPage:
        # 如果页码超出范围，返回最后一页
        regions_paginated = paginator.page(paginator.num_pages)

    # 构建上下文数据
    context = {
        'regions': regions_paginated,
        'search_keyword': search_keyword,
        'paginator': paginator,
        'page_obj': regions_paginated
    }

    return render(request, 'admin/region_list.html', context)


# 添加地区分类视图
@admin_required
def admin_add_region(request):
    if request.method == 'POST':
        # 获取表单数据
        name = request.POST.get('name')

        # 表单验证
        if not name:
            messages.error(request, '地区名称不能为空')
            return render(request, 'admin/add_region.html')

        try:
            # 创建地区
            Region.objects.create(
                name=name
            )
            messages.success(request, '地区添加成功')
            return redirect(reverse('ticket:admin_region_list'))
        except Exception as e:
            messages.error(request, f'添加地区失败: {str(e)}')
            return render(request, 'admin/add_region.html')

    # GET请求，渲染添加表单
    return render(request, 'admin/add_region.html')


# 编辑地区分类视图
@admin_required
def admin_edit_region(request, region_id):
    try:
        # 获取要编辑的地区
        region = Region.objects.get(id=region_id)
    except Region.DoesNotExist:
        messages.error(request, '地区不存在')
        return redirect(reverse('ticket:admin_region_list'))

    if request.method == 'POST':
        # 获取表单数据
        name = request.POST.get('name')

        # 表单验证
        if not name:
            messages.error(request, '地区名称不能为空')
            return render(request, 'admin/edit_region.html', {'region': region})

        try:
            # 更新地区信息
            region.name = name
            region.save()
            messages.success(request, '地区更新成功')
            return redirect(reverse('ticket:admin_region_list'))
        except Exception as e:
            messages.error(request, f'更新地区失败: {str(e)}')
            return render(request, 'admin/edit_region.html', {'region': region})

    # GET请求，渲染编辑表单
    return render(request, 'admin/edit_region.html', {'region': region})


# 删除地区分类视图
@admin_required
def admin_delete_region(request, region_id):
    if request.method == 'POST':
        try:
            # 获取要删除的地区
            region = Region.objects.get(id=region_id)
            region.delete()
            messages.success(request, '地区删除成功')
        except Region.DoesNotExist:
            messages.error(request, '地区不存在')
        except Exception as e:
            messages.error(request, f'删除地区失败: {str(e)}')

    return redirect(reverse('ticket:admin_region_list'))


# 重新排序景点显示ID的辅助函数
def reorder_scenic_display_ids():
    # 按id升序获取所有景点
    scenic_spots = ScenicSpot.objects.all().order_by('id')
    
    # 重新分配display_id
    for index, spot in enumerate(scenic_spots, start=1):
        if spot.display_id != index:
            spot.display_id = index
            spot.save()


# 删除景点视图
@admin_required
def admin_delete_scenic(request, spot_id):
    if request.method == 'POST':
        try:
            # 根据spot_id从数据库获取景点
            scenic_spot = ScenicSpot.objects.get(id=spot_id)
            
            # 删除景点
            scenic_spot.delete()
            
            # 重新排序display_id
            reorder_scenic_display_ids()
            
            # 显示成功消息
            messages.success(request, '景点删除成功')
        except ScenicSpot.DoesNotExist:
            # 景点不存在
            messages.error(request, '景点不存在或已被删除')
        except Exception as e:
            # 删除失败
            messages.error(request, f'删除景点失败: {str(e)}')
    
    # 获取搜索关键词，保持搜索状态
    search_keyword = request.POST.get('search', '')
    redirect_url = reverse('ticket:admin_scenic_list')
    if search_keyword:
        redirect_url += f'?search={search_keyword}'
    
    # 重定向到景点列表页面
    return redirect(redirect_url)


# 批量删除景点视图
@admin_required
def admin_batch_delete_scenic(request):
    if request.method == 'POST':
        # 获取选中的景点ID列表
        scenic_ids = request.POST.getlist('scenic_ids')
        search_keyword = request.POST.get('search', '')
        
        if scenic_ids:
            try:
                # 删除选中的景点
                deleted_count, _ = ScenicSpot.objects.filter(id__in=scenic_ids).delete()
                
                # 重新排序display_id
                reorder_scenic_display_ids()
                
                # 显示成功消息
                messages.success(request, f'成功删除 {deleted_count} 个景点')
            except Exception as e:
                # 删除失败
                messages.error(request, f'批量删除景点失败: {str(e)}')
        else:
            # 没有选中景点
            messages.warning(request, '请至少选择一个景点进行删除')
    
    # 构建重定向URL，保持搜索条件
    redirect_url = reverse('ticket:admin_scenic_list')
    if search_keyword:
        redirect_url += f'?search={search_keyword}'
    
    # 重定向到景点列表页面
    return redirect(redirect_url)


# 新增景点视图
@admin_required
def admin_add_scenic(request):
    if request.method == 'POST':
        # 从POST请求中获取表单数据
        name = request.POST.get('name')
        region = request.POST.get('region')
        category = request.POST.get('category')
        price = request.POST.get('price')
        total_tickets = request.POST.get('total_tickets')
        opening_hours = request.POST.get('opening_hours')
        tags = request.POST.get('tags')
        is_hot = request.POST.get('is_hot') == 'on'
        address = request.POST.get('address')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        # 表单验证
        if not name or not region or not category or not price or not opening_hours or not address or not description or not image:
            messages.error(request, '请填写所有必填字段')
            # 获取所有分类选项
            categories = Category.objects.all()
            # 获取所有地区选项
            regions = Region.objects.all()
            return render(request, 'admin/add_scenic.html', {'categories': categories, 'regions': regions})

        try:
            # 创建新景点
            scenic_spot = ScenicSpot.objects.create(
                name=name,
                region_id=region,
                category=category,
                price=float(price),
                total_tickets=int(total_tickets) if total_tickets else 0,
                opening_hours=opening_hours,
                tags=tags,
                is_hot=is_hot,
                address=address,
                description=description,
                image=image
            )

            # 重新排序display_id
            reorder_scenic_display_ids()

            # 显示成功消息
            messages.success(request, '景点添加成功')

            # 重定向到景点列表页面
            return redirect(reverse('ticket:admin_scenic_list'))
        except Exception as e:
            # 显示错误消息
            messages.error(request, f'添加景点失败: {str(e)}')
            # 获取所有分类选项
            categories = Category.objects.all()
            # 获取所有地区选项
            regions = Region.objects.all()
            return render(request, 'admin/add_scenic.html', {'categories': categories, 'regions': regions})

    # GET请求，渲染新增景点表单
    # 获取所有分类选项
    categories = Category.objects.all()
    # 获取所有地区选项
    regions = Region.objects.all()
    return render(request, 'admin/add_scenic.html', {'categories': categories, 'regions': regions})


# 编辑景点视图
@admin_required
def admin_edit_scenic(request, spot_id):
    try:
        # 根据spot_id从数据库获取景点信息
        scenic_spot = ScenicSpot.objects.get(id=spot_id)
    except ScenicSpot.DoesNotExist:
        # 景点不存在，显示错误消息并重定向
        messages.error(request, '景点不存在')
        return redirect(reverse('ticket:admin_scenic_list'))

    if request.method == 'POST':
        # 从POST请求中获取表单数据
        name = request.POST.get('name')
        region = request.POST.get('region')
        category = request.POST.get('category')
        price = request.POST.get('price')
        total_tickets = request.POST.get('total_tickets')
        opening_hours = request.POST.get('opening_hours')
        tags = request.POST.get('tags')
        is_hot = request.POST.get('is_hot') == 'on'
        address = request.POST.get('address')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        # 表单验证
        if not name or not region or not category or not price or not opening_hours or not address or not description:
            messages.error(request, '请填写所有必填字段')
            # 获取所有分类选项
            categories = Category.objects.all()
            # 获取所有地区选项
            regions = Region.objects.all()
            return render(request, 'admin/edit_scenic.html', {'scenic_spot': scenic_spot, 'categories': categories, 'regions': regions})

        try:
            # 更新景点信息
            scenic_spot.name = name
            scenic_spot.region_id = region
            scenic_spot.category = category
            scenic_spot.price = float(price)
            scenic_spot.total_tickets = int(total_tickets) if total_tickets else 0
            scenic_spot.opening_hours = opening_hours
            scenic_spot.tags = tags
            scenic_spot.is_hot = is_hot
            scenic_spot.address = address
            scenic_spot.description = description

            # 处理图片上传
            if image:
                scenic_spot.image = image

            # 保存更新后的景点信息到数据库
            scenic_spot.save()

            # 显示成功消息
            messages.success(request, '景点信息更新成功')

            # 重定向到景点列表页面
            return redirect(reverse('ticket:admin_scenic_list'))
        except Exception as e:
            # 显示错误消息
            messages.error(request, f'更新景点失败: {str(e)}')
            # 获取所有分类选项
            categories = Category.objects.all()
            # 获取所有地区选项
            regions = Region.objects.all()
            return render(request, 'admin/edit_scenic.html', {'scenic_spot': scenic_spot, 'categories': categories, 'regions': regions})

    # GET请求，渲染编辑景点表单，传递当前景点数据
    # 获取所有分类选项
    categories = Category.objects.all()
    # 获取所有地区选项
    regions = Region.objects.all()
    return render(request, 'admin/edit_scenic.html', {'scenic_spot': scenic_spot, 'categories': categories, 'regions': regions})





# 订单管理视图
@admin_required
def admin_order_list(request):
    # 获取请求参数中的订单状态筛选条件
    status_filter = request.GET.get('status', '')
    # 获取请求参数中的搜索关键词
    search_keyword = request.GET.get('search', '')
    # 获取当前页码，默认为1
    page = request.GET.get('page', 1)

    # 基础查询集：包含关联的用户和景点信息，使用select_related优化查询
    orders = Order.objects.select_related('user', 'scenic_spot', 'ticket_type')

    # 根据订单状态筛选
    if status_filter:
        orders = orders.filter(status=status_filter)

    # 根据搜索关键词筛选：可搜索订单号、用户名、用户邮箱或景点名称
    if search_keyword:
        orders = orders.filter(
            models.Q(order_number__icontains=search_keyword) |
            models.Q(user__username__icontains=search_keyword) |
            models.Q(user__email__icontains=search_keyword) |
            models.Q(scenic_spot__name__icontains=search_keyword)
        )

    # 按创建时间倒序排序
    orders = orders.order_by('-created_at')

    # 统计不同状态的订单数量
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status=0).count()
    paid_orders = Order.objects.filter(status=1).count()
    canceled_orders = Order.objects.filter(status=2).count()
    used_orders = Order.objects.filter(status=3).count()
    refunded_orders = Order.objects.filter(status=4).count()

    # 订单状态选项
    status_choices = Order.STATUS_CHOICES

    # 分页处理
    paginator = Paginator(orders, 10)  # 每页显示10个订单
    try:
        orders_paginated = paginator.page(page)
    except PageNotAnInteger:
        orders_paginated = paginator.page(1)
    except EmptyPage:
        orders_paginated = paginator.page(paginator.num_pages)

    # 构建上下文数据
    context = {
        'orders': orders_paginated,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'paid_orders': paid_orders,
        'canceled_orders': canceled_orders,
        'used_orders': used_orders,
        'refunded_orders': refunded_orders,
        'status_choices': status_choices,
        'status_filter': status_filter,
        'search_keyword': search_keyword
    }

    return render(request, 'admin/order_list.html', context)


# 删除订单视图
@admin_required
def admin_delete_order(request, order_id):
    if request.method == 'POST':
        try:
            # 根据order_id从数据库获取订单
            order = Order.objects.get(id=order_id)
            
            # 删除订单
            order.delete()
            
            # 显示成功消息
            messages.success(request, '订单删除成功')
        except Order.DoesNotExist:
            # 订单不存在
            messages.error(request, '订单不存在或已被删除')
        except Exception as e:
            # 删除失败
            messages.error(request, f'删除订单失败: {str(e)}')
    
    # 获取筛选条件，保持筛选状态
    status_filter = request.POST.get('status_filter', '')
    search_keyword = request.POST.get('search', '')
    
    # 构建重定向URL
    redirect_url = reverse('ticket:admin_order_list')
    query_params = []
    if status_filter:
        query_params.append(f'status={status_filter}')
    if search_keyword:
        query_params.append(f'search={search_keyword}')
    if query_params:
        redirect_url += f'?{"&".join(query_params)}'
    
    # 重定向到订单列表页面
    return redirect(redirect_url)


# 留言管理视图
@admin_required
def admin_comment_list(request):
    # 获取请求参数中的回复状态筛选条件
    replied_filter = request.GET.get('replied', '')
    # 获取请求参数中的搜索关键词
    search_keyword = request.GET.get('search', '')
    # 获取当前页码，默认为1
    page = request.GET.get('page', 1)

    # 基础查询集：包含关联的用户和景点信息，使用select_related优化查询
    comments = ScenicSpotComment.objects.select_related('user', 'scenic_spot').order_by('-created_at')

    # 根据回复状态筛选
    if replied_filter == 'replied':
        comments = comments.filter(is_replied=True)
    elif replied_filter == 'unreplied':
        comments = comments.filter(is_replied=False)

    # 根据搜索关键词筛选：可搜索用户名或留言内容
    if search_keyword:
        comments = comments.filter(
            models.Q(user__username__icontains=search_keyword) |
            models.Q(content__icontains=search_keyword)
        )

    # 统计不同回复状态的留言数量
    total_comments = ScenicSpotComment.objects.count()
    replied_comments = ScenicSpotComment.objects.filter(is_replied=True).count()
    unreplied_comments = ScenicSpotComment.objects.filter(is_replied=False).count()

    # 分页处理
    paginator = Paginator(comments, 10)  # 每页显示10条留言
    try:
        comments_paginated = paginator.page(page)
    except PageNotAnInteger:
        comments_paginated = paginator.page(1)
    except EmptyPage:
        comments_paginated = paginator.page(paginator.num_pages)

    # 构建上下文数据
    context = {
        'comments': comments_paginated,
        'total_comments': total_comments,
        'replied_comments': replied_comments,
        'unreplied_comments': unreplied_comments,
        'replied_filter': replied_filter,
        'search_keyword': search_keyword
    }

    return render(request, 'admin/comment_list.html', context)


# 管理员回复留言视图
@admin_required
def admin_reply_comment(request, comment_id):
    if request.method == 'POST':
        try:
            # 获取要回复的留言
            comment = ScenicSpotComment.objects.get(id=comment_id)
            # 获取回复内容
            reply_content = request.POST.get('reply_content')
            if reply_content and reply_content.strip():
                # 更新留言的回复信息
                comment.reply = reply_content.strip()
                comment.is_replied = True
                # reply_time字段会在save()时自动更新，不需要手动设置
                comment.save()
                # 显示成功消息
                messages.success(request, '回复成功！')
        except ScenicSpotComment.DoesNotExist:
            messages.error(request, '留言不存在或已被删除')
    # 重定向回留言管理页面
    return redirect(reverse('ticket:admin_comment_list'))


# 管理员删除留言视图
@admin_required
def admin_delete_comment(request, comment_id):
    if request.method == 'POST':
        try:
            # 获取要删除的留言
            comment = ScenicSpotComment.objects.get(id=comment_id)
            # 删除留言
            comment.delete()
            # 显示成功消息
            messages.success(request, '留言删除成功！')
        except ScenicSpotComment.DoesNotExist:
            messages.error(request, '留言不存在或已被删除')
    # 重定向回留言管理页面
    return redirect(reverse('ticket:admin_comment_list'))


# 公告管理视图
@admin_required
def admin_announcement_list(request):
    # 获取请求参数中的搜索关键词
    search_keyword = request.GET.get('search', '')
    # 获取当前页码，默认为1
    page = request.GET.get('page', 1)

    # 基础查询集：只获取公告类型的资讯，按创建时间倒序排列
    announcements = News.objects.filter(is_announcement=True).order_by('-created_at')

    # 根据搜索关键词筛选：可搜索公告标题或内容
    if search_keyword:
        announcements = announcements.filter(
            models.Q(title__icontains=search_keyword) |
            models.Q(content__icontains=search_keyword)
        )

    # 统计公告数量
    total_announcements = News.objects.filter(is_announcement=True).count()

    # 分页处理
    paginator = Paginator(announcements, 10)  # 每页显示10条公告
    try:
        announcements_paginated = paginator.page(page)
    except PageNotAnInteger:
        announcements_paginated = paginator.page(1)
    except EmptyPage:
        announcements_paginated = paginator.page(paginator.num_pages)

    # 构建上下文数据
    context = {
        'announcements': announcements_paginated,
        'total_announcements': total_announcements,
        'search_keyword': search_keyword
    }

    return render(request, 'admin/announcement_list.html', context)


# 新增公告视图
@admin_required
def admin_add_announcement(request):
    if request.method == 'POST':
        # 从POST请求中获取表单数据
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        # 表单验证
        if not title or not content:
            messages.error(request, '标题和内容不能为空')
            return render(request, 'admin/add_announcement.html')

        try:
            # 创建新公告
            announcement = News.objects.create(
                title=title,
                content=content,
                image=image,
                is_announcement=True
            )

            # 显示成功消息
            messages.success(request, '公告添加成功')

            # 重定向到公告列表页面
            return redirect(reverse('ticket:admin_announcement_list'))
        except Exception as e:
            # 显示错误消息
            messages.error(request, f'添加公告失败: {str(e)}')
            return render(request, 'admin/add_announcement.html')

    # GET请求，渲染新增公告表单
    return render(request, 'admin/add_announcement.html')


# 编辑公告视图
@admin_required
def admin_edit_announcement(request, announcement_id):
    try:
        # 获取要编辑的公告
        announcement = News.objects.get(id=announcement_id, is_announcement=True)
    except News.DoesNotExist:
        messages.error(request, '公告不存在或已被删除')
        return redirect(reverse('ticket:admin_announcement_list'))
    
    if request.method == 'POST':
        # 从POST请求中获取表单数据
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        # 表单验证
        if not title or not content:
            messages.error(request, '标题和内容不能为空')
            return render(request, 'admin/edit_announcement.html', {'announcement': announcement})

        try:
            # 更新公告信息
            announcement.title = title
            announcement.content = content
            if image:
                announcement.image = image
            announcement.save()

            # 显示成功消息
            messages.success(request, '公告更新成功')
            # 重定向到公告列表页面
            return redirect(reverse('ticket:admin_announcement_list'))
        except Exception as e:
            # 显示错误消息
            messages.error(request, f'更新公告失败: {str(e)}')
            return render(request, 'admin/edit_announcement.html', {'announcement': announcement})
    
    # GET请求，渲染编辑公告表单
    return render(request, 'admin/edit_announcement.html', {'announcement': announcement})


# 删除公告视图
@admin_required
def admin_delete_announcement(request, announcement_id):
    if request.method == 'POST':
        try:
            # 根据announcement_id从数据库获取公告
            announcement = News.objects.get(id=announcement_id, is_announcement=True)
            
            # 删除公告
            announcement.delete()
            
            # 显示成功消息
            messages.success(request, '公告删除成功')
        except News.DoesNotExist:
            # 公告不存在
            messages.error(request, '公告不存在或已被删除')
        except Exception as e:
            # 删除失败
            messages.error(request, f'删除公告失败: {str(e)}')
    
    # 获取搜索关键词，保持搜索状态
    search_keyword = request.POST.get('search', '')
    redirect_url = reverse('ticket:admin_announcement_list')
    if search_keyword:
        redirect_url += f'?search={search_keyword}'
    
    # 重定向到公告列表页面
    return redirect(redirect_url)


# 资讯管理视图
@admin_required
def admin_news_list(request):
    # 获取请求参数中的搜索关键词
    search_keyword = request.GET.get('search', '')
    # 获取当前页码，默认为1
    page = request.GET.get('page', 1)

    # 基础查询集：只获取非公告类型的资讯，按创建时间倒序排列
    news_list = News.objects.filter(is_announcement=False).order_by('-created_at')

    # 根据搜索关键词筛选：可搜索资讯标题或内容
    if search_keyword:
        news_list = news_list.filter(
            models.Q(title__icontains=search_keyword) |
            models.Q(content__icontains=search_keyword)
        )

    # 统计资讯数量
    total_news = News.objects.filter(is_announcement=False).count()

    # 分页处理
    paginator = Paginator(news_list, 10)  # 每页显示10条资讯
    try:
        news_paginated = paginator.page(page)
    except PageNotAnInteger:
        news_paginated = paginator.page(1)
    except EmptyPage:
        news_paginated = paginator.page(paginator.num_pages)

    # 构建上下文数据
    context = {
        'news_list': news_paginated,
        'total_news': total_news,
        'search_keyword': search_keyword
    }

    return render(request, 'admin/news_list.html', context)


# 新增资讯视图
@admin_required
def admin_add_news(request):
    if request.method == 'POST':
        # 从POST请求中获取表单数据
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        # 表单验证
        if not title or not content:
            messages.error(request, '标题和内容不能为空')
            return render(request, 'admin/add_news.html')

        try:
            # 创建新资讯
            news = News.objects.create(
                title=title,
                content=content,
                image=image,
                is_announcement=False
            )

            # 显示成功消息
            messages.success(request, '资讯添加成功')

            # 重定向到资讯列表页面
            return redirect(reverse('ticket:admin_news_list'))
        except Exception as e:
            # 显示错误消息
            messages.error(request, f'添加资讯失败: {str(e)}')
            return render(request, 'admin/add_news.html')

    # GET请求，渲染新增资讯表单
    return render(request, 'admin/add_news.html')


# 编辑资讯视图
@admin_required
def admin_edit_news(request, news_id):
    try:
        # 获取要编辑的资讯
        news = News.objects.get(id=news_id, is_announcement=False)
    except News.DoesNotExist:
        messages.error(request, '资讯不存在或已被删除')
        return redirect(reverse('ticket:admin_news_list'))
    
    if request.method == 'POST':
        # 从POST请求中获取表单数据
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        # 表单验证
        if not title or not content:
            messages.error(request, '标题和内容不能为空')
            return render(request, 'admin/edit_news.html', {'news': news})

        try:
            # 更新资讯信息
            news.title = title
            news.content = content
            if image:
                news.image = image
            news.save()

            # 显示成功消息
            messages.success(request, '资讯更新成功')
            # 重定向到资讯列表页面
            return redirect(reverse('ticket:admin_news_list'))
        except Exception as e:
            # 显示错误消息
            messages.error(request, f'更新资讯失败: {str(e)}')
            return render(request, 'admin/edit_news.html', {'news': news})
    
    # GET请求，渲染编辑资讯表单
    return render(request, 'admin/edit_news.html', {'news': news})


# 删除资讯视图
@admin_required
def admin_delete_news(request, news_id):
    if request.method == 'POST':
        try:
            # 根据news_id从数据库获取资讯
            news = News.objects.get(id=news_id, is_announcement=False)
            
            # 删除资讯
            news.delete()
            
            # 显示成功消息
            messages.success(request, '资讯删除成功')
        except News.DoesNotExist:
            # 资讯不存在
            messages.error(request, '资讯不存在或已被删除')
        except Exception as e:
            # 删除失败
            messages.error(request, f'删除资讯失败: {str(e)}')
    
    # 获取搜索关键词，保持搜索状态
    search_keyword = request.POST.get('search', '')
    redirect_url = reverse('ticket:admin_news_list')
    if search_keyword:
        redirect_url += f'?search={search_keyword}'
    
    # 重定向到资讯列表页面
    return redirect(redirect_url)


# 编辑资讯视图
@admin_required
def admin_edit_news(request, news_id):
    try:
        # 获取要编辑的资讯
        news = News.objects.get(id=news_id, is_announcement=False)
    except News.DoesNotExist:
        messages.error(request, '资讯不存在或已被删除')
        return redirect(reverse('ticket:admin_news_list'))
    
    if request.method == 'POST':
        # 从POST请求中获取表单数据
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        # 表单验证
        if not title or not content:
            messages.error(request, '标题和内容不能为空')
            return render(request, 'admin/edit_news.html', {'news': news})

        try:
            # 更新资讯信息
            news.title = title
            news.content = content
            if image:
                news.image = image
            news.save()

            # 显示成功消息
            messages.success(request, '资讯更新成功')
            # 重定向到资讯列表页面
            return redirect(reverse('ticket:admin_news_list'))
        except Exception as e:
            # 显示错误消息
            messages.error(request, f'更新资讯失败: {str(e)}')
            return render(request, 'admin/edit_news.html', {'news': news})
    
    # GET请求，渲染编辑资讯表单
    return render(request, 'admin/edit_news.html', {'news': news})


# 删除资讯视图
@admin_required
def admin_delete_news(request, news_id):
    if request.method == 'POST':
        try:
            # 根据news_id从数据库获取资讯
            news = News.objects.get(id=news_id, is_announcement=False)
            
            # 删除资讯
            news.delete()
            
            # 显示成功消息
            messages.success(request, '资讯删除成功')
        except News.DoesNotExist:
            # 资讯不存在
            messages.error(request, '资讯不存在或已被删除')
        except Exception as e:
            # 删除失败
            messages.error(request, f'删除资讯失败: {str(e)}')
    
    # 获取搜索关键词，保持搜索状态
    search_keyword = request.POST.get('search', '')
    redirect_url = reverse('ticket:admin_news_list')
    if search_keyword:
        redirect_url += f'?search={search_keyword}'
    
    # 重定向到资讯列表页面
    return redirect(redirect_url)


# 密码管理视图
@admin_required
def admin_password_change(request):
    if request.method == 'POST':
        # 从POST请求中获取表单数据
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # 表单验证
        if not old_password or not new_password or not confirm_password:
            messages.error(request, '请填写所有必填字段')
            return render(request, 'admin/password_change.html')

        if new_password != confirm_password:
            messages.error(request, '两次输入的新密码不一致')
            return render(request, 'admin/password_change.html')

        # 获取当前登录用户
        user = request.user

        # 验证旧密码
        if not user.check_password(old_password):
            messages.error(request, '旧密码错误')
            return render(request, 'admin/password_change.html')

        try:
            # 更新密码
            user.set_password(new_password)
            user.save()

            # 显示成功消息
            messages.success(request, '密码修改成功，请重新登录')

            # 退出登录
            logout(request)

            # 重定向到登录页面
            return redirect(reverse('ticket:user_login'))
        except Exception as e:
            # 显示错误消息
            messages.error(request, f'修改密码失败: {str(e)}')
            return render(request, 'admin/password_change.html')

    # GET请求，渲染密码修改表单
    return render(request, 'admin/password_change.html')


# 获取景点列表API视图函数，用于登录页面的景点选择下拉框
def get_scenic_spots_api(request):
    # 获取所有景点
    scenic_spots = ScenicSpot.objects.all()
    # 构建景点列表数据
    scenic_spots_data = [
        {
            'id': spot.id,
            'name': spot.name
        }
        for spot in scenic_spots
    ]
    # 返回JSON响应
    return JsonResponse(scenic_spots_data, safe=False)


# 注册视图函数，处理用户注册请求
def register(request):
    # 判断请求方法是否为POST（表单提交）
    if request.method == 'POST':
        # 从POST请求中获取数据
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role', 0)  # 默认角色为游客

        # 验证密码是否一致
        if password != confirm_password:
            messages.error(request, '两次输入的密码不一致')
            return render(request, 'register.html')

        # 验证用户名是否已存在
        if User.objects.filter(username=username).exists():
            messages.error(request, '用户名已存在')
            return render(request, 'register.html')

        # 验证邮箱是否已存在
        if User.objects.filter(email=email).exists():
            messages.error(request, '邮箱已被注册')
            return render(request, 'register.html')

        # 创建用户
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # 设置用户角色
        user.role = int(role)
        user.save()

        # 显示注册成功消息
        messages.success(request, '注册成功，请登录')

        # 重定向到登录页面，使用reverse函数根据URL名称生成URL，需要包含命名空间
        return redirect(reverse('ticket:login'))

    # 如果请求方法不是POST，渲染注册页面
    return render(request, 'register.html')


# 个人中心视图函数，处理用户个人中心请求
# @login_required装饰器：要求用户必须登录才能访问该视图
@login_required
def personal_center(request):
    # 获取当前登录用户
    user = request.user
    
    # 判断请求方法是否为POST（表单提交）
    if request.method == 'POST':
        # 更新用户信息
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        user.gender = request.POST.get('gender')

        # 处理出生日期
        birthdate_str = request.POST.get('birthdate')
        if birthdate_str and birthdate_str != 'yyyy/mm/日':
            try:
                # 解析 yyyy/mm/日 格式的日期字符串
                import re
                match = re.match(r'(\d{4})/(\d{1,2})/(\d{1,2})', birthdate_str)
                if match:
                    year, month, day = map(int, match.groups())
                    from datetime import date
                    user.birthdate = date(year, month, day)
            except Exception as e:
                # 解析失败时设置为 None
                user.birthdate = None
        else:
            user.birthdate = None

        # 处理头像上传
        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']

        # 保存用户信息
        user.save()

        # 显示成功消息
        messages.success(request, '个人信息更新成功')

        # 重定向到个人中心页面
        return redirect(reverse('ticket:personal_center'))

    # 获取用户收藏的景点
    favorites = Collection.objects.filter(user=user).select_related('scenic_spot').order_by('-created_at')
    
    # 获取用户的浏览历史
    browse_history = BrowseHistory.objects.filter(user=user).select_related('scenic_spot').order_by('-browse_time')
    
    # 获取用户的评论
    my_comments = ScenicSpotComment.objects.filter(user=user).select_related('scenic_spot').order_by('-created_at')
    
    # 构建上下文数据
    context = {
        'favorites': favorites,
        'browse_history': browse_history,
        'my_comments': my_comments,
    }
    
    # 如果请求方法不是POST，渲染个人中心页面，传递上下文数据
    return render(request, 'personal_center.html', context)


# 修改密码视图函数，需要登录才能访问
@login_required
def change_password(request):
    # 判断请求方法是否为POST（表单提交）
    if request.method == 'POST':
        # 获取表单数据
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        # 获取当前登录用户
        user = request.user

        # 验证原密码
        if not user.check_password(old_password):
            # 显示错误消息
            messages.error(request, '原密码错误')
            # 重定向到个人中心页面
            return redirect(reverse('ticket:personal_center'))

        # 验证新密码
        if new_password1 != new_password2:
            # 显示错误消息
            messages.error(request, '两次输入的新密码不一致')
            # 重定向到个人中心页面
            return redirect(reverse('ticket:personal_center'))

        # 更新密码
        user.set_password(new_password1)
        # 保存用户信息
        user.save()

        # 显示成功消息
        messages.success(request, '密码修改成功')
        # 重定向到个人中心页面
        return redirect(reverse('ticket:personal_center'))

    # 如果请求方法不是POST，重定向到个人中心页面
    return redirect(reverse('ticket:personal_center'))


# 景点信息列表视图
def scenic_spots(request):
    # 获取搜索关键词
    search_keyword = request.GET.get('search', '')
    # 获取地区筛选条件
    region_filter = request.GET.get('region', '')
    # 获取分类筛选条件
    category_filter = request.GET.get('category', '')
    # 获取当前页码，默认为1
    page = request.GET.get('page', 1)

    # 基础查询集
    spots = ScenicSpot.objects.all()

    # 根据搜索关键词筛选
    if search_keyword:
        spots = spots.filter(name__icontains=search_keyword) | spots.filter(
            address__icontains=search_keyword) | spots.filter(region__name__icontains=search_keyword)

    # 根据地区筛选
    if region_filter and region_filter != '全部地区':
        # 尝试将region_filter转换为整数ID，如果失败则按名称筛选
        try:
            region_id = int(region_filter)
            spots = spots.filter(region_id=region_id)
        except ValueError:
            spots = spots.filter(region__name=region_filter)

    # 根据分类筛选
    if category_filter and category_filter != '全部分类':
        spots = spots.filter(category=category_filter)

    # 获取所有地区（用于筛选）
    regions = Region.objects.values_list('name', flat=True).distinct().order_by('name')
    # 获取所有分类（用于筛选）
    # 从Category模型获取分类列表，确保分类名称完整
    categories = Category.objects.values_list('name', flat=True).distinct().order_by('name')

    # 预处理景点数据，将tags转换为列表
    spots_with_tags = []
    for spot in spots:
        # 将tags字符串分割为列表
        tags_list = [tag.strip() for tag in spot.tags.split(',') if tag.strip()]
        # 将处理后的tags列表添加到spot对象中
        spot.tags_list = tags_list
        spots_with_tags.append(spot)

    # 分页处理
    paginator = Paginator(spots_with_tags, 9)  # 每页显示9个景点
    try:
        spots_paginated = paginator.page(page)
    except PageNotAnInteger:
        spots_paginated = paginator.page(1)
    except EmptyPage:
        spots_paginated = paginator.page(paginator.num_pages)

    # 构建上下文
    context = {
        'spots': spots_paginated,
        'search_keyword': search_keyword,
        'region_filter': region_filter,
        'category_filter': category_filter,
        'regions': regions,
        'categories': categories,
    }

    # 渲染scenic_spots.html模板，将数据传递给模板
    return render(request, 'scenic_spots.html', context)


# 景点详情视图函数，处理单个景点的详情页请求
# spot_id: 景点ID，从URL中获取
def scenic_spot_detail(request, spot_id):
    # 根据景点ID从数据库中获取景点信息
    try:
        spot = ScenicSpot.objects.get(id=spot_id)
    except ScenicSpot.DoesNotExist:
        # 景点不存在时显示错误信息并重定向到首页
        messages.error(request, '该景点不存在或已被删除')
        return redirect(reverse('ticket:index'))
    # 将tags字符串分割为列表
    tags_list = [tag.strip() for tag in spot.tags.split(',')]
    # 获取该景点的所有留言，按创建时间倒序排列
    comments = ScenicSpotComment.objects.filter(scenic_spot=spot).order_by('-created_at')
    
    # 记录浏览历史
    if request.user.is_authenticated:
        # 检查用户是否已经浏览过该景点
        browse_history, created = BrowseHistory.objects.get_or_create(
            user=request.user,
            scenic_spot=spot
        )
        # 如果是已存在的记录，更新浏览时间为当前时间
        if not created:
            browse_history.browse_time = timezone.now()
            browse_history.save()
    
    # 处理留言提交
    if request.method == 'POST' and request.user.is_authenticated:
        comment_content = request.POST.get('comment_content')
        if comment_content and comment_content.strip():
            # 创建新的留言
            ScenicSpotComment.objects.create(
                scenic_spot=spot,
                user=request.user,
                content=comment_content.strip()
            )
            # 重定向到当前页面，刷新留言列表
            return redirect(reverse('ticket:scenic_spot_detail', kwargs={'spot_id': spot_id}))
    
    # 构建上下文
    context = {
        'spot': spot,
        'tags_list': tags_list,
        'comments': comments,
    }
    
    # 渲染scenic_spot_detail.html模板，将景点详情数据传递给模板
    return render(request, 'scenic_spot_detail.html', context)


# 资讯公告列表视图函数，处理资讯公告列表页请求
def news_list(request):
    # 获取筛选参数，默认显示全部
    filter_type = request.GET.get('type', 'all')
    # 获取当前页码，默认为1
    page = request.GET.get('page', 1)

    # 根据筛选条件获取资讯公告，按创建时间倒序排列
    if filter_type == 'news':
        news = News.objects.filter(is_announcement=False).order_by('-created_at')
    elif filter_type == 'announcement':
        news = News.objects.filter(is_announcement=True).order_by('-created_at')
    else:
        news = News.objects.all().order_by('-created_at')

    # 分页处理
    paginator = Paginator(news, 10)  # 每页显示10条资讯
    try:
        news_paginated = paginator.page(page)
    except PageNotAnInteger:
        news_paginated = paginator.page(1)
    except EmptyPage:
        news_paginated = paginator.page(paginator.num_pages)

    # 渲染news_list.html模板，将资讯公告数据和筛选类型传递给模板
    return render(request, 'news_list.html', {'news': news_paginated, 'filter_type': filter_type})


# 资讯公告详情视图函数，处理单个资讯公告的详情页请求
# news_id: 资讯ID，从URL中获取
def news_detail(request, news_id):
    # 根据资讯ID从数据库中获取单个资讯公告信息
    try:
        news_item = News.objects.get(id=news_id)
    except News.DoesNotExist:
        # 资讯不存在时显示错误信息并重定向到资讯列表页
        messages.error(request, '该资讯不存在或已被删除')
        return redirect(reverse('ticket:news_list'))
    # 渲染news_detail.html模板，将资讯详情数据传递给模板
    return render(request, 'news_detail.html', {'news': news_item})

# 购票页面视图函数，处理景点购票请求
# spot_id: 景点ID，从URL中获取
@login_required
def buy_ticket(request, spot_id):
    # 导入日期处理模块
    from datetime import date
    # 获取当前日期
    today = date.today()
    # 根据景点ID从数据库中获取景点信息
    try:
        spot = ScenicSpot.objects.get(id=spot_id)
    except ScenicSpot.DoesNotExist:
        # 景点不存在时显示错误信息并重定向到景点列表页
        messages.error(request, '该景点不存在或已被删除')
        return redirect(reverse('ticket:scenic_spots'))
    # 获取该景点的所有激活状态的门票类型
    ticket_types = TicketType.objects.filter(scenic_spot=spot, is_active=True)
    # 分类门票类型：单票和套票
    single_tickets = ticket_types.filter(type='single')
    package_tickets = ticket_types.filter(type='package')
    
    # 检查会话中是否有购票选择
    buy_ticket_selection = request.session.get('buy_ticket_selection')
    selected_use_date = None
    selected_ticket_type = None
    selected_quantity = 1
    
    # 如果有保存的购票选择，获取并应用
    if buy_ticket_selection:
        selected_use_date = buy_ticket_selection.get('use_date')
        selected_ticket_type = buy_ticket_selection.get('ticket_type_id')
        selected_quantity = buy_ticket_selection.get('quantity', 1)
        # 删除会话中的购票选择，避免重复使用
        del request.session['buy_ticket_selection']
        request.session.save()
    
    # 处理表单提交
    if request.method == 'POST':
        # 获取表单数据
        use_date = request.POST.get('use_date')
        ticket_type_id = request.POST.get('ticket_type')
        quantity = int(request.POST.get('quantity', 1))
        action = request.POST.get('action')
        
        # 验证是否选择了门票类型
        if not ticket_type_id:
            # 如果没有选择门票类型，显示错误信息
            messages.error(request, '请选择门票类型')
            # 返回购票页面时保留用户之前的选择
            return render(request, 'buy_ticket.html', {
                'spot': spot,
                'ticket_types': ticket_types,
                'single_tickets': single_tickets,
                'package_tickets': package_tickets,
                'selected_use_date': use_date,
                'selected_quantity': quantity
            })
        
        # 获取门票类型
        ticket_type = TicketType.objects.get(id=ticket_type_id)
        
        # 检查当天的库存是否充足
        from datetime import datetime
        use_date_obj = datetime.strptime(use_date, '%Y-%m-%d').date()
        
        # 获取或创建对应日期的库存记录
        date_stock, created = DateStock.objects.get_or_create(
            ticket_type=ticket_type,
            use_date=use_date_obj,
            defaults={'stock': ticket_type.stock}  # 使用门票类型的默认库存作为初始值
        )
        
        # 检查该日期的库存是否充足
        if date_stock.stock < quantity:
            # 库存不足，显示错误信息
            messages.error(request, f'门票库存不足，{use_date} 当日库存仅剩 {date_stock.stock} 张')
            # 返回购票页面时保留用户之前的选择
            return render(request, 'buy_ticket.html', {
                'spot': spot,
                'ticket_types': ticket_types,
                'single_tickets': single_tickets,
                'package_tickets': package_tickets,
                'selected_use_date': use_date,
                'selected_quantity': quantity,
                'today': today
            })
        
        # 计算总价
        total_price = ticket_type.price * quantity
        
        # 处理不同的操作
        if action == 'buy_now':
            # 直接购买：创建订单并跳转到支付页面
            if request.user.is_authenticated:
                # 生成订单号
                import datetime
                import uuid
                order_number = f"ORD{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:6].upper()}"
                
                # 创建订单
                order = Order.objects.create(
                    user=request.user,
                    scenic_spot=spot,
                    ticket_type=ticket_type,
                    use_date=use_date,
                    quantity=quantity,
                    total_price=total_price,
                    order_number=order_number
                )
                
                # 减少对应日期的库存
                date_stock.stock -= quantity
                date_stock.sold += quantity
                date_stock.save()
                
                # 跳转到支付页面
                return redirect(reverse('ticket:payment', kwargs={'order_id': order.id}))
            else:
                # 用户未登录，保存当前购票选择到会话，然后跳转到登录页面
                messages.error(request, '请先登录')
                # 保存当前购票选择到会话
                request.session['buy_ticket_selection'] = {
                    'spot_id': spot.id,
                    'use_date': use_date,
                    'ticket_type_id': ticket_type_id,
                    'quantity': quantity
                }
            return redirect(reverse('ticket:login'))
        elif action == 'add_to_cart':
            # 加入购物车：添加到用户购物车
            if request.user.is_authenticated:
                # 检查是否已存在相同的购物车项
                cart_item, created = Cart.objects.get_or_create(
                    user=request.user,
                    scenic_spot=spot,
                    ticket_type=ticket_type,
                    use_date=use_date,
                    defaults={'quantity': quantity}
                )
                
                # 如果已存在，更新数量
                if not created:
                    cart_item.quantity += quantity
                    cart_item.save()
                
                return redirect(reverse('ticket:scenic_spots'))
            else:
                # 用户未登录，跳转到登录页面
                messages.error(request, '请先登录')
                return redirect(reverse('ticket:login'))
    
        # 获取当前选择的日期，如果没有则使用今天
    selected_date = selected_use_date if selected_use_date else today.strftime('%Y-%m-%d')
    
    # 为每个门票类型获取对应日期的库存数据
    from datetime import datetime
    selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
    
    # 为每个门票类型创建带有日期特定库存的对象
    single_tickets_with_stock = []
    package_tickets_with_stock = []
    
    for ticket in ticket_types:
        # 获取对应日期的库存记录
        date_stock = ticket.datestock_set.filter(use_date=selected_date_obj).first()
        # 创建带有日期特定库存的门票对象
        ticket_with_stock = {
            'ticket': ticket,
            'stock': date_stock.stock if date_stock else ticket.stock,
            'is_sold_out': (date_stock.stock <= 0 if date_stock else ticket.stock <= 0)
        }
        # 根据门票类型添加到不同列表
        if ticket.type == 'single':
            single_tickets_with_stock.append(ticket_with_stock)
        else:
            package_tickets_with_stock.append(ticket_with_stock)
    
    # 渲染buy_ticket.html模板，将景点和门票类型数据传递给模板
    return render(request, 'buy_ticket.html', {
        'spot': spot,
        'ticket_types': ticket_types,
        'single_tickets': single_tickets_with_stock,
        'package_tickets': package_tickets_with_stock,
        'selected_use_date': selected_use_date,
        'selected_ticket_type': selected_ticket_type,
        'selected_quantity': selected_quantity,
        'today': today,
        'selected_date': selected_date
    })

from .weather_api import get_weather_by_region

# 天气页面视图函数，显示门票使用日期的天气情况
# order_id: 订单ID，从URL中获取
def weather_check(request, order_id):
    # 根据订单ID从数据库中获取订单信息
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        # 订单不存在时显示错误信息并重定向到订单中心
        messages.error(request, '该订单不存在或已被删除')
        return redirect(reverse('ticket:order_center'))
    
    # 获取景点地区名称
    region_name = order.scenic_spot.region.name if order.scenic_spot.region else '未知地区'
    
    # 调用天气API获取真实天气数据
    weather_result = get_weather_by_region(region_name, order.use_date)
    
    if weather_result['success']:
        # 天气查询成功
        weather_data = weather_result
    else:
        # 天气查询失败，使用默认模拟数据
        weather_data = {
            'date': order.use_date,
            'temperature': '15-25°C',
            'weather': '晴',
            'wind': '微风',
            'humidity': '45%',
            'advice': f'天气查询失败：{weather_result.get("error", "未知错误")}，建议关注当地天气预报'
        }
    
    # 渲染weather_check.html模板，将订单和天气数据传递给模板
    return render(request, 'weather_check.html', {
        'order': order,
        'weather_data': weather_data
    })

# AJAX获取门票库存视图函数
def get_ticket_stocks(request):
    # 获取请求参数
    date_str = request.GET.get('date')
    spot_id = request.GET.get('spot_id')
    
    if not date_str or not spot_id:
        return JsonResponse({'success': False, 'message': '缺少必要参数'})
    
    try:
        from datetime import datetime
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        spot = ScenicSpot.objects.get(id=spot_id)
        
        # 获取该景点的所有激活状态的门票类型
        ticket_types = TicketType.objects.filter(scenic_spot=spot, is_active=True)
        
        # 构建库存数据
        stocks_data = []
        for ticket in ticket_types:
            # 获取对应日期的库存记录
            date_stock = ticket.datestock_set.filter(use_date=selected_date).first()
            # 如果没有记录，使用门票的默认库存
            stock = date_stock.stock if date_stock else ticket.stock
            
            stocks_data.append({
                'id': ticket.id,
                'stock': stock,
                'is_sold_out': stock <= 0
            })
        
        return JsonResponse({'success': True, 'data': stocks_data})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

# 支付页面视图函数，处理订单支付请求
# order_id: 订单ID，从URL中获取
def payment(request, order_id):
    # 根据订单ID从数据库中获取订单信息
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        # 订单不存在时显示错误信息并重定向到订单中心
        messages.error(request, '该订单不存在或已被删除')
        return redirect(reverse('ticket:order_center'))
    
    # 渲染通用支付页面，将订单数据传递给模板
    return render(request, 'general_payment.html', {
        'orders': [order],
        'total_price': order.total_price,
        'from_cart': False
    })


# 购物车视图函数，处理用户购物车请求
# @login_required装饰器：要求用户必须登录才能访问该视图
@login_required
def cart(request):
    # 获取当前登录用户的购物车记录
    cart_items = Cart.objects.filter(user=request.user)
    
    # 为每个购物车项添加总价属性
    for item in cart_items:
        # 计算每个购物车项的总价（单价×数量）
        item.total_price = item.ticket_type.price * item.quantity
    
    # 处理表单提交（购买功能）
    if request.method == 'POST':
        # 获取用户选择的购物车项目ID
        selected_item_ids = request.POST.getlist('selected_items')
        
        print(f"=== 购物车视图调试信息 ===")
        print(f"请求方法: {request.method}")
        print(f"选中的购物车项ID: {selected_item_ids}")
        print(f"选中的购物车项数量: {len(selected_item_ids)}")
        
        # 检查是否选择了商品
        if not selected_item_ids:
            messages.error(request, '请选择要购买的商品')
            print(f"错误提示: 请选择要购买的商品")
            return redirect(reverse('ticket:cart'))
        
        # 遍历选中的购物车项目，创建订单
        orders = []
        deleted_ids = []
        
        # 去重处理，避免重复处理同一个购物车项
        unique_item_ids = list(set(selected_item_ids))
        print(f"去重后的购物车项ID: {unique_item_ids}")
        
        for item_id in unique_item_ids:
            try:
                # 检查ID是否已被处理过
                if item_id in deleted_ids:
                    print(f"跳过已处理的购物车项ID: {item_id}")
                    continue
                    
                # 获取购物车项目，使用filter避免DoesNotExist异常
                cart_items = Cart.objects.filter(id=item_id, user=request.user)
                if not cart_items.exists():
                    print(f"购物车项不存在，ID: {item_id}")
                    continue
                    
                cart_item = cart_items.first()
                print(f"获取到购物车项: {cart_item.id}, 景点: {cart_item.scenic_spot.name}")
                
                # 生成订单号
                import datetime
                import uuid
                order_number = f"ORD{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:6].upper()}"
                print(f"生成订单号: {order_number}")
                
                # 检查库存是否充足
                if cart_item.ticket_type.stock < cart_item.quantity:
                    print(f"购物车项ID: {item_id}，库存不足，当前库存: {cart_item.ticket_type.stock}，请求数量: {cart_item.quantity}")
                    messages.error(request, f'{cart_item.scenic_spot.name} - {cart_item.ticket_type.name} 的门票库存不足，当前库存仅剩 {cart_item.ticket_type.stock} 张')
                    continue
                
                # 计算订单总价
                total_price = cart_item.ticket_type.price * cart_item.quantity
                print(f"计算订单总价: {total_price}")
                
                # 创建订单
                order = Order.objects.create(
                    user=request.user,
                    scenic_spot=cart_item.scenic_spot,
                    ticket_type=cart_item.ticket_type,
                    use_date=cart_item.use_date,
                    quantity=cart_item.quantity,
                    total_price=total_price,
                    order_number=order_number
                )
                print(f"创建订单成功: {order.id}")
                
                # 减少库存
                cart_item.ticket_type.stock -= cart_item.quantity
                cart_item.ticket_type.save()
                print(f"减少库存: 门票类型ID={cart_item.ticket_type.id}, 数量={cart_item.quantity}, 剩余库存={cart_item.ticket_type.stock}")
                
                orders.append(order)
                
                # 从购物车中删除已购买的项目
                cart_item.delete()
                print(f"从购物车中删除项目: {item_id}")
                
                # 记录已删除的ID
                deleted_ids.append(item_id)
            except Exception as e:
                # 捕获所有异常，避免处理一个商品失败影响其他商品
                print(f"处理购物车项时发生错误，ID: {item_id}, 错误: {str(e)}")
                # 只在控制台打印错误，不向用户显示，避免影响用户体验
                continue
        
        print(f"成功创建订单数量: {len(orders)}")
        
        if orders:
            # 提取订单ID列表
            order_ids = [order.id for order in orders]
            print(f"订单ID列表: {order_ids}")
            
            # 如果只有一个订单，直接跳转到支付页面
            if len(orders) == 1:
                payment_url = reverse('ticket:payment', kwargs={'order_id': orders[0].id})
                print(f"单个订单，跳转到支付页面: {payment_url}")
                return redirect(payment_url)
            else:
                # 多个订单，将订单ID存储到会话中，然后跳转到批量支付页面
                request.session['batch_order_ids'] = order_ids
                print(f"多个订单，跳转到批量支付页面")
                return redirect(reverse('ticket:batch_payment'))
        else:
            messages.error(request, '没有成功创建订单，请重新尝试')
            print(f"错误: 没有成功创建订单，请重新尝试")
            return redirect(reverse('ticket:cart'))

    # 渲染cart.html模板，将购物车数据传递给模板
    return render(request, 'cart.html', {'cart_items': cart_items})


# 订单中心视图函数，处理用户订单中心请求
# @login_required装饰器：要求用户必须登录才能访问该视图
@login_required
def order_center(request):
    # 获取当前登录用户的所有订单
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    # 获取当前页码，默认为1
    page = request.GET.get('page', 1)

    # 分页处理
    paginator = Paginator(orders, 10)  # 每页显示10个订单
    try:
        orders_paginated = paginator.page(page)
    except PageNotAnInteger:
        orders_paginated = paginator.page(1)
    except EmptyPage:
        orders_paginated = paginator.page(paginator.num_pages)

    # 渲染order_center.html模板，将订单数据传递给模板
    return render(request, 'order_center.html', {'orders': orders_paginated})

# 删除购物车项视图函数
# @login_required装饰器：要求用户必须登录才能访问该视图
@login_required
def delete_cart_item(request, cart_id):
    # 判断请求方法是否为POST
    if request.method == 'POST':
        try:
            # 获取购物车项，确保属于当前用户
            cart_item = Cart.objects.get(id=cart_id, user=request.user)
            # 删除购物车项
            cart_item.delete()
            # 跳转到购物车页面
            return redirect(reverse('ticket:cart'))
        except Cart.DoesNotExist:
            # 购物车项不存在，显示错误信息
            messages.error(request, '购物车项不存在或已被删除')
            return redirect(reverse('ticket:cart'))
    
    # 如果不是POST请求，重定向到购物车页面
    return redirect(reverse('ticket:cart'))

# 移入收藏视图函数
# @login_required装饰器：要求用户必须登录才能访问该视图
@login_required
def add_to_collection(request, cart_id):
    # 判断请求方法是否为POST
    if request.method == 'POST':
        try:
            # 获取购物车项，确保属于当前用户
            cart_item = Cart.objects.get(id=cart_id, user=request.user)
            
            # 创建或获取收藏记录
            collection, created = Collection.objects.get_or_create(
                user=request.user,
                scenic_spot=cart_item.scenic_spot
            )
            
            # 如果是新创建的收藏，显示成功信息
            if created:
                messages.success(request, '已成功加入收藏')
            else:
                messages.info(request, '该景点已在收藏列表中')
            
            # 跳转到购物车页面
            return redirect(reverse('ticket:cart'))
        except Cart.DoesNotExist:
            # 购物车项不存在，显示错误信息
            messages.error(request, '购物车项不存在或已被删除')
            return redirect(reverse('ticket:cart'))
    
    # 如果不是POST请求，重定向到购物车页面
    return redirect(reverse('ticket:cart'))

# 批量支付视图函数，显示所有选中的订单并计算总价格
# @login_required装饰器：要求用户必须登录才能访问该视图
@login_required
def batch_payment(request):
    # 获取订单ID列表（从会话或请求参数中获取）
    order_ids = request.session.pop('batch_order_ids', [])
    print(f"=== 批量支付页面调试信息 ===")
    print(f"请求方法: {request.method}")
    print(f"订单ID列表: {order_ids}")
    
    # 检查是否有订单ID
    if not order_ids:
        messages.error(request, '请选择要支付的订单')
        return redirect(reverse('ticket:cart'))
    
    # 获取订单信息
    orders = Order.objects.filter(id__in=order_ids, user=request.user)
    print(f"获取到订单数量: {orders.count()}")
    
    # 计算总价格
    total_price = sum(order.total_price for order in orders)
    print(f"总价格: {total_price}")
    
    # 渲染通用支付页面
    return render(request, 'general_payment.html', {
        'orders': orders,
        'total_price': total_price,
        'from_cart': True
    })

# 确认支付视图函数，处理实际的支付逻辑
# @login_required装饰器：要求用户必须登录才能访问该视图
@login_required
def confirm_payment(request):
    # 判断请求方法是否为POST（表单提交）
    if request.method == 'POST':
        # 获取选中的订单ID列表
        order_ids = request.POST.getlist('order_ids')
        print(f"=== 确认支付调试信息 ===")
        print(f"请求方法: {request.method}")
        print(f"选中的订单ID: {order_ids}")
        print(f"选中的订单数量: {len(order_ids)}")
        
        # 检查是否选择了订单
        if not order_ids:
            messages.error(request, '请选择要支付的订单')
            return redirect(reverse('ticket:cart'))
        
        # 获取支付方式
        payment_method = request.POST.get('payment_method', 'alipay')
        print(f"支付方式: {payment_method}")
        
        # 统计成功和失败的订单数量
        success_count = 0
        failed_count = 0
        
        # 遍历处理每个订单
        for order_id in order_ids:
            try:
                # 获取订单信息，确保订单属于当前用户
                order = Order.objects.get(id=order_id, user=request.user)
                print(f"获取到订单: {order.id}, 状态: {order.status}")
                
                # 只有待支付订单才能支付
                if order.status == 0:
                    # 模拟支付成功
                    order.status = 1  # 更新订单状态为已支付
                    
                    # 减少对应日期的库存
                    if order.ticket_type and order.use_date:
                        # 获取或创建对应日期的库存记录
                        date_stock, created = DateStock.objects.get_or_create(
                            ticket_type=order.ticket_type,
                            use_date=order.use_date,
                            defaults={'stock': order.ticket_type.stock}
                        )
                        # 减少库存并增加已售数量
                        date_stock.stock -= order.quantity
                        date_stock.sold += order.quantity
                        date_stock.save()
                        print(f"订单 {order.id} 减少 {order.use_date} 库存: {order.quantity}, 剩余库存: {date_stock.stock}")
                    
                    order.save()
                    print(f"订单 {order.id} 支付成功")
                    success_count += 1
                else:
                    print(f"订单 {order.id} 状态不允许支付，当前状态: {order.status}")
                    failed_count += 1
            except Order.DoesNotExist:
                print(f"订单 {order_id} 不存在或已被删除")
                failed_count += 1
                continue
        
        # 显示结果消息
        if success_count > 0:
            messages.success(request, f'成功支付 {success_count} 个订单')
        if failed_count > 0:
            messages.error(request, f'有 {failed_count} 个订单支付失败')
        
        print(f"支付完成: 成功 {success_count} 个，失败 {failed_count} 个")
        
        # 如果有成功支付的订单，跳转到第一个订单的天气页面
        if success_count > 0:
            # 获取第一个成功支付的订单
            first_order = Order.objects.filter(id__in=order_ids, user=request.user).first()
            if first_order:
                # 跳转到天气页面
                return redirect(reverse('ticket:weather_check', kwargs={'order_id': first_order.id}))
        
        # 否则跳转到订单中心
        return redirect(reverse('ticket:order_center'))
    
    # 如果不是POST请求，重定向到购物车
    return redirect(reverse('ticket:cart'))


# 取消订单视图函数，处理用户取消订单请求
# @login_required装饰器：要求用户必须登录才能访问该视图
@login_required
def cancel_order(request, order_id):
    # 判断请求方法是否为POST（表单提交）
    if request.method == 'POST':
        try:
            # 获取订单信息，确保订单属于当前用户
            order = Order.objects.get(id=order_id, user=request.user)
            
            # 只有待支付订单才能取消
            if order.status == 0:
                # 恢复对应日期的库存
                if order.ticket_type and order.use_date:
                    # 获取对应日期的库存记录
                    date_stock = DateStock.objects.filter(
                        ticket_type=order.ticket_type,
                        use_date=order.use_date
                    ).first()
                    if date_stock:
                        # 恢复库存并减少已售数量
                        date_stock.stock += order.quantity
                        date_stock.sold -= order.quantity
                        date_stock.save()
                
                # 更新订单状态为已取消
                order.status = 2
                order.save()
                
                # 显示成功消息
                messages.success(request, '订单已成功取消')
            else:
                # 非待支付订单不能取消
                messages.error(request, '只有待支付订单才能取消')
        except Order.DoesNotExist:
            # 订单不存在或不属于当前用户
            messages.error(request, '订单不存在或您没有权限操作')
        except Exception as e:
            # 其他错误
            messages.error(request, f'取消订单失败: {str(e)}')
    
    # 重定向回订单中心页面
    return redirect(reverse('ticket:order_center'))


# 申请退款视图函数，处理用户申请退款请求
# @login_required装饰器：要求用户必须登录才能访问该视图
@login_required
def apply_refund(request, order_id):
    # 判断请求方法是否为POST（表单提交）
    if request.method == 'POST':
        # 获取退款原因
        refund_reason = request.POST.get('refund_reason')
        
        try:
            # 获取订单信息，确保订单属于当前用户
            order = Order.objects.get(id=order_id, user=request.user)
            
            # 只有已支付订单才能申请退款
            if order.status == 1:
                # 更新订单信息
                order.refund_reason = refund_reason
                order.refund_apply_time = timezone.now()
                order.status = 5  # 设置为退款审核中，等待管理员审核
                order.save()
                
                # 显示成功消息
                messages.success(request, '退款申请已提交，正在等待管理员审核')
            else:
                # 订单状态不是已支付，无法申请退款
                messages.error(request, '只有已支付的订单才能申请退款')
        except Order.DoesNotExist:
            # 订单不存在或不属于当前用户
            messages.error(request, '订单不存在或您没有权限操作')
        except Exception as e:
            # 其他错误
            messages.error(request, f'申请退款失败: {str(e)}')
    
    # 重定向到订单中心页面
    return redirect(reverse('ticket:order_center'))


# 景点管理员处理退款视图函数（审核通过）
@scenic_admin_required
def scenic_admin_refund_order(request, order_id):
    # 判断请求方法是否为POST（表单提交）
    if request.method == 'POST':
        # 获取当前景点管理员
        admin = request.user
        
        try:
            # 获取该管理员管理的景点
            scenic_spots = ScenicSpot.objects.filter(admin=admin)
            scenic_ids = scenic_spots.values_list('id', flat=True)
            
            # 获取订单信息，确保订单属于该管理员管理的景点
            order = Order.objects.get(id=order_id, scenic_spot__id__in=scenic_ids)
            
            if order.status == 1:
                # 已支付订单：管理员主动发起退款，设置为退款审核中
                order.status = 5  # 设置为退款审核中
                order.refund_amount = order.total_price  # 全额退款
                order.refund_apply_time = timezone.now()
                order.save()
                messages.success(request, '已发起退款流程')
            elif order.status == 5:
                # 退款审核中的订单：管理员审核通过
                order.status = 4  # 设置为已退款
                order.refund_audit_time = timezone.now()
                order.save()
                
                # 恢复对应日期的库存
                if order.ticket_type and order.use_date:
                    # 获取对应日期的库存记录
                    date_stock = DateStock.objects.filter(
                        ticket_type=order.ticket_type,
                        use_date=order.use_date
                    ).first()
                    if date_stock:
                        # 恢复库存并减少已售数量
                        date_stock.stock += order.quantity
                        date_stock.sold -= order.quantity
                        date_stock.save()
                
                # 显示成功消息
                messages.success(request, '退款申请已审核通过，订单已退款')
            else:
                # 订单状态不允许退款操作
                messages.error(request, '该订单状态不允许退款操作')
        except Order.DoesNotExist:
            # 订单不存在或不属于该管理员管理的景点
            messages.error(request, '订单不存在或您没有权限操作')
        except Exception as e:
            # 其他错误
            messages.error(request, f'处理退款失败: {str(e)}')
    
    # 重定向到订单管理页面
    return redirect(reverse('ticket:scenic_admin_orders'))


# 景点管理员拒绝退款申请视图函数
@scenic_admin_required
def scenic_admin_refund_reject(request, order_id):
    # 判断请求方法是否为POST（表单提交）
    if request.method == 'POST':
        # 获取当前景点管理员
        admin = request.user
        
        try:
            # 获取该管理员管理的景点
            scenic_spots = ScenicSpot.objects.filter(admin=admin)
            scenic_ids = scenic_spots.values_list('id', flat=True)
            
            # 获取订单信息，确保订单属于该管理员管理的景点
            order = Order.objects.get(id=order_id, scenic_spot__id__in=scenic_ids)
            
            # 只有退款审核中的订单才能被拒绝
            if order.status == 5:
                # 更新订单信息，拒绝退款，恢复为已支付状态
                order.status = 1  # 设置为已支付
                order.refund_audit_time = timezone.now()
                order.save()
                
                # 显示成功消息
                messages.success(request, '退款申请已拒绝，订单已恢复为已支付状态')
            else:
                # 订单状态不是退款审核中，无法拒绝
                messages.error(request, '只有退款审核中的订单才能被拒绝')
        except Order.DoesNotExist:
            # 订单不存在或不属于该管理员管理的景点
            messages.error(request, '订单不存在或您没有权限操作')
        except Exception as e:
            # 其他错误
            messages.error(request, f'拒绝退款失败: {str(e)}')
    
    # 重定向到订单管理页面
    return redirect(reverse('ticket:scenic_admin_orders'))


# 景点管理员查看订单详情视图函数
@scenic_admin_required
def scenic_admin_order_detail(request, order_id):
    # 获取当前景点管理员
    admin = request.user
    
    try:
        # 获取该管理员管理的景点
        scenic_spots = ScenicSpot.objects.filter(admin=admin)
        scenic_ids = scenic_spots.values_list('id', flat=True)
        
        # 获取订单信息，确保订单属于该管理员管理的景点
        order = Order.objects.get(id=order_id, scenic_spot__id__in=scenic_ids)
        
        # 构建上下文数据
        context = {
            'order': order
        }
        
        # 渲染订单详情模板
        return render(request, 'scenic_admin/order_detail.html', context)
    except Order.DoesNotExist:
        # 订单不存在或不属于该管理员管理的景点
        messages.error(request, '订单不存在或您没有权限操作')
        return redirect(reverse('ticket:scenic_admin_orders'))
    except Exception as e:
        # 其他错误
        messages.error(request, f'查看订单详情失败: {str(e)}')
        return redirect(reverse('ticket:scenic_admin_orders'))


# 联系客服视图函数，处理用户联系客服请求
# @login_required装饰器：要求用户必须登录才能访问该视图
@login_required
def contact_service(request):
    # 渲染contact_service.html模板，显示联系客服页面
    return render(request, 'contact_service.html')
