const pptxgen = require("pptxgenjs");

// 创建演示文稿
let pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';
pres.author = '王晓宇';
pres.title = '旅游票务系统毕业设计答辩';

// 颜色方案
const colors = {
  primary: "065A82",  // 深蓝色
  secondary: "1C7293", // 蓝色
  accent: "21295C",   // 深蓝色
  light: "F1F5F9",    // 浅灰色
  text: "1E293B"      // 深灰色
};

// 添加标题页
let titleSlide = pres.addSlide();
titleSlide.background = { color: colors.primary };
titleSlide.addText([
  { text: "旅游票务系统", options: { bold: true, fontSize: 44, color: "FFFFFF", breakLine: true } },
  { text: "毕业设计答辩", options: { fontSize: 28, color: "FFFFFF", breakLine: true } },
  { text: "王晓宇", options: { fontSize: 20, color: "FFFFFF", breakLine: true } },
  { text: "指导教师：XXX", options: { fontSize: 18, color: "FFFFFF" } }
], { x: 0.5, y: 2, w: 9, h: 3, align: "center", valign: "middle" });

// 添加项目概述页
let overviewSlide = pres.addSlide();
overviewSlide.background = { color: colors.light };
overviewSlide.addText("项目概述", { x: 0.5, y: 0.5, w: 9, h: 1, fontSize: 32, color: colors.primary, bold: true });
overviewSlide.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 1.2, w: 0.08, h: 0.8, fill: { color: colors.primary } });
overviewSlide.addText([
  { text: "项目背景：旅游业快速发展，线上票务需求增加", options: { fontSize: 18, color: colors.text, breakLine: true } },
  { text: "项目目标：开发一个功能完整的旅游票务管理系统", options: { fontSize: 18, color: colors.text, breakLine: true } },
  { text: "系统价值：简化购票流程，提高管理效率", options: { fontSize: 18, color: colors.text } }
], { x: 0.8, y: 1.2, w: 8.7, h: 3 });

// 添加技术架构页
let architectureSlide = pres.addSlide();
architectureSlide.background = { color: colors.light };
architectureSlide.addText("技术架构", { x: 0.5, y: 0.5, w: 9, h: 1, fontSize: 32, color: colors.primary, bold: true });
architectureSlide.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 1.2, w: 0.08, h: 0.8, fill: { color: colors.primary } });

// 技术栈
architectureSlide.addText("技术栈", { x: 0.8, y: 1.2, w: 4, h: 0.8, fontSize: 20, color: colors.text, bold: true });
architectureSlide.addText([
  { text: "前端：HTML5, CSS3, JavaScript", options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: "后端：Django, Python", options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: "数据库：SQLite", options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: "API：天气查询API", options: { fontSize: 16, color: colors.text } }
], { x: 0.8, y: 1.8, w: 4, h: 3 });

// MVC架构
architectureSlide.addText("MVC架构", { x: 5.5, y: 1.2, w: 4, h: 0.8, fontSize: 20, color: colors.text, bold: true });
architectureSlide.addText([
  { text: "模型 (Models)：数据结构定义", options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: "视图 (Views)：业务逻辑处理", options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: "模板 (Templates)：页面展示", options: { fontSize: 16, color: colors.text } }
], { x: 5.5, y: 1.8, w: 4, h: 3 });

// 添加系统功能模块页
let featuresSlide = pres.addSlide();
featuresSlide.background = { color: colors.light };
featuresSlide.addText("系统功能模块", { x: 0.5, y: 0.5, w: 9, h: 1, fontSize: 32, color: colors.primary, bold: true });
featuresSlide.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 1.2, w: 0.08, h: 0.8, fill: { color: colors.primary } });

// 功能模块列表
featuresSlide.addText([
  { text: "1. 用户系统", options: { fontSize: 18, color: colors.text, bold: true, breakLine: true } },
  { text: "   - 注册、登录、个人中心", options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: "2. 景点管理", options: { fontSize: 18, color: colors.text, bold: true, breakLine: true } },
  { text: "   - 景点列表、详情、分类筛选", options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: "3. 购票流程", options: { fontSize: 18, color: colors.text, bold: true, breakLine: true } },
  { text: "   - 门票选择、购物车、订单创建、支付", options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: "4. 后台管理", options: { fontSize: 18, color: colors.text, bold: true, breakLine: true } },
  { text: "   - 平台管理员、景点管理员功能", options: { fontSize: 16, color: colors.text } }
], { x: 0.8, y: 1.2, w: 8.7, h: 4 });

// 添加核心功能实现页 - 用户系统
let userSystemSlide = pres.addSlide();
userSystemSlide.background = { color: colors.light };
userSystemSlide.addText("核心功能实现 - 用户系统", { x: 0.5, y: 0.5, w: 9, h: 1, fontSize: 32, color: colors.primary, bold: true });
userSystemSlide.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 1.2, w: 0.08, h: 0.8, fill: { color: colors.primary } });

// 实现细节
userSystemSlide.addText("实现细节", { x: 0.8, y: 1.2, w: 4, h: 0.8, fontSize: 20, color: colors.text, bold: true });
userSystemSlide.addText([
  { text: "• 使用Django内置的认证系统", options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: "• 自定义用户模型，添加角色字段", options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: "• 实现三级权限控制：游客、景点管理员、平台管理员", options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: "• 使用装饰器实现权限验证", options: { fontSize: 16, color: colors.text } }
], { x: 0.8, y: 1.8, w: 4, h: 3 });

// 核心代码
userSystemSlide.addText("核心代码", { x: 5.5, y: 1.2, w: 4, h: 0.8, fontSize: 20, color: colors.text, bold: true });
userSystemSlide.addText([
  { text: "@login_required", options: { fontSize: 14, color: colors.text, breakLine: true } },
  { text: "def personal_center(request):", options: { fontSize: 14, color: colors.text, breakLine: true } },
  { text: "    user = request.user", options: { fontSize: 14, color: colors.text, breakLine: true } },
  { text: "    # 处理用户信息更新", options: { fontSize: 14, color: colors.text } }
], { x: 5.5, y: 1.8, w: 4, h: 3, fontFace: "Consolas" });

// 添加核心功能实现页 - 购票系统
let ticketSystemSlide = pres.addSlide();
ticketSystemSlide.background = { color: colors.light };
ticketSystemSlide.addText("核心功能实现 - 购票系统", { x: 0.5, y: 0.5, w: 9, h: 1, fontSize: 32, color: colors.primary, bold: true });
ticketSystemSlide.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 1.2, w: 0.08, h: 0.8, fill: { color: colors.primary } });

// 实现流程
let flowSteps = [
  { text: "1. 选择景点和门票类型", options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: "2. 选择使用日期", options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: "3. 检查库存", options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: "4. 创建订单", options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: "5. 支付", options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: "6. 生成订单", options: { fontSize: 16, color: colors.text } }
];
ticketSystemSlide.addText(flowSteps, { x: 0.8, y: 1.2, w: 8.7, h: 4 });

// 添加核心功能实现页 - 后台管理
let adminSystemSlide = pres.addSlide();
adminSystemSlide.background = { color: colors.light };
adminSystemSlide.addText("核心功能实现 - 后台管理", { x: 0.5, y: 0.5, w: 9, h: 1, fontSize: 32, color: colors.primary, bold: true });
adminSystemSlide.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 1.2, w: 0.08, h: 0.8, fill: { color: colors.primary } });

// 平台管理员功能
adminSystemSlide.addText("平台管理员功能", { x: 0.8, y: 1.2, w: 4, h: 0.8, fontSize: 20, color: colors.text, bold: true });
adminSystemSlide.addText([
  { text: "• 用户管理：增删改查用户", options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: "• 景点管理：审核、管理景点", options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: "• 订单管理：查看所有订单", options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: "• 评论管理：回复、删除评论", options: { fontSize: 16, color: colors.text } }
], { x: 0.8, y: 1.8, w: 4, h: 3 });

// 景点管理员功能
adminSystemSlide.addText("景点管理员功能", { x: 5.5, y: 1.2, w: 4, h: 0.8, fontSize: 20, color: colors.text, bold: true });
adminSystemSlide.addText([
  { text: "• 景点管理：添加、编辑景点", options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: "• 门票管理：设置门票类型和库存", options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: "• 订单管理：查看景点订单", options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: "• 评论管理：回复游客评论", options: { fontSize: 16, color: colors.text } }
], { x: 5.5, y: 1.8, w: 4, h: 3 });

// 添加系统特色页
let featuresSlide2 = pres.addSlide();
featuresSlide2.background = { color: colors.light };
featuresSlide2.addText("系统特色", { x: 0.5, y: 0.5, w: 9, h: 1, fontSize: 32, color: colors.primary, bold: true });
featuresSlide2.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 1.2, w: 0.08, h: 0.8, fill: { color: colors.primary } });

// 特色列表
featuresSlide2.addText([
  { text: "1. 实时库存管理", options: { fontSize: 18, color: colors.text, bold: true, breakLine: true } },
  { text: "   - 按日期管理门票库存，确保数据准确性", options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: "2. 天气查询集成", options: { fontSize: 18, color: colors.text, bold: true, breakLine: true } },
  { text: "   - 购票时查询景点天气，提升用户体验", options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: "3. 多级权限管理", options: { fontSize: 18, color: colors.text, bold: true, breakLine: true } },
  { text: "   - 不同角色拥有不同权限，确保系统安全", options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: "4. 响应式设计", options: { fontSize: 18, color: colors.text, bold: true, breakLine: true } },
  { text: "   - 适配不同设备，提供良好的用户体验", options: { fontSize: 16, color: colors.text } }
], { x: 0.8, y: 1.2, w: 8.7, h: 4 });

// 添加数据库设计页
let databaseSlide = pres.addSlide();
databaseSlide.background = { color: colors.light };
databaseSlide.addText("数据库设计", { x: 0.5, y: 0.5, w: 9, h: 1, fontSize: 32, color: colors.primary, bold: true });
databaseSlide.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 1.2, w: 0.08, h: 0.8, fill: { color: colors.primary } });

// 主要数据表
let tables = [
  { text: "• User - 用户表", options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: "• ScenicSpot - 景点表", options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: "• TicketType - 门票类型表", options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: "• Order - 订单表", options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: "• Cart - 购物车表", options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: "• ScenicSpotComment - 评论表", options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: "• DateStock - 日期库存表", options: { fontSize: 16, color: colors.text } }
];
databaseSlide.addText(tables, { x: 0.8, y: 1.2, w: 8.7, h: 4 });

// 添加系统演示页
let demoSlide = pres.addSlide();
demoSlide.background = { color: colors.light };
demoSlide.addText("系统演示", { x: 0.5, y: 0.5, w: 9, h: 1, fontSize: 32, color: colors.primary, bold: true });
demoSlide.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 1.2, w: 0.08, h: 0.8, fill: { color: colors.primary } });
demoSlide.addText([
  { text: "• 首页展示：轮播图、热门景点、最新资讯", options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: "• 景点列表：分类筛选、搜索功能", options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: "• 景点详情：景点信息、评论、购票入口", options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: "• 购票流程：选择门票、日期、数量，创建订单", options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: "• 个人中心：个人信息、订单管理、收藏", options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: "• 后台管理：用户、景点、订单管理", options: { fontSize: 16, color: colors.text } }
], { x: 0.8, y: 1.2, w: 8.7, h: 4 });

// 添加项目收获与展望页
let conclusionSlide = pres.addSlide();
conclusionSlide.background = { color: colors.light };
conclusionSlide.addText("项目收获与展望", { x: 0.5, y: 0.5, w: 9, h: 1, fontSize: 32, color: colors.primary, bold: true });
conclusionSlide.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 1.2, w: 0.08, h: 0.8, fill: { color: colors.primary } });

// 项目收获
conclusionSlide.addText("项目收获", { x: 0.8, y: 1.2, w: 4, h: 0.8, fontSize: 20, color: colors.text, bold: true });
conclusionSlide.addText([
  { text: "• 掌握Django框架的使用", options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: "• 理解MVC架构设计模式", options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: "• 学习数据库设计与优化", options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: "• 提升问题解决能力", options: { fontSize: 16, color: colors.text } }
], { x: 0.8, y: 1.8, w: 4, h: 3 });

// 未来展望
conclusionSlide.addText("未来展望", { x: 5.5, y: 1.2, w: 4, h: 0.8, fontSize: 20, color: colors.text, bold: true });
conclusionSlide.addText([
  { text: "• 增加在线支付功能", options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: "• 开发移动端应用", options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: "• 优化系统性能", options: { fontSize: 16, color: colors.text, breakLine: true } },
  { text: "• 添加更多旅游相关功能", options: { fontSize: 16, color: colors.text } }
], { x: 5.5, y: 1.8, w: 4, h: 3 });

// 添加致谢页
let thanksSlide = pres.addSlide();
thanksSlide.background = { color: colors.primary };
thanksSlide.addText([
  { text: "谢谢聆听！", options: { bold: true, fontSize: 44, color: "FFFFFF", breakLine: true } },
  { text: "欢迎提问", options: { fontSize: 24, color: "FFFFFF" } }
], { x: 0.5, y: 2, w: 9, h: 3, align: "center", valign: "middle" });

// 生成PPT文件
pres.writeFile({ fileName: "旅游票务系统毕业设计答辩.pptx" });
console.log("PPT生成完成！");
