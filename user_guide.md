id: 686eaba0696078dbb169ed40_user_guide
summary: Derivative Pricing and Valuation of Forward  Contracts and for an Underlying  with Varying Maturities User Guide
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# Analyzing FX Forward Mark-to-Market (MTM)

## 1. Understanding FX Forward Contracts and Mark-to-Market
Duration: 03:00

Welcome to this codelab on Foreign Exchange (FX) Forward Mark-to-Market (MTM) analysis! In the world of finance, businesses and investors often need to manage their exposure to currency fluctuations. FX Forward contracts are a crucial tool for this.

### What is an FX Forward Contract?
An FX Forward contract is a customized agreement between two parties to exchange a specified amount of one currency for another at a pre-determined exchange rate on a future date. Unlike spot transactions, which involve immediate delivery, forwards lock in a rate for a future exchange. This helps in hedging against adverse currency movements.

For example, if a US company knows it will receive 1 million Euros in 3 months and wants to convert it to USD, it can enter into an FX Forward contract today to sell those Euros at a fixed USD/EUR rate in 3 months. This eliminates the uncertainty of what the spot rate will be in 3 months.

### What is Mark-to-Market (MTM)?
Mark-to-Market (MTM) is the process of valuing a financial position at its current market price. For an FX Forward contract, MTM refers to the hypothetical profit or loss if the contract were to be closed out or revalued at the current market conditions *today*.

Why is MTM important?
*   <b>Risk Management:</b> It helps in understanding the current financial exposure to a contract.
*   <b>Accounting:</b> Many financial regulations require positions to be marked-to-market regularly.
*   <b>Decision Making:</b> It provides insights into how changes in market rates affect the value of existing contracts, helping participants decide whether to hold, close, or adjust their positions.

### The Application's Purpose
This Streamlit application provides an interactive tool to visualize and understand the MTM dynamics of an FX Forward contract. You will be able to:
*   Set up an initial FX Forward contract with specific parameters.
*   Simulate changes in market conditions (spot rates and interest rates) over time.
*   Observe how the initial Forward Price is calculated.
*   Calculate and interpret the MTM value for both long and short positions.
*   Visualize the sensitivity of MTM to key market drivers.

<aside class="positive">
Understanding FX Forwards and MTM is fundamental for anyone involved in international trade, investment, or treasury management. This tool helps demystify these concepts through hands-on interaction.
</aside>

## 2. Setting Up Your FX Forward Contract
Duration: 02:30

Let's begin by configuring the initial parameters of our hypothetical FX Forward contract. All inputs for setting up the contract and simulating market conditions are located in the sidebar on the left.

### Choosing a Currency Pair
At the top of the sidebar, you'll see a section titled "**Currency Pair & Defaults**".

1.  **Select Currency Pair (Pre-fill Rates)**: Use the dropdown to choose a synthetic currency pair like "USD/EUR (Example)" or "ZAR/EUR (Example)", or keep it as "Custom".
    *   Selecting an example pair will pre-populate the initial and current rates and spot prices with typical values for that pair, giving you a good starting point.
    *   Choosing "Custom" allows you to enter all values manually.

    <aside class="positive">
    Starting with an example pair can be very helpful to quickly see the application in action. You can then switch to "Custom" to fine-tune the parameters.
    </aside>

### Initial Contract Parameters ($t=0$)
Scroll down in the sidebar to the "**Initial Contract Parameters ($t=0$)**" section. These values represent the market conditions and terms agreed upon at the very beginning of the contract.

1.  **Initial Spot FX Rate ($S_{0,f/d}$)**: This is the exchange rate for immediate delivery of currencies when the contract was initiated.
    *   The help text clarifies this as "How many units of domestic currency for one unit of foreign currency." For instance, if you choose "USD/EUR (Example)", $S_{0,f/d}$ is the USD per EUR rate.
    *   Adjust this value to reflect the spot rate at inception.

2.  **Original Contract Maturity ($T$)**: This is the total duration of the FX Forward contract, from its inception until it expires, measured in years.
    *   For example, `1.0` means one year.

3.  **Foreign Risk-Free Rate at Inception ($r_{f,initial}$)**: This is the risk-free interest rate applicable to the *foreign* currency at the time the contract was entered into.
    *   Example: If you are dealing with USD/EUR, and EUR is the foreign currency, this would be the EUR risk-free rate.
    *   Enter this as a decimal (e.g., 0.01 for 1%).

4.  **Domestic Risk-Free Rate at Inception ($r_{d,initial}$)**: This is the risk-free interest rate applicable to the *domestic* currency at the time the contract was entered into.
    *   Example: If USD is your domestic currency, this would be the USD risk-free rate.
    *   Enter this as a decimal (e.g., 0.03 for 3%).

    <aside class="negative">
    Remember to distinguish between foreign ($r_f$) and domestic ($r_d$) rates. They are crucial for calculating the forward price. Ensure $r_f$ corresponds to the foreign currency of $S_{0,f/d}$ and $r_d$ to the domestic.
    </aside>

## 3. Simulating Current Market Conditions
Duration: 02:00

Once your initial contract parameters are set, you can simulate how the contract's value changes over time by adjusting the "current" market conditions. These inputs are found under the "**Current Market Parameters ($t$)**" section in the sidebar.

1.  **Current Time ($t$)**: This slider represents how much time has passed since the contract was initiated.
    *   The value is in years, and it can range from $0.0$ (inception) up to $T$ (original maturity).
    *   As $t$ approaches $T$, the remaining time to maturity for the contract decreases.

2.  **Current Spot FX Rate ($S_{t,f/d}$)**: This is the prevailing spot exchange rate in the market *at the current time $t$*.
    *   This rate can be different from the initial spot rate ($S_{0,f/d}$) and is a major driver of MTM changes.
    *   Adjust this to see how changes in the spot market affect your forward contract's value.

3.  **Current Foreign Risk-Free Rate ($r_{f,current}$)**: This is the current risk-free interest rate for the *foreign* currency at time $t$.
    *   It can differ from the initial foreign rate ($r_{f,initial}$), reflecting changes in market interest rates.

4.  **Current Domestic Risk-Free Rate ($r_{d,current}$)**: This is the current risk-free interest rate for the *domestic* currency at time $t$.
    *   Like the foreign rate, it can also differ from its initial counterpart.

As you adjust these current parameters, the application will instantly recalculate and update the output values and graphs, allowing you to see the real-time impact on the FX Forward's MTM.

## 4. Interpreting Calculated Values
Duration: 03:00

After setting up your contract and current market conditions, the main section of the application displays the calculated values.

### FX Forward Price at Inception ($F_{0,f/d}(T)$)
This is the rate at which the parties initially agreed to exchange currencies at the maturity date $T$. It is calculated based on the initial spot rate and the interest rate differential between the two currencies at inception.

The formula used is:
$$F_{0,f/d}(T) = S_{0,f/d}e^{(r_{f,initial} - r_{d,initial})T}$$
Where:
*   $S_{0,f/d}$ is the initial spot FX rate (foreign per domestic).
*   $r_{f,initial}$ is the foreign risk-free rate at inception.
*   $r_{d,initial}$ is the domestic risk-free rate at inception.
*   $T$ is the total time to maturity of the contract.
*   $e$ is Euler's number (the base of the natural logarithm).

<aside class="positive">
The term $e^{(r_{f,initial} - r_{d,initial})T}$ represents the *forward premium* or *discount*. If $r_{f,initial} > r_{d,initial}$, the foreign currency is at a premium, meaning its forward price is higher than its spot price. If $r_{f,initial} < r_{d,initial}$, it's at a discount.
</aside>

### Current Mark-to-Market (MTM) Value
This is the core output of the application. The MTM value represents the hypothetical profit or loss of the FX Forward contract at the current time $t$, given the current market conditions. The application shows MTM for both "Long" and "Short" positions.

The formula for a **long position** (agreeing to buy the foreign currency at the forward rate) is:
$$V_t^{long}(T) = S_{t,f/d} - F_{0,f/d}(T)e^{-(r_{f,current} - r_{d,current})(T - t)}$$
Where:
*   $S_{t,f/d}$ is the current spot FX rate.
*   $F_{0,f/d}(T)$ is the initial FX Forward price.
*   $r_{f,current}$ is the current foreign risk-free rate.
*   $r_{d,current}$ is the current domestic risk-free rate.
*   $T - t$ is the remaining time to maturity.

**Interpretation:**
*   A **positive MTM for a long position** indicates a gain for the party who agreed to buy the foreign currency. This happens if the current spot rate ($S_{t,f/d}$) is more favorable (higher) than the effectively discounted original forward rate.
*   A **negative MTM for a long position** indicates a loss. This occurs if the current spot rate is less favorable (lower).
*   For a **short position** (agreeing to sell the foreign currency), the MTM is simply the negative of the long position's MTM ($V_t^{short}(T) = -V_t^{long}(T)$). So, a positive MTM for a short position means a gain for the seller, and a negative MTM means a loss.

Observe how these values change as you adjust the parameters in the sidebar.

## 5. Analyzing MTM with Interactive Visualizations: Interest Rate Differential
Duration: 03:30

The application provides two interactive plots to help you understand the sensitivity of the MTM value to different market factors. Let's look at the first one.

### MTM Value vs. Interest Rate Differential ($r_f - r_d$)
This graph illustrates how the MTM value of your FX Forward contract changes as the current foreign risk-free rate ($r_{f,current}$) varies, while holding all other parameters (including the domestic risk-free rate $r_{d,current}$ and current spot rate $S_{t,f/d}$) constant.

**Understanding the X-axis:**
The X-axis represents the *interest rate differential* ($r_f - r_d$). A positive value means the foreign interest rate is higher than the domestic rate, and a negative value means the foreign rate is lower.

**Interpreting the Plot:**
*   **Lines:** You will see two lines: one for the "Long Position" and one for the "Short Position". As expected, they are mirror images of each other.
*   **Current Value Marker:** A red star marker indicates the MTM value based on your currently selected parameters in the sidebar.
*   **Zero MTM Line:** A dashed grey line at $y=0$ helps you easily identify where the contract's MTM value is zero.

**What does this tell you?**
The interest rate differential $(r_f - r_d)$ directly influences the *discounting factor* in the MTM formula ($e^{-(r_f - r_d)(T - t)}$).
*   If $r_f$ increases relative to $r_d$, the term $-(r_f - r_d)$ becomes more negative. This means the present value of the original forward price (the second part of the MTM formula) decreases.
*   For a **long position**, if $S_{t,f/d}$ is fixed, a decrease in the discounted original forward value will generally lead to a higher (more positive or less negative) MTM. This is because you are still obligated to buy at the *original* forward price, but the market's expectation for the *future* spot price (implied by current spot and rates) might be shifting.

Experiment by changing $r_{f,current}$ in the sidebar and observe how the red star marker moves along the curve.

<aside class="positive">
This plot helps you understand the interest rate risk of your FX Forward contract. Even if spot rates don't move, significant shifts in interest rate differentials can impact your MTM.
</aside>

## 6. Analyzing MTM with Interactive Visualizations: Current Spot FX Rate
Duration: 03:30

The second interactive plot focuses on the most significant driver of FX Forward MTM: the current spot exchange rate.

### MTM Value vs. Current Spot FX Rate ($S_t$)
This graph shows how the MTM value changes as the current spot FX rate ($S_{t,f/d}$) varies, while all other parameters (including current interest rates and time passed) are held constant.

**Understanding the X-axis:**
The X-axis represents the Current Spot Rate ($S_t$).

**Interpreting the Plot:**
*   **Lines:** Again, you'll see lines for "Long Position" and "Short Position".
*   **Initial Forward Price Line:** A dashed purple line indicates the initial forward price ($F_{0,f/d}(T)$) that was agreed upon at inception.
*   **Current Spot Rate Line:** A solid red line indicates the current spot rate ($S_{t,f/d}$) as set in your sidebar.
*   **Zero MTM Line:** A dashed grey line at $y=0$.

**What does this tell you?**
This plot clearly shows the linear relationship between the current spot rate and the MTM value.
*   For a **long FX forward position** (you agreed to buy foreign currency at $F_{0,f/d}(T)$):
    *   If the current spot rate ($S_{t,f/d}$) is *higher* than the effectively discounted original forward rate (the second term in the MTM formula), your MTM will be positive (a gain). This is because you can buy the currency cheaper (at $F_{0,f/d}(T)$) than its current market value.
    *   If the current spot rate ($S_{t,f/d}$) is *lower*, your MTM will be negative (a loss). You would be buying at a rate ($F_{0,f/d}(T)$) that is higher than what you could get in the current spot market.
*   For a **short FX forward position** (you agreed to sell foreign currency at $F_{0,f/d}(T)$):
    *   The logic is reversed: you gain if $S_{t,f/d}$ is lower, and lose if $S_{t,f/d}$ is higher.

<aside class="positive">
The current spot rate is often the most volatile and impactful variable for MTM. This plot visually demonstrates how sensitive your position is to movements in the spot market. You can clearly see the break-even point where MTM is zero.
</aside>

## 7. Conclusion and Further Exploration
Duration: 01:00

Congratulations! You have successfully navigated the FX Forward Mark-to-Market Analyzer.

You've learned:
*   The fundamental concepts of FX Forward contracts and Mark-to-Market valuation.
*   How to set initial contract parameters and simulate current market conditions.
*   The calculation and interpretation of the FX Forward Price and MTM value.
*   How interest rate differentials and, more significantly, current spot rates impact the MTM of your FX Forward position.

This interactive tool provides a practical way to understand theoretical financial concepts. Feel free to continue experimenting with different parameters to build your intuition about FX Forward MTM dynamics.

### References
The formulas and concepts used in this application are based on established financial derivatives literature:
*   [16] Hull, John C. *Options, Futures, and Other Derivatives*. Pearson Education. (For FX Forward Price formula)
*   [17] (Your specific reference for MTM value formula, acknowledging the exact form provided in the prompt's specification)

<aside class="positive">
Practice makes perfect! Try setting up various scenarios: positive/negative interest rate differentials, different maturities, and significant spot rate swings to see their effects.
</aside>
