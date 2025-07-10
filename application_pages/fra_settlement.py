
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def run_fra_settlement_page():
    st.header("Forward Rate Agreement (FRA) Settlement Simulator")
    st.markdown(\"\"\"
---
### Overview

The **Forward Rate Agreement (FRA) Settlement Simulator** is an interactive tool designed to demystify the mechanics of Forward Rate Agreements. An FRA is an over-the-counter (OTC) derivative contract between two parties that determines the rate of interest, or the exchange rate, to be paid on an agreed notional amount, on a future date. Essentially, it allows parties to lock in an interest rate for a future period.

This application enables users to:
- Configure various FRA terms (Notional Principal, Fixed Rate, Start/End Periods).
- Simulate different market reference rates at settlement.
- Observe the real-time calculation of net payments and their present value (cash settlement).
- Gain intuitive understanding of how FRAs are used to hedge interest rate risk.

### Learning Outcomes

Upon using this simulator, you will be able to:
- **Understand FRA Mechanics**: Grasp the fundamental structure and purpose of a Forward Rate Agreement.
- **Calculate FRA Settlement**: Perform step-by-step calculations for fixed interest, floating interest, net payment, and cash settlement.
- **Analyze Market Impact**: Comprehend how changes in the market reference rate at settlement influence the FRA's value and payment direction.
- **Visualize Risk/Reward**: Interpret graphical representations of FRA cash flows and sensitivities.

### Features

- **Dynamic Input Controls**: Easily adjust all relevant FRA parameters using interactive sliders and number inputs.
- **Real-time Calculations**: See immediate updates to all calculated values and visualizations as inputs change.
- **Graphical Insights**: Interactive Plotly charts to compare interest payments and analyze cash settlement sensitivity to market rates.
- **Clear Explanations**: Inline explanations and narrative interpretations of the results to enhance learning.

### How It Explains the Concept

This simulator brings the theoretical concept of FRAs to life by:
- **Demystifying Formulas**: All key formulas for net payment and cash settlement are displayed using LaTeX, showing exactly how calculations are performed.
- **Illustrating Scenarios**: By allowing users to vary the Market Reference Rate (MRR), the tool demonstrates how an FRA behaves as a hedge:
    - If $MRR_{B-A} > IFR_{A,B-A}$: The fixed-rate payer (borrower) receives a payment from the fixed-rate receiver (lender), effectively offsetting higher borrowing costs in the market.
    - If $MRR_{B-A} < IFR_{A,B-A}$: The fixed-rate payer makes a payment to the fixed-rate receiver, as their locked-in rate was higher than the current market rate.
- **Highlighting Present Value**: Emphasizes that FRA settlement happens at the start of the interest period (settlement date) but is based on rates observed then, thus requiring discounting to present value.

---
\"\"\")

    st.sidebar.header("FRA Parameters")

    # FRA Term Sheet Input
    notional_principal = st.sidebar.number_input(
        "Notional Principal",
        min_value=100_000,
        max_value=100_000_000,
        value=10_000_000,
        step=100_000,
        help="The principal amount on which interest payments are based."
    )
    fixed_rate = st.sidebar.slider(
        "Fixed Rate (IFR)",
        min_value=0.00,
        max_value=0.10,
        value=0.0525,
        step=0.0001,
        format="%.4f%%",
        help="The implied forward rate ($IFR_{A,B-A}$) agreed at the inception of the FRA."
    )
    start_period = st.sidebar.number_input(
        "Start Period (A) (months)",
        min_value=0,
        max_value=60,
        value=3,
        step=1,
        help="Months from today until the FRA's interest period begins (settlement date)."
    )
    end_period = st.sidebar.number_input(
        "End Period (B) (months)",
        min_value=1,
        max_value=120,
        value=6,
        step=1,
        help="Months from today until the FRA's interest period ends."
    )
    days_in_year_basis = st.sidebar.number_input(
        "Days in Year Basis",
        min_value=1,
        value=360,
        step=1,
        help="The day count convention for annualizing rates (e.g., 360 for 30/360 or 365 for Actual/365)."
    )

    st.sidebar.header("Market Rate Simulation")
    market_reference_rate = st.sidebar.slider(
        "Market Reference Rate (MRR)",
        min_value=0.01,
        max_value=0.10,
        value=0.055,
        step=0.0001,
        format="%.4f%%",
        help="The prevailing market interest rate ($MRR_{B-A}$) observed at the settlement date, used for floating interest calculation and discounting."
    )

    st.subheader("FRA Settlement Calculations")

    if end_period <= start_period:
        st.error("Error: End Period (B) must be greater than Start Period (A). Please adjust the input values.")
        return

    if days_in_year_basis <= 0:
        st.error("Error: Days in Year Basis must be a positive number. Please adjust the input value.")
        return

    # Calculate Period Fraction (assuming 30/360 convention for simplicity, or based on days_in_year_basis)
    period_in_months = end_period - start_period
    period_fraction = period_in_months / 12 # This is (B-A)/12 for annual rate

    st.markdown(r"**Period Fraction:** $\frac{\text{End Period} - \text{Start Period}}{12} = \frac{" + f"{end_period} - {start_period}" + r"}{12} = " + f"{period_fraction:.4f}$")

    # Fixed Interest Payment
    fixed_interest_payment = notional_principal * fixed_rate * period_fraction
    st.markdown(r"**Fixed Interest Payment:** $" + f"{notional_principal:,.2f}" + r" \times " + f"{fixed_rate:.4f}" + r" \times " + f"{period_fraction:.4f}" + r" = $" + f"{fixed_interest_payment:,.2f}")

    # Floating Interest Payment
    floating_interest_payment = notional_principal * market_reference_rate * period_fraction
    st.markdown(r"**Floating Interest Payment:** $" + f"{notional_principal:,.2f}" + r" \times " + f"{market_reference_rate:.4f}" + r" \times " + f"{period_fraction:.4f}" + r" = $" + f"{floating_interest_payment:,.2f}")

    # Net Payment at Maturity (undiscounted)
    net_payment_at_maturity = floating_interest_payment - fixed_interest_payment
    st.markdown(r"**Net Payment at Maturity (undiscounted):** $" + f"{floating_interest_payment:,.2f}" + r" - $" + f"{fixed_interest_payment:,.2f}" + r" = $" + f"{net_payment_at_maturity:,.2f}")
    st.markdown(\"\"\"
The **Net Payment** formula is:
$$ (MRR_{B-A} - IFR_{A,B-A}) \\times \\text{Notional Principal} \\times \\text{Period Fraction} $$
Where $\\text{Period Fraction}$ is typically `Days / 360` or `1 / Number of Periods per year`.
\"\"\")

    # Cash Settlement (Present Value)
    discount_factor = 1 + (market_reference_rate * period_fraction)
    if discount_factor <= 0:
        st.error("Error: Discount factor is zero or negative. Please adjust input rates.")
        return

    cash_settlement_pv = net_payment_at_maturity / discount_factor
    st.markdown(r"**Cash Settlement (Present Value):** $ \frac{" + f"{net_payment_at_maturity:,.2f}" + r"}{1 + " + f"{market_reference_rate:.4f}" + r" \times " + f"{period_fraction:.4f}" + r"} = $" + f"{cash_settlement_pv:,.2f}")
    st.markdown(\"\"\"
The **Cash Settlement (Present Value)** formula is:
$$ \\text{Cash Settlement (PV)} = \\frac{\\text{Net Payment}}{1 + MRR_{B-A} \\times \\text{Period Fraction}} $$
\"\"\")

    st.markdown("---")
    st.subheader("Narrative Interpretation of Net Payment")
    if market_reference_rate > fixed_rate:
        st.markdown(f\"\"\"
        Since the Market Reference Rate ($MRR_{{B-A}}$) of {market_reference_rate:.4f} ({market_reference_rate:.2%}) is **higher** than the Fixed Rate ($IFR_{{A,B-A}}$) of {fixed_rate:.4f} ({fixed_rate:.2%}), the fixed-rate payer (borrower) benefits.
        The borrower effectively pays a lower fixed rate than the current market rate, and thus **receives a payment** from the fixed-rate receiver (lender) to compensate for the difference.
        The Net Payment at Maturity is ${net_payment_at_maturity:,.2f}, and the Cash Settlement (PV) is ${cash_settlement_pv:,.2f}.
        \"\"\")
    elif market_reference_rate < fixed_rate:
        st.markdown(f\"\"\"
        Since the Market Reference Rate ($MRR_{{B-A}}$) of {market_reference_rate:.4f} ({market_reference_rate:.2%}) is **lower** than the Fixed Rate ($IFR_{{A,B-A}}$) of {fixed_rate:.4f} ({fixed_rate:.2%}), the fixed-rate receiver (lender) benefits.
        The borrower effectively pays a higher fixed rate than the current market rate, and thus **makes a payment** to the fixed-rate receiver.
        The Net Payment at Maturity is ${net_payment_at_maturity:,.2f}, and the Cash Settlement (PV) is ${cash_settlement_pv:,.2f}.
        \"\"\")
    else:
        st.markdown(f\"\"\"
        Since the Market Reference Rate ($MRR_{{B-A}}$) of {market_reference_rate:.4f} ({market_reference_rate:.2%}) is **equal** to the Fixed Rate ($IFR_{{A,B-A}}$) of {fixed_rate:.4f} ({fixed_rate:.2%}), the Net Payment is zero.
        Both parties are indifferent, and there is no cash settlement.
        \"\"\")

    st.markdown("---")
    st.subheader("Visualizations")

    # Bar Chart: Aggregated Comparison
    fra_data = {
        "Category": ["Fixed Interest Payment", "Floating Interest Payment", "Net Payment"],
        "Amount": [fixed_interest_payment, floating_interest_payment, net_payment_at_maturity]
    }
    fra_df = pd.DataFrame(fra_data)

    fig_bar = px.bar(
        fra_df,
        x="Category",
        y="Amount",
        title="Aggregated Comparison: FRA Interest Payments and Net Settlement",
        color="Category",
        color_discrete_map={
            "Fixed Interest Payment": "lightseagreen",
            "Floating Interest Payment": "royalblue",
            "Net Payment": "salmon"
        },
        labels={"Amount": "Amount ($)", "Category": "Payment Type"},
        hover_data={"Amount": ':.2f'}
    )
    fig_bar.update_layout(title_x=0.5, font_size=12) # Center title and set font size
    st.plotly_chart(fig_bar, use_container_width=True)

    # Line Chart: Cash Settlement vs. Market Reference Rate
    mrr_range = np.linspace(0.01, 0.10, 100) # 1% to 10%
    cash_settlement_sensitivity = []

    for mrr_val in mrr_range:
        float_int_pay_sens = notional_principal * mrr_val * period_fraction
        net_pay_sens = float_int_pay_sens - fixed_interest_payment
        discount_factor_sens = 1 + (mrr_val * period_fraction)
        if discount_factor_sens > 0:
            cash_settlement_sens = net_pay_sens / discount_factor_sens
        else:
            cash_settlement_sens = np.nan # Handle invalid discount factor
        cash_settlement_sensitivity.append(cash_settlement_sens)

    sensitivity_df = pd.DataFrame({
        "Market Reference Rate (MRR)": mrr_range,
        "Cash Settlement ($)": cash_settlement_sensitivity
    })

    fig_line = px.line(
        sensitivity_df,
        x="Market Reference Rate (MRR)",
        y="Cash Settlement ($)",
        title="FRA Cash Settlement vs. Market Reference Rate (MRR)",
        markers=True,
        labels={"Market Reference Rate (MRR)": "Market Reference Rate (MRR) (%)", "Cash Settlement ($)": "Cash Settlement ($)"},
        hover_data={"Market Reference Rate (MRR)": ':.2%', "Cash Settlement ($)": ':.2f'}
    )
    fig_line.update_layout(title_x=0.5, hovermode="x unified", font_size=12)
    fig_line.update_xaxes(tickformat=".2%") # Format x-axis as percentage

    # Add vertical line for Fixed Rate (IFR)
    fig_line.add_vline(
        x=fixed_rate,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Fixed Rate (IFR): {fixed_rate:.2%}",
        annotation_position="top left"
    )

    # Add horizontal line for Zero Settlement
    fig_line.add_hline(
        y=0,
        line_dash="dot",
        line_color="grey",
        annotation_text="Zero Settlement",
        annotation_position="bottom right"
    )
    st.plotly_chart(fig_line, use_container_width=True)
