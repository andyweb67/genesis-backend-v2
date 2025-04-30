from typing import Dict, Any

def build_ps_comparison(gds_data: Dict[str, Any], adjuster_data: Dict[str, Any]) -> Dict[str, Any]:
    gds = gds_data["Genesis Demand Summary Table"]
    adjuster = adjuster_data["adjuster_table"]

    # Pull values
    try:
        ps_attorney = float(gds["pain_and_suffering"]["attorney"].replace(",", ""))
        ps_adjuster = float(adjuster["pain_and_suffering"].replace(",", ""))
        med_specials_attorney = float(gds["medical_specials_total"]["attorney"].replace(",", ""))
        med_specials_adjuster = float(adjuster["medical_specials_total"].replace(",", ""))
    except (KeyError, ValueError):
        return {
            "error": "Invalid or missing data in P&S or Medical Specials. Cannot compute comparison."
        }

    # Calculate multipliers
    attorney_multiplier = round(ps_attorney / med_specials_attorney, 3) if med_specials_attorney else 0
    adjuster_multiplier = round(ps_adjuster / med_specials_adjuster, 3) if med_specials_adjuster else 0

    # Historical jurisdictional data (from Attorney Beaton - Kentucky example)
    jurisdictional_data = {
        "2016": 3.478,
        "2017": 4.482,
        "2018": 2.867,
        "21_year_avg": 1.874
    }

    # Generate observation
    if adjuster_multiplier < jurisdictional_data["21_year_avg"]:
        observation = (
            f"Insurer’s offer ({adjuster_multiplier}x) falls below the 21-year Kentucky average "
            f"({jurisdictional_data['21_year_avg']}x), with recent years exceeding 3x. "
            "This may signal suppression below historical norms."
        )
    else:
        observation = "Adjuster multiplier is within historical jurisdictional range."

    # Final output
    return {
    "category": "Pain & Suffering Comparison",
    "attorney_ps_value": f"{int(ps_attorney):,}",
    "adjuster_ps_value": f"{int(ps_adjuster):,}",
    "attorney_multiplier": f"{attorney_multiplier}x",
    "adjuster_multiplier": f"{adjuster_multiplier}x",
    "jurisdictional_data": jurisdictional_data,
    "observation": observation
}
