
from trading.utils.handlers import api_handler
from trading.utils.endpoints import BinanceEndpoint
from typing import Any, Dict


__all__ = ['Binance']

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
        self.interval = interval if interval in BinanceEndpoint.INTERVALS else '4h'
        self.startTime = startTime
        self.endTime = endTime
        self.limit = limit
    
    
    def kline(self) -> Dict:
        url = '%s%s?symbol=%s&interval=%s' % (BinanceEndpoint.BASE_URL, 
                BinanceEndpoint.KLINES, self.symbol, self.interval)
        candlesticks = api_handler(url)
        return candlesticks

    def test_api(self) -> int:
        url = '%s%s' % (BinanceEndpoint.BASE_URL, BinanceEndpoint.TEST)
        test = api_handler(url)
        return test.status_code

    def check_time(self) -> Dict[str, int]:
        url = '%s%s' % (BinanceEndpoint.BASE_URL, BinanceEndpoint.TIME)
        server_time = api_handler(url)
        return server_time.json()

    def info(self) -> Dict[Any, Any]:
        url = '%s%s' % (BinanceEndpoint.BASE_URL, BinanceEndpoint.INFO)
        info = api_handler(url)
        return info.json()

    def order_book(self) -> pd.DataFrame:
        url = '%s%s?symbol=%s&limit=%s' % (BinanceEndpoint.BASE_URL, BinanceEndpoint.ORDERBOOK, self.symbol, self.limit)
        book = api_handler(url)
        return pd.DataFrame.from_dict(book.json())

    def trades(self, historical=False) -> pd.DataFrame:
        url = '%s%s?symbol=%s&limit=%s' % (BinanceEndpoint.BASE_URL, 
                                           BinanceEndpoint.HISTORICAL if historical else BinanceEndpoint.TRADES, 
                                           self.symbol, self.limit)
        trades = api_handler(url)
        headers = ["id", "price", "qty", "quoteQty", "time", "isBuyerMaker", "isBestMatch"]
        return pd.DataFrame(trades.json(), columns=headers)

