from fastapi import APIRouter
from api.schemas.determine_csv_file import CsvInfo
from api.services.create_csv_tables import create_csv_tables


router = APIRouter()


@router.post("/determine-csv-file")
def determine_csv_file(body: CsvInfo):
    create_csv_tables(body)
