# 导入Django的快捷函数，用于渲染模板、重定向和生成URL
# 导入消息框架，用于向用户显示提示信息
from django.contrib import messages
# 导入Django的认证函数，用于用户登录、退出和认证
from django.contrib.auth import login, logout
# 导入登录装饰器，用于保护需要登录才能访问的视图
from django.contrib.auth.decorators import login_required
# 导入Django ORM模型模块
from django.db import models
# 导入JsonResponse，用于返回JSON响应
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse

# 导入自定义模型，用于数据库查询
from .models import ScenicSpot, News, Carousel, User, Cart, Order, ScenicSpotComment, TicketType


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
    # 判断请求方法是否为POST（表单提交）
    if request.method == 'POST':
        # 从POST请求中获取邮箱
        email = request.POST.get('email')
        # 从POST请求中获取密码
        password = request.POST.get('password')
        # 从POST请求中获取角色
        role = request.POST.get('role')
        # 从POST请求中获取景点ID
        scenic_spot_id = request.POST.get('scenic_spot')

        try:
            # 根据邮箱查找用户
            user = User.objects.get(email=email)
            # 验证密码
            if user.check_password(password):
                # 验证角色是否匹配
                if str(user.role) == role:
                    # 使用Django的login函数登录用户，创建会话
                    login(request, user)
                    # 根据用户角色重定向到不同页面
                    if user.role == 2:  # 网站管理员
                        return redirect(reverse('ticket:admin_index'))
                    elif user.role == 1:  # 景点管理员
                        return redirect(reverse('ticket:scenic_admin_index'))
                    else:  # 游客
                        return redirect(reverse('ticket:index'))
                else:
                    # 角色不匹配
                    messages.error(request, '角色不匹配')
            else:
                # 密码错误
                messages.error(request, '邮箱或密码错误')
        except User.DoesNotExist:
            # 用户不存在
            messages.error(request, '邮箱或密码错误')
    # 如果请求方法不是POST，或者验证失败，渲染login.html模板
    return render(request, 'login.html')


# 退出登录视图函数，处理用户退出请求
def user_logout(request):
    # 使用Django的logout函数退出用户，清除会话
    logout(request)
    # 重定向到首页，使用reverse函数根据URL名称生成URL，需要包含命名空间
    return redirect(reverse('ticket:index'))


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


# 景点管理员控制台视图
def scenic_admin_index(request):
    # 导入日期处理模块
    from datetime import date

    # 获取当前景点管理员
    admin = request.user

    # 从数据库获取该管理员管理的景点
    scenic_spots = ScenicSpot.objects.filter(admin=admin)
    scenic_count = scenic_spots.count()

    # 获取景点ID列表，用于后续查询
    scenic_ids = scenic_spots.values_list('id', flat=True)

    # 今日订单数：查询今天创建的订单
    today = date.today()
    today_orders = Order.objects.filter(scenic_spot__id__in=scenic_ids, created_at__date=today).count()

    # 总销售额：计算所有已支付订单的总价之和
    total_sales = Order.objects.filter(scenic_spot__id__in=scenic_ids, status=1).aggregate(
        total=models.Sum('total_price')
    )['total'] or 0

    # 待处理留言：获取未回复的留言
    pending_comments = ScenicSpotComment.objects.filter(scenic_spot__id__in=scenic_ids, is_replied=False).order_by(
        '-created_at')[:2]

    # 最近订单：获取最新的2个订单
    recent_orders = Order.objects.filter(scenic_spot__id__in=scenic_ids).order_by('-created_at')[:2]

    # 构建上下文数据
    context = {
        'scenic_count': scenic_count,
        'today_orders': today_orders,
        'total_sales': total_sales,
        'pending_comments': pending_comments,
        'recent_orders': recent_orders
    }

    return render(request, 'scenic_admin/index.html', context)


# 景点信息管理视图
@scenic_admin_required
def scenic_admin_scenic_spots(request):
    # 获取当前景点管理员
    admin = request.user

    # 从数据库获取该管理员管理的景点
    scenic_spots = ScenicSpot.objects.filter(admin=admin)

    # 构建上下文数据
    context = {
        'scenic_spots': scenic_spots
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
        image = request.FILES.get('image')
        address = request.POST.get('address')
        opening_hours = request.POST.get('opening_hours')
        is_hot = request.POST.get('is_hot') == 'on'
        region = request.POST.get('region')
        category = request.POST.get('category')
        tags = request.POST.get('tags')
        total_tickets = request.POST.get('total_tickets')

        # 表单验证
        if not name or not description or not price or not address or not opening_hours:
            messages.error(request, '请填写所有必填字段')
            return render(request, 'scenic_admin/edit_scenic_spot.html', {'scenic_spot': scenic_spot})

        try:
            # 更新景点信息
            scenic_spot.name = name
            scenic_spot.description = description
            scenic_spot.price = float(price)
            scenic_spot.address = address
            scenic_spot.opening_hours = opening_hours
            scenic_spot.is_hot = is_hot
            scenic_spot.region = region
            scenic_spot.category = category
            scenic_spot.tags = tags
            scenic_spot.total_tickets = int(total_tickets) if total_tickets else 0

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
        image = request.FILES.get('image')
        address = request.POST.get('address')
        opening_hours = request.POST.get('opening_hours')
        is_hot = request.POST.get('is_hot') == 'on'
        region = request.POST.get('region')
        category = request.POST.get('category')
        tags = request.POST.get('tags')
        total_tickets = request.POST.get('total_tickets')

        # 表单验证
        if not name or not description or not price or not address or not opening_hours or not image:
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
                opening_hours=opening_hours,
                is_hot=is_hot,
                region=region,
                category=category,
                tags=tags,
                total_tickets=int(total_tickets) if total_tickets else 0
            )

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


# 套票管理视图
@scenic_admin_required
def scenic_admin_package_tickets(request):
    return render(request, 'scenic_admin/package_tickets.html')


# 新增套票视图
@scenic_admin_required
def scenic_admin_add_package_ticket(request):
    return render(request, 'scenic_admin/add_package_ticket.html')


# 门票类型管理视图
@scenic_admin_required
def scenic_admin_ticket_types(request):
    return render(request, 'scenic_admin/ticket_types.html')


# 订单管理视图
@scenic_admin_required
def scenic_admin_orders(request):
    # 获取当前景点管理员
    admin = request.user

    # 从数据库获取该管理员管理的景点
    scenic_spots = ScenicSpot.objects.filter(admin=admin)

    # 获取景点ID列表，用于后续查询
    scenic_ids = scenic_spots.values_list('id', flat=True)

    # 从数据库获取该管理员管理的景点的订单
    orders = Order.objects.filter(scenic_spot__id__in=scenic_ids).order_by('-created_at')

    # 构建上下文数据
    context = {
        'orders': orders
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

    # 从数据库获取该管理员管理的景点的留言
    comments = ScenicSpotComment.objects.filter(scenic_spot__id__in=scenic_ids).order_by('-created_at')

    # 构建上下文数据
    context = {
        'comments': comments
    }

    return render(request, 'scenic_admin/comments.html', context)


# 数据统计视图
@scenic_admin_required
def scenic_admin_statistics(request):
    return render(request, 'scenic_admin/statistics.html')


# 账户信息管理视图
@scenic_admin_required
def scenic_admin_account(request):
    return render(request, 'scenic_admin/account.html')


# 资讯公告管理视图
@scenic_admin_required
def scenic_admin_news_announcements(request):
    return render(request, 'scenic_admin/news_announcements.html')


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

    # 构建上下文数据
    context = {
        'users': users,
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


# 景点管理视图
@admin_required
def admin_scenic_list(request):
    # 获取请求参数中的搜索关键词
    search_keyword = request.GET.get('search', '')

    # 基础查询集
    scenic_spots = ScenicSpot.objects.all()

    # 根据搜索关键词筛选景点
    if search_keyword:
        scenic_spots = scenic_spots.filter(
            models.Q(name__icontains=search_keyword) |
            models.Q(address__icontains=search_keyword) |
            models.Q(region__icontains=search_keyword)
        )

    # 统计不同状态的景点数量
    total_scenic_spots = ScenicSpot.objects.count()
    hot_spots = ScenicSpot.objects.filter(is_hot=True).count()
    recommended_spots = ScenicSpot.objects.filter(is_hot=True).count()  # 可以根据实际字段调整

    # 获取所有地区（用于筛选）
    regions = ScenicSpot.objects.values_list('region', flat=True).distinct()

    # 景点分类选项
    categories = ScenicSpot.CATEGORY_CHOICES

    # 构建上下文数据
    context = {
        'scenic_spots': scenic_spots,
        'total_scenic_spots': total_scenic_spots,
        'hot_spots': hot_spots,
        'recommended_spots': recommended_spots,
        'regions': regions,
        'categories': categories,
        'search_keyword': search_keyword
    }

    return render(request, 'admin/scenic_list.html', context)


# 删除景点视图
@admin_required
def admin_delete_scenic(request, spot_id):
    if request.method == 'POST':
        try:
            # 根据spot_id从数据库获取景点
            scenic_spot = ScenicSpot.objects.get(id=spot_id)
            
            # 删除景点
            scenic_spot.delete()
            
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
            return render(request, 'admin/add_scenic.html')

        try:
            # 创建新景点
            scenic_spot = ScenicSpot.objects.create(
                name=name,
                region=region,
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

            # 显示成功消息
            messages.success(request, '景点添加成功')

            # 重定向到景点列表页面
            return redirect(reverse('ticket:admin_scenic_list'))
        except Exception as e:
            # 显示错误消息
            messages.error(request, f'添加景点失败: {str(e)}')
            return render(request, 'admin/add_scenic.html')

    # GET请求，渲染新增景点表单
    return render(request, 'admin/add_scenic.html')


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
            return render(request, 'admin/edit_scenic.html', {'scenic_spot': scenic_spot})

        try:
            # 更新景点信息
            scenic_spot.name = name
            scenic_spot.region = region
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
            return render(request, 'admin/edit_scenic.html', {'scenic_spot': scenic_spot})

    # GET请求，渲染编辑景点表单，传递当前景点数据
    return render(request, 'admin/edit_scenic.html', {'scenic_spot': scenic_spot})


# 地区管理视图
@admin_required
def admin_region_list(request):
    # 获取所有不重复的地区列表
    regions = ScenicSpot.objects.values_list('region', flat=True).distinct().order_by('region')

    # 统计每个地区的景点数量
    region_counts = {}
    for region in regions:
        region_counts[region] = ScenicSpot.objects.filter(region=region).count()

    # 构建上下文数据
    context = {
        'regions': regions,
        'region_counts': region_counts
    }

    return render(request, 'admin/region_list.html', context)


# 订单管理视图
@admin_required
def admin_order_list(request):
    # 获取请求参数中的订单状态筛选条件
    status_filter = request.GET.get('status', '')
    # 获取请求参数中的搜索关键词
    search_keyword = request.GET.get('search', '')

    # 基础查询集：包含关联的用户和景点信息，使用select_related优化查询
    orders = Order.objects.select_related('user', 'scenic_spot', 'ticket_type')

    # 根据订单状态筛选
    if status_filter:
        orders = orders.filter(status=status_filter)

    # 根据搜索关键词筛选：可搜索订单号、用户邮箱或景点名称
    if search_keyword:
        orders = orders.filter(
            models.Q(order_number__icontains=search_keyword) |
            models.Q(user__email__icontains=search_keyword) |
            models.Q(scenic_spot__name__icontains=search_keyword)
        )

    # 统计不同状态的订单数量
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status=0).count()
    paid_orders = Order.objects.filter(status=1).count()
    canceled_orders = Order.objects.filter(status=2).count()
    used_orders = Order.objects.filter(status=3).count()
    refunded_orders = Order.objects.filter(status=4).count()

    # 订单状态选项
    status_choices = Order.STATUS_CHOICES

    # 构建上下文数据
    context = {
        'orders': orders,
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

    # 基础查询集：包含关联的用户和景点信息，使用select_related优化查询
    comments = ScenicSpotComment.objects.select_related('user', 'scenic_spot')

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

    # 构建上下文数据
    context = {
        'comments': comments,
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

    # 构建上下文数据
    context = {
        'announcements': announcements,
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

    # 构建上下文数据
    context = {
        'news_list': news_list,
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


# 系统设置视图
@admin_required
def admin_system_settings(request):
    return render(request, 'admin/system_settings.html')


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
    # 判断请求方法是否为POST（表单提交）
    if request.method == 'POST':
        # 获取当前登录用户
        user = request.user

        # 更新用户信息
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        user.gender = request.POST.get('gender')

        # 处理出生日期
        birthdate_str = request.POST.get('birthdate')
        if birthdate_str:
            user.birthdate = birthdate_str
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

    # 如果请求方法不是POST，渲染个人中心页面
    return render(request, 'personal_center.html')


# 景点信息列表视图
def scenic_spots(request):
    # 获取搜索关键词
    search_keyword = request.GET.get('search', '')
    # 获取地区筛选条件
    region_filter = request.GET.get('region', '')
    # 获取分类筛选条件
    category_filter = request.GET.get('category', '')

    # 基础查询集
    spots = ScenicSpot.objects.all()

    # 根据搜索关键词筛选
    if search_keyword:
        spots = spots.filter(name__icontains=search_keyword) | spots.filter(
            address__icontains=search_keyword) | spots.filter(region__icontains=search_keyword)

    # 根据地区筛选
    if region_filter:
        spots = spots.filter(region=region_filter)

    # 根据分类筛选
    if category_filter:
        spots = spots.filter(category=category_filter)

    # 获取所有地区（用于筛选）
    regions = ScenicSpot.objects.values_list('region', flat=True).distinct()
    # 获取所有分类（用于筛选）
    categories = ScenicSpot.CATEGORY_CHOICES

    # 预处理景点数据，将tags转换为列表
    spots_with_tags = []
    for spot in spots:
        # 将tags字符串分割为列表
        tags_list = [tag.strip() for tag in spot.tags.split(',')]
        # 将处理后的tags列表添加到spot对象中
        spot.tags_list = tags_list
        spots_with_tags.append(spot)

    # 构建上下文
    context = {
        'spots': spots_with_tags,
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
    # 根据景点ID从数据库中获取单个景点信息
    spot = ScenicSpot.objects.get(id=spot_id)
    # 将tags字符串分割为列表
    tags_list = [tag.strip() for tag in spot.tags.split(',')]
    # 获取该景点的所有留言，按创建时间倒序排列
    comments = ScenicSpotComment.objects.filter(scenic_spot=spot).order_by('-created_at')
    
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

    # 根据筛选条件获取资讯公告，按创建时间倒序排列
    if filter_type == 'news':
        news = News.objects.filter(is_announcement=False)
    elif filter_type == 'announcement':
        news = News.objects.filter(is_announcement=True)
    else:
        news = News.objects.all()

    # 渲染news_list.html模板，将资讯公告数据和筛选类型传递给模板
    return render(request, 'news_list.html', {'news': news, 'filter_type': filter_type})


# 资讯公告详情视图函数，处理单个资讯公告的详情页请求
# news_id: 资讯ID，从URL中获取
def news_detail(request, news_id):
    # 根据资讯ID从数据库中获取单个资讯公告信息
    news_item = News.objects.get(id=news_id)
    # 渲染news_detail.html模板，将资讯详情数据传递给模板
    return render(request, 'news_detail.html', {'news': news_item})

# 购票页面视图函数，处理景点购票请求
# spot_id: 景点ID，从URL中获取
def buy_ticket(request, spot_id):
    # 根据景点ID从数据库中获取景点信息
    spot = ScenicSpot.objects.get(id=spot_id)
    # 获取该景点的所有激活状态的门票类型
    ticket_types = TicketType.objects.filter(scenic_spot=spot, is_active=True)
    # 分类门票类型：单票和套票
    single_tickets = ticket_types.filter(type='single')
    package_tickets = ticket_types.filter(type='package')
    
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
        
        # 检查库存
        if ticket_type.stock < quantity:
            # 库存不足，显示错误信息
            messages.error(request, f'门票库存不足，当前库存仅剩 {ticket_type.stock} 张')
            # 返回购票页面时保留用户之前的选择
            return render(request, 'buy_ticket.html', {
                'spot': spot,
                'ticket_types': ticket_types,
                'single_tickets': single_tickets,
                'package_tickets': package_tickets,
                'selected_use_date': use_date,
                'selected_quantity': quantity
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
                
                # 减少库存
                ticket_type.stock -= quantity
                ticket_type.save()
                
                # 跳转到支付页面
                return redirect(reverse('ticket:payment', kwargs={'order_id': order.id}))
            else:
                # 用户未登录，跳转到登录页面
                messages.error(request, '请先登录')
                return redirect(reverse('ticket:login'))
        elif action == 'add_to_cart':
            # 加入购物车：添加到用户购物车
            if request.user.is_authenticated:
                # 创建购物车记录
                Cart.objects.create(
                    user=request.user,
                    scenic_spot=spot,
                    ticket_type=ticket_type,
                    use_date=use_date,
                    quantity=quantity
                )
                messages.success(request, '已成功加入购物车')
                return redirect(reverse('ticket:cart'))
            else:
                # 用户未登录，跳转到登录页面
                messages.error(request, '请先登录')
                return redirect(reverse('ticket:login'))
    
    # 渲染buy_ticket.html模板，将景点和门票类型数据传递给模板
    return render(request, 'buy_ticket.html', {
        'spot': spot,
        'ticket_types': ticket_types,
        'single_tickets': single_tickets,
        'package_tickets': package_tickets
    })

# 支付页面视图函数，处理订单支付请求
# order_id: 订单ID，从URL中获取
def payment(request, order_id):
    # 根据订单ID从数据库中获取订单信息
    order = Order.objects.get(id=order_id)
    
    # 处理支付提交
    if request.method == 'POST':
        # 模拟支付成功
        order.status = 1  # 设置订单状态为已支付
        order.save()
        
        # 显示支付成功消息
        messages.success(request, '支付成功！')
        
        # 跳转到订单中心
        return redirect(reverse('ticket:order_center'))
    
    # 渲染payment.html模板，将订单数据传递给模板
    return render(request, 'payment.html', {
        'order': order
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
        
        # 检查是否选择了商品
        if not selected_item_ids:
            messages.error(request, '请选择要购买的商品')
            return redirect(reverse('ticket:cart'))
        
        # 遍历选中的购物车项目，创建订单
        orders = []
        for item_id in selected_item_ids:
            try:
                # 获取购物车项目
                cart_item = Cart.objects.get(id=item_id, user=request.user)
                
                # 生成订单号
                import datetime
                import uuid
                order_number = f"ORD{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:6].upper()}"
                
                # 计算订单总价
                total_price = cart_item.ticket_type.price * cart_item.quantity
                
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
                
                orders.append(order)
                
                # 从购物车中删除已购买的项目
                cart_item.delete()
            except Cart.DoesNotExist:
                messages.error(request, '购物车项目不存在或已被删除')
                continue
        
        if orders:
            # 如果只有一个订单，直接跳转到支付页面
            if len(orders) == 1:
                return redirect(reverse('ticket:payment', kwargs={'order_id': orders[0].id}))
            else:
                # 多个订单，跳转到订单中心
                messages.success(request, f'已成功创建 {len(orders)} 个订单')
                return redirect(reverse('ticket:order_center'))
        else:
            messages.error(request, '没有成功创建订单，请重新尝试')
            return redirect(reverse('ticket:cart'))

    # 渲染cart.html模板，将购物车数据传递给模板
    return render(request, 'cart.html', {'cart_items': cart_items})


# 订单中心视图函数，处理用户订单中心请求
# @login_required装饰器：要求用户必须登录才能访问该视图
@login_required
def order_center(request):
    # 获取当前登录用户的所有订单
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    # 渲染order_center.html模板，将订单数据传递给模板
    return render(request, 'order_center.html', {'orders': orders})


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
                # 恢复门票库存
                if order.ticket_type:
                    order.ticket_type.stock += order.quantity
                    order.ticket_type.save()
                
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


# 联系客服视图函数，处理用户联系客服请求
# @login_required装饰器：要求用户必须登录才能访问该视图
@login_required
def contact_service(request):
    # 渲染contact_service.html模板，显示联系客服页面
    return render(request, 'contact_service.html')
