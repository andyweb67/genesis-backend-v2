# app/api/upload_handler.py

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import os

router = APIRouter()

@router.post("/report/upload/{claim_id}")
def upload_exhibits(claim_id: int, files: list[UploadFile] = File(...)):
    folder_path = os.path.join("casefiles", str(claim_id), "exhibits")
    os.makedirs(folder_path, exist_ok=True)

    saved_files = []
    for file in files:
        file_path = os.path.join(folder_path, file.filename)
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        saved_files.append(file.filename)

    return JSONResponse(content={
        "status": "success",
        "uploaded_files": saved_files
    })
