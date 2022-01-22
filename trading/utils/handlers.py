from requests import request, Response
import time
import hashlib
import hmac
import base64
import re
from functools import lru_cache
from typing import Any, Dict, Union, Optional
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
    debug: bool = False
) -> Union[Response, Any, Dict]:
    if timer | retries < 0:
        raise ValueError("Values for timer or retries have to be greater than zero!")
    r = {}
    try:
        message = re.search(r"\?([\s\S]*)$", endpoint)
        if secret is not None:
            sig = signature(secret, message.group(1))
            endpoint = endpoint + f"&signature={sig}"
        header = {}
        if api_key is not None:
            header["X-MBX-APIKEY"] = api_key
        r = request(method, endpoint, headers=header)
        status = r.status_code
        if status != 200:
            r.raise_for_status()
        r = r.json()
    except HTTPError as err:
        match status:
            # TODO: Add mechanism to update api_key in case of invalidated api_key
            case 429 | 403 | 418:
                if retries != 0:
                    print(f"\n\r{err} : Retries = {retries}... Sleeping for {round(timer, 2)}s")
                    time.sleep(timer)
                    timer += 5
                    retries -= 1
                    api_handler(method, endpoint, api_key, secret, timer, retries)
            case _:# TODO : Add shortcircuit in case of 500 errors 
                print(f"\n{status} Server probably down...")
                time.sleep(timer)
                return r if debug else api_handler(method, endpoint, api_key, secret, timer)
    finally:
        return r


def signature(
    secret: Union[bytes, str], message: Union[bytes, str], encoding: str = "utf-8"
) -> bytes:
    secret = bytes(secret, encoding)
    message = bytes(message, encoding)
    hashed = hmac.new(secret, message, hashlib.sha256)
    hashed.hexdigest()
    return base64.b64encode(hashed.digest())
