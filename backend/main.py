from fastapi import FastAPI
import os
from fastapi.staticfiles import StaticFiles
from api.routers import run_query, get_csv_files, determine_csv_file, input, result
from config import TEMPLATES_DIR


app = FastAPI()
static_path = os.path.join(TEMPLATES_DIR, "js")
css_path = os.path.join(TEMPLATES_DIR, "css")

app.mount("/static", StaticFiles(directory=static_path), name="static")
app.mount("/css", StaticFiles(directory=css_path), name="css")

app.include_router(run_query.router)
app.include_router(get_csv_files.router)
app.include_router(determine_csv_file.router)
app.include_router(input.router)
app.include_router(result.router)
