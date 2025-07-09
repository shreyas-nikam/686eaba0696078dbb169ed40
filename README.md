
# Forward Contracts with Costs & Benefits Simulator

This Streamlit application provides an interactive platform for understanding the pricing and valuation of forward contracts on underlying assets that incur additional costs (e.g., storage) or provide benefits (e.g., dividends). It demonstrates how these cash flows influence the forward price at inception ($F_0(T)$) and the mark-to-market (MTM) value ($V_t(T)$) throughout the contract's life.

## Features

*   **Illustrates No-Arbitrage Conditions:** Understand the theoretical basis of forward pricing.
*   **Impact Analysis:** Analyze the effect of discrete costs and benefits on forward prices and MTM values.
*   **Visual Representation:** Gain insights from dynamic charts showing MTM evolution and sensitivity.
*   **Comprehensive Valuation:** Incorporates discrete cash flows for realistic modeling.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

*   Python 3.9+
*   pip (Python package installer)
*   Docker (optional, for containerized deployment)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```
    (Note: Replace `<repository_url>` and `<repository_name>` with the actual values once the repository is created.)

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

#### Locally

This will open the application in your default web browser at `http://localhost:8501`.

#### Using Docker

1.  **Build the Docker image:**
    ```bash
    docker build -t forward-contracts-app .
    ```

2.  **Run the Docker container:**
    ```bash
    docker run -p 8501:8501 forward-contracts-app
    ```

    Then, open your web browser and navigate to `http://localhost:8501`.

## Usage

*   Adjust parameters like **Initial Spot Price**, **Maturity**, **Risk-Free Rate**, **Current Time**, and **Current Spot Price** using the interactive widgets.
*   Input **Dividends** and **Costs** as JSON arrays to simulate discrete cash flows.
*   Select your **Position Type** (long/short) for MTM valuation.
*   Observe real-time updates in **Forward Price**, **MTM Value**, and interactive **Charts**.

## Formulas

The application uses the following core formulas:

*   **Forward price at inception ($F_0(T)$) with costs/benefits:**
    $$F_0(T) = (S_0 - PV_0(I) + PV_0(C))(1 + r)^T$$
    Where $PV_0(I) = \sum_{j} I_j (1 + r)^{-t_j^I}$ (present value of benefits/dividends) and $PV_0(C) = \sum_{k} C_k (1 + r)^{-t_k^C}$ (present value of costs).

*   **MTM value during the life of the contract (long position):**
    $$V_t(T) = (S_t - PV_t(I) + PV_t(C)) - F_0(T)(1 + r)^{-(T-t)}$$
    Where $PV_t(I)$ and $PV_t(C)$ are the present values of *remaining* benefits and costs from time $t$ to maturity $T$.

*   **MTM value for a short position:**
    $$V_t(T)_{short} = -V_t(T)_{long}$$

*   **Present value of cash flows:**
    $$PV_t(CF) = \sum_{j | t_j^{CF} \ge t} CF_j (1 + r)^{-(t_j^{CF} - t)}$$

## License

© 2025 QuantUniversity. All Rights Reserved.

The purpose of this demonstration is solely for educational use and illustration. Any reproduction of this demonstration requires prior written consent from QuantUniversity. This lab was generated using the QuCreate platform. QuCreate relies on AI models for generating code, which may contain inaccuracies or errors.
