
import pytest
import math
from <your_module> import calculate_forward_price

@pytest.mark.parametrize("S0, rf, rd, T, expected", [
    # Test case 1: Standard positive inputs and positive interest rate differential.
    # Expected functionality based on covered interest rate parity formula.
    (100.0, 0.05, 0.03, 1.0, 100.0 * math.exp((0.05 - 0.03) * 1.0)),
    # Test case 2: Zero time to maturity (T=0).
    # Edge case: The forward price should be equal to the spot price, as exp(0) = 1.
    (150.0, 0.02, 0.04, 0.0, 150.0),
    # Test case 3: Equal interest rates (rf=rd).
    # Edge case: The forward price should be equal to the spot price, as the differential is zero, leading to exp(0) = 1.
    (80.0, 0.07, 0.07, 2.0, 80.0),
    # Test case 4: Negative foreign interest rate and overall negative differential.
    # This covers a realistic scenario in certain market conditions (e.g., central bank negative rates).
    (120.0, -0.01, 0.05, 0.5, 120.0 * math.exp((-0.01 - 0.05) * 0.5)),
    # Test case 5: Invalid input type for 'T' (e.g., string instead of float).
    # Expects a TypeError, demonstrating robustness and basic input validation.
    (100.0, 0.05, 0.03, "one_year", TypeError),
])
def test_calculate_forward_price(S0, rf, rd, T, expected):
    if isinstance(expected, type) and issubclass(expected, Exception):
        # If the expected outcome is an exception type, assert that the function raises that exception.
        with pytest.raises(expected):
            calculate_forward_price(S0, rf, rd, T)
    else:
        # For valid inputs, calculate the result and assert it matches the expected value.
        # Use pytest.approx for robust float comparisons due to potential precision issues with exponential calculations.
        result = calculate_forward_price(S0, rf, rd, T)
        assert result == pytest.approx(expected)
