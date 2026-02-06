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
    
    # 注册URL：/register/ 映射到views.register视图函数，URL名称为'register'
    path('register/', views.register, name='register'),
    
    # 退出登录URL：/logout/ 映射到views.user_logout视图函数，URL名称为'logout'
    path('logout/', views.user_logout, name='logout'),
    
    # 忘记密码URL：/forgot_password/ 映射到views.forgot_password视图函数，URL名称为'forgot_password'
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    
    # 个人中心URL：/personal_center/ 映射到views.personal_center视图函数，URL名称为'personal_center'
    path('personal_center/', views.personal_center, name='personal_center'),
    
    # 修改密码URL：/change_password/ 映射到views.change_password视图函数，URL名称为'change_password'
    path('change_password/', views.change_password, name='change_password'),
    
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
    
    # 取消订单URL：/cancel_order/[订单ID]/ 映射到views.cancel_order视图函数
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    
    # 申请退款URL：/apply_refund/[订单ID]/ 映射到views.apply_refund视图函数
    path('apply_refund/<int:order_id>/', views.apply_refund, name='apply_refund'),
    
    # 联系客服URL：/contact_service/ 映射到views.contact_service视图函数
    path('contact_service/', views.contact_service, name='contact_service'),
    
    # 购票页面URL：/buy_ticket/[景点ID]/ 映射到views.buy_ticket视图函数
    path('buy_ticket/<int:spot_id>/', views.buy_ticket, name='buy_ticket'),
    
    # 支付页面URL：/payment/[订单ID]/ 映射到views.payment视图函数
    path('payment/<int:order_id>/', views.payment, name='payment'),
    
    # 批量支付URL：/batch_payment/ 映射到views.batch_payment视图函数
    path('batch_payment/', views.batch_payment, name='batch_payment'),
    
    # 确认支付URL：/confirm_payment/ 映射到views.confirm_payment视图函数
    path('confirm_payment/', views.confirm_payment, name='confirm_payment'),
    
    # 删除购物车项URL：/cart/delete/<int:cart_id>/ 映射到views.delete_cart_item视图函数
    path('cart/delete/<int:cart_id>/', views.delete_cart_item, name='delete_cart_item'),
    
    # 移入收藏URL：/cart/add_to_collection/<int:cart_id>/ 映射到views.add_to_collection视图函数
    path('cart/add_to_collection/<int:cart_id>/', views.add_to_collection, name='add_to_collection'),
    
    # 天气检查页面URL：/weather_check/[订单ID]/ 映射到views.weather_check视图函数
    path('weather_check/<int:order_id>/', views.weather_check, name='weather_check'),

    # 获取景点列表API：/api/scenic_spots/ 映射到views.get_scenic_spots_api视图函数
    path('api/scenic_spots/', views.get_scenic_spots_api, name='get_scenic_spots_api'),
    
    # 获取门票库存API：/api/get_ticket_stocks/ 映射到views.get_ticket_stocks视图函数
    path('api/get_ticket_stocks/', views.get_ticket_stocks, name='get_ticket_stocks'),
    
    # 景点管理员后台URL
    # 景点管理景点信息管理
    path('scenic_admin/scenic_spots/', views.scenic_admin_scenic_spots, name='scenic_admin_scenic_spots'),
    # 景点编辑
    path('scenic_admin/scenic_spot/edit/<int:spot_id>/', views.scenic_admin_edit_scenic_spot, name='scenic_admin_edit_scenic_spot'),
    # 景点新增
    path('scenic_admin/scenic_spot/add/', views.scenic_admin_add_scenic_spot, name='scenic_admin_add_scenic_spot'),
    # 景点批量操作
    path('scenic_admin/scenic_spots/batch_operate/', views.scenic_admin_batch_operate_scenic_spots, name='scenic_admin_batch_operate_scenic_spots'),
    # 门票类型管理
    path('scenic_admin/ticket_types/', views.scenic_admin_ticket_types, name='scenic_admin_ticket_types'),
    # 新增门票类型
    path('scenic_admin/ticket_type/add/', views.scenic_admin_add_ticket_type, name='scenic_admin_add_ticket_type'),
    # 编辑门票类型
    path('scenic_admin/ticket_type/edit/<int:ticket_id>/', views.scenic_admin_edit_ticket_type, name='scenic_admin_edit_ticket_type'),
    # 门票类型批量操作
    path('scenic_admin/ticket_types/batch_operate/', views.scenic_admin_batch_operate_ticket_types, name='scenic_admin_batch_operate_ticket_types'),
    # 更新日期库存
    path('scenic_admin/update_date_stock/', views.scenic_admin_update_date_stock, name='scenic_admin_update_date_stock'),
    # 订单管理
    path('scenic_admin/orders/', views.scenic_admin_orders, name='scenic_admin_orders'),
    # 订单退款（审核通过）
    path('scenic_admin/order/refund/<int:order_id>/', views.scenic_admin_refund_order, name='scenic_admin_refund_order'),
    # 订单退款（审核拒绝）
    path('scenic_admin/order/refund/reject/<int:order_id>/', views.scenic_admin_refund_reject, name='scenic_admin_refund_reject'),
    # 订单详情
    path('scenic_admin/order/detail/<int:order_id>/', views.scenic_admin_order_detail, name='scenic_admin_order_detail'),
    # 留言管理
    path('scenic_admin/comments/', views.scenic_admin_comments, name='scenic_admin_comments'),
    # 回复留言
    path('scenic_admin/comment/reply/<int:comment_id>/', views.scenic_admin_reply_comment, name='scenic_admin_reply_comment'),
    # 删除留言
    path('scenic_admin/comment/delete/<int:comment_id>/', views.scenic_admin_delete_comment, name='scenic_admin_delete_comment'),
    # 数据统计
    path('scenic_admin/statistics/', views.scenic_admin_statistics, name='scenic_admin_statistics'),
    # 账户信息管理
    path('scenic_admin/account/', views.scenic_admin_account, name='scenic_admin_account'),
    # 资讯公告管理
    path('scenic_admin/news_announcements/', views.scenic_admin_news_announcements, name='scenic_admin_news_announcements'),
    # 公告管理
    path('scenic_admin/announcements/', views.scenic_admin_announcements, name='scenic_admin_announcements'),
    # 新增公告
    path('scenic_admin/announcement/add/', views.scenic_admin_add_announcement, name='scenic_admin_add_announcement'),
    # 编辑公告
    path('scenic_admin/announcement/edit/<int:announcement_id>/', views.scenic_admin_edit_announcement, name='scenic_admin_edit_announcement'),
    # 删除公告
    path('scenic_admin/announcement/delete/<int:announcement_id>/', views.scenic_admin_delete_announcement, name='scenic_admin_delete_announcement'),
    # 批量删除公告
    path('scenic_admin/announcements/batch_delete/', views.scenic_admin_batch_delete_announcements, name='scenic_admin_batch_delete_announcements'),
    # 资讯管理
    path('scenic_admin/news/', views.scenic_admin_news, name='scenic_admin_news'),
    # 新增资讯
    path('scenic_admin/news/add/', views.scenic_admin_add_news, name='scenic_admin_add_news'),
    # 编辑资讯
    path('scenic_admin/news/edit/<int:news_id>/', views.scenic_admin_edit_news, name='scenic_admin_edit_news'),
    # 删除资讯
    path('scenic_admin/news/delete/<int:news_id>/', views.scenic_admin_delete_news, name='scenic_admin_delete_news'),
    # 批量删除资讯
    path('scenic_admin/news/batch_delete/', views.scenic_admin_batch_delete_news, name='scenic_admin_batch_delete_news'),
    
    # 平台管理员URL
    # 用户管理
    path('admin/users/', views.admin_user_list, name='admin_user_list'),
    path('admin/user/add/', views.admin_add_user, name='admin_add_user'),
    path('admin/user/edit/<int:user_id>/', views.admin_edit_user, name='admin_edit_user'),
    path('admin/user/delete/<int:user_id>/', views.admin_delete_user, name='admin_delete_user'),
    path('admin/users/batch_delete/', views.admin_batch_delete_users, name='admin_batch_delete_users'),
    # 景点分类管理
    path('admin/categories/', views.admin_category_list, name='admin_category_list'),
    path('admin/category/add/', views.admin_add_category, name='admin_add_category'),
    path('admin/category/edit/<int:category_id>/', views.admin_edit_category, name='admin_edit_category'),
    path('admin/category/delete/<int:category_id>/', views.admin_delete_category, name='admin_delete_category'),
    # 地区分类管理
    path('admin/regions/', views.admin_region_list, name='admin_region_list'),
    path('admin/region/add/', views.admin_add_region, name='admin_add_region'),
    path('admin/region/edit/<int:region_id>/', views.admin_edit_region, name='admin_edit_region'),
    path('admin/region/delete/<int:region_id>/', views.admin_delete_region, name='admin_delete_region'),
    # 景点管理
    path('admin/scenic_spots/', views.admin_scenic_list, name='admin_scenic_list'),
    path('admin/scenic_spot/add/', views.admin_add_scenic, name='admin_add_scenic'),
    path('admin/scenic_spot/edit/<int:spot_id>/', views.admin_edit_scenic, name='admin_edit_scenic'),
    path('admin/scenic_spot/delete/<int:spot_id>/', views.admin_delete_scenic, name='admin_delete_scenic'),
    path('admin/scenic_spots/batch_delete/', views.admin_batch_delete_scenic, name='admin_batch_delete_scenic'),
    # 订单管理
    path('admin/orders/', views.admin_order_list, name='admin_order_list'),
    path('admin/order/delete/<int:order_id>/', views.admin_delete_order, name='admin_delete_order'),
    # 留言管理
    path('admin/comments/', views.admin_comment_list, name='admin_comment_list'),
    path('admin/comment/reply/<int:comment_id>/', views.admin_reply_comment, name='admin_reply_comment'),
    path('admin/comment/delete/<int:comment_id>/', views.admin_delete_comment, name='admin_delete_comment'),
    # 公告管理
    path('admin/announcements/', views.admin_announcement_list, name='admin_announcement_list'),
    path('admin/announcement/add/', views.admin_add_announcement, name='admin_add_announcement'),
    path('admin/announcement/edit/<int:announcement_id>/', views.admin_edit_announcement, name='admin_edit_announcement'),
    path('admin/announcement/delete/<int:announcement_id>/', views.admin_delete_announcement, name='admin_delete_announcement'),
    # 资讯管理
    path('admin/news/', views.admin_news_list, name='admin_news_list'),
    path('admin/news/add/', views.admin_add_news, name='admin_add_news'),
    path('admin/news/edit/<int:news_id>/', views.admin_edit_news, name='admin_edit_news'),
    path('admin/news/delete/<int:news_id>/', views.admin_delete_news, name='admin_delete_news'),

    # 密码管理
    path('admin/password/change/', views.admin_password_change, name='admin_password_change'),
]