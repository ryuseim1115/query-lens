from fastapi import APIRouter
from api.schemas.determine_csv_file import CsvInfo
from api.db.create_csv_tables import create_csv_tables


router = APIRouter()


@router.post("/determine-csv-file")
def determine_csv_file(body: CsvInfo):
    create_csv_tables(body.CSV_FILES_DIR, body.csv_files)
