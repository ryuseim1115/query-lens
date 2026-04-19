from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
import os
from api.schemas.determine_csv_file import CsvInfo
from api.db.create_csv_tables import create_csv_tables
from api.validators.csv_file_name_validator import CsvFileNameValidator
from config import CSV_FILES_DIR


router = APIRouter()


@router.post("/determine-csv-file", status_code=204)
def determine_csv_file(body: CsvInfo):
    if body.CSV_FILES_DIR != CSV_FILES_DIR:
        raise HTTPException(status_code=400, detail="不正なファイルパスです")

    if not body.csv_files:
        raise HTTPException(status_code=400, detail=f"{CSV_FILES_DIR} にCSVファイルをアップロードしてください")

    errors = []
    for i, csv_file in enumerate(body.csv_files, start=1):
        try:
            CsvFileNameValidator(csv_file).validate()
        except ValueError as e:
            errors.append(f"{i}行目: {e}")
            continue
        if not os.path.isfile(os.path.join(CSV_FILES_DIR, csv_file)):
            errors.append(f"{i}行目: {csv_file} が見つかりません")
    if errors:
        detail = "\n".join(errors) + "\n※使用できるのは英数字・アンダースコア・ハイフンです"
        raise HTTPException(status_code=400, detail=detail)
    create_csv_tables(body.CSV_FILES_DIR, body.csv_files)
    return Response(status_code=204)
