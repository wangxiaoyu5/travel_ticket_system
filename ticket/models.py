# 导入Django的模型模块
from django.db import models
# 导入Django的用户抽象模型，用于自定义用户模型
from django.contrib.auth.models import AbstractUser

# 自定义用户模型，继承自AbstractUser，支持三种角色
class User(AbstractUser):
    # 定义角色选择元组，用于限制角色取值范围
    # 0-游客，1-景点管理员，2-网站管理员
    ROLE_CHOICES = (
        (0, '游客'),        # 普通用户，可浏览景点、购买门票
        (1, '景点管理员'),  # 可管理自己负责的景点信息
        (2, '网站管理员'),  # 可管理所有系统资源
    )
    # 角色字段，使用IntegerField存储，默认值为0（游客）
    role = models.IntegerField(choices=ROLE_CHOICES, default=0, verbose_name='角色')
    # 头像字段，使用ImageField存储，允许为空，上传路径为'avatars/'
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='头像')
    # 手机号字段，使用CharField存储，最大长度11，允许为空
    phone = models.CharField(max_length=11, null=True, blank=True, verbose_name='手机号')
    # 显式定义objects管理器，解决IDE警告
    objects = models.Manager()
    
    # 模型元数据配置
    class Meta:
        verbose_name = '用户'           # 模型的可读名称
        verbose_name_plural = verbose_name  # 复数形式的可读名称

# 景点信息模型，存储所有景点的详细信息
class ScenicSpot(models.Model):
    # 景点分类选择
    CATEGORY_CHOICES = (
        ('natural', '自然风光类'),
        ('historical', '历史遗迹类'),
        ('folklore', '民俗文化类'),
        ('modern', '现代都市类'),
        ('leisure', '休闲度假类'),
        ('theme', '主题乐园类'),
        ('religious', '宗教文化类'),
        ('rural', '农业乡村类'),
    )
    
    # 景点名称，使用CharField存储，最大长度100
    name = models.CharField(max_length=100, verbose_name='景点名称')
    # 景点描述，使用TextField存储，支持长文本
    description = models.TextField(verbose_name='景点描述')
    # 门票价格，使用DecimalField存储，最大10位数字，2位小数
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='门票价格')
    # 景点图片，使用ImageField存储，上传路径为'scenic_spots/'
    image = models.ImageField(upload_to='scenic_spots/', verbose_name='景点图片')
    # 景点地址，使用CharField存储，最大长度200
    address = models.CharField(max_length=200, verbose_name='景点地址')
    # 开放时间，使用CharField存储，最大长度100
    opening_hours = models.CharField(max_length=100, verbose_name='开放时间')
    # 是否热门景点，使用BooleanField存储，默认值为False
    is_hot = models.BooleanField(default=False, verbose_name='是否热门')
    # 景点地区，使用CharField存储，最大长度50
    region = models.CharField(max_length=50, default='全国', verbose_name='地区')
    # 景点分类，使用CharField存储，最大长度20，选择项来自CATEGORY_CHOICES
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='natural', verbose_name='分类')
    # 景点标签，使用CharField存储，最大长度100，用于存储多个标签，以逗号分隔
    tags = models.CharField(max_length=100, default='热门', verbose_name='标签', help_text='多个标签用逗号分隔')
    # 创建时间，使用DateTimeField存储，自动添加当前时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 更新时间，使用DateTimeField存储，自动更新为当前时间
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    # 显式定义objects管理器，解决IDE警告
    objects = models.Manager()
    
    # 模型元数据配置
    class Meta:
        verbose_name = '景点信息'       # 模型的可读名称
        verbose_name_plural = verbose_name  # 复数形式的可读名称

# 资讯公告模型，存储系统公告和旅游资讯
class News(models.Model):
    # 资讯标题，使用CharField存储，最大长度200
    title = models.CharField(max_length=200, verbose_name='资讯标题')
    # 资讯内容，使用TextField存储，支持长文本
    content = models.TextField(verbose_name='资讯内容')
    # 是否为公告，使用BooleanField存储，默认值为False
    is_announcement = models.BooleanField(default=False, verbose_name='是否为公告')
    # 资讯图片，使用ImageField存储，允许为空，上传路径为'news/'
    image = models.ImageField(upload_to='news/', null=True, blank=True, verbose_name='资讯图片')
    # 创建时间，使用DateTimeField存储，自动添加当前时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 更新时间，使用DateTimeField存储，自动更新为当前时间
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    # 显式定义objects管理器，解决IDE警告
    objects = models.Manager()
    
    # 模型元数据配置
    class Meta:
        verbose_name = '资讯公告'       # 模型的可读名称
        verbose_name_plural = verbose_name  # 复数形式的可读名称
        ordering = ['-created_at']         # 默认按创建时间倒序排列

# 轮播图模型，用于首页轮播展示景点
class Carousel(models.Model):
    # 关联的景点，使用ForeignKey建立一对多关系，景点删除时轮播图也删除
    scenic_spot = models.ForeignKey(ScenicSpot, on_delete=models.CASCADE, verbose_name='关联景点')
    # 轮播图片，使用ImageField存储，上传路径为'carousel/'
    image = models.ImageField(upload_to='carousel/', verbose_name='轮播图片')
    # 轮播顺序，使用IntegerField存储，默认值为0，用于控制轮播图的显示顺序
    order = models.IntegerField(default=0, verbose_name='轮播顺序')
    # 是否激活，使用BooleanField存储，默认值为True，用于控制轮播图是否显示
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    
    # 显式定义objects管理器，解决IDE警告
    objects = models.Manager()
    
    # 模型元数据配置
    class Meta:
        verbose_name = '轮播图'          # 模型的可读名称
        verbose_name_plural = verbose_name  # 复数形式的可读名称
        ordering = ['order']              # 默认按轮播顺序排列

# 购物车模型，存储用户添加的景点门票
class Cart(models.Model):
    # 关联的用户，使用ForeignKey建立一对多关系，用户删除时购物车记录也删除
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    # 关联的景点，使用ForeignKey建立一对多关系，景点删除时购物车记录也删除
    scenic_spot = models.ForeignKey(ScenicSpot, on_delete=models.CASCADE, verbose_name='景点')
    # 门票数量，使用IntegerField存储，默认值为1
    quantity = models.IntegerField(default=1, verbose_name='数量')
    # 创建时间，使用DateTimeField存储，自动添加当前时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 更新时间，使用DateTimeField存储，自动更新为当前时间
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    # 显式定义objects管理器，解决IDE警告
    objects = models.Manager()
    
    # 模型元数据配置
    class Meta:
        verbose_name = '购物车'          # 模型的可读名称
        verbose_name_plural = verbose_name  # 复数形式的可读名称

# 订单模型，存储用户的购票订单
class Order(models.Model):
    # 定义订单状态选择元组，用于限制订单状态取值范围
    STATUS_CHOICES = (
        (0, '待支付'),  # 订单已创建，等待用户支付
        (1, '已支付'),  # 用户已完成支付
        (2, '已取消'),  # 订单已取消
        (3, '已使用'),  # 门票已使用
    )
    # 关联的用户，使用ForeignKey建立一对多关系，用户删除时订单也删除
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    # 关联的景点，使用ForeignKey建立一对多关系，景点删除时订单也删除
    scenic_spot = models.ForeignKey(ScenicSpot, on_delete=models.CASCADE, verbose_name='景点')
    # 门票数量，使用IntegerField存储
    quantity = models.IntegerField(verbose_name='数量')
    # 订单总价，使用DecimalField存储，最大10位数字，2位小数
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='总价')
    # 订单状态，使用IntegerField存储，默认值为0（待支付）
    status = models.IntegerField(choices=STATUS_CHOICES, default=0, verbose_name='订单状态')
    # 订单号，使用CharField存储，最大长度50，必须唯一
    order_number = models.CharField(max_length=50, unique=True, verbose_name='订单号')
    # 创建时间，使用DateTimeField存储，自动添加当前时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 更新时间，使用DateTimeField存储，自动更新为当前时间
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    # 显式定义objects管理器，解决IDE警告
    objects = models.Manager()
    
    # 模型元数据配置
    class Meta:
        verbose_name = '订单'            # 模型的可读名称
        verbose_name_plural = verbose_name  # 复数形式的可读名称
        ordering = ['-created_at']         # 默认按创建时间倒序排列
