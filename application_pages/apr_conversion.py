
import streamlit as st
import math

def run_apr_conversion_page():
    st.header("Annual Percentage Rate (APR) Conversion Utility")
    st.markdown(\"\"\"
This utility helps you convert Annual Percentage Rates (APR) between different compounding frequencies.
Ensuring rates are on a comparable compounding basis is crucial for accurate financial analysis and calculations.

### Formula for APR Conversion

The relationship between two equivalent APRs with different compounding frequencies is given by:

$$ \\left(1 + \\frac{APR_m}{m}\\right)^m = \\left(1 + \\frac{APR_n}{n}\\right)^n $$

Where:
- $APR_m$: Original Annual Percentage Rate compounded $m$ times per year.
- $m$: Original number of compounding periods per year.
- $APR_n$: Target Annual Percentage Rate compounded $n$ times per year.
- $n$: Target number of compounding periods per year.

To convert $APR_m$ (compounded $m$ times a year) to $APR_n$ (compounded $n$ times a year), the formula is rearranged to solve for $APR_n$:

$$ APR_n = n \\times \\left( \\left(1 + \\frac{APR_m}{m}\\right)^{\\frac{m}{n}} - 1 \\right) $$
\"\"\")

    st.sidebar.header("APR Conversion Inputs")

    original_apr = st.sidebar.number_input(
        "Original APR (e.g., 0.06 for 6%)",
        min_value=0.0,
        value=0.06,
        step=0.0001,
        format="%.4f",
        help="The Annual Percentage Rate to convert."
    )
    original_compounding_freq = st.sidebar.number_input(
        "Original Compounding Frequency (m)",
        min_value=1,
        value=2, # Semi-annual
        step=1,
        help="The number of times per year the original APR is compounded."
    )
    target_compounding_freq = st.sidebar.number_input(
        "Target Compounding Frequency (n)",
        min_value=1,
        value=12, # Monthly
        step=1,
        help="The number of times per year for the target APR compounding."
    )

    st.subheader("Conversion Results")

    if original_compounding_freq <= 0 or target_compounding_freq <= 0:
        st.error("Error: Compounding frequencies must be positive integers.")
        return

    # Calculate the equivalent effective annual rate first for robustness
    # (1 + APR_m/m)^m = (1 + EAR)
    # EAR = (1 + APR_m/m)^m - 1
    
    # Calculate the target APR
    # APR_n = n * ((1 + EAR)^(1/n) - 1)
    # Substituting EAR: APR_n = n * ((1 + APR_m/m)^(m/n) - 1)

    try:
        # Avoid division by zero if original_compounding_freq is 0
        if original_compounding_freq == 0:
            st.error("Error: Original compounding frequency cannot be zero.")
            return

        # Calculate the base term (1 + APR_m/m)
        base_term = 1 + (original_apr / original_compounding_freq)
        
        # Check for non-positive base to prevent math domain error for fractional powers
        if base_term <= 0:
            st.error("Error: The term (1 + Original APR / Original Compounding Frequency) must be positive.")
            return

        # Calculate the power (m/n)
        power_term = original_compounding_freq / target_compounding_freq

        # Calculate (1 + APR_m/m)^(m/n)
        intermediate_result = base_term ** power_term

        # Calculate APR_n
        target_apr = target_compounding_freq * (intermediate_result - 1)

        st.markdown(f"**Original APR (compounded {original_compounding_freq} times/year):** {original_apr:.4f} ({original_apr:.2%})")
        st.markdown(f"**Target Compounding Frequency (n):** {target_compounding_freq}")
        st.markdown(f"**Equivalent APR (compounded {target_compounding_freq} times/year):** {target_apr:.4f} ({target_apr:.2%})")

    except ZeroDivisionError:
        st.error("Error: Original Compounding Frequency (m) cannot be zero.")
    except ValueError as e:
        st.error(f"Calculation Error: {e}. Please ensure inputs result in valid mathematical operations (e.g., positive base for fractional powers).")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
