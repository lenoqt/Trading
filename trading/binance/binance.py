# mypy: ignore-errors
"""mypy does not support match statements https://github.com/python/mypy/issues/11829
"""
import ciso8601 as dt
from typing import Any, Dict, Union, Optional
from dataclasses import dataclass, field
from requests import Response
from trading.utils.endpoints import BinanceEndpoints, BinanceIntervals
from trading.utils.handlers import api_handler

__all__ = ['Binance']


@dataclass
class Binance:

    symbol: str
    start_time: str  # Should be a ISO8601 i.e 2016-09-01 10:11:12.123456
    end_time: str  # Should be a ISO8601 i.e 2016-09-01 10:11:12.123456
    interval: BinanceIntervals = field(default=BinanceIntervals.INTERVAL_4H, repr=True)
    api_key: Optional[str] = None
    secret: Optional[str] = None
    limit: int = 1000
    __start: Any = field(init=False)
    __end: Any = field(init=False)

    def __post_init__(self):
        self.__start = dt.parse_datetime(self.start_time)
        self.__end = dt.parse_datetime(self.end_time)
        if self.__start >= self.__end:
            raise ValueError(f"Value {self.start_time}, cannot be greater than {self.end_time}")
        self.__start = self.__start.strftime("%s%f")[:13]
        self.__end = self.__end.strftime("%s%f")[:13]

    def public_data(self, endpoint: BinanceEndpoints, method: str) -> Union[Response, Any, Dict]:
        """
        Method to extract data from public APIs from Binance
        API Key or Secret is not necessary for this instance,
        except for the case of HISTORICAL endpoint.
        """
        match endpoint:
            case BinanceEndpoints.KLINE:
                url = endpoint.format(self.symbol, self.interval, self.__start, self.__end, self.limit)
                data = api_handler(method, url)
                # TODO: Eliminate boilerplate code like this
                columns = ['Open time', 'Open', 'High',
                           'Low', 'Close', 'Volume',
                           'Close time', 'Quote asset volume',
                           'Number of trades', 'Taker buy base asset volume',
                           'Taker buy quote asset volume', 'Ignore']
                return dict(zip(columns, zip(*data)))

            case (BinanceEndpoints.TEST | BinanceEndpoints.TIME | BinanceEndpoints.INFO):
                return api_handler(method, endpoint.value)

            case (BinanceEndpoints.ORDERBOOK
                    | BinanceEndpoints.HISTORICAL
                    | BinanceEndpoints.TRADES
                    | BinanceEndpoints.AGGREGATED):
                if endpoint == BinanceEndpoints.HISTORICAL and self.api_key is None:
                    raise ValueError("Set api_key in order to access to historical data")
                url = endpoint.format(self.symbol, self.limit)
                return api_handler(method, url)

            case (BinanceEndpoints.AVGPRICE
                  | BinanceEndpoints.DAYSTATS
                  | BinanceEndpoints.SYMBOLTPRICE
                  | BinanceEndpoints.SYMBOOKT):
                url = endpoint.format(self.symbol)
                return api_handler(method, url)
            case _:
                raise ValueError('Value %s is not a public endpoint' % endpoint.value)

    def private_data(self):
        raise NotImplementedError
