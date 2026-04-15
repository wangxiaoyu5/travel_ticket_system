from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

# 创建演示文稿
prs = Presentation()
prs.slide_width = Inches(16)
prs.slide_height = Inches(9)

# 颜色方案
primary_color = RGBColor(6, 90, 130)  # 深蓝色
secondary_color = RGBColor(28, 114, 147)  # 蓝色
accent_color = RGBColor(33, 41, 92)  # 深蓝色
light_color = RGBColor(241, 245, 249)  # 浅灰色
text_color = RGBColor(30, 41, 59)  # 深灰色

# 标题页
slide_layout = prs.slide_layouts[0]  # 标题布局
slide = prs.slides.add_slide(slide_layout)

# 设置标题
slide.shapes.title.text = "旅游票务系统"
slide.shapes.title.text_frame.paragraphs[0].font.size = Pt(44)
slide.shapes.title.text_frame.paragraphs[0].font.bold = True
slide.shapes.title.text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)

# 设置副标题
subtitle = slide.placeholders[1]
subtitle.text = "毕业设计答辩\n\n王晓宇\n\n指导教师：XXX"
subtitle.text_frame.paragraphs[0].font.size = Pt(28)
subtitle.text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)

# 设置背景
background = slide.background
fill = background.fill
fill.solid()
fill.fore_color.rgb = primary_color



# 项目概述页
slide = prs.slides.add_slide(prs.slide_layouts[5])

# 设置背景
background = slide.background
fill = background.fill
fill.solid()
fill.fore_color.rgb = light_color

# 添加标题
title = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(1))
tf = title.text_frame
tf.text = "项目概述"
p = tf.paragraphs[0]
p.font.size = Pt(32)
p.font.bold = True
p.font.color.rgb = primary_color

# 添加装饰条
slide.shapes.add_shape(
    autoshape_type_id=1,  # 矩形
    left=Inches(0.5),
    top=Inches(1.2),
    width=Inches(0.08),
    height=Inches(0.8)
).fill.solid().fore_color.rgb = primary_color

# 添加内容
content = slide.shapes.add_textbox(Inches(0.8), Inches(1.2), Inches(8.7), Inches(3))
tf = content.text_frame
tf.text = "项目背景：旅游业快速发展，线上票务需求增加"
p = tf.paragraphs[0]
p.font.size = Pt(18)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "项目目标：开发一个功能完整的旅游票务管理系统"
p.font.size = Pt(18)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "系统价值：简化购票流程，提高管理效率"
p.font.size = Pt(18)
p.font.color.rgb = text_color

# 技术架构页
slide = prs.slides.add_slide(prs.slide_layouts[5])

# 设置背景
background = slide.background
fill = background.fill
fill.solid()
fill.fore_color.rgb = light_color

# 添加标题
title = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(1))
tf = title.text_frame
tf.text = "技术架构"
p = tf.paragraphs[0]
p.font.size = Pt(32)
p.font.bold = True
p.font.color.rgb = primary_color

# 添加装饰条
slide.shapes.add_shape(
    autoshape_type_id=1,  # 矩形
    left=Inches(0.5),
    top=Inches(1.2),
    width=Inches(0.08),
    height=Inches(0.8)
).fill.solid().fore_color.rgb = primary_color

# 添加技术栈
tech_stack = slide.shapes.add_textbox(Inches(0.8), Inches(1.2), Inches(4), Inches(0.8))
tf = tech_stack.text_frame
tf.text = "技术栈"
p = tf.paragraphs[0]
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = text_color

tech_content = slide.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(4), Inches(3))
tf = tech_content.text_frame
tf.text = "• 前端：HTML5, CSS3, JavaScript"
p = tf.paragraphs[0]
p.font.size = Pt(16)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "• 后端：Django, Python"
p.font.size = Pt(16)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "• 数据库：SQLite"
p.font.size = Pt(16)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "• API：天气查询API"
p.font.size = Pt(16)
p.font.color.rgb = text_color

# 添加MVC架构
mvc = slide.shapes.add_textbox(Inches(5.5), Inches(1.2), Inches(4), Inches(0.8))
tf = mvc.text_frame
tf.text = "MVC架构"
p = tf.paragraphs[0]
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = text_color

mvc_content = slide.shapes.add_textbox(Inches(5.5), Inches(1.8), Inches(4), Inches(3))
tf = mvc_content.text_frame
tf.text = "• 模型 (Models)：数据结构定义"
p = tf.paragraphs[0]
p.font.size = Pt(16)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "• 视图 (Views)：业务逻辑处理"
p.font.size = Pt(16)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "• 模板 (Templates)：页面展示"
p.font.size = Pt(16)
p.font.color.rgb = text_color

# 系统功能模块页
slide = prs.slides.add_slide(prs.slide_layouts[5])

# 设置背景
background = slide.background
fill = background.fill
fill.solid()
fill.fore_color.rgb = light_color

# 添加标题
title = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(1))
tf = title.text_frame
tf.text = "系统功能模块"
p = tf.paragraphs[0]
p.font.size = Pt(32)
p.font.bold = True
p.font.color.rgb = primary_color

# 添加装饰条
slide.shapes.add_shape(
    autoshape_type_id=1,  # 矩形
    left=Inches(0.5),
    top=Inches(1.2),
    width=Inches(0.08),
    height=Inches(0.8)
).fill.solid().fore_color.rgb = primary_color

# 添加内容
content = slide.shapes.add_textbox(Inches(0.8), Inches(1.2), Inches(8.7), Inches(4))
tf = content.text_frame
tf.text = "1. 用户系统"
p = tf.paragraphs[0]
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "   - 注册、登录、个人中心"
p.font.size = Pt(16)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "2. 景点管理"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "   - 景点列表、详情、分类筛选"
p.font.size = Pt(16)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "3. 购票流程"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "   - 门票选择、购物车、订单创建、支付"
p.font.size = Pt(16)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "4. 后台管理"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "   - 平台管理员、景点管理员功能"
p.font.size = Pt(16)
p.font.color.rgb = text_color

# 核心功能实现 - 用户系统
slide = prs.slides.add_slide(prs.slide_layouts[5])

# 设置背景
background = slide.background
fill = background.fill
fill.solid()
fill.fore_color.rgb = light_color

# 添加标题
title = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(1))
tf = title.text_frame
tf.text = "核心功能实现 - 用户系统"
p = tf.paragraphs[0]
p.font.size = Pt(32)
p.font.bold = True
p.font.color.rgb = primary_color

# 添加装饰条
slide.shapes.add_shape(
    autoshape_type_id=1,  # 矩形
    left=Inches(0.5),
    top=Inches(1.2),
    width=Inches(0.08),
    height=Inches(0.8)
).fill.solid().fore_color.rgb = primary_color

# 添加实现细节
impl_detail = slide.shapes.add_textbox(Inches(0.8), Inches(1.2), Inches(4), Inches(0.8))
tf = impl_detail.text_frame
tf.text = "实现细节"
p = tf.paragraphs[0]
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = text_color

impl_content = slide.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(4), Inches(3))
tf = impl_content.text_frame
tf.text = "• 使用Django内置的认证系统"
p = tf.paragraphs[0]
p.font.size = Pt(16)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "• 自定义用户模型，添加角色字段"
p.font.size = Pt(16)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "• 实现三级权限控制：游客、景点管理员、平台管理员"
p.font.size = Pt(16)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "• 使用装饰器实现权限验证"
p.font.size = Pt(16)
p.font.color.rgb = text_color

# 添加核心代码
core_code = slide.shapes.add_textbox(Inches(5.5), Inches(1.2), Inches(4), Inches(0.8))
tf = core_code.text_frame
tf.text = "核心代码"
p = tf.paragraphs[0]
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = text_color

code_content = slide.shapes.add_textbox(Inches(5.5), Inches(1.8), Inches(4), Inches(3))
tf = code_content.text_frame
tf.text = "@login_required\ndef personal_center(request):\n    user = request.user\n    # 处理用户信息更新"
p = tf.paragraphs[0]
p.font.size = Pt(14)
p.font.name = "Consolas"
p.font.color.rgb = text_color

# 核心功能实现 - 购票系统
slide = prs.slides.add_slide(prs.slide_layouts[5])

# 设置背景
background = slide.background
fill = background.fill
fill.solid()
fill.fore_color.rgb = light_color

# 添加标题
title = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(1))
tf = title.text_frame
tf.text = "核心功能实现 - 购票系统"
p = tf.paragraphs[0]
p.font.size = Pt(32)
p.font.bold = True
p.font.color.rgb = primary_color

# 添加装饰条
slide.shapes.add_shape(
    autoshape_type_id=1,  # 矩形
    left=Inches(0.5),
    top=Inches(1.2),
    width=Inches(0.08),
    height=Inches(0.8)
).fill.solid().fore_color.rgb = primary_color

# 添加实现流程
content = slide.shapes.add_textbox(Inches(0.8), Inches(1.2), Inches(8.7), Inches(4))
tf = content.text_frame
tf.text = "1. 选择景点和门票类型"
p = tf.paragraphs[0]
p.font.size = Pt(16)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "2. 选择使用日期"
p.font.size = Pt(16)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "3. 检查库存"
p.font.size = Pt(16)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "4. 创建订单"
p.font.size = Pt(16)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "5. 支付"
p.font.size = Pt(16)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "6. 生成订单"
p.font.size = Pt(16)
p.font.color.rgb = text_color

# 核心功能实现 - 后台管理
slide = prs.slides.add_slide(prs.slide_layouts[5])

# 设置背景
background = slide.background
fill = background.fill
fill.solid()
fill.fore_color.rgb = light_color

# 添加标题
title = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(1))
tf = title.text_frame
tf.text = "核心功能实现 - 后台管理"
p = tf.paragraphs[0]
p.font.size = Pt(32)
p.font.bold = True
p.font.color.rgb = primary_color

# 添加装饰条
slide.shapes.add_shape(
    autoshape_type_id=1,  # 矩形
    left=Inches(0.5),
    top=Inches(1.2),
    width=Inches(0.08),
    height=Inches(0.8)
).fill.solid().fore_color.rgb = primary_color

# 平台管理员功能
platform_admin = slide.shapes.add_textbox(Inches(0.8), Inches(1.2), Inches(4), Inches(0.8))
tf = platform_admin.text_frame
tf.text = "平台管理员功能"
p = tf.paragraphs[0]
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = text_color

platform_content = slide.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(4), Inches(3))
tf = platform_content.text_frame
tf.text = "• 用户管理：增删改查用户"
p = tf.paragraphs[0]
p.font.size = Pt(16)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "• 景点管理：审核、管理景点"
p.font.size = Pt(16)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "• 订单管理：查看所有订单"
p.font.size = Pt(16)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "• 评论管理：回复、删除评论"
p.font.size = Pt(16)
p.font.color.rgb = text_color

# 景点管理员功能
scenic_admin = slide.shapes.add_textbox(Inches(5.5), Inches(1.2), Inches(4), Inches(0.8))
tf = scenic_admin.text_frame
tf.text = "景点管理员功能"
p = tf.paragraphs[0]
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = text_color

scenic_content = slide.shapes.add_textbox(Inches(5.5), Inches(1.8), Inches(4), Inches(3))
tf = scenic_content.text_frame
tf.text = "• 景点管理：添加、编辑景点"
p = tf.paragraphs[0]
p.font.size = Pt(16)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "• 门票管理：设置门票类型和库存"
p.font.size = Pt(16)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "• 订单管理：查看景点订单"
p.font.size = Pt(16)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "• 评论管理：回复游客评论"
p.font.size = Pt(16)
p.font.color.rgb = text_color

# 系统特色页
slide = prs.slides.add_slide(prs.slide_layouts[5])

# 设置背景
background = slide.background
fill = background.fill
fill.solid()
fill.fore_color.rgb = light_color

# 添加标题
title = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(1))
tf = title.text_frame
tf.text = "系统特色"
p = tf.paragraphs[0]
p.font.size = Pt(32)
p.font.bold = True
p.font.color.rgb = primary_color

# 添加装饰条
slide.shapes.add_shape(
    autoshape_type_id=1,  # 矩形
    left=Inches(0.5),
    top=Inches(1.2),
    width=Inches(0.08),
    height=Inches(0.8)
).fill.solid().fore_color.rgb = primary_color

# 添加内容
content = slide.shapes.add_textbox(Inches(0.8), Inches(1.2), Inches(8.7), Inches(4))
tf = content.text_frame
tf.text = "1. 实时库存管理"
p = tf.paragraphs[0]
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "   - 按日期管理门票库存，确保数据准确性"
p.font.size = Pt(16)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "2. 天气查询集成"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "   - 购票时查询景点天气，提升用户体验"
p.font.size = Pt(16)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "3. 多级权限管理"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "   - 不同角色拥有不同权限，确保系统安全"
p.font.size = Pt(16)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "4. 响应式设计"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "   - 适配不同设备，提供良好的用户体验"
p.font.size = Pt(16)
p.font.color.rgb = text_color

# 数据库设计页
slide = prs.slides.add_slide(prs.slide_layouts[5])

# 设置背景
background = slide.background
fill = background.fill
fill.solid()
fill.fore_color.rgb = light_color

# 添加标题
title = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(1))
tf = title.text_frame
tf.text = "数据库设计"
p = tf.paragraphs[0]
p.font.size = Pt(32)
p.font.bold = True
p.font.color.rgb = primary_color

# 添加装饰条
slide.shapes.add_shape(
    autoshape_type_id=1,  # 矩形
    left=Inches(0.5),
    top=Inches(1.2),
    width=Inches(0.08),
    height=Inches(0.8)
).fill.solid().fore_color.rgb = primary_color

# 添加主要数据表
content = slide.shapes.add_textbox(Inches(0.8), Inches(1.2), Inches(8.7), Inches(4))
tf = content.text_frame
tf.text = "• User - 用户表"
p = tf.paragraphs[0]
p.font.size = Pt(16)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "• ScenicSpot - 景点表"
p.font.size = Pt(16)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "• TicketType - 门票类型表"
p.font.size = Pt(16)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "• Order - 订单表"
p.font.size = Pt(16)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "• Cart - 购物车表"
p.font.size = Pt(16)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "• ScenicSpotComment - 评论表"
p.font.size = Pt(16)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "• DateStock - 日期库存表"
p.font.size = Pt(16)
p.font.color.rgb = text_color

# 系统演示页
slide = prs.slides.add_slide(prs.slide_layouts[5])

# 设置背景
background = slide.background
fill = background.fill
fill.solid()
fill.fore_color.rgb = light_color

# 添加标题
title = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(1))
tf = title.text_frame
tf.text = "系统演示"
p = tf.paragraphs[0]
p.font.size = Pt(32)
p.font.bold = True
p.font.color.rgb = primary_color

# 添加装饰条
slide.shapes.add_shape(
    autoshape_type_id=1,  # 矩形
    left=Inches(0.5),
    top=Inches(1.2),
    width=Inches(0.08),
    height=Inches(0.8)
).fill.solid().fore_color.rgb = primary_color

# 添加内容
content = slide.shapes.add_textbox(Inches(0.8), Inches(1.2), Inches(8.7), Inches(4))
tf = content.text_frame
tf.text = "• 首页展示：轮播图、热门景点、最新资讯"
p = tf.paragraphs[0]
p.font.size = Pt(16)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "• 景点列表：分类筛选、搜索功能"
p.font.size = Pt(16)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "• 景点详情：景点信息、评论、购票入口"
p.font.size = Pt(16)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "• 购票流程：选择门票、日期、数量，创建订单"
p.font.size = Pt(16)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "• 个人中心：个人信息、订单管理、收藏"
p.font.size = Pt(16)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "• 后台管理：用户、景点、订单管理"
p.font.size = Pt(16)
p.font.color.rgb = text_color

# 项目收获与展望页
slide = prs.slides.add_slide(prs.slide_layouts[5])

# 设置背景
background = slide.background
fill = background.fill
fill.solid()
fill.fore_color.rgb = light_color

# 添加标题
title = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(1))
tf = title.text_frame
tf.text = "项目收获与展望"
p = tf.paragraphs[0]
p.font.size = Pt(32)
p.font.bold = True
p.font.color.rgb = primary_color

# 添加装饰条
slide.shapes.add_shape(
    autoshape_type_id=1,  # 矩形
    left=Inches(0.5),
    top=Inches(1.2),
    width=Inches(0.08),
    height=Inches(0.8)
).fill.solid().fore_color.rgb = primary_color

# 项目收获
harvest = slide.shapes.add_textbox(Inches(0.8), Inches(1.2), Inches(4), Inches(0.8))
tf = harvest.text_frame
tf.text = "项目收获"
p = tf.paragraphs[0]
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = text_color

harvest_content = slide.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(4), Inches(3))
tf = harvest_content.text_frame
tf.text = "• 掌握Django框架的使用"
p = tf.paragraphs[0]
p.font.size = Pt(16)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "• 理解MVC架构设计模式"
p.font.size = Pt(16)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "• 学习数据库设计与优化"
p.font.size = Pt(16)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "• 提升问题解决能力"
p.font.size = Pt(16)
p.font.color.rgb = text_color

# 未来展望
future = slide.shapes.add_textbox(Inches(5.5), Inches(1.2), Inches(4), Inches(0.8))
tf = future.text_frame
tf.text = "未来展望"
p = tf.paragraphs[0]
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = text_color

future_content = slide.shapes.add_textbox(Inches(5.5), Inches(1.8), Inches(4), Inches(3))
tf = future_content.text_frame
tf.text = "• 增加在线支付功能"
p = tf.paragraphs[0]
p.font.size = Pt(16)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "• 开发移动端应用"
p.font.size = Pt(16)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "• 优化系统性能"
p.font.size = Pt(16)
p.font.color.rgb = text_color

p = tf.add_paragraph()
p.text = "• 添加更多旅游相关功能"
p.font.size = Pt(16)
p.font.color.rgb = text_color

# 致谢页
slide = prs.slides.add_slide(prs.slide_layouts[5])

# 设置背景
background = slide.background
fill = background.fill
fill.solid()
fill.fore_color.rgb = primary_color

# 添加标题
title = slide.shapes.add_textbox(Inches(0.5), Inches(2), Inches(9), Inches(3))
tf = title.text_frame
tf.text = "谢谢聆听！"
p = tf.paragraphs[0]
p.font.size = Pt(44)
p.font.bold = True
p.font.color.rgb = RGBColor(255, 255, 255)
p.alignment = 1  # 居中

# 添加副标题
run = p.add_run()
run.text = "\n欢迎提问"
run.font.size = Pt(24)
run.font.bold = False

# 保存PPT文件
prs.save("旅游票务系统毕业设计答辩.pptx")
print("PPT生成完成！")
