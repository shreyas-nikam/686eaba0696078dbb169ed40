id: 686eaba0696078dbb169ed40_documentation
summary: Derivative Pricing and Valuation of Forward  Contracts and for an Underlying  with Varying Maturities Documentation
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# QuLab: Understanding Forward Contracts with Costs & Benefits

## Introduction to Forward Contracts and Their Valuation
Duration: 0:10:00

Welcome to the **QuLab: Forward Contracts with Costs & Benefits Simulator** codelab! In this lab, we will delve into the fascinating world of financial derivatives, specifically focusing on **Forward Contracts**. This application provides a hands-on experience to understand how discrete costs (like storage fees) and benefits (like dividends) affect the pricing and Mark-to-Market (MTM) valuation of these contracts.

Understanding forward contracts is crucial for anyone involved in finance, risk management, or quantitative analysis. They are foundational instruments used for hedging, speculation, and arbitrage in various markets, from commodities to foreign exchange and equities.

### Why is this important?
The ability to accurately price and value forward contracts is fundamental for:
*   **Risk Management:** Companies use forward contracts to lock in prices for future transactions, thereby hedging against adverse price movements.
*   **Investment Decisions:** Investors use forwards to take positions on future price movements of assets.
*   **Arbitrage Opportunities:** Identifying mispriced forwards can lead to risk-free profits if the no-arbitrage principle is violated.

### Core Concepts Explained

This application is built upon the **No-Arbitrage Principle**, a cornerstone of financial economics. This principle posits that in an efficient market, it's impossible to generate risk-free profits. Therefore, the price of a derivative must reflect the cost of replicating its payoff using the underlying asset and risk-free borrowing/lending.

We will focus on two key valuation concepts:

1.  **Forward Price at Inception ($F_0(T)$):** This is the price agreed upon today ($t=0$) for the asset to be bought or sold at a future maturity date $T$. When the underlying asset generates intermediate cash flows (benefits like dividends or costs like storage), these must be incorporated into the forward price. The formula used in this application is:
    $$F_0(T) = (S_0 - PV_0(I) + PV_0(C))(1 + r)^T$$
    Where:
    *   $S_0$: Initial spot price of the underlying asset at time $t=0$.
    *   $PV_0(I)$: Present Value of all discrete benefits (Income/Dividends) received from time $t=0$ to maturity $T$.
        $$PV_0(I) = \sum_{j} I_j (1 + r)^{-t_j^I}$$
        Here, $I_j$ is the amount of the $j$-th benefit, and $t_j^I$ is the time (in years from $t=0$) when the $j$-th benefit is received.
    *   $PV_0(C)$: Present Value of all discrete costs incurred from time $t=0$ to maturity $T$.
        $$PV_0(C) = \sum_{k} C_k (1 + r)^{-t_k^C}$$
        Here, $C_k$ is the amount of the $k$-th cost, and $t_k^C$ is the time (in years from $t=0$) when the $k$-th cost is incurred.
    *   $r$: Annualized risk-free interest rate.
    *   $T$: Total time to maturity of the forward contract in years from $t=0$.

2.  **Mark-to-Market (MTM) Value ($V_t(T)$):** This represents the current value of the forward contract at any point in time $t$ before maturity. It's the profit or loss you would realize if you closed out your position at the current market conditions.

    For a **long position** (agreement to buy), the MTM value at time $t$ is:
    $$V_t(T) = (S_t - PV_t(I) + PV_t(C)) - F_0(T)(1 + r)^{-(T-t)}$$
    Where:
    *   $S_t$: Spot price of the underlying asset at the current time $t$.
    *   $PV_t(I)$: Present Value of *remaining* discrete benefits from time $t$ to maturity $T$.
    *   $PV_t(C)$: Present Value of *remaining* discrete costs from time $t$ to maturity $T$.
    *   $F_0(T)$: The original forward price agreed upon at $t=0$.
    *   $(1 + r)^{-(T-t)}$: Discount factor for the remaining life of the contract $(T-t)$.

    The present value of *remaining* cash flows from time $t$ to maturity $T$ is calculated as:
    $$PV_t(CF) = \sum_{j | t_j^{CF} \ge t} CF_j (1 + r)^{-(t_j^{CF} - t)}$$
    Here, $CF_j$ is the amount of the $j$-th cash flow (either $I_j$ or $C_k$), and $t_j^{CF}$ is its original time from $t=0$. Only cash flows occurring at or after the current time $t$ are considered.

    For a **short position** (agreement to sell), the MTM value is simply the negative of the long position's MTM value:
    $$V_t(T)_{short} = -V_t(T)_{long}$$

This application brings these theoretical concepts to life, allowing you to interactively adjust parameters and visualize their impact in real-time.

## Application Architecture Overview
Duration: 0:03:00

The Streamlit application is structured into two main Python files: `app.py` and `application_pages/forward_contracts_simulator.py`. This modular design helps keep the main application logic separate from the specific page implementation, making the application scalable for multiple features.

Here's a high-level overview of how the files interact:

```
app.py
  ├── Sets global Streamlit page configuration (title, layout)
  ├── Displays main title and the introductory markdown content (including formulas)
  ├── Manages sidebar navigation (though currently only one page is available)
  └── Dynamically loads and runs the selected page's logic
        |
        V
application_pages/forward_contracts_simulator.py
  ├── Contains all core financial calculation logic (helper functions)
  ├── Defines the Streamlit UI elements for inputs and outputs
  ├── Performs input validation
  └── Renders calculated metrics and interactive Plotly visualizations
```

*   `app.py`: This is the entry point of the Streamlit application. It handles the overall setup, displays the main introductory text about forward contracts and their formulas, and acts as a dispatcher for different "pages" of the application.
*   `application_pages/forward_contracts_simulator.py`: This file contains the complete logic for the forward contracts simulator. It encapsulates the helper functions for financial calculations, defines the input widgets, processes user inputs, performs calculations, and generates the interactive charts.

## Setting Up Your Environment
Duration: 0:05:00

To run this Streamlit application, you'll need Python installed on your system along with a few libraries.

### Prerequisites

*   Python 3.7+

### Installation Steps

1.  **Create a Project Directory:**
    Start by creating a dedicated folder for your project.
    ```console
    mkdir qu_forward_contracts
    cd qu_forward_contracts
    ```

2.  **Create `application_pages` Directory:**
    Inside your main project directory, create a sub-directory named `application_pages`.
    ```console
    mkdir application_pages
    ```

3.  **Install Required Libraries:**
    Open your terminal or command prompt and install the necessary Python packages using pip:
    ```console
    pip install streamlit pandas numpy plotly
    ```
    <aside class="positive">
    It's a good practice to use a virtual environment to manage dependencies for your projects. You can create one using `python -m venv venv` and activate it with `source venv/bin/activate` (Linux/macOS) or `.\venv\Scripts\activate` (Windows PowerShell).
    </aside>

4.  **Save the Application Code:**
    Create two Python files (`app.py` and `forward_contracts_simulator.py`) and paste the respective code into them.

    *   **`app.py`**: Save this file directly in your `qu_forward_contracts` directory.
        ```python
        import streamlit as st
        import json
        import pandas as pd
        import numpy as np
        import plotly.express as px
        import plotly.graph_objects as go

        st.set_page_config(page_title="QuLab: Forward Contracts Valuation", layout="wide")
        st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
        st.sidebar.divider()
        st.title("QuLab: Forward Contracts with Costs & Benefits Simulator")
        st.divider()
        st.markdown(r"""
        In this lab, we explore the intricate world of **Forward Contracts**, focusing specifically on how **discrete costs (like storage) and benefits (like dividends)** impact their pricing and valuation. A forward contract is a customized contract between two parties to buy or sell an asset at a specified price on a future date. Unlike futures, forward contracts are over-the-counter (OTC) instruments, meaning they are not traded on exchanges and are subject to counterparty risk.

        ### Core Concepts:

        1.  **No-Arbitrage Principle:** The fundamental concept guiding the pricing of derivatives. It states that in an efficient market, it's impossible to make risk-free profit by simultaneously buying and selling different assets. This principle dictates that the forward price must reflect the cost of holding the underlying asset until maturity, including any costs incurred or benefits received.

        2.  **Forward Price at Inception ($F_0(T)$):** This is the price agreed upon today for a transaction that will occur at a future date $T$. When the underlying asset generates benefits (e.g., dividends, convenience yield) or incurs costs (e.g., storage, insurance) during the contract's life, these cash flows must be accounted for.
            The formula for the forward price at inception, considering discrete costs and benefits, is:
            $$F_0(T) = (S_0 - PV_0(I) + PV_0(C))(1 + r)^T$$
            Where:
            *   $S_0$: Initial spot price of the underlying asset at time $t=0$.
            *   $PV_0(I)$: Present Value of all discrete benefits (Income/Dividends) received from time $t=0$ to maturity $T$.
                $$PV_0(I) = \sum_{j} I_j (1 + r)^{-t_j^I}$$
                Here, $I_j$ is the amount of the $j$-th benefit, and $t_j^I$ is the time (in years from $t=0$) when the $j$-th benefit is received.
            *   $PV_0(C)$: Present Value of all discrete costs incurred from time $t=0$ to maturity $T$.
                $$PV_0(C) = \sum_{k} C_k (1 + r)^{-t_k^C}$$
                Here, $C_k$ is the amount of the $k$-th cost, and $t_k^C$ is the time (in years from $t=0$) when the $k$-th cost is incurred.
            *   $r$: Annualized risk-free interest rate.
            *   $T$: Total time to maturity of the forward contract in years from $t=0$.

        3.  **Mark-to-Market (MTM) Value ($V_t(T)$):** This is the value of the forward contract at any point in time $t$ before maturity. It represents the profit or loss that would be realized if the contract were to be closed out (marked to market) at the current time $t$. The MTM value changes as the spot price of the underlying asset, interest rates, and time to maturity change.

            For a **long position** (agreement to buy), the MTM value at time $t$ is:
            $$V_t(T) = (S_t - PV_t(I) + PV_t(C)) - F_0(T)(1 + r)^{-(T-t)}$$
            Where:
            *   $S_t$: Spot price of the underlying asset at the current time $t$.
            *   $PV_t(I)$: Present Value of *remaining* discrete benefits from time $t$ to maturity $T$.
            *   $PV_t(C)$: Present Value of *remaining* discrete costs from time $t$ to maturity $T$.
            *   $F_0(T)$: The original forward price agreed upon at $t=0$.
            *   $(1 + r)^{-(T-t)}$: Discount factor for the remaining life of the contract $(T-t)$.

            The present value of *remaining* cash flows from time $t$ to maturity $T$ is calculated as:
            $$PV_t(CF) = \sum_{j | t_j^{CF} \ge t} CF_j (1 + r)^{-(t_j^{CF} - t)}$$
            Here, $CF_j$ is the amount of the $j$-th cash flow (either $I_j$ or $C_k$), and $t_j^{CF}$ is its original time from $t=0$. Only cash flows occurring at or after the current time $t$ are considered.

            For a **short position** (agreement to sell), the MTM value is simply the negative of the long position's MTM value:
            $$V_t(T)_{short} = -V_t(T)_{long}$$

        This application allows you to interactively adjust all these parameters and visualize their impact on the forward price and MTM value in real-time.
        """)

        st.divider()

        # Placeholder for navigation, though we have only one page
        page = st.sidebar.selectbox(label="Navigation", options=["Forward Contracts Simulator"])

        if page == "Forward Contracts Simulator":
            from application_pages.forward_contracts_simulator import run_page
            run_page()

        st.divider()
        st.write("© 2025 QuantUniversity. All Rights Reserved.")
        st.caption("The purpose of this demonstration is solely for educational use and illustration. "
                   "Any reproduction of this demonstration "
                   "requires prior written consent from QuantUniversity. "
                   "This lab was generated using the QuCreate platform. QuCreate relies on AI models for generating code, which may contain inaccuracies or errors.")
        ```

    *   **`application_pages/forward_contracts_simulator.py`**: Save this file inside the `application_pages` directory you created.
        ```python
        import streamlit as st
        import json
        import pandas as pd
        import numpy as np
        import plotly.express as px
        import plotly.graph_objects as go

        # Helper Functions
        def parse_cash_flows(json_str):
            try:
                if not json_str.strip():
                    return []
                data = json.loads(json_str)
                if not isinstance(data, list):
                    st.error("Cash flow input must be a JSON list of objects.")
                    return []
                for item in data:
                    if not isinstance(item, dict) or "amount" not in item or "time_from_t0" not in item:
                        st.error("Each cash flow object must have 'amount' and 'time_from_t0' keys.")
                        return []
                    if not isinstance(item["amount"], (int, float)) or not isinstance(item["time_from_t0"], (int, float)):
                        st.error("Cash flow 'amount' and 'time_from_t0' must be numbers.")
                        return []
                    if item["time_from_t0"] < 0:
                        st.error("Cash flow 'time_from_t0' cannot be negative.")
                        return []
                return data
            except json.JSONDecodeError:
                st.error("Invalid JSON format for cash flows. Please check your syntax.")
                return []
            except Exception as e:
                st.error(f"An unexpected error occurred parsing cash flows: {e}")
                return []

        def calculate_present_value(cash_flows, rate, current_time, maturity):
            pv = 0.0
            for cf in cash_flows:
                amount = cf["amount"]
                time_from_t0 = cf["time_from_t0"]
                if time_from_t0 >= current_time and time_from_t0 <= maturity:
                    discount_period = time_from_t0 - current_time
                    if discount_period < 0: # Should not happen with t_j_CF >= t check, but good for robustness
                        continue
                    pv += amount / (1 + rate)**discount_period
            return pv

        def calculate_forward_price_at_inception(S0, T, r, dividends, costs):
            pv_dividends_at_0 = calculate_present_value(dividends, r, 0, T)
            pv_costs_at_0 = calculate_present_value(costs, r, 0, T)
            F0_T = (S0 - pv_dividends_at_0 + pv_costs_at_0) * (1 + r)**T
            return F0_T

        def calculate_mtm_value(St, T, t_current, r, F0_T, dividends, costs):
            pv_remaining_dividends = calculate_present_value(dividends, r, t_current, T)
            pv_remaining_costs = calculate_present_value(costs, r, t_current, T)
            
            # Ensure remaining_time_to_maturity is non-negative
            remaining_time_to_maturity = max(0, T - t_current)
            
            Vt_T_long = (St - pv_remaining_dividends + pv_remaining_costs) - F0_T * (1 + r)**(-remaining_time_to_maturity)
            return Vt_T_long

        def run_page():
            st.header("Forward Contracts with Costs & Benefits Simulator")

            # Layout using columns for input widgets
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Core Contract Parameters")
                S0 = st.number_input(
                    "Initial Spot Price ($S_0$):",
                    min_value=0.01, value=100.0, step=0.1,
                    help="The current market price of the underlying asset at t=0."
                )
                T = st.number_input(
                    "Maturity ($T$):",
                    min_value=0.1, value=1.0, step=0.1,
                    help="Total time to maturity of the forward contract in years from t=0."
                )
                r = st.number_input(
                    "Risk-Free Rate ($r$):",
                    min_value=0.001, value=0.05, step=0.001, format="%.3f",
                    help="The annualized risk-free interest rate (e.g., enter 0.05 for 5%)."
                )

            with col2:
                st.subheader("Current Valuation Parameters")
                t_current = st.number_input(
                    "Current Time ($t$):",
                    min_value=0.0, value=0.5, step=0.01,
                    help="The current point in time for MTM valuation ($0 \\le t \\le T$).",
                    key="current_time_t"
                )
                St = st.number_input(
                    "Current Spot Price ($S_t$):",
                    min_value=0.01, value=102.0, step=0.1,
                    help="The spot price of the underlying asset at the current time t."
                )

            st.subheader("Cash Flow Specification")
            col_cf1, col_cf2 = st.columns(2)
            with col_cf1:
                dividends_json = st.text_area(
                    "Dividends (Benefits) [JSON]:",
                    value='[{"amount": 2.0, "time_from_t0": 0.25}, {"amount": 2.5, "time_from_t0": 0.75}]',
                    height=100,
                    help="Enter discrete dividends as a JSON list of objects. Each object needs 'amount' (float) and 'time_from_t0' (float, in years from t=0). Example: `[{\"amount\": 10.0, \"time_from_t0\": 0.5}]`."
                )
            with col_cf2:
                costs_json = st.text_area(
                    "Costs [JSON]:",
                    value='[{"amount": 1.0, "time_from_t0": 0.5}]',
                    height=100,
                    help="Enter discrete costs (e.g., storage) as a JSON list of objects. Each object needs 'amount' (float) and 'time_from_t0' (float, in years from t=0). Example: `[{\"amount\": 5.0, \"time_from_t0\": 0.75}]`."
                )

            position_type = st.radio(
                "Position Type for MTM Valuation:",
                ('long', 'short'),
                help="Select the position type for MTM valuation."
            )

            st.divider()

            # Input Validation
            if t_current > T:
                st.error("Error: Current Time (t) cannot be greater than Maturity (T). Please adjust the inputs.")
                st.stop()
            if S0 <= 0 or St <= 0:
                st.error("Error: Spot prices ($S_0$, $S_t$) must be positive.")
                st.stop()
            if r < 0:
                st.error("Error: Risk-Free Rate ($r$) cannot be negative.")
                st.stop()


            # Parse cash flows
            dividends = parse_cash_flows(dividends_json)
            costs = parse_cash_flows(costs_json)

            if not dividends and dividends_json.strip():
                st.warning("Could not parse dividends JSON. Using empty list.")
            if not costs and costs_json.strip():
                st.warning("Could not parse costs JSON. Using empty list.")

            # Calculations
            F0_T_with_cb = calculate_forward_price_at_inception(S0, T, r, dividends, costs)
            F0_T_without_cb = calculate_forward_price_at_inception(S0, T, r, [], []) # For comparison

            Vt_T_long = calculate_mtm_value(St, T, t_current, r, F0_T_with_cb, dividends, costs)
            Vt_T_short = -Vt_T_long if position_type == 'short' else Vt_T_long # MTM for short position

            st.subheader("Calculated Outputs")
            col_metrics1, col_metrics2 = st.columns(2)
            with col_metrics1:
                st.metric(label="Forward Price at Inception ($F_0(T)$) (with C/B)", value=f"{F0_T_with_cb:,.2f}")
            with col_metrics2:
                st.metric(label="Forward Price at Inception ($F_0(T)$) (without C/B)", value=f"{F0_T_without_cb:,.2f}")

            mtm_label = f"MTM Value at Current Time ($V_t(T)$) ({position_type.capitalize()} Position)"
            st.metric(label=mtm_label, value=f"{Vt_T_short:,.2f}") # Use Vt_T_short which is already adjusted for position_type

            st.divider()

            st.subheader("Visualizations")

            #  1. MTM Value Evolution Over Time (Long Position) 
            st.markdown("#### MTM Value Evolution Over Time (Long Position)")
            num_points = 100
            time_points = np.linspace(0, T, num_points)
            mtm_values_with_cb = []
            mtm_values_without_cb = []

            # Original F0_T (needed for comparison)
            original_F0_T_with_cb = calculate_forward_price_at_inception(S0, T, r, dividends, costs)
            original_F0_T_without_cb = calculate_forward_price_at_inception(S0, T, r, [], [])

            # Simulating spot price for MTM evolution plot
            # A simple linear interpolation for S_t_plot from S0 to a reasonable end price (e.g., F0_T_with_cb)
            S_T_plot_end_value = F0_T_with_cb 
            S_t_for_plot = np.linspace(S0, S_T_plot_end_value, num_points)

            for i, t_val in enumerate(time_points):
                current_S_t_for_plot = S_t_for_plot[i]
                
                mtm_val_with = calculate_mtm_value(current_S_t_for_plot, T, t_val, r, F0_T_with_cb, dividends, costs)
                mtm_values_with_cb.append(mtm_val_with)
                
                mtm_val_without = calculate_mtm_value(current_S_t_for_plot, T, t_val, r, F0_T_without_cb, [], [])
                mtm_values_without_cb.append(mtm_val_without)

            df_mtm_evolution = pd.DataFrame({
                'Time (Years)': time_points,
                'MTM Value (with C/B)': mtm_values_with_cb,
                'MTM Value (without C/B)': mtm_values_without_cb
            })

            fig_mtm_evolution = go.Figure()
            fig_mtm_evolution.add_trace(go.Scatter(x=df_mtm_evolution['Time (Years)'], y=df_mtm_evolution['MTM Value (with C/B)'],
                                                   mode='lines', name='MTM Value (with C/B)'))
            fig_mtm_evolution.add_trace(go.Scatter(x=df_mtm_evolution['Time (Years)'], y=df_mtm_evolution['MTM Value (without C/B)'],
                                                   mode='lines', name='MTM Value (without C/B)'))

            # Add vertical line for current time
            fig_mtm_evolution.add_vline(x=t_current, line_dash="dash", line_color="grey", annotation_text=f"Current Time (t={t_current:.2f})")
            # Add horizontal line for Y=0
            fig_mtm_evolution.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Break-even (Y=0)")

            fig_mtm_evolution.update_layout(
                title='MTM Value Evolution Over Time (Long Position)',
                xaxis_title='Time (Years)',
                yaxis_title='MTM Value',
                hovermode="x unified",
                legend_title_text='Scenario'
            )
            st.plotly_chart(fig_mtm_evolution, use_container_width=True)

            #  2. Sensitivity of Forward Price to Costs/Benefits Magnitude 
            st.markdown("#### Sensitivity of Forward Price to Costs/Benefits Magnitude")
            multipliers = np.linspace(0, 2, 21) # From 0x to 2x original amount

            f0_sensitivity_costs = []
            f0_sensitivity_dividends = []

            # Original PV of costs/benefits
            original_pv_costs = calculate_present_value(costs, r, 0, T)
            original_pv_dividends = calculate_present_value(dividends, r, 0, T)

            for mult in multipliers:
                # Sensitivity to Costs
                temp_costs_for_sensitivity = [{"amount": cf["amount"] * mult, "time_from_t0": cf["time_from_t0"]} for cf in costs]
                f0_costs = calculate_forward_price_at_inception(S0, T, r, dividends, temp_costs_for_sensitivity)
                f0_sensitivity_costs.append(f0_costs)

                # Sensitivity to Dividends
                temp_dividends_for_sensitivity = [{"amount": cf["amount"] * mult, "time_from_t0": cf["time_from_t0"]} for cf in dividends]
                f0_dividends = calculate_forward_price_at_inception(S0, T, r, temp_dividends_for_sensitivity, costs)
                f0_sensitivity_dividends.append(f0_dividends)

            df_sensitivity = pd.DataFrame({
                'Multiplier': multipliers,
                'Forward Price (Costs Multiplied)': f0_sensitivity_costs,
                'Forward Price (Dividends Multiplied)': f0_sensitivity_dividends
            })

            fig_sensitivity = go.Figure()
            fig_sensitivity.add_trace(go.Scatter(x=df_sensitivity['Multiplier'], y=df_sensitivity['Forward Price (Costs Multiplied)'],
                                                mode='lines', name='F0(T) vs. Costs Multiplier'))
            fig_sensitivity.add_trace(go.Scatter(x=df_sensitivity['Multiplier'], y=df_sensitivity['Forward Price (Dividends Multiplied)'],
                                                mode='lines', name='F0(T) vs. Dividends Multiplier'))

            fig_sensitivity.update_layout(
                title='Sensitivity of Forward Price to Costs/Benefits Magnitude',
                xaxis_title='Multiplier of Original Costs/Benefits',
                yaxis_title='Forward Price ($F_0(T)$)',
                hovermode="x unified",
                legend_title_text='Factor'
            )
            st.plotly_chart(fig_sensitivity, use_container_width=True)

            #  3. Aggregated Comparison Plot (MTM Value Across Scenarios) 
            st.markdown("#### MTM Value Comparison Across Scenarios (Long Position)")

            # Define scenarios
            scenarios = {
                'Base Case (with C/B)': {
                    'dividends': dividends,
                    'costs': costs
                },
                'No Costs/Benefits': {
                    'dividends': [],
                    'costs': []
                },
                'Double Dividends': {
                    'dividends': [{"amount": cf["amount"] * 2, "time_from_t0": cf["time_from_t0"]} for cf in dividends],
                    'costs': costs
                },
                'Double Costs': {
                    'dividends': dividends,
                    'costs': [{"amount": cf["amount"] * 2, "time_from_t0": cf["time_from_t0"]} for cf in costs]
                }
            }

            scenario_mtm_values = []
            scenario_names = []

            for name, params in scenarios.items():
                # Need to recalculate F0_T for each scenario based on *its* cash flows
                # Then calculate MTM using that F0_T.
                
                scenario_F0_T = calculate_forward_price_at_inception(S0, T, r, params['dividends'], params['costs'])
                mtm_val = calculate_mtm_value(St, T, t_current, r, scenario_F0_T, params['dividends'], params['costs'])
                
                # If the displayed MTM is for the selected position_type, apply it here
                if position_type == 'short':
                    mtm_val = -mtm_val
                    
                scenario_mtm_values.append(mtm_val)
                scenario_names.append(name)

            df_scenario_comparison = pd.DataFrame({
                'Scenario': scenario_names,
                'MTM Value': scenario_mtm_values
            })

            fig_scenario_comparison = px.bar(
                df_scenario_comparison,
                x='Scenario',
                y='MTM Value',
                title=f'MTM Value Comparison Across Scenarios ({position_type.capitalize()} Position)',
                labels={'MTM Value': 'MTM Value ($)'},
                text='MTM Value'
            )
            fig_scenario_comparison.update_traces(texttemplate='%{text:,.2f}', textposition='outside')
            fig_scenario_comparison.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_scenario_comparison, use_container_width=True)
        ```
    <aside class="positive">
    Ensure that the `app.py` and `application_pages/forward_contracts_simulator.py` files are placed in their correct relative paths for the application to run successfully.
    </aside>

## Understanding the Core Logic: Helper Functions
Duration: 0:15:00

The heavy lifting of financial calculations happens within the helper functions defined in `application_pages/forward_contracts_simulator.py`. These functions implement the core valuation formulas discussed earlier.

### `parse_cash_flows(json_str)`

```python
def parse_cash_flows(json_str):
    try:
        if not json_str.strip():
            return []
        data = json.loads(json_str)
        if not isinstance(data, list):
            st.error("Cash flow input must be a JSON list of objects.")
            return []
        for item in data:
            if not isinstance(item, dict) or "amount" not in item or "time_from_t0" not in item:
                st.error("Each cash flow object must have 'amount' and 'time_from_t0' keys.")
                return []
            if not isinstance(item["amount"], (int, float)) or not isinstance(item["time_from_t0"], (int, float)):
                st.error("Cash flow 'amount' and 'time_from_t0' must be numbers.")
                return []
            if item["time_from_t0"] < 0:
                st.error("Cash flow 'time_from_t0' cannot be negative.")
                return []
        return data
    except json.JSONDecodeError:
        st.error("Invalid JSON format for cash flows. Please check your syntax.")
        return []
    except Exception as e:
        st.error(f"An unexpected error occurred parsing cash flows: {e}")
        return []
```
*   **Purpose:** This function is crucial for handling user input for discrete dividends and costs. It takes a JSON string as input, which is the standard format for representing structured data in web applications.
*   **Functionality:**
    *   It checks if the input string is empty; if so, it returns an empty list.
    *   It attempts to parse the JSON string into a Python list of dictionaries.
    *   It performs robust validation to ensure:
        *   The parsed data is a list.
        *   Each item in the list is a dictionary.
        *   Each dictionary contains `amount` and `time_from_t0` keys.
        *   The values for `amount` and `time_from_t0` are numbers (integers or floats).
        *   `time_from_t0` is not negative.
    *   It uses `st.error` to display user-friendly error messages directly in the Streamlit app if validation fails.
*   **Importance:** This ensures that the financial calculation functions receive clean, correctly formatted data, preventing runtime errors.

### `calculate_present_value(cash_flows, rate, current_time, maturity)`

```python
def calculate_present_value(cash_flows, rate, current_time, maturity):
    pv = 0.0
    for cf in cash_flows:
        amount = cf["amount"]
        time_from_t0 = cf["time_from_t0"]
        if time_from_t0 >= current_time and time_from_t0 <= maturity:
            discount_period = time_from_t0 - current_time
            if discount_period < 0: # Should not happen with t_j_CF >= t check, but good for robustness
                continue
            pv += amount / (1 + rate)**discount_period
    return pv
```
*   **Purpose:** Calculates the present value of a list of discrete cash flows. This function is generalized to handle both initial PV calculations (where `current_time` is 0) and remaining PV calculations for MTM (where `current_time` is `t`).
*   **Functionality:**
    *   It iterates through each cash flow (`cf`) in the provided `cash_flows` list.
    *   For each cash flow, it checks if `time_from_t0` (the time the cash flow occurs relative to `t=0`) falls within the relevant period (from `current_time` to `maturity`). This is critical for MTM calculations, where only *remaining* cash flows are considered.
    *   It calculates the `discount_period` as the difference between the cash flow's occurrence time and the `current_time`.
    *   It discounts the cash `amount` back to the `current_time` using the simple discrete compounding formula: $PV = CF / (1 + r)^{\text{discount\_period}}$.
*   **Mathematical Concept:** This function directly implements the present value formula for discrete cash flows.

### `calculate_forward_price_at_inception(S0, T, r, dividends, costs)`

```python
def calculate_forward_price_at_inception(S0, T, r, dividends, costs):
    pv_dividends_at_0 = calculate_present_value(dividends, r, 0, T)
    pv_costs_at_0 = calculate_present_value(costs, r, 0, T)
    F0_T = (S0 - pv_dividends_at_0 + pv_costs_at_0) * (1 + r)**T
    return F0_T
```
*   **Purpose:** Computes the theoretical no-arbitrage forward price ($F_0(T)$) at the inception of the contract ($t=0$).
*   **Functionality:**
    *   It calls `calculate_present_value` twice: once for dividends (`pv_dividends_at_0`) and once for costs (`pv_costs_at_0`), both discounted back to time $t=0$.
    *   It then applies the core forward price formula: $(S_0 - PV_0(I) + PV_0(C)) \times (1 + r)^T$.
*   **Financial Insight:** This function demonstrates that benefits reduce the forward price (as they are like receiving cash that reduces your net investment), while costs increase it (as they are additional outlays).

### `calculate_mtm_value(St, T, t_current, r, F0_T, dividends, costs)`

```python
def calculate_mtm_value(St, T, t_current, r, F0_T, dividends, costs):
    pv_remaining_dividends = calculate_present_value(dividends, r, t_current, T)
    pv_remaining_costs = calculate_present_value(costs, r, t_current, T)
    
    # Ensure remaining_time_to_maturity is non-negative
    remaining_time_to_maturity = max(0, T - t_current)
    
    Vt_T_long = (St - pv_remaining_dividends + pv_remaining_costs) - F0_T * (1 + r)**(-remaining_time_to_maturity)
    return Vt_T_long
```
*   **Purpose:** Calculates the Mark-to-Market (MTM) value of a long forward contract at any given `t_current`.
*   **Functionality:**
    *   It calculates the present value of only the *remaining* dividends and costs (those occurring after `t_current` but before `T`) by calling `calculate_present_value` with `current_time` set to `t_current`.
    *   It computes the effective spot price adjusted for future cash flows: $(S_t - PV_t(I) + PV_t(C))$.
    *   It discounts the original forward price ($F_0(T)$) back to the current time $t$ using the remaining time to maturity: $F_0(T) \times (1 + r)^{-(T-t)}$.
    *   The MTM value for a long position is the difference between the adjusted current spot price and the discounted original forward price.
*   **Key Insight:** The MTM value is the current gain or loss on the contract. It depends on how the spot price ($S_t$) has moved relative to the original forward price ($F_0(T)$), adjusted for any cash flows that occurred or are yet to occur.

## Exploring the Streamlit User Interface (`run_page()` function)
Duration: 0:10:00

The `run_page()` function in `application_pages/forward_contracts_simulator.py` is where all the user interaction and display logic resides.

```python
def run_page():
    st.header("Forward Contracts with Costs & Benefits Simulator")

    # Layout using columns for input widgets
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Core Contract Parameters")
        S0 = st.number_input(
            "Initial Spot Price ($S_0$):",
            min_value=0.01, value=100.0, step=0.1,
            help="The current market price of the underlying asset at t=0."
        )
        T = st.number_input(
            "Maturity ($T$):",
            min_value=0.1, value=1.0, step=0.1,
            help="Total time to maturity of the forward contract in years from t=0."
        )
        r = st.number_input(
            "Risk-Free Rate ($r$):",
            min_value=0.001, value=0.05, step=0.001, format="%.3f",
            help="The annualized risk-free interest rate (e.g., enter 0.05 for 5%)."
        )

    with col2:
        st.subheader("Current Valuation Parameters")
        t_current = st.number_input(
            "Current Time ($t$):",
            min_value=0.0, value=0.5, step=0.01,
            help="The current point in time for MTM valuation ($0 \\le t \\le T$).",
            key="current_time_t"
        )
        St = st.number_input(
            "Current Spot Price ($S_t$):",
            min_value=0.01, value=102.0, step=0.1,
            help="The spot price of the underlying asset at the current time t."
        )

    st.subheader("Cash Flow Specification")
    col_cf1, col_cf2 = st.columns(2)
    with col_cf1:
        dividends_json = st.text_area(
            "Dividends (Benefits) [JSON]:",
            value='[{"amount": 2.0, "time_from_t0": 0.25}, {"amount": 2.5, "time_from_t0": 0.75}]',
            height=100,
            help="Enter discrete dividends as a JSON list of objects. Each object needs 'amount' (float) and 'time_from_t0' (float, in years from t=0). Example: `[{\"amount\": 10.0, \"time_from_t0\": 0.5}]`."
        )
    with col_cf2:
        costs_json = st.text_area(
            "Costs [JSON]:",
            value='[{"amount": 1.0, "time_from_t0": 0.5}]',
            height=100,
            help="Enter discrete costs (e.g., storage) as a JSON list of objects. Each object needs 'amount' (float) and 'time_from_t0' (float, in years from t=0). Example: `[{\"amount\": 5.0, \"time_from_t0\": 0.75}]`."
        )

    position_type = st.radio(
        "Position Type for MTM Valuation:",
        ('long', 'short'),
        help="Select the position type for MTM valuation."
    )

    st.divider()

    # Input Validation
    if t_current > T:
        st.error("Error: Current Time (t) cannot be greater than Maturity (T). Please adjust the inputs.")
        st.stop()
    if S0 <= 0 or St <= 0:
        st.error("Error: Spot prices ($S_0$, $S_t$) must be positive.")
        st.stop()
    if r < 0:
        st.error("Error: Risk-Free Rate ($r$) cannot be negative.")
        st.stop()
    
    # ... (rest of the run_page() function)
```

### Input Widgets

The application provides intuitive Streamlit widgets for users to define the forward contract's parameters and observe their impact:

*   **Core Contract Parameters (Column 1):**
    *   `Initial Spot Price ($S_0$)`: The current price of the asset.
    *   `Maturity ($T$)`: The total length of the contract in years.
    *   `Risk-Free Rate ($r$)`: The annual interest rate used for discounting/compounding.
*   **Current Valuation Parameters (Column 2):**
    *   `Current Time ($t$)`: The point in time at which the MTM value is being calculated. This must be between 0 and `T`.
    *   `Current Spot Price ($S_t$)`: The market price of the underlying asset at the `Current Time`.
*   **Cash Flow Specification (Two Columns):**
    *   `Dividends (Benefits) [JSON]`: A `st.text_area` for entering dividends. It expects a JSON list of objects, each with an `amount` and `time_from_t0`. This allows for multiple discrete dividend payments at different times.
        *   Example: `[{"amount": 2.0, "time_from_t0": 0.25}, {"amount": 2.5, "time_from_t0": 0.75}]`
    *   `Costs [JSON]`: Similar to dividends, this `st.text_area` is for entering discrete costs like storage fees.
        *   Example: `[{"amount": 1.0, "time_from_t0": 0.5}]`
*   **Position Type for MTM Valuation:**
    *   `st.radio` allows selection between a 'long' or 'short' position, which flips the sign of the MTM value accordingly.

### Input Validation

Before performing calculations, the application includes basic validation checks:
*   `t_current` must not exceed `T`.
*   `S0` and `St` must be positive.
*   `r` cannot be negative.
*   The `parse_cash_flows` helper function handles the validation of the JSON inputs for dividends and costs, providing specific error messages if the format is incorrect.

<aside class="negative">
It's critical for users to follow the exact JSON format for cash flows. Any syntax errors (e.g., missing commas, incorrect quotes) will result in a parsing error.
</aside>

### Calculated Outputs

After validation and parsing, the application performs the core financial calculations using the helper functions:

```python
    # Calculations
    F0_T_with_cb = calculate_forward_price_at_inception(S0, T, r, dividends, costs)
    F0_T_without_cb = calculate_forward_price_at_inception(S0, T, r, [], []) # For comparison

    Vt_T_long = calculate_mtm_value(St, T, t_current, r, F0_T_with_cb, dividends, costs)
    Vt_T_short = -Vt_T_long if position_type == 'short' else Vt_T_long # MTM for short position

    st.subheader("Calculated Outputs")
    col_metrics1, col_metrics2 = st.columns(2)
    with col_metrics1:
        st.metric(label="Forward Price at Inception ($F_0(T)$) (with C/B)", value=f"{F0_T_with_cb:,.2f}")
    with col_metrics2:
        st.metric(label="Forward Price at Inception ($F_0(T)$) (without C/B)", value=f"{F0_T_without_cb:,.2f}")

    mtm_label = f"MTM Value at Current Time ($V_t(T)$) ({position_type.capitalize()} Position)"
    st.metric(label=mtm_label, value=f"{Vt_T_short:,.2f}") # Use Vt_T_short which is already adjusted for position_type
```
*   **Forward Price at Inception ($F_0(T)$) (with C/B):** The calculated forward price including the effects of dividends and costs.
*   **Forward Price at Inception ($F_0(T)$) (without C/B):** For comparison, the forward price if no dividends or costs were involved. This helps illustrate the impact of cash flows.
*   **MTM Value at Current Time ($V_t(T)$):** The current Mark-to-Market value of the forward contract, adjusted for the selected position type (long/short).

## Deep Dive into Visualizations
Duration: 0:12:00

The application leverages Plotly to generate three interactive visualizations, providing deeper insights into the behavior of forward contracts.

### 1. MTM Value Evolution Over Time (Long Position)

```python
    st.markdown("#### MTM Value Evolution Over Time (Long Position)")
    num_points = 100
    time_points = np.linspace(0, T, num_points)
    mtm_values_with_cb = []
    mtm_values_without_cb = []

    # Original F0_T (needed for comparison)
    original_F0_T_with_cb = calculate_forward_price_at_inception(S0, T, r, dividends, costs)
    original_F0_T_without_cb = calculate_forward_price_at_inception(S0, T, r, [], [])

    # Simulating spot price for MTM evolution plot
    # A simple linear interpolation for S_t_plot from S0 to a reasonable end price (e.g., F0_T_with_cb)
    S_T_plot_end_value = F0_T_with_cb 
    S_t_for_plot = np.linspace(S0, S_T_plot_end_value, num_points)

    for i, t_val in enumerate(time_points):
        current_S_t_for_plot = S_t_for_plot[i]
        
        mtm_val_with = calculate_mtm_value(current_S_t_for_plot, T, t_val, r, F0_T_with_cb, dividends, costs)
        mtm_values_with_cb.append(mtm_val_with)
        
        mtm_val_without = calculate_mtm_value(current_S_t_for_plot, T, t_val, r, F0_T_without_cb, [], [])
        mtm_values_without_cb.append(mtm_val_without)

    df_mtm_evolution = pd.DataFrame({
        'Time (Years)': time_points,
        'MTM Value (with C/B)': mtm_values_with_cb,
        'MTM Value (without C/B)': mtm_values_without_cb
    })

    fig_mtm_evolution = go.Figure()
    fig_mtm_evolution.add_trace(go.Scatter(x=df_mtm_evolution['Time (Years)'], y=df_mtm_evolution['MTM Value (with C/B)'],
                                           mode='lines', name='MTM Value (with C/B)'))
    fig_mtm_evolution.add_trace(go.Scatter(x=df_mtm_evolution['Time (Years)'], y=df_mtm_evolution['MTM Value (without C/B)'],
                                           mode='lines', name='MTM Value (without C/B)'))

    # Add vertical line for current time
    fig_mtm_evolution.add_vline(x=t_current, line_dash="dash", line_color="grey", annotation_text=f"Current Time (t={t_current:.2f})")
    # Add horizontal line for Y=0
    fig_mtm_evolution.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Break-even (Y=0)")

    fig_mtm_evolution.update_layout(
        title='MTM Value Evolution Over Time (Long Position)',
        xaxis_title='Time (Years)',
        yaxis_title='MTM Value',
        hovermode="x unified",
        legend_title_text='Scenario'
    )
    st.plotly_chart(fig_mtm_evolution, use_container_width=True)
```
*   **What it shows:** This line plot visualizes how the MTM value of a long forward position changes from $t=0$ to maturity $T$. It presents two lines: one for the contract with costs and benefits, and one for a simplified contract without them.
*   **How it works:**
    *   It generates a series of `time_points` from $0$ to $T$.
    *   For each `time_point`, it calculates a hypothetical `S_t_for_plot`. For simplicity, this simulation assumes the spot price `S_t` increases linearly from `S0` at $t=0$ to the `F0_T_with_cb` (the forward price at inception including C/B) at maturity `T`. This provides a changing spot price to illustrate MTM movement.
    *   The `calculate_mtm_value` function is then called for each `time_point` using the simulated `S_t_for_plot` and the fixed `F0_T` (calculated at inception).
*   **Interpretation:**
    *   The graph helps understand the path of profit/loss over the contract's life.
    *   The difference between the "with C/B" and "without C/B" lines illustrates the direct impact of these cash flows on the MTM value.
    *   A vertical dashed line indicates the `current_time` (`t_current`) you set in the input, showing the MTM value at that specific moment.
    *   A horizontal red dashed line at Y=0 represents the break-even point for the contract.

### 2. Sensitivity of Forward Price to Costs/Benefits Magnitude

```python
    st.markdown("#### Sensitivity of Forward Price to Costs/Benefits Magnitude")
    multipliers = np.linspace(0, 2, 21) # From 0x to 2x original amount

    f0_sensitivity_costs = []
    f0_sensitivity_dividends = []

    # Original PV of costs/benefits
    original_pv_costs = calculate_present_value(costs, r, 0, T)
    original_pv_dividends = calculate_present_value(dividends, r, 0, T)

    for mult in multipliers:
        # Sensitivity to Costs
        temp_costs_for_sensitivity = [{"amount": cf["amount"] * mult, "time_from_t0": cf["time_from_t0"]} for cf in costs]
        f0_costs = calculate_forward_price_at_inception(S0, T, r, dividends, temp_costs_for_sensitivity)
        f0_sensitivity_costs.append(f0_costs)

        # Sensitivity to Dividends
        temp_dividends_for_sensitivity = [{"amount": cf["amount"] * mult, "time_from_t0": cf["time_from_t0"]} for cf in dividends]
        f0_dividends = calculate_forward_price_at_inception(S0, T, r, temp_dividends_for_sensitivity, costs)
        f0_sensitivity_dividends.append(f0_dividends)

    df_sensitivity = pd.DataFrame({
        'Multiplier': multipliers,
        'Forward Price (Costs Multiplied)': f0_sensitivity_costs,
        'Forward Price (Dividends Multiplied)': f0_sensitivity_dividends
    })

    fig_sensitivity = go.Figure()
    fig_sensitivity.add_trace(go.Scatter(x=df_sensitivity['Multiplier'], y=df_sensitivity['Forward Price (Costs Multiplied)'],
                                        mode='lines', name='F0(T) vs. Costs Multiplier'))
    fig_sensitivity.add_trace(go.Scatter(x=df_sensitivity['Multiplier'], y=df_sensitivity['Forward Price (Dividends Multiplied)'],
                                        mode='lines', name='F0(T) vs. Dividends Multiplier'))

    fig_sensitivity.update_layout(
        title='Sensitivity of Forward Price to Costs/Benefits Magnitude',
        xaxis_title='Multiplier of Original Costs/Benefits',
        yaxis_title='Forward Price ($F_0(T)$)',
        hovermode="x unified",
        legend_title_text='Factor'
    )
    st.plotly_chart(fig_sensitivity, use_container_width=True)
```
*   **What it shows:** This plot demonstrates how the initial forward price ($F_0(T)$) changes as the magnitude of either costs or benefits is scaled.
*   **How it works:**
    *   It creates a range of `multipliers` from 0 (no cost/benefit) to 2 (double the cost/benefit).
    *   For each multiplier, it calculates a `temp_costs_for_sensitivity` or `temp_dividends_for_sensitivity` by multiplying the original cash flow amounts.
    *   It then re-calculates `F0_T` using these scaled cash flows, keeping the other cash flow type constant.
*   **Interpretation:**
    *   You'll observe that as the `Costs Multiplier` increases, $F_0(T)$ increases. This is because higher holding costs need to be covered by a higher forward price.
    *   Conversely, as the `Dividends Multiplier` increases, $F_0(T)$ decreases. Benefits reduce the effective cost of holding the asset, thus lowering the forward price.

### 3. MTM Value Comparison Across Scenarios (Long/Short Position)

```python
    st.markdown("#### MTM Value Comparison Across Scenarios (Long Position)")

    # Define scenarios
    scenarios = {
        'Base Case (with C/B)': {
            'dividends': dividends,
            'costs': costs
        },
        'No Costs/Benefits': {
            'dividends': [],
            'costs': []
        },
        'Double Dividends': {
            'dividends': [{"amount": cf["amount"] * 2, "time_from_t0": cf["time_from_t0"]} for cf in dividends],
            'costs': costs
        },
        'Double Costs': {
            'dividends': dividends,
            'costs': [{"amount": cf["amount"] * 2, "time_from_t0": cf["time_from_t0"]} for cf in costs]
        }
    }

    scenario_mtm_values = []
    scenario_names = []

    for name, params in scenarios.items():
        # Need to recalculate F0_T for each scenario based on *its* cash flows
        # Then calculate MTM using that F0_T.
        
        scenario_F0_T = calculate_forward_price_at_inception(S0, T, r, params['dividends'], params['costs'])
        mtm_val = calculate_mtm_value(St, T, t_current, r, scenario_F0_T, params['dividends'], params['costs'])
        
        # If the displayed MTM is for the selected position_type, apply it here
        if position_type == 'short':
            mtm_val = -mtm_val
            
        scenario_mtm_values.append(mtm_val)
        scenario_names.append(name)

    df_scenario_comparison = pd.DataFrame({
        'Scenario': scenario_names,
        'MTM Value': scenario_mtm_values
    })

    fig_scenario_comparison = px.bar(
        df_scenario_comparison,
        x='Scenario',
        y='MTM Value',
        title=f'MTM Value Comparison Across Scenarios ({position_type.capitalize()} Position)',
        labels={'MTM Value': 'MTM Value ($)'},
        text='MTM Value'
    )
    fig_scenario_comparison.update_traces(texttemplate='%{text:,.2f}', textposition='outside')
    fig_scenario_comparison.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_scenario_comparison, use_container_width=True)
```
*   **What it shows:** This bar chart compares the current MTM value of the forward contract under several predefined scenarios (base case, no costs/benefits, double dividends, double costs).
*   **How it works:**
    *   A dictionary `scenarios` defines different configurations of `dividends` and `costs`.
    *   For each scenario, the application first recalculates the `scenario_F0_T` (as the inception price would be different under different C/B assumptions).
    *   Then, it calculates the `mtm_val` using the current spot price `St`, current time `t_current`, and the `scenario_F0_T`.
    *   The `position_type` selected by the user is applied to flip the MTM sign for short positions.
*   **Interpretation:** This plot quickly illustrates how different assumptions about costs and benefits drastically change the MTM value of a contract at any given time. It reinforces the importance of accurately forecasting and accounting for all cash flows.

## Running the Application
Duration: 0:02:00

Once you have saved both `app.py` and `application_pages/forward_contracts_simulator.py` in their respective directories, you can run the Streamlit application from your terminal.

1.  **Navigate to the main directory:**
    Open your terminal or command prompt and change your current directory to `qu_forward_contracts` (where `app.py` is located).
    ```console
    cd qu_forward_contracts
    ```

2.  **Run the Streamlit app:**
    Execute the following command:
    ```console
    streamlit run app.py
    ```

3.  **Access the application:**
    Streamlit will open a new tab in your default web browser, displaying the application. If it doesn't open automatically, it will provide a local URL (e.g., `http://localhost:8501`) that you can copy and paste into your browser.

<aside class="positive">
Experiment with different input values for initial spot price, maturity, risk-free rate, current time, current spot price, and especially the JSON inputs for dividends and costs. Observe how the Forward Price at Inception and MTM Value change, and how the visualizations respond. This hands-on interaction will deepen your understanding.
</aside>

## Conclusion
Duration: 0:03:00

Congratulations! You have successfully explored the **QuLab: Forward Contracts with Costs & Benefits Simulator**. Through this codelab, you've gained a comprehensive understanding of:

*   The fundamental **No-Arbitrage Principle** in derivative pricing.
*   The calculation of **Forward Price at Inception ($F_0(T)$)**, incorporating discrete costs and benefits.
*   The computation of **Mark-to-Market (MTM) Value ($V_t(T)$)**, reflecting current profit/loss.
*   The practical implementation of these concepts using Python and Streamlit.
*   The impact of varying parameters and cash flow scenarios on contract valuation through interactive visualizations.

This application serves as a robust educational tool for anyone looking to solidify their understanding of forward contracts, particularly how intermediate cash flows (dividends and storage costs) influence their fair value and ongoing profitability.

### Further Exploration

*   **Continuous Costs/Benefits:** Extend the model to include continuous dividend yields or storage costs, which are often modeled differently than discrete payments.
*   **Stochastic Spot Prices:** Instead of a simple linear path for $S_t$ in the MTM evolution plot, implement a more realistic stochastic process like Geometric Brownian Motion to simulate price movements.
*   **Other Derivatives:** Apply similar principles to value other derivatives such as futures contracts (considering daily mark-to-market and margin calls) or options.
*   **Real-World Data:** Integrate real-time market data for spot prices, interest rates, and dividend schedules to make the simulations more reflective of current market conditions.

Keep experimenting, keep learning, and continue to build your quantitative finance skills!
