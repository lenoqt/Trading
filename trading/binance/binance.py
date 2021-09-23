from typing import Any, Dict, Union
from requests import Response
from trading.utils.endpoints import BinanceEndpoint
from trading.utils.handlers import api_handler


__all__ = ['Binance']



class Binance:
    
    api_key: str
    symbol: str
    interval: BinanceEndpoint
    start_time: int
    end_time: int
    limit: int
    
    def __init__(self, symbol,
                 api_key, start_time=0, end_time=0, 
                 limit = 500, interval = f'{BinanceEndpoint._4H}') -> None:
        self.symbol = symbol
        self.api_key = api_key 
        self.interval = interval
        self.start_time = start_time
        self.end_time = end_time
        self.limit = limit
    
    def public(self, endpoint:BinanceEndpoint) -> Union[Response, Any, Dict]:
        """
        Method to extract data from public APIs from Binance
        """

        if BinanceEndpoint.KLINE_FQDN:
            url = endpoint.format(self.symbol, self.interval,self.start_time, self.end_time, self.limit) 
            data = api_handler(url=url, api_key=self.api_key)
            columns = ('Open time','Open High','Low Close',
                       'Volume','Close time','Quote asset volume'
                       'Number of trades','Taker buy base asset volume',
                       'Taker buy quote asset volume','Ignore')
            return dict(zip(columns, zip(*data)))
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
