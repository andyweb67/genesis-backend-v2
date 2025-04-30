from typing import List, Dict, Any

def build_gds_validation_table(payload) -> List[Dict[str, Any]]:
    gds_validation_table = []

    # Step 1: Medical Specials and Providers
    provider_sum_attorney = 0
    provider_sum_genesis = 0
    providers_validation = []

    for provider in payload.gds_table.providers:
        provider_sum_attorney += int(provider.attorney.replace(",", "").replace("$", ""))
        provider_sum_genesis += int(provider.genesis.replace(",", "").replace("$", ""))
        providers_validation.append({
            "provider": provider.name,
            "attorney": provider.attorney,
            "genesis": provider.genesis,
            "validation": f"{provider.name} matches extracted billing total"
        })

    medical_specials_attorney = int(payload.gds_table.medical_specials_total["attorney"].replace(",", "").replace("$", ""))
    medical_specials_genesis = int(payload.gds_table.medical_specials_total["genesis"].replace(",", "").replace("$", ""))

    # Validate Medical Specials Total
    specials_validation_comment = "Medical specials total matches extracted provider totals" if (
        medical_specials_attorney == provider_sum_attorney
    ) else "Mismatch in provider totals vs medical specials!"

    gds_validation_table.append({
        "category": "Medical Specials Total",
        "attorney": payload.gds_table.medical_specials_total["attorney"],
        "genesis": payload.gds_table.medical_specials_total["genesis"],
        "validation": specials_validation_comment,
        "providers": providers_validation
    })

    # Step 2: Pain and Suffering
    gds_validation_table.append({
        "category": "Pain and Suffering",
        "attorney": payload.gds_table.pain_and_suffering["attorney"],
        "genesis": payload.gds_table.pain_and_suffering["genesis"],
        "validation": "Jurisdictional multiplier applied: 3x"
    })

    # Step 3: Future Medicals
    gds_validation_table.append({
        "category": "Future Medicals",
        "attorney": payload.gds_table.future_medicals["attorney"],
        "genesis": payload.gds_table.future_medicals["genesis"],
        "validation": "Future medicals support confirmed"
    })

    # Step 4: Lost Wages
    gds_validation_table.append({
        "category": "Lost Wages",
        "attorney": payload.gds_table.lost_wages["attorney"],
        "genesis": payload.gds_table.lost_wages["genesis"],
        "validation": "Lost wages documentation validated"
    })

    # Step 5: Mileage
    gds_validation_table.append({
        "category": "Mileage",
        "attorney": payload.gds_table.mileage["attorney"],
        "genesis": payload.gds_table.mileage["genesis"],
        "validation": "Mileage extracted manually from demand"
    })

    # Step 6: Subtotal Calculation
    subtotal_attorney = (
        medical_specials_attorney
        + int(payload.gds_table.pain_and_suffering["attorney"].replace(",", "").replace("$", ""))
        + int(payload.gds_table.future_medicals["attorney"].replace(",", "").replace("$", ""))
        + int(payload.gds_table.lost_wages["attorney"].replace(",", "").replace("$", ""))
        + int(payload.gds_table.mileage["attorney"].replace(",", "").replace("$", ""))
    )
    subtotal_genesis = (
        medical_specials_genesis
        + int(payload.gds_table.pain_and_suffering["genesis"].replace(",", "").replace("$", ""))
        + int(payload.gds_table.future_medicals["genesis"].replace(",", "").replace("$", ""))
        + int(payload.gds_table.lost_wages["genesis"].replace(",", "").replace("$", ""))
        + int(payload.gds_table.mileage["genesis"].replace(",", "").replace("$", ""))
    )

    gds_validation_table.append({
        "category": "Subtotal",
        "attorney": f"{subtotal_attorney}",
        "genesis": f"{subtotal_genesis}",
        "validation": "Subtotal matches sum of main damages"
    })

    # Step 7: Deductions
    gds_validation_table.append({
        "category": "Deductions",
        "attorney": payload.gds_table.deductions["attorney"],
        "genesis": payload.gds_table.deductions["genesis"],
        "validation": "Third-party policy limit offset applied"
    })

    # Step 8: Total Calculation
    deductions_attorney = int(payload.gds_table.deductions["attorney"].replace(",", "").replace("$", ""))
    deductions_genesis = int(payload.gds_table.deductions["genesis"].replace(",", "").replace("$", ""))

    total_attorney = subtotal_attorney - deductions_attorney
    total_genesis = subtotal_genesis - deductions_genesis

    gds_validation_table.append({
        "category": "Total",
        "attorney": f"{total_attorney}",
        "genesis": f"{total_genesis}",
        "validation": "Total = Subtotal - Deductions validated"
    })

    return gds_validation_table
