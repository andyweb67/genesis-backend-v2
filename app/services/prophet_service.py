# app/services/prophet_service.py

from app.services.claim_service import claims_db
from app.services.audit_service import perform_audit

def simulate_prophet_litigation(claim_id: int, adjuster_behavior: str = "neutral") -> dict:
    """
    Simulates potential litigation exposure based on audit results and adjuster behavior.
    """

    if claim_id < 1 or claim_id > len(claims_db):
        return {"error": "Claim not found"}

    audit_result = perform_audit(claim_id)

    audit_score = audit_result.get("audit_score", 0)
    suppression_alert = audit_result.get("suppression_alert", False)

    risk_multiplier = 1.0

    # Base adjustments
    if suppression_alert:
        risk_multiplier += 0.5
    if audit_score < 50:
        risk_multiplier += 0.3
    if adjuster_behavior.lower() in ["defensive", "evasive", "resistant"]:
        risk_multiplier += 0.2

    # Estimated jury risk score out of 100
    base_jury_risk = 50
    estimated_jury_risk = base_jury_risk * risk_multiplier

    # Litigation recommendation based on risk level
    if estimated_jury_risk >= 80:
        recommendation = "High risk of excess verdict. Recommend aggressive settlement or immediate litigation filing."
    elif 60 <= estimated_jury_risk < 80:
        recommendation = "Moderate risk of adverse verdict. Recommend strong negotiation pressure."
    else:
        recommendation = "Manageable risk. Recommend settlement if reasonable."

    return {
        "claim_id": claim_id,
        "audit_score": audit_score,
        "suppression_alert": suppression_alert,
        "adjuster_behavior": adjuster_behavior,
        "estimated_jury_risk_score": round(estimated_jury_risk, 2),
        "recommendation": recommendation
    }
