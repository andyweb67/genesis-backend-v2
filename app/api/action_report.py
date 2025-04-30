# app/api/action_report.py

from fastapi import APIRouter
from fastapi.responses import FileResponse
import os
from app.services.action_report_service import generate_action_report
from app.services.casefile_service import zip_casefile, package_casefile

router = APIRouter()

@router.get("/report/markdown/{claim_id}")
def download_markdown_report(claim_id: int):
    result = generate_action_report(claim_id)

    if "error" in result:
        return {"status": "error", "message": result["error"]}

    file_path = result.get("markdown_report_path")
    if not file_path or not os.path.exists(file_path):
        return {"status": "error", "message": "Report file not found"}

    return FileResponse(
        path=file_path,
        filename=os.path.basename(file_path),
        media_type="text/markdown"
    )

@router.get("/report/folder-zip/{claim_id}")
def download_casefile_folder_zip(claim_id: int):
    try:
        zip_path = zip_casefile(claim_id)
        return FileResponse(
            path=zip_path,
            filename=os.path.basename(zip_path),
            media_type="application/zip"
        )
    except FileNotFoundError as e:
        return {"status": "error", "message": str(e)}

@router.get("/report/zip/{claim_id}")
def download_casefile_report_zip(claim_id: int):
    result = generate_action_report(claim_id)

    if "error" in result:
        return {"status": "error", "message": result["error"]}

    file_paths = [
        result.get("markdown_report_path"),
        result.get("pdf_report_path"),
        result.get("final_demand_path"),
        result.get("prophet_summary_path")
    ]
    claim_number = result["claim_info"].get("claim_number")

    if not all(file_paths) or not all(os.path.exists(p) for p in file_paths):
        return {"status": "error", "message": "One or more report files are missing."}

    zip_path = package_casefile(claim_number, file_paths)
    return FileResponse(
        path=zip_path,
        filename=os.path.basename(zip_path),
        media_type="application/zip"
    )
