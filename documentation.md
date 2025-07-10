id: 686eaba0696078dbb169ed40_documentation
summary: Derivative Pricing and Valuation of Forward  Contracts and for an Underlying  with Varying Maturities Documentation
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# Exploring Financial Derivatives: FRA Settlement & APR Conversion with Streamlit

## Introduction to QuLab: Derivative Pricing and Valuation
Duration: 05:00

Welcome to QuLab, an interactive Streamlit application designed to demystify complex financial derivatives, specifically focusing on **Forward Rate Agreements (FRAs)** and **Annual Percentage Rate (APR) conversions**. This codelab will guide you through the architecture, core functionalities, and underlying financial logic of the application, empowering you to understand, run, and even extend its capabilities.

### Why is this application important?

Understanding financial derivatives, particularly FRAs, is crucial for anyone involved in finance, risk management, or quantitative analysis. FRAs are vital tools for hedging against interest rate fluctuations, allowing market participants to lock in future borrowing or lending rates. Similarly, accurately converting APRs with different compounding frequencies is fundamental for comparing financial products and making sound investment or lending decisions.

This application makes these theoretical concepts tangible by:
*   **Providing a hands-on simulator for FRAs:** Users can manipulate parameters and observe real-time calculations and visualizations of cash settlements. This helps in grasping how FRAs function as a hedge and how market rates influence their value.
*   **Simplifying APR conversions:** It demonstrates the mathematical relationship between APRs compounded at different frequencies, an essential skill for accurate financial analysis.
*   **Showcasing Streamlit's power:** For developers, this codelab also highlights how Streamlit can be used to rapidly build interactive, data-driven web applications for financial modeling and education, without needing extensive front-end development knowledge.

### Concepts Explained

*   **Forward Rate Agreement (FRA):** An OTC derivative contract that allows parties to lock in an interest rate for a future period. It's used to hedge against interest rate risk. Key terms include Notional Principal, Fixed Rate (IFR), Market Reference Rate (MRR), Start Period (A), and End Period (B).
*   **Cash Settlement:** FRAs are cash-settled, meaning no exchange of principal occurs. Instead, a net payment is made at the settlement date based on the difference between the agreed fixed rate and the prevailing market rate, discounted to present value.
*   **Annual Percentage Rate (APR):** The annual rate charged for borrowing or earned through an investment, expressed as a single percentage number. Its effective value depends heavily on its compounding frequency.
*   **Compounding Frequency:** The number of times interest is calculated and added to the principal within a year. Different compounding frequencies (e.g., monthly, quarterly, semi-annually) lead to different effective interest rates for the same nominal APR.

By the end of this codelab, you will have a solid understanding of these financial instruments and how they are modeled in a practical application.

## Setting up Your Development Environment
Duration: 03:00

To get started, you'll need Python and Streamlit installed. We'll assume you have Git for cloning the repository.

### Prerequisites

*   Python 3.8+
*   pip (Python package installer)
*   Git

### Steps

1.  **Clone the Repository (Simulated):**
    In a real scenario, you would clone the repository containing the Streamlit application. For this codelab, imagine you have a project structure similar to the one provided. Create the necessary files and directories as shown in the application structure below.

    <aside class="positive">
    <b>Tip:</b> If you are following along locally, create a directory for your project, then create the `application_pages` subdirectory within it. Copy the provided Python code into the respective files.
    </aside>

2.  **Install Dependencies:**
    Navigate to your project directory in the terminal and install the required Python packages.

    ```bash
    pip install streamlit pandas numpy plotly
    ```

    <aside class="positive">
    <b>Note:</b> Streamlit will automatically handle dependencies for its components, but it's good practice to explicitly list all necessary libraries like `pandas`, `numpy`, and `plotly` which are used for data handling and visualizations.
    </aside>

## Understanding the Application Architecture
Duration: 07:00

The application follows a modular structure, leveraging Streamlit's multi-page capabilities. This approach keeps the code organized and makes it easier to manage different functionalities.

### Project Structure

```
.
├── app.py
└── application_pages/
    ├── __init__.py  (Can be an empty file)
    ├── fra_settlement.py
    └── apr_conversion.py
```

### `app.py`: The Main Entry Point

`app.py` is the primary script that Streamlit runs. It sets up the page configuration, displays the main title and introduction, and handles navigation between the different functional pages.

```python
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
```

**Key takeaways from `app.py`:**
*   `st.set_page_config`: Configures the Streamlit page title and layout.
*   `st.sidebar.image` and `st.sidebar.divider`: Customize the sidebar appearance.
*   `st.title` and `st.markdown`: Used for the main heading and rich text content, including an extensive overview of FRA concepts with LaTeX formatting.
*   `st.sidebar.selectbox`: This is the core navigation mechanism. When a user selects an option from the dropdown, `app.py` dynamically imports and calls the corresponding page function (`run_fra_settlement_page` or `run_apr_conversion_page`). This ensures only the code for the active page is executed, optimizing performance.

### `application_pages/` Directory

This directory holds the individual Python scripts for each distinct functionality. Each script defines a function (e.g., `run_fra_settlement_page`) that encapsulates all the Streamlit UI and logic for that specific page. This modularity makes the application scalable and maintainable.

## Deep Dive: FRA Settlement Simulator
Duration: 15:00

The `fra_settlement.py` script implements the Forward Rate Agreement (FRA) Settlement Simulator. It's an interactive tool that allows users to configure various FRA terms and observe real-time calculations.

### `application_pages/fra_settlement.py` Code

```python
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def run_fra_settlement_page():
    st.header("Forward Rate Agreement (FRA) Settlement Simulator")
    st.markdown(\"\"\"

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

    st.markdown("")
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

    st.markdown("")
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
```

### Functionality Breakdown

1.  **User Inputs (`st.sidebar`):**
    *   **FRA Term Sheet:** `st.number_input` and `st.slider` widgets are used for `Notional Principal`, `Fixed Rate (IFR)`, `Start Period (A)`, `End Period (B)`, and `Days in Year Basis`. These allow users to define the core terms of the FRA.
    *   **Market Rate Simulation:** A `st.slider` for `Market Reference Rate (MRR)` enables simulating different market conditions at settlement. All inputs include `help` tooltips for clarity.

2.  **Core Calculations:**
    The application performs a series of sequential calculations to determine the FRA settlement amount.
    *   **Period Fraction:** Calculates the duration of the interest period as a fraction of a year.
        $$ \text{Period Fraction} = \frac{\text{End Period (B)} - \text{Start Period (A)}}{12} $$
    *   **Fixed Interest Payment:** The interest due based on the Notional Principal and the agreed Fixed Rate.
        $$ \text{Fixed Interest Payment} = \text{Notional Principal} \times \text{Fixed Rate} \times \text{Period Fraction} $$
    *   **Floating Interest Payment:** The interest that would be paid if borrowing at the Market Reference Rate.
        $$ \text{Floating Interest Payment} = \text{Notional Principal} \times \text{MRR} \times \text{Period Fraction} $$
    *   **Net Payment at Maturity (undiscounted):** The difference between floating and fixed interest payments. This is the amount that would be exchanged at the end of the interest period (time B).
        $$ \text{Net Payment} = (\text{MRR}_{B-A} - \text{IFR}_{A,B-A}) \times \text{Notional Principal} \times \text{Period Fraction} $$
    *   **Cash Settlement (Present Value):** Since FRAs are typically settled at the start of the interest period (time A) but based on rates observed then, this net payment is discounted back from time B to time A using the Market Reference Rate.
        $$ \text{Cash Settlement (PV)} = \frac{\text{Net Payment}}{1 + \text{MRR}_{B-A} \times \text{Period Fraction}} $$
    *   Input validations are included using `st.error` to prevent invalid period durations or discount factors.

3.  **Narrative Interpretation:**
    Based on the comparison of the `Market Reference Rate` and the `Fixed Rate`, the application provides a clear explanation of which party (fixed-rate payer or receiver) benefits and the direction of the net payment. This makes the financial implications intuitive.

4.  **Visualizations (Plotly):**
    *   **Bar Chart (Aggregated Comparison):** `plotly.express.bar` is used to visually compare the `Fixed Interest Payment`, `Floating Interest Payment`, and the resulting `Net Payment`. This provides a quick overview of the interest cash flows.
    *   **Line Chart (Cash Settlement vs. Market Reference Rate):** This `plotly.express.line` chart shows the sensitivity of the `Cash Settlement (PV)` to a range of `Market Reference Rates`. It includes vertical and horizontal lines to highlight the `Fixed Rate (IFR)` and the `Zero Settlement` point, demonstrating how the FRA's value changes with market conditions and where it effectively neutralizes risk.

### Financial Flow Diagram for FRA Settlement

```mermaid
graph TD
    A[FRA Inception] --> B{Set Parameters: Notional, Fixed Rate (IFR), Start/End Period};
    B --> C[Settlement Date (Time A)];
    C --> D{Observe Market Reference Rate (MRR)};
    D --> E[Calculate Period Fraction: (B-A)/12];
    E --> F[Calculate Fixed Interest Payment];
    E --> G[Calculate Floating Interest Payment];
    F & G --> H[Calculate Net Payment (Undiscounted): Floating - Fixed];
    H --> I[Discount Net Payment to PV using MRR];
    I --> J[Cash Settlement (Present Value)];
    J --> K{Interpret Payment Direction based on MRR vs IFR};
    K --> L[Visualize Payments & Sensitivity];
```

## Deep Dive: APR Conversion Utility
Duration: 08:00

The `apr_conversion.py` script provides a utility for converting Annual Percentage Rates (APR) between different compounding frequencies. This is crucial for comparing financial products on an 'apples-to-apples' basis.

### `application_pages/apr_conversion.py` Code

```python
import streamlit as st
import math

def run_apr_conversion_page():
    st.header("Annual Percentage Rate (APR) Conversion Utility")
    st.markdown(\"\"\"
This utility helps you convert Annual Percentage Rates (APR) between different compounding frequencies.
Ensuring rates are on a comparable compounding basis is crucial for accurate financial analysis and calculations.

### Formula for APR Conversion

The relationship between two equivalent APRs with different compounding frequencies is given by:

$$ \\left(1 + \\frac{APR_m}{m}\\right)^m = \\left(1 + \\frac{APR_n}{n}\\right)^n $$

Where:
- $APR_m$: Original Annual Percentage Rate compounded $m$ times per year.
- $m$: Original number of compounding periods per year.
- $APR_n$: Target Annual Percentage Rate compounded $n$ times per year.
- $n$: Target number of compounding periods per year.

To convert $APR_m$ (compounded $m$ times a year) to $APR_n$ (compounded $n$ times a year), the formula is rearranged to solve for $APR_n$:

$$ APR_n = n \\times \\left( \\left(1 + \\frac{APR_m}{m}\\right)^{\\frac{m}{n}} - 1 \\right) $$
\"\"\")

    st.sidebar.header("APR Conversion Inputs")

    original_apr = st.sidebar.number_input(
        "Original APR (e.g., 0.06 for 6%)",
        min_value=0.0,
        value=0.06,
        step=0.0001,
        format="%.4f",
        help="The Annual Percentage Rate to convert."
    )
    original_compounding_freq = st.sidebar.number_input(
        "Original Compounding Frequency (m)",
        min_value=1,
        value=2, # Semi-annual
        step=1,
        help="The number of times per year the original APR is compounded."
    )
    target_compounding_freq = st.sidebar.number_input(
        "Target Compounding Frequency (n)",
        min_value=1,
        value=12, # Monthly
        step=1,
        help="The number of times per year for the target APR compounding."
    )

    st.subheader("Conversion Results")

    if original_compounding_freq <= 0 or target_compounding_freq <= 0:
        st.error("Error: Compounding frequencies must be positive integers.")
        return

    # Calculate the equivalent effective annual rate first for robustness
    # (1 + APR_m/m)^m = (1 + EAR)
    # EAR = (1 + APR_m/m)^m - 1
    
    # Calculate the target APR
    # APR_n = n * ((1 + EAR)^(1/n) - 1)
    # Substituting EAR: APR_n = n * ((1 + APR_m/m)^(m/n) - 1)

    try:
        # Avoid division by zero if original_compounding_freq is 0
        if original_compounding_freq == 0:
            st.error("Error: Original compounding frequency cannot be zero.")
            return

        # Calculate the base term (1 + APR_m/m)
        base_term = 1 + (original_apr / original_compounding_freq)
        
        # Check for non-positive base to prevent math domain error for fractional powers
        if base_term <= 0:
            st.error("Error: The term (1 + Original APR / Original Compounding Frequency) must be positive.")
            return

        # Calculate the power (m/n)
        power_term = original_compounding_freq / target_compounding_freq

        # Calculate (1 + APR_m/m)^(m/n)
        intermediate_result = base_term ** power_term

        # Calculate APR_n
        target_apr = target_compounding_freq * (intermediate_result - 1)

        st.markdown(f"**Original APR (compounded {original_compounding_freq} times/year):** {original_apr:.4f} ({original_apr:.2%})")
        st.markdown(f"**Target Compounding Frequency (n):** {target_compounding_freq}")
        st.markdown(f"**Equivalent APR (compounded {target_compounding_freq} times/year):** {target_apr:.4f} ({target_apr:.2%})")

    except ZeroDivisionError:
        st.error("Error: Original Compounding Frequency (m) cannot be zero.")
    except ValueError as e:
        st.error(f"Calculation Error: {e}. Please ensure inputs result in valid mathematical operations (e.g., positive base for fractional powers).")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
```

### Functionality Breakdown

1.  **User Inputs (`st.sidebar`):**
    *   `st.number_input` widgets are used for:
        *   `Original APR`: The rate to be converted.
        *   `Original Compounding Frequency (m)`: How many times the original APR compounds per year.
        *   `Target Compounding Frequency (n)`: The desired compounding frequency for the converted APR.
    *   All inputs have `min_value`, `value`, `step`, `format`, and `help` parameters for user-friendliness and validation.

2.  **Core Calculation (APR Conversion Formula):**
    The central part of this utility is the financial formula used for converting APRs between different compounding frequencies. The script directly implements the formula:

    $$ APR_n = n \times \left( \left(1 + \frac{APR_m}{m}\right)^{\frac{m}{n}} - 1 \right) $$

    Where:
    *   $APR_m$: Original Annual Percentage Rate
    *   $m$: Original compounding frequency
    *   $APR_n$: Target Annual Percentage Rate
    *   $n$: Target compounding frequency

    The calculation steps are clearly broken down in the Python code:
    *   `base_term = 1 + (original_apr / original_compounding_freq)`
    *   `power_term = original_compounding_freq / target_compounding_freq`
    *   `intermediate_result = base_term ** power_term`
    *   `target_apr = target_compounding_freq * (intermediate_result - 1)`

    Robust error handling using `try-except` blocks is implemented to catch potential issues like division by zero or mathematical domain errors (e.g., taking the root of a non-positive number).

3.  **Display Results:**
    The calculated `target_apr` is displayed prominently using `st.markdown`, showing both its decimal and percentage format for easy comprehension.

## Running and Experimenting with the Application
Duration: 05:00

Now that you understand the structure and functionality, let's run the application and explore its features.

### How to Run

1.  **Navigate to your project directory** in the terminal where `app.py` is located.
2.  **Run the Streamlit application** using the following command:

    ```bash
    streamlit run app.py
    ```

    This command will open the application in your default web browser (usually at `http://localhost:8501`).

### Experimenting with the FRA Settlement Simulator

1.  In the Streamlit app, select "FRA Settlement Simulator" from the sidebar navigation.
2.  **Adjust the "Notional Principal":** See how scaling the principal scales the settlement amount.
3.  **Change the "Fixed Rate (IFR)":** Observe how your locked-in rate affects the payment direction when compared to the market rate.
4.  **Vary the "Market Reference Rate (MRR)":**
    *   Drag the MRR slider above the Fixed Rate. Notice how the "Net Payment" becomes positive (you receive money), demonstrating the hedging benefit for a fixed-rate payer in a rising rate environment.
    *   Drag the MRR slider below the Fixed Rate. Observe the "Net Payment" becoming negative (you pay money), as your fixed rate was higher than the market rate.
    *   Set MRR equal to the Fixed Rate. The Net Payment should be zero.
5.  **Modify "Start Period" and "End Period":** See how the "Period Fraction" changes and its impact on all calculated values.
6.  **Analyze the Visualizations:**
    *   The bar chart immediately shows the relative magnitudes of fixed, floating, and net payments.
    *   The line chart is crucial for understanding sensitivity. Notice how the cash settlement linearly changes with MRR. The red dashed line (Fixed Rate) always corresponds to the zero settlement point, illustrating that if the MRR equals your fixed rate, the FRA results in no net payment.

### Experimenting with the APR Conversion Utility

1.  In the Streamlit app, select "APR Conversion Utility" from the sidebar navigation.
2.  **Input an "Original APR"** (e.g., 0.05 for 5%).
3.  **Set "Original Compounding Frequency (m)"** (e.g., 12 for monthly).
4.  **Set "Target Compounding Frequency (n)"** (e.g., 1 for annually).
    *   Observe the "Equivalent APR" for annual compounding. It should be slightly higher than 5% due to the effect of compounding.
5.  **Try different combinations:**
    *   Convert from annual (m=1) to quarterly (n=4).
    *   Convert from daily (m=365) to semi-annual (n=2).
    *   Notice how the equivalent APR changes based on the compounding frequency. The more frequent the compounding, the lower the nominal APR needs to be to achieve the same effective annual rate.

## Conclusion and Next Steps
Duration: 02:00

Congratulations! You have successfully navigated through the QuLab Streamlit application, gaining insights into Forward Rate Agreement settlement mechanisms and Annual Percentage Rate conversions. You've seen how Streamlit empowers rapid development of interactive financial tools, making complex concepts accessible and understandable.

### Key Learnings

*   **FRA Mechanics:** You now understand the key components of an FRA, how net payments are calculated, and how discounting to present value is applied.
*   **APR Conversion:** You've grasped the formula for converting APRs between different compounding frequencies and the importance of this conversion for financial comparisons.
*   **Streamlit Development:** You've seen practical examples of Streamlit widgets, layout, data display, and integration with powerful visualization libraries like Plotly.
*   **Modular Application Design:** The use of separate page files (`.py` modules) demonstrates a clean and scalable approach for building multi-functional Streamlit applications.

### Potential Enhancements and Further Exploration

This application serves as a solid foundation. Here are some ideas for future enhancements:

1.  **Add more derivative types:** Implement simulators for options, futures, or swaps.
2.  **Advanced FRA features:**
    *   Include different day count conventions (Actual/Actual, Actual/360, etc.) explicitly instead of just `Days in Year Basis`.
    *   Allow users to input a yield curve for more realistic discounting.
    *   Simulate a series of FRAs as part of a larger hedging strategy.
3.  **Risk Scenarios for FRA:** Add a Monte Carlo simulation for MRR to estimate potential gains/losses.
4.  **APR Conversion Improvements:** Add a visualization to compare the effective annual rates for different compounding frequencies.
5.  **User Authentication:** For a production-ready application, implement user login and data persistence.
6.  **Deployment:** Deploy the application to a cloud platform like Streamlit Community Cloud, Heroku, or AWS.

We encourage you to experiment with the code, modify existing features, and add new ones. This hands-on approach is the best way to solidify your understanding of both financial derivatives and Streamlit development.


© 2025 QuantUniversity. All Rights Reserved.
The purpose of this demonstration is solely for educational use and illustration. Any reproduction of this demonstration requires prior written consent from QuantUniversity. This lab was generated using the QuCreate platform. QuCreate relies on AI models for generating code, which may contain inaccuracies or errors.
