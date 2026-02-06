# 导入Django的模型模块，用于创建数据库表结构
from django.db import models
# 导入Django的用户抽象模型和BaseUserManager，用于自定义用户模型
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# 景点分类模型，用于管理景点分类信息
class Category(models.Model):
    # 分类名称，使用CharField存储，最大长度50，必须唯一
    name = models.CharField(max_length=50, unique=True, verbose_name='分类名称')
    # 分类描述，使用TextField存储，支持长文本，允许为空
    description = models.TextField(null=True, blank=True, verbose_name='分类描述')
    # 创建时间，使用DateTimeField存储，自动添加当前时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 更新时间，使用DateTimeField存储，自动更新为当前时间
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    # 显式定义objects管理器，解决IDE警告
    objects = models.Manager()
    
    # 模型元数据配置
    class Meta:
        verbose_name = '景点分类'       # 模型的可读名称
        verbose_name_plural = verbose_name  # 复数形式的可读名称
        ordering = ['name']             # 默认按分类名称排序

# 自定义用户管理器
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('role', 2)  # 网站管理员
        return self.create_user(username, email, password, **extra_fields)

# 自定义用户模型，继承自AbstractBaseUser，支持三种角色
class User(AbstractBaseUser):
    # 使用自定义UserManager作为管理器
    DoesNotExist = None
    objects = UserManager()
    
    # 定义角色选择元组，用于限制角色取值范围
    # 0-游客，1-景点管理员，2-网站管理员
    ROLE_CHOICES = (
        (0, '游客'),        # 普通用户，可浏览景点、购买门票
        (1, '景点管理员'),  # 可管理自己负责的景点信息
        (2, '网站管理员'),  # 可管理所有系统资源
    )
    
    # 定义性别选择元组
    GENDER_CHOICES = (
        ('', '请选择性别'),  # 默认空值，提示用户选择
        ('male', '男'),      # 男性
        ('female', '女'),    # 女性
        ('other', '其他'),   # 其他性别
    )
    
    # 用户名
    username = models.CharField(max_length=150, unique=True, verbose_name='用户名')
    # 邮箱
    email = models.EmailField(unique=True, verbose_name='邮箱')
    # 角色字段，使用IntegerField存储，默认值为0（游客）
    role = models.IntegerField(choices=ROLE_CHOICES, default=0, verbose_name='角色')
    # 头像字段，使用ImageField存储，允许为空，上传路径为'avatars/'
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='头像')
    # 手机号字段，使用CharField存储，最大长度11，允许为空
    phone = models.CharField(max_length=11, null=True, blank=True, verbose_name='手机号')
    # 性别字段，使用CharField存储，最大长度10，允许为空
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='', verbose_name='性别')
    # 出生日期字段，使用DateField存储，允许为空
    birthdate = models.DateField(null=True, blank=True, verbose_name='出生日期')
    # 重置密码token，用于密码重置功能
    reset_token = models.CharField(max_length=100, null=True, blank=True, verbose_name='重置密码token')
    # 重置密码token过期时间
    reset_token_expiry = models.DateTimeField(null=True, blank=True, verbose_name='重置密码token过期时间')
    # 是否激活
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    
    # 设置用户名字段
    USERNAME_FIELD = 'username'
    # 必需字段
    REQUIRED_FIELDS = ['email']
    
    # 模型元数据配置
    class Meta:
        verbose_name = '用户'           # 模型的可读名称
        verbose_name_plural = verbose_name  # 复数形式的可读名称

# 地区模型，用于管理地区信息
class Region(models.Model):
    # 地区名称，使用CharField存储，最大长度100，必须唯一
    name = models.CharField(max_length=100, unique=True, verbose_name='地区名称')
    # 创建时间，使用DateTimeField存储，自动添加当前时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 更新时间，使用DateTimeField存储，自动更新为当前时间
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    # 显式定义objects管理器，解决IDE警告
    objects = models.Manager()
    
    # 模型元数据配置
    class Meta:
        verbose_name = '地区信息'         # 模型的可读名称
        verbose_name_plural = verbose_name  # 复数形式的可读名称
        ordering = ['name']               # 默认按地区名称排序

# 景点信息模型，存储所有景点的详细信息
class ScenicSpot(models.Model):
    DoesNotExist = None
    
    # 显示ID，用于给用户展示的连续编号
    display_id = models.IntegerField(default=0, verbose_name='显示ID')
    
    # 关联的景点管理员，使用ForeignKey建立一对多关系，允许为空
    # 当关联的用户删除时，该字段设为NULL
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_scenic_spots', verbose_name='景点管理员')
    # 景点分类，直接存储分类名称，使用CharField
    category = models.CharField(max_length=50, default='自然风光类', verbose_name='分类')
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
    # 景点地区，使用ForeignKey关联Region模型
    region = models.ForeignKey('Region', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='地区')
    # 景点标签，使用CharField存储，最大长度100，用于存储多个标签，以逗号分隔
    tags = models.CharField(max_length=100, default='热门', verbose_name='标签', help_text='多个标签用逗号分隔')
    # 景点评分，使用DecimalField存储，最大3位数字，1位小数，默认0.0
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0, verbose_name='评分')
    # 预约人数，使用IntegerField存储，默认0
    booking_count = models.IntegerField(default=0, verbose_name='预约人数')
    # 总票数，使用IntegerField存储，默认1000
    total_tickets = models.IntegerField(default=1000, verbose_name='总票数')
    # 是否激活，使用BooleanField存储，默认值为True，用于控制景点是否上架
    is_active = models.BooleanField(default=True, verbose_name='是否上架')
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



# 门票类型模型，用于管理不同类型的门票
class TicketType(models.Model):
    # 定义门票类型选择元组
    TYPE_CHOICES = (
        ('single', '单票'),       # 单票，适用于单个景点
        ('package', '套票'),      # 套票，适用于多个景点或包含其他服务
    )
    
    # 关联的景点，使用ForeignKey建立一对多关系，景点删除时门票类型也删除
    scenic_spot = models.ForeignKey(ScenicSpot, on_delete=models.CASCADE, verbose_name='景点')
    # 门票名称，使用CharField存储，最大长度100
    name = models.CharField(max_length=100, verbose_name='门票名称')
    # 门票类型，使用CharField存储，选择项来自TYPE_CHOICES
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='single', verbose_name='门票类型')
    # 门票价格，使用DecimalField存储，最大10位数字，2位小数
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='门票价格')
    # 库存数量，使用IntegerField存储，默认值为1000
    stock = models.IntegerField(default=1000, verbose_name='默认库存')
    # 是否激活，使用BooleanField存储，默认值为True
    # 用于控制门票是否可购买
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    # 门票前缀，用于区分不同日期的门票
    prefix = models.CharField(max_length=20, blank=True, default='', verbose_name='前缀')
    # 创建时间，使用DateTimeField存储，自动添加当前时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 更新时间，使用DateTimeField存储，自动更新为当前时间
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    # 显式定义objects管理器，解决IDE警告
    objects = models.Manager()
    
    # 模型元数据配置
    class Meta:
        verbose_name = '门票类型'         # 模型的可读名称
        verbose_name_plural = verbose_name  # 复数形式的可读名称
        ordering = ['-created_at']         # 默认按创建时间倒序排列

# 日期库存模型，用于存储每日的门票库存信息
class DateStock(models.Model):
    # 关联的门票类型
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE, verbose_name='门票类型')
    # 使用日期
    use_date = models.DateField(verbose_name='使用日期')
    # 当天库存
    stock = models.IntegerField(default=1000, verbose_name='当天库存')
    # 当天已售
    sold = models.IntegerField(default=0, verbose_name='当天已售')
    # 创建时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 更新时间
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    # 显式定义objects管理器
    objects = models.Manager()
    
    class Meta:
        verbose_name = '日期库存'
        verbose_name_plural = '日期库存'
        ordering = ['use_date']
        unique_together = ('ticket_type', 'use_date')

# 购物车模型，存储用户添加的景点门票
class Cart(models.Model):
    # 关联的用户，使用ForeignKey建立一对多关系，用户删除时购物车记录也删除
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    # 关联的景点，使用ForeignKey建立一对多关系，景点删除时购物车记录也删除
    scenic_spot = models.ForeignKey(ScenicSpot, on_delete=models.CASCADE, verbose_name='景点')
    # 关联的门票类型，使用ForeignKey建立一对多关系，门票类型删除时购物车记录也删除
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE, null=True, blank=True, verbose_name='门票类型')
    # 使用日期，使用DateField存储，允许为空
    # 用于指定门票的使用日期
    use_date = models.DateField(null=True, blank=True, verbose_name='使用日期')
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
        # 唯一约束：同一用户同一门票同一日期只能添加一次到购物车
        unique_together = ('user', 'scenic_spot', 'ticket_type', 'use_date')

# 景点留言模型，存储用户对景点的留言
class ScenicSpotComment(models.Model):
    # 关联的景点，使用ForeignKey建立一对多关系，景点删除时留言也删除
    DoesNotExist = None
    scenic_spot = models.ForeignKey(ScenicSpot, on_delete=models.CASCADE, verbose_name='景点')
    # 关联的用户，使用ForeignKey建立一对多关系，用户删除时留言也删除
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    # 留言内容，使用TextField存储，支持长文本
    content = models.TextField(verbose_name='留言内容')
    # 回复内容，使用TextField存储，支持长文本，允许为空
    reply = models.TextField(null=True, blank=True, verbose_name='回复内容')
    # 回复时间，使用DateTimeField存储，自动添加当前时间，允许为空
    reply_time = models.DateTimeField(null=True, blank=True, verbose_name='回复时间')
    # 是否回复，使用BooleanField存储，默认值为False
    # 用于标识留言是否已回复
    is_replied = models.BooleanField(default=False, verbose_name='是否回复')
    # 创建时间，使用DateTimeField存储，自动添加当前时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 显式定义objects管理器，解决IDE警告
    objects = models.Manager()
    
    # 模型元数据配置
    class Meta:
        verbose_name = '景点留言'         # 模型的可读名称
        verbose_name_plural = verbose_name  # 复数形式的可读名称
        ordering = ['-created_at']         # 默认按创建时间倒序排列

# 订单模型，存储用户的购票订单
class Order(models.Model):
    # 定义订单状态选择元组，用于限制订单状态取值范围
    DoesNotExist = None
    STATUS_CHOICES = (
        (0, '待支付'),  # 订单已创建，等待用户支付
        (1, '已支付'),  # 用户已完成支付
        (2, '已取消'),  # 订单已取消
        (3, '已使用'),  # 门票已使用
        (4, '已退款'),  # 门票已退款
        (5, '退款审核中'),  # 退款申请已提交，等待管理员审核
    )
    # 关联的用户，使用ForeignKey建立一对多关系，用户删除时订单也删除
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    # 关联的景点，使用ForeignKey建立一对多关系，景点删除时订单也删除
    scenic_spot = models.ForeignKey(ScenicSpot, on_delete=models.CASCADE, verbose_name='景点')
    # 关联的门票类型，使用ForeignKey建立一对多关系，门票类型删除时订单也删除
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE, null=True, blank=True, verbose_name='门票类型')
    # 使用日期，使用DateField存储，允许为空
    # 用于指定门票的使用日期
    use_date = models.DateField(null=True, blank=True, verbose_name='使用日期')
    # 门票数量，使用IntegerField存储
    quantity = models.IntegerField(verbose_name='数量')
    # 订单总价，使用DecimalField存储，最大10位数字，2位小数
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='总价')
    # 订单状态，使用IntegerField存储，默认值为0（待支付）
    status = models.IntegerField(choices=STATUS_CHOICES, default=0, verbose_name='订单状态')
    # 订单号，使用CharField存储，最大长度50，必须唯一
    order_number = models.CharField(max_length=50, unique=True, verbose_name='订单号')
    # 退款原因，使用TextField存储，允许为空
    # 只有退款状态的订单才需要填写
    refund_reason = models.TextField(null=True, blank=True, verbose_name='退款原因')
    # 退款申请时间，使用DateTimeField存储，允许为空
    refund_apply_time = models.DateTimeField(null=True, blank=True, verbose_name='退款申请时间')
    # 退款审核时间，使用DateTimeField存储，允许为空
    refund_audit_time = models.DateTimeField(null=True, blank=True, verbose_name='退款审核时间')
    # 退款金额，使用DecimalField存储，最大10位数字，2位小数，允许为空
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='退款金额')
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

# 收藏模型，用于用户收藏景点
class Collection(models.Model):
    # 关联的用户，使用ForeignKey建立一对多关系，用户删除时收藏记录也删除
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    # 关联的景点，使用ForeignKey建立一对多关系，景点删除时收藏记录也删除
    scenic_spot = models.ForeignKey(ScenicSpot, on_delete=models.CASCADE, verbose_name='景点')
    # 创建时间，使用DateTimeField存储，自动添加当前时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 显式定义objects管理器，解决IDE警告
    objects = models.Manager()
    
    # 模型元数据配置
    class Meta:
        verbose_name = '收藏记录'         # 模型的可读名称
        verbose_name_plural = verbose_name  # 复数形式的可读名称
        # 唯一约束：一个用户只能收藏一个景点一次
        unique_together = ('user', 'scenic_spot')
        ordering = ['-created_at']         # 默认按创建时间倒序排列

# 浏览历史模型，用于记录用户浏览景点的历史
class BrowseHistory(models.Model):
    # 关联的用户，使用ForeignKey建立一对多关系，用户删除时浏览历史也删除
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    # 关联的景点，使用ForeignKey建立一对多关系，景点删除时浏览历史也删除
    scenic_spot = models.ForeignKey(ScenicSpot, on_delete=models.CASCADE, verbose_name='景点')
    # 浏览时间，使用DateTimeField存储，自动添加当前时间
    browse_time = models.DateTimeField(auto_now_add=True, verbose_name='浏览时间')
    # 显式定义objects管理器，解决IDE警告
    objects = models.Manager()
    
    # 模型元数据配置
    class Meta:
        verbose_name = '浏览历史'         # 模型的可读名称
        verbose_name_plural = verbose_name  # 复数形式的可读名称
        ordering = ['-browse_time']        # 默认按浏览时间倒序排列