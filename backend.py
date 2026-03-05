from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel
import requests
import base64
import uvicorn
import io
import json
import os

app = FastAPI(
    title="智能翻译助手 API",
    description="基于 Ollama 的本地 AI 翻译服务，支持文本和图片翻译。",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_API_URL = "http://192.168.12.161:11434/api/generate"
MODEL_NAME = "translategemma:27b"

class TextRequest(BaseModel):
    text: str
    target_language: str = "zh-Hans"

def process_image_translation(image_bytes: bytes, target_language="zh-Hans") -> str:
    encoded_image = base64.b64encode(image_bytes).decode('utf-8')
    
    prompt = f"""你是一名专业翻译员。请将图片中的文本翻译成{target_language}，保持专业准确性。仅输出译文，不要额外解释。"""
    try:
        response = requests.post(
            OLLAMA_API_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "images": [encoded_image]
            },
            timeout=120  # Set a timeout as LLM processing can take time
        )
        response.raise_for_status()
        return response.json().get("response", "")
    except requests.exceptions.RequestException as e:
        print(f"Error calling Ollama API: {e}")
        raise HTTPException(status_code=500, detail=f"Translation service error: {str(e)}")
    
def process_text_translation(text, target_language="zh-Hans") -> str:
    prompt = f"""你是一名专业翻译员。请将以下文本翻译成{target_language}，保持专业准确性。仅输出译文，不要额外解释。

原文内容：
{text}
"""
    try:
        response = requests.post(
            OLLAMA_API_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
            },
            timeout=120
        )
        response.raise_for_status()
        return response.json().get("response", "")
    except requests.exceptions.RequestException as e:
        print(f"Error calling Ollama API: {e}")
        raise HTTPException(status_code=500, detail=f"Translation service error: {str(e)}")

@app.get("/languages", summary="获取支持的语言列表")
def get_languages():
    try:
        file_path = os.path.join(os.path.dirname(__file__), "language.json")
        with open(file_path, "r", encoding="utf-8") as f:
            languages = json.load(f)
        return languages
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading languages: {str(e)}")

@app.post("/translate_text", summary="文本翻译接口", description="将输入的文本翻译成目标语言（默认中文）")
async def translate_text_endpoint(request: TextRequest):
    """
    文本翻译接口
    
    - **text**: 需要翻译的源文本
    - **target_language**: 目标语言代码，默认为 "zh-Hans"
    """
    try:
        translation = await run_in_threadpool(process_text_translation, request.text, request.target_language)
        return {"translation": translation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/translate")
async def translate(file: UploadFile = File(...), target_language: str = Form("zh-Hans")):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        contents = await file.read()
        translation = await run_in_threadpool(process_image_translation, contents, target_language)
        return {"filename": file.filename, "translation": translation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", summary="健康检查", description="检查 API 服务是否正常运行")
def read_root():
    return {"message": "Image Translation API is running"}

if __name__ == "__main__":
    uvicorn.run("backend:app", host="0.0.0.0", port=9081, reload=True)
