from requests import request, Response
import hashlib
import hmac
import base64
import re
from typing import Any, Dict, Union
from time import time
from requests.exceptions import HTTPError
from mysql.connector.errors import DatabaseError, PoolError
from mysql.connector.pooling import MySQLConnectionPool

__all__ = ['api_handler', 'DBHandler', 'signature']

def api_handler(method: str,
                endpoint: str,
                api_key: str,
                secret: str,
                timer:int=5, 
                retries:int=5) -> Union[Response, Any, Dict]:
    r = {}
    try:
        message = re.search(r'\?([\s\S]*)$', endpoint)
        sig = signature(secret, message.group(1)) # type: ignore
        endpoint = endpoint + f"&signature={sig}"
        r = request(method, endpoint, headers={'X-MBX-APIKEY': api_key})
        r = r.json()
        if r.status_code != 200:
            r.raise_for_status()
    except HTTPError as err:
        if r.status_code == 429 and retries != 0: # type: ignore
            print('\n\r{} API Response: {}... {}secs'.format(err, r.status_code, round(timer, 2))) # type: ignore
            time.sleep(timer)
            timer += 5
            retries -= 1
            return api_handler(method, endpoint, api_key, secret,  timer, retries)
        elif r.status_code == 403: # type: ignore
            print('\n{} Sleeping... '.format(r.status_code)) # type: ignore
            return api_handler(method, endpoint, api_key, secret,  timer)
        elif r.status_code == 418: # type: ignore
            print('\n{} API Key Banned!')
            time.sleep(3600)
            return api_handler(method, endpoint,api_key, secret,  timer)
        # 5xx: Server side errors
        elif str(r.status_code).startswith('5'): # type: ignore 
            print('\n{} Binance probably down...'.format(r.status_code)) # type: ignore
            time.sleep(3600)
            return api_handler(method, endpoint, api_key, secret, timer)
    finally:
        return r

def signature(secret: Union[bytes, str], 
              message: Union[bytes, str],
              encoding: str = 'utf-8') -> bytes:
    # TODO: Fix typing on the whole file 
    secret = bytes(secret, encoding) # type: ignore
    message = bytes(message, encoding) # type: ignore
    hashed = hmac.new(secret, message, hashlib.sha256)
    hashed.hexdigest()
    return base64.b64encode(hash.digest())

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

