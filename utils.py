#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具函数模块
包含设备检测、路径处理等工具函数
"""

import platform
import sys
import os


def detect_device():
    """
    检测运行设备并返回合适的设备标识
    
    Returns:
        str: 'cuda', 'mps', 或 'cpu'
    """
    system = platform.system()
    
    # Windows系统 - 检查CUDA
    if system == "Windows":
        try:
            import torch
            if torch.cuda.is_available():
                print(f"检测到CUDA设备: {torch.cuda.get_device_name(0)}")
                return "cuda"
        except ImportError:
            pass
        return "cpu"
    
    # macOS系统 - 检查MPS (Apple Silicon)
    elif system == "Darwin":
        try:
            import torch
            if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                print("检测到Apple Silicon (MPS)")
                return "mps"
        except ImportError:
            pass
        return "cpu"
    
    # Linux系统 - 检查CUDA
    elif system == "Linux":
        try:
            import torch
            if torch.cuda.is_available():
                print(f"检测到CUDA设备: {torch.cuda.get_device_name(0)}")
                return "cuda"
        except ImportError:
            pass
        return "cpu"
    
    return "cpu"


def get_cache_dir():
    """
    获取缓存目录
    Windows系统返回D盘路径，其他系统返回用户目录
    
    Returns:
        str: 缓存目录路径
    """
    system = platform.system()
    
    if system == "Windows":
        # Windows系统使用D盘
        d_drive = "D:"
        if os.path.exists(d_drive):
            cache_dir = os.path.join(d_drive, "PythonCache")
            os.makedirs(cache_dir, exist_ok=True)
            return cache_dir
        else:
            # 如果D盘不存在，使用用户目录
            cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "python")
            os.makedirs(cache_dir, exist_ok=True)
            return cache_dir
    else:
        # macOS和Linux使用用户目录
        cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "python")
        os.makedirs(cache_dir, exist_ok=True)
        return cache_dir


def is_windows():
    """判断是否为Windows系统"""
    return platform.system() == "Windows"


def is_mac():
    """判断是否为macOS系统"""
    return platform.system() == "Darwin"

