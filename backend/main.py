from fastapi import FastAPI
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from api.routers import run_query, get_csv_files, determine_csv_file


app = FastAPI()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates_path = os.path.join(os.path.dirname(BASE_DIR), "templates")
static_path = os.path.join(templates_path, "static")

app.mount("/static", StaticFiles(directory=static_path), name="static")

app.include_router(run_query.router)
app.include_router(get_csv_files.router)
app.include_router(determine_csv_file.router)


@app.get("/index")
def home():
    return FileResponse(os.path.join(templates_path, "index.html"))
