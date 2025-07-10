
import streamlit as st
import os

# Ensure the application_pages directory exists
# This part won't run when writing the file, but it's good practice for local execution
if not os.path.exists("application_pages"):
    os.makedirs("application_pages")

st.set_page_config(page_title="QuLab", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab: Derivative Pricing and Valuation")
st.divider()
st.markdown("""
In this lab, we delve into the core concepts of **Derivative Pricing and Valuation of Forward Contracts**, with a specific focus on **Forward Rate Agreements (FRAs)** and the underlying mechanisms for instruments with varying maturities. This interactive application provides a hands-on approach to understanding complex financial derivatives, their valuation, and how they are used for hedging interest rate risk.

---
### Business Logic Explained: Forward Rate Agreements (FRAs)

A Forward Rate Agreement (FRA) is a financial contract between two parties to exchange an interest rate payment on a notional principal amount at a future date. The purpose of an FRA is to lock in an interest rate for a future borrowing or lending period, thereby hedging against future interest rate fluctuations.

**Key Components of an FRA:**
- **Notional Principal**: The nominal amount on which the interest payment is calculated. No exchange of principal actually occurs.
- **Fixed Rate (IFR)**: The implied forward rate agreed upon at the inception of the contract. This is the rate the fixed-rate payer agrees to pay (or receive).
- **Market Reference Rate (MRR)**: The prevailing market interest rate (e.g., LIBOR, SOFR) observed at the settlement date, used to determine the floating interest payment.
- **Start Period (A)**: The time from today until the FRA's interest period begins (the settlement date).
- **End Period (B)**: The time from today until the FRA's interest period ends.
- **Period Fraction**: The length of the interest period, usually expressed as a fraction of a year (e.g., `(B-A)/12` for months, or `Days / Day Count Basis`).

**How FRAs Work:**
At the settlement date (time A), the Market Reference Rate ($MRR_{B-A}$) for the period (B-A) is compared to the Fixed Rate ($IFR_{A,B-A}$) agreed upon in the FRA. The net difference in interest payments, based on the notional principal and period fraction, is calculated. This net amount is then discounted back from the end of the interest period (B) to the settlement date (A) to arrive at the cash settlement.

- If $MRR_{B-A} > IFR_{A,B-A}$: The floating rate borrower (who agreed to pay fixed and receive floating) would have paid more in the market. The FRA compensates them: the fixed-rate receiver (the counterparty) pays the fixed-rate payer.
- If $MRR_{B-A} < IFR_{A,B-A}$: The floating rate borrower would have paid less in the market. The fixed-rate payer pays the fixed-rate receiver.

This application allows you to interactively explore these concepts, visualize the cash flows, and understand the sensitivity of the cash settlement to changes in market rates.

---
""")

# Your code starts here
page = st.sidebar.selectbox(label="Navigation", options=["FRA Settlement Simulator", "APR Conversion Utility"])

if page == "FRA Settlement Simulator":
    from application_pages.fra_settlement import run_fra_settlement_page
    run_fra_settlement_page()
elif page == "APR Conversion Utility":
    from application_pages.apr_conversion import run_apr_conversion_page
    run_apr_conversion_page()

# Your code ends
st.divider()

st.subheader("References")
st.markdown("""
- Hull, J. C. (2018). *Options, Futures, and Other Derivatives* (10th ed.). Pearson.
- CFA Institute Curriculum. *Level II: Derivatives*.
""")

st.divider()
st.write("© 2025 QuantUniversity. All Rights Reserved.")
st.caption("The purpose of this demonstration is solely for educational use and illustration. "
           "Any reproduction of this demonstration "
           "requires prior written consent from QuantUniversity. "
           "This lab was generated using the QuCreate platform. QuCreate relies on AI models for generating code, which may contain inaccuracies or errors.")
