import pytest
from trading.utils import BinanceEndpoints


def test_object(binance):
    assert binance is not None


def test_kline(binance):
    kline_data = binance.public_endpoints(BinanceEndpoints.KLINE, "GET")
    assert isinstance(kline_data, dict)
    assert len(kline_data) == 12
