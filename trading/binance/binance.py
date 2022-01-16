from typing import Any, Dict, Union, Optional
from dataclasses import dataclass, field
from requests import Response
from datetime import datetime
from trading.utils.endpoints import BinanceEndpoints, BinanceIntervals
from trading.utils.handlers import api_handler


__all__ = ['Binance']


@dataclass
class Binance:
    
    symbol: str
    start_time: datetime 
    end_time: datetime
    interval: BinanceIntervals = field(default=BinanceIntervals.INTERVAL_4H, repr=True)
    api_key: Optional[str] = None
    secret: Optional[str] = None
    limit: int = 1000
    
    def __post__init__(self):
        if self.start_time >= self.end_time:
            raise ValueError(f"Value {self.start_time}, can't be greater than {self.end_time}")
    
    def public(self, endpoint: BinanceEndpoints, method: str) -> Union[Response, Any, Dict]:
        """
        Method to extract data from public APIs from Binance
        API Key or Secret is not necessary for this instance.
        """
        match endpoint:
            
            case BinanceEndpoints.KLINE:
                url = endpoint.format(self.symbol, self.interval,self.start_time, self.end_time, self.limit) 
                data = api_handler(method, url)
                # TODO: Eliminate boilerplate code like this
                columns = ['Open time','Open','High',
                           'Low','Close','Volume',
                           'Close time','Quote asset volume',
                           'Number of trades', 'Taker buy base asset volume',
                           'Taker buy quote asset volume', 'Ignore']
                return dict(zip(columns, zip(*data)))
            case BinanceEndpoints.TEST | BinanceEndpoints.TIME | BinanceEndpoints.INFO:
                return api_handler(method, endpoint.value) 
            case BinanceEndpoints.ORDERBOOK | BinanceEndpoints.HISTORICAL | BinanceEndpoints.TRADES:
                url = endpoint.format(self.symbol, self.limit)
                return api_handler(method, url)
            case _:
                raise ValueError('Value %s is not a public endpoint' % endpoint.value)
