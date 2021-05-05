import requests
import json
import time
from requests.exceptions import HTTPError
import pandas as pd
from typing import Any, Union, Callable
import re

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
        self.interval = interval
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
        url = 'https://api.binance.com/api/v3/klines?symbol='+self.symbol+'&interval='+self.interval
        candlesticks = self.api_handler(url)
        headers = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume',
                   'Close time', 'Quote asset volume', 'No of trades',
                   'Taker buy base asset volume', 'Taker quote asset volume', 'Ignore']
        return pd.DataFrame(candlesticks.json(), columns=headers)

