#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中文视频语音识别主程序
支持批量处理视频文件，生成Word文档和SRT字幕
"""

import os
import sys
from pathlib import Path
from typing import List

from audio_extractor import extract_audio
from speech_recognizer import recognize_speech
from text_processor import process_text
from file_generator import generate_docx, generate_srt


def find_video_files(input_dir: str) -> List[str]:
    """查找所有视频文件"""
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.m4v', '.webm']
    video_files = []
    
    input_path = Path(input_dir)
    if not input_path.exists():
        print(f"警告: 输入目录 {input_dir} 不存在，将创建该目录")
        input_path.mkdir(parents=True, exist_ok=True)
        return video_files
    
    for file_path in input_path.rglob('*'):
        if file_path.suffix.lower() in video_extensions:
            video_files.append(str(file_path))
    
    return sorted(video_files)


def process_video(video_path: str, output_dir: str = "output") -> None:
    """处理单个视频文件"""
    print(f"\n开始处理视频: {video_path}")
    
    # 创建输出目录
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # 1. 提取音频
    print("步骤1: 提取音频...")
    audio_path = extract_audio(video_path, output_dir)
    
    # 2. 语音识别
    print("步骤2: 进行语音识别...")
    recognition_results = recognize_speech(audio_path)
    
    # 3. 文本后处理
    print("步骤3: 文本后处理...")
    processed_text, srt_segments = process_text(recognition_results)
    
    # 4. 生成文件 - 在output下创建以原文件名命名的文件夹
    print("步骤4: 生成输出文件...")
    video_name = Path(video_path).stem
    video_output_dir = os.path.join(output_dir, video_name)
    Path(video_output_dir).mkdir(parents=True, exist_ok=True)
    
    docx_path = os.path.join(video_output_dir, f"{video_name}.docx")
    srt_path = os.path.join(video_output_dir, f"{video_name}.srt")
    
    generate_docx(processed_text, docx_path)
    generate_srt(srt_segments, srt_path)
    
    # 5. 清理临时音频文件
    if os.path.exists(audio_path):
        os.remove(audio_path)
    
    print(f"✓ 处理完成: {video_path}")
    print(f"  - Word文档: {docx_path}")
    print(f"  - SRT字幕: {srt_path}")


def main():
    """主函数"""
    input_dir = "input_videos"
    output_dir = "output"
    
    print("=" * 60)
    print("中文视频语音识别系统")
    print("=" * 60)
    
    # 查找所有视频文件
    video_files = find_video_files(input_dir)
    
    if not video_files:
        print(f"\n未在 {input_dir} 目录下找到视频文件")
        print("支持的格式: .mp4, .avi, .mov, .mkv, .flv, .wmv, .m4v, .webm")
        return
    
    print(f"\n找到 {len(video_files)} 个视频文件")
    
    # 处理所有视频
    success_count = 0
    fail_count = 0
    for video_path in video_files:
        try:
            process_video(video_path, output_dir)
            success_count += 1
        except Exception as e:
            print(f"✗ 处理失败 {video_path}: {str(e)}")
            import traceback
            traceback.print_exc()
            fail_count += 1
    
    # 输出处理结果
    print("\n" + "=" * 60)
    print("处理完成")
    print("=" * 60)
    print(f"成功: {success_count} 个")
    print(f"失败: {fail_count} 个")
    print(f"\n✓ 所有输出文件已保存到: {output_dir}/")


if __name__ == "__main__":
    main()

