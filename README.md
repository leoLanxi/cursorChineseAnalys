# 中文视频语音识别系统

专业的中文视频语音识别助手，支持批量处理视频文件，生成Word文档和SRT字幕。

**当前分支**: mac (macOS M1 Max MPS加速)

## 功能特点

- ✅ 支持多种视频格式（mp4, avi, mov, mkv等）
- ✅ 使用FunASR Paraformer高精度中文语音识别模型
- ✅ 自动文本润色和段落整理
- ✅ 生成Word文档（.docx）和SRT字幕（.srt）
- ✅ 批量处理多个视频文件
- ✅ 自动检测并使用MPS加速（Apple Silicon）

## 安装要求

### 1. 安装FFmpeg（必需）

**macOS:**
```bash
brew install ffmpeg
```

### 2. 安装Python依赖

**方法1: 使用自动安装脚本（推荐）**
```bash
python setup.py
```

脚本会自动检查已安装的依赖，并安装缺失的包。

**方法2: 手动安装**
```bash
pip install -r requirements.txt
```

**推荐使用FunASR（中文优化）:**
```bash
pip install funasr
```

**或者使用Whisper（备选）:**
```bash
pip install openai-whisper
```

**GPU加速支持:**
- **macOS (MPS)**: `pip install torch torchvision torchaudio`
- **CPU only**: `pip install torch torchvision torchaudio`

## 使用方法

### 1. 准备视频文件

将需要识别的视频文件放入 `input_videos` 文件夹：

```bash
mkdir input_videos
# 将视频文件复制到 input_videos 目录
```

### 2. 运行识别程序

```bash
python main.py
```

### 3. 查看结果

- **Word文档**: `output/<视频名>/<视频名>.docx`
- **SRT字幕**: `output/<视频名>/<视频名>.srt`

每个视频的输出文件都保存在以视频文件名命名的独立文件夹中。

## 输出格式

### Word文档特点
- 无时间戳
- 自然段落形式
- 自动合并同一主题的短句
- 语言润色，便于阅读

### SRT字幕特点
- 保留精准时间戳
- 保持自然中文表达
- 适当分行，一句不宜过长

## 分支说明

本项目有两个分支，针对不同的运行环境：

- **main分支**: Windows 11 + RTX 5060Ti (CUDA加速)
- **mac分支**: macOS M1 Max (MPS加速) ← 当前分支

请根据你的运行环境切换到对应的分支。

## 识别规则

- 仅保留中文对白（普通话或方言的标准写法）
- 忽略噪声、环境音、音乐、无法识别内容
- 轻度润色口语重复（如"然后然后" → "然后"）
- 自动拆分不同语义的句子
- 不引入臆造内容，只基于识别结果做语言润色

## 项目结构

```
vedioAnayls/
├── main.py              # 主程序
├── audio_extractor.py   # 音频提取模块
├── speech_recognizer.py # 语音识别模块
├── text_processor.py    # 文本后处理模块
├── file_generator.py    # 文件生成模块
├── utils.py             # 工具函数（设备检测等）
├── setup.py             # 依赖安装脚本
├── requirements.txt     # Python依赖
├── input_videos/        # 输入视频目录
└── output/              # 输出目录
    └── <视频名>/        # 每个视频的输出文件夹
        ├── <视频名>.docx
        └── <视频名>.srt
```

## macOS特定说明

### MPS加速
- 系统会自动检测Apple Silicon (M1/M2/M3)
- 如果检测到MPS设备，会自动使用GPU加速
- 确保已安装支持MPS的PyTorch版本

## 注意事项

1. 首次运行FunASR会自动下载模型（约几百MB），请确保网络连接正常
2. 处理长视频可能需要较长时间，请耐心等待
3. 确保有足够的磁盘空间存储临时音频文件
4. 如果识别效果不理想，可以尝试调整模型参数或使用不同的识别引擎

## 故障排除

### FFmpeg未找到
确保已正确安装FFmpeg，并在命令行中可以运行 `ffmpeg -version`

### 语音识别库未安装
运行 `python setup.py` 自动安装，或手动安装：
- `pip install funasr` （推荐，中文优化）
- `pip install openai-whisper` （备选）

### MPS不可用
1. 确保使用的是Apple Silicon Mac (M1/M2/M3)
2. 安装支持MPS的PyTorch: `pip install torch torchvision torchaudio`
3. 验证: `python -c "import torch; print(torch.backends.mps.is_available())"`

### 内存不足
如果处理大视频文件时内存不足，可以：
- 使用较小的识别模型
- 分段处理视频
