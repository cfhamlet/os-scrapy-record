from typing import Type, Union

from scrapy.exceptions import IgnoreRequest
from scrapy.http.response import Request, Response
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.defer import CancelledError
from twisted.internet.error import (
    ConnectionRefusedError,
    DNSLookupError,
    TCPTimedOutError,
    TimeoutError,
)
from twisted.python.failure import Failure
from twisted.web._newclient import ResponseNeverReceived

from .const import REDIRECT_URLS
from .exceptions import FetchStatusException
from .fetch_status import (
    CANCELED_ACTIVE,
    CONNECT_TIMEOUT_FAILURE,
    CONNECTION_REFUSED,
    CONNECTION_TIMEOUT,
    DNS_LOOKUP,
    RESPONSE_NEVER_RECEIVED,
    ROBOTS_TXT,
    UNKNOW,
    FetchStatus,
    Group,
    http_fetch_status,
)

EXCEPION_TO_FETCH_STATUS = {
    HttpError: lambda e: http_fetch_status(e.response.status),
    FetchStatusException: lambda e: e.fetch_status,
    TCPTimedOutError: lambda e: CONNECTION_TIMEOUT,
    TimeoutError: lambda e: CONNECT_TIMEOUT_FAILURE,
    ConnectionRefusedError: lambda e: CONNECTION_REFUSED,
    DNSLookupError: lambda e: DNS_LOOKUP,
    ResponseNeverReceived: lambda e: RESPONSE_NEVER_RECEIVED,
    CancelledError: lambda e: CANCELED_ACTIVE,
    IgnoreRequest: lambda e: ROBOTS_TXT
    if "Forbidden by robots.txt" in str(e)
    else UNKNOW,
}


def failure_to_status(failure: Failure) -> FetchStatus:
    return exception_to_status(failure.value)


def exception_to_status(exception: Type[Exception]) -> FetchStatus:
    eType = type(exception)
    return EXCEPION_TO_FETCH_STATUS.get(eType, lambda e: UNKNOW)(exception)


def response_to_status(response: Type[Response]) -> FetchStatus:
    return http_fetch_status(response.status)


def origin_url(request_or_response: Union[Request, Response]) -> str:
    url = request_or_response.url
    if REDIRECT_URLS in request_or_response.meta:
        url = request_or_response.meta[REDIRECT_URLS][0]
    return url
