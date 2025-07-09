
import pytest
import json
from <your_module> import parse_cash_flows

@pytest.mark.parametrize("cf_str, cf_type, expected_result", [
    # Test Case 1: Valid input with multiple cash flow items
    # Expected functionality: correctly parses a well-formed JSON string into a list of dictionaries.
    ('[{"amount": 100.0, "time_from_t0": 0.5}, {"amount": 50.0, "time_from_t0": 1.0}]', "dividends",
     [{"amount": 100.0, "time_from_t0": 0.5}, {"amount": 50.0, "time_from_t0": 1.0}]),

    # Test Case 2: Valid empty list input
    # Edge case: an empty cash flow list, which is a valid scenario representing no cash flows.
    ('[]', "costs", []),

    # Test Case 3: Invalid JSON format (e.g., missing closing bracket or invalid syntax)
    # Edge case: The input string is not a syntactically valid JSON.
    # The function is designed to catch json.JSONDecodeError and return an empty list.
    ('{"amount": 200, "time_from_t0": 0.25', "benefits", []), # Malformed JSON

    # Test Case 4: Valid JSON, but the top-level element is a dictionary, not a list
    # Edge case: The JSON is parsable but does not conform to the expected list structure.
    # The function is designed to catch a ValueError (from `if not isinstance(cf_list, list)`) and return an empty list.
    ('{"amount": 200, "time_from_t0": 0.25}', "benefits", []),

    # Test Case 5: Valid JSON list, but an item has an incorrect data type for 'amount' or 'time_from_t0'
    # Edge case: A cash flow dictionary within the list has values of the wrong type (e.g., string for amount).
    # The function is designed to catch a TypeError (from `if not isinstance(cf['amount'], (int, float))`) and return an empty list.
    ('[{"amount": "seventy five", "time_from_t0": 0.5}]', "dividends", []),
])
def test_parse_cash_flows(cf_str, cf_type, expected_result):
    # The parse_cash_flows function handles errors by printing a message and returning an empty list.
    # Therefore, we directly assert the returned value, which will be the parsed list for valid inputs
    # or an empty list for any of the defined error conditions.
    actual_result = parse_cash_flows(cf_str, cf_type)
    assert actual_result == expected_result
