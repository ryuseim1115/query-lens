import os

from api.routers import determine_csv_file, get_csv_files, input, result, run_query
from config import TEMPLATES_DIR
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

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
