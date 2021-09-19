import requests
import json
from requests.exceptions import HTTPError
from typing import Dict, Any, Union
from time import time

__all__ = ['api_handler']

def api_handler(url: str,
                api_key: str, 
                timer:int=5, 
                retries:int=5) -> Union[requests.Response, Any, Dict]:
    r = {}
    try:
        r = requests.get(url, headers={'X-MBX-APIKEY': api_key})
        r = r.json()
        r = json.loads(r)
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
