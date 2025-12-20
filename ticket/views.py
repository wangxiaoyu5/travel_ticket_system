# 导入Django的快捷函数，用于渲染模板、重定向和生成URL
from django.shortcuts import render, redirect, reverse
# 导入Django的认证函数，用于用户登录、退出和认证
from django.contrib.auth import authenticate, login, logout
# 导入登录装饰器，用于保护需要登录才能访问的视图
from django.contrib.auth.decorators import login_required
# 导入消息框架，用于向用户显示提示信息
from django.contrib import messages
# 导入自定义模型，用于数据库查询
from .models import ScenicSpot, News, Carousel

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
        'carousels': carousels,          # 轮播图数据
        'announcements': announcements,  # 公告数据
        'latest_news': latest_news,      # 最新资讯数据
        'hot_spots': hot_spots,          # 热门景点数据
    }
    # 渲染index.html模板，将上下文数据传递给模板
    return render(request, 'index.html', context)

# 登录视图函数，处理用户登录请求
def user_login(request):
    # 判断请求方法是否为POST（表单提交）
    if request.method == 'POST':
        # 从POST请求中获取用户名
        username = request.POST.get('username')
        # 从POST请求中获取密码
        password = request.POST.get('password')
        # 使用Django的authenticate函数验证用户名和密码
        user = authenticate(request, username=username, password=password)
        # 如果验证成功，user不为None
        if user is not None:
            # 使用Django的login函数登录用户，创建会话
            login(request, user)
            # 重定向到首页，使用reverse函数根据URL名称生成URL
            return redirect(reverse('index'))
        else:
            # 如果验证失败，使用messages框架向用户显示错误信息
            messages.error(request, '用户名或密码错误')
    # 如果请求方法不是POST，或者验证失败，渲染login.html模板
    return render(request, 'login.html')

# 退出登录视图函数，处理用户退出请求
def user_logout(request):
    # 使用Django的logout函数退出用户，清除会话
    logout(request)
    # 重定向到首页
    return redirect(reverse('index'))

# 个人中心视图函数，处理用户个人中心请求
# @login_required装饰器：要求用户必须登录才能访问该视图
@login_required
def personal_center(request):
    # 渲染personal_center.html模板
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
        spots = spots.filter(name__icontains=search_keyword) | spots.filter(address__icontains=search_keyword) | spots.filter(region__icontains=search_keyword)
    
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
    # 渲染scenic_spot_detail.html模板，将景点详情数据传递给模板
    return render(request, 'scenic_spot_detail.html', {'spot': spot})

# 资讯公告列表视图函数，处理资讯公告列表页请求
def news_list(request):
    # 从数据库中获取所有资讯公告，按创建时间倒序排列
    news = News.objects.all()
    # 渲染news_list.html模板，将资讯公告数据传递给模板
    return render(request, 'news_list.html', {'news': news})

# 资讯公告详情视图函数，处理单个资讯公告的详情页请求
# news_id: 资讯ID，从URL中获取
def news_detail(request, news_id):
    # 根据资讯ID从数据库中获取单个资讯公告信息
    news_item = News.objects.get(id=news_id)
    # 渲染news_detail.html模板，将资讯详情数据传递给模板
    return render(request, 'news_detail.html', {'news': news_item})

# 购物车视图函数，处理用户购物车请求
# @login_required装饰器：要求用户必须登录才能访问该视图
@login_required
def cart(request):
    # 渲染cart.html模板
    return render(request, 'cart.html')

# 订单中心视图函数，处理用户订单中心请求
# @login_required装饰器：要求用户必须登录才能访问该视图
@login_required
def order_center(request):
    # 渲染order_center.html模板
    return render(request, 'order_center.html')
