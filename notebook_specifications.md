
# Technical Specification: FX Forward MTM Analyzer Jupyter Notebook

This document outlines the detailed specification for a Jupyter Notebook designed to simulate and analyze the Mark-to-Market (MTM) value of a Foreign Exchange (FX) forward contract. It focuses on the logical flow, necessary markdown explanations, and specific code requirements, adhering strictly to LaTeX formatting for all mathematical content.

---

## 1. Notebook Overview

### Learning Goals
This notebook is designed to help users:
- Understand how FX forward prices are determined based on interest rate differentials, specifically through the application of the covered interest rate parity.
- Analyze the factors affecting the MTM value of an FX forward contract over its life.
- Grasp the concepts of forward premium and discount in FX markets.
- Understand the key insights regarding FX forward valuation as presented in relevant financial literature.

### Expected Outcomes
Upon successful execution and interaction with the notebook, users will:
- Have a clear understanding of the mathematical formulas underlying FX forward pricing and MTM valuation.
- Be able to interactively adjust key parameters and observe their impact on the FX forward MTM.
- Visualize the sensitivity of MTM to changes in interest rate differentials and spot rates through dynamic plots.
- Understand scenarios of gain and loss from both long and short contract positions.

---

## 2. Mathematical and Theoretical Foundations

This section will provide the necessary theoretical background and formulas for understanding FX forward contract valuation.

### Definitions
- **Foreign Exchange (FX) Forward Contract:** An agreement to exchange a specified amount of one currency for another at a predetermined rate (the forward rate) on a future date.
- **Spot FX Rate ($S_{t,f/d}$):** The current exchange rate for immediate delivery. In this notebook, the convention $S_{f/d}$ denotes the number of units of domestic currency ($d$) required to purchase one unit of foreign currency ($f$). For example, if the pair is USD/EUR, $f$ is EUR and $d$ is USD, so $S_{USD/EUR}$ indicates how many USD are equal to 1 EUR.
- **Foreign Risk-Free Rate ($r_f$):** The annualized risk-free interest rate applicable to the foreign currency.
- **Domestic Risk-Free Rate ($r_d$):** The annualized risk-free interest rate applicable to the domestic currency.
- **Contract Maturity ($T$):** The total time (in years) from the contract's inception ($t=0$) until its expiration date.
- **Current Time ($t$):** The elapsed time (in years) since the contract's inception ($0 \le t \le T$).
- **Mark-to-Market (MTM) Value:** The current fair value of a contract, representing the gain or loss if the contract were to be closed out immediately at current market rates.
- **Forward Premium/Discount:** A situation where the forward exchange rate is higher (premium) or lower (discount) than the spot exchange rate, typically reflecting interest rate differentials.

### Formulas
All calculations in this notebook assume continuous compounding for interest rates.

1.  **FX Forward Price (at inception, $t=0$)**
    The theoretical no-arbitrage forward price of an FX forward contract, denoted as $F_{0,f/d}(T)$, is determined by the spot rate and the risk-free interest rate differential between the two currencies. This is based on the covered interest rate parity principle [16].
    $$F_{0,f/d}(T) = S_{0,f/d}e^{(r_f - r_d)T}$$
    Where:
    - $F_{0,f/d}(T)$ is the FX forward price at time $0$ for maturity $T$.
    - $S_{0,f/d}$ is the spot FX rate at time $0$ (domestic per foreign).
    - $r_f$ is the foreign risk-free rate.
    - $r_d$ is the domestic risk-free rate.
    - $T$ is the time to maturity in years.

2.  **Mark-to-Market Value of an FX Forward Contract (Long Position)**
    The value of an FX forward contract at any time $t$ between inception and maturity, $V_t(T)$, for a long position (agreeing to buy the foreign currency at the initial forward rate) is given by [17]:
    $$V_t(T) = S_{t,f/d} - F_{0,f/d}(T)e^{-(r_f - r_d)(T - t)}$$
    Where:
    - $V_t(T)$ is the MTM value of the long FX forward contract at time $t$.
    - $S_{t,f/d}$ is the current spot FX rate at time $t$ (domestic per foreign).
    - $F_{0,f/d}(T)$ is the *original* FX forward price agreed upon at inception.
    - $(T - t)$ is the remaining time to maturity.

3.  **Mark-to-Market Value of an FX Forward Contract (Short Position)**
    For a short position (agreeing to sell the foreign currency at the original forward rate), the MTM value is the negative of the long position's MTM value:
    $$V_t(T)_{short} = F_{0,f/d}(T)e^{-(r_f - r_d)(T - t)} - S_{t,f/d}$$

### Real-World Applications
FX forward contracts are widely used for:
-   **Hedging:** Corporations use forward contracts to lock in an exchange rate for future transactions, thereby mitigating foreign exchange risk. For example, an importer expecting to pay a foreign supplier in 3 months might buy foreign currency forward to fix their cost.
-   **Speculation:** Traders might enter into FX forward contracts if they anticipate specific movements in exchange rates to profit from those movements.
-   **Arbitrage:** If the forward rate deviates from the no-arbitrage price dictated by interest rate parity, sophisticated market participants may engage in arbitrage strategies to profit from the mispricing.

---

## 3. Code Requirements

### Expected Libraries
The notebook will utilize the following open-source Python libraries:
-   `numpy`: For efficient numerical operations, especially exponential calculations for continuous compounding.
-   `pandas`: For data structuring, particularly for creating DataFrames to hold simulation results, which can then be easily plotted.
-   `matplotlib.pyplot`: For creating static plots of MTM sensitivities.
-   `seaborn`: To enhance the aesthetic quality and readability of the plots, including color-blind friendly palettes.
-   `ipywidgets`: To create interactive controls (sliders, dropdowns, text inputs) within the Jupyter environment, allowing users to dynamically change parameters.

### Input/Output Expectations

#### Inputs (Interactive Controls)
The notebook will feature a dedicated section with interactive controls for users to define the FX forward contract parameters. Each control will have inline help text or tooltips.
-   **Currency Pair Selection:** A dropdown menu to select synthetic currency pairs (e.g., "USD/EUR", "ZAR/EUR", "JPY/USD"). Selecting a pair will pre-populate default $S_{0,f/d}$, $r_f$, and $r_d$ values.
-   **Initial Spot FX Rate ($S_{0,f/d}$):** A text input or slider for the spot rate at contract inception.
    -   *Default:* Based on selected currency pair.
    -   *Range:* Realistic range for FX rates (e.g., 0.5 to 2.0 for major pairs, 10 to 200 for others).
-   **Foreign Risk-Free Rate ($r_f$):** A slider for the foreign currency interest rate (annualized).
    -   *Default:* Based on selected currency pair.
    -   *Range:* e.g., -0.01 to 0.10 (-1% to 10%).
-   **Domestic Risk-Free Rate ($r_d$):** A slider for the domestic currency interest rate (annualized).
    -   *Default:* Based on selected currency pair.
    -   *Range:* e.g., -0.01 to 0.10 (-1% to 10%).
-   **Contract Maturity ($T$):** A slider for the total contract tenor in years.
    -   *Default:* 1.0 year.
    -   *Range:* e.g., 0.1 to 5.0 years.
-   **Current Time ($t$):** A slider for the current time elapsed since inception in years.
    -   *Default:* 0.0 years (at inception).
    -   *Range:* 0.0 to $T$. This slider should automatically update its maximum value to $T$.

#### Outputs
-   **Calculated Values Display:** A clear display of the initial forward price ($F_{0,f/d}(T)$), the current MTM value for a long position ($V_t(T)$), and the current MTM value for a short position ($V_t(T)_{short}$).
-   **Plots:** Two core visualizations demonstrating MTM sensitivity.
-   **Summary Statistics:** If a dataset is generated for analysis beyond the main MTM calculation, relevant summary statistics (mean, std dev, min, max) for numeric columns should be logged.

### Algorithms and Functions to be Implemented

1.  **`calculate_forward_price(S0, rf, rd, T)`:**
    -   *Purpose:* Computes the no-arbitrage forward price.
    -   *Input:* `S0` (initial spot rate), `rf` (foreign rate), `rd` (domestic rate), `T` (maturity).
    -   *Output:* `F0T` (calculated forward price).

2.  **`calculate_mtm(St, F0T, rf, rd, T, t)`:**
    -   *Purpose:* Computes the MTM value for a long FX forward position.
    -   *Input:* `St` (current spot rate), `F0T` (original forward price), `rf` (foreign rate), `rd` (domestic rate), `T` (maturity), `t` (current time).
    -   *Output:* `Vt_long` (MTM value for long position).

3.  **`simulate_mtm_interest_rate_differential(S0_base, F0T_initial, rd_base, T_base, t_base, rf_range)`:**
    -   *Purpose:* Generates MTM values over a range of foreign interest rates (or interest rate differentials).
    -   *Input:* Base values for $S_0$, $F_{0,f/d}(T)$ (or re-calculate based on initial $S_0$), $r_d$, $T$, $t$, and a list/array `rf_range` to iterate through.
    -   *Output:* A Pandas DataFrame with columns for `rf` (or `rf - rd`) and corresponding `MTM_long` and `MTM_short` values.

4.  **`simulate_mtm_spot_rate_change(F0T_initial, rf_base, rd_base, T_base, t_base, St_range)`:**
    -   *Purpose:* Generates MTM values over a range of current spot FX rates.
    -   *Input:* Base values for $F_{0,f/d}(T)$, $r_f$, $r_d$, $T$, $t$, and a list/array `St_range` to iterate through.
    -   *Output:* A Pandas DataFrame with columns for `St` and corresponding `MTM_long` and `MTM_short` values.

5.  **`update_dashboard(S_0_fd, rf, rd, T, t)`:**
    -   *Purpose:* A main function triggered by `ipywidgets` to recalculate and update all displayed values and plots based on current interactive input parameters.

### Visualization Requirements

All plots must adhere to a color-blind-friendly palette (e.g., from Seaborn), use a minimum font size of 12pt for readability, and have clear titles, labeled axes, and legends. Interactivity should be enabled via `ipywidgets` where supported; otherwise, static PNG images will be saved.

1.  **Interest Rate Differential Impact Plot**
    -   **Type:** Line plot.
    -   **X-axis:** Interest rate differential ($r_f - r_d$) or a range of $r_f$ values while $r_d$ is constant.
    -   **Y-axis:** Mark-to-Market Value.
    -   **Description:** This plot will illustrate how the MTM value of both long and short FX forward positions changes as the interest rate differential between the foreign and domestic currencies varies. It will clearly show scenarios of appreciation/depreciation effects on the MTM. The current MTM point based on user inputs should be highlighted.
    -   **Data Generation:** Call `simulate_mtm_interest_rate_differential`.

2.  **Spot Rate Change Impact Plot**
    -   **Type:** Line plot.
    -   **X-axis:** Current Spot FX Rate ($S_{t,f/d}$).
    -   **Y-axis:** Mark-to-Market Value.
    -   **Description:** This plot will demonstrate the sensitivity of the MTM value for both long and short FX forward positions to instantaneous shifts in the current spot FX rate, holding all other parameters constant. The current MTM point based on user inputs should be highlighted.
    -   **Data Generation:** Call `simulate_mtm_spot_rate_change`.

---

## 4. Additional Notes or Instructions

### Assumptions
-   **Continuous Compounding:** All interest rate calculations throughout the notebook assume continuous compounding.
-   **No Transaction Costs/Credit Risk:** The valuation models assume an ideal market with no transaction costs, bid-ask spreads, or counterparty credit risk.
-   **Synthetic Data:** The notebook will generate synthetic data for demonstration purposes. This means no external data files are required, and default parameters allow immediate execution.
-   **FX Rate Convention:** The FX rate $S_{f/d}$ is quoted as units of domestic currency per unit of foreign currency.

### Constraints
-   **Performance:** The notebook must execute end-to-end on a mid-spec laptop (8 GB RAM) in fewer than 5 minutes.
-   **Libraries:** Only open-source Python libraries available on PyPI may be used.
-   **Narrative:** All major code steps must be accompanied by both inline code comments and brief markdown narrative cells explaining "what" is happening and "why".
-   **Data Handling:** While not external files, the internally generated data for plots should behave as if a lightweight sample (≤ 5 MB) is being processed. Implicit "validation" will be applied to user inputs (e.g., type checks, range checks for numerical inputs).

### Customization Instructions
-   **Adding Currency Pairs:** Users can easily extend the available synthetic currency pairs by modifying a predefined Python dictionary within a code cell. This dictionary will store default spot rates and interest rates for each pair.
-   **Parameter Ranges:** The ranges for sliders and simulation plots can be adjusted by modifying the respective numerical bounds in the code.
-   **User Interaction:** The interactive controls (`ipywidgets`) enable real-time parameter changes. Inline help text will guide users on the function of each control.

### References
-   [16] Pricing and Valuation of Forward Contracts, Derivatives Refresher Reading, page 12.
-   [17] Equation 9, Pricing and Valuation of Forward Contracts, Derivatives Refresher Reading, page 12.
-   `numpy` (for numerical computing)
-   `pandas` (for data manipulation and analysis)
-   `matplotlib` (for plotting)
-   `seaborn` (for statistical data visualization)
-   `ipywidgets` (for interactive controls)

