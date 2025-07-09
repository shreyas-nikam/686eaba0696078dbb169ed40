
# Technical Specification for Jupyter Notebook: Forward Contracts with Costs & Benefits Simulator

## 1. Notebook Overview

This Jupyter Notebook provides an interactive simulator to explore the pricing and valuation of forward contracts when the underlying asset incurs additional costs (e.g., storage costs) or provides benefits (e.g., dividends). It aims to clarify how these factors influence the forward price at inception and the mark-to-market (MTM) value throughout the contract's life.

### Learning Goals

Upon completing this notebook, users will be able to:
*   Understand how costs and benefits associated with an underlying asset affect the forward price at inception, as detailed in the provided document [1].
*   Analyze the impact of different timing and magnitudes of costs (e.g., storage) and benefits (e.g., dividends) on the forward contract's MTM value over time, referencing concepts in the provided document [2, 3].
*   Apply the general MTM valuation formula incorporating costs and benefits.
*   Grasp the no-arbitrage conditions when considering asset ownership expenses or income.
*   Extract key insights from the mathematical foundations and visualize their practical implications.

### Target Audience
Financial analysts, derivatives traders, and students seeking to understand the nuances of forward contract valuation beyond simple cases.

### Scope & Constraints
*   The notebook is designed for end-to-end execution on a mid-spec laptop (8 GB RAM) within five minutes.
*   Only open-source Python libraries available on PyPI will be used.
*   Each major computational or conceptual step will be accompanied by both detailed code comments and brief narrative Markdown cells explaining "what" is happening and "why."
*   This specification focuses on the logical flow, markdown explanations, and code sections within a Jupyter Notebook environment. It explicitly excludes deployment steps or references to specific platforms (e.g., Streamlit).

## 2. Mathematical and Theoretical Foundations

This section will lay out the core financial formulas and concepts for pricing and valuing forward contracts, especially those incorporating costs and benefits. All mathematical content will adhere strictly to LaTeX formatting rules.

### 2.1 Forward Contracts without Costs or Benefits

A forward contract is an agreement to buy or sell an asset at a predetermined price on a future date. At inception ($t=0$), the value of a forward contract is typically zero, but its price is set to prevent arbitrage.

*   **Forward Price at Inception ($F_0(T)$):**
    For an underlying asset that does not generate cash flows, the forward price at inception is the future value of the spot price compounded at the risk-free rate.
    $$F_0(T) = S_0(1+r)^T$$
    Where:
    *   $S_0$: Spot price of the underlying asset at time $t=0$.
    *   $r$: Annual risk-free rate (discrete compounding).
    *   $T$: Time to maturity of the forward contract in years.

*   **Mark-to-Market (MTM) Value during Contract Life ($V_t(T)$):**
    The MTM value of a forward contract at any time $t$ (where $0 < t < T$) reflects the change in the underlying price and other factors that would result in a gain or loss if the contract were settled immediately.
    For a long forward position:
    $$V_t(T) = S_t - F_0(T)(1+r)^{-(T-t)}$$
    For a short forward position, the MTM value is simply the negative of the long position's value:
    $$V_t(T)_{short} = F_0(T)(1+r)^{-(T-t)} - S_t$$
    Where:
    *   $S_t$: Spot price of the underlying asset at current time $t$.
    *   $F_0(T)$: Original forward price agreed upon at inception.
    *   $T$: Original time to maturity.
    *   $t$: Current time (time elapsed from inception).

### 2.2 Forward Contracts with Discrete Costs and Benefits

Many underlying assets of forward contracts incur costs (e.g., storage, insurance) or provide benefits (e.g., dividends, convenience yield). These discrete cash flows significantly influence the forward price and subsequent valuation.

*   **Present Value (PV) of Discrete Cash Flows:**
    For discrete cash flows (dividends $I_j$ and costs $C_k$) occurring before or at maturity $T$, their present values at time $t$ are calculated as:
    $$PV_t(I) = \sum_{\text{all } j \text{ s.t. } t < t_j^I \le T} I_j (1+r)^{-(t_j^I - t)}$$
    $$PV_t(C) = \sum_{\text{all } k \text{ s.t. } t < t_k^C \le T} C_k (1+r)^{-(t_k^C - t)}$$
    Where:
    *   $I_j$: Amount of the $j$-th dividend.
    *   $t_j^I$: Time of the $j$-th dividend payment from inception.
    *   $C_k$: Amount of the $k$-th cost.
    *   $t_k^C$: Time of the $k$-th cost payment from inception.
    *   The sums only include cash flows that *remain* to be paid or received from the current time $t$ until maturity $T$.

*   **Forward Price at Inception ($F_0(T)$) with Costs and Benefits:**
    At inception ($t=0$), the forward price reflects the initial spot price adjusted for the present value of all future benefits (subtracted) and costs (added) associated with owning the underlying asset until maturity, compounded at the risk-free rate.
    $$F_0(T) = (S_0 - PV_0(I) + PV_0(C))(1+r)^T$$
    Where $PV_0(I)$ and $PV_0(C)$ are the present values of all benefits and costs from time $t=0$ until maturity $T$, respectively, discounted back to $t=0$. This formula ensures a no-arbitrage condition [1].

*   **MTM Value during Contract Life ($V_t(T)$) with Costs and Benefits:**
    The MTM value of a forward contract at any time $t$ is calculated by adjusting the current spot price for the present value of *remaining* costs and benefits, then subtracting the present value of the original forward price.
    For a long forward position:
    $$V_t(T) = (S_t - PV_t(I) + PV_t(C)) - F_0(T)(1+r)^{-(T-t)}$$
    For a short forward position:
    $$V_t(T)_{short} = F_0(T)(1+r)^{-(T-t)} - (S_t - PV_t(I) + PV_t(C))$$
    Where $PV_t(I)$ and $PV_t(C)$ are the present values of *remaining* benefits and costs, respectively, from current time $t$ until maturity $T$, discounted back to time $t$ [4].

### 2.3 No-Arbitrage Principle
All these formulas are derived under the assumption of no-arbitrage, meaning that it is not possible to make a risk-free profit by simultaneously entering into offsetting positions in the spot and forward markets. The prices and values ensure that any combination of borrowing, lending, and holding the asset replicates the forward contract.

## 3. Code Requirements

### 3.1 Library Imports
The notebook will begin with a cell dedicated to importing all necessary open-source Python libraries.
```python
# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from ipywidgets import interact, FloatText, Textarea, Layout, HTML
from IPython.display import display, Markdown, clear_output
import json # For parsing string input for cash flows
import io # For sample CSV
```

### 3.2 Data Handling & Validation
The notebook will include functionality to handle and validate input data, providing options for user-defined parameters or a lightweight synthetic sample.

#### Markdown Explanations:
*   A markdown cell will introduce the data input section, explaining how users can provide parameters via interactive widgets.
*   Instructions will be provided for entering discrete cash flows (dividends/costs) in a specific JSON-like string format (e.g., `[(amount, time_from_t0), ...]`).
*   Explanation of data validation steps.

#### Code Sections:
1.  **Synthetic Sample Data (Optional):**
    A small CSV-like string will be embedded to allow the notebook to run without user input, demonstrating the expected data structure.
    ```python
    # Optional: Lightweight sample data
    # This data represents a hypothetical scenario for demonstration
    sample_data_csv = """
    parameter,value,unit
    initial_spot_price,100.0,USD
    maturity_T,1.0,Years
    risk_free_rate,0.05,Decimal
    current_time_t,0.5,Years
    current_spot_price_St,105.0,USD
    dividend_cash_flows,[{"amount": 2.0, "time_from_t0": 0.25}, {"amount": 2.5, "time_from_t0": 0.75}],
    cost_cash_flows,[{"amount": 1.0, "time_from_t0": 0.4}],
    """
    sample_df = pd.read_csv(io.StringIO(sample_data_csv), index_col='parameter')

    # Default values for widgets if no user input
    DEFAULT_S0 = float(sample_df.loc['initial_spot_price', 'value'])
    DEFAULT_T = float(sample_df.loc['maturity_T', 'value'])
    DEFAULT_R = float(sample_df.loc['risk_free_rate', 'value'])
    DEFAULT_CURRENT_T = float(sample_df.loc['current_time_t', 'value'])
    DEFAULT_CURRENT_ST = float(sample_df.loc['current_spot_price_St', 'value'])
    DEFAULT_DIVIDENDS_STR = sample_df.loc['dividend_cash_flows', 'value']
    DEFAULT_COSTS_STR = sample_df.loc['cost_cash_flows', 'value']
    ```

2.  **Interactive Input Widgets:**
    This section will define and display `ipywidgets` for user input.
    ```python
    # Configure widget layout for better readability
    widget_layout = Layout(width='300px', padding='5px')
    label_layout = Layout(width='200px', padding='5px')

    # Define widgets for core parameters
    s0_input = FloatText(value=DEFAULT_S0, description='$S_0$ (Initial Spot Price):', layout=widget_layout)
    T_input = FloatText(value=DEFAULT_T, description='$T$ (Maturity in Years):', layout=widget_layout)
    r_input = FloatText(value=DEFAULT_R, description='$r$ (Risk-Free Rate, e.g., 0.05):', layout=widget_layout)
    current_t_input = FloatText(value=DEFAULT_CURRENT_T, description='$t$ (Current Time in Years):', layout=widget_layout)
    current_st_input = FloatText(value=DEFAULT_CURRENT_ST, description='$S_t$ (Current Spot Price):', layout=widget_layout)

    # Define Textarea widgets for discrete cash flows
    # Format: [{"amount": X, "time_from_t0": Y}, ...]
    dividends_input = Textarea(
        value=DEFAULT_DIVIDENDS_STR,
        description='Dividends (JSON list of {"amount": X, "time_from_t0": Y}):',
        layout=Layout(width='600px', height='100px', padding='5px')
    )
    costs_input = Textarea(
        value=DEFAULT_COSTS_STR,
        description='Costs (JSON list of {"amount": X, "time_from_t0": Y}):',
        layout=Layout(width='600px', height='100px', padding='5px')
    )

    # Display widgets (this would be in a separate cell in the notebook)
    # display(HTML("<h3>Input Parameters:</h3>"))
    # display(s0_input, T_input, r_input, current_t_input, current_st_input, dividends_input, costs_input)

    # A button to trigger calculation if not using interact directly
    # calculate_button = widgets.Button(description="Calculate & Visualize")
    # output_area = widgets.Output()
    # display(calculate_button, output_area)
    ```

3.  **Data Validation and Parsing:**
    A helper function to parse the cash flow strings and validate inputs.
    ```python
    def parse_cash_flows(cf_str, cf_type):
        """Parses cash flow string into a list of dictionaries and validates."""
        try:
            cf_list = json.loads(cf_str)
            if not isinstance(cf_list, list):
                raise ValueError(f"{cf_type} input must be a list.")
            for cf in cf_list:
                if not isinstance(cf, dict) or 'amount' not in cf or 'time_from_t0' not in cf:
                    raise ValueError(f"Each {cf_type} item must be a dictionary with 'amount' and 'time_from_t0'.")
                if not isinstance(cf['amount'], (int, float)) or not isinstance(cf['time_from_t0'], (int, float)):
                    raise TypeError(f"Amount and time for {cf_type} must be numeric.")
            return cf_list
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format for {cf_type}. Please use list of dictionaries.")
            return []
        except ValueError as e:
            print(f"Error validating {cf_type}: {e}")
            return []
        except TypeError as e:
            print(f"Error validating {cf_type}: {e}")
            return []

    def validate_inputs(s0, T, r, current_t, current_st):
        """Validates numeric inputs."""
        if not all(isinstance(x, (int, float)) for x in [s0, T, r, current_t, current_st]):
            raise TypeError("All primary inputs must be numeric.")
        if s0 <= 0 or T <= 0 or r <= -1: # r can be negative, but not -1 or less for discrete comp.
            raise ValueError("Spot price and maturity must be positive. Risk-free rate must be > -1.")
        if not (0 <= current_t <= T):
            raise ValueError("Current time 't' must be between 0 and Maturity 'T'.")
        # Log summary statistics (example, would be more comprehensive in actual notebook)
        print(f"--- Input Summary ---")
        print(f"S0: {s0:.2f}, T: {T:.2f} years, r: {r*100:.2f}%")
        print(f"Current t: {current_t:.2f} years, St: {current_st:.2f}")
        print(f"---------------------")

    # This function would be called by the interact decorator or button
    def run_analysis(s0, T, r, current_t, current_st, dividends_str, costs_str):
        clear_output(wait=True) # Clear previous output for interact

        try:
            validate_inputs(s0, T, r, current_t, current_st)
            dividends = parse_cash_flows(dividends_str, "dividends")
            costs = parse_cash_flows(costs_str, "costs")
            # ... rest of the calculations and plotting will go here ...
        except (ValueError, TypeError) as e:
            display(Markdown(f"<span style='color:red'>**Input Error:** {e}</span>"))
            return
    ```

### 3.3 Algorithms and Functions
The core logic for pricing and valuation.

#### Markdown Explanations:
*   Explanation for each function, detailing its purpose and the formula it implements.

#### Code Sections:
1.  **`calculate_pv(cash_flows, rate, current_time, maturity)`:**
    Calculates the present value of a list of discrete cash flows that occur *after* `current_time` and *before or at* `maturity`.
    ```python
    def calculate_pv(cash_flows, rate, current_time, maturity):
        """
        Calculates the present value of future discrete cash flows from current_time
        to maturity.
        :param cash_flows: List of dictionaries like [{'amount': X, 'time_from_t0': Y}]
        :param rate: Risk-free rate (decimal)
        :param current_time: Current time 't' from inception (years)
        :param maturity: Contract maturity 'T' from inception (years)
        :return: Present value of relevant cash flows at current_time
        """
        pv = 0.0
        for cf in cash_flows:
            cf_amount = cf['amount']
            cf_time_from_t0 = cf['time_from_t0']
            if current_time < cf_time_from_t0 <= maturity:
                time_to_discount = cf_time_from_t0 - current_time
                pv += cf_amount * (1 + rate)**(-time_to_discount)
        return pv
    ```

2.  **`calculate_forward_price_at_inception(S0, r, T, dividends_at_t0, costs_at_t0)`:**
    Calculates the forward price at inception ($F_0(T)$) considering all costs and benefits from $t=0$ to $T$.
    ```python
    def calculate_forward_price_at_inception(S0, r, T, dividends, costs):
        """
        Calculates the forward price at inception, considering all costs and benefits.
        :param S0: Initial spot price
        :param r: Risk-free rate (decimal)
        :param T: Maturity (years)
        :param dividends: List of all dividend cash flows from t=0
        :param costs: List of all cost cash flows from t=0
        :return: Forward price at inception F0(T)
        """
        pv_dividends_at_0 = calculate_pv(dividends, r, 0, T)
        pv_costs_at_0 = calculate_pv(costs, r, 0, T)
        return (S0 - pv_dividends_at_0 + pv_costs_at_0) * (1 + r)**T
    ```

3.  **`calculate_mtm_value(St, F0_T, r, T, t, dividends_at_t, costs_at_t, position_type='long')`:**
    Computes the MTM value for a long or short forward position at a given time $t$.
    ```python
    def calculate_mtm_value(St, F0_T, r, T, t, dividends, costs, position_type='long'):
        """
        Computes the Mark-to-Market (MTM) value of a forward contract.
        :param St: Current spot price
        :param F0_T: Forward price at inception
        :param r: Risk-free rate (decimal)
        :param T: Original maturity (years)
        :param t: Current time (years)
        :param dividends: List of all dividend cash flows (from t=0)
        :param costs: List of all cost cash flows (from t=0)
        :param position_type: 'long' or 'short'
        :return: MTM value at time t
        """
        pv_dividends_at_t = calculate_pv(dividends, r, t, T)
        pv_costs_at_t = calculate_pv(costs, r, t, T)

        # Present value of the original forward price discounted from T to t
        pv_F0_T = F0_T * (1 + r)**(-(T - t))

        if position_type == 'long':
            mtm = (St - pv_dividends_at_t + pv_costs_at_t) - pv_F0_T
        elif position_type == 'short':
            mtm = pv_F0_T - (St - pv_dividends_at_t + pv_costs_at_t)
        else:
            raise ValueError("position_type must be 'long' or 'short'.")
        return mtm
    ```

### 3.4 Visualization
The notebook will generate three types of plots, adhering to style and usability guidelines.

#### Markdown Explanations:
*   Introduction to each plot, explaining what it visualizes and why it's important.
*   Interpretation guidance for each visualization.

#### Code Sections:
1.  **Plotting Configuration:**
    Set a color-blind friendly palette and general plot styles.
    ```python
    # Configure plotting style
    sns.set_theme(style="whitegrid", palette="viridis")
    plt.rcParams.update({'font.size': 12, 'axes.titlesize': 14, 'axes.labelsize': 12,
                          'xtick.labelsize': 10, 'ytick.labelsize': 10,
                          'legend.fontsize': 10})
    ```

2.  **Trend Plot (Line Plot): Evolution of MTM over Time**
    Simulates the evolution of the spot price and calculates MTM values over time for scenarios with and without costs/benefits.
    ```python
    def plot_mtm_trend(s0, T, r, F0_T_with_cb, F0_T_no_cb, dividends, costs):
        """
        Generates a line plot showing MTM evolution over time.
        Assumes a simple linear growth for spot price for demonstration.
        """
        time_points = np.linspace(0.0, T, 100)
        
        # Simple linear spot price path for demonstration
        # Start at S0, end at S0 * (1 + T * 0.02) for example (2% annual growth)
        final_st_for_trend = s0 * (1 + T * 0.02)
        spot_prices_over_time = np.linspace(s0, final_st_for_trend, 100)

        mtm_long_with_cb = [calculate_mtm_value(St_val, F0_T_with_cb, r, T, t_val, dividends, costs, 'long')
                            for t_val, St_val in zip(time_points, spot_prices_over_time)]
        mtm_short_with_cb = [calculate_mtm_value(St_val, F0_T_with_cb, r, T, t_val, dividends, costs, 'short')
                             for t_val, St_val in zip(time_points, spot_prices_over_time)]

        # Calculate MTM without costs/benefits for comparison (assuming no costs/benefits exist)
        F0_T_no_cb_actual = s0 * (1 + r)**T # F0(T) without C/B
        mtm_long_no_cb = [calculate_mtm_value(St_val, F0_T_no_cb_actual, r, T, t_val, [], [], 'long')
                          for t_val, St_val in zip(time_points, spot_prices_over_time)]
        mtm_short_no_cb = [calculate_mtm_value(St_val, F0_T_no_cb_actual, r, T, t_val, [], [], 'short')
                           for t_val, St_val in zip(time_points, spot_prices_over_time)]


        plt.figure(figsize=(10, 6))
        plt.plot(time_points, mtm_long_with_cb, label='Long Position MTM (With C/B)', linestyle='-')
        plt.plot(time_points, mtm_short_with_cb, label='Short Position MTM (With C/B)', linestyle='--')
        plt.plot(time_points, mtm_long_no_cb, label='Long Position MTM (No C/B)', linestyle='-', alpha=0.6, color='gray')
        plt.plot(time_points, mtm_short_no_cb, label='Short Position MTM (No C/B)', linestyle='--', alpha=0.6, color='darkgray')

        plt.title('Evolution of Forward Contract MTM Value Over Time')
        plt.xlabel('Time (Years from Inception)')
        plt.ylabel('MTM Value')
        plt.axhline(0, color='black', linewidth=0.5, linestyle=':')
        plt.legend()
        plt.grid(True, linestyle=':', alpha=0.7)
        plt.tight_layout()
        plt.show()
        # For static fallback: plt.savefig('mtm_trend.png')
    ```

3.  **Relationship Plot (Scatter Plot): Sensitivity of Forward Price to Parameters**
    Illustrates how the initial forward price changes with variations in a key input parameter (e.g., risk-free rate).
    ```python
    def plot_forward_price_sensitivity(s0, T, r_base, dividends, costs):
        """
        Generates a scatter plot showing sensitivity of F0(T) to varying risk-free rates.
        """
        r_values = np.linspace(max(0.001, r_base - 0.03), r_base + 0.03, 50) # Vary r
        forward_prices = [calculate_forward_price_at_inception(s0, r_val, T, dividends, costs) for r_val in r_values]

        plt.figure(figsize=(10, 6))
        plt.scatter(r_values * 100, forward_prices, s=50, alpha=0.7)
        plt.plot(r_values * 100, forward_prices, linestyle='-', alpha=0.5) # Connect points

        plt.title('Sensitivity of Forward Price to Risk-Free Rate')
        plt.xlabel('Risk-Free Rate (%)')
        plt.ylabel('Forward Price at Inception ($F_0(T)$)')
        plt.grid(True, linestyle=':', alpha=0.7)
        plt.tight_layout()
        plt.show()
        # For static fallback: plt.savefig('forward_price_sensitivity.png')
    ```

4.  **Aggregated Comparison (Bar Chart): Comparing Scenarios**
    Compares forward prices at inception for different scenarios of costs and benefits.
    ```python
    def plot_scenario_comparison(s0, T, r):
        """
        Generates a bar chart comparing F0(T) for different cost/benefit scenarios.
        """
        # Define example scenarios for comparison
        scenario_data = {
            'No C/B': [],
            'Only Dividends': [{"amount": 2.0, "time_from_t0": 0.5}],
            'Only Costs': [{"amount": 1.5, "time_from_t0": 0.6}],
            'Both C/B': [{"amount": 2.0, "time_from_t0": 0.5}],
            'Both C/B (High Cost)': [{"amount": 2.0, "time_from_t0": 0.5}],
        }
        
        # Adjusting the high cost scenario to explicitly show more cost impact
        scenario_data['Both C/B'][0]['costs'] = [{"amount": 1.5, "time_from_t0": 0.6}]
        scenario_data['Both C/B (High Cost)'][0]['costs'] = [{"amount": 3.0, "time_from_t0": 0.6}]

        forward_prices_at_inception = {}
        for scenario, dividends_in_scenario in scenario_data.items():
            costs_in_scenario = []
            if scenario in ['Only Costs', 'Both C/B', 'Both C/B (High Cost)']:
                # For simplicity, if scenario_data[scenario] is empty for dividends, this will be fine
                costs_in_scenario = scenario_data[scenario][0].get('costs', []) if scenario_data[scenario] else []
            
            fwd_price = calculate_forward_price_at_inception(s0, r, T, dividends_in_scenario, costs_in_scenario)
            forward_prices_at_inception[scenario] = fwd_price

        scenarios = list(forward_prices_at_inception.keys())
        prices = list(forward_prices_at_inception.values())

        plt.figure(figsize=(10, 6))
        sns.barplot(x=scenarios, y=prices, palette="viridis")

        plt.title('Forward Price at Inception Across Different Scenarios')
        plt.xlabel('Scenario')
        plt.ylabel('Forward Price ($F_0(T)$)')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle=':', alpha=0.7)
        plt.tight_layout()
        plt.show()
        # For static fallback: plt.savefig('scenario_comparison.png')
    ```

### 3.5 Orchestration (Main Execution Logic)
The `interact` function from `ipywidgets` will bind the input widgets to the analysis function, causing recalculations and plot updates on input changes.
```python
# Main analysis function to be linked with interact
@interact(
    s0=s0_input,
    T=T_input,
    r=r_input,
    current_t=current_t_input,
    current_st=current_st_input,
    dividends_str=dividends_input,
    costs_str=costs_input
)
def main_analysis(s0, T, r, current_t, current_st, dividends_str, costs_str):
    # This entire block will run whenever an interactive input changes.
    # It wraps the validation, calculation, and plotting functions.
    
    clear_output(wait=True) # Clear previous output for interact

    try:
        validate_inputs(s0, T, r, current_t, current_st)
        dividends = parse_cash_flows(dividends_str, "dividends")
        costs = parse_cash_flows(costs_str, "costs")

        # --- Calculations ---
        display(Markdown("### Calculated Values:"))
        
        # F0(T) with costs/benefits
        F0_T_with_cb = calculate_forward_price_at_inception(s0, r, T, dividends, costs)
        display(Markdown(f"**Forward Price at Inception (With Costs/Benefits):** $F_0(T) = {F0_T_with_cb:.2f}$"))

        # F0(T) without costs/benefits (for comparison in trend plot)
        F0_T_no_cb = calculate_forward_price_at_inception(s0, r, T, [], [])
        display(Markdown(f"**Forward Price at Inception (Without Costs/Benefits):** $F_0(T) = {F0_T_no_cb:.2f}$"))
        
        # MTM at current_t
        mtm_long_position = calculate_mtm_value(current_st, F0_T_with_cb, r, T, current_t, dividends, costs, 'long')
        mtm_short_position = calculate_mtm_value(current_st, F0_T_with_cb, r, T, current_t, dividends, costs, 'short')
        display(Markdown(f"**MTM Value at Current Time $t={current_t}$ (Long Position):** $V_t(T) = {mtm_long_position:.2f}$"))
        display(Markdown(f"**MTM Value at Current Time $t={current_t}$ (Short Position):** $V_t(T) = {mtm_short_position:.2f}$"))

        # --- Visualizations ---
        display(Markdown("### Visualizations:"))
        
        # Trend Plot
        plot_mtm_trend(s0, T, r, F0_T_with_cb, F0_T_no_cb, dividends, costs)

        # Relationship Plot
        plot_forward_price_sensitivity(s0, T, r, dividends, costs)

        # Aggregated Comparison
        plot_scenario_comparison(s0, T, r)

    except (ValueError, TypeError) as e:
        display(Markdown(f"<span style='color:red'>**Input Error:** {e}</span>"))
    ```

## 4. Additional Notes or Instructions

### Assumptions
*   **Discrete Compounding:** All calculations assume discrete compounding of interest rates, consistent with the provided formulas.
*   **Constant Risk-Free Rate:** The risk-free rate ($r$) is assumed to be constant over the entire life of the contract for simplicity.
*   **Discrete Cash Flows:** Costs and benefits are modeled as discrete cash flows occurring at specific points in time, rather than continuous yields.
*   **Spot Price Evolution (for Trend Plot):** For the MTM Trend Plot, the evolution of the underlying spot price ($S_t$) over time is modeled using a simplified linear growth path. In real-world scenarios, this would be stochastic.
*   **No Transaction Costs:** All pricing and valuation assume no transaction costs or taxes.

### Customization Instructions
*   **Modifying Inputs:** Use the interactive sliders, text boxes, and text areas at the top of the notebook to adjust `initial_spot_price` ($S_0$), `maturity_T` ($T$), `risk_free_rate` ($r$), `current_time_t` ($t$), and `current_spot_price_St` ($S_t$).
*   **Adding/Editing Cash Flows:** For dividends and costs, edit the `Textarea` widgets. Ensure the input adheres to the specified JSON list format: `[{"amount": X, "time_from_t0": Y}, {"amount": X2, "time_from_t0": Y2}]`.
*   **Interpreting Plots:** Each plot includes clear titles, axis labels, and legends to guide interpretation. Pay attention to how the "With C/B" (Costs/Benefits) lines differ from "No C/B" to understand their impact.
*   **Extending Scenarios:** The `plot_scenario_comparison` function can be modified in its code cell to define additional `scenario_data` entries for further comparative analysis.

### References

*   [1] `Pricing and Valuation of Forward Contracts with Additional Costs or Benefits`, [Derivatives Pricing and Valuation of Forward Contracts and for an Underlying with Varying Maturities], provided document, page 10. This section and Equation 6 explain how costs and benefits influence the forward price.
*   [2] Example 4: `Hightest Equity Forward Valuation`, [Derivatives Pricing and Valuation of Forward Contracts and for an Underlying with Varying Maturities], provided document, page 11. This example demonstrates calculating MTM value with dividends.
*   [3] Exhibits 3, 4, and 5, [Derivatives Pricing and Valuation of Forward Contracts and for an Underlying with Varying Maturities], provided document, pages 7-9. These exhibits illustrate the value of forward contracts over time.
*   [4] Equation 7, `Pricing and Valuation of Forward Contracts with Additional Costs or Benefits` section, [Derivatives Pricing and Valuation of Forward Contracts and for an Underlying with Varying Maturities], provided document, page 11. This equation gives the general MTM valuation for forward contracts with costs and benefits.

