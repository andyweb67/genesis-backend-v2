# app/services/action_report_service.py

from app.services.claim_service import claims_db
from app.services.audit_service import perform_audit
from app.services.zap_service import generate_full_zap_response
from app.services.demand_service import generate_final_demand_letter
from app.services.escalation_service import evaluate_escalation
from app.services.prophet_service import simulate_prophet_litigation

def generate_action_report(claim_id: int, jurisdiction: str = "Default State", adjuster_behavior: str = "neutral") -> dict:
    """
    Generates a full Genesis Action Report combining all modules.
    """

    if claim_id < 1 or claim_id > len(claims_db):
        return {"error": "Claim not found"}

    claim = claims_db[claim_id - 1]
    audit = perform_audit(claim_id)
    zap_rebuttals = generate_full_zap_response(audit.get("audit_findings", []), jurisdiction)
    final_demand = generate_final_demand_letter(claim_id, jurisdiction)
    escalation = evaluate_escalation(claim_id, adjuster_behavior)
    prophet = simulate_prophet_litigation(claim_id, adjuster_behavior)

    return {
        "claim_info": {
            "claimant_name": claim.claimant_name,
            "date_of_loss": claim.date_of_loss,
            "amount_claimed": claim.amount_claimed,
            "jurisdiction": jurisdiction
        },
        "audit_summary": audit,
        "zap_rebuttals": zap_rebuttals,
        "final_demand_letter": final_demand.get("final_demand_letter"),
        "escalation_decision": escalation,
        "prophet_simulation": prophet
    }
