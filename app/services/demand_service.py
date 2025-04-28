# app/services/demand_service.py

from app.services.claim_service import claims_db
from app.services.audit_service import perform_audit
from app.services.zap_service import generate_full_zap_response

def generate_final_demand_letter(claim_id: int, jurisdiction: str = "Default State") -> dict:
    if claim_id < 1 or claim_id > len(claims_db):
        return {"error": "Claim not found"}

    claim = claims_db[claim_id - 1]
    audit_result = perform_audit(claim_id)

    if not audit_result.get("suppression_alert"):
        return {"message": "Suppression not detected. Final demand escalation not necessary."}

    zap_rebuttals = generate_full_zap_response(audit_result.get("audit_findings", []), jurisdiction)

    # Assemble the final demand letter
    letter = f"""
To Claims Department,

Re: {claim.claimant_name} — Date of Loss: {claim.date_of_loss}

Following a comprehensive audit of your claim evaluation, several issues have been identified impacting fair claim valuation:

Audit Findings:
"""

    # Add audit findings
    for finding in audit_result.get("audit_findings", []):
        letter += f"- {finding}\n"

    letter += "\nRebuttals to Identified Issues:\n"

    # Add ZAP rebuttals
    for zap in zap_rebuttals:
        letter += f"- {zap['zap_rebuttal']}\n"

    letter += f"""

Given the outlined findings and rebuttals, we formally request a revised settlement offer reflecting a fair and complete evaluation. Failure to adequately address the documented issues may result in further litigation escalation.

Please provide your updated response within 10 business days.

Sincerely,
Genesis Audit Team
PlaintiffMax
"""

    return {
        "claimant_name": claim.claimant_name,
        "jurisdiction": jurisdiction,
        "final_demand_letter": letter.strip()
    }
