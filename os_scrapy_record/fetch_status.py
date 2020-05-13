import enum
from enum import IntEnum
from http import HTTPStatus
from typing import NamedTuple, Union


@enum.unique
class Group(IntEnum):
    UNKNOW = -1
    RESERVED = 0
    HTTP = 1
    SSL = 2
    SERVER = 3
    DNS = 4
    RULE = 5
    CANCELED = 6


@enum.unique
class Server(IntEnum):
    CONNECT_ERROR = 2
    RESPONSE_FAILED = 4
    RESPONSE_NEVER_RECEIVED = 5
    CONNECTION_TIMEOUT = 110
    CONNECTION_REFUSED = 111


@enum.unique
class DNS(IntEnum):
    LOOKUP_ERROR = -2


@enum.unique
class Rule(IntEnum):
    NO_SSL_CTX = 1
    FILE_TYPE = 2
    DOMAIN_FILTERED = 3
    URL_PREFIX_FILTERED = 4
    DUPLICATION = 5
    INVALID_URI = 6
    NO_HOST_INFO = 7
    TOO_MANNY_REDIR = 8
    NO_REDIR = 9
    URL_TOO_LONG = 10
    ERROR_REDIR = 11
    INVALID_PAGE = 12
    URLTYPE_DISALLOWED = 13
    SUBDOMAIN_EXCEED = 14
    INVALID_PAGESIZE = 15
    ROBOTS_TXT = 16
    URL_REGEX_FILTERED = 17
    IP_FILTERED = 18
    DEPTH_EXCEED = 19
    TOO_MANY_URL = 20
    UNFETCH_SUCCESS_RESULT = 21
    INSIGNIFICANT_PAGE = 22
    TRANSFORM_FILTERED = 23
    SIZE_EXCEED = 24
    URL_REGEX_FILTERED_DELETE_REDIRECT = 25
    URL_DELIVER_REQUEST_FAILED = 26
    INVALID_HEADER = 27
    CANCELED_RCV_TASK = 28
    DNS_SUBMIT_FAIL = 29
    UNKNOW_SCHDULE_UNIT = 30
    CANCELED_ACTIVE = 31
    PADDING_TIMEOUT = 32
    INVALID_TASK = 33
    NO_MEMORY = 34
    PAGESIZE_NOCHANGE = 35
    CANCELED_INFERENCE = 41
    CONNECT_TIMEOUT_FAILURE = 51


SERVER_NUMBERS = set(list(Server))
DNS_NUMBERS = set(list(DNS))
RULE_NUMBERS = set(list(Rule))

_TRANS_DICT = {
    Group.UNKNOW: lambda x: x,
    Group.RESERVED: lambda x: x,
    Group.HTTP: lambda x: x,
    Group.SSL: lambda x: x,
    Group.SERVER: lambda x: Server(x).name if x in SERVER_NUMBERS else x,
    Group.DNS: lambda x: DNS(x).name if x in DNS_NUMBERS else x,
    Group.RULE: lambda x: Rule(x).name if x in RULE_NUMBERS else x,
}


class FetchStatus(NamedTuple):
    group: int
    code: int

    def __str__(self):
        g = self.group
        c = self.code
        if self.group in _TRANS_DICT:
            c = _TRANS_DICT[self.group](self.code)
            g = Group(self.group).name
        return f"{g}:{c}"

    def __repr__(self):
        return str(self)


def fetch_status(
    group: Union[int, Group], code: Union[int, Server, DNS, Rule]
) -> FetchStatus:
    g = group.value if isinstance(group, Group) else group
    c = code.value if isinstance(code, IntEnum) else code
    return FetchStatus(g, c)


HTTP_FETCH_STATUS = dict(
    [(status.value, fetch_status(Group.HTTP, status.value)) for status in HTTPStatus]
)


def http_fetch_status(code: int) -> FetchStatus:
    if code in HTTP_FETCH_STATUS:
        return HTTP_FETCH_STATUS[code]
    return fetch_status(Group.HTTP, code)


OK = fetch_status(Group.HTTP, 200)
UNKNOW = fetch_status(Group.UNKNOW, -1)
CONNECTION_TIMEOUT = fetch_status(Group.SERVER, Server.CONNECTION_TIMEOUT)
CONNECTION_REFUSED = fetch_status(Group.SERVER, Server.CONNECTION_REFUSED)
DNS_LOOKUP = fetch_status(Group.DNS, DNS.LOOKUP_ERROR)
RESPONSE_NEVER_RECEIVED = fetch_status(Group.SERVER, Server.RESPONSE_NEVER_RECEIVED)
CANCELED_ACTIVE = fetch_status(Group.RULE, Rule.CANCELED_ACTIVE)
ROBOTS_TXT = fetch_status(Group.RULE, Rule.ROBOTS_TXT)
CONNECT_TIMEOUT_FAILURE = fetch_status(Group.RULE, Rule.CONNECT_TIMEOUT_FAILURE)
