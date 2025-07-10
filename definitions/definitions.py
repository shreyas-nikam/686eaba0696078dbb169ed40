
import pytest
from <your_module> import calculate_period_fraction

@pytest.mark.parametrize("start_month, end_month, days_in_year_basis, expected", [
    # Test case 1: Standard 3x6 FRA (3-month period) using 360-day basis.
    # As per the docstring's calculation logic: (end_month - start_month) / 12 = (6 - 3) / 12 = 0.25
    (3, 6, 360, 0.25),
    # Test case 2: Smallest valid period (1 month) with a non-terminating decimal result, using 365-day basis.
    # This confirms that the 'days_in_year_basis' cancels out in the calculation, resulting in (1 - 0) / 12 = 1/12.
    (0, 1, 365, pytest.approx(1/12)),
    # Test case 3: Edge case - end_month equals start_month.
    # The docstring explicitly states "Must be greater than start_month", implying a ValueError.
    (6, 6, 360, ValueError),
    # Test case 4: Edge case - end_month is less than start_month (results in a negative period).
    # The docstring explicitly states "Must be greater than start_month", implying a ValueError.
    (6, 3, 360, ValueError),
    # Test case 5: Edge case - days_in_year_basis is zero.
    # The intermediate `days_in_period` would be (end_month - start_month) * (0 / 12), which is 0.
    # Dividing this by `days_in_year_basis` (0) results in a ZeroDivisionError (0/0).
    (3, 6, 0, ZeroDivisionError),
])
def test_calculate_period_fraction(start_month, end_month, days_in_year_basis, expected):
    try:
        result = calculate_period_fraction(start_month, end_month, days_in_year_basis)
        # Use pytest.approx for floating-point comparisons to account for potential precision issues.
        assert result == pytest.approx(expected)
    except Exception as e:
        # If an exception is expected, assert that the raised exception is of the expected type.
        assert isinstance(e, expected)
