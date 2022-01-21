def test_api_handler(rest_call):
    print(rest_call)
    expected, test_case_obj = rest_call
    if hasattr(test_case_obj, "get"):
        assert test_case_obj.get("response") == expected
    elif not hasattr(test_case_obj, "get"):
        test_case_obj.status_code == expected
