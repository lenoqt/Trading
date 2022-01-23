import base64
import hashlib
import hmac
import re
import time
from functools import lru_cache
from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

from requests import request
from requests import Response
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
    debug: bool = False,
) -> Union[Response, Any, Dict]:
    """
    The api_handler function is used to handle the requests made to the Binance API and several others API.
    It takes in a method, endpoint and api_key as arguments. The method can be either GET or POST.
    The endpoint is the url that you want to make a request on and api_key is your personal API.

    :param method:str: Used to specify the HTTP method used to query the API.
    :param endpoint:str: Used to specify the endpoint of the API.
    :param api_key:Optional[str]=None: Used to pass an api_key to the function.
    :param secret:Optional[str]=None: Used to pass the secret key to the function.
    :param timer:int=5: Used to define the time to sleep between retries.
    :param retries:int=5: Used to define the number of retries in case of 429 or 403 errors.
    :param debug:bool=False: Used to print the response in case of an error.
    :param : Used to pass the api_key and secret to the function.
    :return: the response of the request, if it is successful.
    """
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
                    print(
                        f"\n\r{err} : Retries = {retries}... Sleeping for {round(timer, 2)}s"
                    )
                    time.sleep(timer)
                    timer += 5
                    retries -= 1
                    api_handler(method, endpoint, api_key, secret, timer, retries)
            case _:  # TODO : Add shortcircuit in case of 500 errors
                print(f"\n{status} Server probably down...")
                time.sleep(timer)
                return (
                    r
                    if debug
                    else api_handler(method, endpoint, api_key, secret, timer)
                )
    finally:
        return r


def signature(
    secret: Union[bytes, str], message: Union[bytes, str], encoding: str = "utf-8"
) -> bytes:
    """
    The signature function takes the secret key and message as arguments. It then hashes the message using
    the secret key, which is a combination of both strings. The output is in bytes.

    :param secret:Union[bytes: Used to pass a secret key to the function.
    :param str]: Used to specify the encoding of the secret and message.
    :param message:Union[bytes: Used to accept either a string or bytes object.
    :param str]: Used to specify the type of data that is being passed into the function.
    :param encoding:str="utf-8": Used to specify the encoding of the secret and message.
    :return: a string containing the hash value of a message.
    """
    secret = bytes(secret, encoding)
    message = bytes(message, encoding)
    hashed = hmac.new(secret, message, hashlib.sha256)
    hashed.hexdigest()
    return base64.b64encode(hashed.digest())
