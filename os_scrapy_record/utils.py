from typing import Type, Union

from idna.core import IDNAError
from scrapy.core.downloader.handlers.http11 import TunnelError
from scrapy.exceptions import IgnoreRequest
from scrapy.http.response import Request, Response
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.defer import CancelledError
from twisted.internet.error import ConnectError, DNSLookupError, TimeoutError
from twisted.python.failure import Failure
from twisted.web._newclient import ParseError, ResponseNeverReceived

from .const import REDIRECT_URLS
from .exceptions import FetchStatusException
from .fetch_status import (
    CANCELED_ACTIVE,
    CONNECT_TIMEOUT_FAILURE,
    DNS_LOOKUP,
    INVALID_URI,
    RESPONSE_NEVER_RECEIVED,
    ROBOTS_TXT,
    TOO_MANNY_REDIR,
    UNKNOW,
    FetchStatus,
    http_fetch_status,
    server_fetch_status,
)


def proc_TunnelError(e):
    try:
        s = str(e)
        if "[" in s and "]" in s:
            r = s[s.find("[") + 1 : s.rfind("]")]
            d = eval(r)
            return http_fetch_status(d["status"])
    except:
        pass
    return UNKNOW


def proc_IgnoreRequest(e):
    e_str = str(e)
    if "Forbidden by robots.txt" in e_str:
        return ROBOTS_TXT
    elif "max redirections reached" in e_str:
        return TOO_MANNY_REDIR

    return UNKNOW


def proc_ParseError(e):
    e_str = str(e)
    if "Unauthorized" in e_str and "401" in e_str:
        return http_fetch_status(401)
    return UNKNOW


def proc_ValueError(e):
    e_str = str(e)
    if "invalid hostname" in e_str:
        return INVALID_URI
    return UNKNOW


def proc_NotSupported(e):
    e_str = str(e)
    if "Unsupported URL scheme" in e_str:
        return INVALID_URI
    return UNKNOW


EXCEPION_TO_FETCH_STATUS = {
    HttpError: lambda e: http_fetch_status(e.response.status),
    FetchStatusException: lambda e: e.fetch_status,
    IDNAError: lambda e: INVALID_URI,
    TimeoutError: lambda e: CONNECT_TIMEOUT_FAILURE,
    DNSLookupError: lambda e: DNS_LOOKUP,
    ResponseNeverReceived: lambda e: RESPONSE_NEVER_RECEIVED,
    CancelledError: lambda e: CANCELED_ACTIVE,
    TunnelError: proc_TunnelError,
    IgnoreRequest: proc_IgnoreRequest,
    ParseError: proc_ParseError,
    ValueError: proc_ValueError,
}


def failure_to_status(failure: Failure) -> FetchStatus:
    return exception_to_status(failure.value)


def exception_to_status(exception: Type[Exception]) -> FetchStatus:
    s = UNKNOW
    if isinstance(exception, ConnectError):
        s = server_fetch_status(exception.osError)
    if s is UNKNOW:
        s = EXCEPION_TO_FETCH_STATUS.get(type(exception), lambda e: UNKNOW)(exception)
    return s


def response_to_status(response: Type[Response]) -> FetchStatus:
    return http_fetch_status(response.status)


def origin_url(request_or_response: Union[Request, Response]) -> str:
    url = request_or_response.url
    if REDIRECT_URLS in request_or_response.meta:
        url = request_or_response.meta[REDIRECT_URLS][0]
    return url
