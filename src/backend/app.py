from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from src.backend.chat_service import chat

app = FastAPI()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'backend', 'templates')

app.mount('/static', StaticFiles(directory=TEMPLATES_DIR), name='static')
templates = Jinja2Templates(directory=TEMPLATES_DIR)


@app.get('/')
async def index(request: Request):
    return templates.TemplateResponse(request, 'index.html')


@app.post('/chat')
async def chat_endpoint(request: Request):
    data = await request.json()
    message = data.get("message", '')
    result = chat(message)
    return PlainTextResponse(result)
