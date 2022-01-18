from requests import request, Response
import hashlib
import hmac
import base64
import re
from functools import lru_cache
from typing import Any, Dict, Union, Optional
from time import time
from requests.exceptions import HTTPError

__all__ = ["api_handler", "signature"]


@lru_cache(maxsize=2)
def api_handler(
    method: str,
    endpoint: str,
    api_key: Optional[str] = None,
    secret: Optional[str] = None,
    timer: int = 5,
    retries: int = 5,
) -> Union[Response, Any, Dict]:
    r = {}
    try:
        message = re.search(r"\?([\s\S]*)$", endpoint)
        if secret is not None:
            sig = signature(secret, message.group(1))  # type: ignore
            endpoint = endpoint + f"&signature={sig}"
        header = {}
        if api_key is not None:
            header["X-MBX-APIKEY"] = api_key
        r = request(method, endpoint, headers=header)
        r = r.json()
        if r.status_code != 200:
            r.raise_for_status()
    except HTTPError as err:
        if r.status_code == 429 and retries != 0:  # type: ignore
            print("\n\r{} API Response: {}... {}secs".format(err, r.status_code, round(timer, 2)))  # type: ignore
            time.sleep(timer)
            timer += 5
            retries -= 1
            return api_handler(method, endpoint, api_key, secret, timer, retries)
        elif r.status_code == 403:  # type: ignore
            print("\n{} Sleeping... ".format(r.status_code))  # type: ignore
            return api_handler(method, endpoint, api_key, secret, timer)
        elif r.status_code == 418:  # type: ignore
            print("\n{} API Key Banned!")
            time.sleep(3600)
            return api_handler(method, endpoint, api_key, secret, timer)
        # 5xx: Server side errors
        elif str(r.status_code).startswith("5"):  # type: ignore
            print("\n{} Binance probably down...".format(r.status_code))  # type: ignore
            time.sleep(3600)
            return api_handler(method, endpoint, api_key, secret, timer)
    finally:
        return r


def signature(
    secret: Union[bytes, str], message: Union[bytes, str], encoding: str = "utf-8"
) -> bytes:
    # TODO: Fix typing on the whole file
    secret = bytes(secret, encoding)  # type: ignore
    message = bytes(message, encoding)  # type: ignore
    hashed = hmac.new(secret, message, hashlib.sha256)
    hashed.hexdigest()
    return base64.b64encode(hash.digest())
