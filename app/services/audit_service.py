# app/services/audit_service.py

from app.services.claim_service import claims_db

def perform_audit(claim_id: int) -> dict:
    if claim_id < 1 or claim_id > len(claims_db):
        return {"error": "Claim not found"}

    claim = claims_db[claim_id - 1]

    # Start audit score
    audit_score = 100
    audit_findings = []  # <-- NEW: Track issues found

    # Check description
    if not claim.description or claim.description.strip() == "":
        audit_score -= 20
        audit_findings.append("Missing description or documentation.")

    # Check claim amount
    if claim.amount_claimed < 2500:
        audit_score -= 30
        audit_findings.append("Claimed amount unusually low (< $2,500).")

    if claim.amount_claimed > 25000:
        audit_score += 10
        audit_findings.append("High claim amount (> $25,000) recognized.")

    # Check liability
    if claim.liability_percent and claim.liability_percent > 0:
        penalty = claim.liability_percent // 2
        audit_score -= penalty
        audit_findings.append(f"Liability dispute detected ({claim.liability_percent}% liability assigned).")

    # Check attached documentation
    if not claim.medical_proof_attached:
        audit_score -= 15
        audit_findings.append("Missing medical proof of injury.")
        
    if not claim.wage_proof_attached:
        audit_score -= 10
        audit_findings.append("Missing wage loss proof.")

    # Risk flag based on final audit score
    if audit_score >= 80:
        risk_flag = "Low Risk"
    elif 50 <= audit_score < 80:
        risk_flag = "Moderate Risk"
    else:
        risk_flag = "High Risk"

    # Suppression Alert
    suppression_alert = False
    if risk_flag == "High Risk":
        suppression_alert = True

    return {
        "claimant_name": claim.claimant_name,
        "date_of_loss": claim.date_of_loss,
        "amount_claimed": claim.amount_claimed,
        "liability_percent": claim.liability_percent,
        "medical_proof_attached": claim.medical_proof_attached,
        "wage_proof_attached": claim.wage_proof_attached,
        "audit_score": audit_score,
        "risk_flag": risk_flag,
        "suppression_alert": suppression_alert,
        "audit_findings": audit_findings  # <-- NEW!
    }
# app/services/audit_service.py

def get_suppression_alerts() -> list:
    suppression_list = []

    for idx, claim in enumerate(claims_db, start=1):
        audit_result = perform_audit(idx)

        if audit_result.get("suppression_alert"):
            suppression_list.append({
                "claim_id": idx,
                "claimant_name": audit_result["claimant_name"],
                "audit_score": audit_result["audit_score"],
                "risk_flag": audit_result["risk_flag"],
                "audit_findings": audit_result["audit_findings"]
            })

    return suppression_list
