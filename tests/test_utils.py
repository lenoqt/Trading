from enum import Enum
import pytest
import trading.utils as utils
from trading.utils import BaseEnum, BinanceEndpoints, BinanceIntervals


def test_api_handler(rest_call):
    expected, test_case_obj = rest_call
    if hasattr(test_case_obj, "get"):
        assert test_case_obj.get("response") == expected
    else:
        test_case_obj.status_code == expected


def test_api_handler_less_than_zero():
    with pytest.raises(ValueError, match=r".* greater .*"):
        utils.api_handler("GET", "https://fakeurl", retries=-11)
        utils.api_handler("GET", "https://fakeurl", timer=-121213)


def test_signature(signed):
    expected = b"7Yean+DStMUBf24rUZ2loBIU03g5WwGQ/BRhImhMPy0="
    assert signed == expected


def test_enum():
    assert issubclass(BaseEnum, Enum)
    assert issubclass(BaseEnum, str)
    assert issubclass(BinanceEndpoints, BaseEnum)
    assert issubclass(BinanceIntervals, BaseEnum)
    describe_method = getattr(BaseEnum, "describe")
    assert callable(describe_method)
