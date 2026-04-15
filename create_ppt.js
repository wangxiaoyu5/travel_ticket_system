// 引入pptxgenjs库
const pptxgen = require('pptxgenjs');

// 创建演示文稿
const pres = new pptxgen();

// 设置演示文稿属性
pres.layout = 'LAYOUT_16x9';
pres.author = '王晓宇';
pres.title = '旅游票务系统毕业设计答辩';

// 颜色方案
const colors = {
  primary: '065A82',    // 深蓝色
  secondary: '1C7293',  // 蓝色
  accent: '21295C',     // 深蓝色
  light: 'F1F5F9',      // 浅灰色
  text: '1E293B'        // 深灰色
};

// 添加标题页
const titleSlide = pres.addSlide();
titleSlide.background = { color: colors.primary };
titleSlide.addText(
  [
    { text: '旅游票务系统', options: { bold: true, fontSize: 48, color: 'FFFFFF', align: 'center', breakLine: true } },
    { text: '毕业设计答辩', options: { fontSize: 28, color: 'FFFFFF', align: 'center', breakLine: true } },
    { text: '王晓宇', options: { fontSize: 22, color: 'FFFFFF', align: 'center', breakLine: true } },
    { text: '指导教师：XXX', options: { fontSize: 20, color: 'FFFFFF', align: 'center' } }
  ],
  { x: 0.5, y: 2, w: 15, h: 5, valign: 'middle' }
);

// 添加项目概述页
const overviewSlide = pres.addSlide();
overviewSlide.background = { color: colors.light };
overviewSlide.addText('项目概述', { x: 1, y: 1, w: 14, h: 1, fontSize: 32, color: colors.primary, bold: true });
overviewSlide.addShape(pres.shapes.RECTANGLE, { x: 1, y: 2, w: 0.1, h: 0.8, fill: { color: colors.primary } });
overviewSlide.addText(
  [
    { text: '项目背景：', options: { bold: true, fontSize: 18, color: colors.text, breakLine: true } },
    { text: '随着旅游业的快速发展，传统的线下购票方式已经无法满足游客的需求。线上票务系统的出现，不仅方便了游客购票，也提高了景区的管理效率。', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '\n项目目标：', options: { bold: true, fontSize: 18, color: colors.text, breakLine: true } },
    { text: '开发一个功能完整的旅游票务管理系统，实现景点信息展示、在线购票、订单管理、用户管理等核心功能。', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '\n系统价值：', options: { bold: true, fontSize: 18, color: colors.text, breakLine: true } },
    { text: '- 简化购票流程，提高用户体验', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '- 实时管理门票库存，避免超售', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '- 提供数据分析，辅助景区决策', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '- 降低运营成本，提高管理效率', options: { fontSize: 16, color: colors.text } }
  ],
  { x: 1.3, y: 2, w: 13.2, h: 5 }
);

// 添加技术架构页
const architectureSlide = pres.addSlide();
architectureSlide.background = { color: colors.light };
architectureSlide.addText('技术架构', { x: 1, y: 1, w: 14, h: 1, fontSize: 32, color: colors.primary, bold: true });
architectureSlide.addShape(pres.shapes.RECTANGLE, { x: 1, y: 2, w: 0.1, h: 0.8, fill: { color: colors.primary } });

// 技术栈
architectureSlide.addText('技术栈', { x: 1.3, y: 2, w: 6, h: 0.8, fontSize: 20, color: colors.text, bold: true });
architectureSlide.addText(
  [
    { text: '- 前端：HTML5, CSS3, JavaScript, Bootstrap', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '- 后端：Django 4.0, Python 3.10', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '- 数据库：SQLite', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '- API：天气查询API', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '- 认证：Django内置认证系统', options: { fontSize: 16, color: colors.text } }
  ],
  { x: 1.3, y: 2.8, w: 6, h: 3 }
);

// MVC架构
architectureSlide.addText('MVC架构', { x: 8.3, y: 2, w: 6, h: 0.8, fontSize: 20, color: colors.text, bold: true });
architectureSlide.addText(
  [
    { text: '- 模型 (Models)：定义数据结构，处理数据库操作', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '- 视图 (Views)：处理业务逻辑，响应HTTP请求', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '- 模板 (Templates)：生成HTML页面，展示数据', options: { fontSize: 16, color: colors.text } }
  ],
  { x: 8.3, y: 2.8, w: 6, h: 3 }
);

// 添加系统功能模块页
const featuresSlide = pres.addSlide();
featuresSlide.background = { color: colors.light };
featuresSlide.addText('系统功能模块', { x: 1, y: 1, w: 14, h: 1, fontSize: 32, color: colors.primary, bold: true });
featuresSlide.addShape(pres.shapes.RECTANGLE, { x: 1, y: 2, w: 0.1, h: 0.8, fill: { color: colors.primary } });

// 功能模块列表
featuresSlide.addText(
  [
    { text: '1. 用户系统', options: { bold: true, fontSize: 18, color: colors.text, breakLine: true } },
    { text: '   - 注册：新用户注册，支持邮箱验证', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '   - 登录：用户登录，支持角色选择', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '   - 个人中心：修改个人信息，查看订单和收藏', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '   - 密码重置：通过邮箱重置密码', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '\n2. 景点管理', options: { bold: true, fontSize: 18, color: colors.text, breakLine: true } },
    { text: '   - 景点列表：展示所有景点，支持分类筛选', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '   - 景点详情：查看景点详细信息，包括图片、描述、评论', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '   - 搜索功能：根据关键词搜索景点', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '   - 浏览历史：记录用户浏览过的景点', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '\n3. 购票流程', options: { bold: true, fontSize: 18, color: colors.text, breakLine: true } },
    { text: '   - 门票选择：选择门票类型和数量', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '   - 日期选择：选择使用日期，查看库存', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '   - 购物车：管理待支付的门票', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '   - 订单创建：生成订单，计算总价', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '   - 支付：支持多种支付方式', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '\n4. 后台管理', options: { bold: true, fontSize: 18, color: colors.text, breakLine: true } },
    { text: '   - 平台管理员：管理所有用户、景点、订单', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '   - 景点管理员：管理所属景点的信息和订单', options: { fontSize: 16, color: colors.text } }
  ],
  { x: 1.3, y: 2, w: 13.2, h: 5 }
);

// 添加核心功能实现 - 用户系统
const userSystemSlide = pres.addSlide();
userSystemSlide.background = { color: colors.light };
userSystemSlide.addText('核心功能实现 - 用户系统', { x: 1, y: 1, w: 14, h: 1, fontSize: 32, color: colors.primary, bold: true });
userSystemSlide.addShape(pres.shapes.RECTANGLE, { x: 1, y: 2, w: 0.1, h: 0.8, fill: { color: colors.primary } });

// 实现细节
userSystemSlide.addText('实现细节', { x: 1.3, y: 2, w: 6, h: 0.8, fontSize: 20, color: colors.text, bold: true });
userSystemSlide.addText(
  [
    { text: '- 使用Django内置的认证系统，自定义用户模型添加角色字段', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '- 实现三级权限控制：游客(0)、景点管理员(1)、平台管理员(2)', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '- 使用装饰器实现权限验证，确保只有授权用户能访问对应页面', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '- 密码加密存储，保障用户数据安全', options: { fontSize: 16, color: colors.text } }
  ],
  { x: 1.3, y: 2.8, w: 6, h: 3 }
);

// 核心代码
userSystemSlide.addText('核心代码', { x: 8.3, y: 2, w: 6, h: 0.8, fontSize: 20, color: colors.text, bold: true });
userSystemSlide.addText(
  [
    { text: '@login_required', options: { fontSize: 14, color: colors.text, fontFace: 'Consolas', breakLine: true } },
    { text: 'def personal_center(request):', options: { fontSize: 14, color: colors.text, fontFace: 'Consolas', breakLine: true } },
    { text: '    user = request.user', options: { fontSize: 14, color: colors.text, fontFace: 'Consolas', breakLine: true } },
    { text: '    # 处理用户信息更新', options: { fontSize: 14, color: colors.text, fontFace: 'Consolas', breakLine: true } },
    { text: '    if request.method == \'POST\':', options: { fontSize: 14, color: colors.text, fontFace: 'Consolas', breakLine: true } },
    { text: '        user.username = request.POST.get(\'username\')', options: { fontSize: 14, color: colors.text, fontFace: 'Consolas', breakLine: true } },
    { text: '        user.email = request.POST.get(\'email\')', options: { fontSize: 14, color: colors.text, fontFace: 'Consolas', breakLine: true } },
    { text: '        # 保存用户信息', options: { fontSize: 14, color: colors.text, fontFace: 'Consolas', breakLine: true } },
    { text: '        user.save()', options: { fontSize: 14, color: colors.text, fontFace: 'Consolas', breakLine: true } },
    { text: '        messages.success(request, \'个人信息更新成功\')', options: { fontSize: 14, color: colors.text, fontFace: 'Consolas', breakLine: true } },
    { text: '    # 获取用户收藏和浏览历史', options: { fontSize: 14, color: colors.text, fontFace: 'Consolas', breakLine: true } },
    { text: '    favorites = Collection.objects.filter(user=user)', options: { fontSize: 14, color: colors.text, fontFace: 'Consolas', breakLine: true } },
    { text: '    browse_history = BrowseHistory.objects.filter(user=user)', options: { fontSize: 14, color: colors.text, fontFace: 'Consolas', breakLine: true } },
    { text: '    return render(request, \'personal_center.html\', {', options: { fontSize: 14, color: colors.text, fontFace: 'Consolas', breakLine: true } },
    { text: '        \'favorites\': favorites,', options: { fontSize: 14, color: colors.text, fontFace: 'Consolas', breakLine: true } },
    { text: '        \'browse_history\': browse_history', options: { fontSize: 14, color: colors.text, fontFace: 'Consolas', breakLine: true } },
    { text: '    })', options: { fontSize: 14, color: colors.text, fontFace: 'Consolas' } }
  ],
  { x: 8.3, y: 2.8, w: 6, h: 3 }
);

// 添加核心功能实现 - 购票系统
const ticketSystemSlide = pres.addSlide();
ticketSystemSlide.background = { color: colors.light };
ticketSystemSlide.addText('核心功能实现 - 购票系统', { x: 1, y: 1, w: 14, h: 1, fontSize: 32, color: colors.primary, bold: true });
ticketSystemSlide.addShape(pres.shapes.RECTANGLE, { x: 1, y: 2, w: 0.1, h: 0.8, fill: { color: colors.primary } });

// 实现流程
const flowSteps = [
  { text: '1. 选择景点和门票类型：用户从景点详情页进入购票页面，选择合适的门票类型', options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: '2. 选择使用日期：选择游玩日期，系统实时检查该日期的门票库存', options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: '3. 检查库存：通过DateStock模型检查对应日期的门票库存是否充足', options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: '4. 创建订单：生成唯一订单号，计算总价，创建订单记录', options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: '5. 支付：跳转到支付页面，完成支付流程', options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: '6. 生成订单：支付成功后，更新订单状态，减少对应日期的库存', options: { fontSize: 16, color: colors.text } }
];
ticketSystemSlide.addText(flowSteps, { x: 1.3, y: 2, w: 13.2, h: 5 });

// 关键技术点
ticketSystemSlide.addText('关键技术点', { x: 1.3, y: 5, w: 13.2, h: 0.8, fontSize: 20, color: colors.text, bold: true });
ticketSystemSlide.addText(
  [
    { text: '- 日期化库存管理：使用DateStock模型记录每天的库存情况', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '- 实时库存检查：购票时实时检查库存，避免超售', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '- 订单号生成：结合时间戳和随机数生成唯一订单号', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '- 事务处理：确保订单创建和库存更新的原子性', options: { fontSize: 16, color: colors.text } }
  ],
  { x: 1.3, y: 5.8, w: 13.2, h: 2 }
);

// 添加核心功能实现 - 后台管理
const adminSystemSlide = pres.addSlide();
adminSystemSlide.background = { color: colors.light };
adminSystemSlide.addText('核心功能实现 - 后台管理', { x: 1, y: 1, w: 14, h: 1, fontSize: 32, color: colors.primary, bold: true });
adminSystemSlide.addShape(pres.shapes.RECTANGLE, { x: 1, y: 2, w: 0.1, h: 0.8, fill: { color: colors.primary } });

// 平台管理员功能
adminSystemSlide.addText('平台管理员功能', { x: 1.3, y: 2, w: 6, h: 0.8, fontSize: 20, color: colors.text, bold: true });
adminSystemSlide.addText(
  [
    { text: '- 用户管理：增删改查用户，分配角色和权限', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '- 景点管理：审核、添加、编辑、删除景点信息', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '- 订单管理：查看所有订单，处理退款和投诉', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '- 评论管理：回复、删除用户评论', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '- 数据统计：查看系统运行数据和趋势', options: { fontSize: 16, color: colors.text } }
  ],
  { x: 1.3, y: 2.8, w: 6, h: 3.5 }
);

// 景点管理员功能
adminSystemSlide.addText('景点管理员功能', { x: 8.3, y: 2, w: 6, h: 0.8, fontSize: 20, color: colors.text, bold: true });
adminSystemSlide.addText(
  [
    { text: '- 景点管理：添加、编辑、上架/下架景点', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '- 门票管理：设置门票类型、价格和库存', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '- 订单管理：查看和处理所属景点的订单', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '- 评论管理：回复游客评论', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '- 数据统计：查看景点的销售和访问数据', options: { fontSize: 16, color: colors.text } }
  ],
  { x: 8.3, y: 2.8, w: 6, h: 3.5 }
);

// 添加系统特色页
const featuresSlide2 = pres.addSlide();
featuresSlide2.background = { color: colors.light };
featuresSlide2.addText('系统特色', { x: 1, y: 1, w: 14, h: 1, fontSize: 32, color: colors.primary, bold: true });
featuresSlide2.addShape(pres.shapes.RECTANGLE, { x: 1, y: 2, w: 0.1, h: 0.8, fill: { color: colors.primary } });

// 特色列表
featuresSlide2.addText(
  [
    { text: '1. 实时库存管理', options: { bold: true, fontSize: 18, color: colors.text, breakLine: true } },
    { text: '   - 按日期管理门票库存，确保数据准确性', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '   - 实时显示库存状态，避免超售', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '   - 支持批量设置和调整库存', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '\n2. 天气查询集成', options: { bold: true, fontSize: 18, color: colors.text, breakLine: true } },
    { text: '   - 购票时查询景点天气，提升用户体验', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '   - 根据天气情况提供游玩建议', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '   - 集成第三方天气API，获取实时天气数据', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '\n3. 多级权限管理', options: { bold: true, fontSize: 18, color: colors.text, breakLine: true } },
    { text: '   - 不同角色拥有不同权限，确保系统安全', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '   - 细粒度的权限控制，保障数据安全', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '   - 权限继承机制，简化权限管理', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '\n4. 响应式设计', options: { bold: true, fontSize: 18, color: colors.text, breakLine: true } },
    { text: '   - 适配不同设备，提供良好的用户体验', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '   - 移动端友好，支持随时随地购票', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '   - 自适应布局，在不同屏幕尺寸下都能正常显示', options: { fontSize: 16, color: colors.text } }
  ],
  { x: 1.3, y: 2, w: 13.2, h: 5 }
);

// 添加数据库设计页
const databaseSlide = pres.addSlide();
databaseSlide.background = { color: colors.light };
databaseSlide.addText('数据库设计', { x: 1, y: 1, w: 14, h: 1, fontSize: 32, color: colors.primary, bold: true });
databaseSlide.addShape(pres.shapes.RECTANGLE, { x: 1, y: 2, w: 0.1, h: 0.8, fill: { color: colors.primary } });

// 主要数据表
const tables = [
  { text: '- User - 用户表：存储用户信息，包括用户名、密码、邮箱、角色等', options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: '- ScenicSpot - 景点表：存储景点信息，包括名称、描述、价格、图片等', options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: '- TicketType - 门票类型表：存储门票类型信息，包括名称、价格、类型等', options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: '- Order - 订单表：存储订单信息，包括订单号、用户、景点、门票、数量、总价等', options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: '- Cart - 购物车表：存储购物车信息，包括用户、景点、门票、数量等', options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: '- ScenicSpotComment - 评论表：存储用户评论，包括用户、景点、内容、回复等', options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: '- DateStock - 日期库存表：存储每天的门票库存情况', options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: '- Collection - 收藏表：存储用户收藏的景点', options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: '- BrowseHistory - 浏览历史表：存储用户的浏览历史', options: { fontSize: 16, color: colors.text } }
];
databaseSlide.addText(tables, { x: 1.3, y: 2, w: 13.2, h: 5 });

// 添加系统演示页
const demoSlide = pres.addSlide();
demoSlide.background = { color: colors.light };
demoSlide.addText('系统演示', { x: 1, y: 1, w: 14, h: 1, fontSize: 32, color: colors.primary, bold: true });
demoSlide.addShape(pres.shapes.RECTANGLE, { x: 1, y: 2, w: 0.1, h: 0.8, fill: { color: colors.primary } });
demoSlide.addText(
  [
    { text: '首页展示：', options: { bold: true, fontSize: 18, color: colors.text, breakLine: true } },
    { text: '   - 轮播图：展示热门景点和活动', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '   - 热门景点：展示当前热门的景点', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '   - 最新资讯：展示最新的旅游资讯和公告', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '   - 快速搜索：方便用户快速找到景点', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '\n景点列表：', options: { bold: true, fontSize: 18, color: colors.text, breakLine: true } },
    { text: '   - 分类筛选：按地区、分类等筛选景点', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '   - 搜索功能：根据关键词搜索景点', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '   - 排序功能：按价格、热度等排序', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '   - 分页展示：提高加载速度和用户体验', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '\n景点详情：', options: { bold: true, fontSize: 18, color: colors.text, breakLine: true } },
    { text: '   - 景点信息：详细介绍景点的特色和设施', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '   - 图片展示：展示景点的多张图片', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '   - 用户评论：查看其他用户的评论和回复', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '   - 购票入口：直接进入购票页面', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '\n购票流程：', options: { bold: true, fontSize: 18, color: colors.text, breakLine: true } },
    { text: '   - 选择门票类型：根据需求选择合适的门票', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '   - 选择日期：选择游玩日期，查看库存', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '   - 确认订单：核对订单信息，确认支付', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '   - 支付成功：生成订单，发送通知', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '\n个人中心：', options: { bold: true, fontSize: 18, color: colors.text, breakLine: true } },
    { text: '   - 个人信息：查看和修改个人信息', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '   - 订单管理：查看所有订单和状态', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '   - 我的收藏：查看收藏的景点', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '   - 浏览历史：查看浏览过的景点', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '\n后台管理：', options: { bold: true, fontSize: 18, color: colors.text, breakLine: true } },
    { text: '   - 仪表盘：查看系统运行数据', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '   - 用户管理：管理所有用户', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '   - 景点管理：管理所有景点', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '   - 订单管理：处理所有订单', options: { fontSize: 16, color: colors.text } }
  ],
  { x: 1.3, y: 2, w: 13.2, h: 5 }
);

// 添加项目收获与展望页
const conclusionSlide = pres.addSlide();
conclusionSlide.background = { color: colors.light };
conclusionSlide.addText('项目收获与展望', { x: 1, y: 1, w: 14, h: 1, fontSize: 32, color: colors.primary, bold: true });
conclusionSlide.addShape(pres.shapes.RECTANGLE, { x: 1, y: 2, w: 0.1, h: 0.8, fill: { color: colors.primary } });

// 项目收获
conclusionSlide.addText('项目收获', { x: 1.3, y: 2, w: 6, h: 0.8, fontSize: 20, color: colors.text, bold: true });
conclusionSlide.addText(
  [
    { text: '- 掌握Django框架的使用，包括模型、视图、模板的开发', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '- 理解MVC架构设计模式，掌握Web应用开发流程', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '- 学习数据库设计与优化，包括表结构设计和关系建立', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '- 提升问题解决能力，学会调试和排查错误', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '- 熟悉前端技术，包括HTML、CSS、JavaScript的使用', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '- 了解API集成，学会调用第三方服务', options: { fontSize: 16, color: colors.text } }
  ],
  { x: 1.3, y: 2.8, w: 6, h: 3.5 }
);

// 未来展望
conclusionSlide.addText('未来展望', { x: 8.3, y: 2, w: 6, h: 0.8, fontSize: 20, color: colors.text, bold: true });
conclusionSlide.addText(
  [
    { text: '- 增加在线支付功能，支持支付宝、微信支付等', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '- 开发移动端应用，提供更好的移动用户体验', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '- 优化系统性能，提高并发处理能力', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '- 添加更多旅游相关功能，如路线规划、攻略分享等', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '- 实现数据分析和预测，辅助景区决策', options: { fontSize: 16, color: colors.text, breakLine: true } },
    { text: '- 加强系统安全性，防止各种攻击', options: { fontSize: 16, color: colors.text } }
  ],
  { x: 8.3, y: 2.8, w: 6, h: 3.5 }
);

// 添加致谢页
const thanksSlide = pres.addSlide();
thanksSlide.background = { color: colors.primary };
thanksSlide.addText(
  [
    { text: '谢谢聆听！', options: { bold: true, fontSize: 48, color: 'FFFFFF', align: 'center', breakLine: true } },
    { text: '欢迎提问', options: { fontSize: 24, color: 'FFFFFF', align: 'center' } }
  ],
  { x: 0.5, y: 2, w: 15, h: 5, valign: 'middle' }
);

// 生成PPT文件
pres.writeFile({ fileName: '旅游票务系统毕业设计答辩.pptx' });
console.log('PPT生成完成！');
