
import streamlit as st
import os

# Set page config at the very beginning
st.set_page_config(page_title="QuLab", layout="wide")

# Ensure the assets directory exists if needed for local images, though we're using a URL for the logo
# if not os.path.exists("assets"):
#    os.makedirs("assets")

st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab - Forward Contract Valuation Simulator")
st.divider()

st.markdown("""
### Purpose and Objectives
The "Forward Contract Valuation Simulator" Streamlit application aims to provide an interactive platform for users, particularly finance students and aspiring traders, to understand and simulate the pricing and mark-to-market (MTM) valuation of forward contracts. The application will demonstrate how initial forward prices are determined based on spot prices and risk-free rates, analyze the evolution of a forward contract's MTM value over its life, and differentiate between contracts with and without additional costs or benefits. A key objective is to visualize potential gains and losses for both long and short positions under varying market conditions, thereby demystifying core derivative concepts like the no-arbitrage principle and mark-to-market adjustments through hands-on engagement.

### Target Audience and Use Cases
*   **Target Audience:** Finance students, financial analysts, aspiring traders, and individuals interested in derivatives markets and quantitative finance.
*   **Use Cases:**
    *   **Educational Tool:** Students can manipulate parameters to gain a deeper understanding of forward contract mechanics and valuation.
    *   **Scenario Analysis:** Users can simulate different market scenarios (e.g., changes in spot price, interest rates) to observe their impact on contract value.
    *   **Risk and Profit Visualization:** Aid in understanding potential profit/loss profiles for different forward positions.

### Key Value Propositions
*   **Interactive Learning:** Provides a dynamic, hands-on experience for complex financial concepts.
*   **Clarity through Visualization:** Converts abstract financial formulas into intuitive, real-time charts.
*   **Practical Application:** Bridges theoretical knowledge with practical valuation scenarios.
*   **Accessibility:** Offers an easy-to-use interface without requiring advanced programming knowledge.

### Lab Overview
In this lab, you will explore the dynamics of forward contract pricing and valuation. A forward contract is an agreement to buy or sell an asset at a predetermined price on a future date. Unlike futures contracts, forward contracts are over-the-counter (OTC) instruments, meaning they are privately negotiated and not traded on an exchange.

The fundamental principle governing forward contract pricing is the **no-arbitrage principle**. This states that in an efficient market, it should not be possible to make risk-free profit by combining a forward contract with other financial instruments. This principle leads to specific formulas for calculating the initial forward price and its subsequent mark-to-market value.

You will interact with various parameters such as the initial spot price, risk-free rate, and time to maturity to observe how these factors influence the initial forward price. Furthermore, you will dynamically adjust current market conditions (current spot price, current time) to see how the mark-to-market (MTM) value of the contract changes. The application also allows you to consider the impact of storage costs or income (e.g., dividends) associated with the underlying asset.

Visualizations will help you understand:
*   The evolution of the MTM value over the contract's life.
*   The sensitivity of the MTM value to changes in the current spot price.
*   The profit/loss profiles at maturity for both long and short positions.

By engaging with this simulator, you will gain a practical intuition for key concepts in derivatives, which are crucial for understanding more complex financial instruments.
""")

# Your code starts here
# Create the directory for application pages if it doesn't exist
if not os.path.exists("application_pages"):
    os.makedirs("application_pages")

# Only one page for this application
page = st.sidebar.selectbox(label="Navigation", options=["Forward Contract Simulator"])
if page == "Forward Contract Simulator":
    # Ensure the page module is imported only when needed
    from application_pages.page1 import run_page
    run_page()
# Your code ends
st.divider()
st.write("© 2025 QuantUniversity. All Rights Reserved.")
st.caption("The purpose of this demonstration is solely for educational use and illustration. "
           "Any reproduction of this demonstration "
           "requires prior written consent from QuantUniversity. "
           "This lab was generated using the QuCreate platform. QuCreate relies on AI models for generating code, which may contain inaccuracies or errors")
