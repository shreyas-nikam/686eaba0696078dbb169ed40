id: 686eaba0696078dbb169ed40_user_guide
summary: Derivative Pricing and Valuation of Forward  Contracts and for an Underlying  with Varying Maturities User Guide
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# QuLab: Understanding Forward Contracts with Costs and Benefits

## Introduction to Forward Contracts and Their Valuation
Duration: 0:05:00

Welcome to the QuLab simulator for Forward Contracts with Costs & Benefits! In this codelab, you'll gain a comprehensive understanding of how discrete costs (like storage) and benefits (like dividends) influence the pricing and valuation of forward contracts. This interactive application will allow you to explore these concepts in real-time, visualizing their impact.

### What are Forward Contracts?
A **forward contract** is a private agreement between two parties to buy or sell an asset at a specified price on a future date. Unlike futures contracts, which are standardized and traded on exchanges, forward contracts are customized and traded over-the-counter (OTC). This customization allows for flexibility but introduces counterparty risk.

### Core Concepts Explained

The valuation of forward contracts is fundamentally guided by the **No-Arbitrage Principle**. This principle asserts that in an efficient market, it's impossible to generate risk-free profits by simultaneously exploiting price discrepancies. This implies that the forward price must reflect the entire cost of holding the underlying asset until maturity, including any income received or expenses incurred.

Let's delve into the key formulas that underpin this application:

1.  **Forward Price at Inception ($F_0(T)$):** This is the price agreed upon today ($t=0$) for a transaction that will occur at a future date $T$. When an asset generates benefits (e.g., dividends, coupon payments) or incurs costs (e.g., storage fees, insurance) during the contract's life, these cash flows must be factored into the forward price.

    The formula for the forward price, considering discrete costs and benefits, is:
    $$F_0(T) = (S_0 - PV_0(I) + PV_0(C))(1 + r)^T$$
    Where:
    *   $S_0$: The initial spot price of the underlying asset at time $t=0$.
    *   $PV_0(I)$: The Present Value of all discrete benefits (Income/Dividends) expected from time $t=0$ up to maturity $T$.
        $$PV_0(I) = \sum_{j} I_j (1 + r)^{-t_j^I}$$
        Here, $I_j$ is the amount of the $j$-th benefit, and $t_j^I$ is the time (in years from $t=0$) when the $j$-th benefit is received.
    *   $PV_0(C)$: The Present Value of all discrete costs incurred from time $t=0$ up to maturity $T$.
        $$PV_0(C) = \sum_{k} C_k (1 + r)^{-t_k^C}$$
        Here, $C_k$ is the amount of the $k$-th cost, and $t_k^C$ is the time (in years from $t=0$) when the $k$-th cost is incurred.
    *   $r$: The annualized risk-free interest rate.
    *   $T$: The total time to maturity of the forward contract in years from $t=0$.

2.  **Mark-to-Market (MTM) Value ($V_t(T)$):** This is the value of the forward contract at any point in time $t$ before maturity. It reflects the profit or loss that would be realized if the contract were to be closed out at the current time $t$. The MTM value fluctuates as the underlying asset's spot price, interest rates, and remaining time to maturity change.

    For a **long position** (an agreement to buy the asset), the MTM value at time $t$ is:
    $$V_t(T) = (S_t - PV_t(I) + PV_t(C)) - F_0(T)(1 + r)^{-(T-t)}$$
    Where:
    *   $S_t$: The spot price of the underlying asset at the current time $t$.
    *   $PV_t(I)$: The Present Value of *remaining* discrete benefits from the current time $t$ to maturity $T$.
    *   $PV_t(C)$: The Present Value of *remaining* discrete costs from the current time $t$ to maturity $T$.
    *   $F_0(T)$: The original forward price agreed upon at $t=0$.
    *   $(1 + r)^{-(T-t)}$: The discount factor for the remaining life of the contract $(T-t)$.

    The present value of *remaining* cash flows from time $t$ to maturity $T$ is calculated by only considering cash flows whose occurrence time ($t_j^{CF}$) is at or after the current time $t$:
    $$PV_t(CF) = \sum_{j | t_j^{CF} \ge t} CF_j (1 + r)^{-(t_j^{CF} - t)}$$
    Here, $CF_j$ is the amount of the $j$-th cash flow (either $I_j$ or $C_k$), and $t_j^{CF}$ is its original time from $t=0$.

    For a **short position** (an agreement to sell the asset), the MTM value is the negative of the long position's MTM value:
    $$V_t(T)_{short} = -V_t(T)_{long}$$

This application is designed to help you interactively adjust these parameters and observe their impact on the forward price and MTM value.

## Exploring the Simulator's Interface
Duration: 0:03:00

The Streamlit application provides an intuitive interface to interact with the forward contract valuation model. Let's familiarize ourselves with the input parameters.

On the left sidebar, you'll see a navigation dropdown, currently set to "Forward Contracts Simulator". This ensures you are on the correct page.

The main area of the application is divided into several sections:

### Core Contract Parameters
This section allows you to define the fundamental characteristics of your forward contract:

*   **Initial Spot Price ($S_0$):** The current market price of the underlying asset at the very beginning of the contract (time $t=0$).
*   **Maturity ($T$):** The total duration of the forward contract, in years, from time $t=0$ until its expiration.
*   **Risk-Free Rate ($r$):** The annualized risk-free interest rate, used for discounting and compounding. Enter it as a decimal (e.g., `0.05` for 5%).

### Current Valuation Parameters
These parameters define the conditions at the specific moment you want to value the contract (mark-to-market):

*   **Current Time ($t$):** The present moment in time, in years, from the contract's inception ($t=0$). This value must be less than or equal to the Maturity ($T$).
*   **Current Spot Price ($S_t$):** The market price of the underlying asset at the current time $t$.

### Cash Flow Specification
This is where you define any discrete dividends (benefits) or costs associated with holding the asset over the contract's life. These are entered as JSON arrays:

*   **Dividends (Benefits) [JSON]:** Enter discrete income payments (like dividends from a stock) as a JSON list. Each item in the list must be an object with two keys:
    *   `"amount"`: The value of the dividend.
    *   `"time_from_t0"`: The time (in years from $t=0$) when the dividend is received.
    For example:
    ```json
    [{"amount": 2.0, "time_from_t0": 0.25}, {"amount": 2.5, "time_from_t0": 0.75}]
    ```
    This example represents a dividend of $2.0 received at 0.25 years and another of $2.5 received at 0.75 years from inception.
*   **Costs [JSON]:** Enter discrete expenses (like storage costs for a commodity) in the same JSON list format as dividends:
    *   `"amount"`: The value of the cost.
    *   `"time_from_t0"`: The time (in years from $t=0$) when the cost is incurred.
    For example:
    ```json
    [{"amount": 1.0, "time_from_t0": 0.5}]
    ```
    This example represents a cost of $1.0 incurred at 0.5 years from inception.

<aside class="negative">
<b>Important:</b> Ensure your JSON input is correctly formatted. Missing brackets, commas, or incorrect key names (`amount`, `time_from_t0`) will result in an error message. The `time_from_t0` for cash flows must be greater than or equal to 0 and less than or equal to the Maturity (T).
</aside>

### Position Type for MTM Valuation
Select whether you hold a 'long' (agreement to buy) or 'short' (agreement to sell) position in the forward contract. This choice impacts the sign of the calculated Mark-to-Market (MTM) value.

Once you adjust any input, the application will automatically recalculate and update the outputs and visualizations.

## Calculating the Forward Price at Inception ($F_0(T)$)
Duration: 0:02:00

After setting your "Core Contract Parameters" and "Cash Flow Specification", the application immediately calculates and displays the forward price at inception.

Navigate to the **"Calculated Outputs"** section. You will see two key metrics related to $F_0(T)$:

*   **Forward Price at Inception ($F_0(T)$) (with C/B):** This is the primary forward price, calculated using the $F_0(T)$ formula that accounts for all your specified **Costs and Benefits** (C/B). This is the fair price an investor would agree upon today to avoid arbitrage.

*   **Forward Price at Inception ($F_0(T)$) (without C/B):** This is provided for comparison. It represents the forward price if there were **no discrete costs or benefits** associated with the underlying asset. In this simplified scenario, the formula becomes:
    $$F_0(T) = S_0 (1 + r)^T$$
    This value helps you understand the direct impact of costs and benefits on the forward price.

<aside class="positive">
<b>Experiment:</b> Try changing the Initial Spot Price ($S_0$), Maturity ($T$), or Risk-Free Rate ($r$). Observe how both forward prices change. Then, add or remove dividends and costs in the JSON input fields and notice how the "with C/B" forward price deviates from the "without C/B" price. You'll see that benefits (dividends) decrease the forward price, while costs increase it.
</aside>

## Understanding the Mark-to-Market (MTM) Value ($V_t(T)$)
Duration: 0:03:00

The **Mark-to-Market (MTM) Value ($V_t(T)$)** is crucial for understanding the current profitability or loss of your forward contract *before* it matures. It tells you what your contract is worth today if you were to close it out.

In the **"Calculated Outputs"** section, below the forward prices, you'll find:

*   **MTM Value at Current Time ($V_t(T)$) (Long/Short Position):** This metric displays the current value of your forward contract.

The MTM value is calculated using the second formula introduced earlier:
$$V_t(T) = (S_t - PV_t(I) + PV_t(C)) - F_0(T)(1 + r)^{-(T-t)}$$

Recall that for a long position, a positive MTM value indicates a profit, and a negative value indicates a loss. For a short position, it's the opposite: a positive MTM is a loss, and a negative MTM is a profit. The application automatically adjusts the displayed MTM value based on your selected "Position Type".

<aside class="positive">
<b>Experiment:</b>
<ul>
  <li>Keep all other parameters constant and change the <b>Current Spot Price ($S_t$)</b>. Notice how a higher $S_t$ increases the MTM value for a long position and decreases it for a short position.</li>
  <li>Adjust the <b>Current Time ($t$)</b> closer to maturity ($T$). You'll observe that as $t$ approaches $T$, the impact of the discount factor $(1 + r)^{-(T-t)}$ diminishes, and the MTM value converges towards $(S_T - F_0(T))$ (ignoring remaining cash flows right at maturity).</li>
  <li>Modify the <b>remaining</b> dividends or costs by changing their amounts or times in the JSON input (ensuring `time_from_t0` is still after `t_current`). See how these changes impact the `PV_t(I)` and `PV_t(C)` terms, and thus the MTM value.</li>
</ul>
</aside>

## Visualizing MTM Value Evolution Over Time
Duration: 0:04:00

The first visualization, **"MTM Value Evolution Over Time (Long Position)"**, provides a dynamic view of how the MTM value of a long forward contract could change from inception ($t=0$) up to maturity ($T$).

### Understanding the Plot:
*   **X-axis: Time (Years)**: Represents the progression of time from the contract's inception to its maturity.
*   **Y-axis: MTM Value**: Shows the Mark-to-Market value of the forward contract.
*   **"MTM Value (with C/B)" line**: This curve shows the MTM value considering the dividends and costs you specified.
*   **"MTM Value (without C/B)" line**: This curve shows the MTM value if no discrete cash flows were present.
*   **Vertical Dashed Line (Current Time):** A grey dashed line indicating your currently set `Current Time ($t$)`. The point where this line intersects the MTM curves corresponds to the MTM value displayed in the "Calculated Outputs".
*   **Horizontal Dashed Line (Break-even (Y=0)):** A red dashed line at Y=0. This line represents the point where the contract has neither made a profit nor incurred a loss.

<aside class="positive">
<b>Insight:</b>
For this visualization, the application simulates a hypothetical path for the spot price ($S_t$) to illustrate the MTM evolution. It assumes $S_t$ generally moves from the initial spot price $S_0$ towards the calculated forward price $F_0(T)$ at maturity. This is a simplification for visualization purposes and does not represent actual market predictions. In a real scenario, $S_t$ would follow a stochastic (random) path.
</aside>

### Key Observations:
*   At $t=0$, the MTM value of a newly entered forward contract is always zero, assuming it was priced without arbitrage.
*   As time progresses and the simulated spot price changes, the MTM value deviates from zero.
*   Observe how the "with C/B" curve differs from the "without C/B" curve. This difference highlights the impact of the present value of future costs and benefits on the contract's value over time.

## Analyzing Sensitivity of Forward Price to Costs/Benefits Magnitude
Duration: 0:03:00

The second visualization, **"Sensitivity of Forward Price to Costs/Benefits Magnitude"**, helps you understand how varying the magnitude of your specified dividends or costs impacts the initial forward price ($F_0(T)$).

### Understanding the Plot:
*   **X-axis: Multiplier of Original Costs/Benefits**: This axis represents a factor by which the *original* amounts of your specified dividends and costs are multiplied. A multiplier of 1 means using the original amounts, 0 means no costs/benefits, and 2 means double the original amounts.
*   **Y-axis: Forward Price ($F_0(T)$)**: Shows the calculated forward price at inception.
*   **"F0(T) vs. Costs Multiplier" line**: This curve illustrates how $F_0(T)$ changes as only the *costs* are scaled by the multiplier (while dividends remain at their original specified amounts).
*   **"F0(T) vs. Dividends Multiplier" line**: This curve illustrates how $F_0(T)$ changes as only the *dividends* are scaled by the multiplier (while costs remain at their original specified amounts).

### Key Observations:
*   **Impact of Costs:** As the multiplier for costs increases, the "F0(T) vs. Costs Multiplier" line will generally show an **increase** in the forward price. This is because higher holding costs need to be compensated for in the future price.
*   **Impact of Benefits:** As the multiplier for dividends increases, the "F0(T) vs. Dividends Multiplier" line will generally show a **decrease** in the forward price. This is because the benefits reduce the net cost of holding the asset, making the forward price lower.
*   The slope of these lines indicates the sensitivity: a steeper slope means the forward price is more sensitive to changes in that specific cash flow type.

<aside class="positive">
<b>Experiment:</b>
Try changing your initial dividend or cost amounts in the JSON input fields. Then, observe how the starting point (at Multiplier=1) and the slope of the corresponding lines change in this sensitivity plot.
</aside>

## Comparing MTM Value Across Different Scenarios
Duration: 0:03:00

The final visualization, **"MTM Value Comparison Across Scenarios (Long/Short Position)"**, provides a bar chart comparing the Mark-to-Market value of your forward contract under several pre-defined scenarios. This helps in understanding the quantitative impact of various cost and benefit assumptions.

### Understanding the Plot:
*   **X-axis: Scenario**: Each bar represents a different predefined scenario for costs and benefits.
*   **Y-axis: MTM Value ($)**: The height of the bar indicates the calculated MTM value for that specific scenario, adjusted for your selected "Position Type".

### Pre-defined Scenarios:
1.  **Base Case (with C/B):** This scenario uses the exact dividends and costs you initially specified in the input fields.
2.  **No Costs/Benefits:** This scenario assumes no discrete dividends or costs (i.e., empty JSON arrays for both).
3.  **Double Dividends:** This scenario uses double the `amount` of each dividend you specified, while costs remain at their original values.
4.  **Double Costs:** This scenario uses double the `amount` of each cost you specified, while dividends remain at their original values.

<aside class="positive">
<b>Insight:</b> This bar chart quickly shows the relative impact of the various cash flow assumptions on your contract's current value. For example, if you have a long position, you'd expect "Double Dividends" to result in a higher (or less negative) MTM value compared to the "Base Case", while "Double Costs" would likely result in a lower (or more negative) MTM value. The exact opposite would be true for a short position.
</aside>

## Conclusion and Further Exploration
Duration: 0:02:00

Congratulations! You've successfully navigated the QuLab Forward Contracts Simulator and gained a practical understanding of how discrete costs and benefits influence forward contract pricing and valuation.

### Key Takeaways:
*   The **No-Arbitrage Principle** is fundamental to forward contract pricing, ensuring that the forward price accounts for all carrying costs and benefits of the underlying asset.
*   **Forward Price at Inception ($F_0(T)$)** is affected by the present value of future income (benefits), which decreases it, and the present value of future expenses (costs), which increases it.
*   The **Mark-to-Market (MTM) Value ($V_t(T)$)** represents the contract's current worth and is influenced by the current spot price, remaining time to maturity, and the present value of any *remaining* costs and benefits.
*   Visualizations provide intuitive insights into the evolution of MTM value and the sensitivity of forward prices to cash flow magnitudes.

### What's Next?
We encourage you to continue experimenting with the simulator:
*   Try different combinations of initial spot prices, maturities, and risk-free rates.
*   Input more complex JSON structures for dividends and costs, with varying amounts and times.
*   Observe how the MTM value responds to your chosen position type (long vs. short).
*   Consider how a real-world scenario (e.g., a stock with quarterly dividends, a commodity with monthly storage fees) would be modeled using this application.

This lab was generated using the QuCreate platform. QuCreate leverages AI models for code generation, which may occasionally contain inaccuracies. Always verify the outputs and underlying concepts.

Thank you for completing this QuLab session!
