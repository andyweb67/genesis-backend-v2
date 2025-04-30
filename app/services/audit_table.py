from typing import Dict, Any, List

def build_genesis_audit_table(gds_data: Dict[str, Any], adjuster_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    gds = gds_data["Genesis Demand Summary Table"]
    adjuster = adjuster_data["adjuster_table"]
    ime_ordered = adjuster_data.get("ime_status", "").lower() == "yes"

    def get_ime_status(category: str) -> str:
        if category in ["Medical Specials Total", "Future Medicals"]:
            return "IME Ordered" if ime_ordered else "Shielded"
        return None

    audit_table = []

    # Parent category: Medical Specials Total
    audit_table.append({
        "category": "Medical Specials Total",
        "attorney": gds["medical_specials_total"]["attorney"],
        "adjuster": adjuster["medical_specials_total"],
        "ime_status": get_ime_status("Medical Specials Total")
    })

    # Subrows: Providers
    for provider in gds["providers"]:
        match = next((p for p in adjuster["providers"] if p["name"] == provider["name"]), None)
        audit_table.append({
            "category": f"├─ {provider['name']}",
            "attorney": provider["attorney"],
            "adjuster": match["adjuster"] if match else "—"
            # No ime_status for subrows
        })

    # Pain and Suffering
    audit_table.append({
        "category": "Pain and Suffering",
        "attorney": gds["pain_and_suffering"]["attorney"],
        "adjuster": adjuster["pain_and_suffering"]
        # No ime_status — subjective
    })

    # Future Medicals
    audit_table.append({
        "category": "Future Medicals",
        "attorney": gds["future_medicals"]["attorney"],
        "adjuster": adjuster["future_medicals"],
        "ime_status": get_ime_status("Future Medicals")
    })

    # Lost Wages
    audit_table.append({
        "category": "Lost Wages",
        "attorney": gds["lost_wages"]["attorney"],
        "adjuster": adjuster["lost_wages"]
    })

    # Mileage
    audit_table.append({
        "category": "Mileage",
        "attorney": gds["mileage"]["attorney"],
        "adjuster": adjuster["mileage"]
    })

    # Subtotal
    audit_table.append({
        "category": "Subtotal",
        "attorney": gds["subtotal"]["attorney"],
        "adjuster": adjuster["subtotal"]
    })

    # Deductions
    audit_table.append({
        "category": "Deductions",
        "attorney": gds["deductions"]["attorney"],
        "adjuster": adjuster["deductions"]
    })

    # Total
    audit_table.append({
        "category": "Total",
        "attorney": gds["total"]["attorney"],
        "adjuster": adjuster["total"]
    })

    return audit_table
