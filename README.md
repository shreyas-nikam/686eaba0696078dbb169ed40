Here's a comprehensive `README.md` file for your Streamlit application lab project, "QuLab: Derivative Pricing and Valuation."

---

# QuLab: Derivative Pricing and Valuation

![Streamlit App](https://img.shields.io/badge/Made%20with-Streamlit-red.svg?logo=streamlit)
![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/License-Proprietary-orange.svg)

## 📊 Project Description

**QuLab** is an interactive Streamlit application designed for an educational lab setting, focusing on the core concepts of **Derivative Pricing and Valuation of Forward Contracts**, with a particular emphasis on **Forward Rate Agreements (FRAs)**. This application also includes a utility for converting Annual Percentage Rates (APR) across different compounding frequencies, a fundamental concept in finance.

The primary goal of QuLab is to provide a hands-on, visual approach to understanding complex financial derivatives, their valuation mechanics, and practical applications like hedging interest rate risk. By enabling users to manipulate key financial parameters and observe real-time calculations and visualizations, QuLab transforms theoretical concepts into practical insights.

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

### Annual Percentage Rate (APR) Conversion Utility

This utility facilitates the conversion of Annual Percentage Rates (APR) between different compounding frequencies. Understanding and correctly converting APRs is fundamental for accurate financial comparisons and calculations, as the effective cost or yield of an investment/loan depends heavily on how frequently interest is compounded.

## ✨ Features

QuLab provides two main utilities accessible via a sidebar navigation:

### 1. FRA Settlement Simulator
- **Dynamic Input Controls**: Easily adjust all relevant FRA parameters (Notional Principal, Fixed Rate, Start/End Periods, Days in Year Basis, Market Reference Rate) using interactive sliders and number inputs.
- **Real-time Calculations**: See immediate updates to all calculated values (fixed interest, floating interest, net payment, cash settlement) as inputs change.
- **Transparent Formulas**: Key formulas for net payment and cash settlement are displayed using LaTeX, showing exactly how calculations are performed.
- **Narrative Interpretation**: Clear textual explanations of the settlement outcome based on the relationship between the fixed rate and the market reference rate.
- **Graphical Insights**:
    - **Bar Chart**: Visual comparison of Fixed Interest Payment, Floating Interest Payment, and Net Payment.
    - **Line Chart**: Sensitivity analysis showing how FRA Cash Settlement changes with varying Market Reference Rates, highlighting the breakeven point (Fixed Rate) and zero settlement.
- **Learning Outcomes**: Designed to help users understand FRA mechanics, perform settlement calculations, analyze market impact, and visualize risk/reward.

### 2. APR Conversion Utility
- **Flexible Input**: Convert APRs from any compounding frequency to another.
- **Formula Display**: The underlying mathematical formula for APR conversion is clearly presented using LaTeX.
- **Accurate Conversion**: Provides precise calculation of equivalent APRs, crucial for financial comparisons.

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8 or higher
- `pip` (Python package installer)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/QuLab.git
    cd QuLab
    ```
    (Replace `your-username/QuLab.git` with the actual repository URL if available)

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    -   **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    -   **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install the required Python packages:**
    Create a `requirements.txt` file in the root directory of your project with the following content:

    ```
    streamlit>=1.0.0
    pandas>=1.0.0
    numpy>=1.20.0
    plotly>=5.0.0
    ```

    Then, install them:
    ```bash
    pip install -r requirements.txt
    ```

## 🏃 Usage

To run the application, navigate to the root directory of the project (`QuLab/`) in your terminal (ensure your virtual environment is activated) and execute:

```bash
streamlit run app.py
```

This command will open the Streamlit application in your default web browser (usually `http://localhost:8501`).

### How to Use the Application:

1.  **Navigation:** Use the "Navigation" selectbox in the sidebar to switch between "FRA Settlement Simulator" and "APR Conversion Utility".
2.  **Input Parameters:**
    *   **FRA Settlement Simulator:** Adjust the FRA parameters (Notional Principal, Fixed Rate, Start/End Periods, Days in Year Basis) and the Market Reference Rate using the sliders and number inputs in the sidebar. Observe the real-time calculation updates, narrative interpretations, and visualizations.
    *   **APR Conversion Utility:** Input the "Original APR," "Original Compounding Frequency," and "Target Compounding Frequency" in the sidebar to see the equivalent converted APR.
3.  **Explore and Learn:** Experiment with different values to gain a deeper understanding of how changes in parameters impact the financial outcomes.

## 📁 Project Structure

The project is organized into a modular structure for clarity and maintainability:

```
QuLab/
├── application_pages/
│   ├── fra_settlement.py     # Contains the Streamlit code for the FRA Settlement Simulator page.
│   └── apr_conversion.py     # Contains the Streamlit code for the APR Conversion Utility page.
├── app.py                    # Main Streamlit application file, handles page navigation and overall layout.
├── README.md                 # This file.
└── requirements.txt          # Lists Python dependencies.
```

## 🛠️ Technology Stack

-   **Frontend & Backend (Unified):** [Streamlit](https://streamlit.io/)
-   **Programming Language:** Python 3
-   **Data Manipulation:** [Pandas](https://pandas.pydata.org/)
-   **Numerical Operations:** [NumPy](https://numpy.org/)
-   **Interactive Visualizations:** [Plotly Express](https://plotly.com/python/plotly-express/) & [Plotly Graph Objects](https://plotly.com/python/graph-objects/)
-   **Mathematical Functions:** Python's built-in `math` module

## 🤝 Contributing

This project is primarily intended for a lab learning environment. However, if you find any issues or have suggestions for improvements, feel free to:

1.  **Open an Issue:** Describe the bug or feature request in detail.
2.  **Fork the Repository:** Make your changes and submit a pull request.

## ⚖️ License

© 2025 QuantUniversity. All Rights Reserved.

The purpose of this demonstration is solely for educational use and illustration. Any reproduction of this demonstration requires prior written consent from QuantUniversity. This lab was generated using the QuCreate platform. QuCreate relies on AI models for generating code, which may contain inaccuracies or errors.

## ✉️ Contact

For questions, feedback, or further inquiries, please visit [QuantUniversity's Website](https://www.quantuniversity.com/) or contact us via `info@quantuniversity.com`.

---

## License

## QuantUniversity License

© QuantUniversity 2025  
This notebook was created for **educational purposes only** and is **not intended for commercial use**.  

- You **may not copy, share, or redistribute** this notebook **without explicit permission** from QuantUniversity.  
- You **may not delete or modify this license cell** without authorization.  
- This notebook was generated using **QuCreate**, an AI-powered assistant.  
- Content generated by AI may contain **hallucinated or incorrect information**. Please **verify before using**.  

All rights reserved. For permissions or commercial licensing, contact: [info@quantuniversity.com](mailto:info@quantuniversity.com)
