# app/api/prophet.py

from fastapi import APIRouter
from app.services.prophet_service import simulate_prophet_litigation

router = APIRouter(
    prefix="/prophet",
    tags=["Prophet Simulation"]
)

@router.post("/simulate")
def prophet_simulation(claim_id: int, adjuster_behavior: str = "neutral"):
    simulation = simulate_prophet_litigation(claim_id, adjuster_behavior)
    return {
        "message": "Prophet Litigation Simulation Complete",
        "prophet_simulation": simulation
    }
