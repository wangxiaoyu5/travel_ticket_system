from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

# 创建演示文稿
prs = Presentation()

# 标题页
def add_title_slide():
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = "旅游票务系统"
    subtitle = slide.placeholders[1]
    subtitle.text = "毕业设计答辩\n王晓宇\n指导教师：XXX"

# 内容页
def add_content_slide(title, content):
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = title
    content_placeholder = slide.placeholders[1]
    content_placeholder.text = content

# 生成PPT
add_title_slide()

add_content_slide(
    "项目概述",
    "项目背景：\n随着旅游业的快速发展，传统的线下购票方式已经无法满足游客的需求。线上票务系统的出现，不仅方便了游客购票，也提高了景区的管理效率。\n\n项目目标：\n开发一个功能完整的旅游票务管理系统，实现景点信息展示、在线购票、订单管理、用户管理等核心功能。\n\n系统价值：\n- 简化购票流程，提高用户体验\n- 实时管理门票库存，避免超售\n- 提供数据分析，辅助景区决策\n- 降低运营成本，提高管理效率"
)

add_content_slide(
    "技术架构",
    "技术栈：\n- 前端：HTML5, CSS3, JavaScript, Bootstrap\n- 后端：Django 4.0, Python 3.10\n- 数据库：SQLite\n- API：天气查询API\n- 认证：Django内置认证系统\n\nMVC架构：\n- 模型 (Models)：定义数据结构，处理数据库操作\n- 视图 (Views)：处理业务逻辑，响应HTTP请求\n- 模板 (Templates)：生成HTML页面，展示数据\n\n系统架构：\n- 客户端：浏览器、移动设备\n- 服务端：Django应用\n- 数据层：SQLite数据库"
)

add_content_slide(
    "系统功能模块",
    "1. 用户系统\n   - 注册：新用户注册，支持邮箱验证\n   - 登录：用户登录，支持角色选择\n   - 个人中心：修改个人信息，查看订单和收藏\n   - 密码重置：通过邮箱重置密码\n\n2. 景点管理\n   - 景点列表：展示所有景点，支持分类筛选\n   - 景点详情：查看景点详细信息，包括图片、描述、评论\n   - 搜索功能：根据关键词搜索景点\n   - 浏览历史：记录用户浏览过的景点\n\n3. 购票流程\n   - 门票选择：选择门票类型和数量\n   - 日期选择：选择使用日期，查看库存\n   - 购物车：管理待支付的门票\n   - 订单创建：生成订单，计算总价\n   - 支付：支持多种支付方式\n\n4. 后台管理\n   - 平台管理员：管理所有用户、景点、订单\n   - 景点管理员：管理所属景点的信息和订单"
)

add_content_slide(
    "核心功能实现 - 用户系统",
    "实现细节：\n- 使用Django内置的认证系统，自定义用户模型添加角色字段\n- 实现三级权限控制：游客(0)、景点管理员(1)、平台管理员(2)\n- 使用装饰器实现权限验证，确保只有授权用户能访问对应页面\n- 密码加密存储，保障用户数据安全\n\n核心代码：\n@login_required\ndef personal_center(request):\n    user = request.user\n    # 处理用户信息更新\n    if request.method == 'POST':\n        user.username = request.POST.get('username')\n        user.email = request.POST.get('email')\n        # 保存用户信息\n        user.save()\n        messages.success(request, '个人信息更新成功')\n    # 获取用户收藏和浏览历史\n    favorites = Collection.objects.filter(user=user)\n    browse_history = BrowseHistory.objects.filter(user=user)\n    return render(request, 'personal_center.html', {\n        'favorites': favorites,\n        'browse_history': browse_history\n    })"
)

add_content_slide(
    "核心功能实现 - 购票系统",
    "实现流程：\n1. 选择景点和门票类型：用户从景点详情页进入购票页面，选择合适的门票类型\n2. 选择使用日期：选择游玩日期，系统实时检查该日期的门票库存\n3. 检查库存：通过DateStock模型检查对应日期的门票库存是否充足\n4. 创建订单：生成唯一订单号，计算总价，创建订单记录\n5. 支付：跳转到支付页面，完成支付流程\n6. 生成订单：支付成功后，更新订单状态，减少对应日期的库存\n\n关键技术点：\n- 日期化库存管理：使用DateStock模型记录每天的库存情况\n- 实时库存检查：购票时实时检查库存，避免超售\n- 订单号生成：结合时间戳和随机数生成唯一订单号\n- 事务处理：确保订单创建和库存更新的原子性"
)

add_content_slide(
    "核心功能实现 - 后台管理",
    "平台管理员功能：\n- 用户管理：增删改查用户，分配角色和权限\n- 景点管理：审核、添加、编辑、删除景点信息\n- 订单管理：查看所有订单，处理退款和投诉\n- 评论管理：回复、删除用户评论\n- 数据统计：查看系统运行数据和趋势\n\n景点管理员功能：\n- 景点管理：添加、编辑、上架/下架景点\n- 门票管理：设置门票类型、价格和库存\n- 订单管理：查看和处理所属景点的订单\n- 评论管理：回复游客评论\n- 数据统计：查看景点的销售和访问数据\n\n实现方式：\n- 使用装饰器实现权限控制\n- 后台页面使用响应式设计\n- 数据分页展示，提高管理效率"
)

add_content_slide(
    "系统特色",
    "1. 实时库存管理\n   - 按日期管理门票库存，确保数据准确性\n   - 实时显示库存状态，避免超售\n   - 支持批量设置和调整库存\n\n2. 天气查询集成\n   - 购票时查询景点天气，提升用户体验\n   - 根据天气情况提供游玩建议\n   - 集成第三方天气API，获取实时天气数据\n\n3. 多级权限管理\n   - 不同角色拥有不同权限，确保系统安全\n   - 细粒度的权限控制，保障数据安全\n   - 权限继承机制，简化权限管理\n\n4. 响应式设计\n   - 适配不同设备，提供良好的用户体验\n   - 移动端友好，支持随时随地购票\n   - 自适应布局，在不同屏幕尺寸下都能正常显示"
)

add_content_slide(
    "数据库设计",
    "主要数据表：\n- User - 用户表：存储用户信息，包括用户名、密码、邮箱、角色等\n- ScenicSpot - 景点表：存储景点信息，包括名称、描述、价格、图片等\n- TicketType - 门票类型表：存储门票类型信息，包括名称、价格、类型等\n- Order - 订单表：存储订单信息，包括订单号、用户、景点、门票、数量、总价等\n- Cart - 购物车表：存储购物车信息，包括用户、景点、门票、数量等\n- ScenicSpotComment - 评论表：存储用户评论，包括用户、景点、内容、回复等\n- DateStock - 日期库存表：存储每天的门票库存情况\n- Collection - 收藏表：存储用户收藏的景点\n- BrowseHistory - 浏览历史表：存储用户的浏览历史\n\n表关系：\n- User与Order、Cart、ScenicSpotComment、Collection、BrowseHistory是一对多关系\n- ScenicSpot与TicketType、Order、Cart、ScenicSpotComment是一对多关系\n- TicketType与Order、Cart、DateStock是一对多关系"
)

add_content_slide(
    "系统演示",
    "首页展示：\n- 轮播图：展示热门景点和活动\n- 热门景点：展示当前热门的景点\n- 最新资讯：展示最新的旅游资讯和公告\n- 快速搜索：方便用户快速找到景点\n\n景点列表：\n- 分类筛选：按地区、分类等筛选景点\n- 搜索功能：根据关键词搜索景点\n- 排序功能：按价格、热度等排序\n- 分页展示：提高加载速度和用户体验\n\n景点详情：\n- 景点信息：详细介绍景点的特色和设施\n- 图片展示：展示景点的多张图片\n- 用户评论：查看其他用户的评论和回复\n- 购票入口：直接进入购票页面\n\n购票流程：\n- 选择门票类型：根据需求选择合适的门票\n- 选择日期：选择游玩日期，查看库存\n- 确认订单：核对订单信息，确认支付\n- 支付成功：生成订单，发送通知\n\n个人中心：\n- 个人信息：查看和修改个人信息\n- 订单管理：查看所有订单和状态\n- 我的收藏：查看收藏的景点\n- 浏览历史：查看浏览过的景点\n\n后台管理：\n- 仪表盘：查看系统运行数据\n- 用户管理：管理所有用户\n- 景点管理：管理所有景点\n- 订单管理：处理所有订单"
)

add_content_slide(
    "项目收获与展望",
    "项目收获：\n- 掌握Django框架的使用，包括模型、视图、模板的开发\n- 理解MVC架构设计模式，掌握Web应用开发流程\n- 学习数据库设计与优化，包括表结构设计和关系建立\n- 提升问题解决能力，学会调试和排查错误\n- 熟悉前端技术，包括HTML、CSS、JavaScript的使用\n- 了解API集成，学会调用第三方服务\n\n未来展望：\n- 增加在线支付功能，支持支付宝、微信支付等\n- 开发移动端应用，提供更好的移动用户体验\n- 优化系统性能，提高并发处理能力\n- 添加更多旅游相关功能，如路线规划、攻略分享等\n- 实现数据分析和预测，辅助景区决策\n- 加强系统安全性，防止各种攻击"
)

# 致谢页
def add_thanks_slide():
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = "谢谢聆听！"
    subtitle = slide.placeholders[1]
    subtitle.text = "欢迎提问"

add_thanks_slide()

# 保存PPT文件
prs.save("旅游票务系统毕业设计答辩.pptx")
print("PPT生成完成！")
