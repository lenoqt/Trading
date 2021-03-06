from enum import Enum


__all__ = ["BaseEnum", "BinanceEndpoints", "BinanceIntervals"]


class BaseEnum(str, Enum):
    def describe(self):
        """
        The describe function prints out the name and its value.

        :param self: Used to access variables that belong to the class.
        :return: name, value
        """
        return self.name, self.value


class BinanceEndpoints(BaseEnum):

    BASE_URL = "https://api.binance.com"
    # Endpoints SPOT (GET)
    _TEST = "/api/v3/ping"
    _TIME = "/api/v3/time"
    _INFO = "/api/v3/exchangeInfo"
    _ORDERBOOK = "/api/v3/depth"
    _TRADES = "/api/v3/trades"
    _HISTORICAL = "/api/v3/historicalTrades"
    _AGGREGATED = "/api/v3/aggTrades"
    _KLINES = "/api/v3/klines"
    _AVGPRICE = "/api/v3/avgPrice"
    _DAYSTATS = "/api/v3/ticker/24hr"
    _SYMBOLTPRICE = "/api/v3/ticker/price"
    _SYMBOOKT = "/api/v3/ticker/bookTicker"
    # FQDNs
    KLINE = (
        BASE_URL + _KLINES + "?symbol={}&interval={}&startTime={}&endTime={}&limit={}"
    )
    TEST = BASE_URL + _TEST
    TIME = BASE_URL + _TIME
    INFO = BASE_URL + _INFO
    ORDERBOOK = BASE_URL + _ORDERBOOK + "?symbol={}&limit={}"
    HISTORICAL = BASE_URL + _HISTORICAL + "?symbol={}&limit={}"
    TRADES = BASE_URL + _TRADES + "?symbol={}&limit={}"
    AGGREGATED = BASE_URL + _AGGREGATED + "?symbol={}&limit={}"
    AVGPRICE = BASE_URL + _AVGPRICE + "?symbol={}"
    DAYSTATS = BASE_URL + _DAYSTATS + "?symbol={}"
    SYMBOLTPRICE = BASE_URL + _SYMBOLTPRICE + "?symbol={}"
    SYMBOOKT = BASE_URL + _SYMBOOKT + "?symbol={}"


class BinanceIntervals(BaseEnum):
    # Intervals for public API
    INTERVAL_1MIN = "1m"
    INTERVAL_3MIN = "3m"
    INTERVAL_5MIN = "5m"
    INTERVAL_15MIN = "15m"
    INTERVAL_30MIN = "30m"
    INTERVAL_1H = "1h"
    INTERVAL_2H = "2h"
    INTERVAL_4H = "4h"
    INTERVAL_6H = "6h"
    INTERVAL_8H = "8h"
    INTERVAL_12H = "12h"
    INTERVAL_1D = "1d"
    INTERVAL_3D = "3d"
    INTERVAL_1W = "1w"
    INTERVAL_1M = "1M"
