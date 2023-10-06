import httpx
import functools
from typing import List, Callable, Awaitable
from python.core.exception import ResponseError
from python.core.logger import logger

try:
    from typing import ParamSpec
except ImportError:
    from typing_extensions import ParamSpec

P = ParamSpec("P")


class StatusCodes:
    OK = 200
    CREATED = 201


def validate_response(response: httpx.Response, expected_status_codes: List[int], log_responses: bool = False):
    request_endpoint = f"{response.request.method} {response.request.url}"
    if response.status_code in expected_status_codes:
        if log_responses:
            logger.debug(f"Received expected response ({response.status_code}) from {request_endpoint}")
    else:
        msg = f"Received unexpected response ({response.status_code}) from {request_endpoint}\n{response.text}"
        raise ResponseError(msg)


def http_request(expected_status_codes: List[int], log_responses: bool = False):
    def decorator(func: Callable[[P], Awaitable[httpx.Response]]) -> Callable[[P], Awaitable[dict]]:
        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> dict:
            response: httpx.Response = await func(*args, **kwargs)
            validate_response(response, expected_status_codes=expected_status_codes, log_responses=log_responses)
            return response.json()

        return wrapper

    return decorator
