from fastapi import APIRouter
from fastapi.responses import FileResponse
import os
from config import TEMPLATES_DIR

router = APIRouter()


@router.get("/input")
def input():
    return FileResponse(os.path.join(TEMPLATES_DIR, "html", "input.html"))
