import os
from app.services.prophet_service import generate_prophet_summary  # Adjust path if needed
from app.services.file_naming_service import (
    get_casefile_folder,
    get_report_filename,
    get_full_path
)

def generate_rrt_markdown_report(claim_number: str, zap_rebuttals, audit_table, ps_comparison, claim_data):
    claim_id = claim_data.get("claim_id", "unknown")
    folder_path = get_casefile_folder(claim_id)
    os.makedirs(folder_path, exist_ok=True)
    filename = get_full_path(claim_id, get_report_filename(claim_number))

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# 🔍 Genesis Audit Summary: Claim {claim_number}\n\n")
        f.write(f"## 📌 Adjuster: {ps_comparison.get('adjuster_name', 'N/A')} ({ps_comparison.get('adjuster_email', 'N/A')})\n")
        f.write("---\n\n")

        f.write("## ⚡ ZAP Rebuttals\n\n")
        for key, val in zap_rebuttals.items():
            label = key.replace("_", " ").title()
            f.write(f"- **{label}**: {val}\n")
        f.write("\n---\n\n")

        f.write("## 📊 Reconciliation Review Table\n\n")
        f.write("| Category | Attorney | Adjuster | IME Status |\n")
        f.write("|----------|----------|----------|------------|\n")
        for row in audit_table:
            f.write(f"| {row['category']} | {row['attorney']} | {row['adjuster']} | {row.get('ime_status', '')} |\n")
        f.write("\n---\n\n")

        f.write("## ⚖️ Pain & Suffering Comparison\n\n")
        f.write("| Source     | Pain & Suffering ($) | Multiplier |\n")
        f.write("|------------|----------------------|------------|\n")
        f.write(f"| Attorney   | ${ps_comparison['attorney_ps_value']} | {ps_comparison['attorney_multiplier']} |\n")
        f.write(f"| Adjuster   | ${ps_comparison['adjuster_ps_value']} | {ps_comparison['adjuster_multiplier']} |\n")
        f.write("\n")

        f.write("### 📚 Jurisdictional Benchmarks (Kentucky):\n")
        jd = ps_comparison["jurisdictional_data"]
        for year, multiplier in jd.items():
            f.write(f"- {year}: {multiplier}x\n")

        f.write("\n### 🔍 Observation:\n")
        f.write(ps_comparison["observation"] + "\n")

        f.write("\n---\n\n")
        f.write("## 🧠 Prophet Litigation Summary\n\n")
        prophet = generate_prophet_summary(claim_data)

        f.write(f"**Trigger Condition:** {prophet['trigger'].replace('_', ' ').title()}\n")
        f.write(f"**Claim Type:** {prophet['claim_type'].title()}\n")
        f.write(f"**Risk Level:** {prophet['risk_level']}\n")
        f.write(f"**Bad Faith Exposure:** {prophet['bad_faith_exposure']}\n")
        f.write(f"**WPI Detected:** {prophet['wpi_detected']}\n")
        f.write(f"**Jurisdictional Multiplier (P&S):** {prophet['jurisdiction_multiplier']}\n")
        f.write(f"**Adjuster Refused P&S Breakdown:** {'Yes' if prophet['adjuster_refused_ps'] else 'No'}\n")
        f.write(f"**Revised Offer:** ${prophet['revised_offer']:,}\n\n")

        f.write("### Defense-Side AI Recommendation\n")
        f.write(f"> _{prophet['defense_ai_recommendation']} — based on projected jury risk and internal valuation conflicts._\n\n")

        f.write("### Legal Escalation Rationale\n")
        f.write(prophet['escalation_basis'] + "\n")

        if prophet.get("suppression_alerts"):
            f.write("\n### ⚠️ Suppression Alerts Detected\n")
            for alert in prophet["suppression_alerts"]:
                f.write(f"- {alert}\n")