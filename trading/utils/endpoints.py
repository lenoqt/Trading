# type: ignore
from enum import Enum

__all__ = ['BinanceEndpoint']

class BinanceEndpoint(Enum):
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
