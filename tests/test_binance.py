import pytest
import trading.utils as utils
import trading.binance as bi


def test_date():

    interval = utils.BinanceIntervals.INTERVAL_1D
    with pytest.raises(ValueError, match=".* greater than .*"):
        bi.Binance(
            symbol="BTCUSDT",
            start_time="2022-01-01 00:00:00.000000",
            end_time="2021-12-01 00:00:00.000000",
            interval=interval,
        )


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
    kline_data = binance.public_data(utils.BinanceEndpoints.KLINE, "GET")
    assert isinstance(kline_data, dict)
    assert len(kline_data) == 12
    assert primary_keys_expected in kline_data


def test_time(binance):
    time_data = binance.public_data(utils.BinanceEndpoints.TIME, "GET")
    assert "serverTime" in time_data
    assert len(time_data) == 1


def test_test(binance):
    test_data = binance.public_data(utils.BinanceEndpoints.TEST, "GET")
    assert test_data == {}


@pytest.mark.parametrize(
    "primary_keys_expected",
    ["timezone", "serverTime", "rateLimits", "exchangeFilters", "symbols"],
)
def test_info(binance, primary_keys_expected):
    info_data = binance.public_data(utils.BinanceEndpoints.INFO, "GET")
    assert primary_keys_expected in info_data


@pytest.mark.parametrize("primary_keys_expected", ["lastUpdateId", "bids", "asks"])
def test_orderbook(binance, primary_keys_expected):
    info_orderbook = binance.public_data(utils.BinanceEndpoints.ORDERBOOK, "GET")
    assert primary_keys_expected in info_orderbook


def test_historical(binance):
    with pytest.raises(ValueError, match=r".* api_key .*"):
        binance.public_data(utils.BinanceEndpoints.HISTORICAL, "GET")


# TODO: Assert data content
def test_trades(binance):
    info_trades = binance.public_data(utils.BinanceEndpoints.TRADES, "GET")
    assert len(info_trades) == binance.limit


def test_aggregated(binance):
    info_trades = binance.public_data(utils.BinanceEndpoints.TRADES, "GET")
    assert len(info_trades) == binance.limit


def test_avgprice(binance):
    binance.public_data(utils.BinanceEndpoints.AVGPRICE, "GET")
    assert 1


def test_daystats(binance):
    binance.public_data(utils.BinanceEndpoints.DAYSTATS, "GET")
    assert 1


def test_symbolprice(binance):
    binance.public_data(utils.BinanceEndpoints.SYMBOLTPRICE, "GET")
    assert 1


def test_symbolbook(binance):
    binance.public_data(utils.BinanceEndpoints.SYMBOOKT, "GET")
    assert 1
