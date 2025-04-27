# --- Section 9: Call Centre Escalation Tracker ---

import streamlit as st
import datetime

def run():
    st.title("Section 9: Call Centre Escalation Tracker")
    st.markdown("---")

    # Initialize call log in session state
    if "call_escalation_log" not in st.session_state:
        st.session_state["call_escalation_log"] = []

    st.subheader("📞 Log a New Call Attempt")

    adjuster_name = st.text_input("Adjuster's Name", placeholder="e.g., Mary Jones")
    contact_date = st.date_input("Call Date", datetime.date.today())
    contact_time = st.time_input("Call Time", datetime.datetime.now().time())
    outcome = st.selectbox("Call Outcome", [
        "✅ Adjuster Escalated Internally (Awaiting Response)",
        "❌ Adjuster Refused to Engage",
        "📞 Left Voicemail / No Contact",
        "🕓 Adjuster Requested More Time",
