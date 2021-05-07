import requests
import time
from requests.exceptions import HTTPError
import pandas as pd
from typing import Any, Dict, Union, Callable


BASE_URL = 'https://api.binance.com'
#Endpoints (GET)
TEST = '/api/v3/ping'
TIME = '/api/v3/time'
INFO = '/api/v3/exchangeInfo'
ORDERBOOK = '/api/v3/depth'
TRADES = '/api/v3/trades'
HISTORICAL = '/api/v3/historicalTrades'
AGGREGATED = '/api/v3/aggTrades'
KLINES = '/api/v3/klines'
AVGPRICE = '/api/v3/avgPrice'
DAYSTATS = '/api/v3/ticker/24hr'
SYMBOLTPRICE = '/api/v3/ticker/price'
SYMBOOKT = '/api/v3/ticker/bookTicker'

#Intervals for public API
INTERVALS = ['1m', '3m', '5m', '15m', '30m',
             '1h', '2h', '4h', '6h', '8h', '12h',
             '1d', '3d', '1w', '1M']

class Binance:
    
    api_key: str
    symbol: str
    interval: str
    startTime: int
    endTime: int
    limit: int

    def __init__(self, symbol,
                 api_key, interval,
                 startTime, endTime, limit = 500) -> None:
        self.symbol = symbol
        self.api_key = api_key
        self.interval = interval if interval in INTERVALS else '4h'
        self.startTime = startTime
        self.endTime = endTime
        self.limit = limit
    
    def api_handler(self, url:str, timer:int=5, retries:int=5) -> Union[Callable[[Any], requests.models.Response] , requests.models.Response, None]:
        r = None
        try:
            r = requests.get(url, headers={'X-MBX-APIKEY':self.api_key})
            if r.status_code != 200:
                raise HTTPError('Not expected API response')
        except HTTPError as err:
            if r.status_code == 429 and retries != 0:
                print('\n\r{} API Response: {}... {}secs'.format(err, r.status_code, round(timer, 2)))
                time.sleep(timer)
                timer += 5
                retries -= 1
                return self.api_handler(url, timer, retries)
            elif r.status_code == 403:
                print('\n{} Sleeping... '.format(r.status_code))
                return self.api_handler(url, timer)
            elif r.status_code == 418:
                print('\n{} API Key Banned!')
                time.sleep(3600)
                return self.api_handler(url, timer)
            # 5xx: Server side errors
            elif str(r.status_code).startswith('5'):
                print('\n{} Binance probably down...'.format(r.status_code))
                time.sleep(3600)
                return self.api_handler(url, timer)
        finally:
            return r
    
    def kline(self) -> pd.DataFrame:
        url = '%s%s?symbol=%s&interval=%s' % (BASE_URL, KLINES, self.symbol, self.interval)
        candlesticks = self.api_handler(url)
        headers = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume',
                   'Close time', 'Quote asset volume', 'No of trades',
                   'Taker buy base asset volume', 'Taker quote asset volume', 'Ignore']
        return pd.DataFrame(candlesticks.json(), columns=headers)

    def test_api(self) -> int:
        url = '%s%s' % (BASE_URL, TEST)
        test = self.api_handler(url)
        return test.status_code

    def check_time(self) -> Dict[str, int]:
        url = '%s%s' % (BASE_URL, TIME)
        server_time = self.api_handler(url)
        return server_time.json()

    def info(self) -> Dict[Any, Any]:
        url = '%s%s' % (BASE_URL, INFO)
        info = self.api_handler(url)
        return info.json()

    def order_book(self) -> pd.DataFrame:
        url = '%s%s?symbol=%s&limit=%s' % (BASE_URL, ORDERBOOK, self.symbol, self.limit)
        book = self.api_handler(url)
        return pd.DataFrame.from_dict(book.json())

    def trades(self, historical=False) -> pd.DataFrame:
        url = '%s%s?symbol=%s&limit=%s' % (BASE_URL, 
                                           HISTORICAL if historical else TRADES, 
                                           self.symbol, self.limit)
        trades = self.api_handler(url)
        headers = ["id", "price", "qty", "quoteQty", "time", "isBuyerMaker", "isBestMatch"]
        return pd.DataFrame(trades.json(), columns=headers)

