# --- Section 5: Reconciliation Review Table (RRT) ---

import streamlit as st

def run():
    st.title("Section 5: Reconciliation Review Table (RRT)")
    st.markdown("---")

    if "gds" not in st.session_state or "adjuster_responses" not in st.session_state:
        st.error("❌ Missing GDS or Adjuster Response data. Please complete earlier sections.")
        return

    gds = st.session_state["gds"]
    adjuster_responses = st.session_state["adjuster_responses"]

    # Initialize ZAP flags
    if "zap_flags" not in st.session_state:
        st.session_state["zap_flags"] = 0
    if "zap_notes" not in st.session_state:
        st.session_state["zap_notes"] = []

    st.subheader("📊 Reconciliation Review Table (Attorney vs Adjuster Values)")

    rrt_rows = []

    damages = [
        ("Medical Specials", "medical_specials_total"),
        ("Pain & Suffering", "pain_and_suffering"),
        ("Future Medicals", "future_medicals"),
        ("Lost Wages", "lost_wages"),
        ("Mileage", "mileage")
    ]

    for label, key in damages:
        atty_val = next((item["Amount"] for item in gds.get("Damages", []) if item["Category"] == label), 0)
        adjuster_val = adjuster_responses.get(key, "0")
        adjuster_val = float(str(adjuster_val).replace(",", "").replace("$", "").strip() or 0)

        display_adjuster_val = f"${adjuster_val:,.0f}" if adjuster_val else "—"
        display_atty_val = f"${atty_val:,.0f}" if atty_val else "—"

        # --- ZAP flagging ---
        zap_note = None

        if label == "Pain & Suffering":
            if adjuster_responses.get("refuses_ps_breakdown") == "Yes":
                zap_note = "Adj_
