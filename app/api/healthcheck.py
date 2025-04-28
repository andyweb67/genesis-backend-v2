# app/api/healthcheck.py

from fastapi import APIRouter
import os

router = APIRouter(
    tags=["Health Check"]
)

@router.get("/healthcheck")
def genesis_healthcheck(auto_repair: bool = True):
    """
    Returns basic health status of the Genesis backend system.
    Checks and optionally repairs critical folders like casefiles/ and logs/.
    """

    required_folders = ["casefiles", "logs"]
    health_report = {}

    for folder in required_folders:
        exists = os.path.exists(folder)
        health_report[f"{folder}_exists"] = exists

        if not exists and auto_repair:
            os.makedirs(folder)
            health_report[f"{folder}_repaired"] = True
        else:
            health_report[f"{folder}_repaired"] = False

    health_report["status"] = "healthy" if all(health_report[f"{folder}_exists"] or health_report[f"{folder}_repaired"] for folder in required_folders) else "issues detected"

    return health_report

