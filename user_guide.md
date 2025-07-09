id: 686eaba0696078dbb169ed40_user_guide
summary: Derivative Pricing and Valuation of Forward  Contracts and for an Underlying  with Varying Maturities User Guide
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# QuLab: Understanding FX Forward Contract Valuation

## Introduction to FX Forward MTM Analysis
Duration: 0:05

Welcome to the QuLab FX Forward Mark-to-Market (MTM) Analyzer! This interactive tool is designed to demystify the valuation of Foreign Exchange (FX) forward contracts. Understanding how these financial instruments are valued and how their value changes over time is crucial for anyone involved in international trade, investment, or financial risk management.

This codelab will guide you through the application's features, helping you grasp key financial concepts without delving into complex programming. You'll learn to:

*   **Define an FX Forward Contract**: Understand what an FX forward is and how its initial price is set based on the concept of Interest Rate Parity, preventing arbitrage opportunities.
*   **Calculate Mark-to-Market (MTM)**: Learn how the current value of an existing forward contract is determined. MTM tells you the theoretical profit or loss if the contract were to be closed out (offset) at this very moment.
*   **Analyze Market Impact**: Observe directly how changes in spot exchange rates and interest rate differentials influence the MTM value of your forward positions.
*   **Visualize Valuation Dynamics**: Use interactive plots to see the sensitivity of MTM to various market parameters.

<aside class="positive">
<b>Why is this important?</b> FX forward contracts are widely used by companies to hedge foreign exchange risk. Understanding their valuation is key to managing financial exposure and making informed trading decisions.
</aside>

At its core, the application calculates:

1.  **Initial FX Forward Price ($F_{0,f/d}(T)$)**: This is the exchange rate agreed upon at the start of the contract ($t=0$) for a future exchange. It's determined by the initial spot rate and the interest rate differential between the two currencies involved.

    $$F_{0,f/d}(T) = S_{0,f/d}e^{(r_f - r_d)T}$$

    Here, $S_{0,f/d}$ is the initial spot rate (how many units of domestic currency for one unit of foreign currency), $r_f$ and $r_d$ are the foreign and domestic risk-free interest rates, and $T$ is the total time to maturity in years.

2.  **Mark-to-Market Value ($V_t(T)$)**: This is the current value of the contract at any given time $t$ *after* inception ($0 \le t \le T$). For a **long position** (agreement to buy foreign currency at maturity):

    $$V_t^{long}(T) = S_{t,f/d} - F_{0,f/d}(T)e^{-(r_f - r_d)(T - t)}$$

    $S_{t,f/d}$ is the current spot rate, $F_{0,f/d}(T)$ is the initial forward price, and $(T - t)$ is the remaining time to maturity. For a **short position** (agreement to sell foreign currency), the MTM is simply the negative of the long position's MTM: $V_t^{short}(T) = -V_t^{long}(T)$.

By interacting with the application, you'll gain practical insights into how these parameters dynamically influence forward prices and MTM values.

## Setting Up Your Forward Contract
Duration: 0:07

Let's begin by defining the characteristics of our FX forward contract. All the input controls for this application are located in the sidebar on the left.

1.  **Access the Sidebar:** Ensure the sidebar is visible. If not, look for a `>` symbol or a hamburger menu icon (☰) on the top-left of the page and click it.

2.  **Select a Currency Pair (Optional Pre-fill):**
    *   Under "**1. Initial Contract Parameters (t=0)**", locate the "Select Currency Pair (Pre-fill Rates)" dropdown.
    *   You can choose "Custom" to enter all values manually, or select one of the pre-defined synthetic pairs like "USD/EUR" or "EUR/USD". Choosing a pre-defined pair will automatically populate the initial spot rate and interest rates, giving you a starting point.
    *   For example, if you select "USD/EUR (Domestic=USD, Foreign=EUR)", the initial spot rate represents how many US Dollars ($S_{0,f/d}$) are needed to buy one Euro.

3.  **Define Initial Contract Parameters (at $t=0$):**
    *   **Initial Spot FX Rate ($S_{0,f/d}$):** This is the exchange rate between the foreign and domestic currencies at the moment the contract is initiated. Adjust this value to represent the market spot rate when your forward contract was agreed upon.
    *   **Original Contract Maturity ($T$):** This slider sets the total lifespan of your forward contract from its inception, measured in years. For example, a value of `1.0` means a one-year contract.
    *   **Foreign Risk-Free Rate at Inception ($r_{f,initial}$):** This is the risk-free interest rate applicable to the foreign currency at the contract's start.
    *   **Domestic Risk-Free Rate at Inception ($r_{d,initial}$):** This is the risk-free interest rate applicable to the domestic currency at the contract's start.

<aside class="positive">
Experiment with different currency pairs and initial settings. Notice how the "Initial FX Forward Price ($F_{0,f/d}(T)$)" displayed in the main content area changes immediately as you adjust these parameters. This reflects the no-arbitrage pricing of the forward contract.
</aside>

## Analyzing Current Market Conditions and MTM
Duration: 0:10

Now that we've defined our contract's initial terms, let's explore how its value changes over time due to evolving market conditions.

1.  **Set Current Market Parameters (at time $t$):**
    *   In the sidebar, move to "**2. Current Market Parameters (at time t)**".
    *   **Current Time ($t$):** This slider allows you to simulate the passage of time from the contract's inception. Drag it from `0.0` (inception) up to `T_maturity` (contract maturity).
        <aside class="negative">
        <b>Important:</b> The current time ($t$) cannot exceed the original contract maturity ($T$). The application will show an error if you try to set $t > T$.
        </aside>
    *   **Current Spot FX Rate ($S_{t,f/d}$):** This represents the prevailing spot exchange rate in the market at the current time $t$. This is the most significant driver of MTM changes.
    *   **Current Foreign Risk-Free Rate ($r_{f,current}$):** This is the current risk-free interest rate for the foreign currency. This rate can differ from the initial foreign rate.
    *   **Current Domestic Risk-Free Rate ($r_{d,current}$):** Similarly, this is the current risk-free interest rate for the domestic currency. This can also differ from the initial domestic rate.

2.  **Observe Calculated MTM Values:**
    *   As you adjust these "current" parameters, observe the "Calculated Values" section in the main content area.
    *   **Current MTM Value (Long Position, $V_t^{long}(T)$):** This shows the Mark-to-Market value for a party holding a **long position** (i.e., they agreed to *buy* the foreign currency at the initial forward price).
        *   A **positive MTM** means the long position has gained value since inception, indicating a theoretical profit if closed out today.
        *   A **negative MTM** means the long position has lost value, indicating a theoretical loss.
    *   **Current MTM Value (Short Position, $V_t^{short}(T)$):** This shows the MTM value for a party holding a **short position** (i.e., they agreed to *sell* the foreign currency).
        *   For a short position, the interpretation is reversed: a positive MTM indicates a loss, and a negative MTM indicates a gain.

<aside class="positive">
<b>Practical Tip:</b> When the current time ($t$) is `0.0`, and all current rates match initial rates, the MTM value should be very close to zero. This is because at inception, there's no gain or loss unless transaction costs are considered.
</aside>

## Interpreting Interactive Plots
Duration: 0:15

The application provides two interactive plots to help you visualize the sensitivity of the MTM value to changes in market parameters.

1.  **MTM Value vs. Interest Rate Differential ($r_f - r_d$):**
    *   This plot shows how the MTM value changes as the **Foreign Risk-Free Rate** ($r_f$) is varied, while keeping the **Domestic Risk-Free Rate** ($r_d$) constant. This effectively demonstrates the impact of changes in the interest rate differential ($r_f - r_d$).
    *   **Interaction:** While you cannot directly manipulate this plot, it dynamically updates based on your current inputs. Pay attention to how the slope of the lines changes when you adjust the `Current Foreign Risk-Free Rate` and `Current Domestic Risk-Free Rate` sliders in the sidebar.
    *   **Interpretation:**
        *   Observe the blue line for a **long position** and the red line for a **short position**.
        *   Notice where the lines cross the 'Zero MTM' dashed line. This indicates the interest rate differential at which the contract would have zero value (at the given spot rate and time).
        *   How steeply do the lines rise or fall? This indicates the sensitivity of the MTM to changes in interest rate differentials.

2.  **MTM Value vs. Current Spot FX Rate ($S_{t,f/d}$):**
    *   This plot is crucial for understanding the primary driver of MTM changes: the **Current Spot FX Rate** ($S_{t,f/d}$).
    *   The vertical dashed green line indicates the **Initial FX Forward Price ($F_{0,f/d}(T)$)**, which is the rate at which your contract was originally agreed upon.
    *   **Interaction:** Directly manipulate the `Current Spot FX Rate ($S_{t,f/d}$)` slider in the sidebar and observe how the current spot rate moves along the x-axis, and how the MTM value (the blue/red line) changes correspondingly.
    *   **Interpretation:**
        *   For a **long position** (blue line), if the current spot rate ($S_{t,f/d}$) is *above* the initial forward price ($F_{0,f/d}(T)$), the MTM is positive (a gain). This means you agreed to buy at a cheaper rate than the current market offers.
        *   If the current spot rate ($S_{t,f/d}$) is *below* the initial forward price, the MTM for a long position is negative (a loss).
        *   For a **short position** (red line), the inverse is true. If the current spot rate is *below* the initial forward price, the MTM is positive (a gain).

<aside class="positive">
<b>Challenge:</b> Try setting the "Current Time ($t$)" slider to its maximum value, equal to the "Original Contract Maturity ($T$)". What happens to the MTM value? At maturity, the forward contract effectively becomes a spot contract, and its value should reflect the difference between the prevailing spot rate and the original forward price, adjusted for interest rates until maturity.
</aside>

## Summary and Key Takeaways
Duration: 0:03

Congratulations! You've successfully navigated the QuLab FX Forward Mark-to-Market Analyzer. Through this interactive experience, you should now have a clearer understanding of:

*   **FX Forward Contract Basics**: How initial terms like spot rates, interest rates, and maturity define the contract.
*   **No-Arbitrage Forward Pricing**: The initial forward price is set to prevent risk-free profit opportunities based on interest rate parity.
*   **Mark-to-Market Valuation**: MTM is a dynamic measure of the contract's current value, reflecting potential gains or losses.
*   **Sensitivity to Market Changes**: The MTM value is highly sensitive to fluctuations in the current spot exchange rate and the changing interest rate differentials between the two currencies.
*   **Time Decay**: While not explicitly plotted as a separate curve, you observed that as time ($t$) approaches maturity ($T$), the remaining time to maturity $(T-t)$ diminishes, which impacts the MTM calculation, particularly the present value of the forward price component.

This hands-on exploration provides a solid foundation for understanding the mechanics of FX forward valuation, a critical skill in financial analysis and risk management. Keep experimenting with the sliders to build your intuition about these powerful derivatives!
