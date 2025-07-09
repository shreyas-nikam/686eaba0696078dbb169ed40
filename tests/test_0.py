import pytest
import math
from definition_02759245efa947478a9906f8e99dbbcc import calculate_forward_price

@pytest.mark.parametrize("S0, rf, rd, T, expected", [
    # Standard valid cases
    # rf < rd (forward discount)
    (1.2, 0.01, 0.02, 1.0, 1.2 * math.exp((0.01 - 0.02) * 1.0)),
    (0.85, 0.005, 0.03, 0.75, 0.85 * math.exp((0.005 - 0.03) * 0.75)),
    # rf > rd (forward premium)
    (1.2, 0.02, 0.01, 1.0, 1.2 * math.exp((0.02 - 0.01) * 1.0)),
    (120.0, 0.04, 0.01, 2.0, 120.0 * math.exp((0.04 - 0.01) * 2.0)),
    # rf = rd (forward equals spot)
    (1.2, 0.01, 0.01, 1.0, 1.2),
    (95.0, 0.0, 0.0, 3.0, 95.0), # All zero rates
    # Negative interest rates (within typical financial ranges)
    (1.5, -0.005, 0.005, 0.5, 1.5 * math.exp((-0.005 - 0.005) * 0.5)),
    (1.3, -0.01, -0.005, 1.0, 1.3 * math.exp((-0.01 - (-0.005)) * 1.0)), # Both negative, rf < rd
    (1.3, -0.005, -0.01, 1.0, 1.3 * math.exp((-0.005 - (-0.01)) * 1.0)), # Both negative, rf > rd

    # Edge Cases
    # Zero time to maturity (T=0)
    (1.2, 0.01, 0.02, 0.0, 1.2),
    (99.9, 0.05, 0.0, 0.0, 99.9),
    # Zero initial spot rate (S0=0)
    (0.0, 0.01, 0.02, 1.0, 0.0),
    (0.0, -0.01, 0.05, 5.0, 0.0),
    # Very large values
    (1e9, 0.1, 0.0, 10.0, 1e9 * math.exp((0.1 - 0.0) * 10.0)),
    (1e12, 0.001, 0.0005, 50.0, 1e12 * math.exp((0.001 - 0.0005) * 50.0)),
    # Very small non-zero values
    (1e-9, 0.01, 0.005, 1e-9, 1e-9 * math.exp((0.01 - 0.005) * 1e-9)),
    (1.0, 1e-6, 1e-7, 1.0, 1.0 * math.exp((1e-6 - 1e-7) * 1.0)), # Very small rates

    # Invalid Inputs - Type Errors
    (None, 0.01, 0.02, 1.0, TypeError),
    ('abc', 0.01, 0.02, 1.0, TypeError),
    ([], 0.01, 0.02, 1.0, TypeError),
    (1.2, None, 0.02, 1.0, TypeError),
    (1.2, 0.01, 'xyz', 1.0, TypeError),
    (1.2, 0.01, 0.02, {}, TypeError),
    (1.2, 0.01, 0.02, [], TypeError),
    (None, None, None, None, TypeError), # All invalid
    (1.2, 0.01, 0.02, True, TypeError), # Boolean for T
    (1.2, False, 0.02, 1.0, TypeError), # Boolean for rf

    # Invalid Inputs - Value Errors (for S0 and T based on financial domain constraints)
    (-1.2, 0.01, 0.02, 1.0, ValueError), # S0 negative
    (-0.0001, 0.01, 0.02, 1.0, ValueError), # S0 slightly negative
    (1.2, 0.01, 0.02, -1.0, ValueError), # T negative
    (1.2, 0.01, 0.02, -0.0001, ValueError), # T slightly negative
])
def test_calculate_forward_price(S0, rf, rd, T, expected):
    """
    Test cases for the calculate_forward_price function, covering valid inputs,
    edge cases, and invalid inputs (TypeErrors and ValueErrors).
    """
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            calculate_forward_price(S0, rf, rd, T)
    else:
        result = calculate_forward_price(S0, rf, rd, T)
        # Use math.isclose for floating-point comparisons to account for precision errors
        assert math.isclose(result, expected, rel_tol=1e-9, abs_tol=1e-12)