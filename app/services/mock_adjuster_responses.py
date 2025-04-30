# === MOCK DATA START ===
# This file is used only until AI or real adjuster uploads go live.
# To disable, toggle MOCK_MODE = False in /api/adjuster.py
# =======================

def get_mock_adjuster_response(claim_number: str) -> dict:
    if claim_number == "GEICO-123456":
        return {
            "adjuster_name": "Mary Jones",
            "adjuster_email": "mary.jones@geico.com",
            "claim_number": "GEICO-123456",
            "fiduciary_ack": "Yes",
            "liability_acknowledged": "Yes",
            "ime_status": "No",
            "claim_software": "Claim IQ",
            "medical_specials_justification": "Accepted in full, no IME conducted",
            "refuses_ps_breakdown": "Yes",
            "no_ime_acknowledgment": "Acknowledged treating physician findings",
            "med_basis_if_adjusted": "Not applicable",
            "mileage_justification": "Mileage appears consistent with treatment",
            "lost_wages_justification": "Reduced slightly due to employer report",
            "profile_name": "Mary Jones",
            "adjuster_table": {
                "medical_specials_total": "25,000",
                "providers": [
                    {"name": "Spine Center", "adjuster": "12,000"},
                    {"name": "Physical Therapy", "adjuster": "8,000"},
                    {"name": "Chiropractor", "adjuster": "5,000"}
                ],
                "pain_and_suffering": "15,000",
                "future_medicals": "5,000",
                "lost_wages": "4,000",
                "mileage": "250",
                "subtotal": "49,250",
                "deductions": "25,000",
                "total": "24,250"
            }
        }

    # Default fallback
    return {
        "adjuster_name": "Test Adjuster",
        "adjuster_email": "adjuster@example.com",
        "claim_number": claim_number,
        "adjuster_table": {
            "medical_specials_total": "0",
            "providers": [],
            "pain_and_suffering": "0",
            "future_medicals": "0",
            "lost_wages": "0",
            "mileage": "0",
            "subtotal": "0",
            "deductions": "0",
            "total": "0"
        }
    }

# === MOCK DATA END ===
