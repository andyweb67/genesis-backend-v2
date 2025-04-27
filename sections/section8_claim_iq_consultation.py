# --- Section 8: Claim IQ Consultation Review ---

import streamlit as st

def run():
    st.title("Section 8: Claim IQ Consultation Review")
    st.markdown("---")

    st.subheader("🔍 Overview")
    st.markdown("""
    This claim was compromised from the moment the adjuster received the file. GEICO's **Claim IQ** software predetermined valuation,
    leaving the adjuster as a controlled executor with no true authority to negotiate.

    Every step taken by the adjuster was influenced by ALP (Average Loss Payment) metrics — a system designed to suppress payouts 
    systematically, regardless of claim legitimacy. Genesis exposes these suppression systems and forces accountability.
    """)

    st.subheader("📄 Internal Claim IQ Evaluation Summary")
    st.table({
        "Category": ["Permanency", "Pain & Suffering", "Claim IQ General Range", "Final Evaluated"],
        "Value": ["34% WPI", "$2,000", "$14,072–$20,072", "$2,000 (Total Offer)"]
    })

    st.subheader("📌 Suppression of Additional Damages")
    st.markdown("""
    - **Mileage Claimed:** $250 → **Evaluated:** $0  
    - **Future Medicals / Dental Needs:** Present in medical estimate, **disregarded**  
    - **Lost Income Claimed:** $292.33 → **Minimized**  
    - **Loss of Consortium Claim:** Raised but **not documented**  
    - **Surveillance Authorized:** $1,000 approved for investigation  
    - **Supervisor Approval:** Anchored strictly to Claim IQ high range
    """)

    st.warning("⚠️ GEICO initially demanded a full release of all claims in exchange for policy limits.")
    st.success("✅ After legal escalation, GEICO retracted the release condition — confirming suppression exposure.")

    st.subheader("📈 Timeline of Suppression and Escalation")
    st.markdown("""
    | Event | Amount | Insight |
    |:------|:-------|:--------|
    | Attorney Demand | $75,000 | Based on injury severity (34% WPI) |
    | 3rd Party Paid | $25,000 | Third-party limits exhausted |
    | UIM Demand to GEICO | $50,000 | Policy limits triggered |
    | GEICO Offer #1 | $16,000 | Offer pegged to low Claim IQ range |
    | GEICO Offer #2 | $19,000 | Minor increase after audit pressure |
    | Genesis Escalation | — | Full suppression exposed |
    | GEICO Offers Full Limits | $50,000 | Following pressure campaign |
    | Full Release Condition Retracted | ✅ | Proved bad faith threat worked |
    """, unsafe_allow_html=True)

    st.info("""
    Genesis is the **only system** that not only detects this suppression — it turns the insurer’s internal logic **against them**, 
    forcing transparency, leveraging escalation, and exposing their risk in litigation.
    """)

