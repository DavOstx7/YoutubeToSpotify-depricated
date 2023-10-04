import time
import requests
import functools
from python.core.logger import logger
from typing import List, Callable

try:
    from typing import ParamSpec
except ImportError:
    from typing_extensions import ParamSpec

P = ParamSpec("P")


class StatusCodes:
    OK = 200
    CREATED = 201


def validate_response(response: requests.Response, expected_status_codes: List[int], log_responses: bool = False):
    request_endpoint = f"{response.request.method} {response.request.url}"
    if response.status_code in expected_status_codes:
        if log_responses:
            logger.debug(f"Received expected response ({response.status_code}) from {request_endpoint}")
    else:
        logger.error(f"Received unexpected response ({response.status_code}) from {request_endpoint}\n{response.text}")
        logger.critical("Exiting...")
        exit()


def http_request(expected_status_codes: List[int], wait_time: float = 0.2, log_responses: bool = False):
    def decorator(func: Callable[[P], requests.Response]) -> Callable[[P], dict]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> dict:
            response: requests.Response = func(*args, **kwargs)
            validate_response(response, expected_status_codes=expected_status_codes, log_responses=log_responses)
            if wait_time > 0:
                time.sleep(wait_time)
            return response.json()

        return wrapper

    return decorator
