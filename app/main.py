from fastapi import FastAPI
import os
from app.api import claims, audit, demand, escalation, prophet, action_report, casefile, healthcheck, dashboard

app = FastAPI(
    title="Genesis API",
    description="Backend for Genesis claim audit platform",
    version="1.0.0"
)

# --- Startup Folder Check ---
@app.on_event("startup")
async def genesis_startup_event():
    """
    Ensures critical system folders are created when Genesis backend boots.
    """
    required_folders = ["casefiles", "logs"]

    for folder in required_folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

# --- Include Routers ---
app.include_router(claims.router)
app.include_router(audit.router)
app.include_router(demand.router)
app.include_router(escalation.router)
app.include_router(prophet.router)
app.include_router(action_report.router)
app.include_router(casefile.router)
app.include_router(healthcheck.router)
app.include_router(dashboard.router)

# --- Basic root endpoint ---
@app.get("/")
def read_root():
    return {"message": "Welcome to Genesis API!"}
