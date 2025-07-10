import pytest
from definition_7f9c2e3424ff4822860ea1e679fc6e0d import calculate_period_fraction

@pytest.mark.parametrize("start_month, end_month, days_in_year_basis, expected", [
    # Valid cases - standard calculations
    (0, 3, 360, pytest.approx(0.25)), # 3 months period, 360-day basis
    (3, 6, 360, pytest.approx(0.25)), # Standard 3x6 FRA
    (3, 6, 365, pytest.approx(0.25)), # Same 3x6 FRA, 365-day basis (days_in_year_basis cancels out per spec's algorithm)
    (6, 12, 360, pytest.approx(0.5)), # 6 months period
    (0, 12, 360, pytest.approx(1.0)), # 12 months period
    (1, 2, 365, pytest.approx(1/12.0)), # 1 month period
    (5, 17, 360, pytest.approx(1.0)), # 12 months period shifted

    # Invalid cases - ValueError (due to business logic constraints)
    (3, 3, 360, pytest.raises(ValueError, match="end_month must be greater than start_month")), # end_month == start_month
    (6, 3, 360, pytest.raises(ValueError, match="end_month must be greater than start_month")), # end_month < start_month
    (0, 0, 365, pytest.raises(ValueError, match="end_month must be greater than start_month")), # end_month == start_month (zero)
    (-1, 3, 360, pytest.raises(ValueError, match="start_month and end_month cannot be negative")), # Negative start_month
    (3, -1, 360, pytest.raises(ValueError, match="end_month must be greater than start_month")), # Negative end_month and end < start
    (-5, -2, 360, pytest.raises(ValueError, match="start_month and end_month cannot be negative")), # Negative start_month and end_month
    (3, 6, 0, pytest.raises(ValueError, match="days_in_year_basis must be a positive integer")), # days_in_year_basis is zero
    (3, 6, -360, pytest.raises(ValueError, match="days_in_year_basis must be a positive integer")), # days_in_year_basis is negative

    # Invalid cases - TypeError (due to incorrect input types)
    ('a', 6, 360, pytest.raises(TypeError, match="start_month, end_month, and days_in_year_basis must be integers")), # start_month not int
    (3, 'b', 360, pytest.raises(TypeError, match="start_month, end_month, and days_in_year_basis must be integers")), # end_month not int
    (3, 6, 'c', pytest.raises(TypeError, match="start_month, end_month, and days_in_year_basis must be integers")), # days_in_year_basis not int
    (3.0, 6, 360, pytest.raises(TypeError, match="start_month, end_month, and days_in_year_basis must be integers")), # start_month float
    (3, 6.0, 360, pytest.raises(TypeError, match="start_month, end_month, and days_in_year_basis must be integers")), # end_month float
    (3, 6, 360.0, pytest.raises(TypeError, match="start_month, end_month, and days_in_year_basis must be integers")), # days_in_year_basis float
    (None, 6, 360, pytest.raises(TypeError, match="start_month, end_month, and days_in_year_basis must be integers")), # start_month None
    (3, None, 360, pytest.raises(TypeError, match="start_month, end_month, and days_in_year_basis must be integers")), # end_month None
    (3, 6, None, pytest.raises(TypeError, match="start_month, end_month, and days_in_year_basis must be integers")), # days_in_year_basis None
    ([1], 6, 360, pytest.raises(TypeError, match="start_month, end_month, and days_in_year_basis must be integers")), # start_month list
    (3, [6], 360, pytest.raises(TypeError, match="start_month, end_month, and days_in_year_basis must be integers")), # end_month list
    (3, 6, [360], pytest.raises(TypeError, match="start_month, end_month, and days_in_year_basis must be integers")), # days_in_year_basis list
])
def test_calculate_period_fraction(start_month, end_month, days_in_year_basis, expected):
    if isinstance(expected, pytest.raises):
        with expected:
            calculate_period_fraction(start_month, end_month, days_in_year_basis)
    else:
        result = calculate_period_fraction(start_month, end_month, days_in_year_basis)
        assert result == expected