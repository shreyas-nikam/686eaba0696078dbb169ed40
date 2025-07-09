import pytest
from definition_eeb9f1d483f646238f6be69ccc3ab177 import calculate_forward_price_initial

@pytest.mark.parametrize("S0, r, T, PV0_I, PV0_C, expected", [
    # --- Valid Cases (Standard & Edge) ---

    # 1. Basic case, no income/costs (S0 * (1+r)^T)
    (100.0, 0.05, 1.0, 0.0, 0.0, 105.0),
    (50.0, 0.03, 0.5, 0.0, 0.0, 50.0 * (1.03**0.5)), # Approx 50.7439
    (200.0, 0.10, 2.0, 0.0, 0.0, 200.0 * (1.10**2)), # 200 * 1.21 = 242.0

    # 2. With income (S0 - PV0_I) * (1+r)^T
    (100.0, 0.05, 1.0, 10.0, 0.0, 94.5), # (100 - 10) * 1.05 = 90 * 1.05 = 94.5
    (75.0, 0.04, 3.0, 5.0, 0.0, (75.0 - 5.0) * (1.04**3)), # 70 * 1.124864 = 78.74048

    # 3. With costs (S0 + PV0_C) * (1+r)^T
    (100.0, 0.05, 1.0, 0.0, 10.0, 115.5), # (100 + 10) * 1.05 = 110 * 1.05 = 115.5
    (120.0, 0.06, 0.75, 0.0, 8.0, (120.0 + 8.0) * (1.06**0.75)), # 128 * 1.04473 = 133.72544

    # 4. With both income and costs (S0 - PV0_I + PV0_C) * (1+r)^T
    (100.0, 0.05, 1.0, 10.0, 5.0, 99.75), # (100 - 10 + 5) * 1.05 = 95 * 1.05 = 99.75
    (150.0, 0.08, 1.5, 20.0, 10.0, (150.0 - 20.0 + 10.0) * (1.08**1.5)), # 140 * 1.12249 = 157.1486

    # 5. T = 0 (maturity at inception) - F0(T) = S0 - PV0_I + PV0_C
    (100.0, 0.05, 0.0, 0.0, 0.0, 100.0),
    (100.0, 0.05, 0.0, 10.0, 5.0, 95.0), # (100 - 10 + 5)
    (50.0, 0.02, 0.0, 0.0, 0.0, 50.0),
    (0.0, 0.05, 0.0, 0.0, 0.0, 0.0), # S0=0, T=0

    # 6. r = 0 (zero risk-free rate) - F0(T) = S0 - PV0_I + PV0_C
    (100.0, 0.0, 1.0, 0.0, 0.0, 100.0),
    (100.0, 0.0, 5.0, 10.0, 5.0, 95.0),
    (200.0, 0.0, 0.25, 10.0, 0.0, 190.0),

    # 7. Small positive values for S0, r, T
    (1.0, 0.001, 0.1, 0.0, 0.0, 1.0000999500249875),
    (1.0, 0.001, 0.1, 0.01, 0.005, 0.9950999500249875),

    # 8. Large values for S0, r, T
    (100000.0, 0.1, 10.0, 5000.0, 2000.0, 251693.028639702),
    (1_000_000.0, 0.2, 20.0, 100_000.0, 50_000.0, (1_000_000 - 100_000 + 50_000) * (1.2**20)), # 950000 * 38.3375 = 36420625.0

    # 9. S0 = 0 (zero spot price)
    (0.0, 0.05, 1.0, 0.0, 0.0, 0.0),
    (0.0, 0.05, 1.0, 0.0, 10.0, 10.5), # (0 - 0 + 10) * 1.05 = 10.5
    (0.0, 0.05, 1.0, 10.0, 0.0, -10.5), # (0 - 10 + 0) * 1.05 = -10.5

    # 10. Negative effective initial investment (S0 - PV0_I + PV0_C < 0) - result should be negative
    (10.0, 0.05, 1.0, 15.0, 0.0, -5.25), # (10 - 15) * 1.05 = -5 * 1.05 = -5.25
    (5.0, 0.1, 2.0, 10.0, 2.0, -3.63), # (5 - 10 + 2) * (1.1**2) = -3 * 1.21 = -3.63

    # 11. PV values are negative (though unusual in financial context, float allows it)
    (100.0, 0.05, 1.0, -10.0, -5.0, 110.25), # (100 - (-10) + (-5)) * 1.05 = (100 + 10 - 5) * 1.05 = 105 * 1.05 = 110.25

    # --- Invalid Input Types (Python will raise TypeError) ---
    ('100.0', 0.05, 1.0, 0.0, 0.0, TypeError), # S0 as string
    (100.0, '0.05', 1.0, 0.0, 0.0, TypeError), # r as string
    (100.0, 0.05, '1.0', 0.0, 0.0, TypeError), # T as string
    (100.0, 0.05, 1.0, '10.0', 0.0, TypeError), # PV0_I as string
    (100.0, 0.05, 1.0, 0.0, '10.0', TypeError), # PV0_C as string
    (None, 0.05, 1.0, 0.0, 0.0, TypeError), # S0 as None
    (100.0, None, 1.0, 0.0, 0.0, TypeError), # r as None
    (100.0, 0.05, None, 0.0, 0.0, TypeError), # T as None
    (100.0, 0.05, 1.0, None, 0.0, TypeError), # PV0_I as None
    (100.0, 0.05, 1.0, 0.0, None, TypeError), # PV0_C as None
    ([100.0], 0.05, 1.0, 0.0, 0.0, TypeError), # S0 as list
    (100.0, 0.05, 1.0, 0.0, [10.0], TypeError), # PV0_C as list

    # --- Invalid Input Values (Financial/Mathematical domain errors leading to ValueError) ---
    # S0 negative (Spot price cannot be negative in financial context)
    (-100.0, 0.05, 1.0, 0.0, 0.0, ValueError),
    (-1.0, 0.01, 1.0, 0.0, 0.0, ValueError),
    # T negative (Time to maturity cannot be negative)
    (100.0, 0.05, -1.0, 0.0, 0.0, ValueError),
    (100.0, 0.05, -0.1, 0.0, 0.0, ValueError),
    # r <= -1.0 (Risk-free rate leading to 1+r <= 0, which is financially unsound for compounding).
    # This also naturally causes ValueError in Python for non-integer T.
    (100.0, -1.0, 0.5, 0.0, 0.0, ValueError), # (1 - 1.0)**0.5 = 0**0.5 -> 0.0, but should be caught by financial constraint
    (100.0, -1.1, 0.5, 0.0, 0.0, ValueError), # (1 - 1.1)**0.5 = (-0.1)**0.5 -> ValueError in Python
    (100.0, -2.0, 2.0, 0.0, 0.0, ValueError), # (1 - 2.0)**2.0 = (-1)**2.0 -> 1.0, but should be caught by financial constraint
    (100.0, -1.0, 1.0, 0.0, 0.0, ValueError), # For T=1.0, (1 - 1.0)**1.0 = 0.0. Still, r <= -1.0 is invalid financially.
])
def test_calculate_forward_price_initial(S0, r, T, PV0_I, PV0_C, expected):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            # The actual implementation of calculate_forward_price_initial should
            # include explicit checks to raise ValueError for financially invalid inputs
            # such as S0 < 0, T < 0, or r <= -1.0.
            # If the stub's underlying operations would raise TypeError (e.g., string input),
            # that is also caught.
            calculate_forward_price_initial(S0, r, T, PV0_I, PV0_C)
    else:
        # For floating point comparisons, use pytest.approx to account for precision differences
        result = calculate_forward_price_initial(S0, r, T, PV0_I, PV0_C)
        assert result == pytest.approx(expected)