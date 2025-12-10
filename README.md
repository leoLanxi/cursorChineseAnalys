# 中文视频语音识别系统

专业的中文视频语音识别助手，支持批量处理视频文件，生成Word文档和SRT字幕。

## 功能特点

- ✅ 支持多种视频格式（mp4, avi, mov, mkv等）
- ✅ 使用FunASR Paraformer高精度中文语音识别模型
- ✅ 自动文本润色和段落整理
- ✅ 生成Word文档（.docx）和SRT字幕（.srt）
- ✅ 批量处理多个视频文件

## 安装要求

### 1. 安装FFmpeg（必需）

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt-get install ffmpeg
```

**Windows:**
下载并安装 [FFmpeg](https://ffmpeg.org/download.html)

### 2. 安装Python依赖

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

- **Word文档**: `output/<视频名>.docx`
- **SRT字幕**: `output/<视频名>.srt`
- **JSON结果**: `output/results.json`

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

### JSON结果格式

```json
[
  {
    "video": "视频文件名.mp4",
    "word_content": "按自然段整理后的中文对白（无时间戳）",
    "srt_content": "完整SRT字幕文本"
  }
]
```

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
├── requirements.txt     # Python依赖
├── input_videos/        # 输入视频目录
└── output/              # 输出目录
```

## 注意事项

1. 首次运行FunASR会自动下载模型（约几百MB），请确保网络连接正常
2. 处理长视频可能需要较长时间，请耐心等待
3. 确保有足够的磁盘空间存储临时音频文件
4. 如果识别效果不理想，可以尝试调整模型参数或使用不同的识别引擎

## 故障排除

### FFmpeg未找到
确保已正确安装FFmpeg，并在命令行中可以运行 `ffmpeg -version`

### 语音识别库未安装
根据你的需求选择安装：
- `pip install funasr` （推荐，中文优化）
- `pip install openai-whisper` （备选）

### 内存不足
如果处理大视频文件时内存不足，可以：
- 使用较小的识别模型
- 分段处理视频

