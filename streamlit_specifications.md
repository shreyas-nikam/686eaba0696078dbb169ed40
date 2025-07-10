# Streamlit Application Requirements Specification: Forward Rate Agreement (FRA) Settlement Simulator

## 1. Application Overview

*   **Purpose and Objectives**:
    The primary purpose of the Streamlit application is to serve as an interactive educational tool for understanding the mechanics, pricing, and settlement of Forward Rate Agreements (FRAs). It aims to provide users with a dynamic platform to:
    *   Configure various FRA terms and observe how changes in market conditions impact settlement.
    *   Demystify the calculation of net payments and their present value (cash settlement).
    *   Illuminate the critical interplay between the implied forward rate ($IFR_{A,B-A}$) and the market reference rate ($MRR_{B-A}$) at settlement.
    *   Offer a practical utility for converting Annual Percentage Rates (APR) between different compounding frequencies, emphasizing rate consistency in financial calculations.

*   **Target Audience and Use Cases**:
    *   **Target Audience**: Students of finance, aspiring financial analysts, derivative traders, and anyone seeking a deeper, interactive understanding of interest rate derivatives and risk management.
    *   **Use Cases**:
        *   **Interactive Learning**: Students can experiment with FRA parameters to build intuition about their behavior and settlement.
        *   **Scenario Analysis**: Financial practitioners can quickly simulate different market rate scenarios to understand potential profit/loss implications.
        *   **Concept Reinforcement**: Users can directly visualize how FRAs hedge interest rate risk and the cash flow implications for both fixed-rate payers and receivers.
        *   **Rate Consistency Check**: The APR conversion utility aids in ensuring all rates are on a comparable compounding basis for accurate analysis.

*   **Key Value Propositions**:
    *   **Hands-on Experience**: Provides a practical, interactive environment to apply theoretical FRA knowledge.
    *   **Visual Clarity**: Transforms complex financial calculations into intuitive visualizations, enhancing understanding.
    *   **Risk Insight**: Helps users comprehend interest rate risk hedging and the sensitivity of FRA values to market movements.
    *   **Utility**: Integrates a valuable APR conversion tool for broader financial applications.

## 2. User Interface Requirements

*   **Layout and Navigation Structure**:
    *   The application shall feature a clean, intuitive, single-page layout.
    *   A prominent main title "Forward Rate Agreement (FRA) Settlement Simulator" at the top.
    *   An introductory section outlining the "Overview," "Learning Outcomes," "Features," and "How It Explains the Concept" will be displayed at the top, potentially collapsible.
    *   Input controls for FRA parameters and market rate simulation will be organized in a dedicated section (e.g., a sidebar or a distinct column) on the left.
    *   Results, calculations, and visualizations will occupy the main content area on the right.
    *   A separate, clearly delineated section or tab will house the "APR Conversion Utility."
    *   A "References" section will be included at the bottom of the page.

*   **Input Widgets and Controls**:
    *   **FRA Term Sheet Input**:
        *   **Notional Principal**: `st.number_input` with a default of `10,000,000`, minimum of `100,000`, maximum of `100,000,000`, and a step of `100,000`. Inline help: "The principal amount on which interest payments are based."
        *   **Fixed Rate (IFR)**: `st.slider` with a range from `0.00` to `0.10` (0% to 10%), step `0.0001`, and default `0.0525` (5.25%), formatted as a percentage. Inline help: "The implied forward rate ($IFR_{A,B-A}$) agreed at the inception of the FRA."
        *   **Start Period (A)**: `st.number_input` (integer) with a default of `3`, minimum of `0`, maximum of `60`, and step of `1`. Inline help: "Months from today until the FRA's interest period begins (settlement date)."
        *   **End Period (B)**: `st.number_input` (integer) with a default of `6`, minimum of `1`, maximum of `120`, and step of `1`. Inline help: "Months from today until the FRA's interest period ends." This input must be validated such that $B > A$.
        *   **Days in Year Basis**: `st.number_input` (integer) with a default of `360`. Inline help: "The day count convention for annualizing rates (e.g., 360 for 30/360 or 365 for Actual/365)."
    *   **Market Rate Simulation**:
        *   **Market Reference Rate (MRR)**: `st.slider` with a range from `0.01` to `0.10` (1% to 10%), step `0.0001`, and default `0.055` (5.5%), formatted as a percentage. Inline help: "The prevailing market interest rate ($MRR_{B-A}$) observed at the settlement date, used for floating interest calculation and discounting."
    *   **APR Conversion Utility Inputs**:
        *   **Original APR**: `st.number_input` with a default of `0.06` (6%), formatted as a percentage. Inline help: "The Annual Percentage Rate to convert."
        *   **Original Compounding Frequency (m)**: `st.number_input` (integer) with a default of `2` (semi-annual). Inline help: "The number of times per year the original APR is compounded."
        *   **Target Compounding Frequency (n)**: `st.number_input` (integer) with a default of `12` (monthly). Inline help: "The number of times per year for the target APR compounding."
    *   All input widgets shall include clear labels and descriptive inline help text or tooltips as per user requirements.

*   **Visualization Components (charts, graphs, tables)**:
    *   **FRA Simulation Results Display**:
        *   Calculated Period Fraction: Displayed as a formatted number (e.g., `0.2500`).
        *   Calculated Fixed Interest Payment, Floating Interest Payment, Net Payment at Maturity, and Cash Settlement (PV): Displayed as formatted currency amounts (e.g., `$1,250.00`).
        *   A narrative interpretation of the net payment (e.g., who pays whom and why, based on $MRR_{B-A}$ vs. $IFR_{A,B-A}$).
    *   **APR Conversion Results Display**:
        *   Display the calculated equivalent APR at the target compounding frequency as a formatted percentage.

*   **Interactive Elements and Feedback Mechanisms**:
    *   All calculations and visualizations must update dynamically and instantaneously upon any change in user input parameters.
    *   Appropriate error messages (e.g., for `end_month <= start_month`, or `days_in_year_basis = 0`, or invalid discounting factors) should be displayed prominently using `st.error`.
    *   Input sliders and number inputs should provide immediate visual feedback on the selected values.

## 3. Visualization Requirements

*   **Chart Types and Visualization Libraries**:
    *   **Aggregated Comparison (Bar Chart)**:
        *   Purpose: To visually compare the components of the FRA settlement.
        *   Type: Bar chart, generated using `plotly.express.bar`.
        *   Data: Displays "Fixed Interest Payment," "Floating Interest Payment," and "Net Payment."
        *   Coloring: Apply a color-blind-friendly palette. The notebook specifies `lightseagreen` for Fixed, `royalblue` for Floating, and `salmon` for Net Payment, which should be retained.
    *   **Trend Plot (Line Chart)**:
        *   Purpose: To show the sensitivity of the FRA cash settlement to variations in the Market Reference Rate.
        *   Type: Line chart, generated using `plotly.express.line`.
        *   Data: X-axis representing a range of $MRR_{B-A}$ values (e.g., 1% to 10%) and Y-axis representing the corresponding Cash Settlement (PV) amounts.
        *   Markers: Enabled on the line plot points.
    *   **Visualization Library**: Plotly (`plotly.express` and `plotly.graph_objects`) will be exclusively used for interactive charts.

*   **Interactive Visualization Features**:
    *   **Tooltips**: Both charts must display detailed information on hover. For the bar chart, hovering over a bar should show its exact category and amount. For the line chart, hovering over a point should show the exact $MRR_{B-A}$ and Cash Settlement value. `hovermode="x unified"` for the line chart is required.
    *   **Zoom and Pan**: Standard Plotly features for exploring chart details (zooming, panning, resetting view) should be available.

*   **Real-time Updates and Responsiveness**:
    *   Both the bar chart and the line chart, along with all numerical outputs, must update in real-time as users adjust any input parameter. This ensures a highly interactive and responsive user experience.

*   **Annotation and Tooltip Specifications**:
    *   **Titles**: All charts must have clear, descriptive titles prominently displayed (e.g., "Aggregated Comparison: FRA Interest Payments and Net Settlement", "FRA Cash Settlement vs. Market Reference Rate (MRR)"). Titles should be centered.
    *   **Axis Labels**: All axes must be clearly labeled (e.g., "Amount ($)", "Market Reference Rate (MRR)", "Cash Settlement ($)"). Rates should be formatted as percentages on axes.
    *   **Legends**: Legends should be visible and easily understandable, differentiating data series where applicable.
    *   **Line Chart Specific Annotations**:
        *   A vertical dashed line marking the "Fixed Rate ($IFR_{A,B-A}$)" on the MRR axis, with an annotation indicating its value (e.g., "Fixed Rate (IFR): 5.25%").
        *   A horizontal dotted line at $y=0$ (zero settlement) on the Cash Settlement axis, with an annotation (e.g., "Zero Settlement").
    *   **Font Size**: All text within charts, including titles, labels, and annotations, must be easily readable (equivalent to $\ge 12$ pt).

## 4. Mathematical Formula Display

All key financial formulas used in the application, especially in explanatory sections or alongside calculations, must be rendered using proper LaTeX syntax for clarity and accuracy. They will be displayed as follows:

*   **Net Payment**:
    $$ (MRR_{B-A} - IFR_{A,B-A}) \times \text{Notional Principal} \times \text{Period Fraction} $$
    *Inline explanation*: $\text{Period Fraction}$ is typically `Days / 360` or `1 / Number of Periods per year`.

*   **Cash Settlement (Present Value)**:
    $$ \text{Cash Settlement (PV)} = \frac{\text{Net Payment}}{1 + MRR_{B-A} \times \text{Period Fraction}} $$

*   **Annual Percentage Rate (APR) Conversion**:
    The conversion formula is:
    $$ \left(1 + \frac{APR_m}{m}\right)^m = \left(1 + \frac{APR_n}{n}\right)^n $$
    Where:
    *   $IFR_{A,B-A}$: Fixed rate agreed at inception (Implied Forward Rate)
    *   $MRR_{B-A}$: Market Reference Rate observed at settlement
    *   $A$: Start period of the forward rate
    *   $B$: End period of the forward rate
    *   $m, n$: Number of compounding periods per year

    To convert $APR_m$ (compounded $m$ times a year) to $APR_n$ (compounded $n$ times a year), the formula is rearranged to solve for $APR_n$:
    $$ APR_n = n \times \left( \left(1 + \frac{APR_m}{m}\right)^{\frac{m}{n}} - 1 \right) $$