# --- Section 7: Prophet Litigation Risk Simulation ---

import streamlit as st
import time

def run():
    st.title("Section 7: Prophet Litigation Risk Simulation")
    st.markdown("---")

    if "system_decision" not in st.session_state:
        st.error("❌ Missing audit outcome. Please complete prior sections first.")
        return

    decision = st.session_state["system_decision"]
    zap_flags = st.session_state.get("zap_flags", 0)
    zap_notes = st.session_state.get("zap_notes", [])

    st.subheader("🔍 Genesis Litigation Risk Simulation")

    if decision == "PNS_WITHHELD":
        st.error("🚨 Litigation Trigger: Pain & Suffering valuation withheld.")
        with st.spinner("📄 Building escalation case..."):
            time.sleep(1)
        st.markdown("""
        ### ⚖️ Internal Suppression Detected
        - Adjuster refused to disclose Pain & Suffering valuation
        - Multiplier comparison blocked
        - Genesis flags systemic suppression risk
        """)
        st.warning("""
        **Recommended Action:**  
        Immediate escalation to litigation. Internal claim handling documents (ALOG, CIQ rules) should be subpoenaed during discovery.
        """)

    elif decision == "TRIGGER_PROPHET":
        st.error("🚨 Litigation Trigger: Adjuster refused to revise offer despite audit pressure.")
        with st.spinner("📄 Initiating simulated litigation timeline..."):
            time.sleep(1)
        st.markdown("""
        ### 📜 Projected Litigation Milestones
        - Complaint Filed
        - Discovery on claim suppression tactics
        - Subpoena ALOG / CIQ software usage logs
        - Deposition of adjuster and supervisor
        - Jury simulation indicating internal suppression exposure
        """)

    elif decision == "REVISE_OFFER_
