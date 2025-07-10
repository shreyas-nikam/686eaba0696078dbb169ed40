# Technical Specification for Jupyter Notebook: Forward Rate Agreement (FRA) Settlement Simulator

## 1. Notebook Overview

This Jupyter Notebook serves as an interactive educational tool to explore the intricacies of Forward Rate Agreements (FRAs). It allows users to define FRA terms, simulate market rate changes, and observe the resulting net payment and cash settlement calculations. By providing a hands-on experience, the notebook aims to clarify the mechanics and applications of FRAs in interest rate risk management.

### Learning Goals

Upon completing this lab, users will be able to:
-   Explain how Forward Rate Agreements (FRAs) function as Over-The-Counter (OTC) derivatives for managing interest rate exposure.
-   Understand the fundamental components of an FRA, including the notional principal, fixed rate (Implied Forward Rate), floating rate (Market Reference Rate), and the contract period.
-   Calculate the net payment at the end of the interest period and its present value (cash settlement) at the beginning of the period, based on the fixed rate and the market reference rate at settlement.
-   Explore the relationship between implied forward rates and the fixed rates in FRAs.
-   Convert annual percentage rates (APR) for different compounding frequencies, understanding its importance in financial calculations.

### Expected Outcomes

Users will:
-   Gain practical experience in setting up and simulating FRA scenarios.
-   Visually analyze the impact of varying market reference rates on FRA settlement.
-   Develop a deeper understanding of interest rate derivative mechanics.
-   Be proficient in converting interest rates across different compounding bases.

## 2. Mathematical and Theoretical Foundations

This section will introduce the core concepts and formulas essential for understanding and calculating FRA settlements. All rates are assumed to be expressed as decimals (e.g., 5% as 0.05).

### 2.1 Forward Rate Agreement (FRA) Fundamentals

A Forward Rate Agreement (FRA) is an OTC derivative contract between two parties that determines an interest rate to be paid on a notional principal at a future date. It allows parties to lock in an interest rate for a future period, hedging against adverse interest rate movements. No principal amount is exchanged; only the net difference in interest payments is settled.

-   $IFR_{A,B-A}$: The *Implied Forward Rate* (also referred to as the fixed rate or contract rate), agreed upon at the inception of the FRA ($t=0$). It represents the agreed-upon interest rate for the period from A to B.
-   $MRR_{B-A}$: The *Market Reference Rate* (or floating rate), observed at the settlement date ($t=A$). This is typically a benchmark rate like LIBOR or SOFR for the period from A to B.
-   Notional Principal: The agreed-upon principal amount on which interest payments are calculated. This amount is never exchanged.
-   Period Fraction: The fraction of a year corresponding to the interest period ($B-A$). It is commonly calculated as $\text{Days in Period} / 360$ or $\text{Days in Period} / 365$. For simplicity and alignment with common market conventions (e.g., money market instruments), this notebook will primarily use a `Days / 360` convention, or `(B-A months) / 12` if periods are specified in months.

### 2.2 Net Payment Calculation

The net payment of an FRA is the difference between the floating interest payment and the fixed interest payment. It is calculated at the end of the interest period ($t=B$) but typically settled (paid) at the beginning of the interest period ($t=A$).

The formula for the Net Payment, from the perspective of the fixed-rate payer (who receives floating and pays fixed), is:

$$ \text{Net Payment} = (MRR_{B-A} - IFR_{A,B-A}) \times \text{Notional Principal} \times \text{Period Fraction} $$

-   If $MRR_{B-A} > IFR_{A,B-A}$, the fixed-rate payer receives a net payment.
-   If $MRR_{B-A} < IFR_{A,B-A}$, the fixed-rate payer makes a net payment (represented as a negative value).

This formula directly applies the concept from [1, p.23]. The "Period Fraction" is crucial for annualizing rates to match the specific duration of the FRA's interest period. For instance, if the period is 3 months and a 360-day basis is used, Period Fraction would be $90/360 = 0.25$.

### 2.3 Cash Settlement (Present Value)

Although the net payment is conceptually calculated at the end of the interest period ($t=B$), FRAs are typically cash-settled (i.e., the payment is made) at the *beginning* of the interest period ($t=A$). Therefore, the calculated Net Payment must be discounted back to the settlement date ($t=A$) using the Market Reference Rate for the period ($MRR_{B-A}$).

The formula for the Cash Settlement (Present Value) at $t=A$ is:

$$ \text{Cash Settlement (PV)} = \frac{\text{Net Payment}}{1 + MRR_{B-A} \times \text{Period Fraction}} $$

This present value calculation ensures that the payment reflects its value at the actual settlement date, as described in [1, p.23].

### 2.4 Annual Percentage Rate (APR) Conversion

Financial instruments often quote interest rates with different compounding frequencies (e.g., semi-annual, quarterly, monthly, annual). To compare or combine rates, it's essential to convert them to a consistent compounding basis. The APR conversion formula relates two Annual Percentage Rates ($APR_m$ and $APR_n$) with different compounding frequencies ($m$ and $n$ periods per year, respectively):

$$ \left(1 + \frac{APR_m}{m}\right)^m = \left(1 + \frac{APR_n}{n}\right)^n $$

This formula, derived from equating the effective annual rates of two different compounding frequencies, is critical for aligning rates in FRA calculations and other financial analyses [1, p.21, Equation 12].

-   $APR_m$: The known annual rate compounded $m$ times per year.
-   $m$: The number of compounding periods per year for $APR_m$.
-   $APR_n$: The annual rate we want to find, compounded $n$ times per year.
-   $n$: The target number of compounding periods per year for $APR_n$.

## 3. Code Requirements

### 3.1 Expected Libraries

The notebook will utilize the following open-source Python libraries:
-   `numpy`: For numerical operations, especially array manipulations and mathematical functions.
-   `pandas`: For structured data handling, particularly for creating tables to display results or for generating data for visualizations.
-   `matplotlib.pyplot`: For creating static and dynamic plots and charts.
-   `seaborn`: Built on matplotlib, provides a high-level interface for drawing attractive and informative statistical graphics.
-   `ipywidgets`: To create interactive elements like sliders, dropdowns, and text inputs for user-defined parameters, enabling dynamic simulations.

### 3.2 Input/Output Expectations

#### Inputs (User-Configurable via `ipywidgets`):

1.  **FRA Term Sheet Inputs**:
    -   `Notional Principal` (float, e.g., $1,000,000): The nominal amount of the agreement.
    -   `Fixed Rate (IFR_A,B-A)` (float, as decimal, e.g., $0.025$ for 2.5%): The implied forward rate agreed upon at inception.
    -   `Start Period A` (int, in months, e.g., 3): The number of months from today when the forward rate period begins.
    -   `End Period B` (int, in months, e.g., 6): The number of months from today when the forward rate period ends. `B` must be greater than `A`.
    -   `Days in Year Basis` (int, e.g., 360 or 365): Convention for calculating Period Fraction.

2.  **Market Rate Simulation Input**:
    -   `Market Reference Rate (MRR_B-A) at Settlement` (float, as decimal, e.g., $0.028$ for 2.8%): A slider or text input allowing users to vary this rate to observe its impact on settlement. This will represent the `MRR` observed at time $A$.

3.  **APR Conversion Utility Inputs**:
    -   `APR to Convert` (float, as decimal): The initial Annual Percentage Rate.
    -   `Current Compounding Frequency (m)` (dropdown/int): Number of compounding periods per year (e.g., 1 for annual, 2 for semi-annual, 4 for quarterly, 12 for monthly).
    -   `Target Compounding Frequency (n)` (dropdown/int): Desired number of compounding periods per year.

#### Outputs:

1.  **Calculated FRA Settlement**:
    -   `Period Duration` (in months).
    -   `Period Fraction` (calculated from Start Period, End Period, and Days in Year Basis).
    -   `Fixed Interest Payment` (for visualization).
    -   `Floating Interest Payment` (for visualization).
    -   `Net Payment` (float, in currency units).
    -   `Cash Settlement (PV)` (float, in currency units).
2.  **Converted APR Value**:
    -   `Converted APR` (float, as decimal/percentage).
3.  **Visualizations**: Charts and plots as specified below.

### 3.3 Algorithms or Functions to be Implemented

1.  **`calculate_period_fraction(start_month, end_month, days_in_year_basis)`**:
    -   Input: `start_month` (int), `end_month` (int), `days_in_year_basis` (int).
    -   Calculates the number of days in the period `(end_month - start_month) * (days_in_year_basis / 12)`.
    -   Returns: `period_fraction` (float) calculated as `days_in_period / days_in_year_basis`.
2.  **`calculate_fra_net_payment(mrr, ifr, notional_principal, period_fraction)`**:
    -   Input: `mrr` (float), `ifr` (float), `notional_principal` (float), `period_fraction` (float).
    -   Implements the Net Payment formula.
    -   Returns: `net_payment` (float).
3.  **`calculate_fra_cash_settlement(net_payment, mrr, period_fraction)`**:
    -   Input: `net_payment` (float), `mrr` (float), `period_fraction` (float).
    -   Implements the Cash Settlement (PV) formula.
    -   Returns: `cash_settlement_pv` (float).
4.  **`convert_apr_frequency(apr_m, m, n)`**:
    -   Input: `apr_m` (float), `m` (int), `n` (int).
    -   Implements the APR Conversion formula to solve for `APR_n`.
    -   Returns: `apr_n` (float).

### 3.4 Logical Flow (Jupyter Cells)

The notebook will follow a clear, sequential structure:

#### Cell 1: Markdown - Notebook Title and Introduction
-   H1: "Forward Rate Agreement (FRA) Settlement Simulator"
-   Brief overview of the notebook's purpose.
-   Learning Goals and Expected Outcomes.

#### Cell 2: Code - Library Imports and Configuration
-   Import `numpy`, `pandas`, `matplotlib.pyplot` (as `plt`), `seaborn`, `ipywidgets` (as `widgets`), `IPython.display` (as `display`).
-   Set `seaborn` style and `matplotlib` font sizes for better readability (e.g., `plt.rcParams.update({'font.size': 12})`).
-   Define a color-blind-friendly palette.

#### Cell 3: Markdown - Mathematical and Theoretical Foundations
-   H2: "Mathematical and Theoretical Foundations"
-   Detailed explanations of FRAs, their components, and how they function.
-   Presentation of Net Payment formula using `$$...$$` LaTeX formatting, with inline explanations for variables using `$...$`.
-   Presentation of Cash Settlement (PV) formula using `$$...$$` LaTeX formatting, with inline explanations for variables.
-   Presentation of APR Conversion formula using `$$...$$` LaTeX formatting, with inline explanations for variables.
-   Contextual information regarding `Period Fraction` calculation (e.g., assuming 360-day year basis for default, deriving from start/end months).

#### Cell 4: Code - Core Calculation Functions
-   Implement the Python functions: `calculate_period_fraction`, `calculate_fra_net_payment`, `calculate_fra_cash_settlement`, and `convert_apr_frequency`.
-   Include docstrings and comments for each function explaining its purpose, arguments, and return values.

#### Cell 5: Markdown - Interactive FRA Settlement Simulation
-   H2: "Interactive FRA Settlement Simulation"
-   Explanation of the interactive inputs for the FRA term sheet and market rate simulation.
-   Instructions on how to use the widgets.

#### Cell 6: Code - Interactive FRA Parameter Inputs and Display
-   Define `ipywidgets` for:
    -   `notional_principal_widget`: Slider or `FloatText` (e.g., default 1,000,000, min 100,000, max 10,000,000).
    -   `fixed_rate_widget`: Slider or `FloatText` (e.g., default 0.025, min 0.005, max 0.05, step 0.0001).
    -   `start_period_widget`: `IntSlider` (e.g., default 3, min 0, max 12, step 1, label "Start Period (months from now) A").
    -   `end_period_widget`: `IntSlider` (e.g., default 6, min 1, max 24, step 1, label "End Period (months from now) B").
    -   `days_in_year_basis_widget`: `Dropdown` (options: [360, 365], default 360).
    -   `mrr_at_settlement_widget`: `FloatSlider` (e.g., default 0.028, min 0.005, max 0.05, step 0.0001, label "Market Reference Rate (MRR) at Settlement").
-   Create an `interactive` function `simulate_fra_settlement(notional_principal, fixed_rate, start_period, end_period, days_in_year_basis, mrr_at_settlement)` that:
    -   Validates inputs (e.g., `end_period > start_period`).
    -   Calculates `period_duration_months = end_period - start_period`.
    -   Calls `calculate_period_fraction`.
    -   Calls `calculate_fra_net_payment`.
    -   Calls `calculate_fra_cash_settlement`.
    -   Prints/displays the calculated results in a clear, formatted manner.
-   Display the interactive widgets.
-   Provide inline help text for each control (`description` argument in `ipywidgets`).

#### Cell 7: Markdown - APR Conversion Utility
-   H2: "APR Conversion Utility"
-   Explanation of the utility's purpose and how to use it.

#### Cell 8: Code - Interactive APR Conversion
-   Define `ipywidgets` for:
    -   `apr_to_convert_widget`: `FloatText` (e.g., default 0.05).
    -   `current_m_widget`: `Dropdown` (options: [1, 2, 4, 12, 365], labels: ['Annual (1)', 'Semi-Annual (2)', 'Quarterly (4)', 'Monthly (12)', 'Daily (365)'], default 1).
    -   `target_n_widget`: `Dropdown` (options: [1, 2, 4, 12, 365], labels: ['Annual (1)', 'Semi-Annual (2)', 'Quarterly (4)', 'Monthly (12)', 'Daily (365)'], default 1).
-   Create an `interactive` function `perform_apr_conversion(apr_to_convert, current_m, target_n)` that:
    -   Validates inputs (e.g., `apr_to_convert > 0`).
    -   Calls `convert_apr_frequency`.
    -   Prints/displays the converted APR.
-   Display the interactive widgets.
-   Provide inline help text for each control.

#### Cell 9: Markdown - Visualizations
-   H2: "Visualizations"
-   Explanation of the bar chart: what it shows and its purpose.

#### Cell 10: Code - Aggregated Comparison (Bar Chart)
-   Obtain current `ifr`, `mrr`, `notional_principal`, `period_fraction` from the interactive widgets' current values (or use default values if not running interactively).
-   Calculate `fixed_interest_payment = ifr * notional_principal * period_fraction`.
-   Calculate `floating_interest_payment = mrr * notional_principal * period_fraction`.
-   Calculate `net_payment = floating_interest_payment - fixed_interest_payment`. (Note: perspective is fixed-rate payer, so (Floating - Fixed) as per input context)
-   Create a `pandas.DataFrame` for plotting.
-   Generate a bar chart using `matplotlib.pyplot` or `seaborn`:
    -   X-axis: Categories like "Fixed Interest", "Floating Interest", "Net Payment".
    -   Y-axis: Amount.
    -   Apply color-blind-friendly palette.
    -   Set clear title (e.g., "FRA Interest Payments and Net Settlement").
    -   Label axes clearly.
    -   Ensure font size >= 12pt.
    -   Include a static fallback (save as PNG) if the environment doesn't support interactivity or for documentation.

#### Cell 11: Markdown - Trend Plot Explanation
-   Explanation of the line chart: what it shows and its purpose (how net settlement changes with MRR).

#### Cell 12: Code - Trend Plot (Line Chart)
-   Obtain `ifr`, `notional_principal`, `period_fraction` from the interactive widgets' current values.
-   Generate a range of `mrr_values` (e.g., from `ifr - 0.02` to `ifr + 0.02`).
-   For each `mrr_value` in the range:
    -   Calculate `net_payment` and `cash_settlement_pv` using the defined functions.
-   Create a `pandas.DataFrame` with `MRR`, `Net Payment`, and `Cash Settlement PV`.
-   Generate a line chart using `matplotlib.pyplot` or `seaborn`:
    -   X-axis: `MRR_B-A` (Market Reference Rate).
    -   Y-axis: `Net Settlement Amount` (or both Net Payment and Cash Settlement PV).
    -   Apply color-blind-friendly palette.
    -   Set clear title (e.g., "Impact of Market Reference Rate on FRA Settlement").
    -   Label axes clearly.
    -   Include a legend for multiple lines (if applicable).
    -   Ensure font size >= 12pt.
    -   Enable interactivity (e.g., `plotly` if chosen, but `matplotlib` allows basic zooming).
    -   Include a static fallback (save as PNG).

## 4. Additional Notes or Instructions

### Assumptions:
-   **Day Count Convention**: For `Period Fraction`, the default assumption is `Actual/360`. Users can select between `360` and `365` days in the year basis through the widget. The "Period" for the FRA calculation is derived from `End Period (months) - Start Period (months)`. For example, a 3x6 FRA (3 months starting in 3 months, ending in 6 months from now) has a 3-month period.
-   **Rate Quoting**: All interest rates (IFR, MRR, APR) are assumed to be quoted as annual rates, which are then adjusted by their respective compounding frequencies or period fractions for calculations.
-   **FRA Payer/Receiver**: Calculations are presented from the perspective of the *fixed-rate payer* (who pays fixed and receives floating). If the net payment is negative, the fixed-rate payer makes the payment to the floating-rate payer.

### Constraints:
-   The notebook is designed to execute efficiently on a mid-spec laptop (8 GB RAM) within 5 minutes.
-   Only open-source Python libraries available on PyPI are permitted.
-   No external data files are required; all data is generated dynamically through user input or internal simulation.
-   No deployment steps or platform-specific references (e.g., Streamlit, Dash) are included. The focus is purely on the Jupyter Notebook environment.

### Customization Instructions:
-   **Parameter Exploration**: Users are encouraged to adjust the sliders and input fields to observe how changes in notional principal, fixed rate, period, and especially the market reference rate, affect the FRA settlement.
-   **Code Modification**: Advanced users can explore modifying the Python functions to incorporate different day count conventions, alternative compounding methods (e.g., continuous compounding), or different perspectives (e.g., floating-rate payer).
-   **Visualization Refinement**: Users can customize the plots' appearance (colors, labels, types) using `matplotlib` and `seaborn`'s extensive options.

### References:

[1] Refresher Reading: Derivatives, Pricing and Valuation of Forward Contracts and for an Underlying with Varying Maturities, [Document ID: DerivativesRefresherReading_CFA2024]. This document provides the definition, mechanics, and calculation examples for Forward Rate Agreements.

[2] CFA Institute. (n.d.). Pricing and Valuation of Forward Contracts and for an Underlying with.... Retrieved from https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2025/pricing-valuation-forward-contracts-underlying-varying-maturities.

[3] Examples.com. (n.d.). Pricing and Valuation of Forward Contracts and Forwards - Examples. Retrieved from https://www.examples.com/cfa/pricing-and-valuation-of-forward-contracts-and-forwards.

