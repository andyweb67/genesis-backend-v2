# app/api/audit.py

from fastapi import APIRouter
from app.services.audit_service import perform_audit, get_suppression_alerts

router = APIRouter(
    prefix="/audit",
    tags=["Audit"]
)

# Existing endpoint
@router.post("/")
def audit_claim(claim_id: int):
    audit_result = perform_audit(claim_id)
    return {
        "message": "Audit completed",
        "result": audit_result
    }

# NEW endpoint: Suppression Report
@router.get("/suppression-alerts")
def suppression_alerts():
    suppression_claims = get_suppression_alerts()
    return {
        "message": "Suppression Alerts Report",
        "suppression_claims": suppression_claims
    }
# app/api/audit.py

from fastapi import APIRouter
from app.services.audit_service import perform_audit, get_suppression_alerts
from app.services.zap_service import generate_full_zap_response  # <-- NEW

router = APIRouter(
    prefix="/audit",
    tags=["Audit"]
)

@router.post("/")
def audit_claim(claim_id: int):
    audit_result = perform_audit(claim_id)

    return {
        "message": "Audit completed",
        "result": audit_result
    }

@router.get("/suppression-alerts")
def suppression_alerts():
    suppression_claims = get_suppression_alerts()
    return {
        "message": "Suppression Alerts Report",
        "suppression_claims": suppression_claims
    }

# NEW: Generate full ZAP rebuttal
@router.post("/zap")
def generate_zap_from_audit(claim_id: int, jurisdiction: str = "Default State"):
    audit_result = perform_audit(claim_id)

    if not audit_result.get("suppression_alert"):
        return {"message": "Suppression not detected. No ZAP response generated."}

    zap_output = generate_full_zap_response(audit_result.get("audit_findings", []), jurisdiction)

    return {
        "message": "ZAP Rebuttal Prepared",
        "claim_id": claim_id,
        "jurisdiction": jurisdiction,
        "zap_rebuttals": zap_output
    }
