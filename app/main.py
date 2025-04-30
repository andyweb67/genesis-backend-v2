from fastapi import FastAPI
import os
from app.api import (
    healthcheck,
    gds,
    adjuster,
    # claims,
    # audit,
    # demand,
    # escalation,
    # prophet,
    # casefile,
    # dashboard,
)

app = FastAPI(
    title="Genesis API",
    description="Backend for Genesis claim audit platform",
    version="1.1.0"
)

@app.on_event("startup")
async def genesis_startup_event():
    required_folders = ["casefiles", "logs"]
    for folder in required_folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

# Load Routers
app.include_router(healthcheck.router)
app.include_router(gds.router, prefix="/gds", tags=["Genesis Demand Summary"])
app.include_router(adjuster.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Genesis API!"}
