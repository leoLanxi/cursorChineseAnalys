#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文本后处理模块
对识别结果进行润色、分段、整理
"""

import re
from typing import List, Dict, Tuple


def process_text(recognition_results: List[Dict]) -> Tuple[str, List[Dict]]:
    """
    处理识别结果，生成Word文档内容和SRT字幕内容
    
    Args:
        recognition_results: 识别结果列表
    
    Returns:
        (word_content, srt_segments)
        - word_content: 用于Word文档的文本（无时间戳，自然段落）
        - srt_segments: 用于SRT字幕的段落列表（带时间戳）
    """
    if not recognition_results:
        return "", []
    
    # 1. 清理和润色文本
    cleaned_segments = []
    for seg in recognition_results:
        text = seg.get('text', '').strip()
        if not text:
            continue
        
        # 清理文本
        text = clean_text(text)
        
        # 轻度润色（去除重复、口语化处理）
        text = polish_text(text)
        
        if text:
            cleaned_segments.append({
                'text': text,
                'start': seg.get('start', 0.0),
                'end': seg.get('end', 0.0)
            })
    
    # 2. 生成SRT字幕段落（保持时间戳，适当拆分长句）
    srt_segments = generate_srt_segments(cleaned_segments)
    
    # 3. 生成Word文档内容（无时间戳，自然段落）
    word_content = generate_word_content(cleaned_segments)
    
    return word_content, srt_segments


def clean_text(text: str) -> str:
    """清理文本，移除噪声标记等"""
    # 移除常见的噪声标记
    noise_patterns = [
        r'\[.*?\]',  # [音乐], [笑声] 等
        r'\(.*?\)',  # (环境音) 等
        r'【.*?】',  # 【音乐】等
    ]
    
    for pattern in noise_patterns:
        text = re.sub(pattern, '', text)
    
    # 移除多余空格
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()


def polish_text(text: str) -> str:
    """轻度润色文本，去除口语重复等"""
    # 去除重复的词语（如"然后然后" -> "然后"）
    text = re.sub(r'([\u4e00-\u9fa5，。！？、])\1{2,}', r'\1', text)
    
    # 去除常见的口语重复模式
    patterns = [
        (r'然后然后+', '然后'),
        (r'就是就是+', '就是'),
        (r'那个那个+', '那个'),
        (r'这个这个+', '这个'),
        (r'我我我+', '我'),
        (r'你你你+', '你'),
        (r'他他他+', '他'),
        (r'嗯嗯+', '嗯'),
        (r'啊+', '啊'),
    ]
    
    for pattern, replacement in patterns:
        text = re.sub(pattern, replacement, text)
    
    # 清理标点符号重复
    text = re.sub(r'([，。！？])\1+', r'\1', text)
    
    return text.strip()


def generate_srt_segments(segments: List[Dict]) -> List[Dict]:
    """生成SRT字幕段落，适当拆分长句"""
    srt_segments = []
    
    for seg in segments:
        text = seg['text']
        start = seg['start']
        end = seg['end']
        
        # 如果句子过长（超过30个字符），尝试拆分
        if len(text) > 30:
            # 按标点符号拆分
            sentences = re.split(r'([。！？])', text)
            sentences = [s for s in sentences if s.strip()]
            
            # 重新组合，每句不超过30字符
            current_sentence = ""
            sentence_start = start
            duration = end - start if end > start else 1.0
            
            for i, part in enumerate(sentences):
                if len(current_sentence + part) <= 30:
                    current_sentence += part
                else:
                    if current_sentence:
                        # 计算时间
                        sentence_end = sentence_start + (duration * len(current_sentence) / len(text))
                        srt_segments.append({
                            'text': current_sentence.strip(),
                            'start': sentence_start,
                            'end': sentence_end
                        })
                        sentence_start = sentence_end
                    current_sentence = part
            
            # 添加最后一句
            if current_sentence:
                srt_segments.append({
                    'text': current_sentence.strip(),
                    'start': sentence_start,
                    'end': end
                })
        else:
            # 短句直接添加
            srt_segments.append({
                'text': text,
                'start': start,
                'end': end
            })
    
    return srt_segments


def generate_word_content(segments: List[Dict]) -> str:
    """生成Word文档内容，按自然段落组织"""
    if not segments:
        return ""
    
    # 合并文本（忽略时间戳）
    all_text = ' '.join([seg['text'] for seg in segments])
    
    # 按标点符号分段
    paragraphs = []
    current_para = ""
    
    # 按句号、问号、感叹号分段
    sentences = re.split(r'([。！？])', all_text)
    sentences = [s for s in sentences if s.strip()]
    
    for i, sentence in enumerate(sentences):
        current_para += sentence
        
        # 如果遇到句号、问号、感叹号，且当前段落已有一定长度，开始新段落
        if sentence in ['。', '！', '？']:
            if len(current_para.strip()) > 50:  # 段落长度阈值
                paragraphs.append(current_para.strip())
                current_para = ""
    
    # 添加最后一段
    if current_para.strip():
        paragraphs.append(current_para.strip())
    
    # 如果段落太少，合并一些
    if len(paragraphs) == 0:
        paragraphs = [all_text]
    
    # 合并成最终文本，段落之间用换行分隔
    word_content = '\n\n'.join(paragraphs)
    
    # 清理多余空格
    word_content = re.sub(r'\s+', ' ', word_content)
    word_content = re.sub(r'\n\s+', '\n', word_content)
    
    return word_content.strip()

