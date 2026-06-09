from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from app.api import routes

#Инициализация главного приложения FastAPI
app = FastAPI(
    title="URL Shortener",
    description="Сервис для сокращения ссылок",
    version="1.0.0"
)

# Подключаем роутер
app.include_router(routes.router)

#Настраиваем раздачу статических файлов (HTML, CSS, JS, картинки)
# Мы вычисляем путь к папке static, которая лежит на уровень выше папки app
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(os.path.dirname(current_dir), "static")

app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Отдаем главную HTML-страницу, когда пользователь заходит на корень сайта "/"
@app.get("/")
def serve_frontend():
    index_path = os.path.join(static_dir, "index.html")
    return FileResponse(index_path)