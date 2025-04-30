# app/services/file_naming_service.py

import os
from datetime import datetime

def get_casefile_folder(claim_id: int) -> str:
    return os.path.join("casefiles", str(claim_id))

def get_report_filename(claim_number: str, extension: str = "md") -> str:
    return f"{claim_number}_rrt_report.{extension}"

def get_final_demand_filename(claim_number: str) -> str:
    return f"{claim_number}_final_demand.pdf"

def get_prophet_summary_filename(claim_number: str) -> str:
    return f"{claim_number}_prophet_summary.pdf"

def get_casefile_zip_filename(claim_id: int) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    return f"casefile_{claim_id}_{today}.zip"

def get_full_path(claim_id: int, filename: str) -> str:
    return os.path.join(get_casefile_folder(claim_id), filename)
