
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd

def calculate_forward_price(S0, r, T, PV0_I, PV0_C, include_costs_benefits):
    if include_costs_benefits:
        F0T = (S0 - PV0_I + PV0_C) * (1 + r)**T
    else:
        F0T = S0 * (1 + r)**T
    return F0T

def calculate_mtm_value(St, F0T, r, T, t, PVt_I, PVt_C, include_costs_benefits):
    if T - t < 0: # Handle cases where current time exceeds maturity
        return 0.0
    
    discount_factor = (1 + r)**(-(T - t))

    if include_costs_benefits:
        VtT = (St - PVt_I + PVt_C) - F0T * discount_factor
    else:
        VtT = St - F0T * discount_factor
    return VtT

def run_page1():
    st.header("Forward Contract Valuation Simulator")
    st.markdown("---")

    # Business Logic Explanation
    st.markdown(\"\"\"
    ## Overview
    This application allows you to explore the pricing and valuation of forward contracts. A forward contract is a customized contract between two parties to buy or sell an asset at a specified price on a future date.

    ### Key Concepts:
    *   **Initial Forward Price ($F_0(T)$):** This is the price agreed upon today for a transaction that will occur at a future date $T$. It's determined by the current spot price ($S_0$), the risk-free rate ($r$), and the time to maturity ($T$), often adjusted for any costs or benefits associated with holding the underlying asset.
    *   **Mark-to-Market (MTM) Value ($V_t(T)$):** This represents the current value of the forward contract at any time $t$ before maturity. It reflects the profit or loss that would be realized if the contract were closed out today. The MTM value changes as the spot price, interest rates, and time to maturity evolve.

    ### No-Arbitrage Principle:
    The formulas used in this simulator are derived from the no-arbitrage principle, which states that in an efficient market, it should not be possible to make a risk-free profit by simultaneously entering into offsetting transactions. This principle ensures that the forward price reflects the cost of replicating the forward contract using the underlying asset and risk-free borrowing/lending.

    ### Why Varying Maturities?
    While a single forward contract has a fixed maturity, understanding how the value changes *over time* (as $t$ approaches $T$) and how different *initial maturities* ($T$) impact the initial forward price is crucial. This simulator allows you to observe the MTM value as time progresses and market conditions change, providing insights into the contract's sensitivity to these factors.
    \"\"\")
    st.markdown("---")

    st.subheader("Input Parameters")

    # Input Widgets - Contract Inception Parameters
    st.markdown("#### Contract Inception Parameters ($F_0(T)$ calculation)")
    col1, col2, col3 = st.columns(3)
    with col1:
        S0 = st.number_input("Initial Spot Price ($S_0$)", min_value=50.0, max_value=200.0, value=100.0, step=1.0, format="%.2f", help="The price of the underlying asset at the inception of the contract.")
    with col2:
        r = st.number_input("Risk-Free Rate ($r$)", min_value=0.01, max_value=0.10, value=0.05, step=0.001, format="%.3f", help="The annual risk-free interest rate (e.g., U.S. Treasury bill rate).")
    with col3:
        T = st.number_input("Time to Maturity ($T$, in years)", min_value=0.25, max_value=5.0, value=1.0, step=0.25, format="%.2f", help="The total time from inception until the contract expires.")

    include_costs_benefits = st.checkbox("Include Costs/Benefits (Income/Costs of Carry)", value=False, help="Toggle to include present values of income (e.g., dividends) or costs (e.g., storage costs) associated with the underlying asset.")

    if include_costs_benefits:
        col_inc1, col_inc2 = st.columns(2)
        with col_inc1:
            PV0_I = st.number_input("Initial PV of Income ($PV_0(I)$)", min_value=0.0, max_value=20.0, value=0.0, step=0.1, format="%.2f", help="The present value of any income expected from the underlying asset over the contract's life, at inception.")
        with col_inc2:
            PV0_C = st.number_input("Initial PV of Costs ($PV_0(C)$)", min_value=0.0, max_value=20.0, value=0.0, step=0.1, format="%.2f", help="The present value of any costs associated with holding the underlying asset over the contract's life, at inception.")
    else:
        PV0_I = 0.0
        PV0_C = 0.0

    st.markdown("---")
    st.markdown("#### Current Valuation Parameters ($V_t(T)$ calculation)")
    col4, col5 = st.columns(2)
    with col4:
        t_max = max(0.01, T) # Ensure t_max is at least 0.01 if T is very small or 0
        t = st.slider("Current Time ($t$, in years)", min_value=0.0, max_value=t_max, value=min(0.0, t_max), step=0.01, format="%.2f", help="The current time elapsed since the contract's inception. Must be less than or equal to Time to Maturity ($T$).")
        if t > T:
            st.warning(f"Current Time (t={t:.2f}) cannot be greater than Time to Maturity (T={T:.2f}). Adjusting t to T.")
            t = T # Auto-correct t if it exceeds T

    with col5:
        St_default = S0 # Default current spot price to initial spot price
        St = st.number_input("Current Spot Price ($S_t$)", min_value=0.0, max_value=300.0, value=St_default, step=1.0, format="%.2f", help="The current price of the underlying asset at time $t$.")

    if include_costs_benefits:
        col_inc3, col_inc4 = st.columns(2)
        with col_inc3:
            PVt_I = st.number_input("Current PV of Income ($PV_t(I)$)", min_value=0.0, max_value=20.0, value=0.0, step=0.1, format="%.2f", help="The present value of any remaining income from the underlying asset from time $t$ to $T$.")
        with col_inc4:
            PVt_C = st.number_input("Current PV of Costs ($PV_t(C)$)", min_value=0.0, max_value=20.0, value=0.0, step=0.1, format="%.2f", help="The present value of any remaining costs associated with holding the underlying asset from time $t$ to $T$.")
    else:
        PVt_I = 0.0
        PVt_C = 0.0

    position_type = st.radio("Position Type", ("Long", "Short"), help="Select whether you hold a long (buy) or short (sell) position in the forward contract.")

    st.markdown("---")
    st.subheader("Calculated Values")

    # Calculations
    F0T = calculate_forward_price(S0, r, T, PV0_I, PV0_C, include_costs_benefits)
    VtT_long = calculate_mtm_value(St, F0T, r, T, t, PVt_I, PVt_C, include_costs_benefits)
    VtT_short = -VtT_long # Short position MTM is the negative of long position MTM

    st.markdown(f"**Initial Forward Price ($F_0(T)$):** {F0T:,.2f}")
    if position_type == "Long":
        st.markdown(f"**Current MTM Value (Long Position, $V_t(T)$):** {VtT_long:,.2f}")
    else:
        st.markdown(f"**Current MTM Value (Short Position, $V_t(T)$):** {VtT_short:,.2f}")

    st.markdown("---")
    st.subheader("Valuation Formulas")

    # Valuation Formulas Display
    st.markdown("### Initial Forward Price ($F_0(T)$)")
    if include_costs_benefits:
        st.latex(r"F_0(T) = (S_0 - PV_0(I) + PV_0(C)) (1+r)^T")
    else:
        st.latex(r"F_0(T) = S_0 (1+r)^T")

    st.markdown("### Mark-to-Market (MTM) Value ($V_t(T)$) for a Long Position")
    if include_costs_benefits:
        st.latex(r"V_t(T) = (S_t - PV_t(I) + PV_t(C)) - F_0(T)(1+r)^{-(T-t)}")
    else:
        st.latex(r"V_t(T) = S_t - F_0(T)(1+r)^{-(T-t)}")

    st.markdown("### Mark-to-Market (MTM) Value ($V_t(T)$) for a Short Position")
    st.markdown(r"The MTM value for a short position is the negative of the long position's MTM value.")
    st.markdown(r"$$V_t(T)_{\text{Short}} = -V_t(T)_{\text{Long}}$$")

    st.markdown("---")
    st.subheader("Visualizations")

    # 1. Trend Plot (MTM over Time)
    st.markdown("#### MTM Value Over Time")
    st.markdown("This chart shows how the Mark-to-Market (MTM) value of the forward contract evolves from inception ($t=0$) to maturity ($t=T$), assuming a linear path for the spot price.")

    time_points = np.linspace(0, T, 100)
    S_end_at_maturity = S0 * (1 + r)**T 
    spot_prices_over_time = np.linspace(S0, S_end_at_maturity, len(time_points))

    mtm_long_trend = []
    mtm_short_trend = []
    for i, current_time_point in enumerate(time_points):
        remaining_time_ratio_0_to_T = (T - current_time_point) / T if T > 0 else 0
        current_PV_I_for_trend = PV0_I * remaining_time_ratio_0_to_T
        current_PV_C_for_trend = PV0_C * remaining_time_ratio_0_to_T

        mtm_long_trend.append(calculate_mtm_value(spot_prices_over_time[i], F0T, r, T, current_time_point, current_PV_I_for_trend, current_PV_C_for_trend, include_costs_benefits))
        mtm_short_trend.append(-mtm_long_trend[-1]) 

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(x=time_points, y=mtm_long_trend, mode='lines', name='Long Position MTM', line=dict(color='blue')))
    fig_trend.add_trace(go.Scatter(x=time_points, y=mtm_short_trend, mode='lines', name='Short Position MTM', line=dict(color='red')))
    fig_trend.update_layout(
        title='MTM Value Over Time for Long/Short Forward Position',
        xaxis_title='Time (Years)',
        yaxis_title='MTM Value ($)',
        hovermode='x unified'
    )
    fig_trend.add_hline(y=0, line_dash="dot", line_color="grey") 
    st.plotly_chart(fig_trend, use_container_width=True)

    # 2. Relationship Plot (MTM vs. Spot Price)
    st.markdown("#### MTM Value vs. Current Spot Price")
    st.markdown("This chart illustrates how the MTM value changes with varying current spot prices ($S_t$) at the selected current time ($t$).")

    st_range = np.linspace(max(0, St - S0*0.5), St + S0*0.5, 100) 
    mtm_long_relationship = []
    mtm_short_relationship = []
    
    for s_val in st_range:
        mtm_long_relationship.append(calculate_mtm_value(s_val, F0T, r, T, t, PVt_I, PVt_C, include_costs_benefits))
        mtm_short_relationship.append(-mtm_long_relationship[-1])

    fig_relationship = go.Figure()
    fig_relationship.add_trace(go.Scatter(x=st_range, y=mtm_long_relationship, mode='lines', name='Long Position MTM', line=dict(color='blue')))
    fig_relationship.add_trace(go.Scatter(x=st_range, y=mtm_short_relationship, mode='lines', name='Short Position MTM', line=dict(color='red')))
    
    # Highlight current St and MTM
    fig_relationship.add_trace(go.Scatter(
        x=[St], y=[VtT_long], mode='markers', name='Current St (Long)',
        marker=dict(size=10, color='blue', symbol='circle')
    ))
    fig_relationship.add_trace(go.Scatter(
        x=[St], y=[VtT_short], mode='markers', name='Current St (Short)',
        marker=dict(size=10, color='red', symbol='circle')
    ))

    fig_relationship.update_layout(
        title='MTM Value vs. Current Spot Price at time t',
        xaxis_title='Current Spot Price ($S_t$)',
        yaxis_title='MTM Value ($)',
        hovermode='x unified'
    )
    fig_relationship.add_hline(y=0, line_dash="dot", line_color="grey") 
    st.plotly_chart(fig_relationship, use_container_width=True)

    # 3. Aggregated Comparison (P&L at Maturity)
    st.markdown("#### Profit/Loss at Maturity ($P\&L_T$)")
    st.markdown("This bar chart visualizes the profit or loss realized at maturity ($T$) for various possible settlement spot prices ($S_T$) relative to the initial forward price ($F_0(T)$). At maturity, $t=T$, and $V_T(T) = S_T - F_0(T)$ for a long position (ignoring PVs as they expire).")

    st_maturity_scenarios = [F0T * 0.8, F0T * 0.9, F0T, F0T * 1.1, F0T * 1.2]
    scenario_labels = [f"0.8 * F0(T)", f"0.9 * F0(T)", f"F0(T)", f"1.1 * F0(T)", f"1.2 * F0(T)"]

    pnl_long_maturity = []
    pnl_short_maturity = []
    
    for s_t_maturity in st_maturity_scenarios:
        pnl_long = s_t_maturity - F0T
        pnl_long_maturity.append(pnl_long)
        pnl_short_maturity.append(-pnl_long)

    df_pnl = pd.DataFrame({
        'Settlement Spot Price Scenario ($S_T$)': scenario_labels,
        'Long Position P&L': pnl_long_maturity,
        'Short Position P&L': pnl_short_maturity
    })

    fig_pnl = go.Figure()

    if position_type == "Long":
        colors_long = ['red' if val < 0 else 'blue' for val in df_pnl['Long Position P&L']]
        fig_pnl.add_trace(go.Bar(
            x=df_pnl['Settlement Spot Price Scenario ($S_T$)'],
            y=df_pnl['Long Position P&L'],
            marker_color=colors_long,
            name='Long Position P&L'
        ))
    else: 
        colors_short = ['red' if val > 0 else 'blue' for val in df_pnl['Short Position P&L']]
        fig_pnl.add_trace(go.Bar(
            x=df_pnl['Settlement Spot Price Scenario ($S_T$)'],
            y=df_pnl['Short Position P&L'],
            marker_color=colors_short,
            name='Short Position P&L'
        ))

    fig_pnl.update_layout(
        title=f'Profit/Loss at Maturity for {position_type} Position',
        xaxis_title='Settlement Spot Price Scenario ($S_T$)',
        yaxis_title='Profit/Loss ($)',
        hovermode='x unified'
    )
    fig_pnl.add_hline(y=0, line_dash="dot", line_color="grey") 
    st.plotly_chart(fig_pnl, use_container_width=True)

