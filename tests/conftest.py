import json
import trading.binance as bi
import trading.utils as utils
import pytest


@pytest.fixture(scope="session")
def binance():
    interval = utils.BinanceIntervals.INTERVAL_1D
    binance = bi.Binance(
        symbol="BTCUSDT",
        start_time="2021-12-01 00:00:00.000000",
        end_time="2022-01-01 00:00:00.000000",
        interval=interval,
    )
    return binance


@pytest.fixture(scope="session")
def binance_with_apikey():
    interval = utils.BinanceIntervals.INTERVAL_1D
    binance = bi.Binance(
        symbol="BTCUSDT",
        start_time="2021-12-01 00:00:00.000000",
        end_time="2022-01-01 00:00:00.000000",
        interval=interval,
        api_key="a4db08b7-5729-4ba9-8c08-f2df493465a1",
    )
    return binance


@pytest.fixture(scope="module")
def endpoints():
    with open("tests/endpoints.json") as infile:
        d = json.loads(infile.read())
        return d


@pytest.fixture(scope="module")
def rest_call(endpoints):
    expected, test_obj = endpoints.popitem()
    yield expected, utils.api_handler("GET", test_obj)
