
# Forward Contract Valuation Simulator

This Streamlit application provides an interactive platform for users to understand and simulate the pricing and mark-to-market (MTM) valuation of forward contracts. It's designed for finance students, financial analysts, aspiring traders, and anyone interested in derivatives markets and quantitative finance.

## Table of Contents
- [Application Overview](#application-overview)
- [Features](#features)
- [How to Run](#how-to-run)
- [Key Concepts Covered](#key-concepts-covered)
- [Contributing](#contributing)
- [License](#license)

## Application Overview
The "Forward Contract Valuation Simulator" demonstrates how initial forward prices are determined based on spot prices and risk-free rates, analyzes the evolution of a forward contract's MTM value over its life, and differentiates between contracts with and without additional costs or benefits. A key objective is to visualize potential gains and losses for both long and short positions under varying market conditions, thereby demystifying core derivative concepts like the no-arbitrage principle and mark-to-market adjustments through hands-on engagement.

## Features
- **Interactive Learning:** Dynamic, hands-on experience for complex financial concepts.
- **Clarity through Visualization:** Converts abstract financial formulas into intuitive, real-time charts using Plotly.
- **Practical Application:** Bridges theoretical knowledge with practical valuation scenarios.
- **Accessibility:** Easy-to-use interface without requiring advanced programming knowledge.
- **Real-time Updates:** All calculations and visualizations update instantaneously as input parameters are adjusted.

## How to Run

### Using Docker (Recommended)
1.  **Build the Docker image:**
    ```bash
    docker build -t forward-contract-simulator .
    ```
2.  **Run the Docker container:**
    ```bash
    docker run -p 8501:8501 forward-contract-simulator
    ```
3.  Open your web browser and navigate to `http://localhost:8501`.

### Locally
1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```
2.  **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scriptsctivate`
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```
5.  Open your web browser and navigate to the address provided by Streamlit (usually `http://localhost:8501`).

## Key Concepts Covered
- Initial Forward Price ($F_0(T)$) calculation.
- Mark-to-Market (MTM) Valuation ($V_t(T)$) for long and short positions.
- Impact of costs and benefits (income/carrying costs) on forward prices and MTM.
- Visualization of MTM evolution over time.
- Sensitivity of MTM to current spot price.
- Profit/Loss at maturity for various settlement scenarios.

## Contributing
Feel free to fork the repository, make improvements, and submit pull requests.

## License
© 2025 QuantUniversity. All Rights Reserved.

The purpose of this demonstration is solely for educational use and illustration. Any reproduction of this demonstration requires prior written consent from QuantUniversity. This lab was generated using the QuCreate platform. QuCreate relies on AI models for generating code, which may contain inaccuracies or errors.
