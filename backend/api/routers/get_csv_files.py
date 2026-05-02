import os

from config import CSV_FILES_DIR
from fastapi import APIRouter

router = APIRouter()


@router.get("/get-csv-files")
def get_csv_files():
    if not os.path.isdir(CSV_FILES_DIR):
        return {"CSV_FILES_DIR": CSV_FILES_DIR, "csv_files": []}
    csv_files = [
        f
        for f in os.listdir(CSV_FILES_DIR)
        if os.path.isfile(os.path.join(CSV_FILES_DIR, f))
    ]
    return {"CSV_FILES_DIR": CSV_FILES_DIR, "csv_files": csv_files}
