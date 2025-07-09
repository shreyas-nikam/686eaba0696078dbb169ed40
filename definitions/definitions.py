
import pytest
from <your_module> import calculate_forward_price_initial

@pytest.mark.parametrize("S0, r, T, PV0_I, PV0_C, expected", [
    # Test Case 1: Basic scenario with no additional income or costs.
    # F_0(T) = (100 - 0 + 0) * (1 + 0.05)^1.0 = 100 * 1.05 = 105.0
    (100.0, 0.05, 1.0, 0.0, 0.0, 105.0),

    # Test Case 2: Scenario including present value of income (PV0_I > 0).
    # F_0(T) = (100 - 10 + 0) * (1 + 0.05)^1.0 = 90 * 1.05 = 94.5
    (100.0, 0.05, 1.0, 10.0, 0.0, 94.5),

    # Test Case 3: Scenario including present value of costs (PV0_C > 0).
    # F_0(T) = (100 - 0 + 5) * (1 + 0.05)^1.0 = 105 * 1.05 = 110.25
    (100.0, 0.05, 1.0, 0.0, 5.0, 110.25),
    
    # Test Case 4: Edge case - Zero time to maturity (T=0).
    # Formula: F_0(T) = (S_0 - PV_0(I) + PV_0(C))(1+r)^0 = S_0 - PV_0(I) + PV_0(C)
    # Expected: (100 - 10 + 5) * (1 + 0.05)^0 = 95 * 1 = 95.0
    (100.0, 0.05, 0.0, 10.0, 5.0, 95.0),

    # Test Case 5: Edge case - Invalid type for a parameter (e.g., 'r' is a string).
    # This should result in a TypeError when arithmetic operations are attempted.
    (100.0, 'invalid_rate', 1.0, 0.0, 0.0, TypeError),
])
def test_calculate_forward_price_initial(S0, r, T, PV0_I, PV0_C, expected):
    """
    Test cases for calculate_forward_price_initial covering expected functionality and edge cases,
    including invalid input types.
    """
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            calculate_forward_price_initial(S0, r, T, PV0_I, PV0_C)
    else:
        actual_F0_T = calculate_forward_price_initial(S0, r, T, PV0_I, PV0_C)
        assert actual_F0_T == pytest.approx(expected)
