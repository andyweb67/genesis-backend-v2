# app/services/escalation_service.py

from app.services.claim_service import claims_db
from app.services.audit_service import perform_audit

def evaluate_escalation(claim_id: int, adjuster_behavior: str = "neutral") -> dict:
    """
    Evaluates whether to accept settlement or escalate based on audit score and adjuster behavior.
    """

    if claim_id < 1 or claim_id > len(claims_db):
        return {"error": "Claim not found"}

    audit_result = perform_audit(claim_id)

    audit_score = audit_result.get("audit_score", 0)
    suppression_alert = audit_result.get("suppression_alert", False)

    recommendation = ""
    reasoning = []

    # Default starting point
    if suppression_alert:
        reasoning.append("Suppression alert triggered based on audit results.")
    if audit_score < 50:
        reasoning.append("Audit score indicates significant undervaluation risk.")

    # Adjuster behavior influence
    if adjuster_behavior.lower() in ["defensive", "evasive", "resistant"]:
        reasoning.append(f"Adjuster's behavior ({adjuster_behavior}) suggests unwillingness to negotiate in good faith.")

    # Decision logic
    if suppression_alert or audit_score < 60 or adjuster_behavior.lower() in ["defensive", "evasive", "resistant"]:
        recommendation = "Escalate to Litigation Preparation (Prophet Mode)"
    else:
        recommendation = "Consider Accepting Revised Offer"

    return {
        "claim_id": claim_id,
        "audit_score": audit_score,
        "suppression_alert": suppression_alert,
        "adjuster_behavior": adjuster_behavior,
        "recommendation": recommendation,
        "reasoning": reasoning
    }
