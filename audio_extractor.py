#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音频提取模块
从视频文件中提取音频
"""

import os
from pathlib import Path
import subprocess


def extract_audio(video_path: str, output_dir: str = "temp") -> str:
    """
    从视频文件中提取音频
    
    Args:
        video_path: 视频文件路径
        output_dir: 输出目录
    
    Returns:
        提取的音频文件路径
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    video_name = Path(video_path).stem
    audio_path = os.path.join(output_dir, f"{video_name}_audio.wav")
    
    # 使用ffmpeg提取音频
    # 转换为16kHz单声道WAV格式，适合语音识别
    cmd = [
        'ffmpeg',
        '-i', video_path,
        '-ar', '16000',  # 采样率16kHz
        '-ac', '1',      # 单声道
        '-y',            # 覆盖已存在文件
        audio_path
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return audio_path
    except subprocess.CalledProcessError as e:
        raise Exception(f"音频提取失败: {e.stderr.decode('utf-8', errors='ignore')}")
    except FileNotFoundError:
        raise Exception("未找到ffmpeg，请先安装ffmpeg: brew install ffmpeg (macOS) 或 apt-get install ffmpeg (Linux)")

