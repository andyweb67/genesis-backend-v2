# --- Section 6: Final Demand & Adjuster Reaction ---

import streamlit as st
from datetime import datetime

def run():
    st.title("Section 6: Final Demand & Adjuster Reaction")
    st.markdown("---")

    if "gds" not in st.session_state or "adjuster_responses" not in st.session_state:
        st.error("❌ Missing claim data. Please complete previous sections first.")
        return

    adjuster_responses = st.session_state["adjuster_responses"]
    zap_flags = st.session_state.get("zap_flags", 0)
    zap_notes = st.session_state.get("zap_notes", [])

    st.subheader("📨 Final Audit Outcome")

    refuses_ps = adjuster_responses.get("refuses_ps_breakdown", "No") == "Yes"
    original_offer = 0.0
    revised_offer = 0.0

    try:
        ms = float(str(adjuster_responses.get("medical_specials_total", "0")).replace(",", "").replace("$", ""))
        ps = float(str(adjuster_responses.get("pain_and_suffering", "0")).replace(",", "").replace("$", ""))
        lw = float(str(adjuster_responses.get("lost_wages", "0")).replace(",", "").replace("$", ""))
        original_offer = ms + ps + lw
    except:
        original_offer = 0

    # --- Decision Logic ---
    if refuses_ps:
        decision = "PNS_WITHHELD"
    elif zap_flags >= 3:
        decision = "TRIGGER_PROPHET"
    elif zap_flags >= 1:
        decision = "REVISE_OFFER"
    else:
        decision = "ACCEPTABLE"

    # Save system decision in session state
    st.session_state["system_decision"] = decision

    st.markdown("### 🧠 Genesis Decision")
    if decision == "REVISE_OFFER":
        st.success("📈 Adjuster has modestly increased the settlement offer.")
        revised_offer = original_offer * 1.2  # Assume 20% increase
        st.markdown(f"- **Original Offer:** ${original_offer:,.2f}")
        st.markdown(f"- **Revised Offer:** ${revised_offer:,.2f}")

    elif decision == "MARKED_INCREASE":
        st.success("🚀 Adjuster significantly increased the settlement offer.")
        revised_offer = original_offer * 1.5
        st.markdown(f"- **Original Offer:** ${original_offer:,.2f}")
        st.markdown(f"- **Revised Offer:** ${revised_offer:,.2f}")

    elif decision == "TRIGGER_PROPHET":
        st.error("⚠️ Adjuster behavior suggests suppression. Litigation risk simulation will be triggered.")

    elif decision == "PNS_WITHHELD":
        st.warning("🔐 Pain & Suff
