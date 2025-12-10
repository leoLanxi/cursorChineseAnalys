#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件生成模块
生成Word文档和SRT字幕文件
"""

from pathlib import Path
from typing import List, Dict


def generate_docx(content: str, output_path: str):
    """
    生成Word文档
    
    Args:
        content: 文档内容（纯文本）
        output_path: 输出文件路径
    """
    try:
        from docx import Document
        from docx.shared import Pt
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        
        # 创建文档
        doc = Document()
        
        # 设置中文字体
        style = doc.styles['Normal']
        font = style.font
        font.name = '宋体'
        font.size = Pt(12)
        
        # 添加内容
        # 按段落分割
        paragraphs = content.split('\n\n')
        for para_text in paragraphs:
            if para_text.strip():
                para = doc.add_paragraph(para_text.strip())
                para.alignment = WD_ALIGN_PARAGRAPH.LEFT
        
        # 保存文档
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        doc.save(output_path)
        
    except ImportError:
        # 如果python-docx不可用，生成简单的文本文件
        with open(output_path.replace('.docx', '.txt'), 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"警告: python-docx未安装，已生成文本文件: {output_path.replace('.docx', '.txt')}")
        print("安装命令: pip install python-docx")


def generate_srt(segments: List[Dict], output_path: str):
    """
    生成SRT字幕文件
    
    Args:
        segments: 字幕段落列表，每个元素包含:
            {
                'text': '字幕文本',
                'start': 开始时间(秒),
                'end': 结束时间(秒)
            }
        output_path: 输出文件路径
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, seg in enumerate(segments, 1):
            start_time = format_timestamp(seg['start'])
            end_time = format_timestamp(seg['end'])
            text = seg['text'].strip()
            
            if text:
                f.write(f"{i}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{text}\n")
                f.write("\n")


def format_timestamp(seconds: float) -> str:
    """
    将秒数转换为SRT时间戳格式 (HH:MM:SS,mmm)
    
    Args:
        seconds: 秒数
    
    Returns:
        格式化的时间戳字符串
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

