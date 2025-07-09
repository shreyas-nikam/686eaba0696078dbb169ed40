
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd

def run_page():
    st.header("Forward Contract Valuation Simulator")
    st.markdown("""
    This interactive tool allows you to explore the pricing and mark-to-market (MTM) valuation of forward contracts.
    Adjust the parameters in the sidebar to observe real-time changes in initial forward prices, current MTM values,
    and various visualizations.
    """)

    st.subheader("1. Input Parameters")

    # Contract Inception Parameters (for F_0(T) calculation)
    st.sidebar.subheader("Contract Inception Parameters")
    s0 = st.sidebar.number_input("Initial Spot Price ($S_0$)", min_value=50.0, max_value=200.0, value=100.0, step=1.0)
    r = st.sidebar.number_input("Risk-Free Rate ($r$)", min_value=0.01, max_value=0.10, value=0.05, step=0.001, format="%.3f")
    T = st.sidebar.number_input("Time to Maturity ($T$, in years)", min_value=0.25, max_value=5.0, value=1.0, step=0.25)

    include_costs_benefits = st.sidebar.checkbox("Include Costs/Benefits?", value=False)

    pv0_i = 0.0
    pv0_c = 0.0
    if include_costs_benefits:
        st.sidebar.markdown("---")
        st.sidebar.subheader("Initial Costs/Benefits (PV_0)")
        pv0_i = st.sidebar.number_input("Initial Present Value of Income ($PV_0(I)$)", min_value=0.0, max_value=20.0, value=0.0, step=0.1)
        pv0_c = st.sidebar.number_input("Initial Present Value of Costs ($PV_0(C)$)", min_value=0.0, max_value=20.0, value=0.0, step=0.1)

    # Current Valuation Parameters (for V_t(T) calculation and scenario analysis)
    st.sidebar.markdown("---")
    st.sidebar.subheader("Current Valuation Parameters")
    t = st.sidebar.slider("Current Time ($t$, in years)", min_value=0.0, max_value=float(T), value=0.0, step=0.01)
    
    # Ensure current spot price default is S0, and adjust its range dynamically
    s_t_min = max(0.0, s0 - 50)
    s_t_max = s0 + 50
    st_val_default = max(s_t_min, min(s_t_max, s0)) # Ensure default is within bounds
    st_val = st.sidebar.number_input("Current Spot Price ($S_t$)", min_value=s_t_min, max_value=s_t_max, value=st_val_default, step=1.0)

    pvt_i = 0.0
    pvt_c = 0.0
    if include_costs_benefits:
        st.sidebar.markdown("---")
        st.sidebar.subheader("Current Costs/Benefits (PV_t)")
        pvt_i = st.sidebar.number_input("Current Present Value of Income ($PV_t(I)$)", min_value=0.0, max_value=20.0, value=0.0, step=0.1)
        pvt_c = st.sidebar.number_input("Current Present Value of Costs ($PV_t(C)$)", min_value=0.0, max_value=20.0, value=0.0, step=0.1)

    position_type = st.sidebar.radio("Position Type", ["Long", "Short"])

    # --- Calculations ---
    def calculate_initial_forward_price(S0, r, T, PV0_I, PV0_C, include_costs_benefits):
        if include_costs_benefits:
            return (S0 - PV0_I + PV0_C) * (1 + r)**T
        else:
            return S0 * (1 + r)**T

    def calculate_mtm_value(St, F0_T, r, T, t, PVt_I, PVt_C, include_costs_benefits):
        discount_factor = (1 + r)**(-(T - t))
        if include_costs_benefits:
            # MTM for long position: (St - PVt_I + PVt_C) - F0_T * e^(-r(T-t))
            # Using (1+r)^-(T-t) for discrete compounding
            return (St - PVt_I + PVt_C) - F0_T * discount_factor
        else:
            return St - F0_T * discount_factor

    F0_T = calculate_initial_forward_price(s0, r, T, pv0_i, pv0_c, include_costs_benefits)
    Vt_T_long = calculate_mtm_value(st_val, F0_T, r, T, t, pvt_i, pvt_c, include_costs_benefits)
    Vt_T = Vt_T_long if position_type == "Long" else -Vt_T_long

    st.subheader("2. Calculated Values")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Initial Forward Price ($F_0(T)$)", value=f"{F0_T:,.2f}")
    with col2:
        st.metric(label=f"Current MTM Value ($V_t(T)$) for a {position_type} Position", value=f"{Vt_T:,.2f}")

    st.subheader("3. Valuation Formulas")
    st.markdown("The formulas displayed below show how the initial forward price and the mark-to-market value are calculated.")

    st.markdown("#### Initial Forward Price ($F_0(T)$)")
    if include_costs_benefits:
        st.latex(r"F_0(T) = (S_0 - PV_0(I) + PV_0(C)) (1+r)^T")
    else:
        st.latex(r"F_0(T) = S_0 (1+r)^T")

    st.markdown("#### Mark-to-Market (MTM) Value ($V_t(T)$) for a Long Position")
    if include_costs_benefits:
        st.latex(r"V_t(T) = (S_t - PV_t(I) + PV_t(C)) - F_0(T)(1+r)^{-(T-t)}")
    else:
        st.latex(r"V_t(T) = S_t - F_0(T)(1+r)^{-(T-t)}")
    st.markdown(r"For a short position, $V_t(T)$ is the negative of the long position's MTM value.")

    st.subheader("4. Visualizations")

    # --- Trend Plot: MTM Value Over Time ---
    st.markdown("### MTM Value Over Time")
    st.markdown("This plot shows how the Mark-to-Market value of the forward contract evolves from inception ($t=0$) to maturity ($t=T$).")

    time_points = np.linspace(0, T, 100)
    # Simple assumed spot price path for visualization: linearly moves from S0 to St_at_T
    # For a realistic trend, S_t can follow a drift-diffusion process, but for simplicity, we'll make it linear for now.
    # Let's assume S_t linearly moves from S0 to a value at T which could be around F0_T for simplicity of initial visual
    # Or, for demonstration, we can show multiple paths: constant S, linearly increasing S, linearly decreasing S.
    
    # For simplicity, let's use the current St for the current time t, and then project linearly.
    # To make it more illustrative, we can fix the *end* spot price for a few scenarios.
    
    # Scenario 1: Spot price remains constant at S0
    s_path_constant = np.full_like(time_points, s0)
    
    # Scenario 2: Spot price linearly increases from S0 to S0 + 20%
    s_path_increasing = np.linspace(s0, s0 * 1.2, 100)

    # Scenario 3: Spot price linearly decreases from S0 to S0 - 20%
    s_path_decreasing = np.linspace(s0, s0 * 0.8, 100)

    mtm_long_constant = [calculate_mtm_value(s, F0_T, r, T, t_val, pv0_i, pv0_c, include_costs_benefits) for s, t_val in zip(s_path_constant, time_points)]
    mtm_long_increasing = [calculate_mtm_value(s, F0_T, r, T, t_val, pv0_i, pv0_c, include_costs_benefits) for s, t_val in zip(s_path_increasing, time_points)]
    mtm_long_decreasing = [calculate_mtm_value(s, F0_T, r, T, t_val, pv0_i, pv0_c, include_costs_benefits) for s, t_val in zip(s_path_decreasing, time_points)]

    fig_trend = go.Figure()

    fig_trend.add_trace(go.Scatter(x=time_points, y=mtm_long_constant if position_type == "Long" else [-x for x in mtm_long_constant],
                                   mode='lines', name='Spot Constant', line=dict(color='blue')))
    fig_trend.add_trace(go.Scatter(x=time_points, y=mtm_long_increasing if position_type == "Long" else [-x for x in mtm_long_increasing],
                                   mode='lines', name='Spot Increasing', line=dict(color='green')))
    fig_trend.add_trace(go.Scatter(x=time_points, y=mtm_long_decreasing if position_type == "Long" else [-x for x in mtm_long_decreasing],
                                   mode='lines', name='Spot Decreasing', line=dict(color='red')))

    # Highlight current time and MTM
    current_mtm_val_for_plot = calculate_mtm_value(st_val, F0_T, r, T, t, pvt_i, pvt_c, include_costs_benefits)
    if position_type == "Short":
        current_mtm_val_for_plot = -current_mtm_val_for_plot

    fig_trend.add_trace(go.Scatter(x=[t], y=[current_mtm_val_for_plot],
                                   mode='markers',
                                   marker=dict(size=10, color='orange', symbol='star'),
                                   name=f'Current (t={t:.2f}, MTM={current_mtm_val_for_plot:.2f})',
                                   hoverinfo='text',
                                   text=f'Time: {t:.2f}<br>Spot: {st_val:.2f}<br>MTM: {current_mtm_val_for_plot:.2f}'))


    fig_trend.update_layout(title=f'MTM Value Over Time for a {position_type} Forward Position',
                            xaxis_title='Time (Years)',
                            yaxis_title='MTM Value ($)',
                            hovermode='x unified',
                            template='plotly_dark')
    st.plotly_chart(fig_trend, use_container_width=True)

    # --- Relationship Plot: MTM Value vs. Current Spot Price ---
    st.markdown("### MTM Value vs. Current Spot Price")
    st.markdown(f"This plot shows the sensitivity of the Mark-to-Market value ($V_t(T)$) to changes in the current spot price ($S_t$) at fixed time $t={t:.2f}$.")

    # Generate a range of St values around the current St
    st_range = np.linspace(st_val * 0.5, st_val * 1.5, 100) # From 50% to 150% of current St
    mtm_values_relationship_long = [calculate_mtm_value(s, F0_T, r, T, t, pvt_i, pvt_c, include_costs_benefits) for s in st_range]
    
    if position_type == "Short":
        mtm_values_relationship = [-val for val in mtm_values_relationship_long]
    else:
        mtm_values_relationship = mtm_values_relationship_long

    fig_relationship = go.Figure()
    fig_relationship.add_trace(go.Scatter(x=st_range, y=mtm_values_relationship,
                                         mode='lines', name=f'{position_type} Position MTM',
                                         line=dict(color='purple')))

    # Highlight current St and corresponding MTM
    fig_relationship.add_trace(go.Scatter(x=[st_val], y=[Vt_T],
                                         mode='markers',
                                         marker=dict(size=10, color='orange', symbol='star'),
                                         name=f'Current (S_t={st_val:.2f}, MTM={Vt_T:.2f})',
                                         hoverinfo='text',
                                         text=f'Spot Price: {st_val:.2f}<br>MTM: {Vt_T:.2f}'))

    fig_relationship.update_layout(title=f'MTM Value vs. Spot Price ($S_t$) at t={t:.2f} for a {position_type} Position',
                                   xaxis_title='Current Spot Price ($S_t$)',
                                   yaxis_title='MTM Value ($V_t(T)$)',
                                   hovermode='x unified',
                                   template='plotly_dark')
    st.plotly_chart(fig_relationship, use_container_width=True)

    # --- Aggregated Comparison: Profit/Loss at Maturity ---
    st.markdown("### Profit/Loss at Maturity")
    st.markdown(f"This bar chart visualizes the potential Profit/Loss at maturity ($T={T:.2f}$) for various settlement spot price ($S_T$) scenarios relative to the initial forward price $F_0(T)={F0_T:.2f}$.")

    # Define several ST scenarios around F0_T
    st_scenarios = [F0_T * 0.8, F0_T * 0.9, F0_T * 0.95, F0_T, F0_T * 1.05, F0_T * 1.1, F0_T * 1.2]
    pnl_at_maturity = []

    for s_T_scenario in st_scenarios:
        # At maturity (t=T), PV(I) and PV(C) would typically be 0 unless specific to settlement.
        # For simplicity of P&L at maturity: S_T - F_0(T) for long, F_0(T) - S_T for short
        # Or more accurately, V_T(T) = S_T - F_0(T) if no further costs/benefits apply post-settlement.
        # Assuming P&L at maturity is simply S_T - F_0(T) (or inverse for short)
        pnl = (s_T_scenario - F0_T)
        if position_type == "Short":
            pnl = -pnl
        pnl_at_maturity.append(pnl)

    df_pnl = pd.DataFrame({
        'Settlement Spot Price ($S_T$)': [f"{s:.2f}" for s in st_scenarios],
        'Profit/Loss at Maturity ($P&L_T$)': pnl_at_maturity,
        'Outcome': ['Profit' if p > 0 else ('Loss' if p < 0 else 'Break-even') for p in pnl_at_maturity]
    })

    fig_pnl = go.Figure(data=[go.Bar(
        x=df_pnl['Settlement Spot Price ($S_T$)'],
        y=df_pnl['Profit/Loss at Maturity ($P&L_T$)'],
        marker_color=df_pnl['Profit/Loss at Maturity ($P&L_T$)'].apply(lambda x: 'green' if x > 0 else 'red' if x < 0 else 'blue'),
        hoverinfo='text',
        text=[f"S_T: {st_scenarios[i]:.2f}<br>P&L: {pnl_at_maturity[i]:.2f}" for i in range(len(st_scenarios))]
    )])

    fig_pnl.update_layout(title=f'Profit/Loss at Maturity for a {position_type} Forward Position',
                          xaxis_title='Settlement Spot Price ($S_T$)',
                          yaxis_title='Profit/Loss at Maturity ($P&L_T$)',
                          template='plotly_dark')
    st.plotly_chart(fig_pnl, use_container_width=True)

    st.markdown("""
    ---
    **Explanation of P&L at Maturity:**
    *   **Long Position:** Profits when $S_T > F_0(T)$ (spot price at maturity is higher than the agreed forward price). Losses when $S_T < F_0(T)$.
    *   **Short Position:** Profits when $S_T < F_0(T)$ (spot price at maturity is lower than the agreed forward price). Losses when $S_T > F_0(T)$.
    *   **Break-even:** Occurs when $S_T = F_0(T)$, resulting in zero profit or loss.
    """)
