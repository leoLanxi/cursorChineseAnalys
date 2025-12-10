#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语音识别模块
使用FunASR Paraformer进行高精度中文语音识别
"""

import os
from typing import List, Dict
import numpy as np
from utils import detect_device


def recognize_speech(audio_path: str) -> List[Dict]:
    """
    识别音频中的中文语音
    
    Args:
        audio_path: 音频文件路径
    
    Returns:
        识别结果列表，每个元素包含:
        {
            'text': '识别的文本',
            'start': 开始时间(秒),
            'end': 结束时间(秒)
        }
    """
    try:
        # 尝试使用FunASR
        return recognize_with_funasr(audio_path)
    except ImportError:
        try:
            # 如果FunASR不可用，尝试使用Whisper
            return recognize_with_whisper(audio_path)
        except ImportError:
            raise Exception(
                "未找到语音识别库。请安装以下之一:\n"
                "  pip install funasr (推荐，中文优化)\n"
                "  或 pip install openai-whisper"
            )


def recognize_with_funasr(audio_path: str) -> List[Dict]:
    """使用FunASR Paraformer进行识别"""
    from funasr import AutoModel
    
    # 自动检测设备
    device = detect_device()
    print(f"使用设备: {device}")
    
    # 初始化模型（首次运行会自动下载）
    # 使用Paraformer模型，对中文有专门优化
    try:
        # 尝试使用带时间戳的模型
        model = AutoModel(
            model="paraformer-zh",
            model_revision="v2.0.4",
            device=device,
            vad_model="fsmn-vad",
            vad_model_revision="v2.0.4",
            punc_model="ct-punc",
            punc_model_revision="v2.0.4"
        )
    except:
        # 如果完整模型加载失败，使用基础模型
        model = AutoModel(
            model="paraformer-zh",
            model_revision="v2.0.4",
            device=device
        )
    
    # 进行识别
    try:
        result = model.generate(
            input=audio_path,
            cache={},
            language="zh",
            use_itn=True,  # 使用逆文本归一化
        )
    except Exception as e:
        # 如果带参数失败，尝试简单调用
        result = model.generate(input=audio_path)
    
    # 解析结果
    segments = []
    
    # FunASR返回格式可能是多种形式
    if isinstance(result, list):
        for item in result:
            if isinstance(item, dict):
                text = item.get('text', '') or item.get('pred', '')
                # 尝试获取时间戳
                timestamp = item.get('timestamp', [])
                if timestamp and len(timestamp) >= 2:
                    start = float(timestamp[0])
                    end = float(timestamp[1])
                else:
                    # 如果没有时间戳，尝试从其他字段获取
                    start = item.get('start', 0.0)
                    end = item.get('end', 0.0)
                
                if text:
                    segments.append({
                        'text': text.strip(),
                        'start': start,
                        'end': end
                    })
            elif isinstance(item, str):
                if item.strip():
                    segments.append({
                        'text': item.strip(),
                        'start': 0.0,
                        'end': 0.0
                    })
    elif isinstance(result, dict):
        text = result.get('text', '') or result.get('pred', '')
        timestamp = result.get('timestamp', [])
        if text:
            if timestamp and len(timestamp) >= 2:
                segments.append({
                    'text': text.strip(),
                    'start': float(timestamp[0]),
                    'end': float(timestamp[1])
                })
            else:
                segments.append({
                    'text': text.strip(),
                    'start': 0.0,
                    'end': 0.0
                })
    elif isinstance(result, str):
        if result.strip():
            segments.append({
                'text': result.strip(),
                'start': 0.0,
                'end': 0.0
            })
    
    # 如果没有时间戳，尝试根据音频长度估算
    if segments and segments[0]['end'] == 0.0:
        try:
            import soundfile as sf
            data, samplerate = sf.read(audio_path)
            duration = len(data) / samplerate
            # 简单平均分配时间
            if len(segments) > 1:
                segment_duration = duration / len(segments)
                for i, seg in enumerate(segments):
                    seg['start'] = i * segment_duration
                    seg['end'] = (i + 1) * segment_duration
            else:
                segments[0]['end'] = duration
        except:
            pass
    
    return segments if segments else [{'text': '', 'start': 0.0, 'end': 0.0}]


def recognize_with_whisper(audio_path: str) -> List[Dict]:
    """使用OpenAI Whisper进行识别（备用方案）"""
    import whisper
    from utils import detect_device
    
    # 自动检测设备
    device = detect_device()
    print(f"使用设备: {device}")
    
    # 加载模型（使用medium模型，对中文支持较好）
    # Whisper会自动使用可用的GPU
    model = whisper.load_model("medium", device=device)
    
    # 进行识别（带时间戳）
    result = model.transcribe(
        audio_path,
        language="zh",
        task="transcribe",
        word_timestamps=False
    )
    
    # 解析结果
    segments = []
    for segment in result.get("segments", []):
        segments.append({
            'text': segment.get('text', '').strip(),
            'start': segment.get('start', 0.0),
            'end': segment.get('end', 0.0)
        })
    
    return segments

