
import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Forward Contract Valuation Simulator", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab: Forward Contract Valuation Simulator")
st.divider()
st.markdown(r\"\"\"
### Purpose and Objectives
The "Forward Contract Valuation Simulator" Streamlit application aims to provide an interactive platform for users, particularly finance students and aspiring traders, to understand and simulate the pricing and mark-to-market (MTM) valuation of forward contracts. The application will demonstrate how initial forward prices are determined based on spot prices and risk-free rates, analyze the evolution of a forward contract's MTM value over its life, and differentiate between contracts with and without additional costs or benefits. A key objective is to visualize potential gains and losses for both long and short positions under varying market conditions, thereby demystifying core derivative concepts like the no-arbitrage principle and mark-to-market adjustments through hands-on engagement.

### Key Value Propositions
*   **Interactive Learning:** Provides a dynamic, hands-on experience for complex financial concepts.
*   **Clarity through Visualization:** Converts abstract financial formulas into intuitive, real-time charts.
*   **Practical Application:** Bridges theoretical knowledge with practical valuation scenarios.
*   **Accessibility:** Offers an easy-to-use interface without requiring advanced programming knowledge.

---

### Understanding Forward Contracts

A forward contract is a customized contract between two parties to buy or sell an asset at a specified price on a future date. Unlike futures, forward contracts are over-the-counter (OTC) instruments and are not traded on exchanges.

#### 1. Initial Forward Price ($F_0(T)$)
The initial forward price is determined at the inception of the contract, such that there is no arbitrage opportunity.

*   **Without costs/benefits (e.g., dividends for equities, storage costs for commodities):**
    $$F_0(T) = S_0 (1+r)^T$$
    Where:
    *   $S_0$ is the current spot price of the underlying asset.
    *   $r$ is the risk-free interest rate (continuously compounded or discrete, depending on convention; here, we assume discrete compounding for simplicity).
    *   $T$ is the time to maturity of the contract in years.

*   **With costs/benefits (e.g., present value of income $PV_0(I)$ and costs $PV_0(C)$):**
    $$F_0(T) = (S_0 - PV_0(I) + PV_0(C)) (1+r)^T$$
    Where:
    *   $PV_0(I)$ is the present value of all expected income (e.g., dividends) from the underlying asset until maturity.
    *   $PV_0(C)$ is the present value of all expected costs (e.g., storage costs) associated with holding the underlying asset until maturity.

#### 2. Mark-to-Market (MTM) Value ($V_t(T)$)
The MTM value of a forward contract represents its current worth at any given time $t$ before maturity. It reflects the profit or loss that would be realized if the contract were closed out at the current market conditions.

*   **For a Long Position (you agree to buy the asset):**
    *   Without costs/benefits:
        $$V_t(T) = S_t - F_0(T)(1+r)^{-(T-t)}$$
    *   With costs/benefits:
        $$V_t(T) = (S_t - PV_t(I) + PV_t(C)) - F_0(T)(1+r)^{-(T-t)}$$
    Where:
    *   $S_t$ is the current spot price of the underlying asset at time $t$.
    *   $F_0(T)$ is the initial forward price.
    *   $PV_t(I)$ is the present value of income expected from time $t$ to $T$.
    *   $PV_t(C)$ is the present value of costs expected from time $t$ to $T$.
    *   $(T-t)$ is the remaining time to maturity.

*   **For a Short Position (you agree to sell the asset):**
    The MTM value for a short position is the negative of the long position's MTM value:
    $$V_t(T)_{\\text{Short}} = -V_t(T)_{\\text{Long}}$$

This application allows you to interactively explore these concepts by adjusting various parameters and observing the impact on forward prices and MTM values.
\"\"\")

st.header("Simulation Parameters")
st.markdown("Adjust the parameters below to observe the impact on forward contract pricing and valuation.")

# Your code starts here
# Using session state to persist values across reruns and pages
if 'S0' not in st.session_state:
    st.session_state.S0 = 100.0
if 'r' not in st.session_state:
    st.session_state.r = 0.05
if 'T' not in st.session_state:
    st.session_state.T = 1.0
if 'PV0_I' not in st.session_state:
    st.session_state.PV0_I = 0.0
if 'PV0_C' not in st.session_state:
    st.session_state.PV0_C = 0.0
if 'include_costs_benefits' not in st.session_state:
    st.session_state.include_costs_benefits = False

if 't' not in st.session_state:
    st.session_state.t = 0.0
if 'St' not in st.session_state:
    st.session_state.St = 100.0
if 'PVt_I' not in st.session_state:
    st.session_state.PVt_I = 0.0
if 'PVt_C' not in st.session_state:
    st.session_state.PVt_C = 0.0
if 'position_type' not in st.session_state:
    st.session_state.position_type = "Long"

with st.sidebar:
    st.subheader("Contract Inception Parameters ($F_0(T)$)")
    st.session_state.S0 = st.number_input("Initial Spot Price ($S_0$)", min_value=1.0, max_value=500.0, value=st.session_state.S0, step=1.0, format="%.2f")
    st.session_state.r = st.number_input("Risk-Free Rate ($r$)", min_value=0.001, max_value=0.20, value=st.session_state.r, step=0.001, format="%.4f")
    st.session_state.T = st.number_input("Time to Maturity ($T$, years)", min_value=0.25, max_value=10.0, value=st.session_state.T, step=0.25, format="%.2f")

    st.session_state.include_costs_benefits = st.checkbox("Include Costs/Benefits", value=st.session_state.include_costs_benefits)

    if st.session_state.include_costs_benefits:
        st.session_state.PV0_I = st.number_input("Initial PV of Income ($PV_0(I)$)", min_value=0.0, max_value=100.0, value=st.session_state.PV0_I, step=0.1, format="%.2f")
        st.session_state.PV0_C = st.number_input("Initial PV of Costs ($PV_0(C)$)", min_value=0.0, max_value=100.0, value=st.session_state.PV0_C, step=0.1, format="%.2f")
    else:
        st.session_state.PV0_I = 0.0
        st.session_state.PV0_C = 0.0

    st.subheader("Current Valuation Parameters ($V_t(T)$)")
    st.session_state.t = st.slider("Current Time ($t$, years)", min_value=0.0, max_value=st.session_state.T, value=min(st.session_state.t, st.session_state.T), step=0.01)
    st.session_state.St = st.number_input("Current Spot Price ($S_t$)", min_value=1.0, max_value=500.0, value=st.session_state.St, step=1.0, format="%.2f")

    if st.session_state.include_costs_benefits:
        st.session_state.PVt_I = st.number_input("Current PV of Income ($PV_t(I)$)", min_value=0.0, max_value=100.0, value=st.session_state.PVt_I, step=0.1, format="%.2f")
        st.session_state.PVt_C = st.number_input("Current PV of Costs ($PV_t(C)$)", min_value=0.0, max_value=100.0, value=st.session_state.PVt_C, step=0.1, format="%.2f")
    else:
        st.session_state.PVt_I = 0.0
        st.session_state.PVt_C = 0.0

    st.session_state.position_type = st.radio("Position Type", ["Long", "Short"], index=0 if st.session_state.position_type == "Long" else 1)

# Calculations
def calculate_forward_price(S0, r, T, PV0_I, PV0_C, include_costs_benefits):
    if include_costs_benefits:
        return (S0 - PV0_I + PV0_C) * (1 + r)**T
    else:
        return S0 * (1 + r)**T

def calculate_mtm_value(St, F0T, r, T, t, PVt_I, PVt_C, include_costs_benefits, position_type):
    time_to_maturity_remaining = T - t
    if time_to_maturity_remaining <= 0: # At or past maturity
        long_mtm = St - F0T
    else:
        if include_costs_benefits:
            long_mtm = (St - PVt_I + PVt_C) - F0T * (1 + r)**(-time_to_maturity_remaining)
        else:
            long_mtm = St - F0T * (1 + r)**(-time_to_maturity_remaining)

    if position_type == "Short":
        return -long_mtm
    else:
        return long_mtm

F0T = calculate_forward_price(st.session_state.S0, st.session_state.r, st.session_state.T, st.session_state.PV0_I, st.session_state.PV0_C, st.session_state.include_costs_benefits)
VtT = calculate_mtm_value(st.session_state.St, F0T, st.session_state.r, st.session_state.T, st.session_state.t, st.session_state.PVt_I, st.session_state.PVt_C, st.session_state.include_costs_benefits, st.session_state.position_type)

st.subheader("Calculated Values")
col1, col2 = st.columns(2)
with col1:
    st.metric("Initial Forward Price ($F_0(T)$)", f"${F0T:.2f}")
with col2:
    st.metric("Current MTM Value ($V_t(T)$)", f"${VtT:.2f}")

st.divider()

### Visualizations

# 1. Trend Plot: MTM Value Over Time
st.subheader("1. MTM Value Over Time")
st.markdown("This plot shows the hypothetical evolution of the Mark-to-Market (MTM) value of the forward contract from inception ($t=0$) to maturity ($t=T$). The spot price path is assumed to be linear for demonstration.")

time_points = np.linspace(0, st.session_state.T, 100)
spot_path = []
for tm in time_points:
    if tm <= st.session_state.t:
        if st.session_state.t > 0:
            spot_val = st.session_state.S0 + (st.session_state.St - st.session_state.S0) * (tm / st.session_state.t)
        else:
            spot_val = st.session_state.S0
    else:
        if st.session_state.T - st.session_state.t > 0:
            spot_val = st.session_state.St + (F0T - st.session_state.St) * ((tm - st.session_state.t) / (st.session_state.T - st.session_state.t))
        else:
            spot_val = st.session_state.St
    spot_path.append(spot_val)

mtm_long_path = [calculate_mtm_value(S, F0T, st.session_state.r, st.session_state.T, tp, st.session_state.PVt_I, st.session_state.PVt_C, st.session_state.include_costs_benefits, "Long") for S, tp in zip(spot_path, time_points)]
mtm_short_path = [-val for val in mtm_long_path]

fig_trend = go.Figure()
fig_trend.add_trace(go.Scatter(x=time_points, y=mtm_long_path, mode='lines', name='Long Position MTM', line=dict(color='green')))
fig_trend.add_trace(go.Scatter(x=time_points, y=mtm_short_path, mode='lines', name='Short Position MTM', line=dict(color='red')))
fig_trend.add_trace(go.Scatter(x=[st.session_state.t], y=[VtT if st.session_state.position_type == "Long" else -VtT],
                             mode='markers', name=f'Current {st.session_state.position_type} MTM',
                             marker=dict(size=10, color='blue', symbol='star')))

fig_trend.update_layout(title="MTM Value Over Time",
                        xaxis_title="Time (Years)",
                        yaxis_title="MTM Value ($)",
                        hovermode="x unified")
st.plotly_chart(fig_trend, use_container_width=True)


# 2. Relationship Plot: MTM Value vs. Current Spot Price
st.subheader("2. MTM Value vs. Current Spot Price ($S_t$)")
st.markdown("This plot illustrates how the MTM value changes with variations in the current spot price ($S_t$) for a fixed time $t$.")

spot_range = np.linspace(max(1.0, st.session_state.St * 0.5), st.session_state.St * 1.5, 100)
mtm_long_spot_sensitivity = [calculate_mtm_value(S_val, F0T, st.session_state.r, st.session_state.T, st.session_state.t, st.session_state.PVt_I, st.session_state.PVt_C, st.session_state.include_costs_benefits, "Long") for S_val in spot_range]
mtm_short_spot_sensitivity = [-val for val in mtm_long_spot_sensitivity]

fig_relation = go.Figure()
fig_relation.add_trace(go.Scatter(x=spot_range, y=mtm_long_spot_sensitivity, mode='lines', name='Long Position MTM', line=dict(color='green')))
fig_relation.add_trace(go.Scatter(x=spot_range, y=mtm_short_spot_sensitivity, mode='lines', name='Short Position MTM', line=dict(color='red')))
fig_relation.add_trace(go.Scatter(x=[st.session_state.St], y=[VtT if st.session_state.position_type == "Long" else -VtT],
                                mode='markers', name=f'Current {st.session_state.position_type} MTM',
                                marker=dict(size=10, color='blue', symbol='star')))

fig_relation.update_layout(title="MTM Value vs. Current Spot Price",
                           xaxis_title="Current Spot Price ($S_t$)",
                           yaxis_title="MTM Value ($V_t(T)$)",
                           hovermode="x unified")
st.plotly_chart(fig_relation, use_container_width=True)

# 3. Aggregated Comparison: Profit/Loss at Maturity
st.subheader("3. Profit/Loss at Maturity ($T$)")
st.markdown("This bar chart visualizes the Profit/Loss (P&L) at maturity for various hypothetical settlement spot prices ($S_T$) relative to the initial forward price ($F_0(T)$).")

settlement_spot_scenarios = [F0T * 0.8, F0T * 0.9, F0T, F0T * 1.1, F0T * 1.2]
scenario_labels = [f"0.8 * F0T ({settlement_spot_scenarios[0]:.2f})",
                   f"0.9 * F0T ({settlement_spot_scenarios[1]:.2f})",
                   f"1.0 * F0T ({settlement_spot_scenarios[2]:.2f})",
                   f"1.1 * F0T ({settlement_spot_scenarios[3]:.2f})",
                   f"1.2 * F0T ({settlement_spot_scenarios[4]:.2f})"]

pnl_long_scenarios = [s_t_val - F0T for s_t_val in settlement_spot_scenarios]
pnl_short_scenarios = [-val for val in pnl_long_scenarios]

pnl_to_display = pnl_long_scenarios if st.session_state.position_type == "Long" else pnl_short_scenarios
colors = ['green' if pnl >= 0 else 'red' for pnl in pnl_to_display]

fig_pnl = go.Figure(data=[go.Bar(x=scenario_labels, y=pnl_to_display, marker_color=colors)])
fig_pnl.update_layout(title=f"Profit/Loss at Maturity for a {st.session_state.position_type} Position",
                      xaxis_title="Settlement Spot Price ($S_T$) Scenario",
                      yaxis_title="Profit/Loss at Maturity ($P\&L_T$)",
                      yaxis_tickformat=".2f")

st.plotly_chart(fig_pnl, use_container_width=True)

# Your code ends
st.divider()
st.write("© 2025 QuantUniversity. All Rights Reserved.")
st.caption("The purpose of this demonstration is solely for educational use and illustration. "
           "Any reproduction of this demonstration "
           "requires prior written consent from QuantUniversity. "
           "This lab was generated using the QuCreate platform. QuCreate relies on AI models for AI models for generating code, which may contain inaccuracies or errors.")
