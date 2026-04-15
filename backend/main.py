from fastapi import FastAPI
import os
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from api.routers import run_query, get_csv_files


app = FastAPI()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(os.path.dirname(BASE_DIR), "templates", "static")

# 静的ファイルの設定
app.mount("/static", StaticFiles(directory=static_path), name="static")


app.include_router(run_query.router)
app.include_router(get_csv_files.router)


@app.get("/index")
def home():
    file_path = os.path.join("..", "templates", "index.html")
    print(file_path)
    return FileResponse(file_path)
