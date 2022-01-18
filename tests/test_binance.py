import pytest
from trading.utils import BinanceEndpoints


def test_object(binance):
    assert binance is not None


@pytest.mark.parametrize(
    "primary_keys_expected",
    [
        "Open time",
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
        "Close time",
        "Quote asset volume",
        "Number of trades",
        "Taker buy base asset volume",
        "Taker buy quote asset volume",
        "Ignore",
    ],
)
def test_kline(binance, primary_keys_expected):
    kline_data = binance.public_endpoints(BinanceEndpoints.KLINE, "GET")
    assert isinstance(kline_data, dict)
    assert len(kline_data) == 12
    assert primary_keys_expected in kline_data


def test_time(binance):
    time_data = binance.public_endpoints(BinanceEndpoints.TIME, "GET")
    assert "serverTime" in time_data
    assert len(time_data) == 1


def test_test(binance):
    test_data = binance.public_endpoints(BinanceEndpoints.TEST, "GET")
    assert test_data == {}


@pytest.mark.parametrize(
    "primary_keys_expected",
    ["timezone", "serverTime", "rateLimits", "exchangeFilters", "symbols"],
)
def test_info(binance, primary_keys_expected):
    info_data = binance.public_endpoints(BinanceEndpoints.INFO, "GET")
    assert primary_keys_expected in info_data


@pytest.mark.parametrize("primary_keys_expected", ["lastUpdateId", "bids", "asks"])
def test_orderbook(binance, primary_keys_expected):
    info_orderbook = binance.public_endpoints(BinanceEndpoints.ORDERBOOK, "GET")
    assert primary_keys_expected in info_orderbook


def test_historical(binance):
    with pytest.raises(ValueError) as e:
        info_historical = binance.public_endpoints(BinanceEndpoints.HISTORICAL, "GET")
