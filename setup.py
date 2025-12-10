#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
依赖安装脚本
自动检测已安装的依赖，并安装缺失的包
Windows系统会将下载内容保存到D盘
"""

import subprocess
import sys
import os
import platform
from pathlib import Path
from utils import is_windows, get_cache_dir


def check_package_installed(package_name: str) -> bool:
    """检查包是否已安装"""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False


def install_package(package: str, use_cache_dir: bool = False):
    """安装Python包"""
    cmd = [sys.executable, "-m", "pip", "install", package]
    
    if use_cache_dir:
        cache_dir = get_cache_dir()
        # 设置pip缓存目录
        os.environ["PIP_CACHE_DIR"] = cache_dir
        # 设置临时目录
        os.environ["TMPDIR"] = cache_dir
        os.environ["TEMP"] = cache_dir
        os.environ["TMP"] = cache_dir
        print(f"使用缓存目录: {cache_dir}")
    
    try:
        subprocess.check_call(cmd)
        print(f"✓ 成功安装: {package}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ 安装失败: {package}")
        print(f"  错误信息: {e}")
        return False


def check_ffmpeg():
    """检查FFmpeg是否已安装"""
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✓ FFmpeg 已安装")
            return True
    except FileNotFoundError:
        pass
    
    print("✗ FFmpeg 未安装")
    return False


def install_ffmpeg_instructions():
    """显示FFmpeg安装说明"""
    system = platform.system()
    print("\n" + "=" * 60)
    print("FFmpeg 安装说明")
    print("=" * 60)
    
    if system == "Darwin":  # macOS
        print("macOS 安装命令:")
        print("  brew install ffmpeg")
    elif system == "Windows":
        print("Windows 安装方法:")
        print("  1. 下载: https://ffmpeg.org/download.html")
        print("  2. 解压到 D:\\ffmpeg (推荐)")
        print("  3. 将 D:\\ffmpeg\\bin 添加到系统PATH环境变量")
    elif system == "Linux":
        print("Linux 安装命令:")
        print("  sudo apt-get install ffmpeg")
    print("=" * 60 + "\n")


def main():
    """主安装函数"""
    print("=" * 60)
    print("依赖检查和安装")
    print("=" * 60)
    
    system = platform.system()
    is_win = is_windows()
    
    # 检查FFmpeg
    print("\n检查 FFmpeg...")
    ffmpeg_installed = check_ffmpeg()
    if not ffmpeg_installed:
        install_ffmpeg_instructions()
    
    # 定义需要安装的包
    packages = {
        "funasr": "funasr>=1.0.0",
        "docx": "python-docx>=1.0.0",
        "soundfile": "soundfile>=0.12.0",
        "numpy": "numpy>=1.21.0",
    }
    
    # 可选包（如果FunASR不可用，可以使用Whisper）
    optional_packages = {
        "whisper": "openai-whisper>=20231117",
    }
    
    # 检查并安装基础包
    print("\n检查 Python 包...")
    missing_packages = []
    
    for module_name, package_spec in packages.items():
        if check_package_installed(module_name):
            print(f"✓ {module_name} 已安装")
        else:
            print(f"✗ {module_name} 未安装")
            missing_packages.append(package_spec)
    
    # 如果FunASR未安装，询问是否安装Whisper作为备选
    if "funasr" in [p.split(">=")[0] for p in missing_packages]:
        print("\n提示: FunASR未安装，可以选择安装Whisper作为备选")
        response = input("是否安装Whisper? (y/n, 默认n): ").strip().lower()
        if response == 'y':
            if not check_package_installed("whisper"):
                missing_packages.append(optional_packages["whisper"])
    
    # 安装缺失的包
    if missing_packages:
        print(f"\n开始安装 {len(missing_packages)} 个缺失的包...")
        use_cache = is_win  # Windows系统使用缓存目录
        
        for package in missing_packages:
            print(f"\n安装: {package}")
            install_package(package, use_cache_dir=use_cache)
    else:
        print("\n✓ 所有必需的包都已安装")
    
    # 检查PyTorch和CUDA支持（Windows）
    if is_win:
        print("\n检查 PyTorch CUDA 支持...")
        try:
            import torch
            if torch.cuda.is_available():
                print(f"✓ PyTorch CUDA 可用: {torch.cuda.get_device_name(0)}")
            else:
                print("✗ PyTorch CUDA 不可用")
                print("  如果需要CUDA加速，请安装支持CUDA的PyTorch:")
                print("  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")
        except ImportError:
            print("✗ PyTorch 未安装")
            print("  如果需要GPU加速，请安装PyTorch:")
            print("  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")
    
    # 检查MPS支持（macOS）
    if system == "Darwin":
        print("\n检查 PyTorch MPS 支持...")
        try:
            import torch
            if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                print("✓ PyTorch MPS (Apple Silicon) 可用")
            else:
                print("✗ PyTorch MPS 不可用")
        except ImportError:
            print("✗ PyTorch 未安装")
            print("  如果需要GPU加速，请安装PyTorch:")
            print("  pip install torch torchvision torchaudio")
    
    print("\n" + "=" * 60)
    print("依赖检查完成")
    print("=" * 60)


if __name__ == "__main__":
    main()

