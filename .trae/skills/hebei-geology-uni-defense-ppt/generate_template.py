#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
河北地质大学华信学院毕业设计答辩PPT模板生成器
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.oxml.ns import nsdecls
from pptx.oxml import parse_xml

# 配色方案
COLORS = {
    'primary': RGBColor(0, 51, 102),      # 深蓝色 #003366
    'secondary': RGBColor(255, 215, 0),    # 金色 #FFD700
    'accent': RGBColor(0, 128, 192),       # 浅蓝色 #0080C0
    'background': RGBColor(255, 255, 255), # 白色 #FFFFFF
    'text': RGBColor(51, 51, 51),          # 深灰色 #333333
    'light_text': RGBColor(255, 255, 255)  # 白色文本
}

def set_slide_background(slide, color):
    """设置幻灯片背景"""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_logo_placeholder(slide):
    """添加学校标志占位符"""
    # 添加标志占位符
    left = Inches(1)
    top = Inches(0.5)
    width = Inches(2)
    height = Inches(2)
    slide.shapes.add_textbox(left, top, width, height).text = "[学校标志]"

def add_footer(slide, text):
    """添加页脚"""
    left = Inches(1)
    top = Inches(6.5)
    width = Inches(11.333)
    height = Inches(0.5)
    textbox = slide.shapes.add_textbox(left, top, width, height)
    textbox.text = text
    textbox.text_frame.paragraphs[0].font.size = Pt(12)
    textbox.text_frame.paragraphs[0].font.color.rgb = COLORS['text']
    textbox.text_frame.paragraphs[0].alignment = 1  # 居中

def create_template():
    """创建PPT模板"""
    # 创建空白演示文稿
    prs = Presentation()
    
    # 设置幻灯片大小为16:9
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # 1. 封面幻灯片
    slide_layout = prs.slide_layouts[0]  # 标题幻灯片
    slide = prs.slides.add_slide(slide_layout)
    
    # 设置背景
    set_slide_background(slide, COLORS['primary'])
    
    # 添加标志
    add_logo_placeholder(slide)
    
    # 标题
    title = slide.shapes.title
    title.text = "毕业设计答辩"
    title.text_frame.paragraphs[0].font.size = Pt(48)
    title.text_frame.paragraphs[0].font.color.rgb = COLORS['light_text']
    title.text_frame.paragraphs[0].alignment = 1  # 居中
    
    # 副标题
    subtitle = slide.placeholders[1]
    subtitle.text = "河北地质大学华信学院\n论文题目\n作者：XXX\n导师：XXX\n日期：2026年6月"
    subtitle.text_frame.paragraphs[0].font.size = Pt(24)
    subtitle.text_frame.paragraphs[0].font.color.rgb = COLORS['light_text']
    subtitle.text_frame.paragraphs[0].alignment = 1  # 居中
    
    # 2. 目录幻灯片
    slide_layout = prs.slide_layouts[1]  # 标题和内容
    slide = prs.slides.add_slide(slide_layout)
    
    # 设置背景
    set_slide_background(slide, COLORS['background'])
    
    # 标题
    title = slide.shapes.title
    title.text = "目录"
    title.text_frame.paragraphs[0].font.size = Pt(36)
    title.text_frame.paragraphs[0].font.color.rgb = COLORS['primary']
    title.text_frame.paragraphs[0].alignment = 1  # 居中
    
    # 添加装饰线条
    left = Inches(3)
    top = Inches(2)
    width = Inches(7.333)
    height = Inches(0.1)
    shape = slide.shapes.add_shape(
        autoshape_type_id=1,  # 矩形
        left=left, top=top, width=width, height=height
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = COLORS['secondary']
    
    # 内容
    content = slide.placeholders[1]
    content.text = "1. 选题背景\n2. 研究目标\n3. 研究方法\n4. 研究过程\n5. 结果分析\n6. 结论与建议\n7. 致谢\n8. 参考文献"
    content.text_frame.paragraphs[0].font.size = Pt(20)
    content.text_frame.paragraphs[0].font.color.rgb = COLORS['text']
    
    # 添加页脚
    add_footer(slide, "河北地质大学华信学院 · 毕业设计答辩")
    
    # 3-10. 内容幻灯片
    sections = [
        ("一、选题背景", "• 研究背景\n• 研究意义\n• 国内外研究现状\n• 研究问题的提出"),
        ("二、研究目标", "• 研究目的\n• 研究内容\n• 研究假设\n• 研究创新点"),
        ("三、研究方法", "• 研究设计\n• 数据收集方法\n• 数据分析方法\n• 研究工具"),
        ("四、研究过程", "• 研究步骤\n• 实施过程\n• 遇到的问题及解决方法\n• 数据收集与整理"),
        ("五、结果分析", "• 研究结果\n• 数据分析\n• 结果讨论\n• 图表展示"),
        ("六、结论与建议", "• 研究结论\n• 实践意义\n• 局限性\n• 未来研究建议"),
        ("七、致谢", "• 感谢导师的悉心指导\n• 感谢同学的帮助与支持\n• 感谢家人的理解与鼓励\n• 感谢相关单位的支持"),
        ("八、参考文献", "[1] 作者. 书名[M]. 出版社, 出版年份.\n[2] 作者. 文章标题[J]. 期刊名称, 年份, 卷(期): 页码.\n[3] 作者. 网页标题[EB/OL]. URL, 访问日期.\n[4] 其他参考文献...")
    ]
    
    for i, (title_text, content_text) in enumerate(sections):
        slide_layout = prs.slide_layouts[1]
        slide = prs.slides.add_slide(slide_layout)
        
        # 设置背景
        set_slide_background(slide, COLORS['background'])
        
        # 标题
        title = slide.shapes.title
        title.text = title_text
        title.text_frame.paragraphs[0].font.size = Pt(32)
        title.text_frame.paragraphs[0].font.color.rgb = COLORS['primary']
        
        # 添加装饰线条
        left = Inches(1)
        top = Inches(1.5)
        width = Inches(2)
        height = Inches(0.1)
        shape = slide.shapes.add_shape(
            autoshape_type_id=1,  # 矩形
            left=left, top=top, width=width, height=height
        )
        shape.fill.solid()
        shape.fill.fore_color.rgb = COLORS['accent']
        
        # 内容
        content = slide.placeholders[1]
        content.text = content_text
        if i == 7:  # 参考文献
            content.text_frame.paragraphs[0].font.size = Pt(18)
        else:
            content.text_frame.paragraphs[0].font.size = Pt(20)
        content.text_frame.paragraphs[0].font.color.rgb = COLORS['text']
        
        # 添加页脚
        add_footer(slide, "河北地质大学华信学院 · 毕业设计答辩")
    
    # 保存模板
    template_path = "河北地质大学华信学院毕业设计答辩模板.pptx"
    prs.save(template_path)
    print(f"模板已生成：{template_path}")
    return template_path

if __name__ == "__main__":
    create_template()