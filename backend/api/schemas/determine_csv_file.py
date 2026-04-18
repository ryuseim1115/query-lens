from pydantic import BaseModel


class CsvInfo(BaseModel):
    CSV_FILES_DIR: str
    csv_files: list[str]
