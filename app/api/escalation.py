# app/api/escalation.py

from fastapi import APIRouter
from app.services.escalation_service import evaluate_escalation

router = APIRouter(
    prefix="/escalation",
    tags=["Escalation"]
)

@router.post("/decision")
def escalation_decision(claim_id: int, adjuster_behavior: str = "neutral"):
    result = evaluate_escalation(claim_id, adjuster_behavior)
    return {
        "message": "Escalation Decision Made",
        "decision": result
    }
