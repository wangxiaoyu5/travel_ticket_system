# 导入Django的path函数，用于定义URL路由
from django.urls import path
# 导入当前应用的视图模块，用于将URL映射到视图函数
from . import views

# 定义应用的命名空间，用于区分不同应用的URL名称
# 使用时格式为：{% url 'ticket:index' %} 或 reverse('ticket:index')
app_name = 'ticket'

# URL路由列表，定义了应用的所有URL映射规则
urlpatterns = [
    # 首页URL：空路径映射到views.index视图函数，URL名称为'index'
    path('', views.index, name='index'),
    
    # 登录URL：/login/ 映射到views.user_login视图函数，URL名称为'login'
    path('login/', views.user_login, name='login'),
    
    # 退出登录URL：/logout/ 映射到views.user_logout视图函数，URL名称为'logout'
    path('logout/', views.user_logout, name='logout'),
    
    # 个人中心URL：/personal_center/ 映射到views.personal_center视图函数，URL名称为'personal_center'
    path('personal_center/', views.personal_center, name='personal_center'),
    
    # 景点列表URL：/scenic_spots/ 映射到views.scenic_spots视图函数，URL名称为'scenic_spots'
    path('scenic_spots/', views.scenic_spots, name='scenic_spots'),
    
    # 景点详情URL：/scenic_spot/[景点ID]/ 映射到views.scenic_spot_detail视图函数
    # <int:spot_id> 是路径参数，将URL中的数字转换为整数并传递给视图函数的spot_id参数
    # URL名称为'scenic_spot_detail'
    path('scenic_spot/<int:spot_id>/', views.scenic_spot_detail, name='scenic_spot_detail'),
    
    # 资讯列表URL：/news/ 映射到views.news_list视图函数，URL名称为'news_list'
    path('news/', views.news_list, name='news_list'),
    
    # 资讯详情URL：/news/[资讯ID]/ 映射到views.news_detail视图函数
    # <int:news_id> 是路径参数，将URL中的数字转换为整数并传递给视图函数的news_id参数
    # URL名称为'news_detail'
    path('news/<int:news_id>/', views.news_detail, name='news_detail'),
    
    # 购物车URL：/cart/ 映射到views.cart视图函数，URL名称为'cart'
    path('cart/', views.cart, name='cart'),
    
    # 订单中心URL：/order_center/ 映射到views.order_center视图函数，URL名称为'order_center'
    path('order_center/', views.order_center, name='order_center'),
]