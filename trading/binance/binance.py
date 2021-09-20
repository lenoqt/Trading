from typing import Any, Dict, Union
from requests import Response
from trading.utils.endpoints import BinanceEndpoint
from trading.utils.handlers import api_handler


__all__ = ['Binance']



class Binance:
    
    api_key: str
    symbol: str
    interval: BinanceEndpoint
    startTime: int
    endTime: int
    limit: int
    
    def __init__(self, symbol,
                 api_key, startTime, endTime, 
                 limit = 500, interval = f'{BinanceEndpoint._4H}') -> None:
        self.symbol = symbol
        self.api_key = api_key 
        self.interval = interval
        self.startTime = startTime
        self.endTime = endTime
        self.limit = limit
    
    def public(self, endpoint:BinanceEndpoint) -> Union[Response, Any, Dict]:
        """
        Method to extract data from public APIs from Binance
        """

        if BinanceEndpoint.KLINE_FQDN:
            url = endpoint % (self.symbol, self.interval) 
            return api_handler(url=url, api_key=self.api_key)
        elif BinanceEndpoint.TEST_FQDN or \
                BinanceEndpoint.TIME_FQDN or \
                BinanceEndpoint.INFO_FQDN:
            return api_handler(url=f"{endpoint}", api_key=self.api_key) 
        elif BinanceEndpoint.ORDERBOOK_FQDN or \
                BinanceEndpoint.HISTORICAL_FQDN or \
                BinanceEndpoint.TRADES_FQDN:
            url = endpoint % (self.symbol, self.limit)
            return api_handler(url=url, api_key=self.api_key)
        else:
            raise ValueError('Value %s is not a public endpoint' % endpoint)
