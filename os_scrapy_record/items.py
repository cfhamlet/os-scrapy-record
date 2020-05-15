# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import copy
from typing import Optional, Type

import scrapy
from scrapy.http.response import Response
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.python.failure import Failure

from .const import REDIRECT_URLS
from .fetch_status import FetchStatus
from .utils import failure_to_status, origin_url, response_to_status


class RequestItem(scrapy.Item):
    url = scrapy.Field()
    method = scrapy.Field()
    headers = scrapy.Field()


class ResponseItem(scrapy.Item):
    headers = scrapy.Field()
    body = scrapy.Field(serializer=lambda x: x)
    status = scrapy.Field()
    ip_address = scrapy.Field()
    failure = scrapy.Field(serializer=lambda x: repr(x))


class FetchRecord(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    request = scrapy.Field()
    meta = scrapy.Field()
    response = scrapy.Field()


class FetchRecords(scrapy.Item):
    records = scrapy.Field()


def fetch_record(
    response: Optional[Type[Response]] = None,
    failure: Optional[Failure] = None,
    status: Optional[FetchStatus] = None,
) -> FetchRecord:
    req = res = request = None

    if failure is None:
        if response is not None:
            request = response.request
    else:
        request = failure.request
        if failure.check(HttpError):
            response = failure.value.response

    assert request is not None

    req = RequestItem(
        url=origin_url(request), method=request.method, headers=request.headers
    )

    meta = copy.deepcopy(request.meta)
    if REDIRECT_URLS in meta:
        meta[REDIRECT_URLS].append(response.url)
        meta[REDIRECT_URLS] = meta[REDIRECT_URLS][1:]

    if response:
        ip_address = None
        if hasattr(response, "ip_address"):
            ip_address = str(response.ip_address)  # add: Scrapy 2.1.0
        res = ResponseItem(
            headers=response.headers,
            body=response.body,
            ip_address=ip_address,
            status=response_to_status(response),
            failure=failure,
        )
    else:
        res = ResponseItem(status=failure_to_status(failure), failure=failure)

    return FetchRecord(request=req, response=res, meta=meta)
