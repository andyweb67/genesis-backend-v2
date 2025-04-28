# app/api/dashboard.py

from fastapi import APIRouter
import os
from datetime import datetime
from app.version import GENESIS_VERSION  # <-- added this import

router = APIRouter(
    tags=["Dashboard"]
)

@router.get("/dashboard")
def genesis_dashboard():
    """
    Returns a snapshot of Genesis system health, version, and casefile activity.
    """

    # --- Health Check ---
    casefiles_exists = os.path.exists("casefiles")
    logs_exists = os.path.exists("logs")

    system_health = "healthy" if casefiles_exists and logs_exists else "issues detected"

    # --- Total Casefile Count ---
    casefile_count = 0
    if casefiles_exists:
        casefile_count = len([f for f in os.listdir("casefiles") if f.endswith(".zip")])

    # --- Last Casefile Generation Timestamp + Today's Count ---
    last_casefile_generated = "No records found"
    casefiles_generated_today = 0
    today_str = datetime.now().strftime("%Y-%m-%d")

    log_path = os.path.join("logs", "casefile_generation.log")
    if os.path.exists(log_path):
        with open(log_path, "r") as log_file:
            lines = log_file.readlines()
            if lines:
                # Last generated timestamp
                last_line = lines[-1]
                if last_line.startswith("["):
                    timestamp = last_line.split("]")[0].strip("[]")
                    last_casefile_generated = timestamp

            # Count today's entries
            for line in lines:
                if line.startswith(f"[{today_str}"):
                    casefiles_generated_today += 1

    return {
        "genesis_version": GENESIS_VERSION,  # <-- included version here
        "system_health": system_health,
        "casefile_count_total": casefile_count,
        "casefile_count_today": casefiles_generated_today,
        "last_casefile_generated": last_casefile_generated
    }
from app.version import GENESIS_VERSION

@router.get("/genesis-version")
def get_genesis_version():
    """
    Returns only the current Genesis backend version.
    Lightweight endpoint for health checks or monitoring tools.
    """
    return {"genesis_version": GENESIS_VERSION}
