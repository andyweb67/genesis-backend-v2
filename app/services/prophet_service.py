# app/services/prophet_service.py

def simulate_prophet_litigation(claim_id: int, adjuster_behavior: str = "neutral") -> dict:
    # Mock suppression logic
    suppression_alert = False
    adjuster_refused_ps = adjuster_behavior.lower() == "suppressive"
    suppression_alert = adjuster_refused_ps

    # Mock revised offer logic
    revised_offer = 50000 if suppression_alert else 32000

    # Mock jury risk score
    jury_risk = 85 if suppression_alert else 60

    # Suppression alert triggers
    claim_data = {
        "claim_id": claim_id,
        "insurer": "GEICO",
        "claim_software": "Claim IQ"
    }
    insurer = claim_data.get("insurer", "").lower()
    software = claim_data.get("claim_software", "").lower()

    subpoena_alog = False
    subpoena_ciq = False
    flags = []

    if "geico" in insurer and "claim iq" in software:
        subpoena_alog = True
        subpoena_ciq = True
        flags.append("Insurer uses Claim IQ — known suppression behavior")
        flags.append("Subpoena ALOG and CIQ valuation logic recommended")

    return {
        "claim_id": claim_id,
        "adjuster_behavior": adjuster_behavior,
        "estimated_jury_risk_score": jury_risk,
        "audit_score": 87,
        "suppression_alert": suppression_alert,
        "adjuster_refused_ps": adjuster_refused_ps,
        "recommendation": "Escalate to trial prep phase",
        "revised_offer": revised_offer,
        "trigger": "pain_suffering_withheld" if adjuster_refused_ps else "lowball_offer",
        "claim_type": "first_party",
        "risk_level": "High" if jury_risk > 75 else "Moderate",
        "bad_faith_exposure": "Yes" if suppression_alert else "Potential",
        "jurisdiction_multiplier": 3.2,
        "defense_ai_recommendation": "Advise early settlement to avoid discovery risk",
        "insurer": insurer.title(),
        "claim_software": software.title(),
        "subpoena_alog": subpoena_alog,
        "subpoena_ciq": subpoena_ciq,
        "suppression_alerts": flags
    }
