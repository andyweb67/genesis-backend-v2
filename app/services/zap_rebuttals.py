from typing import Dict, Any

def build_zap_rebuttals(adjuster_data: Dict[str, Any]) -> Dict[str, str]:
    zap = {}

    # Pain & Suffering withheld
    if adjuster_data.get("refuses_ps_breakdown", "").lower() == "yes":
        zap["pain_and_suffering"] = (
            "Adjuster refused to disclose the pain & suffering valuation breakdown. "
            "This blocks meaningful negotiation and may constitute a failure of good faith."
        )

    # No IME conducted
    if adjuster_data.get("ime_status", "").lower() == "no":
        zap["future_medicals"] = (
            "No IME was conducted. Denial or reduction of future medicals without a counter-medical opinion lacks medical authority."
        )
        zap["medical_specials_total"] = (
            "Medical specials were accepted without IME. Adjuster may not later dispute these values."
        )

    # Lost wages reduced
    if "reduced" in adjuster_data.get("lost_wages_justification", "").lower():
        zap["lost_wages"] = (
            "Lost wages were reduced despite documentation. Employer opinion does not override physician work capacity statements."
        )

    # Mileage reduced
    if int(adjuster_data.get("adjuster_table", {}).get("mileage", "0").replace(",", "")) < 300:
        zap["mileage"] = (
            "Mileage was reduced. Claimant's treatment location and frequency were disclosed and verifiable."
        )

    # Medical adjusted without justification
    if adjuster_data.get("med_basis_if_adjusted", "").lower() not in ["", "not applicable", "n/a"]:
        zap["medical_specials_total"] = (
            "Adjuster indicated medical specials were adjusted, but no valid basis (e.g. IME) was provided. "
            "This will be challenged."
        )

    # Failsafe default if no responses
    if not zap:
        zap["notice"] = (
            "Genesis reviewed the adjuster’s answers. No rebuttal triggers detected at this stage."
        )

    return zap
