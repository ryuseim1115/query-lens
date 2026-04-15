from fastapi import APIRouter
import os

router = APIRouter()


CSV_FILES_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "csv_files")
)


@router.get("/csv-files")
def get_csv_files():
    if not os.path.isdir(CSV_FILES_DIR):
        return {"CSV_FILES_DIR": CSV_FILES_DIR, "csv_files": []}
    csv_files = [
        f
        for f in os.listdir(CSV_FILES_DIR)
        if os.path.isfile(os.path.join(CSV_FILES_DIR, f))
    ]
    return {"CSV_FILES_DIR": CSV_FILES_DIR, "csv_files": csv_files}
