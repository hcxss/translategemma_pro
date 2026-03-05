# 智能翻译助手 (AI Translator)

这是一个基于 **FastAPI** 和 **Ollama** 的本地智能翻译工具，提供现代化、响应式的 Web 界面。项目支持 **图片翻译**（OCR + 翻译）和 **文本翻译**，并且支持动态加载 100+ 种目标语言。

<img width="1092" height="903" alt="image" src="https://github.com/user-attachments/assets/5e20ab90-4ed5-4028-857b-ded010aa5003" />




## ✨ 功能特点

- **多模态智能翻译**：
  - 📸 **图片翻译**：上传图片（支持拖拽），系统自动识别并翻译图片中的文字。
  - 📝 **文本翻译**：直接输入文本进行快速翻译。
- **动态多语言支持**：
  - 前端自动从后端获取支持的语言列表（基于 `language.json`）。
  - 下拉框显示“语言名称 (代码)”，方便用户选择。
  - 默认目标语言为 **Chinese (zh-Hans)**。
- **现代化 UI/UX**：
  - 简洁的卡片式设计，支持实时加载状态反馈。
  - 图片上传后支持实时预览。
- **数据隐私安全**：
  - 完全基于本地 Ollama 模型运行，数据不上传至第三方云服务。

## 📂 项目结构

```
e:\project\faster-whisper\
├── backend.py        # FastAPI 后端服务：处理翻译请求、调用 Ollama API
├── index.html        # 前端界面：包含 HTML/CSS/JS，处理用户交互
├── language.json     # 语言配置文件：定义支持的语言代码和名称 (如 "zh-Hans": "中文（简体）")
└── readme.md         # 项目说明文档
```

## 🛠 技术栈

- **后端**：Python 3.8+, FastAPI, Uvicorn, Requests
- **前端**：原生 HTML5, CSS3, JavaScript (Fetch API)
- **AI 模型**：Ollama (`translategemma:27b`)

## � 快速开始

### 1. 环境准备

确保已安装 Python 3.8+ 和 Ollama 服务。

**安装 Python 依赖**：
```bash
pip install fastapi uvicorn requests python-multipart pydantic
```

**Ollama 设置**：
确保 Ollama 服务正在运行，并已拉取 `translategemma:27b` 模型（或在 `backend.py` 中修改为其他模型）。

### 2. 启动后端

```bash
python backend.py
```
服务启动后默认监听：`http://0.0.0.0:9081`

### 3. 访问前端

直接在浏览器中打开项目目录下的 `index.html` 文件即可。

> **⚠️ 注意**：默认前端代码配置连接到 `http://127.0.0.1:9081`。如果您的后端在本地运行 (`localhost`)，请编辑 `index.html` 中的 API 地址。

## 🔌 API 接口文档

后端服务提供以下 RESTful API 接口：

| 方法 | 路径 | 功能描述 | 请求参数 / Body |
|------|------|----------|----------------|
| `GET` | `/languages` | 获取支持语言列表 | 无 |
| `POST` | `/translate` | 图片翻译 | **Form Data**: <br>- `file`: 图片文件 (Binary)<br>- `target_language`: 目标语言代码 (如 `zh-Hans`) |
| `POST` | `/translate_text` | 文本翻译 | **JSON Body**: <br>`{ "text": "Hello", "target_language": "zh-Hans" }` |
| `GET` | `/` | 服务健康检查 | 无 |

### 接口示例

**1. 获取语言列表**
```json
GET /languages
Response:
{
  "en": "英语",
  "zh-Hans": "中文（简体）",
  ...
}
```

**2. 文本翻译**
```json
POST /translate_text
Content-Type: application/json

{
    "text": "This is a test.",
    "target_language": "zh-Hans"
}
```

## ⚙️ 配置指南

### 修改 Ollama 地址
编辑 `backend.py` 中的 `OLLAMA_API_URL`：
```python
# 默认为
OLLAMA_API_URL = "http://127.0.0.1:11434/api/generate"
```

### 修改默认语言
虽然前端默认选中 `zh-Hans`，但你可以在 `backend.py` 中修改 `TextRequest` 模型和 `translate` 函数的默认参数来改变后端默认行为。

### 扩展语言支持
编辑 `language.json` 文件即可添加或修改支持的语言。格式为 `"语言代码": "语言名称"`。前端会自动读取并更新下拉列表。
