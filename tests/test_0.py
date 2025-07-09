import pytest
import json # Not strictly needed for the test file itself for execution, but good for context if one were to debug
from definition_904640b1f6b14316b292c9379549f19e import parse_cash_flows

@pytest.mark.parametrize(
    "cf_str, cf_type, expected_output, expected_err_msg_part",
    [
        # --- Valid Inputs (Successful Parsing) ---
        ('[]', 'empty', [], None),
        ('[{"amount": 10, "time_from_t0": 0.5}]', 'single_cf_float', [{'amount': 10, 'time_from_t0': 0.5}], None),
        ('[{"amount": 20, "time_from_t0": 1}]', 'single_cf_int', [{'amount': 20, 'time_from_t0': 1}], None),
        ('[{"amount": 5, "time_from_t0": 0.1}, {"amount": 15.0, "time_from_t0": 1.2}]', 'multiple_cf', [{'amount': 5, 'time_from_t0': 0.1}, {'amount': 15.0, 'time_from_t0': 1.2}], None),
        ('[{"amount": -5, "time_from_t0": 0.1}]', 'negative_amount', [{'amount': -5, 'time_from_t0': 0.1}], None),
        ('[{"amount": 0, "time_from_t0": 0}]', 'zero_amount_time', [{'amount': 0, 'time_from_t0': 0}], None),
        ('[{"amount": 10, "time_from_t0": 0.5, "extra_key": "value"}]', 'extra_key', [{'amount': 10, 'time_from_t0': 0.5, 'extra_key': 'value'}], None),
        ('[{"amount": 10.0, "time_from_t0": 0.0}]', 'float_zero_time', [{'amount': 10.0, 'time_from_t0': 0.0}], None),
        
        # --- Invalid JSON Format (Returns [] and prints JSONDecodeError message) ---
        ('not a json string', 'invalid_json', [], "Error: Invalid JSON format for invalid_json"),
        ('[{"amount": 10, "time_from_t0": 0.5', 'unclosed_bracket', [], "Error: Invalid JSON format for unclosed_bracket"),
        ('{"amount": 10, "time_from_t0": 0.5}]', 'missing_open_bracket', [], "Error: Invalid JSON format for missing_open_bracket"),
        ('', 'empty_string', [], "Error: Invalid JSON format for empty_string"),
        ('[', 'partial_json', [], "Error: Invalid JSON format for partial_json"),
        
        # --- Valid JSON, but Invalid Structure/Types (Returns [] and prints ValueError/TypeError message) ---
        # Case: Top-level not a list (ValueError)
        ('{"amount": 10, "time_from_t0": 0.5}', 'object_not_list', [], "Error validating object_not_list: object_not_list input must be a list."), 
        
        # Case: List items are not dictionaries (ValueError)
        ('[1, 2, 3]', 'list_of_non_dicts', [], "Error validating list_of_non_dicts: Each list_of_non_dicts item must be a dictionary with 'amount' and 'time_from_t0'."),
        ('[{"amount": 10, "time_from_t0": 0.5}, "not_a_dict"]', 'mixed_types', [], "Error validating mixed_types: Each mixed_types item must be a dictionary with 'amount' and 'time_from_t0'."),
        
        # Case: Dictionary items missing required keys (ValueError)
        ('[{"amount": 10}]', 'missing_time_key', [], "Error validating missing_time_key: Each missing_time_key item must be a dictionary with 'amount' and 'time_from_t0'."),
        ('[{"time_from_t0": 0.5}]', 'missing_amount_key', [], "Error validating missing_amount_key: Each missing_amount_key item must be a dictionary with 'amount' and 'time_from_t0'."),
        ('[{"amount": 10, "time_from_t0": 0.5, "extra_key": 1}, {"no_amount": 1, "no_time": 1}]', 'mixed_valid_invalid_keys', [], "Error validating mixed_valid_invalid_keys: Each mixed_valid_invalid_keys item must be a dictionary with 'amount' and 'time_from_t0'."),
        
        # Case: Amount or time_from_t0 not numeric (TypeError)
        ('[{"amount": "ten", "time_from_t0": 0.5}]', 'amount_not_numeric_str', [], "Error validating amount_not_numeric_str: Amount and time for amount_not_numeric_str must be numeric."),
        ('[{"amount": 10, "time_from_t0": "half"}]', 'time_not_numeric_str', [], "Error validating time_not_numeric_str: Amount and time for time_not_numeric_str must be numeric."),
        ('[{"amount": 10, "time_from_t0": null}]', 'time_is_none', [], "Error validating time_is_none: Amount and time for time_is_none must be numeric."),
        ('[{"amount": null, "time_from_t0": 0.5}]', 'amount_is_none', [], "Error validating amount_is_none: Amount and time for amount_is_none must be numeric."),
        ('[{"amount": 10, "time_from_t0": 0.5}, {"amount": "twenty", "time_from_t0": 1.0}]', 'one_invalid_item_type', [], "Error validating one_invalid_item_type: Amount and time for one_invalid_item_type must be numeric."),
        ('[{"amount": true, "time_from_t0": 0.5}]', 'amount_is_bool', [], "Error validating amount_is_bool: Amount and time for amount_is_bool must be numeric."),
        ('[{"amount": 10, "time_from_t0": false}]', 'time_is_bool', [], "Error validating time_is_bool: Amount and time for time_is_bool must be numeric."),

        # --- Edge cases for cf_type parameter (no expected error message part if successful) ---
        ('[]', '', [], None), # empty cf_type, successful parse
        ('[]', 'a_very_long_and_descriptive_cash_flow_type_name_to_test_long_string_in_error_message', [], None), # long cf_type, successful parse
        ('[{"amount": "a", "time_from_t0": 1}]', 'long_cf_type_error', [], "Error validating long_cf_type_error: Amount and time for long_cf_type_error must be numeric."), # long cf_type, error case

        # --- Non-string inputs for cf_str (caught by TypeError in json.loads, then by the function's TypeError handler) ---
        (None, 'None_input', [], "Error validating None_input: the JSON object must be str, bytes or bytearray, not NoneType"), 
        (123, 'int_input', [], "Error validating int_input: the JSON object must be str, bytes or bytearray, not int"), 
        (True, 'bool_input', [], "Error validating bool_input: the JSON object must be str, bytes or bytearray, not bool"), 
        (['{"amount": 10, "time_from_t0": 0.5}'], 'list_input_direct', [], "Error validating list_input_direct: the JSON object must be str, bytes or bytearray, not list"),
        (b'[{"amount": 10, "time_from_t0": 0.5}]', 'bytes_input', [{'amount': 10, 'time_from_t0': 0.5}], None), # bytes input is valid for json.loads
    ]
)
def test_parse_cash_flows(cf_str, cf_type, expected_output, expected_err_msg_part, capsys):
    """
    Tests the parse_cash_flows function for various valid and invalid inputs,
    checking both the return value and printed error messages.
    """
    result = parse_cash_flows(cf_str, cf_type)
    assert result == expected_output

    captured = capsys.readouterr()
    if expected_err_msg_part:
        # Check if the expected part of the error message is present in stdout
        # The exact message can vary slightly by Python version or specific error,
        # so checking for a key part is more robust.
        assert expected_err_msg_part in captured.out
        # Ensure nothing is printed to stderr as per the function's implementation
        assert captured.err == "" 
    else:
        # For successful cases, no output to stdout or stderr is expected
        assert captured.out == ""
        assert captured.err == ""

