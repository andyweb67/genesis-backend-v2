# --- Section 3: Adjuster Setup ---

import streamlit as st

def run():
    st.title("Section 3: Adjuster Setup")
    st.markdown("---")

    if "gds_ready" not in st.session_state:
        st.error("❌ Please complete the Upload & GDS (Section 1) first.")
        return

    st.subheader("👤 Adjuster Information")

    adjuster_name = st.text_input("Adjuster's Name", placeholder="e.g., Mary Jones")
    adjuster_email = st.text_input("Adjuster's Email", placeholder="e.g., mary.jones@insurer.com")
    policy_limit = st.text_input("Policy Limit (Optional)", placeholder="e.g., 50,000")

    st.markdown("---")

    if st.button("✅ Confirm Adjuster Details"):
        st.session_state["adjuster_info"] = {
            "adjuster_name": adjuster_name.strip(),
            "adjuster_email": adjuster_email.strip(),
            "policy_limit": policy_limit.strip()
        }
        st.success("Adjuster information saved successfully.")

    # --- If previously saved, show summary ---
    if "adjuster_info" in st.session_state:
        adjuster_info = st.session_state["adjuster_info"]
        st.markdown(f"""
            ### 📋 Adjuster Summary
            - **Name:** {adjuster_info.get("adjuster_name", "N/A")}
            - **Email:** {adjuster_info.get("adjuster_email", "N/A")}
            - **Policy Limit:** ${adjuster_info.get("policy_limit", "N/A")}
        """)

