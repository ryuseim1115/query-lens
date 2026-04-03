from fastapi import FastAPI
import os
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from api.routers import connection, run_query

app = FastAPI()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(os.path.dirname(BASE_DIR), "templates", "static")
views_path = os.path.join(os.path.dirname(BASE_DIR), "templates", "views")

# 静的ファイルの設定
app.mount("/static", StaticFiles(directory=static_path), name="static")
app.mount("/views", StaticFiles(directory=views_path), name="views")

app.include_router(connection.router)
app.include_router(run_query.router)


@app.get("/index")
def home():
    file_path = os.path.join("..", "templates", "index.html")
    return FileResponse(file_path)
