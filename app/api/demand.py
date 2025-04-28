# app/api/demand.py

from fastapi import APIRouter
from app.services.demand_service import generate_final_demand_letter

router = APIRouter(
    prefix="/demand",
    tags=["Final Demand"]
)

@router.post("/final")
def generate_final_demand(claim_id: int, jurisdiction: str = "Default State"):
    final_demand = generate_final_demand_letter(claim_id, jurisdiction)
    return {
        "message": "Final Demand Letter Generated",
        "final_demand": final_demand
    }
