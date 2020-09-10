# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import copy
from typing import Type, Union

import scrapy
from scrapy.http.response import Response
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.python.failure import Failure

from .const import REDIRECT_URLS
from .utils import failure_to_status, origin_url, response_to_status


class RequestItem(scrapy.Item):
    url = scrapy.Field()
    method = scrapy.Field()
    headers = scrapy.Field()
    body = scrapy.Field()


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
    response: Union[Type[Response], Failure],
) -> FetchRecord:
    req = res = request = failure = None

    if isinstance(response, Failure):
        failure = response
        request = failure.request
        if failure.check(HttpError):
            response = failure.value.response
        else:
            response = None
    else:
        request = response.request

    assert request is not None

    req = RequestItem(
        url=origin_url(request),
        method=request.method,
        headers=request.headers,
        body=request.body,
    )

    meta = copy.deepcopy(request.meta)
    if REDIRECT_URLS in meta:
        meta[REDIRECT_URLS].append(request.url)
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
