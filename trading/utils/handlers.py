from time import time
from typing import Any, Dict, Union

import requests
from requests.exceptions import HTTPError

from mysql.connector.errors import DatabaseError, PoolError
from mysql.connector.pooling import MySQLConnectionPool

__all__ = ['api_handler']

def api_handler(url: str,
                api_key: str, 
                timer:int=5, 
                retries:int=5) -> Union[requests.Response, Any, Dict]:
    r = {}
    try:
        r = requests.get(url, headers={'X-MBX-APIKEY': api_key})
        r = r.json()
        if r.status_code != 200:
            raise HTTPError('Not expected API response')
    except HTTPError as err:
        if r.status_code == 429 and retries != 0: # type: ignore
            print('\n\r{} API Response: {}... {}secs'.format(err, r.status_code, round(timer, 2))) # type: ignore
            time.sleep(timer)
            timer += 5
            retries -= 1
            return api_handler(url, api_key, timer, retries)
        elif r.status_code == 403: # type: ignore
            print('\n{} Sleeping... '.format(r.status_code)) # type: ignore
            return api_handler(url, api_key, timer)
        elif r.status_code == 418: # type: ignore
            print('\n{} API Key Banned!')
            time.sleep(3600)
            return api_handler(url,api_key, timer)
        # 5xx: Server side errors
        elif str(r.status_code).startswith('5'): # type: ignore 
            print('\n{} Binance probably down...'.format(r.status_code)) # type: ignore
            time.sleep(3600)
            return api_handler(url, api_key, timer)
    finally:
        return r

class DBHandler:

    db_host: str
    db_port: int
    db_username: str
    db_password: str
    db_name: str
    pool_size: int
    pool_name: str
    connected: bool

    def __init__(self, 
                 db_host, db_port,
                 db_username, db_password,
                 db_name, pool_name,
                 pool_size) -> None:
        self.db_host = db_host
        self.db_port = db_port
        self.db_username = db_username
        self.db_password = db_password
        self.db_name = db_name
        self.pool_name = pool_name
        self.pool_size = pool_size
        self.connected = False

    def __enter__(self):
        while not self.connected:
            try:
                connection_pool = MySQLConnectionPool(pool_name=self.pool_name,
                                                      pool_size=self.pool_size,
                                                      database=self.db_name,
                                                      user=self.db_username,
                                                      password=self.db_password,
                                                      host=self.db_host,
                                                      port=self.db_port,
                                                      pool_reset_session=False) 
                self.connection = connection_pool.get_connection()
                if self.connection.is_connected():
                    self.connected = True
                    print('Connected to %s' % self.connection.get_server_info()) 
                    return self.connection
            except PoolError as err:
                print('Connection failed due %s' % err)
            except DatabaseError as err:
                print("Encountered error while operating DB %s" % err)

    def __exit__(self, type, value, traceback):
        self.connection.close() 

