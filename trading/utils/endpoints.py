# type: ignore
from enum import Enum


__all__ = ['BinanceEndpoint']

class BinanceEndpoint(str, Enum):

    BASE_URL = 'https://api.binance.com'
    # Endpoints (GET) 
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
    # FQDNs
    KLINE_FQDN = BASE_URL + KLINES + '?symbol=%s&interval=%s'
    TEST_FQDN = BASE_URL + TEST 
    TIME_FQDN = BASE_URL + TIME 
    INFO_FQDN = BASE_URL + INFO 
    ORDERBOOK_FQDN = BASE_URL + ORDERBOOK + 'symbol=%s&limit=%s' 
    HISTORICAL_FQDN = BASE_URL + HISTORICAL + '?symbol=%s&limit=%s' 
    TRADES_FQDN = BASE_URL + TRADES + '?symbol=%s&limit=%s' 
    # Intervals for public API 
    
    _1MIN = '1m'
    _3MIN = '3m'
    _5MIN = '5m'
    _15MIN = '15m'
    _30MIN = '30m'
    _1H = '1h'
    _2H = '2h'
    _4H = '4h'
    _6H = '6h'
    _8H = '8h'
    _12H = '12h'
    _1D = '1d'
    _3D = '3d'
    _1W = '1w'
    _1M = '1M'
    
    def describe(self):
        return self.name, self.value

